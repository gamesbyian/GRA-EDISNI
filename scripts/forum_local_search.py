#!/usr/bin/env python3
"""Offline forum-corpus ingest/search: SQLite FTS5, optional warcio WARC/ARC reader.

No crawling, web requests, API credentials or external model calls.
Inputs must be locally obtained, publicly usable/authorized research material.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sqlite3
import sys
from urllib.parse import urlsplit

MAX_TEXT = 2_000_000

class VisibleText(HTMLParser):
    """Recall-oriented text extraction: retain all visible forum replies.

    This is not a reliable post/author/date parser. Treat output as page text.
    """
    BLOCKED = {"script", "style", "svg", "noscript", "template"}
    SEPARATORS = {"p", "div", "article", "section", "li", "br", "tr", "h1", "h2", "h3"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.blocked = 0
    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCKED:
            self.blocked += 1
        if tag in self.SEPARATORS and not self.blocked:
            self.parts.append("\n")
        if tag == "img" and not self.blocked:
            attr = dict(attrs)
            if attr.get("alt"):
                self.parts.append(" [image alt: " + attr["alt"] + "] ")
    def handle_endtag(self, tag):
        if tag in self.BLOCKED and self.blocked:
            self.blocked -= 1
        if tag in self.SEPARATORS and not self.blocked:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.blocked and data.strip():
            self.parts.append(data)
    def text(self) -> str:
        return "\n".join(x.strip() for x in "".join(self.parts).splitlines()
                         if x.strip())

def html_to_text(html: str) -> str:
    parser = VisibleText()
    parser.feed(html)
    parser.close()
    return parser.text()

def connection(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    db.execute("""CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        forum TEXT NOT NULL DEFAULT '',
        url TEXT NOT NULL,
        host TEXT NOT NULL,
        title TEXT NOT NULL DEFAULT '',
        text TEXT NOT NULL,
        fold_text TEXT NOT NULL,
        language TEXT NOT NULL DEFAULT '',
        source_kind TEXT NOT NULL,
        captured_at TEXT NOT NULL DEFAULT '',
        original_post_date TEXT NOT NULL DEFAULT '',
        source_collection TEXT NOT NULL DEFAULT '',
        content_sha256 TEXT NOT NULL,
        UNIQUE(url, captured_at, source_kind, content_sha256)
    )""")
    try:
        db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS forum_tri USING fts5(
            fold_text, content='documents', content_rowid='id', tokenize='trigram'
        )""")
        db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS forum_terms USING fts5(
            text, content='documents', content_rowid='id', tokenize='unicode61'
        )""")
    except sqlite3.OperationalError as exc:
        raise RuntimeError("This Python's SQLite requires FTS5 and the trigram tokenizer") from exc
    db.executescript("""
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO forum_tri(rowid, fold_text) VALUES (new.id, new.fold_text);
            INSERT INTO forum_terms(rowid, text) VALUES (new.id, new.text);
        END;
        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO forum_tri(forum_tri, rowid, fold_text)
                VALUES('delete', old.id, old.fold_text);
            INSERT INTO forum_terms(forum_terms, rowid, text)
                VALUES('delete', old.id, old.text);
        END;
    """)
    return db

def add_document(db: sqlite3.Connection, record: dict) -> bool:
    url = record.get("url", "")
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.netloc:
        raise ValueError("Document needs its original HTTP(S) URL")
    body = record.get("text", "")
    title = record.get("title", "")
    if not isinstance(body, str) or not body.strip():
        raise ValueError("Document needs nonempty text")
    if not isinstance(title, str):
        raise ValueError("Document title must be text")
    if len(body) > MAX_TEXT:
        raise ValueError("Document exceeds 2-million-character safety limit")
    text = (title + "\n" if title else "") + body
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    source_kind = record.get("source_kind", "provided_text")
    if source_kind not in {"warc_capture", "provided_text", "verified_thread", "index_snippet"}:
        raise ValueError("Unrecognized source_kind")
    cur = db.execute("""INSERT OR IGNORE INTO documents
        (forum, url, host, title, text, fold_text, language,
         source_kind, captured_at, original_post_date, source_collection, content_sha256)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (record.get("forum", ""), url, parts.netloc.lower(), title, text,
         text.casefold(), record.get("language", ""), source_kind,
         record.get("captured_at", ""), record.get("original_post_date", ""),
         record.get("source_collection", ""), digest))
    return cur.rowcount == 1

def ingest_jsonl(db: sqlite3.Connection, path: Path) -> dict:
    stats = {"attempted": 0, "inserted": 0, "duplicates": 0, "errors": 0}
    with path.open(encoding="utf-8") as fh, db:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            stats["attempted"] += 1
            try:
                obj = json.loads(line)
                if not isinstance(obj, dict):
                    raise ValueError("Expected object")
                if add_document(db, obj):
                    stats["inserted"] += 1
                else:
                    stats["duplicates"] += 1
            except (ValueError, TypeError, sqlite3.Error) as exc:
                stats["errors"] += 1
                print(f"{path}:{line_no}: {type(exc).__name__}: {exc}", file=sys.stderr)
    return stats

def ingest_warc(db: sqlite3.Connection, path: Path, max_records: int) -> dict:
    try:
        from warcio.archiveiterator import ArchiveIterator
    except ImportError as exc:
        raise RuntimeError("WARC ingestion requires: python -m pip install warcio") from exc
    stats = {"attempted": 0, "inserted": 0, "duplicates": 0, "skipped": 0}
    with path.open("rb") as fh, db:
        for rec in ArchiveIterator(fh, arc2warc=True):
            if stats["attempted"] >= max_records:
                break
            if rec.rec_type != "response" or rec.http_headers is None:
                continue
            stats["attempted"] += 1
            ctype = rec.http_headers.get_header("Content-Type") or ""
            status = rec.http_headers.get_statuscode()
            if not status or not status.startswith("2") or "html" not in ctype.lower():
                stats["skipped"] += 1
                continue
            url = rec.rec_headers.get_header("WARC-Target-URI") or ""
            if urlsplit(url).scheme not in ("http", "https"):
                stats["skipped"] += 1
                continue
            raw = rec.content_stream().read(MAX_TEXT * 4 + 1)
            if len(raw) > MAX_TEXT * 4:
                stats["skipped"] += 1
                continue
            import re
            charset = re.search(r"charset=([-\w]+)", ctype, re.I)
            encoding = charset.group(1) if charset else "utf-8"
            try:
                page = raw.decode(encoding, errors="replace")
            except LookupError:
                page = raw.decode("utf-8", errors="replace")
            extracted = html_to_text(page)
            if not extracted or len(extracted) > MAX_TEXT:
                stats["skipped"] += 1
                continue
            record = {
                "url": url, "text": extracted, "source_kind": "warc_capture",
                "captured_at": rec.rec_headers.get_header("WARC-Date") or "",
                "source_collection": str(path),
            }
            if add_document(db, record):
                stats["inserted"] += 1
            else:
                stats["duplicates"] += 1
    return stats

def snippet(text: str, needle: str, ignore_case: bool) -> str:
    # casefold length can differ from original: locate conservatively.
    pos = text.casefold().find(needle.casefold()) if ignore_case else text.find(needle)
    start = max(0, pos - 90) if pos >= 0 else 0
    return text[start : start + 270].replace("\n", " ")

def search(db: sqlite3.Connection, term: str, *, mode: str = "exact",
           ignore_case: bool = False, host: str = "", limit: int = 100) -> dict:
    if not term:
        raise ValueError("Empty term")
    if limit < 1 or limit > 1000:
        raise ValueError("Limit must be 1..1000")
    where, params = [], []
    if mode == "exact":
        if len(term.casefold()) >= 3 and "%" not in term and "_" not in term:
            where.append("tri.fold_text LIKE ?")
            params.append("%" + term.casefold() + "%")
            join = "JOIN forum_tri tri ON tri.rowid = d.id"
        else:
            join = ""
        if ignore_case:
            where.append("instr(d.fold_text, ?) > 0")
            params.append(term.casefold())
        else:
            where.append("instr(d.text, ?) > 0")
            params.append(term)
    elif mode == "phrase":
        join = "JOIN forum_terms tok ON tok.rowid = d.id"
        where.append("tok.text MATCH ?")
        params.append('"' + term.replace('"', '""') + '"')
    else:
        raise ValueError("Unknown search mode")
    if host:
        where.append("d.host = ?")
        params.append(host.lower())
    sql = """SELECT d.id,d.forum,d.url,d.host,d.title,d.text,d.language,
                    d.source_kind,d.captured_at,d.original_post_date,
                    d.source_collection,d.content_sha256
             FROM documents d """ + join + " WHERE " + " AND ".join(where) + (
                 " ORDER BY d.id LIMIT ?"
             )
    try:
        results = db.execute(sql, params + [limit + 1]).fetchall()
    except sqlite3.OperationalError as exc:
        raise ValueError("Invalid query or search index unavailable") from exc
    names = ["id","forum","url","host","title","text","language","source_kind",
             "captured_at","original_post_date","source_collection","content_sha256"]
    docs = []
    for row in results[:limit]:
        item = dict(zip(names, row))
        text = item.pop("text")
        item["snippet"] = snippet(text, term, ignore_case)
        item["scope"] = "offline_ingested_corpus_only"
        docs.append(item)
    return {"term": term, "mode": mode, "ignore_case": ignore_case,
            "host": host, "hits_shown": len(docs), "truncated": len(results) > limit,
            "coverage": "only_documents_present_in_local_database",
            "matches": docs}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    load = commands.add_parser("ingest-jsonl")
    load.add_argument("--input", type=Path, required=True)
    warc = commands.add_parser("ingest-warc")
    warc.add_argument("--input", type=Path, required=True)
    warc.add_argument("--max-records", type=int, default=10000)
    query = commands.add_parser("search")
    query.add_argument("--term", action="append", default=[])
    query.add_argument("--terms-file", type=Path)
    query.add_argument("--mode", choices=["exact", "phrase"], default="exact")
    query.add_argument("--ignore-case", action="store_true")
    query.add_argument("--host", default="")
    query.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    db = connection(args.db)
    try:
        if args.command == "ingest-jsonl":
            result = ingest_jsonl(db, args.input)
        elif args.command == "ingest-warc":
            result = ingest_warc(db, args.input, args.max_records)
        else:
            terms = list(args.term)
            if args.terms_file:
                terms += [line.strip() for line in args.terms_file.read_text(
                    encoding="utf-8").splitlines() if line.strip()]
            if not terms:
                parser.error("Search requires --term or --terms-file")
            result = [search(db, term, mode=args.mode, ignore_case=args.ignore_case,
                             host=args.host, limit=args.limit) for term in dict.fromkeys(terms)]
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        db.close()

if __name__ == "__main__":
    main()

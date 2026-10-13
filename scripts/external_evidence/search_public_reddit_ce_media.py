#!/usr/bin/env python3
"""Cross-community public INSIDE CE search over Arctic Shift's bounded Reddit archive API.

No Reddit login, account profiling, owner outreach, private data, general web crawling
or physical-sticker promotion. Search hits require primary media/context review.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_HOST = "arctic-shift.photon-reddit.com"
MAX_BYTES = 7 * 1024 * 1024
ALLOWED_IMAGES = {"i.redd.it", "preview.redd.it", "i.imgur.com",
                  "pbs.twimg.com", "i.ebayimg.com"}
GALLERY_HOSTS = {"imgur.com", "www.imgur.com", "flickr.com", "www.flickr.com",
                 "postimg.cc", "ibb.co", "www.ebay.com", "www.mercari.com"}
URL_RE = re.compile(r"https?://[^\s\]\[()<>\"']+", re.I)
POST_RE = re.compile(r"(?:reddit\.com/(?:r/[^/]+/)?comments/)([a-z0-9]{5,9})", re.I)
IMGUR_RE = re.compile(r"(?:imgur\.com/(?:gallery|a)/)([A-Za-z0-9]+)", re.I)
CE_ANCHORS = ("iam8bit", "real doll", "realdoll", "playdead", "huddle")
PURCHASE = ("got mine", "i bought", "i purchased", "i received", "arrived",
            "i have the", "selling", "for sale", "shipped", "unbox", "my copy",
            "my collector", "i own", "received my", "pickup", "my ce")
STICKERS = ("sticker", "adhesive", "seal", "numbered", "serial", "wrapper",
            "symbol", "slash", "dash")
IGNORE = ("[deleted]", "[removed]")


def valid_media(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        return ""
    if parsed.hostname.lower() in ALLOWED_IMAGES | GALLERY_HOSTS:
        return url
    return ""


def media_urls(item: dict) -> tuple[list[str], list[str]]:
    found = set()
    for key in ("url", "url_overridden_by_dest"):
        if isinstance(item.get(key), str):
            found.add(html.unescape(item[key]))
    body = str(item.get("selftext") or item.get("body") or "")
    for raw in URL_RE.findall(html.unescape(body)):
        found.add(raw.rstrip(".,!?:;}>"))
    preview = item.get("preview") or {}
    if isinstance(preview, dict):
        for img in preview.get("images", []):
            if isinstance(img, dict) and isinstance(img.get("source"), dict):
                found.add(html.unescape(str(img["source"].get("url", ""))))
    if isinstance(item.get("media_metadata"), dict):
        for meta in item["media_metadata"].values():
            if isinstance(meta, dict) and isinstance(meta.get("s"), dict):
                found.add(html.unescape(str(meta["s"].get("u", ""))))
    accepted = sorted(filter(None, (valid_media(u) for u in found)))
    direct = [u for u in accepted if urllib.parse.urlparse(u).hostname.lower() in ALLOWED_IMAGES]
    gallery = [u for u in accepted if u not in direct]
    return direct, gallery


def relevant(item: dict) -> bool:
    sample = " ".join(str(item.get(k) or "") for k in ("title", "selftext", "body")).lower()
    if sample.strip().startswith(IGNORE):
        return False
    if any(anchor in sample for anchor in CE_ANCHORS):
        return True
    return "inside" in sample and ("collector" in sample or "collectors" in sample) and (
        "edition" in sample or "ce " in sample or "huddle" in sample
    )


def score_item(item: dict, direct: list[str], galleries: list[str]) -> int:
    sample = " ".join(str(item.get(k) or "") for k in ("title", "selftext", "body")).lower()
    return (5 * bool(direct) + 4 * bool(galleries) +
            2 * any(v in sample for v in PURCHASE) +
            3 * any(v in sample for v in STICKERS) +
            2 * ("realdoll" in sample or "real doll" in sample) +
            1 * ("iam8bit" in sample))


def known_url_evidence(path: Path) -> dict[str, set[str]]:
    """Exact link matching only. No person/serial inferred from incomplete archive."""
    raw = path.read_text(encoding="utf-8") if path.is_file() else ""
    return {
        "reddit": set(x.lower() for x in POST_RE.findall(raw)),
        "imgur": set(x.lower() for x in IMGUR_RE.findall(raw)),
    }


def curated_case_map(path: Path) -> dict[str, str]:
    """Exact source ID whitelist, explicitly curated from known public case ledgers."""
    if not path.is_file():
        return {}
    entries = json.loads(path.read_text(encoding="utf-8")).get("sources", [])
    result = {}
    for item in entries:
        post_id = item.get("reddit_post_id")
        if not post_id:
            continue
        if not re.fullmatch(r"[a-z0-9]{5,9}", str(post_id), re.I):
            raise ValueError("invalid curated public post ID")
        case_ref = item.get("case_ref")
        if not isinstance(case_ref, str) or not re.fullmatch(r"(?:U\d{1,3}|L\d{1,3}|[/.-]\d{3})", case_ref):
            raise ValueError("invalid curated case reference")
        if post_id.lower() in result:
            raise ValueError("duplicate curated post ID")
        result[post_id.lower()] = case_ref
    return result


def known_status(record: dict, known: dict[str, set[str]]) -> str:
    case_ref = known.get("case_by_post_id", {}).get(record["post_id"].lower())
    if case_ref:
        return "existing-curated-case-" + case_ref
    if record["post_id"].lower() in known["reddit"]:
        return "post-id-present-in-known-ledger"
    for url in record["direct_image_urls"] + record["gallery_urls"]:
        match = IMGUR_RE.search(url)
        if match and match.group(1).lower() in known["imgur"]:
            return "imgur-gallery-present-in-known-ledger"
    return "unreconciled-by-exact-url"


CE_CONTEXT = ("iam8bit", "real doll", "realdoll", "inside collector",
              "inside ce", "huddle", "playdead")
FALLBACK_CONTEXT = ("collector", "inside", "sticker")


def relevant_excerpt(item: dict, limit: int = 320) -> tuple[str, int]:
    """Keep a small source excerpt around CE evidence in lengthy resale lists.

    Character offset belongs to the original post *body*, not a transcript.
    Never mistake a 240-character introductory excerpt for the only CE mention.
    """
    title = re.sub(r"\s+", " ", str(item.get("title") or ""))[:90]
    body = str(item.get("selftext") or item.get("body") or "")
    lower = body.lower()
    positions = [lower.find(term) for term in CE_CONTEXT if term in lower]
    if not positions:
        positions = [lower.find(term) for term in FALLBACK_CONTEXT if term in lower]
    first = min(positions) if positions else 0
    start = max(0, first - 55)
    sample = body[start:start + max(1, limit - len(title) - 10)]
    sample = re.sub(r"\s+", " ", URL_RE.sub("[public URL]", sample))
    excerpt = (title + " | " + ("…" if start else "") + sample).strip()[:limit]
    return excerpt, start


def clean_item(item: dict, kind: str) -> dict | None:
    ident = str(item.get("id") or "").removeprefix("t1_").removeprefix("t3_")
    if not re.fullmatch(r"[a-z0-9]{5,12}", ident, flags=re.I):
        return None
    post_id = ident if kind == "post" else str(item.get("link_id") or "").removeprefix("t3_")
    if not re.fullmatch(r"[a-z0-9]{5,9}", post_id, flags=re.I):
        return None
    if not relevant(item):
        return None
    direct, galleries = media_urls(item)
    page = (f"https://www.reddit.com/comments/{post_id}/"
            if kind == "post" else f"https://www.reddit.com/comments/{post_id}/_/{ident}/")
    sample, excerpt_offset = relevant_excerpt(item)
    return {"id": ident.lower(), "kind": kind, "post_id": post_id.lower(),
            "source_page_url": page, "created_utc": item.get("created_utc"),
            "subreddit": str(item.get("subreddit") or "")[:90],
            "context_excerpt": sample, "excerpt_body_offset": excerpt_offset,
            "score": score_item(item, direct, galleries),
            "direct_image_urls": direct, "gallery_urls": galleries,
            "archived-source-only": True}


def search_url(entry: dict, limit: int) -> str:
    kind = entry["kind"]
    sub = entry["subreddit"]
    term = entry["term"]
    if kind not in {"post", "comment"} or not re.fullmatch(r"[A-Za-z0-9_]{2,35}", sub):
        raise ValueError("invalid source filter")
    if not isinstance(term, str) or not 1 <= len(term) <= 100:
        raise ValueError("invalid search term")
    endpoint = "/api/posts/search" if kind == "post" else "/api/comments/search"
    parameters = {"subreddit": sub, "sort": "asc", "after": "2018-01-01",
                  "before": "2026-10-14", "limit": min(limit, 40),
                  "query" if kind == "post" else "body": term}
    return "https://" + API_HOST + endpoint + "?" + urllib.parse.urlencode(parameters)


class ArchiveHTTPFailure(OSError):
    def __init__(self, code: int, detail: str, retry_after: str = ""):
        super().__init__(f"archive HTTP {code}: {detail[:260]}")
        self.code = code
        self.retry_after = retry_after[:80]


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname != API_HOST:
            raise ValueError("unexpected archive search redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request_json(url: str) -> tuple[dict, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != API_HOST:
        raise ValueError("unapproved archive API host")
    request = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": "GRA-EDISNI-public-CE-photo-search/1.0"
    })
    try:
        response = urllib.request.build_opener(SafeRedirect()).open(request, timeout=25)
    except urllib.error.HTTPError as exc:
        detail = re.sub(r"\s+", " ", exc.read(1200).decode("utf-8", "replace"))
        raise ArchiveHTTPFailure(exc.code, detail,
                                 exc.headers.get("Retry-After", "") if exc.headers else "") from exc
    with response:
        if response.headers.get_content_type() != "application/json":
            raise ValueError("archive response is not JSON")
        blob = response.read(MAX_BYTES + 1)
        if not blob or len(blob) > MAX_BYTES:
            raise ValueError("empty or oversized archive response")
        payload = json.loads(blob)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("unexpected archive search response schema")
        return payload, hashlib.sha256(blob).hexdigest()


def scan(searches: list[dict], known: dict[str, set[str]], requester=request_json,
         per_query: int = 30, max_total: int = 500):
    """Filter hits; do not mistake 'no matches' or archive failure for exhaustive absence."""
    hits: dict[str, dict] = {}
    failures = []
    audit = []
    consecutive_rejections = 0
    stopped_reason = None
    for search in searches:
        sid = search["id"]
        kind = search["kind"]
        if stopped_reason:
            audit.append({"search_id": sid, "status": "not-attempted",
                          "reason": stopped_reason})
            continue
        try:
            url = search_url(search, per_query)
            payload, digest = requester(url)
            rows = payload["data"]
            consecutive_rejections = 0
            if not isinstance(rows, list):
                raise ValueError("response data is not an array")
            matched = 0
            for item in rows[:per_query]:
                if not isinstance(item, dict):
                    continue
                row = clean_item(item, kind)
                if row is None:
                    continue
                matched += 1
                identity = kind + ":" + row["id"]
                if identity in hits:
                    hits[identity]["matched_search_ids"].add(sid)
                    continue
                if len(hits) >= max_total:
                    break
                row["matched_search_ids"] = {sid}
                row["source_status"] = known_status(row, known)
                row["curated_case_ref"] = known.get("case_by_post_id", {}).get(row["post_id"])
                hits[identity] = row
            audit.append({"search_id": sid, "kind": kind, "subreddit": search["subreddit"],
                          "term": search["term"], "status": "ok", "archive_sha256": digest,
                          "returned": len(rows), "relevant": matched,
                          "page_limit": per_query, "possibly_truncated": len(rows) >= per_query})
        except (OSError, ValueError, urllib.error.URLError) as exc:
            error = {"search_id": sid, "status": "unavailable",
                     "reason": str(exc)[:350]}
            if isinstance(exc, ArchiveHTTPFailure):
                error["http_status"] = exc.code
                if exc.retry_after:
                    error["retry_after"] = exc.retry_after
                if exc.code == 429:
                    stopped_reason = "HTTP 429; postponed to a future run (respect Retry-After)"
                elif exc.code == 422:
                    consecutive_rejections += 1
                    if consecutive_rejections >= 3:
                        stopped_reason = "Three consecutive HTTP 422 query rejections; inspect diagnostics before retry"
            audit.append(error)
            failures.append(error)
        if requester is request_json and not stopped_reason:
            time.sleep(1.5)
    records = list(hits.values())
    for r in records:
        r["matched_search_ids"] = sorted(r["matched_search_ids"])
    records.sort(key=lambda r: (-r["score"], r["source_status"] != "unreconciled-by-exact-url",
                                r["created_utc"] or 0, r["source_page_url"]))
    photo = []
    galleries = []
    for record in records:
        for media_url in record["direct_image_urls"]:
            photo.append({"source_id": "archive-"+record["kind"]+"-"+record["id"],
                          "source_page_url": record["source_page_url"],
                          "image_url": media_url,
                          "contexts": [record["context_excerpt"]],
                          "keyword_hints": [], "hint_count": 1,
                          "review_status": "archived-public-media-link-unverified"})
        for gallery_url in record["gallery_urls"]:
            galleries.append({"source_id": "archive-"+record["kind"]+"-"+record["id"],
                              "source_page_url": record["source_page_url"],
                              "gallery_url": gallery_url,
                              "review_status": "gallery-not-retrieved"})
    return records, audit, failures, photo, galleries


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path,
                   default=Path("data/reference/inside-ce-public-reddit-cross-community-queries.json"))
    p.add_argument("--canonical-ledger", type=Path,
                   default=Path("archive/external/twinysam-inside-arg/stickers.md"))
    p.add_argument("--output", type=Path, default=Path("visual-evidence-work/archived-market-discovery"))
    p.add_argument("--curated-known-sales", type=Path,
                   default=Path("data/reference/inside-ce-curated-known-public-sale-links.json"))
    p.add_argument("--max-queries", type=int, default=8)
    p.add_argument("--start-query", type=int, default=0)
    p.add_argument("--per-query", type=int, default=30)
    args = p.parse_args()
    if not 1 <= args.max_queries <= 32 or not 1 <= args.per_query <= 40 or not 0 <= args.start_query < 32:
        p.error("max-queries must be 1..32, per-query 1..40, start-query 0..31")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    selected = manifest["searches"][args.start_query:args.start_query + args.max_queries]
    if len({x["id"] for x in selected}) != len(selected):
        p.error("duplicate query ID in selected manifest")
    known = known_url_evidence(args.canonical_ledger)
    known["case_by_post_id"] = curated_case_map(args.curated_known_sales)
    records, audit, failures, photos, galleries = scan(
        selected, known, per_query=args.per_query,
        max_total=manifest.get("limits", {}).get("max_total_unique_records", 500))
    args.output.mkdir(parents=True, exist_ok=True)
    contents = {
        "search-report.json": {"schema_version": 1, "searches": audit,
                               "failures": failures, "note": "Archive results are non-exhaustive"},
        "review-queue.json": {"schema_version": 1, "candidates": records,
                              "note": "Not independent owners or physical sticker discoveries"},
        "image-leads.json": {"schema_version": 1, "image_mentions": photos},
        "gallery-leads.json": {"schema_version": 1, "galleries": galleries},
    }
    for name, value in contents.items():
        (args.output / name).write_text(json.dumps(value, ensure_ascii=False,
                                                     indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queries": len(selected), "query_failures": len(failures),
                      "candidate_records": len(records), "direct_image_mentions": len(photos),
                      "gallery_mentions": len(galleries),
                      "not_attempted_queries": sum(a["status"] == "not-attempted" for a in audit),
                      "unreconciled_exact_urls": sum(
                          r["source_status"] == "unreconciled-by-exact-url" for r in records)}))


if __name__ == "__main__":
    main()

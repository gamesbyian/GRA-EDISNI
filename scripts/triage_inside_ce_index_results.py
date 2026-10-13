#!/usr/bin/env python3
"""Offline, provenance-conservative triage of licensed web-index CE search hits.

Reads successful results from run_global_forum_index_search.py. Links exact URL
duplicates and topic-level overlap with a known public evidence ledger. Makes NO
CE ownership, distinct-edition, sticker-number or historical completeness claim.
No network requests or external packages.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import re
from urllib.parse import parse_qs, quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/reference/inside-ce-owner-search-ledger-2026-10-12.tsv"
CANONICAL_HINTS = ROOT / "docs/reference/inside-ce-native-owner-hunt-2026-10-12.md"
TRACKING = {"utm_source", "utm_medium", "utm_campaign", "utm_content",
            "utm_term", "fbclid", "gclid", "ref", "share_id", "context"}
REDDIT_HOSTS = {"old.reddit.com", "new.reddit.com", "www.reddit.com",
                "reddit.com", "sh.reddit.com"}
OUTPUT = ("candidate_id", "canonical_url", "thread_key", "evidence_key",
          "first_title", "first_description", "index_hit_occurrences",
          "distinct_query_tasks", "query_languages", "prior_ledger_relation",
          "canonical_relation", "source_relation", "review_warning", "review_status",
          "new_confirmed_stickers")

def normalize_url(raw: str) -> tuple[str, str, str]:
    """Stable source ID, preserving comment-level attribution when available."""
    raw = raw.strip()
    u = urlsplit(raw)
    if u.scheme not in ("https", "http") or not u.hostname:
        raise ValueError("Expected an HTTP(S) search result URL")
    host = u.hostname.lower()
    path = unquote(u.path).rstrip("/")
    if host in REDDIT_HOSTS or host == "redd.it":
        if host == "redd.it":
            match = re.fullmatch(r"/([a-z0-9]+)", path, re.I)
            if match:
                tid = match.group(1).lower()
                return "https://www.reddit.com/comments/" + tid, "reddit:" + tid, "reddit:" + tid
        host = "www.reddit.com"
        m = re.search(r"/comments/([a-z0-9]+)(?=/|$)", path, re.I)
        if m:
            tid = m.group(1).lower()
            rest = [p for p in path[m.end():].split("/") if p]
            # Reddit permalinks use both /comments/TID/title/CID and
            # /comments/TID/comment/CID; preserve comment IDs when present.
            cid = ""
            if len(rest) >= 3 and rest[1].lower() == "comment":
                cid = rest[2].lower()
            elif len(rest) >= 2:
                cid = rest[1].lower()
            elif len(rest) == 1 and rest[0].lower().startswith("t1_"):
                cid = rest[0][3:].lower()
            if cid and not re.fullmatch(r"[a-z0-9]+", cid):
                cid = ""
            canonical = ("https://www.reddit.com/comments/" + tid +
                         ("/comment/" + cid if cid else ""))
            return canonical, "reddit:" + tid, ("reddit-comment:" + cid if cid
                                                else "reddit-thread:" + tid)
        if "/s/" in path:
            # Short Reddit redirect keys are not resolvable without a request;
            # don't pretend two links identify the same post.
            return "https://" + host + path.lower(), "", "reddit-short:" + path.lower()
    if host in ("youtu.be", "www.youtube.com", "youtube.com", "m.youtube.com"):
        qs = parse_qs(u.query)
        if host == "youtu.be":
            vid = path.strip("/").split("/")[0]
        else:
            vid = qs.get("v", [""])[0]
        if vid:
            comment = qs.get("lc", [""])[0]
            normal = "https://www.youtube.com/watch?v=" + quote(vid, safe="")
            if comment:
                normal += "&lc=" + quote(comment, safe="")
            return normal, "youtube:" + vid, ("youtube-comment:" + comment if comment
                                              else "youtube-video:" + vid)
    if host.endswith(".ebay.com") or host == "ebay.com":
        m = re.search(r"/itm/(?:[^/]+/)?(\d{9,15})", path)
        if m:
            item = m.group(1)
            return "https://www.ebay.com/itm/" + item, "ebay-item:" + item, "ebay-item:" + item
    # Do not conflate paths with different thread message anchors by force.
    # Ordinary query parameters are dropped ONLY if all are known tracking;
    # otherwise preserve a sorted query representation.
    query = parse_qs(u.query, keep_blank_values=True)
    meaningful = [(k, v) for k, values in query.items() for v in values
                  if k.lower() not in TRACKING and not k.lower().startswith("utm_")]
    from urllib.parse import urlencode
    suffix = "?" + urlencode(sorted(meaningful)) if meaningful else ""
    host = host[4:] if host.startswith("www.") else host
    canonical = "https://" + host + quote(path or "/", safe="/-._~:%@+") + suffix
    return canonical, "", "url:" + canonical

def load_ledger(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def read_index_hits(paths: list[Path]) -> tuple[dict[str, dict], dict]:
    found: dict[str, dict] = {}
    stats = {"index_result_records": 0, "successful_queries": 0,
             "failed_queries": 0, "raw_search_hits": 0, "malformed_hits": 0,
             "results_with_manifest": 0, "result_manifests": []}
    manifests = set()
    for path in paths:
        with path.open(encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                if not line.strip():
                    continue
                result = json.loads(line)
                if not isinstance(result, dict):
                    raise ValueError(f"Unexpected index row {path}:{ln}")
                stats["index_result_records"] += 1
                if result.get("status") != "index_search_success":
                    stats["failed_queries"] += 1
                    continue
                stats["successful_queries"] += 1
                manifest = result.get("manifest_sha256", "")
                if manifest:
                    manifests.add(manifest)
                    stats["results_with_manifest"] += 1
                task = result.get("task_id", "")
                if not task:
                    raise ValueError(f"Missing search task ID at {path}:{ln}")
                matches = result.get("matches", [])
                if not isinstance(matches, list):
                    raise ValueError(f"Malformed matches list at {path}:{ln}")
                for hit in matches:
                    stats["raw_search_hits"] += 1
                    if not isinstance(hit, dict) or not hit.get("url"):
                        stats["malformed_hits"] += 1
                        continue
                    try:
                        canonical, thread, evidence = normalize_url(hit["url"])
                    except ValueError:
                        stats["malformed_hits"] += 1
                        continue
                    item = found.setdefault(canonical, {
                        "canonical_url": canonical, "thread_key": thread,
                        "evidence_key": evidence, "first_title": str(hit.get("title") or "")[:500],
                        "first_description": str(hit.get("description") or "")[:800],
                        "index_hit_occurrences": 0,
                        "tasks": set(), "languages": set(), "manifests": set(),
                    })
                    item["index_hit_occurrences"] += 1
                    item["tasks"].add(task)
                    item["languages"].add(result.get("language_hint", ""))
                    if manifest:
                        item["manifests"].add(manifest)
    stats["result_manifests"] = sorted(manifests)
    return found, stats

def canonical_refs(markdown: str) -> tuple[set[str], set[str]]:
    """Parse source URLs in canonical sticker markdown; no HTTP or owner inference."""
    urls, threads = set(), set()
    # Markdown is a source list, not a verified equivalence table. Only URLs
    # and Reddit/video topic IDs are used for context checks.
    for match in re.finditer(r'https?://[^\s<>\])"]+', markdown):
        original = match.group(0).rstrip(".,;:'")
        try:
            url, topic, _ = normalize_url(original)
        except ValueError:
            continue
        urls.add(url)
        if topic:
            threads.add(topic)
    return urls, threads


def classify(found: dict[str, dict], ledger: list[dict],
             canonical_urls: set[str] | None = None,
             canonical_threads: set[str] | None = None) -> list[dict]:
    prior_urls, prior_threads = set(), set()
    canonical_urls = canonical_urls or set()
    canonical_threads = canonical_threads or set()
    for item in ledger:
        url = item.get("source_url", "").strip()
        if not url:
            continue
        try:
            canonical, thread, _ = normalize_url(url)
        except ValueError:
            continue
        prior_urls.add(canonical)
        if thread:
            prior_threads.add(thread)
    groups = defaultdict(set)
    for k, item in found.items():
        if item["thread_key"]:
            groups[item["thread_key"]].add(k)
    output = []
    for key, item in found.items():
        exact = key in prior_urls
        context = bool(item["thread_key"] and item["thread_key"] in prior_threads)
        can_exact = key in canonical_urls
        can_context = bool(item["thread_key"] and item["thread_key"] in canonical_threads)
        canonical_relation = ("canonical_exact_source_url" if can_exact else
                              "canonical_thread_context_only" if can_context else
                              "not_in_canonical_link_list_or_not_provided")
        prior = ("exact_ledger_url" if exact else
                 "same_thread_only_no_independent_owner_proof" if context else
                 "not_in_local_ledger_unreconciled")
        same_thread_count = len(groups[item["thread_key"]]) if item["thread_key"] else 1
        snippet = (item["first_title"] + " " + item["first_description"]).casefold()
        caveats = []
        if any(v in snippet for v in (
                "inside ps4 physical game", "limited edition of 2000",
                "$29.99", "game only", "standalone", "solo ps4",
                "insidece_lifestyle")):
            caveats.append("possible_standalone_ps4_false_positive")
        if "sticker" not in snippet and "貼紙" not in snippet and "シール" not in snippet:
            caveats.append("no_sticker_in_search_snippet")
        if same_thread_count > 1:
            caveats.append("other_hits_same_thread_not_other_copies")
        if item["evidence_key"].startswith("reddit-thread:"):
            caveats.append("thread_level_result_not_comment_attributed")
        if item["evidence_key"].startswith("reddit-short:"):
            caveats.append("unresolved_reddit_shortlink")
        result = {
            "candidate_id": hashlib.sha256(key.encode("utf-8")).hexdigest()[:20],
            "canonical_url": key, "thread_key": item["thread_key"],
            "evidence_key": item["evidence_key"],
            "first_title": item["first_title"],
            "first_description": item["first_description"],
            "index_hit_occurrences": item["index_hit_occurrences"],
            "distinct_query_tasks": len(item["tasks"]),
            "query_languages": ",".join(sorted(item["languages"])),
            "prior_ledger_relation": prior,
            "canonical_relation": canonical_relation,
            "source_relation": "index_candidate_url_only",
            "review_warning": ",".join(caveats),
            "review_status": "unreviewed_source_content",
            "new_confirmed_stickers": 0,
        }
        output.append(result)
    return sorted(output, key=lambda x: (x["prior_ledger_relation"],
                                         x["canonical_url"]))

def spreadsheet_safe(v: object) -> object:
    """Prevent untrusted index snippets being interpreted as spreadsheet formulas."""
    if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + v
    return v

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, nargs="+", required=True)
    ap.add_argument("--ledger", type=Path, default=LEDGER)
    ap.add_argument("--canonical-stickers", type=Path,
                    help="Optional downloaded twinysam/INSIDE-ARG stickers.md for exact URL checks")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--summary", type=Path, required=True)
    args = ap.parse_args()
    found, stats = read_index_hits(args.input)
    urls, threads = set(), set()
    if args.canonical_stickers:
        source = args.canonical_stickers.read_bytes()
        stats["canonical_sha256"] = hashlib.sha256(source).hexdigest()
        urls, threads = canonical_refs(source.decode("utf-8"))
        stats["canonical_urls_indexed"] = len(urls)
        stats["canonical_threads_indexed"] = len(threads)
    else:
        stats["canonical_sha256"] = None
        stats["canonical_urls_indexed"] = 0
        stats["canonical_threads_indexed"] = 0
    candidates = classify(found, load_ledger(args.ledger), urls, threads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=OUTPUT, delimiter="\t")
        writer.writeheader()
        writer.writerows([{k: spreadsheet_safe(v) for k, v in row.items()}
                          for row in candidates])
    stats.update({
        "candidate_urls": len(candidates),
        "ledger_exact_urls": sum(x["prior_ledger_relation"] == "exact_ledger_url"
                                 for x in candidates),
        "ledger_thread_context_only": sum(
            x["prior_ledger_relation"] == "same_thread_only_no_independent_owner_proof"
            for x in candidates),
        "canonical_exact_urls": sum(
            x["canonical_relation"] == "canonical_exact_source_url" for x in candidates),
        "canonical_thread_context_only": sum(
            x["canonical_relation"] == "canonical_thread_context_only" for x in candidates),
        "new_confirmed_stickers": 0,
        "status": "index_candidate_triage_requires_original_source_review",
        "caveat": "A URL, title, snippet or alias never establishes a new owner or sticker.",
    })
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()

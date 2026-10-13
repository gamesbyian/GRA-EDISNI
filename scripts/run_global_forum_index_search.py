#!/usr/bin/env python3
"""Execute a limited, explicitly authorized web-index pass over planned tasks.

This queries ONLY the official Brave Search API. It does not crawl any
community, download posts, use Reddit's API, or certify exhaustive coverage.
Requires BRAVE_SEARCH_API_KEY and an affirmative manual workflow input.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
STOP_CODES = {401, 402, 403, 429}


def search_brave(query: str, key: str, count: int) -> list[dict[str, str]]:
    params = urllib.parse.urlencode({"q": query, "count": count})
    req = urllib.request.Request(
        ENDPOINT + "?" + params,
        headers={
            "X-Subscription-Token": key,
            "Accept": "application/json",
            "User-Agent": "GRA-EDISNI-forum-research/1.0 (GitHub Actions)",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        data = json.loads(response.read(1_000_000).decode("utf-8"))
    pages = data.get("web", {}).get("results", [])
    if not isinstance(pages, list):
        raise ValueError("Unexpected Brave response shape")
    return [
        {
            "url": p.get("url", ""),
            "title": p.get("title", ""),
            "description": p.get("description", "")[:350],
        }
        for p in pages
        if isinstance(p, dict) and p.get("url")
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--max-queries", type=int, default=20)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--delay-seconds", type=float, default=1.5)
    args = parser.parse_args()
    if not 1 <= args.max_queries <= 1000:
        parser.error("--max-queries must be between 1 and 1000")
    if not 1 <= args.max_results <= 20:
        parser.error("--max-results must be between 1 and 20")
    if args.delay_seconds < 1:
        parser.error("--delay-seconds must be >= 1")

    key = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    if not key:
        parser.error("Explicit index execution requires BRAVE_SEARCH_API_KEY")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    queried = 0
    failed = 0
    stop_reason = None
    with args.tasks.open(encoding="utf-8") as inp, args.output.open("w", encoding="utf-8") as out:
        for line in inp:
            if queried >= args.max_queries or stop_reason:
                break
            task = json.loads(line)
            if task.get("state") != "planned_unexecuted":
                raise ValueError("Refusing unplanned task")
            q = task["index_query"]
            result = {
                "task_id": task["task_id"],
                "community": task["community"],
                "term": task["term"],
                "query": q,
                "retrieval_source": "brave_web_index_only",
                "coverage": "partial_external_index_no_negative_evidence",
                "status": "not_attempted",
                "matches": [],
            }
            if queried:
                time.sleep(args.delay_seconds)
            queried += 1
            try:
                result["matches"] = search_brave(q, key, args.max_results)
                result["status"] = "index_search_success"
            except urllib.error.HTTPError as exc:
                failed += 1
                result["status"] = "http_error"
                result["http_status"] = exc.code
                if exc.code in STOP_CODES:
                    stop_reason = f"Provider rejected or throttled (HTTP {exc.code}); no retry"
            except (urllib.error.URLError, ValueError, TimeoutError, json.JSONDecodeError) as exc:
                failed += 1
                result["status"] = "request_error"
                result["error_type"] = type(exc).__name__
            out.write(json.dumps(result, ensure_ascii=False) + "\n")
    summary = {
        "index_queries_attempted": queried,
        "failures": failed,
        "stopped": stop_reason,
        "limit": args.max_queries,
        "retrieval_source": "brave_web_index_only",
        "coverage_note": "Indexing and quotas prevent a comprehensive negative conclusion; native and archived passes outstanding.",
        "results_file": str(args.output),
    }
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()

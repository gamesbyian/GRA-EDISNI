#!/usr/bin/env python3
"""Run a bounded, resumable, authorized web-index pass over a frozen manifest.

Only the official Brave Search API is contacted. No forum scraping, Reddit
API access, historical completeness claims, or automatic campaign scheduling.
Requires BRAVE_SEARCH_API_KEY and explicit index execution in the GHA workflow.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
STOP_CODES = {401, 402, 403, 429}

def search_brave(query: str, key: str, count: int, language: str) -> list[dict[str, str]]:
    options = {"q": query, "count": count, "spellcheck": "false"}
    code = language.split("-")[0].lower()
    if len(code) == 2 and code.isalpha():
        options["search_lang"] = code
    params = urllib.parse.urlencode(options)
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
        {"url": p.get("url", ""), "title": p.get("title", ""),
         "description": p.get("description", "")[:350]}
        for p in pages if isinstance(p, dict) and p.get("url")
    ]

def load_manifest(path: Path) -> tuple[list[dict], str]:
    raw = path.read_bytes()
    signature = hashlib.sha256(raw).hexdigest()
    tasks = []
    for number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        task = json.loads(line)
        if (not isinstance(task, dict) or task.get("state") != "planned_unexecuted"
                or not all(task.get(k) for k in ("task_id", "community", "term", "index_query"))):
            raise ValueError(f"Invalid planned task at line {number}")
        tasks.append(task)
    if len(tasks) != len({x["task_id"] for x in tasks}):
        raise ValueError("Duplicate task IDs in manifest")
    return tasks, signature

def run_campaign(
    tasks: list[dict], *, manifest_sha256: str, key: str,
    output: Path, start_index: int, max_queries: int,
    max_results: int = 10, delay_seconds: float = 1.5,
    search_fn=None, sleep_fn=None,
) -> dict:
    if start_index < 0 or start_index > len(tasks):
        raise ValueError("--start-index must be within the manifest")
    if not 1 <= max_queries <= 1000:
        raise ValueError("--max-queries must be 1..1000")
    if not 1 <= max_results <= 20:
        raise ValueError("--max-results must be 1..20")
    if delay_seconds < 1:
        raise ValueError("--delay-seconds must be >= 1")
    if not key:
        raise ValueError("BRAVE_SEARCH_API_KEY is required for index execution")
    if search_fn is None:
        search_fn = search_brave
    if sleep_fn is None:
        sleep_fn = time.sleep
    queried, failed, stopped = 0, 0, None
    next_index = start_index
    last_successful_id = None
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as out:
        for idx in range(start_index, min(start_index + max_queries, len(tasks))):
            task = tasks[idx]
            if queried:
                sleep_fn(delay_seconds)
            queried += 1
            result = {
                "manifest_sha256": manifest_sha256,
                "task_index": idx, "task_id": task["task_id"],
                "community": task["community"], "term": task["term"],
                "query": task["index_query"], "language_hint": task.get("language", ""),
                "retrieval_source": "brave_web_index_only",
                "coverage": "partial_external_index_no_negative_evidence",
                "status": "not_attempted", "matches": [],
            }
            try:
                result["matches"] = search_fn(
                    task["index_query"], key, max_results, task.get("language", "")
                )
                result["status"] = "index_search_success"
                next_index = idx + 1
                last_successful_id = task["task_id"]
            except urllib.error.HTTPError as exc:
                failed += 1
                result["status"], result["http_status"] = "http_error", exc.code
                stopped = (f"HTTP {exc.code}: provider rejected/throttled; "
                           "resume from failed index, no immediate retry"
                           if exc.code in STOP_CODES else
                           f"HTTP {exc.code}: resume from failed index after investigation")
            except (urllib.error.URLError, ValueError, TimeoutError, json.JSONDecodeError) as exc:
                failed += 1
                result["status"] = "request_error"
                result["error_type"] = type(exc).__name__
                stopped = "Request failed; resume from failed index after investigation"
            out.write(json.dumps(result, ensure_ascii=False) + "\n")
            if stopped:
                break
    return {
        "index_queries_attempted": queried, "failures": failed, "stopped": stopped,
        "start_index": start_index, "next_index": next_index,
        "total_planned_tasks": len(tasks), "complete": next_index == len(tasks),
        "manifest_sha256": manifest_sha256,
        "last_successful_task_id": last_successful_id,
        "limit": max_queries, "retrieval_source": "brave_web_index_only",
        "coverage_note": "Only returned web-index results; no zero-hit historical absence is inferred.",
        "results_file": str(output),
        "resume_instruction": (
            "On the NEXT explicit run, use next_index as start_index, "
            "with the SAME manifest_sha256 and source/filters. "
            "Review failed tasks and never skip their offsets silently."
        ),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--expect-manifest-sha256", default="",
                        help="Reject a changed query manifest during campaign continuation")
    parser.add_argument("--max-queries", type=int, default=20)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--delay-seconds", type=float, default=1.5)
    args = parser.parse_args()
    tasks, digest = load_manifest(args.tasks)
    if args.start_index > 0 and not args.expect_manifest_sha256:
        parser.error("Resumed runs require --expect-manifest-sha256 from the previous summary")
    if args.expect_manifest_sha256 and args.expect_manifest_sha256 != digest:
        parser.error("Campaign manifest changed; refuse to reuse old offset")
    key = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    if not key:
        parser.error("Explicit index execution requires BRAVE_SEARCH_API_KEY")
    try:
        result = run_campaign(
            tasks, manifest_sha256=digest, key=key,
            output=args.output, start_index=args.start_index,
            max_queries=args.max_queries, max_results=args.max_results,
            delay_seconds=args.delay_seconds,
        )
    except ValueError as exc:
        parser.error(str(exc))
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()

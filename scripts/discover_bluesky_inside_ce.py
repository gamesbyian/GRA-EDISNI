#!/usr/bin/env python3
"""Source-native, bounded 2023–2026 Bluesky CE discovery pilot.

Unlike the Caswell known-positive recall benchmark, this is an exploratory,
cross-year query set. It never contacts owners or confirms physical stickers.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.error

from audit_bluesky_ce_recall import fetch, summarize

# Frozen BEFORE viewing any results from this exploratory campaign. These are
# public-source product and puzzle query families, NOT owner-handle lookups.
EXPRESSIONS = (
    ("named_edition_exact", '"inside collector\'s edition"'),
    ("named_edition_typographic", '"inside collector’s edition"'),
    ("named_edition_reverse", '"collector\'s edition of inside"'),
    ("named_edition_unpunctuated", '"inside collectors edition"'),
    ("playdead_edition", '"playdead" "collector"'),
    ("playdead_inside_edition", '"playdead" "inside" "edition"'),
    ("iam8bit_inside", '"iam8bit" "inside"'),
    ("iam8bit_huddle", '"iam8bit" "huddle"'),
    ("inside_sticker", '"inside" "sticker"'),
    ("playdead_sticker", '"playdead" "sticker"'),
    ("inside_jelly_statue", '"inside" "jelly statue"'),
    ("inside_huddle_figure", '"inside" "huddle" "figure"'),
    ("inside_numbered", '"inside" "numbered" "sticker"'),
    ("inside_cipher", '"inside" "cipher"'),
    ("inside_realdoll", '"inside" "realdoll"'),
    ("inside_ce_abbrev", '"inside" "ce" "playdead"'),
)
START = "2023-01-01T00:00:00.000Z"
END = "2026-10-17T00:00:00.000Z"

def discovery_plan():
    return [
        {
            "kind": "blind_discovery", "key": key, "version": "v2",
            "endpoint": "app.bsky.feed.searchPostsV2", "query": query,
            "params": {"query": query, "limit": "50", "sort": "recent",
                       "allTime": "true", "since": START, "until": END},
        }
        for key, query in EXPRESSIONS
    ]

def execute(*, live=False, request_cap=16, delay=1.0,
            fetch_fn=None, sleep_fn=None):
    if not 1 <= request_cap <= len(EXPRESSIONS):
        raise ValueError("request cap outside frozen search manifest")
    if delay < 1:
        raise ValueError("minimum delay is 1 second")
    tasks = discovery_plan()
    manifest = hashlib.sha256(json.dumps(
        tasks, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if not live:
        return {"state": "planned_unexecuted", "manifest_sha256": manifest,
                "tasks": tasks, "requests_sent": 0, "results": []}
    fetch_fn = fetch_fn or (lambda endpoint, params: fetch(
        endpoint, params, api_host="primary"))
    sleep_fn = sleep_fn or time.sleep
    results = []
    stop_reason = None
    for index, task in enumerate(tasks[:request_cap]):
        if index:
            sleep_fn(delay)
        try:
            row = summarize(index, task,
                            fetch_fn(task["endpoint"], task["params"]))
        except (urllib.error.HTTPError, urllib.error.URLError,
                TimeoutError, OSError, ValueError) as exc:
            row = summarize(index, task, error=exc)
            if isinstance(exc, urllib.error.HTTPError) and exc.code in (
                    401, 402, 403, 429):
                stop_reason = "provider_access_stop_" + str(exc.code)
        results.append(row)
        if stop_reason:
            break
    return {
        "state": "executed_bounded", "api_host": "primary",
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": manifest, "requests_sent": len(results),
        "tasks_planned": len(tasks), "tasks_attempted": len(results),
        "tasks_unattempted": len(tasks) - len(results),
        "stop_reason": stop_reason,
        "results": results,
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--request-cap", type=int, default=16)
    args = p.parse_args()
    report = execute(live=args.execute, request_cap=args.request_cap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in
                      ("results", "tasks")}, ensure_ascii=False))

if __name__ == "__main__":
    main()

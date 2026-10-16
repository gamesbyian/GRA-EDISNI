#!/usr/bin/env python3
"""Bounded public Bluesky CE search-recall benchmark. Offline unless --execute.

No credentials, account enumeration, contact lookup or owner outreach. Source
control is checked independently; controls are withheld from discovery queries.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = "https://public.api.bsky.app/xrpc/"
GOLD_DID = "did:plc:msovagwqdq3ew2rrikvpqp7c"
GOLD_RKEY = "3mta6ecjbvk2i"
GOLD_URI = f"at://{GOLD_DID}/app.bsky.feed.post/{GOLD_RKEY}"
SINCE, UNTIL = "2026-08-01T00:00:00.000Z", "2026-10-16T00:00:00.000Z"
# Frozen category-level discovery queries; never leak post ID or owner handle.
QUERIES = (
    ("edition_exact_words", "inside collector's edition"),
    ("edition_quoted", "\"inside collector's edition\""),
    ("edition_no_apostrophe", "inside collectors edition"),
    ("huddle_playdead", "playdead huddle"),
    ("huddle_inside", "inside huddle"),
    ("edition_playdead", "playdead collector edition"),
    ("iam8bit_inside", "iam8bit inside"),
    ("realdoll_inside", "realdoll inside"),
)
STOP_HTTP = {401, 402, 403, 429}
ALLOWED = {"app.bsky.feed.getPostThread",
           "app.bsky.feed.searchPosts", "app.bsky.feed.searchPostsV2"}

def plan():
    result = [{
        "kind": "direct_control", "key": "post_thread",
        "endpoint": "app.bsky.feed.getPostThread",
        "params": {"uri": GOLD_URI, "depth": "0"},
    }]
    for key, q in QUERIES:
        for version in ("v2", "v1"):
            v2 = version == "v2"
            params = {
                "query" if v2 else "q": q,
                "limit": "50", "sort": "recent" if v2 else "latest",
                "since": SINCE, "until": UNTIL,
            }
            if v2:
                params["allTime"] = "true"
            result.append({
                "kind": "blind_discovery", "key": key, "query": q,
                "version": version,
                "endpoint": ("app.bsky.feed.searchPostsV2" if v2
                             else "app.bsky.feed.searchPosts"),
                "params": params,
            })
    return result

def fingerprint(tasks):
    return hashlib.sha256(json.dumps(tasks, sort_keys=True,
              separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def fetch(endpoint, params):
    if endpoint not in ALLOWED:
        raise ValueError("Unapproved public endpoint")
    req = urllib.request.Request(
        ROOT + endpoint + "?" + urllib.parse.urlencode(params),
        headers={"Accept": "application/json",
                 "User-Agent": "GRA-EDISNI-CE-recall-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=18) as response:
        content = response.read(800_001)
        if len(content) > 800_000:
            raise ValueError("Oversized response")
        return json.loads(content.decode("utf-8"))

def extract_post(x):
    if not isinstance(x, dict):
        return None
    uri = x.get("uri")
    author, record = x.get("author"), x.get("record")
    if not isinstance(uri, str) or not uri.startswith("at://"):
        return None
    if not isinstance(author, dict) or not isinstance(record, dict):
        return None
    body = record.get("text", "")
    return {
        "uri": uri, "handle": author.get("handle"),
        "created_at": record.get("createdAt"),
        "text_excerpt": body[:450] if isinstance(body, str) else "",
        "target": uri == GOLD_URI,
    }

def summarize(index, task, response=None, error=None):
    result = {k: task[k] for k in ("kind", "key", "endpoint") if k in task}
    result.update({
        "task_index": index, "version": task.get("version"),
        "query": task.get("query"),
        "status": "ok" if error is None else "error",
    })
    if error is not None:
        result["error"] = str(error)[:200]
        if isinstance(error, urllib.error.HTTPError):
            result["http_status"] = error.code
        return result
    if not isinstance(response, dict):
        return {**result, "status": "bad_shape"}
    if task["kind"] == "direct_control":
        thread = response.get("thread")
        post = extract_post(thread.get("post") if isinstance(thread, dict) else None)
        result.update({
            "status": "ok" if post else "bad_shape",
            "post": post, "gold_accessible": bool(post and post["target"]),
        })
        return result
    posts = response.get("posts")
    if not isinstance(posts, list):
        return {**result, "status": "bad_shape", "error": "no posts array"}
    parsed = [post for post in (extract_post(x) for x in posts) if post]
    positions = [i for i, post in enumerate(parsed, 1) if post["target"]]
    result.update({
        "returned": len(posts), "parsed": len(parsed),
        "hits_total_reported": response.get("hitsTotal"),
        "cursor_available": bool(response.get("cursor")),
        "gold_found": bool(positions), "gold_ranks": positions,
        "posts": parsed,
    })
    return result

def run(*, execute=False, max_requests=17, delay=1.0,
        fetch_fn=None, sleep_fn=None):
    if not 1 <= max_requests <= 17:
        raise ValueError("max_requests must be 1..17")
    if delay < 1:
        raise ValueError("delay must be >=1")
    tasks = plan()
    sha = fingerprint(tasks)
    if not execute:
        return {"state": "planned_unexecuted", "manifest_sha256": sha,
                "requests_sent": 0, "tasks": tasks, "results": []}
    fetch_fn, sleep_fn = fetch_fn or fetch, sleep_fn or time.sleep
    results, stop_reason, blocked_versions = [], None, set()
    requests_sent, skipped_blocked = 0, 0
    for i, task in enumerate(tasks):
        if task.get("version") in blocked_versions:
            results.append({"task_index": i, "kind": task["kind"],
                            "key": task["key"], "version": task["version"],
                            "status": "skipped_after_endpoint_access_failure"})
            skipped_blocked += 1
            continue
        if requests_sent >= max_requests:
            break
        if requests_sent:
            sleep_fn(delay)
        requests_sent += 1
        try:
            row = summarize(i, task, fetch_fn(task["endpoint"], task["params"]))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                ValueError, OSError, json.JSONDecodeError) as exc:
            row = summarize(i, task, error=exc)
            if isinstance(exc, urllib.error.HTTPError):
                if exc.code == 429 or exc.code == 402:
                    stop_reason = f"provider_access_stop_{exc.code}"
                elif exc.code in (401, 403) and task["kind"] == "blind_discovery":
                    # No repeated requests to a forbidden version. The independently
                    # documented other search version may have distinct permissions.
                    blocked_versions.add(task["version"])
        results.append(row)
        if stop_reason:
            break
    return {
        "state": "executed_bounded",
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": sha, "requests_sent": requests_sent,
        "tasks_planned": len(tasks),
        "tasks_attempted": requests_sent,
        "tasks_skipped_endpoint_block": skipped_blocked,
        "tasks_unattempted": len(tasks) - len(results),
        "blocked_versions": sorted(blocked_versions),
        "stop_reason": stop_reason,
        "direct_post_retrievable": results[0].get("gold_accessible") if results else None,
        "blind_hits": [
            {"key": x["key"], "version": x["version"], "ranks": x["gold_ranks"]}
            for x in results if x.get("gold_found")
        ],
        "results": results,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--max-requests", type=int, default=17)
    ap.add_argument("--delay-seconds", type=float, default=1.0)
    args = ap.parse_args()
    report = run(execute=args.execute, max_requests=args.max_requests,
                 delay=args.delay_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("results", "tasks")}, ensure_ascii=False))

if __name__ == "__main__":
    main()

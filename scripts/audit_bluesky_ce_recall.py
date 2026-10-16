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
from urllib.parse import urlsplit

# Both hosts are documented Bluesky AppView entrypoints. The cached public
# hostname returned 403 for both native search versions on 2026-10-16;
# use the separately documented primary AppView hostname by default.
HOSTS = {"primary": "https://api.bsky.app/xrpc/",
         "cached": "https://public.api.bsky.app/xrpc/"}
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

def fetch(endpoint, params, *, api_host="primary"):
    if api_host not in HOSTS:
        raise ValueError("Unapproved Bluesky API host")
    if endpoint not in ALLOWED:
        raise ValueError("Unapproved public endpoint")
    req = urllib.request.Request(
        HOSTS[api_host] + endpoint + "?" + urllib.parse.urlencode(params),
        headers={"Accept": "application/json",
                 "User-Agent": "GRA-EDISNI-CE-recall-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=18) as response:
        content = response.read(800_001)
        if len(content) > 800_000:
            raise ValueError("Oversized response")
        return json.loads(content.decode("utf-8"))

def public_image_url(value):
    """Retain only unchanged public Bluesky CDN URLs; never fetch media here."""
    if not isinstance(value, str):
        return ""
    try:
        u = urlsplit(value)
        if u.scheme != "https" or u.hostname != "cdn.bsky.app" or u.username or u.password:
            return ""
    except ValueError:
        return ""
    return value


def media_metadata(x, record):
    """Keep source media cues that text-only search snapshots used to drop."""
    view = x.get("embed") if isinstance(x.get("embed"), dict) else {}
    rec = record.get("embed") if isinstance(record.get("embed"), dict) else {}
    nested = view.get("media") if isinstance(view.get("media"), dict) else view
    visual_images = nested.get("images")
    if not isinstance(visual_images, list):
        visual_images = []
    images = []
    for item in visual_images[:12]:
        if not isinstance(item, dict):
            continue
        images.append({
            "thumbnail": public_image_url(item.get("thumb")),
            "fullsize": public_image_url(item.get("fullsize")),
            "alt": str(item.get("alt") or "")[:450],
        })
    # A recordWithMedia embed holds the original image declarations under
    # record.embed.media, not directly under record.embed.
    rec_media = rec.get("media") if isinstance(rec.get("media"), dict) else rec
    declared = rec_media.get("images")
    if not isinstance(declared, list):
        declared = []
    external = nested.get("external") if isinstance(nested.get("external"), dict) else (
        rec_media.get("external") if isinstance(rec_media.get("external"), dict) else {})
    uri = external.get("uri", "")
    if not isinstance(uri, str):
        uri = ""
    try:
        if urlsplit(uri).scheme not in ("https", "http"):
            uri = ""
    except ValueError:
        uri = ""
    return {
        "record_embed_type": rec.get("$type", ""),
        "view_embed_type": view.get("$type", ""),
        "record_declared_image_count": len(declared),
        "record_image_alts": [str(x.get("alt") or "")[:450] for x in declared[:12]
                              if isinstance(x, dict)],
        "public_view_image_count": len(images),
        "image_previews": images,
        "external_public_url": uri[:1000],
        "record_media_without_view_image_urls": bool(declared) and not any(
            img["fullsize"] or img["thumbnail"] for img in images),
        "media_image_urls_preserved": sum(bool(img["fullsize"] or img["thumbnail"])
                                          for img in images),
        "original_media_downloaded": False,
        "evidence_class": "public_search_metadata_only_not_a_sticker_photo",
    }


def author_date_outside_filter(post, task):
    """Report calendar mismatch; do not assume Bluesky filters author's createdAt."""
    from datetime import datetime
    try:
        date = datetime.fromisoformat(str(post.get("created_at", "")).replace("Z", "+00:00"))
        since = datetime.fromisoformat(task["params"]["since"].replace("Z", "+00:00"))
        until = datetime.fromisoformat(task["params"]["until"].replace("Z", "+00:00"))
        return date < since or date >= until
    except (KeyError, ValueError, TypeError):
        return False


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
        "indexed_at": x.get("indexedAt"),
        "text_excerpt": body[:450] if isinstance(body, str) else "",
        "media_metadata": media_metadata(x, record),
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
        "posts_with_view_image_metadata": sum(bool(p["media_metadata"]["public_view_image_count"]) for p in parsed),
        "posts_with_record_declared_images_but_no_view_urls": sum(bool(p["media_metadata"]["record_media_without_view_image_urls"]) for p in parsed),
        "author_created_at_outside_requested_window": sum(author_date_outside_filter(p, task) for p in parsed),
        "time_filter_semantics": "reported_author_timestamp_disagreement_only_not_provider_falsification",
        "posts": parsed,
    })
    return result

def run(*, execute=False, max_requests=17, delay=1.0,
        api_host="primary", fetch_fn=None, sleep_fn=None):
    if api_host not in HOSTS:
        raise ValueError("Unapproved Bluesky API host")
    if not 1 <= max_requests <= 17:
        raise ValueError("max_requests must be 1..17")
    if delay < 1:
        raise ValueError("delay must be >=1")
    tasks = plan()
    sha = fingerprint(tasks)
    if not execute:
        return {"state": "planned_unexecuted", "manifest_sha256": sha,
                "api_host": api_host, "requests_sent": 0, "tasks": tasks,
                "results": []}
    if fetch_fn is None:
        fetch_fn = lambda endpoint, params: fetch(endpoint, params, api_host=api_host)
    sleep_fn = sleep_fn or time.sleep
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
        "state": "executed_bounded", "api_host": api_host,
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
    ap.add_argument("--api-host", choices=tuple(HOSTS), default="primary",
                    help="Official AppView hostname; primary avoids cached public search 403")
    ap.add_argument("--max-requests", type=int, default=17)
    ap.add_argument("--delay-seconds", type=float, default=1.0)
    args = ap.parse_args()
    report = run(execute=args.execute, max_requests=args.max_requests,
                 api_host=args.api_host, delay=args.delay_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("results", "tasks")}, ensure_ascii=False))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One-time bounded public Bluesky photograph + missing-page followthrough.

No owner contact; no authenticating; no private media; no sticker interpretation.
The EXACT pre-recorded three image URLs and four source-native query keys
are the only permitted targets. The default invocation is offline planning.
"""
from __future__ import annotations
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

from audit_bluesky_ce_recall import fetch, summarize
from discover_bluesky_inside_ce import discovery_plan

SOURCE_PATH = (Path(__file__).resolve().parents[1] /
               "data/reference/inside-ce-bluesky-visual-source-pins-2026-10-16.json")
RETRY = ("playdead_inside_edition", "inside_numbered")
PAGINATE = ("inside_sticker", "inside_cipher")
EXPECTED = set(RETRY + PAGINATE)
STOP_HTTP = {401, 402, 403, 429}
MAX_PUBLIC_IMAGE_BYTES = 6_000_000


def manifest(source=SOURCE_PATH):
    data = json.loads(Path(source).read_text(encoding="utf-8"))
    images = data.get("images", [])
    if len(images) != 3 or len({r["case_id"] for r in images}) != 3:
        raise ValueError("Must have exactly three pinned public image controls")
    for item in images:
        u = urllib.parse.urlsplit(item["cdn_url"])
        if (u.scheme != "https" or u.hostname != "cdn.bsky.app"
                or u.port is not None or u.username or u.password
                or not u.path.startswith("/img/feed_fullsize/plain/did:plc:")
                or u.query or u.fragment):
            raise ValueError("Refusing non-exact public Bluesky CDN image locator")
    tasks = {t["key"]: t for t in discovery_plan() if t["key"] in EXPECTED}
    if set(tasks) != EXPECTED:
        raise ValueError("Missing a frozen query from the original 16-query pilot")
    return {"source_images": images,
            "queries": [tasks[key] for key in RETRY + PAGINATE],
            "source_manifest_path": str(source.name)}


def get_image(url):
    req = urllib.request.Request(
        url, headers={"Accept": "image/jpeg,image/png,image/webp",
                      "User-Agent": "GRA-EDISNI-Bluesky-source-review/1.0"})
    with urllib.request.urlopen(req, timeout=18) as response:
        payload = response.read(MAX_PUBLIC_IMAGE_BYTES + 1)
        if len(payload) > MAX_PUBLIC_IMAGE_BYTES:
            raise ValueError("Public photo exceeded 6 MB ceiling")
        mime = response.headers.get("Content-Type", "").split(";", 1)[0].strip()
    if payload.startswith(bytes.fromhex("ffd8ff")):
        ext = ".jpg"
    elif payload.startswith(bytes.fromhex("89504e470d0a1a0a")):
        ext = ".png"
    elif payload.startswith(b"RIFF") and payload[8:12] == b"WEBP":
        ext = ".webp"
    else:
        raise ValueError("Non-image or unidentified public CDN bytes")
    return payload, mime, ext


def probe(*, live=False, output: Path, image_getter=None,
          query_fetcher=None, sleep_fn=None):
    inputs = manifest()
    fingerprint = hashlib.sha256(json.dumps(inputs, sort_keys=True,
                       separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    report = {"state": "executed_bounded" if live else "planned_unexecuted",
              "source_manifest_sha256": fingerprint,
              "source_original_bluesky_run": "38882275551",
              "run_at_utc": datetime.now(timezone.utc).isoformat() if live else None,
              "planned_image_transfers": 3,
              "planned_unique_query_keys": 4,
              "max_total_query_requests": 6,
              "image_records": [], "query_records": [],
              "requests_sent": 0, "stop_reason": None,
              "source_image_review": "no_physical_sticker_claim",
              "new_confirmed_stickers": 0}
    if not live:
        report["planned"] = inputs
        return report
    output.mkdir(parents=True, exist_ok=True)
    image_getter = image_getter or get_image
    query_fetcher = query_fetcher or (lambda ep, params: fetch(
        ep, params, api_host="primary"))
    sleep_fn = sleep_fn or time.sleep
    for item in inputs["source_images"]:
        rec = {"case_id": item["case_id"], "source_post": item["source_post"],
               "source_alt": item["alt"],
               "source_cdn_url": item["cdn_url"], "status": "not_attempted"}
        try:
            data, mimetype, ext = image_getter(item["cdn_url"])
            if len(data) > MAX_PUBLIC_IMAGE_BYTES:
                raise ValueError("6 MB image bound exceeded")
            if not (data.startswith(bytes.fromhex("ffd8ff")) or
                    data.startswith(bytes.fromhex("89504e470d0a1a0a")) or
                    (data.startswith(b"RIFF") and data[8:12] == b"WEBP")):
                raise ValueError("Image signature unavailable")
            if ext not in {".jpg", ".png", ".webp"}:
                raise ValueError("Unsupported image suffix")
            filename = item["case_id"] + ext
            (output / filename).write_bytes(data)
            rec.update({"status": "downloaded_uninspected",
                        "content_type": mimetype, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "local_file": filename, "image_subject_verified": False,
                        "sticker_verified": False})
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                OSError, ValueError) as exc:
            rec.update({"status": "acquisition_error", "error": str(exc)[:250]})
        report["image_records"].append(rec)
    for task in inputs["queries"]:
        if report["stop_reason"]:
            report["query_records"].append(
                {"key": task["key"], "status": "not_attempted_after_provider_block"})
            continue
        phases = ["retry_original_page"] if task["key"] in RETRY else [
            "refetch_page_one", "next_page_if_cursor"]
        cursor = None
        for phase in phases:
            if phase == "next_page_if_cursor" and not cursor:
                report["query_records"].append({
                    "key": task["key"], "phase": phase,
                    "status": "no_cursor_to_follow"})
                continue
            if report["requests_sent"]:
                sleep_fn(1)
            params = dict(task["params"])
            if phase == "next_page_if_cursor":
                params["cursor"] = cursor
            rec = {"key": task["key"], "phase": phase,
                   "endpoint": task["endpoint"], "query": task["query"],
                   "status": "unattempted"}
            report["requests_sent"] += 1
            try:
                response = query_fetcher(task["endpoint"], params)
                body = json.dumps(response, sort_keys=True,
                                  separators=(",", ":"), ensure_ascii=False)
                rec["response_sha256"] = hashlib.sha256(body.encode()).hexdigest()
                rec["source"] = summarize(report["requests_sent"], task, response)
                rec["status"] = rec["source"]["status"]
                cursor = response.get("cursor") if isinstance(response, dict) else None
                rec["has_further_cursor"] = bool(cursor)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                    ValueError, OSError) as exc:
                rec.update({"status": "request_error", "error": str(exc)[:250]})
                cursor = None
                if isinstance(exc, urllib.error.HTTPError):
                    rec["http_status"] = exc.code
                    if exc.code in STOP_HTTP:
                        report["stop_reason"] = "provider_access_stop_" + str(exc.code)
            report["query_records"].append(rec)
            if report["stop_reason"]:
                break
    report["successful_search_requests"] = sum(
        r["status"] == "ok" for r in report["query_records"])
    report["failed_search_requests"] = sum(
        r["status"] in ("request_error", "bad_shape") for r in report["query_records"])
    report["media_retrieval_count"] = sum(
        r["status"] == "downloaded_uninspected" for r in report["image_records"])
    report["original_media_interpreted_in_automated_run"] = False
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result = probe(live=args.execute, output=args.output)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "source-followthrough.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "state": result["state"], "images": len(result["image_records"]),
        "successful_search_requests": result.get("successful_search_requests", 0),
        "failed_search_requests": result.get("failed_search_requests", 0),
        "requests_sent": result["requests_sent"],
        "stop_reason": result["stop_reason"],
        "new_confirmed_stickers": 0,
    }))


if __name__ == "__main__":
    main()

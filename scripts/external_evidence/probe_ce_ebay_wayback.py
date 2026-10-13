#!/usr/bin/env python3
"""Check Wayback snapshot metadata for exact historical public eBay CE listing URLs.

Queries ONLY the Internet Archive's public Availability API. Never fetches archived
media, changes sales records, bypasses subscriber images or equates a capture with
a readable numbered sticker. Respect remote rate limits immediately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ARCHIVE_API = "https://archive.org/wayback/available"
MAX_BYTES = 100_000


def snapshot_metadata(entry: dict, response: dict) -> dict:
    snapshots = response.get("archived_snapshots", {})
    closest = snapshots.get("closest", {}) if isinstance(snapshots, dict) else {}
    available = bool(closest.get("available"))
    snapshot_url = str(closest.get("url") or "") if available else ""
    if snapshot_url:
        p = urllib.parse.urlparse(snapshot_url)
        if p.hostname not in {"web.archive.org", "wayback.archive-it.org"} or p.scheme not in {"https", "http"}:
            raise ValueError("unexpected non-Wayback snapshot URL")
    return {
        "item_id": entry["item_id"], "original_ebay_url": entry["ebay_url"],
        "third_party_sale_date": entry["sale_date"],
        "status": "snapshot-advertised-not-fetched" if snapshot_url else "no-snapshot-advertised",
        "snapshot_url": snapshot_url or None,
        "capture_timestamp": closest.get("timestamp") if snapshot_url else None,
        "archive_capture_http_status": closest.get("status") if snapshot_url else None,
        "evidence_grade": "archival availability pointer only; bytes and sticker not reviewed",
    }


def fetch(entry: dict) -> tuple[dict, str]:
    url = entry["ebay_url"]
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname != "www.ebay.com" or p.path != "/itm/" + entry["item_id"]:
        raise ValueError("item URL invalid for exact archive lookup")
    params = urllib.parse.urlencode({"url": url, "timestamp": entry["sale_date"].replace("-", "")})
    req = urllib.request.Request(ARCHIVE_API + "?" + params, headers={
        "User-Agent": "GRA-EDISNI-public-historical-CE-wayback/1.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        if urllib.parse.urlparse(resp.geturl()).hostname != "archive.org":
            raise ValueError("unapproved archive API redirect")
        if resp.headers.get_content_type() != "application/json":
            raise ValueError("archive response was not JSON")
        blob = resp.read(MAX_BYTES + 1)
        if not 0 < len(blob) <= MAX_BYTES:
            raise ValueError("archive response invalid length")
        result = json.loads(blob)
        if not isinstance(result, dict) or not isinstance(result.get("archived_snapshots"), dict):
            raise ValueError("unexpected archival response structure")
        return result, hashlib.sha256(blob).hexdigest()


def inspect(records: list[dict], requester=fetch) -> list[dict]:
    if len(records) > 8:
        raise ValueError("maximum eight separately approved public sale URLs")
    results = []
    for index, record in enumerate(records):
        if record.get("initial_reconciliation") != "unreconciled-by-canonical-exact-item-id":
            raise ValueError("Only unresolved source IDs can enter this probe")
        try:
            payload, sha = requester(record)
            item = snapshot_metadata(record, payload)
            item["response_sha256"] = sha
        except urllib.error.HTTPError as exc:
            item = {"item_id": record["item_id"], "status": "archive-http-error",
                    "http_status": exc.code, "reason": str(exc)[:160]}
            results.append(item)
            if exc.code in {429, 503}:
                for pending in records[index + 1:]:
                    results.append({"item_id": pending["item_id"], "status": "not-attempted-after-rate-limit"})
                break
            continue
        except (OSError, ValueError, urllib.error.URLError) as exc:
            item = {"item_id": record["item_id"], "status": "archive-unavailable",
                    "reason": str(exc)[:200]}
        results.append(item)
        if requester is fetch and index + 1 < len(records):
            time.sleep(2)
    return results


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path,
                   default=Path("data/reference/inside-ce-public-historic-ebay-sale-index.json"))
    p.add_argument("--output", type=Path,
                   default=Path("visual-evidence-work/historical-ebay-wayback-availability.json"))
    args = p.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))["sale_records"]
    selected = [r for r in data if r["initial_reconciliation"] ==
                "unreconciled-by-canonical-exact-item-id"]
    result = {"schema_version": 1, "api": ARCHIVE_API,
              "interpretation": "Availability only. No images fetched or owner/sticker inferred.",
              "sources": inspect(selected)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checked":len(result["sources"]),
                      "snapshot_pointers":sum(r["status"] == "snapshot-advertised-not-fetched"
                                              for r in result["sources"])}))


if __name__ == "__main__":
    main()

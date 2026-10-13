#!/usr/bin/env python3
"""Probe exact public eBay listing *capture indexes* using Wayback CDX.

Metadata only: no archived HTML/media is fetched. CDX prefix searches may find
permalink variants missed by Wayback's single nearest-snapshot availability
endpoint. All records must match a 12-digit eBay item ID *at the URL path
boundary*, not merely a convenient prefix or a similar product page.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CDX_HOST = "web.archive.org"
CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
MAX_RESPONSE_BYTES = 512_000
PER_ID_LIMIT = 24
ID_RE = re.compile(r"\d{12}")
HOSTS = {"www.ebay.com", "ebay.com", "www.ebay.ca", "www.ebay.co.uk"}


class CDXHTTPError(OSError):
    def __init__(self, status: int, retry_after: str = ""):
        super().__init__(f"CDX HTTP {status}")
        self.status = status
        self.retry_after = retry_after[:50]


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname != CDX_HOST:
            raise ValueError("CDX index redirected outside Wayback HTTPS host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def item_id_matches_url(url: str, item_id: str) -> bool:
    if not ID_RE.fullmatch(item_id):
        return False
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in HOSTS:
        return False
    if parsed.username or parsed.password:
        return False
    path = urllib.parse.unquote(parsed.path)
    # Canonical numbered permalink, or a slug followed by the exact item ID.
    return bool(re.fullmatch(
        rf"/itm/(?:[^/?#]+/)?{re.escape(item_id)}/?", path, flags=re.I
    ))


def query_url(item_id: str, *, limit: int = PER_ID_LIMIT) -> str:
    if not ID_RE.fullmatch(item_id):
        raise ValueError("Invalid 12-digit public eBay listing ID")
    if not 1 <= limit <= PER_ID_LIMIT:
        raise ValueError("CDX per-item capture limit exceeded")
    # Prefix intentionally includes only one numbered listing URL. Results
    # differing by trailing digits or product slugs must be rejected later.
    params = urllib.parse.urlencode({
        "url": f"www.ebay.com/itm/{item_id}",
        "matchType": "prefix",
        "output": "json",
        "filter": "statuscode:200",
        "fl": "timestamp,original,statuscode,mimetype,digest",
        "limit": limit,
    })
    return CDX_ENDPOINT + "?" + params


def fetch_cdx(item_id: str) -> tuple[list, str]:
    url = query_url(item_id)
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "GRA-EDISNI-public-historical-ebay-capture-index/1.0",
    })
    try:
        resp = urllib.request.build_opener(SafeRedirect()).open(req, timeout=25)
    except urllib.error.HTTPError as exc:
        raise CDXHTTPError(exc.code, exc.headers.get("Retry-After", "") if exc.headers else "") from exc
    with resp:
        parsed = urllib.parse.urlparse(resp.geturl())
        if parsed.scheme != "https" or parsed.hostname != CDX_HOST:
            raise ValueError("CDX final origin mismatch")
        if "json" not in resp.headers.get_content_type():
            raise ValueError("CDX index did not return JSON")
        body = resp.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("Oversized CDX capture-index response")
        if not body.strip():
            raise ValueError("Empty CDX response")
        return json.loads(body), hashlib.sha256(body).hexdigest()


def parse_capture_rows(body: object, item_id: str) -> tuple[list[dict], int]:
    if body == []:
        return [], 0  # Wayback CDX returns [] for a successful empty capture-index query.
    if not isinstance(body, list) or not body:
        raise ValueError("Expected CDX array with field-name header")
    header = body[0]
    required = {"timestamp", "original", "statuscode", "mimetype", "digest"}
    if not isinstance(header, list) or not required.issubset(set(header)):
        raise ValueError("Unexpected CDX result fields")
    indices = {v: header.index(v) for v in required}
    valid = []
    rejected = 0
    seen = set()
    for row in body[1:]:
        if not isinstance(row, list) or len(row) <= max(indices.values()):
            rejected += 1
            continue
        details = {name: str(row[index]) for name, index in indices.items()}
        original = details["original"]
        timestamp = details["timestamp"]
        if (not item_id_matches_url(original, item_id)
                or not re.fullmatch(r"\d{14}", timestamp)
                or details["statuscode"] != "200"
                or "html" not in details["mimetype"].lower()):
            rejected += 1
            continue
        identity = (timestamp, original)
        if identity in seen:
            continue
        seen.add(identity)
        valid.append({
            "timestamp": timestamp,
            "original_url": original,
            "status_code": details["statuscode"],
            "mimetype": details["mimetype"],
            "archive_digest": details["digest"],
            "wayback_snapshot_url": f"https://web.archive.org/web/{timestamp}/{original}",
            "capture_status": "CDX-index-only-not-fetched",
            "serial_number_observed": False,
        })
    return valid, rejected


def inspect(records: list[dict], *, fetcher=fetch_cdx, nap=2.0) -> list[dict]:
    if not 1 <= len(records) <= 8:
        raise ValueError("Only one to eight curated source items can be checked")
    results = []
    blocked = ""
    for i, entry in enumerate(records):
        item_id = entry["item_id"]
        if entry.get("initial_reconciliation") != "unreconciled-by-canonical-exact-item-id":
            raise ValueError("Known or non-CE source must not be probed as unknown")
        if entry.get("ebay_url") != f"https://www.ebay.com/itm/{item_id}" or not ID_RE.fullmatch(item_id):
            raise ValueError("Exact eBay URL or listing ID invalid")
        if blocked:
            results.append({"item_id": item_id, "status": "not-attempted", "reason": blocked})
            continue
        try:
            payload, response_sha = fetcher(item_id)
            captures, rejects = parse_capture_rows(payload, item_id)
            result = {
                "item_id": item_id,
                "original_listing_url": entry["ebay_url"],
                "status": "CDX-capture-pointers-unverified" if captures else "CDX-no-capture-pointers",
                "archive_query_sha256": response_sha,
                "capture_count": len(captures),
                "excluded_nonmatching_rows": rejects,
                "captures": captures,
                "note": "Index metadata only; no captured HTML, original images, numbered sticker or physical CE confirmed.",
            }
        except CDXHTTPError as exc:
            result = {"item_id": item_id, "status": "CDX-http-error",
                      "http_status": exc.status, "retry_after": exc.retry_after}
            if exc.status in {401, 403, 429, 503}:
                blocked = f"CDX HTTP {exc.status}; no further requests in this run"
        except (OSError, ValueError, urllib.error.URLError) as exc:
            result = {"item_id": item_id, "status": "CDX-unavailable",
                      "reason": str(exc)[:220]}
        results.append(result)
        if not blocked and fetcher is fetch_cdx and i + 1 < len(records):
            time.sleep(nap)
    return results


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path,
                   default=Path("data/reference/inside-ce-public-historic-ebay-sale-index.json"))
    p.add_argument("--output", type=Path,
                   default=Path("visual-evidence-work/historic-ebay-cdx-captures.json"))
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--count", type=int, default=7)
    args = p.parse_args()
    source = json.loads(args.manifest.read_text(encoding="utf-8"))["sale_records"]
    unresolved = [x for x in source if x.get("initial_reconciliation") ==
                  "unreconciled-by-canonical-exact-item-id"]
    if not 0 <= args.start < len(unresolved) or not 1 <= args.count <= 8:
        p.error("Invalid bounded source slice")
    rows = inspect(unresolved[args.start:args.start + args.count])
    payload = {"schema_version": 1,
               "source": "Wayback CDX prefix capture index; archived original page bytes not requested",
               "sources": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "sources_checked": len(rows),
        "captures": sum(r.get("capture_count", 0) for r in rows),
        "unavailable_or_blocked": sum(r["status"] in
            {"not-attempted", "CDX-http-error", "CDX-unavailable"} for r in rows),
    }))


if __name__ == "__main__":
    main()

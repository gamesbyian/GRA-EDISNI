#!/usr/bin/env python3
"""Recover historical PUBLIC Reddit submission photo URLs via third-party archives.

This is metadata recovery, not live Reddit access, permission to view removed
content, new sticker evidence, account investigation or owner outreach.
Archives may be stale or incomplete; every failure becomes a reproducible record.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from scripts.external_evidence.fetch_html_images import approved

POST_ID = re.compile(r"/comments/([0-9a-z]+)/", re.IGNORECASE)
ARCHIVE_HOSTS = {"arctic-shift.photon-reddit.com", "api.pullpush.io"}
LIMIT_BYTES = 4 * 1024 * 1024


class ArchiveRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname not in ARCHIVE_HOSTS:
            raise ValueError("Archive redirected outside allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def endpoints(post_id: str) -> list[tuple[str, str]]:
    if not re.fullmatch(r"[a-z0-9]{5,9}", post_id, re.IGNORECASE):
        raise ValueError("Invalid public Reddit post ID")
    return [
        ("arctic-shift", "https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + post_id),
        ("pullpush", "https://api.pullpush.io/reddit/search/submission/?ids=" + post_id),
    ]


def fetch_json(url: str) -> tuple[object, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ARCHIVE_HOSTS:
        raise ValueError("Archived metadata host not allowlisted")
    req = urllib.request.Request(url, headers={
        "User-Agent": "GRA-EDISNI-CE-public-archive-metadata/1.0",
        "Accept": "application/json",
    })
    opener = urllib.request.build_opener(ArchiveRedirects())
    with opener.open(req, timeout=20) as resp:
        if resp.headers.get_content_type() != "application/json":
            raise ValueError("Unexpected archive content type")
        data = resp.read(LIMIT_BYTES + 1)
        if len(data) > LIMIT_BYTES:
            raise ValueError("Oversized archive metadata response")
        return json.loads(data), hashlib.sha256(data).hexdigest()


def unpack(response: object, post_id: str) -> dict | None:
    if isinstance(response, dict):
        records = response.get("data", [])
    elif isinstance(response, list):
        records = response
    else:
        return None
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list):
        return None
    for item in records:
        if isinstance(item, dict) and item.get("id", "").lower() == post_id.lower():
            return item
    return None


def visible_image_urls(post: dict) -> list[str]:
    """Extract *claimed post media URL* fields, never unrelated profile thumbnails."""
    urls = set()
    def add(raw: object) -> None:
        if isinstance(raw, str):
            candidate = html.unescape(raw)
            if approved(candidate):
                urls.add(candidate)
    for key in ("url", "url_overridden_by_dest"):
        add(post.get(key))
    preview = post.get("preview")
    if isinstance(preview, dict):
        for photo in preview.get("images", []):
            if isinstance(photo, dict):
                src = photo.get("source")
                if isinstance(src, dict):
                    add(src.get("url"))
    meta = post.get("media_metadata")
    if isinstance(meta, dict):
        for entry in meta.values():
            if isinstance(entry, dict):
                src = entry.get("s")
                if isinstance(src, dict):
                    add(src.get("u"))
    return sorted(urls)


def scan(sources: list[dict], requester=fetch_json) -> tuple[list[dict], list[dict]]:
    report, found = [], []
    for source in sources:
        match = POST_ID.search(source.get("url", ""))
        if not match or "reddit.com" not in urllib.parse.urlparse(source["url"]).netloc:
            continue
        post_id = match.group(1)
        record = {"source_id": source["id"], "post_id": post_id,
                  "source_page_url": source["url"], "status": "unavailable",
                  "archive_attempts": []}
        for provider, target in endpoints(post_id):
            try:
                data, sha = requester(target)
                post = unpack(data, post_id)
                if not post:
                    record["archive_attempts"].append({"provider": provider, "status": "not-found"})
                    continue
                urls = visible_image_urls(post)
                record.update({"status": "archived-metadata-available", "provider": provider,
                               "archive_sha256": sha, "image_url_count": len(urls)})
                for url in urls:
                    found.append({"source_id": source["id"], "image_url": url,
                                  "source_page_url": source["url"], "keyword_hints": [],
                                  "hint_count": 0, "contexts": [f"{provider} public post media metadata"],
                                  "review_status": "archive-url-unfetched"})
                break
            except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
                record["archive_attempts"].append({"provider": provider,
                                                   "status": "failed", "error": str(exc)[:180]})
        report.append(record)
    return report, found


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/reference/inside-ce-visual-historical-pages.json"))
    p.add_argument("--out", type=Path, default=Path("visual-evidence-work"))
    args = p.parse_args()
    sources = json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    report, images = scan(sources)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "reddit-archival-report.json").write_text(json.dumps({
        "schema_version": 1, "sources": report,
        "note": "Historical metadata only; no new ownership or sticker observations",
    }, indent=2) + "\n", encoding="utf-8")
    (args.out / "reddit-archival-image-leads.json").write_text(json.dumps({
        "schema_version": 1, "image_mentions": images,
        "note": "URLs extracted from public archives, not necessarily live or accurate",
    }, indent=2) + "\n", encoding="utf-8")
    print(f"archived post metadata available: {sum(x['status']=='archived-metadata-available' for x in report)}/{len(report)}")
    print(f"archived media URL mentions: {len(images)}")


if __name__ == "__main__":
    main()

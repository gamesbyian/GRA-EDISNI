#!/usr/bin/env python3
"""Fetch a bounded allowlisted subset of image URLs extracted from PUBLIC HTML.

No page crawling, proxying, credentials, external-search automation, or arbitrary host
fetches. Preserve URL -> source page -> original media SHA256 -> local file mapping.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

Image.MAX_IMAGE_PIXELS = 40_000_000
MAX_IMAGE_BYTES = 15 * 1024 * 1024
HOSTS = {
    "www.iam8bit.com", "cdn.shopify.com", "cdn.vox-cdn.com",
    "i.redd.it", "preview.redd.it", "i.imgur.com",
    "pbs.twimg.com", "i.ebayimg.com",
}
FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}
MAX_TOTAL_BYTES = 180 * 1024 * 1024


def approved(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.scheme == "https" and parsed.hostname in HOSTS
            and not parsed.username and not parsed.password)


class RestrictRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not approved(newurl):
            raise ValueError("Image redirect not on approved HTTPS hosts")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def retrieve(url: str) -> tuple[bytes, str, str]:
    if not approved(url):
        raise ValueError("Image host not approved; source kept for manual review")
    req = urllib.request.Request(url, headers={
        "User-Agent": "GRA-EDISNI-public-CE-visual-research/1.0",
        "Accept": "image/jpeg,image/png,image/webp,image/gif",
    })
    op = urllib.request.build_opener(RestrictRedirects())
    with op.open(req, timeout=25) as response:
        if not approved(response.geturl()):
            raise ValueError("Image final URL not approved")
        if not response.headers.get_content_type().startswith("image/"):
            raise ValueError("Not image content-type")
        data = response.read(MAX_IMAGE_BYTES + 1)
        if not 0 < len(data) <= MAX_IMAGE_BYTES:
            raise ValueError("Image empty or over size limit")
        with Image.open(io.BytesIO(data)) as im:
            fmt = im.format
            w, h = im.size
            im.verify()
        if fmt not in FORMATS or min(w, h) < 32 or w * h > Image.MAX_IMAGE_PIXELS:
            raise ValueError("Unsupported image type or dimensions")
        return data, response.geturl(), FORMATS[fmt]


def safe_dir(name: str) -> str:
    return "htmlimg-" + re.sub(r"[^a-zA-Z0-9_-]+", "-", name)[:80]


def select(leads: list[dict], per_page: int, total: int) -> list[dict]:
    """Stable, bounded selection; no claim that the richest hint is the best image."""
    grouped: dict[str, list[dict]] = {}
    for entry in leads:
        key = entry.get("source_id", "")
        if not key:
            continue
        grouped.setdefault(key, []).append(entry)
    selected = []
    for key, rows in sorted(grouped.items()):
        seen = set()
        count = 0
        for row in sorted(rows, key=lambda r: (-r.get("hint_count", 0), r["image_url"])):
            if row["image_url"] in seen:
                continue
            seen.add(row["image_url"])
            if not approved(row["image_url"]):
                continue
            selected.append(row)
            count += 1
            if count >= per_page:
                break
            if len(selected) >= total:
                break
        if len(selected) >= total:
            break
    return selected


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--leads", type=Path, default=Path("visual-evidence-work/html-image-leads.json"))
    p.add_argument("--out", type=Path, default=Path("evidence-work"))
    p.add_argument("--max-per-page", type=int, default=8)
    p.add_argument("--max-images", type=int, default=48)
    args = p.parse_args()
    if not (1 <= args.max_images <= 200 and 1 <= args.max_per_page <= 50):
        p.error("max-images must be 1..200 and max-per-page 1..50")
    rows = json.loads(args.leads.read_text(encoding="utf-8"))["image_mentions"]
    chosen = select(rows, args.max_per_page, args.max_images)
    reports = []
    total_bytes = 0
    by_source: dict[str, dict] = {}
    for row in chosen:
        parent = args.out / safe_dir(row["source_id"])
        parent.mkdir(parents=True, exist_ok=True)
        name = hashlib.sha256(row["image_url"].encode("utf-8")).hexdigest()[:24]
        record = {"image_url": row["image_url"], "source_id": row["source_id"],
                  "source_page_url": row["source_page_url"], "keyword_hints": row["keyword_hints"],
                  "status": "unavailable"}
        try:
            if total_bytes >= MAX_TOTAL_BYTES:
                raise ValueError("Run total-byte budget reached")
            data, final_url, suffix = retrieve(row["image_url"])
            if total_bytes + len(data) > MAX_TOTAL_BYTES:
                raise ValueError("Run would exceed total-byte budget")
            dest = parent / (name + suffix)
            dest.write_bytes(data)
            total_bytes += len(data)
            record.update({"status": "downloaded", "path": str(dest.relative_to(args.out)),
                           "final_url": final_url, "bytes": len(data),
                           "sha256": hashlib.sha256(data).hexdigest()})
            bucket = by_source.setdefault(row["source_id"], {
                "source_id": safe_dir(row["source_id"]), "url": row["source_page_url"],
                "kind": "public-html-image-candidate", "classification": "unreviewed",
                "image_urls": {},
            })
            bucket["image_urls"][dest.name] = row["image_url"]
        except (OSError, ValueError, urllib.error.URLError) as exc:
            record["error"] = str(exc)[:240]
        reports.append(record)
        print(row["source_id"], record["status"])
    for source_id, data in by_source.items():
        out = args.out / safe_dir(source_id) / "acquisition.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path = args.out / "html-image-download-report.json"
    report_path.write_text(json.dumps({
        "schema_version": 1, "max_images": args.max_images,
        "bytes_downloaded": total_bytes, "image_downloads": reports,
        "note": "Remote media unreviewed; nothing here confirms an edition or sticker"
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

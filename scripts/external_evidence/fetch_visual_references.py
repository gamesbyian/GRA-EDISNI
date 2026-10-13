#!/usr/bin/env python3
"""Bounded public-image acquisition for CE promotional negative controls."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 40_000_000
ALLOWED_HOSTS = {"www.iam8bit.com", "cdn.shopify.com", "cdn.vox-cdn.com", "static0.polygonimages.com", "i.redd.it"}
MAX_BYTES = 20 * 1024 * 1024


def allowed(url: str) -> bool:
    u = urlparse(url)
    return u.scheme == "https" and u.hostname in ALLOWED_HOSTS and not u.username and not u.password


class ControlledRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError(f"unapproved image redirect: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str) -> tuple[bytes, str]:
    if not allowed(url):
        raise ValueError(f"unapproved image source: {url}")
    request = urllib.request.Request(url, headers={
        "User-Agent": "GRA-EDISNI-public-image-research/1.0",
        "Accept": "image/jpeg,image/png,image/webp",
    })
    opener = urllib.request.build_opener(ControlledRedirect())
    with opener.open(request, timeout=25) as response:
        if not allowed(response.geturl()):
            raise ValueError(f"unapproved final URL: {response.geturl()}")
        media_type = response.headers.get_content_type()
        if not media_type.startswith("image/"):
            raise ValueError(f"expected image content, received {media_type}")
        data = response.read(MAX_BYTES + 1)
        if not 0 < len(data) <= MAX_BYTES:
            raise ValueError("image empty or over 20 MiB")
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        with Image.open(io.BytesIO(data)) as im:
            width, height = im.size
            if min(width, height) < 32 or width * height > Image.MAX_IMAGE_PIXELS:
                raise ValueError("image dimensions invalid or too large")
        return data, response.geturl()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/reference/inside-ce-visual-sources.json"))
    p.add_argument("--out", type=Path, default=Path("visual-reference-work"))
    args = p.parse_args()
    sources = json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    args.out.mkdir(parents=True, exist_ok=True)
    reports = []
    for source in sources:
        url = source["url"]
        filename = source["id"] + source["extension"]
        dest = args.out / filename
        item = {"id": source["id"], "source_url": url, "path": filename,
                "source_page": source["source_page"], "role": source["role"]}
        try:
            if not allowed(url):
                raise ValueError("source not allowlisted")
            if dest.is_file():
                with Image.open(dest) as im:
                    im.verify()
                data = dest.read_bytes()
                if not 0 < len(data) <= MAX_BYTES:
                    raise ValueError("existing file invalid length")
                item["status"] = "local-existing"
                item["final_url"] = url  # existing bytes, not a fresh retrieval claim
            else:
                data, final_url = fetch(url)
                dest.write_bytes(data)
                item["status"] = "downloaded"
                item["final_url"] = final_url
            item["bytes"] = len(data)
            item["sha256"] = hashlib.sha256(data).hexdigest()
            expected = source.get("expected_sha256")
            if expected and item["sha256"].lower() != expected.lower():
                raise ValueError("source media changed: expected SHA256 " + expected)
        except (OSError, ValueError, UnidentifiedImageError, urllib.error.URLError) as exc:
            item["status"] = "unavailable"
            item["error"] = str(exc)[:240]
        reports.append(item)
        print(item["id"], item["status"])
    (args.out / "retrieval-report.json").write_text(json.dumps({
        "schema_version": 1, "sources": reports
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

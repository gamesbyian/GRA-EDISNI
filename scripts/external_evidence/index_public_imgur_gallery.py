#!/usr/bin/env python3
"""Normalize downloaded public Imgur gallery media into visual search source manifests.

This script does not fetch anything. Feed it the file tree and per-image .json
metadata written by gallery-dl. It verifies bytes, dimensions and exact public
source provenance before producing the candidate-index acquisition.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 40_000_000
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MEDIA_HOSTS = {"i.imgur.com", "imgur.com"}


def verify_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme == "https" and p.hostname in MEDIA_HOSTS and not p.username and not p.password


def gallery_metadata(root: Path, gallery: dict) -> dict:
    """Preserve both comment permalink and full Imgur media provenance."""
    name = gallery["id"]
    if not name.isalnum() or len(name) > 20:
        raise ValueError("unsafe gallery id")
    if gallery["url"] != "https://imgur.com/gallery/" + name:
        raise ValueError("gallery URL/id mismatch")
    comment_url = gallery["source_page_url"]
    parsed = urlparse(comment_url)
    if parsed.scheme != "https" or parsed.hostname not in {"www.reddit.com", "reddit.com"}:
        raise ValueError("comment source not approved public Reddit URL")
    result = {
        "source_id": "gallery-" + name,
        "kind": "public-comment-linked-gallery",
        "url": comment_url,
        "gallery_url": gallery["url"],
        "role": gallery["evidence_role"],
        "classification": "unreviewed-source-media",
        "image_urls": {},
        "source_pages": {},
        "sha256": {},
        "file_metadata": {},
        "errors": [],
    }
    files = sorted(x for x in root.rglob("*") if x.is_file() and x.suffix.lower() in SUPPORTED)
    if len(files) > 100:
        raise ValueError("gallery has more than 100 media items; shard before indexing")
    for path in files:
        try:
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                w, h = im.size
                if min(w, h) < 32 or w * h > Image.MAX_IMAGE_PIXELS:
                    raise ValueError("invalid media dimensions")
            metadata = path.with_suffix(path.suffix + ".json")
            if not metadata.is_file():
                raise ValueError("missing gallery-dl original media metadata")
            info = json.loads(metadata.read_text(encoding="utf-8"))
            original_url = info.get("url")
            if not isinstance(original_url, str) or not verify_url(original_url):
                raise ValueError("missing/unsafe original Imgur media URL")
            data_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if (name == "YLXcetH" and path.name.endswith("_mOHC6nr.jpg")
                    and data_hash != gallery.get("known_original_sha256")):
                raise ValueError("known canonical sticker 171 original SHA256 mismatch")
            result["image_urls"][path.name] = original_url
            result["source_pages"][path.name] = comment_url
            result["sha256"][path.relative_to(root).as_posix()] = data_hash
            result["file_metadata"][path.name] = {
                "gallery_id": name, "media_id": info.get("id"),
                "media_url": original_url, "width": w, "height": h,
                "original_published_date_claim": info.get("date"),
            }
        except (OSError, ValueError, KeyError, UnidentifiedImageError) as exc:
            result["errors"].append({"path": path.relative_to(root).as_posix(),
                                     "reason": str(exc)[:240]})
    result["image_count"] = len(result["image_urls"])
    result["retrieval_status"] = "images-verified" if result["image_count"] else "no-verified-images"
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path,
                   default=Path("data/reference/inside-ce-archived-public-galleries.json"))
    p.add_argument("--root", type=Path, default=Path("evidence-work"))
    p.add_argument("--gallery-id", type=str, default="all")
    args = p.parse_args()
    galleries = json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    if args.gallery_id != "all":
        galleries = [g for g in galleries if g["id"] == args.gallery_id]
        if not galleries:
            p.error("unknown gallery ID")
    for gallery in galleries:
        folder = args.root / ("gallery-" + gallery["id"])
        folder.mkdir(parents=True, exist_ok=True)
        report = gallery_metadata(folder, gallery)
        (folder / "acquisition.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"gallery_id": gallery["id"], "verified_images": report["image_count"],
                          "invalid": len(report["errors"]),
                          "status": report["retrieval_status"]}))


if __name__ == "__main__":
    main()

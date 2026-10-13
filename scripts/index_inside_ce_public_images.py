#!/usr/bin/env python3
"""Offline INSIDE CE photo provenance and duplicate-candidate index.

Input is locally acquired, approved image files with SOURCE metadata supplied
by the researcher. No fetching, scraping, face-recognition, identity resolution
or reading image text. Exact/pixel/perceptual matches are only review candidates,
never independent CE/sticker sightings. Requires Pillow.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, ImageOps, UnidentifiedImageError

EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
MAX_FILE_BYTES = 25_000_000
MAX_IMAGE_PIXELS = 24_000_000
REQUIRED = {"asset_id", "file_path", "source_url", "source_kind", "published_at",
            "captured_at", "permission_basis"}
SOURCE_KINDS = {"official_marketing", "owner_public_post", "public_resale",
                "public_review", "community_repost", "unknown_public"}
OUTPUT = ["asset_id", "source_url", "source_kind", "published_at", "captured_at",
          "permission_basis", "file_sha256", "pixel_sha256", "dhash64", "ahash64",
          "width", "height", "aspect_ratio", "candidate_cluster",
          "other_assets_in_cluster", "marketing_reference_proximity",
          "assessment", "new_confirmed_stickers"]

def hash_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def img_hash(gray: Image.Image, kind: str) -> int:
    if kind == "dhash":
        pixels = list(gray.resize((9, 8), Image.Resampling.LANCZOS).getdata())
        bits = [pixels[y*9+x] > pixels[y*9+x+1]
                for y in range(8) for x in range(8)]
    elif kind == "ahash":
        px = list(gray.resize((8, 8), Image.Resampling.LANCZOS).getdata())
        mean = sum(px) / len(px)
        bits = [p >= mean for p in px]
    else:
        raise ValueError("Unknown image hashing method")
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value

def normalized_image(path: Path) -> dict:
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError("Non-image file extension")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Image exceeds 25MB file budget")
    raw = path.read_bytes()
    with Image.open(path) as source:
        if source.width * source.height > MAX_IMAGE_PIXELS:
            raise ValueError("Image exceeds 24-million-pixel budget")
        # First frame only; animated media requires a distinct video/frame
        # extraction witness rather than silently declaring coverage of video.
        frame = ImageOps.exif_transpose(source)
        rgb = frame.convert("RGB")
        width, height = rgb.size
        if min(width, height) < 24:
            raise ValueError("Image too small for reliable provenance matching")
        gray = rgb.convert("L")
        # Pixel-equivalent re-encodings share a SHA digest. Metadata/different
        # JPEG quality can differ; dHash/aHash provide review-only candidates.
        return {
            "file_sha256": hash_hex(raw),
            "pixel_sha256": hash_hex(
                width.to_bytes(4, "big") + height.to_bytes(4, "big") + rgb.tobytes()
            ),
            "dhash64": f"{img_hash(gray, 'dhash'):016x}",
            "ahash64": f"{img_hash(gray, 'ahash'):016x}",
            "width": width, "height": height,
            "aspect_ratio": round(width / height, 6),
        }

def validate_row(row: dict) -> None:
    if not REQUIRED.issubset(row):
        raise ValueError("Media row missing required provenance columns")
    if not row["asset_id"].strip():
        raise ValueError("Every image needs stable asset_id")
    if row["source_kind"] not in SOURCE_KINDS:
        raise ValueError("Unsupported source_kind")
    u = urlsplit(row["source_url"])
    if u.scheme not in {"https", "http"} or not u.hostname:
        raise ValueError("A source image requires an original public source URL")
    if not row["permission_basis"].strip():
        raise ValueError("Permission/retention review must be recorded")

def similar(a: dict, b: dict, *, dhash_limit: int = 7,
            ahash_limit: int = 8, aspect_tolerance: float = 0.12) -> bool:
    """Conservative *candidate* similarity, not positive ownership identity."""
    if a["pixel_sha256"] == b["pixel_sha256"]:
        return True
    aspect = a["aspect_ratio"] / b["aspect_ratio"]
    if not 1 - aspect_tolerance <= aspect <= 1 + aspect_tolerance:
        return False
    d = (int(a["dhash64"], 16) ^ int(b["dhash64"], 16)).bit_count()
    h = (int(a["ahash64"], 16) ^ int(b["ahash64"], 16)).bit_count()
    return d <= dhash_limit and h <= ahash_limit

def analyze(rows: list[dict], *, root: Path) -> tuple[list[dict], dict]:
    metadata = []
    seen = set()
    root = root.resolve()
    for row in rows:
        validate_row(row)
        if row["asset_id"] in seen:
            raise ValueError("Repeated asset_id")
        seen.add(row["asset_id"])
        candidate = (root / row["file_path"]).resolve()
        if not candidate.is_relative_to(root):
            raise ValueError("Image path escapes --root")
        if not candidate.is_file():
            raise ValueError("Missing image file")
        record = {k: row[k] for k in REQUIRED}
        record.update(normalized_image(candidate))
        metadata.append(record)

    # Non-transitive near matches may bridge unrelated images. We retain
    # every pair separately; grouping is only a candidate review convenience.
    parent = list(range(len(metadata)))
    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k
    def join(a, b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[max(pa, pb)] = min(pa, pb)

    candidates = []
    for i in range(len(metadata)):
        for j in range(i + 1, len(metadata)):
            a, b = metadata[i], metadata[j]
            if similar(a, b):
                join(i, j)
                category = ("same_file_bytes" if a["file_sha256"] == b["file_sha256"]
                            else "same_decoded_pixels" if a["pixel_sha256"] == b["pixel_sha256"]
                            else "perceptual_similarity_needs_review")
                candidates.append({
                    "a": a["asset_id"], "b": b["asset_id"], "kind": category,
                    "dhash_distance": (int(a["dhash64"], 16) ^ int(b["dhash64"], 16)).bit_count(),
                    "ahash_distance": (int(a["ahash64"], 16) ^ int(b["ahash64"], 16)).bit_count(),
                    "independent_sticker_evidence": False,
                })
    by_group = {}
    for i, row in enumerate(metadata):
        by_group.setdefault(find(i), []).append(row)
    ordered_groups = sorted(by_group.values(), key=lambda group:
                            min(row["asset_id"] for row in group))
    index = {}
    for number, group in enumerate(ordered_groups, 1):
        for member in group:
            index[member["asset_id"]] = (number, group)
    for row in metadata:
        gid, members = index[row["asset_id"]]
        others = [v["asset_id"] for v in members if v["asset_id"] != row["asset_id"]]
        official_nearby = any(
            v["source_kind"] == "official_marketing" and
            v["asset_id"] != row["asset_id"] for v in members
        )
        row["candidate_cluster"] = f"C{gid:05d}"
        row["other_assets_in_cluster"] = ",".join(others)
        row["marketing_reference_proximity"] = (
            "potential_reused_official_asset_needs_review" if official_nearby
            else "none_in_supplied_corpus"
        )
        row["assessment"] = "unreviewed_image_provenance_only"
        row["new_confirmed_stickers"] = 0
    summary = {
        "images": len(metadata), "candidate_pairs": len(candidates),
        "candidate_clusters": len(ordered_groups),
        "possible_marketing_reuses": sum(
            v["marketing_reference_proximity"].startswith("potential_")
            for v in metadata
        ), "new_confirmed_stickers": 0,
        "coverage": "only_locally_supplied_and_rights_reviewed_image_files",
        "pair_records": candidates,
        "disclaimer": "Hashes do not establish a unique physical CE, sticker image or owner.",
    }
    return metadata, summary

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    with args.manifest.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    records, report = analyze(rows, root=args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({k: str(record.get(k, "")).replace("\t", " ").replace("\n", " ")
                             for k in OUTPUT})
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "pair_records"}))

if __name__ == "__main__":
    main()

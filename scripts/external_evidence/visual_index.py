#!/usr/bin/env python3
"""Offline INSIDE CE visual provenance triage. Matches suggest review, never sticker truth.

Inputs are preserved originals and locally acquired public photographs. No scraping,
owner identification, facial recognition, OCR, external services, or model downloads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 40_000_000
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif", ".bmp", ".gif"}
# Historical visually similar editions may differ by crop and compression.
# Thresholds are deliberately conservative; calibrate on known false positives.
FULL_DHASH_MAX = 6
FULL_AHASH_MAX = 9
CROP_DHASH_MAX = 4
CROP_AHASH_MAX = 7
MAX_ASPECT_LOG = 0.10


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dhash(im: Image.Image) -> int:
    pixels = list(im.convert("L").resize((9, 8), Image.Resampling.LANCZOS).getdata())
    n = 0
    for row in range(8):
        for col in range(8):
            n = (n << 1) | (pixels[row * 9 + col] > pixels[row * 9 + col + 1])
    return n


def ahash(im: Image.Image) -> int:
    pixels = list(im.convert("L").resize((8, 8), Image.Resampling.LANCZOS).getdata())
    avg = sum(pixels) / 64
    n = 0
    for px in pixels:
        n = (n << 1) | (px >= avg)
    return n


def variants(image: Image.Image) -> dict[str, dict[str, str]]:
    """Full and overlap windows, so a partial repost has a chance to surface.

    These windows do not confer arbitrary-crop invariance or scene recognition.
    """
    w, h = image.size
    boxes = {"full": (0, 0, w, h)}
    if min(w, h) >= 128:
        cw, ch = round(w * .75), round(h * .75)
        for name, x, y in (
            ("centre", (w - cw)//2, (h - ch)//2),
            ("tl", 0, 0), ("tr", w - cw, 0),
            ("bl", 0, h - ch), ("br", w - cw, h - ch),
        ):
            boxes[name] = (x, y, x + cw, y + ch)
    result = {}
    for name, bounds in boxes.items():
        crop = image.crop(bounds)
        result[name] = {"dhash64": f"{dhash(crop):016x}", "ahash64": f"{ahash(crop):016x}"}
    return result


def image_record(path: Path, *, root: Path, ref_id: str, role: str,
                 source_url: str = "", source_kind: str = "", image_url: str = "") -> dict:
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError(f"unsupported extension: {path}")
    with Image.open(path) as raw:
        raw.verify()
    with Image.open(path) as raw:
        im = ImageOps.exif_transpose(raw)
        im.seek(0) if getattr(im, "n_frames", 1) > 1 else None
        im = im.convert("RGB")
        w, h = im.size
        if min(w, h) < 32:
            raise ValueError("image too small for visual fingerprint")
        if w * h > Image.MAX_IMAGE_PIXELS:
            raise ValueError("image exceeds pixel bound")
        fp = variants(im)
    return {
        "id": ref_id, "role": role, "path": path.relative_to(root).as_posix(),
        "sha256": digest(path), "width": w, "height": h,
        "source_url": source_url, "source_kind": source_kind, "image_url": image_url,
        "fingerprints": fp,
    }


def sticker_refs(repo_root: Path, manifest: Path) -> list[dict]:
    refs = []
    with manifest.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["category"] != "community-original" or row["canonical_input"].lower() != "yes":
                continue
            path = (repo_root / row["path"]).resolve()
            if not path.is_relative_to(repo_root.resolve()):
                raise ValueError("sticker path escapes repo")
            if not path.is_file():
                raise FileNotFoundError(path)
            actual = digest(path)
            if actual != row["sha256"]:
                raise ValueError(f"physical image SHA256 mismatch: {path}")
            record = image_record(
                path, root=repo_root, ref_id=f"sticker-{row['serial']}",
                role="known-sticker-photo",
                source_url=f"https://github.com/{row['source_repo']}/blob/{row['source_ref']}/{row['source_path']}",
                source_kind="canonical-community-original",
            )
            record["sticker"] = {
                "serial": row["serial"], "background": row["tile"], "symbol": row["symbol"]
            }
            refs.append(record)
    return refs


def promotional_refs(repo_root: Path, directory: Path, manifest: Path) -> tuple[list[dict], list[dict]]:
    records = []
    skipped = []
    sources = json.loads(manifest.read_text(encoding="utf-8"))["sources"]
    for source in sources:
        ident = source["id"]
        path = directory / (ident + source["extension"])
        if not path.is_file():
            skipped.append({"id": ident, "reason": "not-downloaded", "source_url": source["url"]})
            continue
        rec = image_record(
            path, root=repo_root, ref_id=ident, role=(
                "standalone-product-reference" if source["role"] == "negative-control-standalone"
                else "historical-owner-photo-no-visible-sticker"
                if source["role"] == "positive-control-public-owner-open-ce-no-visible-sticker"
                else "promotional-reference"
            ),
            source_url=source["url"], source_kind=source["origin"],
        )
        records.append(rec)
    return records, skipped


def provenance(path: Path, candidate_root: Path, acquisition: dict) -> tuple[str, str, str]:
    relative = path.relative_to(candidate_root)
    if len(relative.parts) > 1:
        source_id = relative.parts[0]
        if source_id in acquisition:
            record = acquisition[source_id]
            page = record.get("source_pages", {}).get(path.name, record.get("url", ""))
            return page, source_id, record.get("image_urls", {}).get(path.name, "")
    return "", "", ""


def read_acquisition(candidate_root: Path) -> dict:
    out = {}
    for path in candidate_root.glob("*/acquisition.json"):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(record, dict):
                out[path.parent.name] = record
        except (ValueError, OSError):
            continue
    return out


def candidates(root: Path, *, max_files: int) -> tuple[list[dict], list[dict]]:
    out, errors = [], []
    acquisition = read_acquisition(root)
    paths = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS)
    if len(paths) > max_files:
        raise ValueError(f"{len(paths)} images exceeds --max-files={max_files}; shard corpus")
    for index, path in enumerate(paths):
        url, source_id, original_image_url = provenance(path, root, acquisition)
        try:
            rec = image_record(
                path, root=root, ref_id=f"candidate-{index:06d}",
                role="unreviewed-candidate", source_url=url, source_kind=source_id,
                image_url=original_image_url)
            out.append(rec)
        except (UnidentifiedImageError, ValueError, OSError, Image.DecompressionBombError) as exc:
            errors.append({"path": path.relative_to(root).as_posix(), "error": str(exc)[:240]})
    return out, errors


def ham(a: str, b: str) -> int:
    return (int(a, 16) ^ int(b, 16)).bit_count()


def compare(candidate: dict, ref: dict) -> dict | None:
    if candidate["sha256"] == ref["sha256"]:
        return {"kind": "byte-identical", "dhash_distance": 0, "ahash_distance": 0,
                "candidate_window": "full", "reference_window": "full"}
    a, b = candidate["fingerprints"], ref["fingerprints"]
    # Whole-frame perceptual agreement is useful for recompression/resizing.
    x, y = a["full"], b["full"]
    d, h = ham(x["dhash64"], y["dhash64"]), ham(x["ahash64"], y["ahash64"])
    aspect_a = candidate["width"] / candidate["height"]
    aspect_b = ref["width"] / ref["height"]
    from math import log
    if abs(log(aspect_a / aspect_b)) <= MAX_ASPECT_LOG and d <= FULL_DHASH_MAX and h <= FULL_AHASH_MAX:
        return {"kind": "whole-image-similar", "dhash_distance": d, "ahash_distance": h,
                "candidate_window": "full", "reference_window": "full"}
    # Cropped repost hint. Requiring BOTH hashes reduces false positives but does
    # not establish same object. In particular, sticker backs can be very alike.
    best = None
    for aname, av in a.items():
        for bname, bv in b.items():
            if aname == bname == "full":
                continue
            d = ham(av["dhash64"], bv["dhash64"])
            h = ham(av["ahash64"], bv["ahash64"])
            if d <= CROP_DHASH_MAX and h <= CROP_AHASH_MAX:
                item = {"kind": "possible-cropped-repost", "dhash_distance": d,
                        "ahash_distance": h, "candidate_window": aname,
                        "reference_window": bname}
                if best is None or (d + h, d, h) < (best["dhash_distance"] + best["ahash_distance"],
                                                       best["dhash_distance"], best["ahash_distance"]):
                    best = item
    return best


def cluster_exact(records: list[dict]) -> list[dict]:
    clusters = defaultdict(list)
    for rec in records:
        clusters[rec["sha256"]].append(rec["id"])
    return [{"sha256": sha, "candidate_ids": ids} for sha, ids in sorted(clusters.items())
            if len(ids) > 1]


def analyze(refs: list[dict], items: list[dict], limit: int) -> dict:
    matches = []
    for item in items:
        found = []
        for ref in refs:
            match = compare(item, ref)
            if match:
                found.append({
                    "candidate_id": item["id"], "candidate_path": item["path"],
                    "candidate_source_url": item["source_url"], "candidate_image_url": item["image_url"],
                    "reference_id": ref["id"],
                    "reference_role": ref["role"], "reference_url": ref["source_url"],
                    **match,
                })
        ordering = {"byte-identical": 0, "whole-image-similar": 1, "possible-cropped-repost": 2}
        found.sort(key=lambda a: (ordering[a["kind"]], a["dhash_distance"] +
                                 a["ahash_distance"], a["reference_id"]))
        matches.extend(found[:limit])
    by_candidate = defaultdict(list)
    for match in matches:
        by_candidate[match["candidate_id"]].append(match)
    triage = []
    for item in items:
        hit = by_candidate.get(item["id"], [])
        promo = any(x["reference_role"] == "promotional-reference" for x in hit)
        standalone = any(x["reference_role"] == "standalone-product-reference" for x in hit)
        known = any(x["reference_role"] == "known-sticker-photo" for x in hit)
        owner_original = any(x["reference_role"] == "historical-owner-photo-no-visible-sticker" for x in hit)
        if standalone:
            label = "standalone-ps4-image-review"
        elif promo:
            label = "promotional-reuse-review"
        elif known:
            label = "known-sticker-photo-repost-review"
        elif owner_original:
            label = "known-owner-photo-repost-review"
        else:
            label = "unmatched-visual-review"
        triage.append({
            "candidate_id": item["id"], "path": item["path"], "source_url": item["source_url"],
            "image_url": item["image_url"], "classification": label, "match_count": len(hit),
            "review_required": True, "new_sticker_confirmed": False,
        })
    return {"matches": matches, "triage": triage, "exact_candidate_groups": cluster_exact(items)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--stickers-manifest", type=Path,
                   default=Path("archive/stickers/manifest.csv"))
    p.add_argument("--promotional-manifest", type=Path,
                   default=Path("data/reference/inside-ce-visual-sources.json"))
    p.add_argument("--promotional-dir", type=Path, default=Path("visual-reference-work"))
    p.add_argument("--candidates", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("visual-evidence-work"))
    p.add_argument("--max-files", type=int, default=3000)
    p.add_argument("--max-matches", type=int, default=5)
    p.add_argument("--skip-stickers", action="store_true")
    args = p.parse_args()
    if args.max_files <= 0 or args.max_matches <= 0:
        p.error("max-files and max-matches must be positive")
    root = args.repo_root.resolve()
    def rel(path: Path) -> Path:
        return path if path.is_absolute() else root / path
    refs = [] if args.skip_stickers else sticker_refs(root, rel(args.stickers_manifest))
    promo, missing = promotional_refs(root, rel(args.promotional_dir),
                                      rel(args.promotional_manifest))
    refs.extend(promo)
    items, errors = candidates(rel(args.candidates), max_files=args.max_files)
    result = analyze(refs, items, args.max_matches)
    output = rel(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "reference-index.json").write_text(json.dumps({
        "schema_version": 1, "references": refs, "missing_remote_references": missing,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "candidate-index.json").write_text(json.dumps({
        "schema_version": 1, "candidates": items, "errors": errors,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "visual-matches.json").write_text(json.dumps({
        "schema_version": 1, **result,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (output / "review-queue.csv").open("w", newline="", encoding="utf-8") as fh:
        cols = ["candidate_id", "path", "source_url", "image_url", "classification",
                "match_count", "review_required", "new_sticker_confirmed"]
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        writer.writerows(result["triage"])
    print(json.dumps({
        "references": len(refs), "candidates": len(items),
        "hits": len(result["matches"]), "errors": len(errors),
        "missing_promotional_references": len(missing), "output": str(output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

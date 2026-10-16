#!/usr/bin/env python3
"""Offline multi-scale sticker-region *candidate* ranking (never identification).

Uses reviewed original-photo ROIs to search regions of already acquired public
photographs. PIL dHash+aHash is a cheap candidate generator, NOT a detector,
not a serial reader, and not evidence that two photographs show one object.
No network, models, OCR, faces, account inference or downloads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

Image.MAX_IMAGE_PIXELS = 40_000_000
PROXY_LONG_SIDE = 1100
FRACTIONS = (0.075, 0.10, 0.14, 0.20, 0.28, 0.40, 0.55, 0.75)
ASPECTS = (0.75, 1.0, 1.33)
ANGLES = (0, 90, 180, 270)
MIN_SIDE = 30


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fingerprint(image: Image.Image) -> tuple[int, int]:
    gray = image.convert("L")
    d = list(gray.resize((9, 8), Image.Resampling.LANCZOS).getdata())
    a = list(gray.resize((8, 8), Image.Resampling.LANCZOS).getdata())
    difference = 0
    for y in range(8):
        for x in range(8):
            difference = (difference << 1) | (d[y * 9 + x] > d[y * 9 + x + 1])
    mean = sum(a) / 64
    average = 0
    for value in a:
        average = (average << 1) | (value >= mean)
    return difference, average


def load_regions(manifest: Path, repo_root: Path) -> list[dict]:
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    with manifest.open(encoding="utf-8", newline="") as f:
        records = list(csv.DictReader(f))
    if not records:
        raise ValueError("region manifest is empty")
    refs = []
    seen = set()
    root = repo_root.resolve()
    for row in records:
        serial = row["serial"]
        if serial in seen or not (len(serial) == 3 and serial.isdigit()):
            raise ValueError("invalid or repeated reference serial")
        seen.add(serial)
        if row.get("roi_review_status") != "visually-inspected-2026-10-16":
            raise ValueError("reference ROI lacks documented manual inspection")
        path = (root / row["source_path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("reference path missing or outside approved repo")
        if not path.relative_to(root).as_posix().startswith("archive/stickers/originals/"):
            raise ValueError("reference must be an original physical photo")
        actual = sha256(path)
        if actual != row["source_sha256"]:
            raise ValueError("reference image digest mismatch")
        coords = tuple(float(row[field]) for field in ("left", "top", "right", "bottom"))
        l, t, r, b = coords
        if not (0 <= l < r <= 1 and 0 <= t < b <= 1 and
                (r-l)*(b-t) >= .01):
            raise ValueError("invalid normalized region bounds")
        with Image.open(path) as img:
            if img.width * img.height > Image.MAX_IMAGE_PIXELS:
                raise ValueError("reference image pixel cap exceeded")
            original = ImageOps.exif_transpose(img).convert("RGB")
            bounds = (round(l * original.width), round(t * original.height),
                      round(r * original.width), round(b * original.height))
            roi = original.crop(bounds)
            if min(roi.size) < MIN_SIDE:
                raise ValueError("reference patch too small")
            for angle in ANGLES:
                rotated = roi.rotate(angle, expand=True)
                dh, ah = fingerprint(rotated)
                refs.append({
                    "reference_id": "sticker-" + serial, "reference_source_sha256": actual,
                    "reference_crop_fraction": list(coords),
                    "reference_rotation_degrees": angle,
                    "dhash": dh, "ahash": ah,
                    "crop_aspect": round(rotated.width / rotated.height, 3),
                })
    return refs


def proxy_image(image: Image.Image, long_side: int = PROXY_LONG_SIDE) -> Image.Image:
    if not 32 <= long_side <= 4096:
        raise ValueError("proxy long-side bound must be 32..4096")
    if image.width * image.height > Image.MAX_IMAGE_PIXELS:
        raise ValueError("candidate image pixel cap exceeded")
    copy = ImageOps.exif_transpose(image).convert("RGB")
    if max(copy.size) > long_side:
        copy.thumbnail((long_side, long_side), Image.Resampling.LANCZOS)
    return copy


def strata(image_width: int, image_height: int) -> list[dict]:
    """Bounded overlapping squareish regions; count ALL proposals before sampling."""
    shorter = min(image_width, image_height)
    groups = []
    for scale in FRACTIONS:
        h = round(shorter * scale)
        for aspect in ASPECTS:
            w = round(h * aspect)
            if min(w, h) < MIN_SIDE or w > image_width or h > image_height:
                continue
            stride = max(8, round(min(w, h) * 0.29))
            xs = list(range(0, image_width - w + 1, stride))
            ys = list(range(0, image_height - h + 1, stride))
            if xs[-1] != image_width - w:
                xs.append(image_width - w)
            if ys[-1] != image_height - h:
                ys.append(image_height - h)
            # Sample evenly later, not only top-left or the smallest scale.
            boxes = [(x, y, x+w, y+h) for y in ys for x in xs]
            groups.append({"scale": scale, "aspect": aspect, "boxes": boxes})
    return groups


def select_windows(width: int, height: int, max_windows: int) -> tuple[list[tuple[int,int,int,int]], dict]:
    if max_windows <= 0 or max_windows > 10000:
        raise ValueError("max_windows must be 1..10000")
    groups = strata(width, height)
    all_count = sum(len(g["boxes"]) for g in groups)
    if all_count <= max_windows:
        selection = [box for g in groups for box in g["boxes"]]
    else:
        # Round-robin scales and aspect ratios. A narrow global cap must not
        # silently remove all large/small regions or every later source group.
        per = [len(g["boxes"]) for g in groups]
        allocations = [0] * len(groups)
        remaining = max_windows
        while remaining:
            available = [i for i, n in enumerate(per) if allocations[i] < n]
            if not available:
                break
            for idx in available:
                if not remaining:
                    break
                allocations[idx] += 1
                remaining -= 1
        selection = []
        for group, amount in zip(groups, allocations):
            n = len(group["boxes"])
            for i in range(amount):
                pos = ((2*i+1)*n)//(2*amount)
                selection.append(group["boxes"][min(n-1, pos)])
    return selection, {
        "proposed_windows": all_count,
        "scored_windows": len(selection),
        "windows_omitted_at_cap": all_count - len(selection),
        "strata_available": len(groups),
        "strata_sampled": len({(b[2]-b[0], b[3]-b[1]) for b in selection}),
        "not_exhaustive_when_capped": all_count > max_windows,
    }


def box_iou(a: list[int], b: list[int]) -> float:
    w = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = w*h
    if not intersection:
        return 0.0
    area_a = (a[2]-a[0])*(a[3]-a[1])
    area_b = (b[2]-b[0])*(b[3]-b[1])
    return intersection/(area_a + area_b - intersection)


def refine_windows(first_pass: list[tuple], width: int, height: int,
                   max_refine_windows: int = 1200) -> tuple[list[tuple[int,int,int,int]], dict]:
    """Coarse-to-fine second pass around spatially distinct low-distance hints.

    Deliberately reconsiders larger boxes around partial-hit regions: a hash
    matched against the inner mark can be more competitive than the full paper.
    It is a bounded proposal generator, not a proof of detector recall.
    """
    if not 0 <= max_refine_windows <= 5000:
        raise ValueError("max_refine_windows must be 0..5000")
    seeds = []
    for _, _, _, bbox, _ in first_pass:
        if any(box_iou(bbox, x) > .55 for x in seeds):
            continue
        seeds.append(bbox)
        if len(seeds) >= 16:
            break
    buckets = []
    for x1,y1,x2,y2 in seeds:
        cx,cy=(x1+x2)/2,(y1+y2)/2
        proposals = []
        for zoom in (0.75,1.0,1.35,1.7,2.0):
            for aspect in ASPECTS:
                h=max(MIN_SIDE,round((y2-y1)*zoom))
                w=max(MIN_SIDE,round(h*aspect))
                if w>width or h>height:
                    continue
                for dy in (-0.25,0.0,0.25):
                    for dx in (-0.25,0.0,0.25):
                        bx=min(max(0,round(cx-w/2+dx*w)),width-w)
                        by=min(max(0,round(cy-h/2+dy*h)),height-h)
                        proposals.append((bx,by,bx+w,by+h))
        buckets.append(list(dict.fromkeys(proposals)))
    total=sum(len(b) for b in buckets)
    if total <= max_refine_windows:
        selected=[box for bucket in buckets for box in bucket]
    else:
        # Equal opportunities for distinct hint locations and spatially
        # stratified sampling *inside* each seed's multiscale proposal set.
        allocated=[0]*len(buckets)
        remaining=max_refine_windows
        while remaining:
            active=[i for i,bucket in enumerate(buckets) if allocated[i]<len(bucket)]
            if not active:
                break
            for i in active:
                if not remaining:
                    break
                allocated[i]+=1
                remaining-=1
        selected=[]
        for bucket,n in zip(buckets,allocated):
            for i in range(n):
                selected.append(bucket[min(len(bucket)-1,((2*i+1)*len(bucket))//(2*n))])
    unique=list(dict.fromkeys(selected))
    return unique,{
        "refinement_seeds":len(seeds),
        "refinement_windows_proposed":total,
        "refinement_windows_scored":len(unique),
        "refinement_omitted_at_cap":max(0,total-len(selected)),
        "refinement_not_exhaustive_when_capped":total>max_refine_windows,
    }


def scan(image: Image.Image, references: list[dict], *, max_windows: int = 1600,
         max_suggestions: int = 8, long_side: int = PROXY_LONG_SIDE,
         max_refine_windows: int = 1200) -> tuple[list[dict], dict]:
    if not references:
        raise ValueError("no region references")
    if not 1 <= max_suggestions <= 50:
        raise ValueError("max_suggestions must be 1..50")
    proxy = proxy_image(image, long_side=long_side)
    boxes, coverage = select_windows(proxy.width, proxy.height, max_windows)
    possibilities = []
    def rank_box(box):
        dh, ah = fingerprint(proxy.crop(box))
        for ref in references:
            d = (dh ^ ref["dhash"]).bit_count()
            h = (ah ^ ref["ahash"]).bit_count()
            score = d+h
            # All accepted low-distance proposals remain review-only.
            if score <= 65:
                possibilities.append((score, d, h, box, ref))
    for box in boxes:
        rank_box(box)
    possibilities.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]["reference_id"]))
    refined, refine_coverage = refine_windows(
        possibilities, proxy.width, proxy.height, max_refine_windows)
    existing=set(boxes)
    unique_refined=[box for box in refined if box not in existing]
    for box in unique_refined:
        rank_box(box)
    coverage.update(refine_coverage)
    coverage["refinement_windows_new_after_coarse_overlap"] = len(unique_refined)
    coverage["total_windows_fingerprinted"] = len(boxes) + len(unique_refined)
    possibilities.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]["reference_id"]))
    chosen = []
    oriented_size = ImageOps.exif_transpose(image).size
    sx = oriented_size[0] / proxy.width
    sy = oriented_size[1] / proxy.height
    for score,d,h,box,ref in possibilities:
        original = [round(box[0]*sx), round(box[1]*sy),
                    round(box[2]*sx), round(box[3]*sy)]
        if any(box_iou(original, item["bbox_xyxy_original_pixels"]) > .45 for item in chosen):
            continue
        chosen.append({
            "bbox_xyxy_original_pixels": original,
            "coordinate_system": "exif-oriented-source-image-pixels",
            "reference_id": ref["reference_id"],
            "reference_rotation_degrees": ref["reference_rotation_degrees"],
            "hash_distance_sum": score,
            "dhash_distance": d, "ahash_distance": h,
            "evidence_grade": "unvalidated-region-similarity-only",
            "new_sticker_confirmed": False,
        })
        if len(chosen) >= max_suggestions:
            break
    coverage.update({
        "proxy_width": proxy.width, "proxy_height": proxy.height,
        "suggestions_shown": len(chosen),
        "candidate_regions_ranking": "low-hash-distance-only; uncalibrated",
    })
    return chosen, coverage


def diverse_candidates(items: list[dict], max_files: int) -> list[dict]:
    """Round-robin original source groups, not alphabetical media file paths.

    A large batch of files from one early seller must not consume every scan
    slot while an independent collector's image never gets examined.
    """
    if not 1 <= max_files <= 200:
        raise ValueError("max_files must be 1..200")
    groups = {}
    for item in items:
        key = str(item.get("source_kind") or item.get("source_url") or "unknown-source")
        groups.setdefault(key, []).append(item)
    keys = sorted(groups)
    chosen = []
    for depth in range(max(map(len, groups.values()), default=0)):
        for key in keys:
            if depth < len(groups[key]):
                chosen.append(groups[key][depth])
                if len(chosen) == max_files:
                    return chosen
    return chosen


def run(index: dict, refs: list[dict], candidates_root: Path,
        *, max_files: int = 48, max_windows: int = 1600,
        max_refine_windows: int = 1200) -> dict:
    if not 1 <= max_files <= 200:
        raise ValueError("max_files must be 1..200")
    source = index.get("candidates", [])
    if not isinstance(source, list):
        raise ValueError("candidate index requires array")
    root = candidates_root.resolve()
    results, errors = [], []
    selection = diverse_candidates(source, max_files)
    for item in selection:
        ident = item.get("id", "")
        if not isinstance(ident, str) or not ident:
            errors.append({"id": str(ident), "failure": "missing_candidate_id"})
            continue
        path = (root / str(item.get("path",""))).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append({"id":ident, "failure":"unavailable_or_unsafe_image"})
            continue
        if not item.get("sha256") or sha256(path) != item["sha256"]:
            errors.append({"id":ident, "failure":"source_digest_mismatch"})
            continue
        try:
            with Image.open(path) as img:
                img.load()
                hits, stats = scan(img, refs, max_windows=max_windows,
                                   max_refine_windows=max_refine_windows)
            results.append({"candidate_id":ident, "source_url":item.get("source_url",""),
                            "source_kind":item.get("source_kind",""),
                            "suggestions":hits, "coverage":stats})
        except (ValueError,OSError,UnidentifiedImageError,Image.DecompressionBombError) as exc:
            errors.append({"id":ident, "failure":type(exc).__name__,
                           "detail":str(exc)[:140]})
    return {
        "schema_version":1, "method":"review-only-rotated-multiscale-dhash-ahash",
        "reference_variants":len(refs), "candidate_files_available":len(source),
        "candidate_files_selected":len(selection),
        "source_groups_selected":len({str(x.get("source_kind") or x.get("source_url") or "unknown-source") for x in selection}),
        "candidate_files_not_scanned_by_cap":max(0,len(source)-max_files),
        "candidate_files_scanned":len(results),
        "errors":errors, "candidates":results,
        "new_confirmed_stickers":0,
        "limitations":"unvalidated similarity: overlapping crops, sampling and generic marks yield false positives; no serial reading, no distinct-object or owner inference",
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--roi-manifest",type=Path,
                   default=Path("data/reference/inside-ce-sticker-region-pilot-rois.csv"))
    p.add_argument("--candidate-index",type=Path,default=Path("visual-evidence-work/candidate-index.json"))
    p.add_argument("--candidates",type=Path,default=Path("evidence-work"))
    p.add_argument("--output",type=Path,default=Path("visual-evidence-work/region-suggestions.json"))
    p.add_argument("--max-files",type=int,default=48)
    p.add_argument("--max-windows",type=int,default=1600)
    p.add_argument("--max-refine-windows",type=int,default=1200)
    args=p.parse_args()
    repo=args.repo_root.resolve()
    manifest=args.roi_manifest if args.roi_manifest.is_absolute() else repo/args.roi_manifest
    refs=load_regions(manifest,repo)
    result=run(json.loads(args.candidate_index.read_text(encoding="utf-8")),
               refs,args.candidates,max_files=args.max_files,max_windows=args.max_windows,
               max_refine_windows=args.max_refine_windows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "candidate_files_scanned":result["candidate_files_scanned"],
        "candidate_files_not_scanned_by_cap":result["candidate_files_not_scanned_by_cap"],
        "reference_variants":len(refs),"errors":len(result["errors"]),
        "new_confirmed_stickers":0},sort_keys=True))


if __name__=="__main__":
    main()

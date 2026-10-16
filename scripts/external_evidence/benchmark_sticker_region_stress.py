#!/usr/bin/env python3
"""Offline sticker-region specificity and small-in-scene challenge, NOT detector QA.

Four source-pinned physically distinct holdout sticker crops are pasted into
synthetic clutter at 1%, 3%, and 8% image area, with predeclared placements.
Four sticker-free synthetic adversarial scenes assess spurious proposal rates.
The test is not a real-world negative or tiny original-scene benchmark.
No networking, model, OCR, author/owner identification, or verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

if __package__:
    from .visual_region_probe import box_iou, load_regions, scan
    from .benchmark_sticker_region_holdout import load_holdouts
else:
    from visual_region_probe import box_iou, load_regions, scan
    from benchmark_sticker_region_holdout import load_holdouts

SIZE = (720, 540)
# Fix a priori. Do not choose operating points after seeing these results.
PATCH_FRACTIONS = (0.01, 0.03, 0.08)
DISTANCE_CUTOFFS = (24, 32, 40, 48, 56, 65)
NEGATIVE_KINDS = ("cluttered-table", "paper-product-box", "lettered-bar-label",
                  "ticket-with-slash")
IOU_CUTOFF = 0.40


def scene_background(kind: str) -> Image.Image:
    if kind not in NEGATIVE_KINDS:
        raise ValueError("unknown synthetic negative kind")
    im = Image.new("RGB", SIZE, (57, 64, 68))
    d = ImageDraw.Draw(im)
    # Deterministic texture and visually plausible product/desk objects.
    for i in range(12):
        x = (37 + 89*i) % SIZE[0]
        y = (61 + 71*i) % SIZE[1]
        d.line([(x, y), (min(SIZE[0]-1, x+70), min(SIZE[1]-1, y+15))],
               fill=(76+i*3, 70+i*2, 67+i*2), width=2)
    d.rectangle([25, 25, 205, 139], fill=(143, 118, 94))
    d.rectangle([28, 32, 198, 132], outline=(185, 162, 140), width=4)
    d.ellipse([270, 31, 405, 165], fill=(125, 34, 42))
    d.rectangle([545, 378, 697, 516], fill=(31, 42, 50))
    if kind == "cluttered-table":
        d.rectangle([487, 56, 665, 176], fill=(155, 151, 144))
        d.line([495, 101, 654, 101], fill=(48, 56, 64), width=4)
    elif kind == "paper-product-box":
        d.rectangle([387, 205, 575, 443], fill=(230, 229, 224))
        d.rectangle([409, 246, 551, 266], fill=(33, 37, 43))
        d.text((410, 390), "GAME CASE 2020", fill=(31, 34, 42))
    elif kind == "lettered-bar-label":
        d.rectangle([376, 197, 571, 397], fill=(238, 238, 233))
        d.line([400, 293, 551, 293], fill=(26, 30, 34), width=14)
        d.text((445, 368), "A-023", fill=(40, 40, 40))
    elif kind == "ticket-with-slash":
        d.rectangle([367, 196, 572, 398], fill=(230, 231, 222))
        d.polygon([(421, 327), (447, 327), (524, 235), (498, 235)],
                  fill=(26, 28, 29))
        d.text((445, 363), "TICKET 061", fill=(26, 28, 29))
    return im


def crop_holdout(case: dict, repo_root: Path) -> Image.Image:
    path = (repo_root / case["source_path"]).resolve()
    with Image.open(path) as original:
        photo = ImageOps.exif_transpose(original).convert("RGB")
        w, h = photo.size
        l,t,r,b = case["ground_truth_box_fraction"]
        box = (round(l*w),round(t*h),round(r*w),round(b*h))
        if min(box[2]-box[0], box[3]-box[1]) < 20:
            raise ValueError("holdout sticker crop too small")
        return photo.crop(box)


def composite(case: dict, repo_root: Path, fraction: float, index: int) -> tuple[Image.Image, list[int]]:
    if fraction not in PATCH_FRACTIONS:
        raise ValueError("unfrozen patch area fraction")
    scene = scene_background("cluttered-table")
    crop = crop_holdout(case, repo_root)
    if index % 2:
        crop = crop.transpose(Image.Transpose.ROTATE_90)
    area = SIZE[0] * SIZE[1] * fraction
    ratio = crop.width / crop.height
    width = round(math.sqrt(area*ratio))
    height = round(math.sqrt(area/ratio))
    if min(width,height) < 20:
        raise ValueError("composite crop too small to score")
    patch = crop.resize((width,height), Image.Resampling.LANCZOS)
    locations = ((.06,.57),(.56,.37),(.72,.09),(.32,.64))
    fx,fy=locations[index%len(locations)]
    x=min(round(fx*SIZE[0]), SIZE[0]-width)
    y=min(round(fy*SIZE[1]), SIZE[1]-height)
    scene.paste(patch,(x,y))
    return scene, [x,y,x+width,y+height]


def challenge(reference_rows: list[dict], holdout_rows: list[dict], root: Path,
              *, max_windows: int = 1600, max_refine_windows: int = 1200,
              top_k: int = 8) -> dict:
    if len({r["reference_id"] for r in reference_rows}) != 5:
        raise ValueError("stress benchmark expects five frozen reference photographs")
    if {h["serial"] for h in holdout_rows} != {"039","047","063","118"}:
        raise ValueError("stress benchmark expects exactly four independent held-outs")
    if top_k != 8 or max_windows != 1600 or max_refine_windows != 1200:
        raise ValueError("stress budgets and top-k are frozen; changes require a versioned benchmark")
    positives, negatives = [], []
    for i,case in enumerate(sorted(holdout_rows,key=lambda x:x["serial"])):
        for j,fraction in enumerate(PATCH_FRACTIONS):
            scene, truth = composite(case, root, fraction, i+j)
            proposals, stats = scan(scene,reference_rows,
                                    max_windows=max_windows,
                                    max_refine_windows=max_refine_windows,
                                    max_suggestions=top_k)
            scored = [{
                "distance":p["hash_distance_sum"],
                "iou":round(box_iou(truth,p["bbox_xyxy_original_pixels"]),5),
            } for p in proposals]
            positives.append({
                "control":case["serial"], "area_fraction":fraction,
                "placement_variant":(i+j)%4, "gt_box":truth,
                "paper_area_fraction_of_frame":round((truth[2]-truth[0])*(truth[3]-truth[1])/(SIZE[0]*SIZE[1]),5),
                "best_iou":max([x["iou"] for x in scored],default=0),
                "hits_at_040":sum(x["iou"]>=IOU_CUTOFF for x in scored),
                "topk_distances_and_ious":scored,
                "coverage":stats, "verified_sticker":False,
            })
    for kind in NEGATIVE_KINDS:
        scene = scene_background(kind)
        suggestions, stats = scan(scene,reference_rows,
                                  max_windows=max_windows,
                                  max_refine_windows=max_refine_windows,
                                  max_suggestions=top_k)
        negatives.append({
            "synthetic_control":kind, "physical_sticker_present":False,
            "proposals_on_sticker_free_image":len(suggestions),
            "distances":[x["hash_distance_sum"] for x in suggestions],
            "coverage":stats,
            "verified_sticker":False,
        })
    curve=[]
    for cutoff in DISTANCE_CUTOFFS:
        found=sum(any(hit["distance"]<=cutoff and hit["iou"]>=IOU_CUTOFF
                      for hit in case["topk_distances_and_ious"]) for case in positives)
        false=sum(any(d<=cutoff for d in neg["distances"]) for neg in negatives)
        curve.append({
            "max_hash_distance":cutoff,
            "synthetic_positive_localization_hits":found,
            "synthetic_positive_total":len(positives),
            "synthetic_negative_images_with_a_proposal":false,
            "synthetic_negative_total":len(negatives),
        })
    return {
        "schema_version":1, "benchmark":"frozen-tiny-sticker-and-adversarial-synthetic-scenes",
        "reference_original_photographs":5,
        "holdout_original_photographs_used_as_source_crops":4,
        "synthetic_small_sticker_composites":len(positives),
        "synthetic_negative_photographs":len(negatives),
        "negative_images_are_real_original_photographs":False,
        "positives_are_original_uncropped_collector_photographs":False,
        "matching_window_budget":{"coarse":max_windows,"refined":max_refine_windows,"top_k":top_k},
        "localization_iou_threshold":IOU_CUTOFF,
        "area_fractions":list(PATCH_FRACTIONS),
        "distance_operating_points":curve,
        "positive_cases":positives, "negative_cases":negatives,
        "unthresholded_top8_positive_localizations_at_iou_040":sum(c["best_iou"]>=IOU_CUTOFF for c in positives),
        "unthresholded_top8_negative_images_with_proposals":sum(n["proposals_on_sticker_free_image"]>0 for n in negatives),
        "new_confirmed_stickers":0,
        "limitation":"only synthetic scenes; hard negatives visually overlap real sticker designs; not independent real-world specificity or tiny scene recall",
    }


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root",type=Path,default=Path("."))
    ap.add_argument("--output",type=Path,default=Path("visual-evidence-work/region-specificity-stress.json"))
    args=ap.parse_args()
    root=args.repo_root.resolve()
    refs=load_regions(root/"data/reference/inside-ce-sticker-region-pilot-rois.csv",root)
    cases=load_holdouts(root/"data/reference/inside-ce-sticker-region-independent-holdout.csv",
                        root,{r["reference_id"] for r in refs})
    report=challenge(refs,cases,root)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k in (
        "benchmark","synthetic_small_sticker_composites","synthetic_negative_photographs",
        "unthresholded_top8_positive_localizations_at_iou_040",
        "unthresholded_top8_negative_images_with_proposals","distance_operating_points",
        "new_confirmed_stickers")},sort_keys=True))


if __name__=="__main__":
    main()

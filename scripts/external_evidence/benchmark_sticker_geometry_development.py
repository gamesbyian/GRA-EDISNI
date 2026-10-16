#!/usr/bin/env python3
"""Measure geometric paper proposals on frozen previously-examined CE challenges.

This is an exploratory DEVELOPMENT SET comparison: previous hash benchmark has
already exposed these 12 composites / 4 negatives. Metrics must never be
described as independent new detector accuracy. The method sees neither serials
nor reference source labels; it is a rectangle proposal engine only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image,ImageOps

if __package__:
    from .visual_geometry_proposals import propose
    from .visual_region_probe import box_iou,load_regions
    from .benchmark_sticker_region_holdout import load_holdouts
    from .benchmark_sticker_region_stress import (PATCH_FRACTIONS,NEGATIVE_KINDS,
                                                  composite,scene_background)
else:
    from visual_geometry_proposals import propose
    from visual_region_probe import box_iou,load_regions
    from benchmark_sticker_region_holdout import load_holdouts
    from benchmark_sticker_region_stress import (PATCH_FRACTIONS,NEGATIVE_KINDS,
                                                 composite,scene_background)

IOU=.40


def measure(root:Path, *, max_proposals:int=8) -> dict:
    if max_proposals!=8:
        raise ValueError("same-review-budget geometry benchmark is frozen at top 8")
    refs=load_regions(root/"data/reference/inside-ce-sticker-region-pilot-rois.csv",root)
    cases=load_holdouts(root/"data/reference/inside-ce-sticker-region-independent-holdout.csv",
                        root,{x["reference_id"] for x in refs})
    positives=[]
    for i,case in enumerate(sorted(cases,key=lambda x:x["serial"])):
        for j,fraction in enumerate(PATCH_FRACTIONS):
            scene,ground_truth=composite(case,root,fraction,i+j)
            proposals,counts=propose(scene,max_proposals=max_proposals)
            ious=[round(box_iou(p["bbox_xyxy_original_pixels"],ground_truth),5)
                  for p in proposals]
            positives.append({
                "original_holdout_serial_only_for_benchmark":case["serial"],
                "source_photo_sha256":case["source_sha256"],
                "area_fraction":fraction,"best_iou":max(ious,default=0.0),
                "localized_at_iou_040":any(x>=IOU for x in ious),
                "positions_proposed":len(proposals),
                "proposals":proposals,"window_accounting":counts,
                "new_sticker_confirmed":False,
            })
    negatives=[]
    for kind in NEGATIVE_KINDS:
        proposals,counts=propose(scene_background(kind),max_proposals=max_proposals)
        negatives.append({
            "synthetic_negative_type":kind,
            "false_visual_prompts_in_review_queue":len(proposals),
            "at_least_one_false_visual_prompt":bool(proposals),
            "proposals":proposals,"window_accounting":counts,
            "new_sticker_confirmed":False,
        })
    physical=[]
    for case in sorted(cases,key=lambda x:x["serial"]):
        with Image.open(root/case["source_path"]) as raw:
            img=ImageOps.exif_transpose(raw).copy()
        box=[round(case["ground_truth_box_fraction"][i]*
                   (img.width if i%2==0 else img.height)) for i in range(4)]
        proposals,counts=propose(img,max_proposals=max_proposals)
        overlaps=[round(box_iou(box,p["bbox_xyxy_original_pixels"]),5)
                  for p in proposals]
        physical.append({
            "holdout_original_photo":case["serial"],"source_sha256":case["source_sha256"],
            "best_iou":max(overlaps,default=0),"localized_at_iou_040":any(x>=IOU for x in overlaps),
            "proposals":proposals,"window_accounting":counts,
            "new_sticker_confirmed":False,
        })
    per_area=[{"paper_area_fraction":f,
               "localized":sum(row["localized_at_iou_040"]
                               for row in positives if row["area_fraction"]==f),
               "examined":sum(row["area_fraction"]==f for row in positives)}
              for f in PATCH_FRACTIONS]
    return {
        "schema_version":1,
        "method":"cpu-opencv-bright-paper-contour-proposal",
        "evaluation_status":"previously-observed-development-composites-and-known-original-photos; NOT unseen validation",
        "top_k_review_budget":max_proposals,
        "positive_composite_total":len(positives),
        "positive_composite_localized_iou_040":sum(x["localized_at_iou_040"] for x in positives),
        "per_area_localization":per_area,
        "synthetic_negative_total":len(negatives),
        "synthetic_negative_images_with_false_visual_prompts":sum(
            x["at_least_one_false_visual_prompt"] for x in negatives),
        "independent_real_original_positive_total":len(physical),
        "independent_real_original_localized_iou_040":sum(
            x["localized_at_iou_040"] for x in physical),
        "independent_real_negative_total":0,
        "actual_real_negative_false_prompt_rate_established":False,
        "comparison_note":"baseline hash previous 8/12 synthetic positives at IoU .4, 4/4 negatives prompted; source 4/4 large frontal positives at IoU .6. Different algorithm, same 8 review proposals, development data already inspected",
        "new_confirmed_stickers":0,
        "positive_cases":positives,"negative_cases":negatives,"physical_originals":physical,
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--out",type=Path,default=Path("visual-evidence-work/geometry-developments.json"))
    args=p.parse_args()
    result=measure(args.repo_root.resolve())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in (
        "positive_cases","negative_cases","physical_originals")},sort_keys=True))


if __name__=="__main__":
    main()

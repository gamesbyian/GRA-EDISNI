#!/usr/bin/env python3
"""Measure ROI localizer on DIFFERENT physically photographed CE stickers.

Hold-out originals must have sticker-paper boundaries manually annotated,
SHA-pinned, and never appear among query/reference templates. Reports measured
box overlap only. It NEVER identifies the candidate's printed serial.
No external media access, OCR, model download or owner communication.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageOps

if __package__:
    from .visual_region_probe import box_iou, load_regions, scan, sha256
else:
    from visual_region_probe import box_iou, load_regions, scan, sha256


def load_holdouts(path: Path, root: Path, reference_ids: set[str]) -> list[dict]:
    with path.open(encoding="utf-8",newline="") as stream:
        rows=list(csv.DictReader(stream))
    if not rows:
        raise ValueError("empty independent original-photo holdout")
    found=set()
    results=[]
    root=root.resolve()
    for row in rows:
        serial=row.get("serial","")
        if serial in found or len(serial)!=3 or not serial.isdecimal():
            raise ValueError("duplicate or invalid holdout serial")
        found.add(serial)
        if "sticker-"+serial in reference_ids:
            raise ValueError("a held-out photograph is also in the reference training set")
        if row.get("annotation_status")!="source-photo-paper-boundary-inspected-2026-10-16":
            raise ValueError("uninspected ground-truth sticker boundary")
        if row.get("benchmark_role")!="independent-known-physical-sticker-positive":
            raise ValueError("unsupported known-positive benchmark role")
        source=(root/row["source_path"]).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError("held-out original path unavailable or unsafe")
        if not source.relative_to(root).as_posix().startswith("archive/stickers/originals/"):
            raise ValueError("held-out photograph must be an original")
        if sha256(source)!=row["source_sha256"]:
            raise ValueError("held-out original digest mismatch")
        frac=[float(row[key]) for key in ("left","top","right","bottom")]
        if not (0<=frac[0]<frac[2]<=1 and 0<=frac[1]<frac[3]<=1):
            raise ValueError("bad held-out ground-truth paper bounds")
        results.append({"serial":serial, "source_path":row["source_path"],
                        "source_sha256":row["source_sha256"],
                        "ground_truth_box_fraction":frac})
    return results


def evaluate_holdouts(holdouts: list[dict], refs: list[dict], root: Path,
                      *, max_windows: int=1600, max_refine_windows: int=1200,
                      top_k: int=8) -> dict:
    output=[]
    for case in holdouts:
        source=(root/case["source_path"]).resolve()
        with Image.open(source) as raw:
            oriented=ImageOps.exif_transpose(raw)
            w,h=oriented.size
            true=[round(case["ground_truth_box_fraction"][i]*(w if i%2==0 else h))
                  for i in range(4)]
            suggestions, coverage=scan(raw,refs,max_windows=max_windows,
                                       max_refine_windows=max_refine_windows,
                                       max_suggestions=top_k)
        overlaps=[round(box_iou(true,p["bbox_xyxy_original_pixels"]),5)
                  for p in suggestions]
        output.append({
            "known_holdout_serial_for_evaluation_only":case["serial"],
            "original_source_path":case["source_path"],
            "source_sha256":case["source_sha256"],
            "ground_truth_xyxy_original_pixels":true,
            "top1_box_iou":overlaps[0] if overlaps else 0.,
            "best_topk_box_iou":max(overlaps,default=0.),
            "hit_at_iou_025":any(x>=.25 for x in overlaps),
            "hit_at_iou_040":any(x>=.40 for x in overlaps),
            "hit_at_iou_060":any(x>=.60 for x in overlaps),
            "topk_iou":overlaps,
            "reference_templates_disjoint":True,
            "suggestions":suggestions,
            "coverage":coverage,
            "new_sticker_confirmed":False,
        })
    n=len(output)
    summary={
        "schema_version":1,
        "benchmark_kind":"physically_distinct_original-sticker-photo-held-out",
        "holdout_photographs":n,
        "reference_unique_photographs":len(set(r["reference_id"] for r in refs)),
        "reference_vs_holdout_serial_disjoint":True,
        "top_k":top_k,
        "max_windows_per_photo":max_windows,
        "max_refine_windows_per_photo":max_refine_windows,
        "detected_at_iou_025":sum(c["hit_at_iou_025"] for c in output),
        "detected_at_iou_040":sum(c["hit_at_iou_040"] for c in output),
        "detected_at_iou_060":sum(c["hit_at_iou_060"] for c in output),
        "mean_best_iou":round(sum(c["best_topk_box_iou"] for c in output)/n,5) if n else None,
        "independent_negative_photographs_evaluated":0,
        "false_positive_rate_measured":False,
        "evidence_limit":"four known-positive different-photo paper-box localizations only; not serial or sticker classifier, no negative photo controls",
        "new_confirmed_stickers":0,
    }
    return {"summary":summary,"cases":output}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--reference-manifest",type=Path,
                   default=Path("data/reference/inside-ce-sticker-region-pilot-rois.csv"))
    p.add_argument("--holdout-manifest",type=Path,
                   default=Path("data/reference/inside-ce-sticker-region-independent-holdout.csv"))
    p.add_argument("--max-windows",type=int,default=1600)
    p.add_argument("--max-refine-windows",type=int,default=1200)
    p.add_argument("--top-k",type=int,default=8)
    p.add_argument("--output",type=Path,default=Path("visual-evidence-work/region-independent-holdout.json"))
    args=p.parse_args()
    root=args.repo_root.resolve()
    ref=args.reference_manifest if args.reference_manifest.is_absolute() else root/args.reference_manifest
    hold=args.holdout_manifest if args.holdout_manifest.is_absolute() else root/args.holdout_manifest
    references=load_regions(ref,root)
    holdouts=load_holdouts(hold,root,{r["reference_id"] for r in references})
    result=evaluate_holdouts(holdouts,references,root,max_windows=args.max_windows,
                              max_refine_windows=args.max_refine_windows,top_k=args.top_k)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result["summary"],sort_keys=True))


if __name__=="__main__":
    main()

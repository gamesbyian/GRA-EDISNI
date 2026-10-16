#!/usr/bin/env python3
"""Descriptive OCR-free ink-layout research on original CE paper photographs.

No model fit, rejection threshold, accuracy/FPR metric, serial OCR or owners.
The physical positive photos were previously examined, and simulated negative
cards/tickets were already used for geometry development. Do NOT claim blind
generalization from differences in these descriptive distributions.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
from statistics import median

from PIL import Image,ImageOps

if __package__:
    from .visual_ink_layout import ink_layout
    from .visual_region_probe import sha256
    from .benchmark_sticker_region_stress import scene_background
    from .benchmark_sliced_geometry_new_sources import background as wide_background
else:
    from visual_ink_layout import ink_layout
    from visual_region_probe import sha256
    from benchmark_sticker_region_stress import scene_background
    from benchmark_sliced_geometry_new_sources import background as wide_background


MANIFESTS=(
    "data/reference/inside-ce-sticker-region-pilot-rois.csv",
    "data/reference/inside-ce-sticker-region-independent-holdout.csv",
    "data/reference/inside-ce-novel-tiny-paper-crop-holdouts-20261016.csv",
)
SIMULATED_NEGATIVES={
    "cluttered-table":[487,56,665,176],
    "paper-product-box":[387,205,575,443],
    "lettered-bar-label":[376,197,571,397],
    "ticket-with-slash":[367,196,572,398],
}
WIDE_NEGATIVES={
    "plain-dark":[1038,60,1377,437],
    "game-case":[870,430,1220,876],
    "shipping-ticket":[793,470,1167,830],
    "bright-collector-art":[752,428,1120,778],
}


def source_cases(root:Path)->list[dict]:
    result=[];seen=set()
    for manifest in MANIFESTS:
        with (root/manifest).open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f))
        for row in rows:
            ident=row["serial"]
            if ident in seen:
                raise ValueError("physical source overlap between manifests")
            seen.add(ident)
            if row.get("roi_review_status") not in ("visually-inspected-2026-10-16",None):
                raise ValueError("source crop reference not reviewed")
            if row.get("annotation_status") not in ("source-photo-paper-boundary-inspected-2026-10-16",None):
                raise ValueError("holdout crop not reviewed")
            if row.get("annotation_grade") not in ("visually-inspected-2026-10-16",None):
                raise ValueError("novel crop not reviewed")
            path=(root/row["source_path"]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError("missing or unsafe original physical source")
            if not path.relative_to(root).as_posix().startswith("archive/stickers/originals/"):
                raise ValueError("not an original source")
            if sha256(path)!=row["source_sha256"]:
                raise ValueError("physical original digest mismatch")
            with Image.open(path) as raw:
                original=ImageOps.exif_transpose(raw).convert("RGB")
                l,t,r,b=[float(row[k]) for k in ("left","top","right","bottom")]
                coords=[round(l*original.width),round(t*original.height),
                        round(r*original.width),round(b*original.height)]
                roi=original.crop(coords)
                features=ink_layout(roi)
            result.append({
                "source_sticker_known_serial_for_annotation_only":ident,
                "original_source_path":row["source_path"],
                "source_sha256":row["source_sha256"],
                "paper_bbox_fraction":[l,t,r,b],
                "kind":"previously-known-and-inspected-original-CE-sticker",
                "ink_features":features,
                "new_sticker_confirmed":False,
            })
    return result


def benchmark(root:Path)->dict:
    original=source_cases(root)
    negatives=[]
    for kind,box in SIMULATED_NEGATIVES.items():
        image=scene_background(kind)
        negatives.append({
            "name":"old-"+kind,
            "kind":"previously-examined-synthetic-non-sticker-paper",
            "roi_box":box,"ink_features":ink_layout(image.crop(box)),
            "new_sticker_confirmed":False})
    for kind,box in WIDE_NEGATIVES.items():
        image=wide_background(kind)
        negatives.append({
            "name":"wide-"+kind,
            "kind":"source-free-generated-non-sticker-object",
            "roi_box":box,"ink_features":ink_layout(image.crop(box)),
            "new_sticker_confirmed":False})
    def overview(rows:list[dict])->dict:
        zone_names=("top_margin","center_mark","bottom_print","edge_band")
        return {
            name:{
                "median_dark_fraction":round(median(
                    item["ink_features"]["dark_pixel_fractions_by_zone"][name]
                    for item in rows),6),
                "minimum":min(item["ink_features"]["dark_pixel_fractions_by_zone"][name]
                              for item in rows),
                "maximum":max(item["ink_features"]["dark_pixel_fractions_by_zone"][name]
                              for item in rows),
            } for name in zone_names}
    return {
        "schema_version":1,"method":"uncalibrated-three-band-printed-ink-layout",
        "physical_sticker_originals":len(original),
        "generated_negative_region_crops":len(negatives),
        "distinct_original_sticker_ids":sorted(x["source_sticker_known_serial_for_annotation_only"]
                                              for x in original),
        "descriptive_zone_distribution_by_known_class":{
            "known_original_sticker_photo_crop":overview(original),
            "generated_unrelated_paper_or_packaging_crop":overview(negatives)},
        "real_original_negative_photos_examined":0,
        "learned_score_fitted":False,"classification_accuracy_measured":False,
        "claim":"describes centered mark and bottom print placement only; no OCR, serial, or CE proof",
        "new_confirmed_stickers":0,
        "original_photo_controls":original,
        "simulated_negative_controls":negatives,
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--out",type=Path,default=Path("visual-evidence-work/ink-layout-exploration.json"))
    args=p.parse_args()
    report=benchmark(args.repo_root.resolve())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ("original_photo_controls","simulated_negative_controls")},sort_keys=True))


if __name__=="__main__":
    main()

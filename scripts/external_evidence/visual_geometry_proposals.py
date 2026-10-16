#!/usr/bin/env python3
"""CPU-only paper-rectangle proposal experiment on already-approved images.

Adapted from the contour/connected-region strategy documented by OpenCV.
This deliberately proposes *generic light rectangular surfaces*, NOT stickers:
plain paper, game cases, tickets and shipping labels can all match.

No OCR, models, network, owner association, serial inference or verification.
Requires opt-in opencv-python-headless (not imported by normal hash pipeline).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

if __package__:
    from .visual_region_probe import proxy_image, sha256, box_iou, diverse_candidates
else:
    from visual_region_probe import proxy_image, sha256, box_iou, diverse_candidates

MAX_COMPONENTS_PER_MASK = 3000
DEFAULT_MAX_PROPOSALS = 48
MIN_AREA_FRACTION = 0.0010
MAX_AREA_FRACTION = 0.55


def _clip_gray(im: Image.Image) -> np.ndarray:
    proxy = proxy_image(im, long_side=1100)
    return np.asarray(proxy.convert("L"), dtype=np.uint8)


def propose(im: Image.Image, *, max_proposals: int = DEFAULT_MAX_PROPOSALS) -> tuple[list[dict], dict]:
    if not 1 <= max_proposals <= 200:
        raise ValueError("geometry proposal budget must be 1..200")
    gray = _clip_gray(im)
    height,width=gray.shape
    area=width*height
    otsu, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Frozen illumination sweeps: a photo's global Otsu threshold alone fails
    # when a bright PS4 case or a dark vignette dominates the image.
    thresholds=sorted({int(max(90,min(245,x))) for x in
                       (otsu-20,otsu,otsu+20,155,185,215)})
    pool=[]
    count=0
    skipped_shapes=0
    skipped_component_caps=0
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    for threshold in thresholds:
        binary=(gray>=threshold).astype(np.uint8)*255
        binary=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,kernel,iterations=1)
        # External contours avoid mistaking the slash/serial *inside* a light
        # sticker as separate paper regions.
        contours,_=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        count+=len(contours)
        if len(contours)>MAX_COMPONENTS_PER_MASK:
            skipped_component_caps+=len(contours)-MAX_COMPONENTS_PER_MASK
            contours=sorted(contours,key=cv2.contourArea,reverse=True)[:MAX_COMPONENTS_PER_MASK]
        for contour in contours:
            x,y,w,h=cv2.boundingRect(contour)
            size=w*h
            frac=size/area
            if min(w,h)<20 or not MIN_AREA_FRACTION<=frac<=MAX_AREA_FRACTION:
                skipped_shapes+=1
                continue
            aspect=w/h
            if not 0.55<=aspect<=1.85:
                skipped_shapes+=1
                continue
            perimeter=cv2.arcLength(contour,True)
            if perimeter<=0:
                continue
            rectangularity=float(cv2.contourArea(contour))/size
            # Occluded, curled and angled paper can have irregular edges,
            # but too thin or sparse a contour is not a paper candidate.
            if rectangularity<0.60:
                skipped_shapes+=1
                continue
            patch=gray[y:y+h,x:x+w]
            inner=float(np.median(patch))
            # Detect local surround contrast without using test labels.
            pad=max(4,int(min(w,h)*.15))
            left=max(0,x-pad);right=min(width,x+w+pad)
            top=max(0,y-pad);bottom=min(height,y+h+pad)
            envelope=gray[top:bottom,left:right]
            # 5%-lowest surrounding pixels improve resilience to glare but
            # cannot establish that the object is printed sticker paper.
            surrounding=float(np.percentile(envelope,10))
            contrast=inner-surrounding
            if inner<112 or contrast<15:
                skipped_shapes+=1
                continue
            # Score is only for ordering *within* a review-only alternative.
            # Bounding boxes are not classifier outputs.
            quality=rectangularity*min(85,contrast)*(1-.2*abs(np.log(aspect)))
            pool.append((quality,threshold,(x,y,x+w,y+h),
                         rectangularity,contrast,inner))
    pool.sort(key=lambda x:(-x[0],-x[3],x[2],x[1]))
    selected=[]
    # EXIF transposition happens in proxy_image; these coordinates are in the
    # same oriented source space used by visual_region_probe.scan().
    from PIL import ImageOps
    oriented=ImageOps.exif_transpose(im)
    sx=oriented.width/width
    sy=oriented.height/height
    for quality,threshold,box,extent,contrast,inner in pool:
        mapped=[round(box[0]*sx),round(box[1]*sy),
                round(box[2]*sx),round(box[3]*sy)]
        if any(box_iou(mapped,p["bbox_xyxy_original_pixels"])>.65
               for p in selected):
            continue
        selected.append({
            "bbox_xyxy_original_pixels":mapped,
            "coordinate_system":"exif-oriented-source-image-pixels",
            "candidate_type":"bright-rectangle-unverified",
            "proposal_method":"multi-threshold-external-contours",
            "threshold_gray":threshold,
            "shape_extent":round(extent,4),
            "local_luminance_contrast":round(contrast,2),
            "heuristic_order_score":round(quality,3),
            "new_sticker_confirmed":False,
        })
        if len(selected)>=max_proposals:
            break
    return selected,{
        "method":"opencv-otsu-fixed-sweep-external-contours",
        "proxy_width":width,"proxy_height":height,
        "thresholds_attempted":thresholds,
        "all_contours_considered":count,
        "contours_censored_by_component_cap":skipped_component_caps,
        "rejected_by_size_shape_or_contrast":skipped_shapes,
        "valid_papers_before_dedup":len(pool),
        "retained_after_dedup_and_budget":len(selected),
        "max_proposals":max_proposals,
        "not_exhaustive_when_capped":len(pool)>max_proposals or skipped_component_caps>0,
        "negative_specificity_not_established":True,
    }


def scan_index(index: dict, root: Path, *, max_files: int=48, max_proposals: int=48) -> dict:
    selected=diverse_candidates(index.get("candidates",[]),max_files)
    out=[];errors=[]
    root=root.resolve()
    for item in selected:
        ident=item.get("id","")
        path=(root/str(item.get("path",""))).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append({"candidate_id":ident,"status":"source-unavailable-or-outside-root"})
            continue
        if sha256(path)!=item.get("sha256"):
            errors.append({"candidate_id":ident,"status":"source-sha256-mismatch"})
            continue
        try:
            with Image.open(path) as image:
                proposals,coverage=propose(image,max_proposals=max_proposals)
            out.append({"candidate_id":ident,"source_url":item.get("source_url",""),
                        "proposals":proposals,"coverage":coverage,
                        "new_sticker_confirmed":False})
        except (ValueError,OSError,Image.DecompressionBombError) as exc:
            errors.append({"candidate_id":ident,"status":"image-invalid",
                           "exception_class":type(exc).__name__})
    return {"schema_version":1,"source_images_available":len(index.get("candidates",[])),
            "source_images_selected":len(selected),
            "source_images_not_selected_by_budget":max(0,len(index.get("candidates",[]))-len(selected)),
            "source_images_examined":len(out),
            "source_images_failed":errors,"candidates":out,
            "claim_ceiling":"generic visually bright rectangles for human review, not sticker detection",
            "new_confirmed_stickers":0}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidate-index",type=Path,required=True)
    p.add_argument("--candidate-root",type=Path,required=True)
    p.add_argument("--output",type=Path,default=Path("visual-evidence-work/geometry-proposals.json"))
    p.add_argument("--max-files",type=int,default=48)
    p.add_argument("--max-proposals",type=int,default=48)
    args=p.parse_args()
    report=scan_index(json.loads(args.candidate_index.read_text(encoding="utf-8")),
                      args.candidate_root,max_files=args.max_files,max_proposals=args.max_proposals)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="candidates"},sort_keys=True))


if __name__=="__main__":
    main()

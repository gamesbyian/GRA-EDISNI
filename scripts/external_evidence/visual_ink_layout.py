#!/usr/bin/env python3
"""OCR-free, bounded visual ink-layout *description* for CE paper regions.

Measure evidence of separate center-mark and bottom-print zones without
reading any text or verifying that a generic rectangle is an INSIDE sticker.
Values are not probabilities, and a two-zone layout is NOT sufficient to
identify a physical sticker or owner: inventory tickets can mimic it.

Works on in-memory already-acquired, SHA-pinned source photo crops.
No network, OCR library, model weights, personal-account resolution or edits.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

if __package__:
    from .visual_region_probe import sha256
else:
    from visual_region_probe import sha256

NORMAL_SIZE = 192
MAX_IMAGE_PIXELS = 40_000_000


def ink_layout(crop: Image.Image) -> dict:
    """Describe orientation-sensitive printed ink, not inferred sticker class."""
    if min(crop.size) < 16 or crop.width*crop.height > MAX_IMAGE_PIXELS:
        raise ValueError("unsafe or undersized paper crop")
    im=ImageOps.exif_transpose(crop).convert("L")
    image=np.asarray(im.resize((NORMAL_SIZE,NORMAL_SIZE),Image.Resampling.LANCZOS),dtype=np.uint8)
    paper_median=float(np.median(image))
    # A deliberately fixed absolute offset from central paper luminance.
    # Otsu on mostly-blank textured paper often identifies wrinkles as ink.
    threshold=int(max(30,min(185,round(paper_median)-70)))
    black=(image<threshold).astype(np.uint8)
    zones={
        "top_margin":black[4:40,25:167],
        "center_mark":black[44:138,30:162],
        "bottom_print":black[145:187,35:157],
        "edge_band":np.concatenate((black[:20,:].ravel(),black[-20:,:].ravel(),
                                    black[:, :20].ravel(),black[:,-20:].ravel())),
    }
    proportions={name:round(float(np.mean(array)),6) for name,array in zones.items()}
    center=zones["center_mark"]
    bottom=zones["bottom_print"]
    def components(zone:np.ndarray)->dict:
        n,labels,stats,centers=cv2.connectedComponentsWithStats(zone.astype(np.uint8),connectivity=8)
        if n>2500:
            raise ValueError("too many foreground components")
        useful=[(int(s[4]),int(s[2]),int(s[3]))
                for s in stats[1:] if s[4]>=3]
        useful.sort(reverse=True)
        return {
            "components_area_at_least_3":len(useful),
            "largest_component_pixels":useful[0][0] if useful else 0,
            "top_three_component_areas":[row[0] for row in useful[:3]],
            "largest_component_box_size":[useful[0][1],useful[0][2]] if useful else [0,0],
        }
    mid=components(center)
    low=components(bottom)
    texture=float(cv2.Laplacian(image,cv2.CV_64F).var())
    return {
        "descriptor_version":1,
        "coordinate_system":"normalized orientation-preserving rectangular ROI",
        "normalized_size":[NORMAL_SIZE,NORMAL_SIZE],
        "paper_median_luminance":round(paper_median,3),
        "fixed_ink_threshold":threshold,
        "dark_pixel_fractions_by_zone":proportions,
        "center_component_stats":mid,
        "bottom_component_stats":low,
        "laplacian_variance_blur_proxy":round(texture,3),
        "layout_interpretation":"uncalibrated regional ink geometry; no digit, symbol, CE or sticker recognition",
        "serial_read":None,
        "new_sticker_confirmed":False,
    }


def validate_geometry(row:dict,width:int,height:int)->tuple[int,int,int,int]:
    coords=row.get("bbox_xyxy_original_pixels")
    if not isinstance(coords,list) or len(coords)!=4 or any(type(x)!=int for x in coords):
        raise ValueError("invalid integer-only source-region coordinates")
    l,t,r,b=coords
    if not 0<=l<r<=width or not 0<=t<b<=height or min(r-l,b-t)<16:
        raise ValueError("unsafe source crop bounds")
    if row.get("new_sticker_confirmed") is not False:
        raise ValueError("visual proposal must remain unverified")
    return l,t,r,b


def annotate(index:dict, proposed:dict, root:Path, *, max_files:int=48,
             max_regions_per_file:int=8)->dict:
    if not 1<=max_files<=48 or not 1<=max_regions_per_file<=8:
        raise ValueError("source review budgets are 1..48 photos and 1..8 regions")
    if proposed.get("new_confirmed_stickers",0)!=0:
        raise ValueError("source region report may not declare a verified sticker")
    lookup={}
    for item in index.get("candidates",[]):
        ident=item.get("id")
        if not isinstance(ident,str) or not ident or ident in lookup:
            raise ValueError("duplicate or invalid candidate ID")
        lookup[ident]=item
    results=[];errors=[]
    root=root.resolve()
    for source in proposed.get("candidates",[])[:max_files]:
        if source.get("new_sticker_confirmed") is not False:
            raise ValueError("source row incorrectly declares a verified sticker")
        ident=source.get("candidate_id")
        if ident not in lookup:
            errors.append({"candidate_id":ident,"reason":"missing-pinned-source-reference"})
            continue
        item=lookup[ident]
        file=(root/str(item.get("path",""))).resolve()
        if not file.is_relative_to(root) or not file.is_file():
            errors.append({"candidate_id":ident,"reason":"unsafe-or-unavailable-source"})
            continue
        if sha256(file)!=item.get("sha256"):
            errors.append({"candidate_id":ident,"reason":"source-sha256-mismatch"})
            continue
        try:
            with Image.open(file) as raw:
                im=ImageOps.exif_transpose(raw).convert("RGB")
                proposals=[]
                for region in source.get("proposals",[])[:max_regions_per_file]:
                    bounds=validate_geometry(region,im.width,im.height)
                    descriptor=ink_layout(im.crop(bounds))
                    proposals.append({**region,"ink_layout":descriptor,
                                      "new_sticker_confirmed":False})
                results.append({"candidate_id":ident,"source_url":item.get("source_url",""),
                                "proposals":proposals,
                                "source_sha256":item["sha256"],
                                "new_sticker_confirmed":False})
        except (ValueError,OSError,UnidentifiedImageError,Image.DecompressionBombError) as exc:
            errors.append({"candidate_id":ident,"reason":type(exc).__name__,
                           "description":str(exc)[:140]})
    return {
        "schema_version":1,
        "mode":"unverified-ink-layout-annotation-only",
        "source_candidates_total":len(index.get("candidates",[])),
        "proposal_sources_total":len(proposed.get("candidates",[])),
        "source_files_scanned":len(results),
        "source_files_censored_by_cap":max(0,len(proposed.get("candidates",[]))-max_files),
        "source_errors":errors,
        "candidates":results,
        "auto_sticker_detector_validated":False,
        "new_confirmed_stickers":0,
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidate-index",type=Path,required=True)
    p.add_argument("--candidate-root",type=Path,required=True)
    p.add_argument("--proposals",type=Path,required=True)
    p.add_argument("--out",type=Path,default=Path("visual-evidence-work/sliced-ink-layout-proposals.json"))
    args=p.parse_args()
    index=json.loads(args.candidate_index.read_text(encoding="utf-8"))
    proposed=json.loads(args.proposals.read_text(encoding="utf-8"))
    report=annotate(index,proposed,args.candidate_root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="candidates"},sort_keys=True))


if __name__=="__main__":
    main()

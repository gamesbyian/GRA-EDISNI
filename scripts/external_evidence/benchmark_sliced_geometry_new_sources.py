#!/usr/bin/env python3
"""FROZEN synthetic tiny-object challenge from new original source-photo crops.

Compares whole-frame OpenCV paper proposals vs overlapping local tiles at a
fixed eight-region review budget. Novel *source photograph* IDs 021 and 171
were not in development templates or previously measured 039/047/063/118.
Pasting them into generated scenes still means this is NOT native real-camera
tiny-sticker validation. Report misses and false prompts without retuning.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps

if __package__:
    from .visual_region_probe import sha256,box_iou
    from .visual_geometry_proposals import propose
    from .visual_sliced_geometry import suggest, tile_plan
else:
    from visual_region_probe import sha256,box_iou
    from visual_geometry_proposals import propose
    from visual_sliced_geometry import suggest,tile_plan

SIZE=(1440,1080)
FRACTIONS=(0.001,0.003,0.01)
NEGATIVES=("plain-dark","game-case","shipping-ticket","bright-collector-art")
IOU=.40
TOP_K=8


def load_novel(path:Path,root:Path)->list[dict]:
    with path.open(encoding="utf-8",newline="") as f:
        records=list(csv.DictReader(f))
    if {r["serial"] for r in records}!={"021","171"}:
        raise ValueError("holdout source identities must remain fixed")
    for row in records:
        if row["serial"] in {"003","037","038","065","125","039","047","063","118"}:
            raise ValueError("leaked previously-used development physical source")
        if row["annotation_grade"]!="visually-inspected-2026-10-16":
            raise ValueError("no source paper-boundary annotation")
        loc=(root/row["source_path"]).resolve()
        if not loc.is_relative_to(root.resolve()) or not loc.is_file():
            raise ValueError("unsafe or missing original source photograph")
        if not loc.relative_to(root.resolve()).as_posix().startswith("archive/stickers/originals/"):
            raise ValueError("candidate source is not a physical original")
        if sha256(loc)!=row["source_sha256"]:
            raise ValueError("source image digest mismatch")
        box=tuple(float(row[k]) for k in ("left","top","right","bottom"))
        if not (0<=box[0]<box[2]<=1 and 0<=box[1]<box[3]<=1):
            raise ValueError("bad paper boundary fractions")
    return records


def background(kind:str)->Image.Image:
    if kind not in NEGATIVES:
        raise ValueError("unknown negative variant")
    im=Image.new("RGB",SIZE,(38,43,50))
    d=ImageDraw.Draw(im)
    for i in range(18):
        x=(59+i*201)%SIZE[0]; y=(37+i*147)%SIZE[1]
        d.line([x,y,min(SIZE[0]-1,x+123),min(SIZE[1]-1,y+42)],
               fill=(60+i%5*5,66+i%7*3,68),width=5)
    d.rectangle([20,90,340,293],fill=(103,88,77))
    d.ellipse([610,85,828,300],fill=(132,55,59))
    d.polygon([(1099,65),(1372,158),(1328,434),(1040,370)],fill=(52,64,86))
    if kind=="game-case":
        d.rounded_rectangle([870,430,1220,876],radius=14,fill=(234,231,223))
        d.text((945,680),"PS4 GAME 001",fill=(45,45,45))
    elif kind=="shipping-ticket":
        d.rectangle([793,470,1167,830],fill=(229,231,222))
        d.polygon([(950,710),(973,710),(1050,590),(1030,590)],fill=(37,39,42))
        d.text((855,780),"INVENTORY 2026",fill=(29,29,29))
    elif kind=="bright-collector-art":
        d.rectangle([752,428,1120,778],fill=(235,237,229))
        d.rectangle([790,528,1060,573],fill=(34,36,39))
        d.rectangle([880,693,990,709],fill=(46,48,50))
    return im


def paper_patch(case:dict,root:Path)->Image.Image:
    with Image.open(root/case["source_path"]) as raw:
        photo=ImageOps.exif_transpose(raw).convert("RGB")
        l,t,r,b=[float(case[k]) for k in ("left","top","right","bottom")]
        box=[round(l*photo.width),round(t*photo.height),
             round(r*photo.width),round(b*photo.height)]
        if min(box[2]-box[0],box[3]-box[1])<30:
            raise ValueError("paper patch too small")
        return photo.crop(box)


def positive(case:dict,root:Path,fraction:float,order:int)->tuple[Image.Image,list[int]]:
    if fraction not in FRACTIONS:
        raise ValueError("unfrozen paper area fraction")
    scene=background(NEGATIVES[order%len(NEGATIVES)])
    sticker=paper_patch(case,root)
    if order%2:
        sticker=sticker.transpose(Image.Transpose.ROTATE_90)
    area=SIZE[0]*SIZE[1]*fraction
    ratio=sticker.width/sticker.height
    width=round(math.sqrt(area*ratio))
    height=round(math.sqrt(area/ratio))
    sticker=sticker.resize((width,height),Image.Resampling.LANCZOS)
    positions=((.07,.75),(.56,.10),(.84,.65),(.34,.38),(.62,.74),(.10,.48))
    fx,fy=positions[order%len(positions)]
    x=min(round(fx*SIZE[0]),SIZE[0]-width)
    y=min(round(fy*SIZE[1]),SIZE[1]-height)
    scene.paste(sticker,(x,y))
    return scene,[x,y,x+width,y+height]


def run(root:Path, *, max_tiles:int=24, top_k:int=TOP_K)->dict:
    if top_k!=TOP_K or max_tiles!=24:
        raise ValueError("frozen review and tile budgets require new challenge version")
    records=load_novel(root/"data/reference/inside-ce-novel-tiny-paper-crop-holdouts-20261016.csv",root)
    data=[];negatives=[]
    def compare(im:Image.Image,truth:list[int]|None)->dict:
        baseline,b_stats=propose(im,max_proposals=top_k)
        tiled,t_stats=suggest(im,max_tiles=max_tiles,top_k=top_k)
        original_ious=[box_iou(truth,p["bbox_xyxy_original_pixels"]) for p in baseline] if truth else []
        tiled_ious=[box_iou(truth,p["bbox_xyxy_original_pixels"]) for p in tiled] if truth else []
        return {
            "global_best_iou":round(max(original_ious,default=0.),5) if truth else None,
            "sliced_best_iou":round(max(tiled_ious,default=0.),5) if truth else None,
            "global_top8_papers":len(baseline),
            "sliced_top8_papers":len(tiled),
            "global_localized_iou_040":any(x>=IOU for x in original_ious) if truth else None,
            "sliced_localized_iou_040":any(x>=IOU for x in tiled_ious) if truth else None,
            "global_boxes":[p["bbox_xyxy_original_pixels"] for p in baseline],
            "sliced_boxes":[p["bbox_xyxy_original_pixels"] for p in tiled],
            "global_accounting":b_stats,"sliced_accounting":t_stats,
            "serial_read":None,"new_sticker_confirmed":False}
    for i,row in enumerate(sorted(records,key=lambda d:d["serial"])):
        for j,fraction in enumerate(FRACTIONS):
            im,ground=positive(row,root,fraction,3*i+j)
            data.append({
                "source_serial_ground_truth_only":row["serial"],
                "source_sha256":row["source_sha256"],
                "area_fraction":fraction,"target_box":ground,
                **compare(im,ground)})
    for kind in NEGATIVES:
        im=background(kind)
        negatives.append({"negative_case":kind,"sticker_present":False,**compare(im,None)})
    grouped=[]
    for frac in FRACTIONS:
        subs=[r for r in data if r["area_fraction"]==frac]
        grouped.append({
            "fraction":frac,"cases":len(subs),
            "global_localized":sum(x["global_localized_iou_040"] for x in subs),
            "sliced_localized":sum(x["sliced_localized_iou_040"] for x in subs)})
    return {
        "schema_version":1,"method":"frozen-original-021-171-paper-in-generated-wide-scenes",
        "novel_original_photo_sources":2,
        "synthetic_composites":len(data),
        "synthetic_negative_images":len(negatives),
        "global_hits_at_iou_040":sum(x["global_localized_iou_040"] for x in data),
        "sliced_hits_at_iou_040":sum(x["sliced_localized_iou_040"] for x in data),
        "global_negative_images_prompted":sum(x["global_top8_papers"]>0 for x in negatives),
        "sliced_negative_images_prompted":sum(x["sliced_top8_papers"]>0 for x in negatives),
        "per_size":grouped,"cases":data,"negatives":negatives,
        "new_confirmed_stickers":0,
        "validated_real_photo_tiny_sticker_detector":False,
        "source_scope":"new source-photo IDs but generated composites, no external real-camera specificity",
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--out",type=Path,default=Path("visual-evidence-work/sliced-novel-small-paper-challenge.json"))
    args=p.parse_args()
    root=args.repo_root.resolve()
    out=run(root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k not in ("cases","negatives")},sort_keys=True))


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Auditable *source-provenance* control for three historical cover crops.

The native cover and historic monitor crops are pinned by original Git
blob SHA in probe_original_cover_a1.py. Locations in 50%-size interior
image were found retrospectively by source-to-source template matching
and FROZEN; check only those original coordinates and same coordinates
on exterior cover as a negative control. No sticker glyph, original
running-man cipher image or creative transform is an input.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image

SOURCES={
    "INSIDE_A-5d197786f158c567.JPG":"875403acac93d83a8acae97e14240c35b88d33ab",
    "INSIDE_B-80fbff1237c37913.JPG":"d533d4161f0572b65d134d54f4fa6477029f2d64",
    "image-7be117e2c68d1b1e.png":"40039a204800383f69c1b0e4475edcc0989944ef",
    "image-21b86ef8e34e269b.png":"c07e87d72a92d4181b1014f3a8269e086a4ef471",
    "image-d6d0d0f76ab751ca.png":"b6216e584a62e44ae0594cb881c9ad27ef5266fe",
}
# Frozen 1-based? No: pixel origin zero-based in a 3276x2520 image.
# x0,y0 found using template comparison; (w,h) equals native PNG size.
MATCHES={
    "acorn_family_monitor":("image-7be117e2c68d1b1e.png",1890,1647),
    "planet_family_monitor":("image-21b86ef8e34e269b.png",563,1469),
    "graph_family_monitor":("image-d6d0d0f76ab751ca.png",1116,1441),
}
NATIVE_ROI={
    "acorn_monitor_context":[3630,3180,4090,3520],
    "running_figure_context":[5550,2850,6500,3600],
    "monitors_environment":[700,2770,4070,3500],
}
def sha_git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()

def read_verified(folder,name):
    data=(folder/name).read_bytes()
    assert sha_git_blob(data)==SOURCES[name],name+" authentic SHA mismatch"
    return Image.open(folder/name).convert("L")

def pearson(a,b):
    aa=list(a.getdata());bb=list(b.getdata())
    assert len(aa)==len(bb) and len(aa)>1
    n=len(aa);mu=sum(aa)/n;mv=sum(bb)/n
    xy=sum((x-mu)*(y-mv) for x,y in zip(aa,bb))
    xx=sum((x-mu)**2 for x in aa);yy=sum((y-mv)**2 for y in bb)
    return xy/math.sqrt(xx*yy) if xx and yy else 0

def run(root):
    a=read_verified(root,"INSIDE_A-5d197786f158c567.JPG")
    b=read_verified(root,"INSIDE_B-80fbff1237c37913.JPG")
    assert a.size==b.size==(6552,5040)
    halves=[im.resize((3276,2520),resample=Image.Resampling.LANCZOS)
            for im in (a,b)]
    rows=[]
    for role,(file,x,y) in MATCHES.items():
        ref=read_verified(root,file)
        w,h=ref.size
        xy=(x,y,x+w,y+h)
        ra=pearson(halves[0].crop(xy),ref)
        rb=pearson(halves[1].crop(xy),ref)
        # This is provenance of screenshot/crop, *not* the code itself.
        assert ra>0.84, f"{role}: source crop no longer registers"
        assert abs(rb)<0.25, f"{role}: exterior negative unexpectedly similar"
        rows.append({
            "role":role,"file":file,
            "fixed_match_50_percent_image":[x,y,w,h],
            "corresponding_original_A_native_bbox":[2*x,2*y,2*(x+w),2*(y+h)],
            "pearson_interior":round(ra,6),
            "pearson_exterior_negative":round(rb,6),
            "interpretation":"historical crop originates in this scanned interior artwork; NOT a decoded cover transformation"
        })
    return {
        "status":"authenticated and confirmed provenance for three historical monitor crops",
        "source":"gamesbyian/playdead-unofficial-exports pinned original binary Git objects",
        "coordinate_selection":"retrospective native crop-to-cover localization, not prospectively predicted",
        "cover_A_dimensions":[6552,5040],
        "matches":rows,
        "semantic_observations":{
            "acorn_screen":"genuinely an illuminated foreground monitor, physical geometry as frozen above",
            "running_figure":"a small running figure on a separate illuminated platform is visible in the right-hand window; its exact cipher identity remains UNVERIFIED",
            "running_figure_native_context_roi":NATIVE_ROI["running_figure_context"],
            "no_2021_running_man_overlay_source_verified":True
        },
        "scope":"physical scan/crop source identity ONLY. No sticker symbol or author's intended interpretation validated."
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,
                   default=Path("cover_source_artifacts/verified_source"))
    p.add_argument("--report",type=Path)
    args=p.parse_args()
    result=run(args.source_dir)
    serialized=json.dumps(result,indent=2)+"\n"
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(serialized,encoding="utf8")
    print(serialized)

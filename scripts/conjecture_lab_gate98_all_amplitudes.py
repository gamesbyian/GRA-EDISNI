#!/usr/bin/env python3
"""CL05b: source-only exact RGB palette search for 16x16-lattice markers.

Search ALL 255 possible common channel amplitudes k in the nonblack 3-bit
cube RGB in {0,k}^3. No sticker data and no expected plaintext scored.
The physically published method isolated specific RGB values and found
some exactly 16 pixels apart in the original image.

A high pixel frequency alone is NOT an identifying mark. Compute frequency
enrichment on EXACT sampling coordinates against all unsampled
coordinates in the SAME upper 1024-pixel source region.
"""
import argparse
from collections import Counter
from io import BytesIO
import json
from pathlib import Path

from PIL import Image
from conjecture_lab_gate98_real_pixels import load_bytes, EXPECTED_DIMENSIONS

W,H=EXPECTED_DIMENSIONS
STRIDE=16
REGION_H=1024
GRID_TOTAL=(W//STRIDE)*(REGION_H//STRIDE)
OFF_GRID_TOTAL=W*REGION_H-GRID_TOTAL


def amplitude(rgb):
    nz={v for v in rgb if v}
    if len(nz)!=1:return 0
    return next(iter(nz))


def run(path):
    original,h=load_bytes(path)
    with Image.open(BytesIO(original)) as src:
        assert src.size==(W,H)
        im=src.convert("RGB")
    # Count ALL 3-bit nonzero cube colors of EVERY amplitude,
    # separately on and off the historical 16px grid.
    top_on=Counter()
    top_off=Counter()
    bottom_on=Counter()
    color_on=Counter()
    color_off=Counter()
    for y in range(H):
        row=[im.getpixel((x,y)) for x in range(W)]
        if y<REGION_H:
            for x,rgb in enumerate(row):
                a=amplitude(rgb)
                if not a:continue
                if y%STRIDE==0 and x%STRIDE==0:
                    top_on[a]+=1
                    color_on[(a,rgb)]+=1
                else:
                    top_off[a]+=1
                    color_off[(a,rgb)]+=1
        elif y%STRIDE==0:
            for x in range(0,W,STRIDE):
                a=amplitude(row[x])
                if a:bottom_on[a]+=1
    out=[]
    for a in range(1,256):
        on=top_on[a];off=top_off[a]
        ratio=(on/GRID_TOTAL)/(off/OFF_GRID_TOTAL) if off else None
        out.append({
            "level":a,"top_grid":on,"top_off_grid":off,
            "other_grid":bottom_on[a],
            "top_grid_enrichment":round(ratio,6) if ratio is not None else None,
            "per_nonblack_rgb":[
                {"rgb":"#"+bytes(rgb).hex().upper(),
                 "top_grid":color_on[(a,rgb)],
                 "top_off_grid":color_off[(a,rgb)]}
                for rgb in [
                    (a,0,0),(0,a,0),(0,0,a),
                    (a,a,0),(a,0,a),(0,a,a),(a,a,a)
                ]
            ]
        })
    order_by_on=sorted(out,key=lambda q:(-q["top_grid"],q["level"]))
    order_by_ratio=sorted([q for q in out if q["top_grid"]>=15 and q["top_off_grid"]>=25],
                          key=lambda q:(-q["top_grid_enrichment"],-q["top_grid"]))
    return {
        "status":"source-only exhaustive 255-amplitude exact 3-bit palette scan; no sticker values used",
        "source_git_sha1":h,
        "sample_grid":"top 1024 pixels of original, sampled at (x mod 16, y mod 16)=(0,0)",
        "reference_region":"all other pixels within exactly same first 1024 rows",
        "first_region_total_grid":GRID_TOTAL,
        "first_region_off_grid":OFF_GRID_TOTAL,
        "levels_scanned":255,
        "all_amplitudes":out,
        "top_20_by_grid_hits":order_by_on[:20],
        "top_30_by_relative_enrichment":order_by_ratio[:30],
        "important_levels":[q for q in out if q["level"] in (1,64,128,207,254,255)],
        "caveat":"The amplitude family is source-archeology search; any ranked choice is post-selected and requires a separate historical route reconstruction.",
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source")
    p.add_argument("--output")
    a=p.parse_args()
    z=run(a.source)
    if a.output: Path(a.output).write_text(json.dumps(z,indent=2)+"\n",encoding="utf8")
    print(json.dumps({
        "source":z["source_git_sha1"],
        "top20_by_hits":[
            {"a":x["level"],"on":x["top_grid"],"off":x["top_off_grid"],
             "relative":x["top_grid_enrichment"],"below":x["other_grid"]}
            for x in z["top_20_by_grid_hits"]
        ],
        "top20_by_enrichment":[
            {"a":x["level"],"on":x["top_grid"],"off":x["top_off_grid"],
             "relative":x["top_grid_enrichment"],"below":x["other_grid"]}
            for x in z["top_30_by_relative_enrichment"][:20]
        ],
        "important_levels":[
            {"a":x["level"],"on":x["top_grid"],"off":x["top_off_grid"],
             "relative":x["top_grid_enrichment"],"below":x["other_grid"]}
            for x in z["important_levels"]
        ]
    },indent=2))

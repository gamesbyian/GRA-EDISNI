#!/usr/bin/env python3
"""Reproduce 2021 acorn->LIFE DETECTED operation from original 2018 printer rows.

Inputs, independently archived:
* ORIGINAL 32 x 32 PC/PS4 acorn printer solved row order in this repo;
* Standard Conway Acorn seed B3/S23, exact generation 41;
* Fixed offset (1,16) observed in byte-authenticated archived 2021 video;
* Source colour classes: slash=red; dash=blue; dot=orange.

Operation: orange survives *outside* the mask, blue/dash pixels flip to
orange *inside* the mask. Red is never promoted to orange.
Expected final orange 32x32 bitmap SHA256 derives from the final frame
of the original archived 2021 visual demonstration, not from an
English-text fitter. The code neither guesses nor touches stickers.

This is a replay with historical registration known from the video,
NOT a blind discovery of the original acorn offset.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROWS=ROOT/"data/printer-reference/pc-ps4-acorn-order.txt"
FINAL_SHA256="38ea14a45bffbd735cec104cad5ba0499bbb36163bc3c2bf0b9cf250b773bd6d"
ACORN={(1,0),(3,1),(0,2),(1,2),(4,2),(5,2),(6,2)}


def load_rows(path):
    rows=[s.strip() for s in Path(path).read_text(encoding="utf8").splitlines()
          if re.fullmatch(r"[.\-/]{32}",s.strip())]
    assert len(rows)==32 and all(len(r)==32 for r in rows)
    return rows


def evolve(live):
    neighbours=Counter((x+dx,y+dy)
                        for x,y in live
                        for dx in (-1,0,1) for dy in (-1,0,1)
                        if dx or dy)
    return {point for point,k in neighbours.items()
            if k==3 or (k==2 and point in live)}


def acorn_mask():
    cells=set(ACORN)
    assert len(cells)==7
    for generation in range(41):
        cells=evolve(cells)
    assert len(cells)==102
    left=min(x for x,y in cells)
    top=min(y for x,y in cells)
    assert max(x for x,y in cells)-left+1==30
    assert max(y for x,y in cells)-top+1==15
    # Video's historically documented registration, not fit to phrase:
    normalized={(x-left+1,y-top+16) for x,y in cells}
    assert min(x for x,y in normalized)==1
    assert max(x for x,y in normalized)==30
    assert min(y for x,y in normalized)==16
    assert max(y for x,y in normalized)==30
    return normalized


def decode(rows):
    mask=acorn_mask()
    census=Counter("".join(rows))
    assert census==Counter({"-":613,"/":308,".":103}),census
    orange=set()
    diagnostics=Counter()
    for y,line in enumerate(rows):
        for x,mark in enumerate(line):
            active=(x,y) in mask
            diagnostics[("masked" if active else "unmasked",mark)]+=1
            # Orange is the output channel. The black overlay removes
            # original orange where it covers it; masked original blue
            # is recolored orange. Red is never selected.
            if (mark=="." and not active) or (mark=="-" and active):
                orange.add((x,y))
    assert diagnostics["masked","-"]==39
    assert diagnostics["masked","."]==52
    assert diagnostics["masked","/"]==11
    assert len(orange)==90
    bitmap=["".join("#" if (x,y) in orange else "." for x in range(32))
            for y in range(32)]
    s="\n".join(bitmap)+"\n"
    digest=hashlib.sha256(s.encode("ascii")).hexdigest()
    assert digest==FINAL_SHA256, (digest,FINAL_SHA256)
    return {
        "source_size":[32,32],
        "source_symbol_census":dict(census),
        "generation":41,
        "game_of_life":"B3/S23",
        "acorn_live_cells":len(mask),
        "registered_offset_x_y_0_based":[1,16],
        "registered_bbox_x0_y0_x1_y1":[1,16,31,31],
        "masked_source_counts":{k[1]:v for k,v in diagnostics.items() if k[0]=="masked"},
        "output_orange_cells":len(orange),
        "output_bitmap_sha256":digest,
        "bitmap":bitmap,
        "source_precedence":"canonical 2018 row order plus recovered archived 2021 visual registration",
        "scope":"historical PC/PS4 acorn LIFE DETECTED ONLY; not the CE sticker foreground"
    }


def compare_video_still(bitmap,video_still):
    """Optional file is a 512x512 screenshot from video >=frame 565.

    Pixels are sampled at 16px-cell centers to avoid animation labels.
    Colour class threshold is fixed from the source RGB orange palette.
    """
    from PIL import Image
    im=Image.open(video_still).convert("RGB")
    assert im.size==(512,512),im.size
    bright=set()
    for y in range(32):
        for x in range(32):
            red,green,blue=im.getpixel((16*x+8,16*y+8))
            if red>180 and 45<green<180 and blue<70:
                bright.add((x,y))
    decoded={(x,y) for y,row in enumerate(bitmap)
             for x,v in enumerate(row) if v=="#"}
    return {"video_orange_cells":len(bright),
            "independent_raster_intersection":len(bright&decoded),
            "xor_disagreements":len(bright^decoded),
            "exact_equivalence":bright==decoded}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=ROWS)
    p.add_argument("--video-final-frame",type=Path,
                   help="optional genuine MP4 final frame >=565, 512x512 PNG")
    p.add_argument("--save-bitmap",type=Path)
    args=p.parse_args()
    obj=decode(load_rows(args.source))
    if args.video_final_frame:
        obj["independent_video_comparison"]=compare_video_still(
            obj["bitmap"],args.video_final_frame)
        assert obj["independent_video_comparison"]["exact_equivalence"]
    if args.save_bitmap:
        args.save_bitmap.parent.mkdir(parents=True,exist_ok=True)
        args.save_bitmap.write_text("\n".join(obj["bitmap"])+"\n",encoding="ascii")
    print(json.dumps(obj,indent=2))

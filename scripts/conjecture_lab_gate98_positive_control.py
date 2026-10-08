#!/usr/bin/env python3
"""CL05: reproduce the original gate-98 16px-grid RGB overlay as a positive control.

Only the HISTORICALLY REPORTED algorithm (isolate exact RGB values, overlay
visible layers, observe message/planet) may be confirmed. The 0xCF colour
family, seven choose six colours, orientation and display parameters are
EXPLORATORY, discovered after looking at the image and not a confirmed
2018 palette legend.

No CE sticker values are imported into this probe.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from io import BytesIO
from itertools import combinations
import json
from pathlib import Path

from PIL import Image
from conjecture_lab_gate98_real_pixels import (
    EXPECTED_DIMENSIONS, PIXELS_PER_ROW, PIXELS_PER_COL, load_bytes,
)

LEVEL = 207
MARKER_COLORS = tuple(tuple(LEVEL if (v >> i) & 1 else 0 for i in (2,1,0))
                      for v in range(1,8))
GRID_W, GRID_H = 128, 64
KNOWN_ROUTE = "REPO/SYS/ACTIVATE_SHUTDOWN_PROTOCOL/PROT6y723g90ty9r80234"

def bounds(indices):
    if not indices:
        return None
    xs=[i%GRID_W for i in indices]
    ys=[i//GRID_W for i in indices]
    return [min(xs),min(ys),max(xs),max(ys)]

def make_result(original):
    pix = original.convert("RGB")
    samples = [tuple(pix.getpixel((16*x, 16*y)))
               for y in range(GRID_H) for x in range(GRID_W)]
    assert len(samples) == GRID_H*GRID_W
    assert len(set(MARKER_COLORS))==7

    individual={}
    bits_by_color={}
    for c in MARKER_COLORS:
        indices=[i for i,v in enumerate(samples) if v==c]
        mask=bytearray((GRID_H*GRID_W+7)//8)
        for i in indices:
            mask[i//8] |= 128 >> (i%8)
        k="#"+bytes(c).hex().upper()
        individual[k]={"n":len(indices),"bounds":bounds(indices),
                       "rows_touched":len(set(i//GRID_W for i in indices)),
                       "mask_base64":base64.b64encode(mask).decode()}
        bits_by_color[k]=set(indices)

    colors=list(individual)
    def rendering(keys, char_on="X"):
        merged=set().union(*(bits_by_color[k] for k in keys))
        rows=["".join(char_on if y*GRID_W+x in merged else " "
                      for x in range(GRID_W)).rstrip()
              for y in range(GRID_H)]
        # Save all rows, including leading blanks, to preserve registration
        return {
            "colors":keys,"n":len(merged),
            "bounds":bounds(sorted(merged)),
            "rows":rows,
            "row_counts":[sum(i//GRID_W == y for i in merged)
                          for y in range(GRID_H)],
        }

    variants={"all_nonblack_seven":rendering(colors)}
    for excluded in colors:
        variants["six_minus_"+excluded]=rendering([k for k in colors
                                                  if k!=excluded])
    # Contemporaneous description says exactly black plus SIX other colours;
    # seven non-black colour choices are not independently attested.
    return {
        "source_git_sha1":None,
        "positive_control_target_historical_not_fitted":KNOWN_ROUTE,
        "lattice":"top-left source pixels, 16px stride, 128x64 first quarter",
        "historical_documented_color_count":"black plus six additional exact RGB values",
        "candidate_palette":"seven RGB combinations with components 0 or 207",
        "palette_selected_after_inspection":True,
        "source_qualified_as_HISTORICAL_PALETTE":False,
        "single_color_masks":individual,
        "multi_color_six_of_seven_and_all":variants,
        "candidate_total":len(colors),
        "no_CE_data_used":True,
        "legend_status":"NOT recovered: needs six source-authenticated RGB values and crop",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source")
    ap.add_argument("--output")
    ap.add_argument("--preserve-source", help="Local original-byte output for one-off forensic use")
    args=ap.parse_args()
    raw,h=load_bytes(args.source)
    if args.preserve_source:
        Path(args.preserve_source).write_bytes(raw)
    with Image.open(BytesIO(raw)) as im:
        assert im.size==EXPECTED_DIMENSIONS
        result=make_result(im)
    result["source_git_sha1"]=h
    if args.output:
        Path(args.output).write_text(json.dumps(result,indent=2)+"\n",
                                     encoding="utf8")
    summary={
        "source_git_sha1":h,
        "selected_counts":{k:v["n"] for k,v in
                           result["single_color_masks"].items()},
        "all_nonblack":result["multi_color_six_of_seven_and_all"]
                             ["all_nonblack_seven"]["n"],
        "all_nonblack_grid_preview_lines":[
            "%02d |%s" %(i,line)
            for i,line in enumerate(
                result["multi_color_six_of_seven_and_all"]
                      ["all_nonblack_seven"]["rows"]
            )
        ],
    }
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()

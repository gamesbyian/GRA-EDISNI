#!/usr/bin/env python3
"""A source-native Conway acorn positive control, not a sticker decoder.

2021 Playdead ARG community account describes taking standard Game of
Life acorn (B3/S23), advancing it to generation 41, and registering the
result against a separate 'running man' image to recover LIFE DETECTED.

This module verifies the mathematically specified acorn generation(s).
Original 'running man' pixel/registration bytes and the 2021 video are
not part of this source-only positive control, so it DOES NOT attempt
to derive LIFEDETECTED from invented overlays.
"""
import argparse
import json
from collections import Counter

# Acorn RLE: x=7,y=3, B3/S23, bo$3bo$2o2b3o!
# https://conwaylife.com/wiki/Acorn
SEED={(1,0),(3,1),(0,2),(1,2),(4,2),(5,2),(6,2)}


def evolve(live):
    counts=Counter((x+dx,y+dy) for x,y in live
                   for dx in (-1,0,1) for dy in (-1,0,1)
                   if dx or dy)
    return {pos for pos,n in counts.items()
            if n==3 or (n==2 and pos in live)}


def bounds(live):
    xs=[p[0] for p in live]
    ys=[p[1] for p in live]
    return {"min_x":min(xs),"max_x":max(xs),
            "min_y":min(ys),"max_y":max(ys),
            "width":max(xs)-min(xs)+1,
            "height":max(ys)-min(ys)+1}


def run(generations=(0,41,42), render=False):
    assert len(SEED)==7
    assert bounds(SEED)["width"]==7 and bounds(SEED)["height"]==3
    wanted=set(generations)
    assert all(isinstance(i,int) and i>=0 for i in wanted)
    state=SEED.copy()
    out=[]
    for t in range(max(wanted)+1):
        if t in wanted:
            entry={"generation":t,"live_cells":len(state),**bounds(state)}
            if render:
                b=bounds(state)
                entry["rows"]=[
                    "".join("#" if (x,y) in state else "."
                            for x in range(b["min_x"],b["max_x"]+1))
                    for y in range(b["min_y"],b["max_y"]+1)]
            out.append(entry)
        if t<max(wanted):
            state=evolve(state)
    records={r["generation"]:r for r in out}
    if 41 in records:
        r=records[41]
        assert (r["live_cells"],r["width"],r["height"])==(102,30,15)
    if 42 in records:
        r=records[42]
        assert (r["live_cells"],r["width"],r["height"])==(92,30,15)
    return {
        "status":"2021 operation component independently replayed; historic overlay NOT reproduced",
        "source_seed":"standard Game of Life Acorn: bo$3bo$2o2b3o!",
        "rule":"B3/S23", "snapshots":out,
        "overlay_status":"unverified: needs original running-man pixels and authorially justified registration",
        "warning":"The known LIFEDETECTED answer was used only as provenance, not fitted to these coordinates."
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--render",action="store_true")
    args=parser.parse_args()
    print(json.dumps(run(render=args.render),indent=2))

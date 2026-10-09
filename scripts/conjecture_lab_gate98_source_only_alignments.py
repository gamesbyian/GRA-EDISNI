#!/usr/bin/env python3
"""CL-08: Does the original gate-98 source alone register its colour panels?

No 2019 reference pixels participate in scoring. We first find exact source
RGB dots of each hypothesized historic panel, filter each to its strongest
16px-phase (original source coordinates), then count *every* pairwise source
pixel displacement inside a coarse and deliberately generous source-layout
search rectangle.

Only AFTER ranking displacements do we compare to the known historic
reference-assisted offsets. If that offset is not the best-scoring shift,
the proposed 'blind registration by phase-dot overlap' does NOT work.

Colours themselves were learned through comparison to the known 2019 image,
so this is only a conditional source-only ALIGNMENT test, not discovery of
the full decoder or evidence that stickers encode these colours.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"data"/"conjecture-lab-gate98-source-only-registration-control-2026-10-08.json"
SOURCE_SHA256="db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded"

def freeze():
    d=json.loads(FIXTURE.read_text(encoding="utf8"))
    assert d["original_gate98_source_sha256"]==SOURCE_SHA256
    assert d["source_only_scoring"] is True
    assert d["color_choice_was_already_target_assisted"] is True
    pairs=d["phase_filtered_pairs"]
    assert len(pairs)==3
    assert all(p["candidate_offsets_considered"]==1002001 for p in pairs)
    assert [(x["a_rgb"],x["b_rgb"],x["historical_delta_xy"]) for x in pairs]==[
        ("050105","020206",[1137,117]),
        ("030303","030300",[1107,-64]),
        ("030101","010401",[1029,21]),
    ]
    assert [(p["correct_delta_overlap"],p["better_overlaps"],p["equal_overlaps"]) for p in pairs]==[
        (52,136,5),(24,1148,93),(5,2233,164),
    ]
    assert all(p["better_overlaps"]>0 for p in pairs)
    return d

def source_only_scan(d, source_path):
    from PIL import Image
    import numpy as np
    raw=Path(source_path).read_bytes()
    assert sha256(raw).hexdigest()==SOURCE_SHA256
    im=np.asarray(Image.open(source_path).convert("RGB"))
    assert im.shape==(4096,2048,3)
    wanted=set()
    for p in d["phase_filtered_pairs"]:
        wanted.add(p["a_rgb"])
        wanted.add(p["b_rgb"])
    xy={}
    for c in sorted(wanted):
        rgb=tuple(bytes.fromhex(c))
        ys,xs=np.where(np.all(im==rgb,axis=2))
        phase=d["source_native_phases"][c]
        good=(xs%16==phase[0])&(ys%16==phase[1])
        xy[c]=(xs[good].astype(np.int32),ys[good].astype(np.int32))
        assert len(xy[c][0])==d["source_phase_point_counts"][c],(c,len(xy[c][0]))

    results=[]
    for p in d["phase_filtered_pairs"]:
        ax,ay=xy[p["a_rgb"]]
        bx,by=xy[p["b_rgb"]]
        low_x,high_x=p["dx_search_range"]
        low_y,high_y=p["dy_search_range"]
        w=high_x-low_x+1
        h=high_y-low_y+1
        assert (w,h)==(1001,1001)
        hist=np.zeros((h,w),dtype=np.int32)
        # Correlation is counted FROM ORIGINAL SOURCE COORDINATES ONLY.
        # Each B-to-A pair votes for a source displacement (xB-xA,yB-yA).
        for j in range(0,len(bx),40):
            dx=bx[j:j+40,None]-ax[None,:]
            dy=by[j:j+40,None]-ay[None,:]
            keep=(dx>=low_x)&(dx<=high_x)&(dy>=low_y)&(dy<=high_y)
            ids=(dy[keep]-low_y)*w+(dx[keep]-low_x)
            hist+=np.bincount(ids,minlength=h*w).reshape(h,w).astype(np.int32)
        # The historical correct delta is examined only AFTER computing the
        # source-only shift histogram; it never affects candidate scoring.
        tx,ty=p["historical_delta_xy"]
        actual=int(hist[ty-low_y,tx-low_x])
        better=int((hist>actual).sum())
        equal=int((hist==actual).sum())
        winner=int(hist.max())
        winners=np.argwhere(hist==winner)
        best=[int(winners[0,1]+low_x),int(winners[0,0]+low_y)]
        assert (actual,better,equal,winner,best)==(
            p["correct_delta_overlap"],p["better_overlaps"],p["equal_overlaps"],
            p["top_overlap_count"],p["winning_delta_xy"]
        ),(p,actual,better,equal,winner,best)
        results.append({
            "colors":[p["a_rgb"],p["b_rgb"]],
            "historical_delta":[tx,ty],
            "source_only_pair_overlap_at_historical_delta":actual,
            "shifts_scoring_strictly_better":better,
            "shifts_tied":equal,
            "source_only_top_delta":best,
            "source_only_top_overlap":winner,
            "conclusion":"historical delta is NOT the source-only maximum",
        })
    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",help="Original authenticated gate98 PNG; optional for strict source replay")
    args=p.parse_args()
    d=freeze()
    if args.source:
        print(json.dumps(source_only_scan(d,args.source),indent=2))
    else:
        print(json.dumps({
            "status":"PASS: historical delta is not best source-only overlap for three independent phase-filtered layer pairs",
            "note":"Fixture-only; --source replays full phase-dot correlations on authenticated PNG",
            "tests":[{"colors":[q["a_rgb"],q["b_rgb"]],
                      "better_shifts":q["better_overlaps"],
                      "best_overlap":q["top_overlap_count"],
                      "historic_overlap":q["correct_delta_overlap"]}
                     for q in d["phase_filtered_pairs"]]
        },indent=2))

if __name__=="__main__":
    main()

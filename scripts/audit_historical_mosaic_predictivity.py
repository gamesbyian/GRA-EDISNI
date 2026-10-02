#!/usr/bin/env python3
"""Experiment 364: holdout predictivity of the exact Dec-2022 historical 3x3 mosaic."""
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/"data"/"observations.csv"
OUT=ROOT/"data"/"experiment-364-historical-mosaic-predictivity.json"

# Within one consecutive A-I row, historical screenshots place cells in:
# I A B / C D E / F G H.
LOCAL={
    8:(0,0), 0:(0,1), 1:(0,2),
    2:(1,0), 3:(1,1), 4:(1,2),
    5:(2,0), 6:(2,1), 7:(2,2),
}

def load():
    out={}
    with OBS.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s:
                raise AssertionError(f"conflict at residue {r}")
            out[r]=s
    return out

def coord(r):
    frame=(r-1)//9
    within=(r-1)%9
    mr,mc=divmod(frame,3)
    lr,lc=LOCAL[within]
    return mr*3+lr,mc*3+lc

def alphabet(r):
    return {"/","-"} if r<=81 else {"/","."}

def baseline(r):
    return "/" if r<=81 else "."

def predict_one(r,truth,obs,mode):
    inverse={coord(x):x for x in range(1,109)}
    rr,cc=coord(r)
    vals=[]
    for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)):
        q=(rr+dr,cc+dc)
        other=inverse.get(q)
        if other is None or other==r or other not in obs:
            continue
        same_tile=(q[0]//3,q[1]//3)==(rr//3,cc//3)
        if mode=="within_tile" and not same_tile:
            continue
        if mode=="cross_tile" and same_tile:
            continue
        sym=obs[other]
        if sym in alphabet(r):
            vals.append(sym)
    pred=None
    if vals:
        c=Counter(vals).most_common()
        if len(c)==1 or c[0][1]>c[1][1]:
            pred=c[0][0]
    return {
        "residue":r,
        "truth":truth,
        "prediction":pred,
        "neighbors":vals,
        "prediction_correct":None if pred is None else pred==truth,
        "baseline":baseline(r),
        "baseline_correct":baseline(r)==truth,
    }

def summarize(rows):
    p=[x for x in rows if x["prediction"] is not None]
    return {
        "observations":len(rows),
        "predicted":len(p),
        "abstained":len(rows)-len(p),
        "correct":sum(bool(x["prediction_correct"]) for x in p),
        "accuracy":sum(bool(x["prediction_correct"]) for x in p)/len(p),
        "baseline_correct_same_coverage":sum(bool(x["baseline_correct"]) for x in p),
        "baseline_accuracy_same_coverage":sum(bool(x["baseline_correct"]) for x in p)/len(p),
    }

def main():
    obs=load()
    assert len(obs)==65
    result={
        "experiment":364,
        "input":"data/observations.csv",
        "historical_transform":{
            "within_row_background_geometry":["IAB","CDE","FGH"],
            "tile_layout":"12 consecutive 3x3 tiles arranged 3 across x 4 down",
            "source_attachment_top9":"image-a6a790f9807f3e47.png",
            "source_attachment_full":"image-e272a602e0c11f7a.png",
        },
        "modes":{},
    }
    for mode in ("all","within_tile","cross_tile"):
        rows=[predict_one(r,obs[r],obs,mode) for r in sorted(obs)]
        result["modes"][mode]={"summary":summarize(rows),"predictions":rows}
    a=result["modes"]["all"]["summary"]
    w=result["modes"]["within_tile"]["summary"]
    c=result["modes"]["cross_tile"]["summary"]
    assert (a["predicted"],a["correct"],a["baseline_correct_same_coverage"])==(46,19,28)
    assert (w["predicted"],w["correct"],w["baseline_correct_same_coverage"])==(47,21,29)
    assert (c["predicted"],c["correct"],c["baseline_correct_same_coverage"])==(26,11,14)
    result["interpretation"]="The exact historical mosaic does not improve local same-symbol holdout inference; its durable value is frame-internal 3x3 structure rather than cross-frame visual continuity."
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

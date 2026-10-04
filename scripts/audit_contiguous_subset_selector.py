#!/usr/bin/env python3
"""Experiment 400: test the historically proposed 9+3 'smaller subset' idea
as a contiguous three-bit body-chunk selector.

The first nine cells of each class word have three contiguous Q-chunks of
three d-bits. The tail is a one-of-three selector. This experiment asks whether
using the tail value to choose one contiguous Q-chunk yields a natural ternary
one-minority code inside that chosen chunk.
"""

from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-400-contiguous-subset-selector.json"

SERIAL="ABCDEFGHI"

def tail_selector(master,j):
    depths=[
        d for d in range(3)
        if master[(82+9*d+j)-1]=="/"
    ]
    return depths[0] if len(depths)==1 else None

def selected_chunk(master,j):
    q=tail_selector(master,j)
    if q is None:
        return None
    return tuple(
        master[(1+27*q+9*d+j)-1]
        for d in range(3)
    )

def decode_one_mark(chunk,mark):
    hits=[i for i,ch in enumerate(chunk) if ch==mark]
    return hits[0] if len(hits)==1 else None

def summarize(masters,mark):
    counts={}
    valid=0
    for master in masters:
        vals=[]
        ok=True
        for j in range(9):
            chunk=selected_chunk(master,j)
            v=decode_one_mark(chunk,mark)
            if v is None:
                ok=False
                break
            vals.append(str(v))
        if ok:
            valid+=1
            key="".join(vals)
            counts[key]=counts.get(key,0)+1
    return {
        "candidate_count":len(masters),
        "valid_all_nine":valid,
        "distinct_outputs":len(counts),
        "output_counts":dict(sorted(counts.items())),
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    result={
        "experiment":400,
        "historical_cue":"May-2026 proposal: first nine bits form a larger domain and last three select a smaller subset",
        "tested_operation":"tail one-of-three selector chooses one of the three contiguous Q chunks inside the first-nine body; selected 3-bit chunk is then asked to encode a one-dash or one-slash ternary position",
        "ensembles":{},
    }
    for mark,name in (("-","one_dash"),("/","one_slash")):
        result["ensembles"][name]={
            "U2":summarize(u2,mark),
            "U4":summarize(u4,mark),
            "U5":summarize(u5,mark),
            "E2":summarize(e2,mark),
        }

    for mode in result["ensembles"].values():
        for summary in mode.values():
            assert summary["valid_all_nine"]==0

    result["classification"]="hard negative"
    result["interpretation"]=(
        "The natural contiguous-subset reading of the historical 9+3 proposal fails before semantics. "
        "No U2/U4/U5/E2 completion makes all nine tail-selected Q chunks into valid one-dash or one-slash "
        "three-state codes. This sharply favors the type-preserving strided d-selection used by G5 over "
        "the cross-axis idea that the d-typed tail simply chooses a contiguous Q chunk. Do not widen into "
        "arbitrary regroupings of the first nine bits without a new external cue."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

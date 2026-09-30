#!/usr/bin/env python3
"""Experiment 342: test the historically attested sticker-symbol -> lever cue.

The March-2021 community hypothesis supplies an independent geometric mapping:
slash=UP, dash=RIGHT, dot=LEFT. This script tests the cheapest direct consumer:
whether the known 14-input bunker password occurs as a contiguous cyclic H108
window, without filling unknown sticker residues.
"""

from __future__ import annotations
import argparse, csv, json
from itertools import permutations
from pathlib import Path

DIRECTIONS="URL"
SYMBOLS="/-."
NORMAL_CODE="UURLRRRUUURLLL"
CUE_MAP={"U":"/","R":"-","L":"."}

def load(path:Path)->dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s:
                raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def scan(obs,code,mapping):
    pattern="".join(mapping[x] for x in code)
    rows=[]
    for start in range(1,109):
        bad=[]; known=0
        for j,want in enumerate(pattern):
            residue=((start-1+j)%108)+1
            got=obs.get(residue)
            if got is not None:
                known+=1
                if got!=want:
                    bad.append({"residue":residue,"observed":got,"expected":want})
        rows.append({"start":start,"known":known,"mismatch_count":len(bad),"mismatches":bad})
    exact=[x for x in rows if x["mismatch_count"]==0]
    best=min(x["mismatch_count"] for x in rows)
    best_rows=[x for x in rows if x["mismatch_count"]==best]
    return {"pattern":pattern,"exact":exact,"best_mismatch_count":best,"best":best_rows}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))

    forward=scan(obs,NORMAL_CODE,CUE_MAP)
    reverse=scan(obs,NORMAL_CODE[::-1],CUE_MAP)

    relabel_controls=[]
    for perm in permutations(SYMBOLS):
        mapping=dict(zip(DIRECTIONS,perm))
        f=scan(obs,NORMAL_CODE,mapping)
        r=scan(obs,NORMAL_CODE[::-1],mapping)
        relabel_controls.append({
            "mapping":mapping,
            "forward_exact_count":len(f["exact"]),
            "reverse_exact_count":len(r["exact"]),
            "best_forward_mismatches":f["best_mismatch_count"],
            "best_reverse_mismatches":r["best_mismatch_count"],
        })

    cyclic=[]
    for reverse_flag in (False,True):
        base=NORMAL_CODE[::-1] if reverse_flag else NORMAL_CODE
        for rotation in range(len(base)):
            code=base[rotation:]+base[:rotation]
            result=scan(obs,code,CUE_MAP)
            for hit in result["exact"]:
                cyclic.append({
                    "reverse":reverse_flag,
                    "rotation":rotation,
                    "rotated_code":code,
                    "pattern":result["pattern"],
                    "start":hit["start"],
                    "known_cells_tested":hit["known"],
                })

    out={
      "normal_lever_code":NORMAL_CODE,
      "historical_cue_mapping":CUE_MAP,
      "canonical_forward":forward,
      "canonical_reverse":reverse,
      "all_six_symbol_direction_relabel_controls":relabel_controls,
      "cyclic_rotation_sensitivity_under_historical_mapping":cyclic,
      "interpretation":{
        "canonical_direct_read":"ruled out: no contiguous cyclic H108 start matches the known normal lever code",
        "mapping_sensitivity":"all six symbol-direction permutations also have zero exact forward/reverse canonical-start placements",
        "cyclic_sensitivity":"one weak hit appears only after adding cyclic code rotation: rotation 11 at H108 start 98, constrained by just five observed cells",
        "consumer_status":"the lever remains independently motivated as a possible consumer of sticker symbols; only the cheapest known-password replay is closed"
      }
    }
    assert len(forward["exact"])==0
    assert forward["best_mismatch_count"]==2
    assert [(x["start"],x["known"]) for x in forward["best"]]==[(47,8),(101,6)]
    assert len(reverse["exact"])==0
    assert reverse["best_mismatch_count"]==1
    assert sum(x["forward_exact_count"]+x["reverse_exact_count"] for x in relabel_controls)==0
    assert cyclic==[{
      "reverse":False,"rotation":11,"rotated_code":"LLLUURLRRRUUUR",
      "pattern":"...//-.---///-","start":98,"known_cells_tested":5
    }]
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

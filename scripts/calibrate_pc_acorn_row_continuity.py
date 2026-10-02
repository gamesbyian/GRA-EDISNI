#!/usr/bin/env python3
"""Experiment 362: positive-control calibration on the solved PC acorn order."""
from __future__ import annotations
import json, random, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/printer-reference/pc-ps4-raw.txt"
SOLVED=ROOT/"data/printer-reference/pc-ps4-acorn-order.txt"
OUT=ROOT/"data/experiment-362-pc-acorn-row-continuity.json"
TRIALS=100_000
SEED=362

def data_lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines()
            if x.strip() and not x.startswith("#")]

def pair(a,b,cols):
    return sum(1 if a[j]==b[j] else -1 for j in cols)

def score(order,cols):
    return sum(pair(a,b,cols) for a,b in zip(order,order[1:]))

def monte(rows,cols):
    rng=random.Random(SEED)
    vals=[]
    p=list(rows)
    for _ in range(TRIALS):
        rng.shuffle(p)
        vals.append(score(p,cols))
    return vals

def summarize(rows,solved,cols):
    canonical=score(solved,cols)
    vals=monte(rows,cols)
    exceed=sum(v>=canonical for v in vals)
    mu=statistics.mean(vals); sd=statistics.pstdev(vals)
    return {
        "canonical_score":canonical,
        "null_trials":TRIALS,
        "null_seed":SEED,
        "null_mean":mu,
        "null_sd":sd,
        "null_min":min(vals),
        "null_max":max(vals),
        "null_count_ge_canonical":exceed,
        "add_one_tail_estimate":(exceed+1)/(TRIALS+1),
        "z_from_null_mean_sd":(canonical-mu)/sd if sd else None,
    }

def main():
    raw=data_lines(RAW)
    solved=data_lines(SOLVED)
    assert len(raw)==32 and len(solved)==32
    assert len(set(raw))==32 and set(raw)==set(solved)
    assert all(len(x)==32 for x in raw+solved)

    spaces={
        "all32":list(range(32)),
        "left8":list(range(8)),
        "right8":list(range(24,32)),
        "inner24":list(range(4,28)),
    }
    result={
        "experiment":362,
        "raw_fixture":"data/printer-reference/pc-ps4-raw.txt",
        "solved_fixture":"data/printer-reference/pc-ps4-acorn-order.txt",
        "score":"sum across adjacent rows and selected aligned columns of +1 equal / -1 unequal",
        "spaces":{name:summarize(raw,solved,cols) for name,cols in spaces.items()},
        "published_raw_order_score_all32":score(raw,range(32)),
    }
    allr=result["spaces"]["all32"]
    assert allr["canonical_score"]==176
    assert allr["null_count_ge_canonical"]==0
    assert allr["null_max"] < allr["canonical_score"]
    assert result["published_raw_order_score_all32"]==124
    result["interpretation"]="The same continuity family used on H108 strongly detects the independently solved PC acorn order, making the negative H108 ordering results materially more informative."
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

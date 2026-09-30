#!/usr/bin/env python3
"""Experiment 337: null calibration for the exploratory row-vs-column asymmetry.

The one-exception criterion was discovered after inspecting row/column outputs.
This script therefore does not claim a preregistered p-value. It asks how often
an asymmetry at least as qualitative as "some row solutions, zero column
solutions" arises under two simple fixed-mask permutation nulls.
"""

from __future__ import annotations
import argparse, csv, json, random
from pathlib import Path

CLASSES="ABCDEFGHI"
TAIL_ALLOWED={
    "A":[0,1,2],"B":[2],"C":[0,1,2],"D":[1,2],"E":[0],
    "F":[1],"G":[0,2],"H":[2],"I":[2],
}

def load(path:Path):
    vals={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in vals and vals[r]!=s: raise ValueError(f"conflict at residue {r}")
            vals[r]=s
    return vals

def template(vals):
    return {c:[vals.get(1+i+9*k,"?") for k in range(9)] for i,c in enumerate(CLASSES)}

def one_exception_possible(line):
    known=[x for x in line if x!="?"]
    if len(known)<3: return True
    return len(set(known))==2

def survivor_counts(body):
    rows=cols=1
    for c in CLASSES:
        nr=nc=0
        for p in TAIL_ALLOWED[c]:
            r=body[c][3*p:3*p+3]
            q=[body[c][p],body[c][p+3],body[c][p+6]]
            nr+=one_exception_possible(r)
            nc+=one_exception_possible(q)
        rows*=nr
        cols*=nc
    return rows,cols

def run_null(body,iterations,seed,stratified):
    rng=random.Random(seed)
    positions=[(c,k) for c in CLASSES for k,x in enumerate(body[c]) if x!="?"]
    global_labels=[body[c][k] for c,k in positions]
    per_class={
      c:([k for k,x in enumerate(body[c]) if x!="?"],
         [x for x in body[c] if x!="?"])
      for c in CLASSES
    }
    counts={"row_positive_col_zero":0,"row_at_least_observed_col_zero":0,
            "exact_observed_12_0":0,"row_at_least_observed":0,"col_zero":0}
    row_sum=col_sum=0
    for _ in range(iterations):
        b={c:["?"]*9 for c in CLASSES}
        if stratified:
            for c in CLASSES:
                idx,labs=per_class[c]
                shuffled=labs[:]; rng.shuffle(shuffled)
                for k,s in zip(idx,shuffled): b[c][k]=s
        else:
            shuffled=global_labels[:]; rng.shuffle(shuffled)
            for (c,k),s in zip(positions,shuffled): b[c][k]=s
        nr,nc=survivor_counts(b)
        row_sum+=nr; col_sum+=nc
        counts["row_positive_col_zero"] += nr>0 and nc==0
        counts["row_at_least_observed_col_zero"] += nr>=12 and nc==0
        counts["exact_observed_12_0"] += nr==12 and nc==0
        counts["row_at_least_observed"] += nr>=12
        counts["col_zero"] += nc==0
    return {
      "iterations":iterations,"seed":seed,
      "mean_row_survivors":row_sum/iterations,
      "mean_column_survivors":col_sum/iterations,
      **{k:{"count":v,"fraction":v/iterations} for k,v in counts.items()}
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    ap.add_argument("--iterations",type=int,default=200_000)
    ap.add_argument("--seed",type=int,default=337)
    args=ap.parse_args()
    body=template(load(Path(args.observations)))
    observed=survivor_counts(body)
    out={
      "observed":{"row_survivors":observed[0],"column_survivors":observed[1]},
      "global_fixed_mask_census_null":run_null(body,args.iterations,args.seed,False),
      "within_class_fixed_mask_census_null":run_null(body,args.iterations,args.seed,True),
      "interpretation":"The qualitative row-positive/column-zero asymmetry is common enough under both nulls that Experiment 329 should remain exploratory rather than be treated as strong retrospective evidence."
    }
    assert observed==(12,0)
    g=out["global_fixed_mask_census_null"]; s=out["within_class_fixed_mask_census_null"]
    assert g["row_positive_col_zero"]["count"]==55905
    assert g["exact_observed_12_0"]["count"]==8503
    assert s["row_positive_col_zero"]["count"]==44721
    assert s["exact_observed_12_0"]["count"]==6483
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

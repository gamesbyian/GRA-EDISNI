#!/usr/bin/env python3
"""Experiment 340: selection-aware calibration of Experiment 330 leave-one-out.

The row+one-exception family was formed using the full observed corpus.
Consequently a leave-one-out "correct forced prediction" from that same corpus
is not an independent holdout: whenever the full corpus is compatible, the true
symbol is necessarily among the hidden-cell possibilities, so any singleton
prediction must equal the held-out truth.

This script demonstrates that logical fact and calibrates the number of forced
cells under null datasets that would have produced the same qualitative
row-survives / column-dies discovery event.
"""

from __future__ import annotations
import argparse, csv, json, random
from itertools import product
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
            nr+=one_exception_possible(body[c][3*p:3*p+3])
            col=[body[c][p],body[c][p+3],body[c][p+6]]
            nc+=one_exception_possible(col)
        rows*=nr; cols*=nc
    return rows,cols

def hidden_possibilities(body,c,k):
    hidden=body[c][:]
    hidden[k]="?"
    viable=[p for p in TAIL_ALLOWED[c] if one_exception_possible(hidden[3*p:3*p+3])]
    poss=set()
    row_k=k//3
    for p in viable:
        if p!=row_k:
            poss.update("/-")
            continue
        line=hidden[3*p:3*p+3]
        unknown=[i for i,x in enumerate(line) if x=="?"]
        for bits in product("/-",repeat=len(unknown)):
            a=line[:]
            for i,s in zip(unknown,bits): a[i]=s
            if a.count("/") in (1,2):
                poss.add(a[k%3])
    return poss

def loo_metrics(body):
    forced=correct=wrong=0
    for c in CLASSES:
        for k,true in enumerate(body[c]):
            if true=="?": continue
            poss=hidden_possibilities(body,c,k)
            if len(poss)==1:
                forced+=1
                pred=next(iter(poss))
                correct+=pred==true
                wrong+=pred!=true
    return forced,correct,wrong

def run_null(body,iterations,seed,stratified):
    rng=random.Random(seed)
    positions=[(c,k) for c in CLASSES for k,x in enumerate(body[c]) if x!="?"]
    global_labels=[body[c][k] for c,k in positions]
    per_class={
      c:([k for k,x in enumerate(body[c]) if x!="?"],[x for x in body[c] if x!="?"])
      for c in CLASSES
    }
    selected=0
    forced_hist={}
    wrong_after_selection=0
    ge_observed=0
    for _ in range(iterations):
        b={c:["?"]*9 for c in CLASSES}
        if stratified:
            for c in CLASSES:
                idx,labs=per_class[c]
                sh=labs[:]; rng.shuffle(sh)
                for k,s in zip(idx,sh): b[c][k]=s
        else:
            sh=global_labels[:]; rng.shuffle(sh)
            for (c,k),s in zip(positions,sh): b[c][k]=s

        nr,nc=survivor_counts(b)
        if not (nr>0 and nc==0):
            continue
        selected+=1
        forced,correct,wrong=loo_metrics(b)
        forced_hist[str(forced)]=forced_hist.get(str(forced),0)+1
        wrong_after_selection+=wrong
        ge_observed+=forced>=4

    return {
      "iterations":iterations,
      "selected_row_positive_column_zero":selected,
      "selected_fraction":selected/iterations,
      "forced_count_histogram_after_selection":forced_hist,
      "forced_at_least_observed_4":ge_observed,
      "forced_at_least_observed_4_conditional_fraction":ge_observed/selected,
      "wrong_forced_predictions_after_selection":wrong_after_selection,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    ap.add_argument("--iterations",type=int,default=200_000)
    ap.add_argument("--seed",type=int,default=340)
    args=ap.parse_args()

    body=template(load(Path(args.observations)))
    observed=loo_metrics(body)
    out={
      "observed":{"forced":observed[0],"correct":observed[1],"wrong":observed[2]},
      "logical_result":"Because the family was selected on the complete corpus, any leave-one-out singleton prediction is guaranteed correct whenever that corpus remains compatible. Correctness is therefore not independent validation.",
      "global_fixed_mask_census_null":run_null(body,args.iterations,args.seed,False),
      "within_class_matched_null":run_null(body,args.iterations,args.seed,True),
    }
    assert observed==(4,4,0)
    g=out["global_fixed_mask_census_null"]
    s=out["within_class_matched_null"]
    assert g["selected_row_positive_column_zero"]==55410
    assert g["forced_count_histogram_after_selection"]=={"3":46940,"4":8470}
    assert g["wrong_forced_predictions_after_selection"]==0
    assert s["selected_row_positive_column_zero"]==44438
    assert s["forced_count_histogram_after_selection"]=={"3":38148,"4":6290}
    assert s["wrong_forced_predictions_after_selection"]==0
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Experiment 330: leave-one-out validation of the frozen row-selector rival."""

from __future__ import annotations
import argparse, csv, json
from itertools import product
from pathlib import Path

CLASSES="ABCDEFGHI"

def load(path:Path)->dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def tail_allowed(obs:dict[int,str])->dict[str,list[int]]:
    out={}
    for i,c in enumerate(CLASSES):
        t=[obs.get(82+i+9*k,"?") for k in range(3)]
        poss=[]
        for p in range(3):
            target=[".",".","."]; target[p]="/"
            if all(x=="?" or x==target[k] for k,x in enumerate(t)): poss.append(p)
        out[c]=poss
    return out

def body(obs:dict[int,str], c:str)->list[str]:
    i=CLASSES.index(c)
    return [obs.get(1+i+9*k,"?") for k in range(9)]

def line_completions(obs:dict[int,str],c:str,p:int)->list[list[str]]:
    line=body(obs,c)[3*p:3*p+3]
    unknown=[i for i,x in enumerate(line) if x=="?"]
    out=[]
    for bits in product("/-",repeat=len(unknown)):
        a=line[:]
        for i,b in zip(unknown,bits): a[i]=b
        if a.count("/") in (1,2): out.append(a)
    return out

def selectors(obs:dict[int,str])->list[dict[str,int]]:
    allowed=tail_allowed(obs)
    out=[]
    for picks in product(*(allowed[c] for c in CLASSES)):
        a=dict(zip(CLASSES,picks))
        if all(line_completions(obs,c,a[c]) for c in CLASSES): out.append(a)
    return out

def hidden_possibilities(obs:dict[int,str],residue:int)->set[str]:
    i=(residue-1)%9; c=CLASSES[i]; layer=(residue-1)//9
    row_i,cell_i=divmod(layer,3)
    poss=set()
    for a in selectors(obs):
        p=a[c]
        if p!=row_i:
            poss.update("/-")
        else:
            for comp in line_completions(obs,c,p): poss.add(comp[cell_i])
    return poss

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    results=[]
    for r,true in sorted((r,s) for r,s in obs.items() if r<=81):
        hidden=dict(obs); del hidden[r]
        poss=hidden_possibilities(hidden,r)
        results.append({"residue":r,"true":true,"possible":"".join(sorted(poss)),
                        "forced":len(poss)==1,"correct":true in poss})
    forced=[x for x in results if x["forced"]]
    excluded=[x for x in results if not x["correct"]]
    out={"body_holdouts":len(results),"forced":len(forced),"ambiguous":len(results)-len(forced),
         "excluded_true_symbol":len(excluded),"forced_cases":forced,"results":results,
         "status":"validation of frozen exploratory family; no further tuning performed"}
    assert len(results)==54
    assert [(x["residue"],x["true"]) for x in forced]==[(5,"/"),(66,"/"),(72,"-"),(74,"-")]
    assert not excluded
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

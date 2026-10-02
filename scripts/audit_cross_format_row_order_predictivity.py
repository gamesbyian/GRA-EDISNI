#!/usr/bin/env python3
"""Experiment 360: leave-one-observation-out row-order predictivity audit."""
from __future__ import annotations
import csv, json
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/"data"/"observations.csv"
OUT=ROOT/"data"/"experiment-360-row-order-predictivity.json"
FORMATS=("9x12","12x9")
CAP=500000

def load():
    out={}
    with OBS.open(newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise AssertionError(f"conflict at {r}")
            out[r]=s
    return out

def matrix(fmt,obs):
    if fmt=="9x12":
        m=[["?"]*12 for _ in range(9)]
        for r,s in obs.items(): m[(r-1)%9][(r-1)//9]=s
        return m
    m=[["?"]*9 for _ in range(12)]
    for r,s in obs.items(): m[(r-1)//9][(r-1)%9]=s
    return m

def weights(m):
    n=len(m); w=[[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(a+1,n):
            v=0
            for x,y in zip(m[a],m[b]):
                if x=="?" or y=="?": continue
                v += 1 if x==y else -1
            w[a][b]=w[b][a]=v
    return w

def max_paths(w):
    n=len(w); full=(1<<n)-1; neg=-10**9
    best=[[neg]*n for _ in range(1<<n)]
    count=[[0]*n for _ in range(1<<n)]
    preds=[[0]*n for _ in range(1<<n)]
    for j in range(n): best[1<<j][j]=0; count[1<<j][j]=1
    for mask in range(1,1<<n):
        if mask&(mask-1)==0: continue
        for last in range(n):
            if not mask&(1<<last): continue
            pm=mask^(1<<last); top=neg; ways=0; pb=0
            for prev in range(n):
                if not pm&(1<<prev): continue
                v=best[pm][prev]+w[prev][last]
                if v>top: top=v; ways=count[pm][prev]; pb=1<<prev
                elif v==top: ways+=count[pm][prev]; pb|=1<<prev
            best[mask][last]=top; count[mask][last]=ways; preds[mask][last]=pb
    maximum=max(best[full])
    ends=[j for j in range(n) if best[full][j]==maximum]
    total=sum(count[full][j] for j in ends)
    if total>CAP: raise AssertionError(f"{total} maximizing paths exceeds cap")
    paths=[]
    def bt(mask,last,suffix):
        if mask==(1<<last):
            paths.append(tuple(reversed(suffix+[last]))); return
        pm=mask^(1<<last); bits=preds[mask][last]
        while bits:
            bit=bits&-bits; bits-=bit; prev=bit.bit_length()-1
            bt(pm,prev,suffix+[last])
    for end in ends: bt(full,end,[])
    assert len(paths)==total
    return maximum,total,paths

def coords(fmt,r):
    return ((r-1)%9,(r-1)//9) if fmt=="9x12" else ((r-1)//9,(r-1)%9)

def alphabet(r): return ("/","-") if r<=81 else ("/",".")
def baseline(r): return "/" if r<=81 else "."

def predict(fmt,r,truth,full):
    train=dict(full); del train[r]
    m=matrix(fmt,train)
    maximum,total,paths=max_paths(weights(m))
    row,col=coords(fmt,r)
    scores={x:0 for x in alphabet(r)}
    for path in paths:
        i=path.index(row)
        ns=[]
        if i: ns.append(path[i-1])
        if i+1<len(path): ns.append(path[i+1])
        for other in ns:
            sym=m[other][col]
            if sym=="?": continue
            for cand in scores: scores[cand]+=1 if cand==sym else -1
    ranked=sorted(scores.items(),key=lambda x:x[1],reverse=True)
    pred=ranked[0][0] if ranked[0][1]>ranked[1][1] else None
    return {
        "residue":r,"truth":truth,"prediction":pred,
        "domain_majority_baseline":baseline(r),
        "candidate_scores":scores,
        "training_max_boundary_score":maximum,
        "maximizing_order_count":total,
        "prediction_correct":None if pred is None else pred==truth,
        "baseline_correct":baseline(r)==truth,
    }

def summary(rows):
    p=[x for x in rows if x["prediction"] is not None]
    body=[x for x in p if x["residue"]<=81]; tail=[x for x in p if x["residue"]>81]
    oo=bo=same=0
    for x in p:
        a=x["prediction_correct"]; b=x["baseline_correct"]
        if a and not b: oo+=1
        elif b and not a: bo+=1
        else: same+=1
    def part(xs):
        return {"predicted":len(xs),"correct":sum(bool(x["prediction_correct"]) for x in xs),
                "baseline_correct_same_coverage":sum(bool(x["baseline_correct"]) for x in xs)}
    return {
        "observations":len(rows),"predicted":len(p),"abstained":len(rows)-len(p),
        "correct":sum(bool(x["prediction_correct"]) for x in p),
        "accuracy":sum(bool(x["prediction_correct"]) for x in p)/len(p),
        "domain_majority_baseline_correct_same_coverage":sum(bool(x["baseline_correct"]) for x in p),
        "domain_majority_baseline_accuracy_same_coverage":sum(bool(x["baseline_correct"]) for x in p)/len(p),
        "paired_order_only_correct":oo,"paired_baseline_only_correct":bo,"paired_same_outcome":same,
        "body":part(body),"tail":part(tail),
        "maximizing_order_count":{"min":min(x["maximizing_order_count"] for x in rows),
                                  "max":max(x["maximizing_order_count"] for x in rows),
                                  "mean":mean(x["maximizing_order_count"] for x in rows)}
    }

def main():
    obs=load(); assert len(obs)==65
    result={"experiment":360,"input":"data/observations.csv",
      "question":"does continuity-optimized row sorting improve held-out symbol guessing in 9x12 or 12x9?",
      "selection_note":"exploratory utility calibration using the boundary score already frozen in Experiments 345/347; not prospective evidence for an ordering mechanism",
      "formats":{}}
    for fmt in FORMATS:
        rows=[predict(fmt,r,obs[r],obs) for r in sorted(obs)]
        result["formats"][fmt]={"summary":summary(rows),"predictions":rows}
    a=result["formats"]["9x12"]["summary"]; b=result["formats"]["12x9"]["summary"]
    assert (a["predicted"],a["correct"],a["domain_majority_baseline_correct_same_coverage"])==(47,29,33)
    assert (a["paired_order_only_correct"],a["paired_baseline_only_correct"])==(5,9)
    assert (b["predicted"],b["correct"],b["domain_majority_baseline_correct_same_coverage"])==(49,16,29)
    assert (b["paired_order_only_correct"],b["paired_baseline_only_correct"])==(3,16)
    result["interpretation"]="Neither continuity-optimized row-order family improves held-out symbol guessing over the body/tail majority baseline. Any productive row-sorting lane now needs an independent ordering cue or a different pre-specified image feature."
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()

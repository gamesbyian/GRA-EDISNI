#!/usr/bin/env python3
"""Experiment 361: literal Xbox printer envelope transfer to H108."""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/"data"/"observations.csv"
OUT=ROOT/"data"/"experiment-361-xbox-envelope-transfer.json"

def load():
    out={}
    with OBS.open(newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s:
                raise AssertionError(f"conflict at residue {r}")
            out[r]=s
    return out

def matrix(fmt,obs):
    if fmt=="12x9":
        m=[["?"]*9 for _ in range(12)]
        for r,s in obs.items():
            m[(r-1)//9][(r-1)%9]=s
        return m
    if fmt=="9x12":
        m=[["?"]*12 for _ in range(9)]
        for r,s in obs.items():
            m[(r-1)%9][(r-1)//9]=s
        return m
    raise ValueError(fmt)

def compatible_depths(row):
    w=len(row); out=[]
    for k in range((w-1)//2+1):
        right=w-1-k
        ok=True
        for j,s in enumerate(row):
            if s=="?":
                continue
            if j==k or j==right:
                if s!="/":
                    ok=False; break
            elif j<k or j>right:
                if s!="-":
                    ok=False; break
        if ok:
            out.append(k)
    return out

def analyse(fmt,obs):
    rows=matrix(fmt,obs)
    detail=[]
    for i,row in enumerate(rows):
        ds=compatible_depths(row)
        detail.append({
            "index":i+1,
            "trace":"".join(row),
            "compatible_depths_zero_based":ds,
            "compatible":bool(ds),
        })
    return {
        "row_count":len(rows),
        "compatible_rows":sum(x["compatible"] for x in detail),
        "incompatible_rows":[x["index"] for x in detail if not x["compatible"]],
        "rows":detail,
    }

def main():
    obs=load()
    result={
        "experiment":361,
        "input":"data/observations.csv",
        "historical_mechanism":"mirrored slash boundary with dash exterior; interior payload unrestricted",
        "guardrail":"literal Xbox mechanism only; unknown cells remain free; no symbol-role permutations or cyclic offsets",
        "formats":{
            "12x9":analyse("12x9",obs),
            "9x12":analyse("9x12",obs),
        },
    }
    a=result["formats"]["12x9"]; b=result["formats"]["9x12"]
    assert a["compatible_rows"]==8
    assert a["incompatible_rows"]==[3,5,8,10]
    assert b["compatible_rows"]==8
    assert b["incompatible_rows"]==[3]
    result["body_12x9_first9"]={
        "compatible_rows":sum(result["formats"]["12x9"]["rows"][i]["compatible"] for i in range(9)),
        "incompatible_rows":[i+1 for i in range(9) if not result["formats"]["12x9"]["rows"][i]["compatible"]],
    }
    assert result["body_12x9_first9"]=={"compatible_rows":6,"incompatible_rows":[3,5,8]}
    result["interpretation"]="The literal Xbox slash-envelope ordering channel is contradicted in both candidate sticker layouts before row ordering is attempted."
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Experiment 333: background-coordinate vs frozen 3x3 token-coordinate audit."""

from __future__ import annotations
import argparse, csv, json
from itertools import product
from pathlib import Path

CLASSES="ABCDEFGHI"
BACKGROUND={"I":(0,0),"A":(0,1),"B":(0,2),"C":(1,0),"D":(1,1),"E":(1,2),"F":(2,0),"G":(2,1),"H":(2,2)}

def load(path:Path)->dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def one_exception(line):
    u=[i for i,x in enumerate(line) if x=="?"]
    out=[]
    for bits in product("/-",repeat=len(u)):
        a=line[:]
        for i,b in zip(u,bits): a[i]=b
        if a.count("/") in (1,2): out.append(a)
    return out

def d4(p):
    r,c=p
    return {
      "identity":(r,c),"rot90":(c,2-r),"rot180":(2-r,2-c),"rot270":(2-c,r),
      "mirror_vertical":(r,2-c),"mirror_horizontal":(2-r,c),
      "main_diagonal":(c,r),"anti_diagonal":(2-c,2-r),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    coords={}
    tokens={}
    for ci,c in enumerate(CLASSES):
        body=[obs.get(1+ci+9*k,"?") for k in range(9)]
        tail=[obs.get(82+ci+9*k,"?") for k in range(3)]
        ts=set()
        for p in range(3):
            target=[".",".","."]; target[p]="/"
            if not all(x=="?" or x==target[k] for k,x in enumerate(tail)): continue
            for comp in one_exception(body[3*p:3*p+3]):
                if comp.count("/")==1: e=comp.index("/"); pol="/"
                else: e=comp.index("-"); pol="-"
                ts.add((p,e,pol))
        tokens[c]=ts
        coords[c]={(p,e) for p,e,_ in ts}

    fixed={c:next(iter(tokens[c])) for c in CLASSES if len(tokens[c])==1}
    d4_results={}
    for name in d4((0,0)):
        failures=[]
        for c in CLASSES:
            target=d4(BACKGROUND[c])[name]
            if target not in coords[c]: failures.append(c)
        d4_results[name]={"compatible":not failures,"failing_classes":failures}

    same_fixed_coordinate_pairs=[]
    fixed_names=sorted(fixed)
    for i,a in enumerate(fixed_names):
        for b in fixed_names[i+1:]:
            if fixed[a][:2]==fixed[b][:2]:
                same_fixed_coordinate_pairs.append({
                    "classes":[a,b],
                    "background_coordinates":[BACKGROUND[a],BACKGROUND[b]],
                    "token_coordinate":fixed[a][:2],
                    "token_polarities":[fixed[a][2],fixed[b][2]],
                })

    out={
      "physical_background_layout":"IAB/CDE/FGH",
      "fixed_tokens":{c:fixed[c] for c in fixed},
      "fixed_distinct_sources_same_token_coordinate":same_fixed_coordinate_pairs,
      "injective_coordinate_map_possible":len(same_fixed_coordinate_pairs)==0,
      "d4_tests":d4_results,
      "d4_survivors":[k for k,v in d4_results.items() if v["compatible"]],
      "interpretation":"Direct coordinate-copy is impossible; this does not exclude background artwork as a non-coordinate mask, ordering cue, or transform source."
    }
    assert set(fixed)=={"B","C","E","I"}
    assert [(x["classes"],tuple(x["token_coordinate"])) for x in same_fixed_coordinate_pairs]==[(["C","I"],(2,1))]
    assert out["injective_coordinate_map_possible"] is False
    assert out["d4_survivors"]==[]
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

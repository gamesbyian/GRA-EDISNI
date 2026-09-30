#!/usr/bin/env python3
"""Experiment 334: enumerate bounded conventional Pigpen A-R codebooks.

No semantic scoring is performed. This only maps the frozen 3x3x2 token carrier
onto the conventional two row-major 3x3 Pigpen grids under D4 orientation and
global binary-layer swap.
"""

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

def one_exception(line):
    u=[i for i,x in enumerate(line) if x=="?"]
    out=[]
    for bits in product("/-",repeat=len(u)):
        a=line[:]
        for i,b in zip(u,bits): a[i]=b
        if a.count("/") in (1,2): out.append(a)
    return out

def d4_named(p):
    r,c=p
    return {
      "identity":(r,c),"rot90":(c,2-r),"rot180":(2-r,2-c),"rot270":(2-c,r),
      "mirror_vertical":(r,2-c),"mirror_horizontal":(2-r,c),
      "main_diagonal":(c,r),"anti_diagonal":(2-c,2-r),
    }

def token_sets(obs):
    out={}
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
        out[c]=ts
    return out

def letter_for(token, transform, slash_first):
    r,c,pol=token
    rr,cc=d4_named((r,c))[transform]
    layer=0 if ((pol=="/") == slash_first) else 1
    idx=rr*3+cc
    return chr(ord("A")+layer*9+idx)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    tokens=token_sets(obs)
    fixed={c:next(iter(ts)) for c,ts in tokens.items() if len(ts)==1}
    codebooks=[]
    for transform in d4_named((0,0)):
        for slash_first in (True,False):
            possible={}
            for c,ts in tokens.items():
                possible[c]="".join(sorted({letter_for(t,transform,slash_first) for t in ts}))
            fixed_signature="".join(letter_for(fixed[c],transform,slash_first) for c in sorted(fixed))
            codebooks.append({
              "transform":transform,
              "slash_exception_grid":"A-I" if slash_first else "J-R",
              "dash_exception_grid":"J-R" if slash_first else "A-I",
              "possible_letters":possible,
              "fixed_class_order":"BCEI",
              "fixed_signature_BCEI":fixed_signature,
            })
    signatures={x["fixed_signature_BCEI"] for x in codebooks}
    out={
      "codebook_count":len(codebooks),
      "global_degrees_of_freedom":{"D4_orientations":8,"binary_layer_swaps":2},
      "fixed_classes":{c:fixed[c] for c in sorted(fixed)},
      "distinct_fixed_signatures":len(signatures),
      "codebooks":codebooks,
      "status":"enumeration only; no plaintext/language scoring or codebook selection"
    }
    assert len(codebooks)==16
    assert len(fixed)==4
    assert len(signatures)==16
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

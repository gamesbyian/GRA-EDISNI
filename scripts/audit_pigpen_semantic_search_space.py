#!/usr/bin/env python3
"""Experiment 335: quantify the bounded Pigpen A-R semantic search space.

No language scoring is performed. Counts all 9-letter outputs licensed by
Experiment 334's 16 global codebooks and Experiment 332's observation-compatible
token sets.
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

def d4(p):
    r,c=p
    return {
      "identity":(r,c),"rot90":(c,2-r),"rot180":(2-r,2-c),"rot270":(2-c,r),
      "mirror_vertical":(r,2-c),"mirror_horizontal":(2-r,c),
      "main_diagonal":(c,r),"anti_diagonal":(2-c,2-r),
    }

def letter(token,transform,slash_first):
    r,c,pol=token; rr,cc=d4((r,c))[transform]
    layer=0 if ((pol=="/")==slash_first) else 1
    return chr(ord("A")+layer*9+rr*3+cc)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    tokens=token_sets(load(Path(args.observations)))
    per_codebook={}
    union=set()
    for transform in d4((0,0)):
        for slash_first in (True,False):
            key=f"{transform}|{'slash_first' if slash_first else 'dash_first'}"
            strings={
              "".join(letter(t,transform,slash_first) for t in choice)
              for choice in product(*(tokens[c] for c in CLASSES))
            }
            per_codebook[key]=len(strings)
            union |= strings
    product_size=1
    for c in CLASSES: product_size*=len(tokens[c])
    out={
      "token_assignments_per_codebook":product_size,
      "global_codebooks":len(per_codebook),
      "strings_per_codebook":per_codebook,
      "codebook_string_pairs":sum(per_codebook.values()),
      "unique_strings_across_all_codebooks":len(union),
      "cross_codebook_string_collisions":sum(per_codebook.values())-len(union),
      "fixed_letters_per_codebook":sum(len(tokens[c])==1 for c in CLASSES),
      "status":"counting only; semantic/language scoring prohibited without an external registration cue",
    }
    assert product_size==900
    assert len(per_codebook)==16
    assert set(per_codebook.values())=={900}
    assert len(union)==14400
    assert out["cross_codebook_string_collisions"]==0
    assert out["fixed_letters_per_codebook"]==4
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

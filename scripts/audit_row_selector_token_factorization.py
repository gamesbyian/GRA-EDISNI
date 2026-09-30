#!/usr/bin/env python3
"""Experiment 332: factor frozen row-selector outputs into 3x3x2 tokens."""

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

def one_exception_completions(line):
    unknown=[i for i,x in enumerate(line) if x=="?"]
    out=[]
    for bits in product("/-",repeat=len(unknown)):
        a=line[:]
        for i,b in zip(unknown,bits): a[i]=b
        if a.count("/") in (1,2): out.append(a)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    rows={}
    all_tokens=set()
    for ci,c in enumerate(CLASSES):
        body=[obs.get(1+ci+9*k,"?") for k in range(9)]
        tail=[obs.get(82+ci+9*k,"?") for k in range(3)]
        tokens=set()
        for p in range(3):
            target=[".",".","."]; target[p]="/"
            if not all(x=="?" or x==target[k] for k,x in enumerate(tail)): continue
            for comp in one_exception_completions(body[3*p:3*p+3]):
                if comp.count("/")==1:
                    exceptional_symbol="/"; e=comp.index("/")
                else:
                    exceptional_symbol="-"; e=comp.index("-")
                tokens.add((p,e,exceptional_symbol))
        all_tokens |= tokens
        rows[c]={
          "token_count":len(tokens),
          "tokens":[{"row":p,"column":e,"exceptional_symbol":s} for p,e,s in sorted(tokens)]
        }

    universe=[(r,c,s) for r in range(3) for c in range(3) for s in ("/","-")]
    fixed={c:rows[c]["tokens"][0] for c in CLASSES if rows[c]["token_count"]==1}
    out={
      "token_definition":"(tail-selected row, exceptional position within row, exceptional symbol)",
      "abstract_token_universe_size":len(universe),
      "pigpen_tic_tac_toe_half_cardinality":18,
      "full_standard_pigpen_alphabet_cardinality":26,
      "missing_full_alphabet_states":8,
      "classes":rows,
      "fully_fixed_classes":fixed,
      "fixed_class_count":len(fixed),
      "note":"18-state cardinality is isomorphic to two 3x3 grids, but cardinality alone does not establish a Pigpen codebook and supplies no X-grid/S-Z family."
    }
    assert len(universe)==18
    assert {c:rows[c]["token_count"] for c in CLASSES}=={"A":9,"B":1,"C":1,"D":5,"E":1,"F":2,"G":5,"H":2,"I":1}
    assert set(fixed)=={"B","C","E","I"}
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

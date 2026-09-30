#!/usr/bin/env python3
"""Experiment 328: one-symbol-as-ink 3x3 D4 identifiability audit.

Unknown body cells are exhaustively completed. Slash is treated as filled/ink
and dash as empty; the opposite global polarity is an exact complement
bijection and therefore has identical identifiability counts.
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

def d4(mask:tuple[int,...])->set[tuple[int,...]]:
    g=[list(mask[i*3:(i+1)*3]) for i in range(3)]
    out=set(); cur=g
    for _ in range(4):
        out.add(tuple(x for row in cur for x in row))
        refl=[row[::-1] for row in cur]
        out.add(tuple(x for row in refl for x in row))
        cur=[list(row) for row in zip(*cur[::-1])]
    return out

def canon(mask:tuple[int,...])->tuple[int,...]:
    return min(d4(mask))

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    orbit_sets={}
    rows={}
    for i,c in enumerate(CLASSES):
        body=[obs.get(1+i+9*k,"?") for k in range(9)]
        unknown=[j for j,x in enumerate(body) if x=="?"]
        orbits=set()
        for bits in product("/-",repeat=len(unknown)):
            a=body[:]
            for j,b in zip(unknown,bits): a[j]=b
            orbits.add(canon(tuple(1 if x=="/" else 0 for x in a)))
        orbit_sets[c]=orbits
        rows[c]={"trace":"".join(body),"unknown_cells":len(unknown),
                 "raw_completions":2**len(unknown),"d4_orbits":len(orbits)}

    ordered=sorted(CLASSES,key=lambda c:len(orbit_sets[c]))
    def distinct_count(k:int,used:set[tuple[int,...]])->int:
        if k==len(ordered): return 1
        c=ordered[k]
        return sum(distinct_count(k+1,used|{o}) for o in orbit_sets[c] if o not in used)

    all_choices=1
    for c in CLASSES: all_choices*=len(orbit_sets[c])
    distinct=distinct_count(0,set())
    overlaps={}
    for ai,a in enumerate(CLASSES):
        for b in CLASSES[ai+1:]:
            n=len(orbit_sets[a]&orbit_sets[b])
            if n: overlaps[a+b]=n

    out={"classes":rows,"pairwise_orbit_overlaps":overlaps,
         "all_orbit_choice_assignments":all_choices,
         "all_distinct_orbit_assignments":distinct,
         "all_distinct_fraction":distinct/all_choices,
         "global_polarity_note":"dash-as-ink is the complement bijection of slash-as-ink, so these counts are unchanged."}
    assert [rows[c]["d4_orbits"] for c in CLASSES]==[28,2,1,16,16,4,20,8,8]
    assert all_choices==73_400_320
    assert distinct==50_550_408
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

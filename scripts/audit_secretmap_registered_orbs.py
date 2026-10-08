#!/usr/bin/env python3
"""SecretMap preregistered marker-to-orb comparison. No fit to CE sticker data.

The *only* permitted registration is explicit beforehand in a JSON file.
Use physical or Unity scene coordinates with documented common units.
Input JSON: {"source": "...", "orb_source": "...",
 "registration": {"matrix_2x3": [[a,b,tx],[c,d,ty]],
                  "provenance": "...", "frozen_before_sticker_comparison": true},
 "tolerance": 0.5,
 "marks": [{"id":"m1","x":1,"y":2}, ...],
 "orbs": [{"id":"orb1","x":1,"y":2}, ...]}

Mismatched marker count, few matches, and unmatched marks are *results*,
not invitations to refit a transform. No arbitrary scene projection is inferred.
"""
from __future__ import annotations
import argparse
import json
from collections import deque
from pathlib import Path
from math import hypot

def register(p: dict, m: list[list[float]]) -> tuple[float,float]:
    return m[0][0]*p["x"]+m[0][1]*p["y"]+m[0][2], m[1][0]*p["x"]+m[1][1]*p["y"]+m[1][2]

def compare(doc: dict) -> dict:
    reg=doc["registration"]
    assert reg["frozen_before_sticker_comparison"] is True
    assert reg["provenance"] and doc["source"] and doc["orb_source"]
    matrix=reg["matrix_2x3"]
    assert len(matrix)==2 and all(len(r)==3 for r in matrix)
    tol=float(doc["tolerance"])
    assert tol > 0
    marks=doc["marks"]; orbs=doc["orbs"]
    assert all("id" in p and "x" in p and "y" in p for p in marks+orbs)
    assert len({p["id"] for p in marks})==len(marks)
    assert len({p["id"] for p in orbs})==len(orbs)
    transformed=[register(p,matrix) for p in marks]
    adjacency=[
        [j for j,o in enumerate(orbs) if hypot(x-o["x"],y-o["y"])<=tol]
        for x,y in transformed
    ]
    # Maximum *one-to-one* matching, not arbitrary reuse of an orb.
    assigned={}
    def augment(i, seen):
        for j in adjacency[i]:
            if j in seen: continue
            seen.add(j)
            if j not in assigned or augment(assigned[j],seen):
                assigned[j]=i
                return True
        return False
    for i in range(len(marks)):
        augment(i,set())
    matched_marks=set(assigned.values())
    pairs=[{"mark":marks[i]["id"],"orb":orbs[j]["id"],
            "distance":round(hypot(transformed[i][0]-orbs[j]["x"],
                                   transformed[i][1]-orbs[j]["y"]),6)}
           for j,i in sorted(assigned.items())]
    return {"marks":len(marks),"orbs":len(orbs),"matches":len(assigned),
            "unmatched_marks":[p["id"] for i,p in enumerate(marks) if i not in matched_marks],
            "unmatched_orbs":[p["id"] for j,p in enumerate(orbs) if j not in assigned],
            "matched_pairs":pairs,"tolerance":tol,
            "meaning":"Only a frozen source-derived transform was tested. Unmatched marks have not been established to be intentional puzzle residue."}

def self_test():
    base={"source":"synthetic marks","orb_source":"synthetic orbs",
          "registration":{"matrix_2x3":[[1,0,0],[0,1,0]],"provenance":"synthetic identity","frozen_before_sticker_comparison":True},
          "tolerance":0.1,"marks":[{"id":"m1","x":0,"y":0},{"id":"m2","x":0.01,"y":0},
                                   {"id":"m3","x":4,"y":4}],
          "orbs":[{"id":"o1","x":0,"y":0},{"id":"o2","x":5,"y":5}]}
    got=compare(base)
    assert got["matches"]==1 and len(got["unmatched_marks"])==2
    base["marks"][2]["x"]=5; base["marks"][2]["y"]=5
    got=compare(base)
    assert got["matches"]==2 and len(got["unmatched_marks"])==1
    bad=dict(base)
    bad["registration"]=dict(base["registration"],frozen_before_sticker_comparison=False)
    try: compare(bad)
    except AssertionError: pass
    else: raise AssertionError("Unfrozen transform accepted")
    print("PASS: unique-orb matching, leftover marks, and frozen registration enforcement")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path,nargs="?")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test: self_test(); return
    if args.input is None: p.error("provide input JSON or --self-test")
    print(json.dumps(compare(json.loads(args.input.read_text(encoding="utf-8"))),indent=2))
if __name__=="__main__": main()

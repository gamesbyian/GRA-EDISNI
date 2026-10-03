#!/usr/bin/env python3
"""Experiment 386: compare 534brn and one-shot objects as ternary coordinate relations."""

from itertools import permutations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-386-534brn-coordinate-role-isomorphism.json"

SOURCE = (
    (1,0,1),
    (2,1,1),
    (0,2,2),
)

ONE_SHOT = (
    ("102","002","120"),
    ("102","012","100"),
    ("102","022","100"),
    ("112","012","100"),
    ("112","012","120"),
    ("122","022","100"),
)

AXES=("physical_row_r","physical_col_c","keypad_row_k")

def target_grid(words):
    return tuple(tuple(int(ch) for ch in row) for row in words)

def q_relabel(g,a,u):
    return tuple(g[(a*q+u)%3] for q in range(3))

def relation_grid(triples):
    g=[[None]*3 for _ in range(3)]
    for x,y,z in triples:
        if g[x][y] is not None and g[x][y] != z:
            return None
        g[x][y]=z
    if any(v is None for row in g for v in row):
        return None
    return tuple(tuple(row) for row in g)

def fmt(g):
    return "/".join("".join(map(str,row)) for row in g)

def main():
    external=[(r,c,SOURCE[r][c]) for r in range(3) for c in range(3)]
    targets=[target_grid(x) for x in ONE_SHOT]

    records=[]
    hits=[]
    for perm in permutations(range(3)):
        role=tuple(AXES[i] for i in perm)
        triples=[tuple(t[i] for i in perm) for t in external]
        g=relation_grid(triples)
        rec={
            "role_assignment":{
                "target_Q":role[0],
                "target_c":role[1],
                "target_value_r":role[2],
            },
            "forms_total_3x3_function":g is not None,
            "grid":fmt(g) if g is not None else None,
            "hits":[],
        }
        if g is not None:
            for idx,target in enumerate(targets):
                for a in (1,2):
                    for u in range(3):
                        transformed=q_relabel(target,a,u)
                        if transformed==g:
                            hit={
                                "canonical_target":"/".join(ONE_SHOT[idx]),
                                "q_map":f"q'={a}q+{u} mod 3",
                            }
                            rec["hits"].append(hit)
                            hits.append({
                                "role_assignment":rec["role_assignment"],
                                "grid":rec["grid"],
                                **hit,
                            })
        records.append(rec)

    assert sum(r["forms_total_3x3_function"] for r in records)==2
    assert len(hits)==1
    assert hits[0]=={
        "role_assignment":{
            "target_Q":"physical_col_c",
            "target_c":"physical_row_r",
            "target_value_r":"keypad_row_k",
        },
        "grid":"120/012/112",
        "canonical_target":"112/012/120",
        "q_map":"q'=2q+2 mod 3",
    }

    result={
        "experiment":386,
        "external_relation":"nine triples (physical row r, physical column c, DTMF keypad row k)",
        "target_relation":"one-shot surface as nine triples (Q, physical column c, minority-row value r)",
        "coordinate_role_permutations_tested":6,
        "records":records,
        "summary":{
            "role_permutations_forming_total_3x3_functions":2,
            "role_gauge_hits":1,
            "unique_hit":hits[0],
        },
        "interpretation":(
            "Treating both artifacts as ternary coordinate relations gives a bounded six-way role-permutation family "
            "rather than an unconstrained image transform family. Four role permutations cannot even form a total 3x3 "
            "function because the keypad-row coordinate is not bijective enough to serve as a target input axis. Of the "
            "two valid functions, the direct r,c->k surface has no one-shot hit under the six preregistered q maps. The "
            "swapped-axis c,r->k surface is the strict transpose 120/012/112 and has exactly one hit: canonical "
            "112/012/120 under q'=2q+2. This makes the candidate a unique isomorphism inside the smallest coordinate-role "
            "family, while still not supplying an authorial cue for choosing that role assignment."
        ),
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

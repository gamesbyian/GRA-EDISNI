#!/usr/bin/env python3
"""Experiment 387: gauge-robustness audit for the 534brn coordinate isomorphism."""

from itertools import permutations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-387-534brn-gauge-robustness.json"

DIRECT = (
    (1,0,1),
    (2,1,1),
    (0,2,2),
)
TRANSPOSED = (
    (1,2,0),
    (0,1,2),
    (1,1,2),
)
ONE_SHOT_WORDS = (
    ("102","002","120"),
    ("102","012","100"),
    ("102","022","100"),
    ("112","012","100"),
    ("112","012","120"),
    ("122","022","100"),
)
PERMS = tuple(permutations(range(3)))

def grid(words):
    return tuple(tuple(int(ch) for ch in row) for row in words)

def q_relabel(g, a, u):
    return tuple(g[(a*q+u)%3] for q in range(3))

def global_value_relabel(g, p):
    return tuple(tuple(p[v] for v in row) for row in g)

def per_column_relabel(g, ps):
    return tuple(
        tuple(ps[c][v] for c,v in enumerate(row))
        for row in g
    )

def label(words):
    return "/".join(words)

def audit(source, per_column=False):
    hits=[]
    for words in ONE_SHOT_WORDS:
        base=grid(words)
        for a in (1,2):
            for u in range(3):
                qg=q_relabel(base,a,u)
                if per_column:
                    for ps in product(PERMS, repeat=3):
                        if per_column_relabel(qg,ps)==source:
                            hits.append({
                                "state":label(words),
                                "q_map":f"q'={a}q+{u}",
                                "column_value_maps":[list(p) for p in ps],
                            })
                else:
                    for p in PERMS:
                        if global_value_relabel(qg,p)==source:
                            hits.append({
                                "state":label(words),
                                "q_map":f"q'={a}q+{u}",
                                "global_value_map":list(p),
                            })
    return hits

def main():
    direct_global=audit(DIRECT,False)
    trans_global=audit(TRANSPOSED,False)
    direct_local=audit(DIRECT,True)
    trans_local=audit(TRANSPOSED,True)

    assert direct_global == []
    assert direct_local == []
    assert trans_global == [{
        "state":"112/012/120",
        "q_map":"q'=2q+2",
        "global_value_map":[0,1,2],
    }]
    assert len(trans_local)==4
    assert {h["state"] for h in trans_local} == {
        "102/002/120",
        "112/012/100",
        "112/012/120",
        "122/022/100",
    }
    assert {h["q_map"] for h in trans_local} == {"q'=2q+2"}
    assert all(h["column_value_maps"][0]==[0,1,2] for h in trans_local)
    assert all(h["column_value_maps"][2]==[0,1,2] for h in trans_local)

    result={
        "experiment":387,
        "question":"Does the 534brn coordinate hit survive the POS3 row-label gauges identified in Experiment 352?",
        "shared_global_row_label_gauge":{
            "family_size":6,
            "direct_role_hits":direct_global,
            "transposed_role_hits":trans_global,
            "result":"Exactly one hit survives, and it uses the identity row-value labeling."
        },
        "independent_per_column_row_label_gauge":{
            "family_size":216,
            "direct_role_hits":len(direct_local),
            "transposed_role_hits":len(trans_local),
            "hit_states":[h["state"] for h in trans_local],
            "all_hits_require_q_map":"q'=2q+2",
            "outer_columns_require_identity_value_map":true,
            "note":"The four hits differ only by relabeling the middle output column, exactly where the Experiment-374 one-shot family carries all six-state variation."
        },
        "interpretation":(
            "The source-axis swap and q reversal are robust: the direct role assignment never hits even if every output "
            "column receives its own arbitrary ternary row-label permutation, and every transposed hit still requires "
            "q'=2q+2. The exact state 112/012/120 is unique when the three physical columns share one global physical-row "
            "coordinate, as expected for a literal 3x3 grid. If independent per-column value gauges are admitted, four "
            "one-shot states become equivalent because all one-shot uncertainty lives in the middle column. Thus the "
            "external artifact strongly fixes the role assignment and q registration; its discrimination among the four "
            "middle-column variants depends on treating physical row as one shared coordinate rather than three unrelated "
            "column-local labels."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

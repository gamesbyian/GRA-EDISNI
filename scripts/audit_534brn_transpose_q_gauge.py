#!/usr/bin/env python3
"""Experiment 385: decompose the 534brn quarter-turn into historical transpose + preregistered q relabeling."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-385-534brn-transpose-q-gauge.json"

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

def grid_from_words(words):
    return tuple(tuple(int(x) for x in row) for row in words)

def words(g):
    return tuple("".join(map(str,row)) for row in g)

def transpose(g):
    return tuple(tuple(g[r][c] for r in range(3)) for c in range(3))

def q_relabel(g, a, u):
    # Experiment 266 maximum-retention family:
    # internal q' = a*q + u mod 3, a in {1,2}, u in {0,1,2}.
    # Output row at external q therefore comes from canonical internal row q'.
    return tuple(g[(a*q+u)%3] for q in range(3))

def main():
    targets=[grid_from_words(x) for x in ONE_SHOT]
    transposed=transpose(SOURCE)

    direct_hits=[]
    transpose_hits=[]

    for idx,target in enumerate(targets):
        for a in (1,2):
            for u in range(3):
                transformed=q_relabel(target,a,u)
                rec={
                    "target":"/".join(ONE_SHOT[idx]),
                    "q_map":f"q'={a}q+{u} mod 3",
                    "rows":"/".join(words(transformed)),
                }
                if transformed==SOURCE:
                    direct_hits.append(rec)
                if transformed==transposed:
                    transpose_hits.append(rec)

    assert direct_hits == []
    assert transpose_hits == [{
        "target":"112/012/120",
        "q_map":"q'=2q+2 mod 3",
        "rows":"120/012/112",
    }]

    result={
        "experiment":385,
        "source_keypad_row_grid":["101","211","022"],
        "historically_proposed_operation":"transpose the sticker/grid structure in relation to 534brn",
        "transposed_source_grid":["120","012","112"],
        "preregistered_q_family":{
            "source":"Experiment 266, reconciled in Experiment 355",
            "maps":["q'=q","q'=q+1","q'=q+2","q'=2q","q'=2q+1","q'=2q+2"],
            "property":"all six are maximum-retention first-pass affine consumers with d'=S exactly"
        },
        "direct_source_hits_under_q_family":direct_hits,
        "transpose_hits_under_q_family":transpose_hits,
        "decomposition":{
            "previous_description":"90-degree CCW rotation of 101/211/022",
            "equivalent_description":"transpose 101/211/022 -> 120/012/112, then compare in q'=2q+2 gauge",
            "identity":"rot90_ccw = q-row reversal after transpose"
        },
        "interpretation":(
            "The last apparent geometric free parameter can be decomposed into two independently pre-existing pieces: "
            "a transpose operation explicitly proposed in Nov 2025 around the sticker/534brn relation, and one member "
            "of the six q relabelings already tied for maximum first-pass retention in Experiment 266 before the external "
            "match was known. No direct, untransposed source grid matches any one-shot state under those q relabelings; "
            "the transposed grid matches exactly one state/gauge pair, 112/012/120 with q'=2q+2. This removes the need "
            "to posit an otherwise free CCW rotation, but the selected q gauge is still fixed by the external match rather "
            "than an authorial cue, so the result remains a strong candidate rather than a solved decoder."
        )
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

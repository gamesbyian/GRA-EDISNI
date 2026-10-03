#!/usr/bin/env python3
"""Experiment 373: native coordinate typing of the 9+3 class carrier."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-373-native-coordinate-typing.json"

SERIAL_ORDER = "ABCDEFGHI"

def coord(residue):
    z = residue - 1
    Q = z // 27
    d = (z % 27) // 9
    j = z % 9
    return Q, d, j

def main():
    # The first 108 residues form 4 quarter layers, each 3 depths x 9 classes.
    grid = {r: coord(r) for r in range(1, 109)}

    primary = [r for r in range(1, 82)]
    tail = [r for r in range(82, 109)]

    assert {grid[r][0] for r in primary} == {0,1,2}
    assert {grid[r][0] for r in tail} == {3}
    assert {grid[r][1] for r in tail} == {0,1,2}
    assert {grid[r][2] for r in tail} == set(range(9))

    # For each A-I class j, the 12-position class word has 9 primary cells
    # ordered as (Q,d) = 00,01,02,10,11,12,20,21,22, followed by tail d=0,1,2.
    class_words = {}
    for j, letter in enumerate(SERIAL_ORDER):
        residues = [1 + j + 9*k for k in range(12)]
        coords = [grid[r] for r in residues]
        class_words[letter] = {
            "residues": residues,
            "primary_Qd": [[Q,d] for Q,d,_j in coords[:9]],
            "tail_Qd": [[Q,d] for Q,d,_j in coords[9:]],
        }
        assert [tuple(x) for x in class_words[letter]["primary_Qd"]] == [
            (0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)
        ]
        assert [tuple(x) for x in class_words[letter]["tail_Qd"]] == [
            (3,0),(3,1),(3,2)
        ]

    # A one-slash tail at one of the three final positions therefore encodes
    # a native d-coordinate. Reusing it type-preservingly against the 3x3
    # primary (Q,d) body selects a d-column and preserves Q.
    result = {
        "experiment": 373,
        "native_address": "r-1 = 27*Q + 9*d + j",
        "primary_domain": {"Q":[0,1,2],"d":[0,1,2],"j":[0,1,2,3,4,5,6,7,8]},
        "tail_domain": {"Q":[3],"d":[0,1,2],"j":[0,1,2,3,4,5,6,7,8]},
        "class_word_layout": {
            "primary_9_positions": ["Q0d0","Q0d1","Q0d2","Q1d0","Q1d1","Q1d2","Q2d0","Q2d1","Q2d2"],
            "tail_3_positions": ["Q3d0","Q3d1","Q3d2"]
        },
        "selector_type": "d",
        "type_preserving_selector_on_primary": "(Q,d,j) -> (Q,S(j),j)",
        "experiment_318_relation": {
            "column_rail": "type-preserving d selection; exactly the G5 physical axis",
            "row_chunk": "cross-axis reinterpretation of the tail d-position as Q"
        },
        "g5_effect": (
            "Given the independently supported one-slash tail/index architecture, the selector's "
            "position is natively a d-coordinate. If that selector is applied to the preceding 3x3 "
            "(Q,d) body while preserving coordinate type and class registration j, d=S(j) is uniquely "
            "identified without consulting first-pass outputs."
        ),
        "g6_effect": (
            "A second use of S(j) to consume Q crosses coordinate types: S is physically a d-position, "
            "whereas Q labels the three primary quarter layers. Native coordinate typing therefore "
            "supports the first G5 depth selection but does not support G6 q-consumption."
        ),
        "class_words": class_words
    }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

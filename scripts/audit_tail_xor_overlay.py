#!/usr/bin/env python3
"""Experiment 419: repeat the 27-cell tail over the 81-cell body and XOR.

Community-proposed operation, frozen before inspection of completed outputs:

* arrange H108 in canonical 12x9 serial rows;
* encode body slash=0, dash=1;
* encode tail slash=0, dot=1;
* repeat tail rows 10-12 over body rows 1-9 by row modulo 3;
* XOR cellwise, yielding a 9x9 binary surface.

The operation is evaluated over the live U2/U3/U4/U5 ensembles.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-419-tail-xor-overlay.json"


def xor_surface(master: str) -> tuple[str, ...]:
    rows = []
    for r in range(9):
        bits = []
        for c in range(9):
            body = 1 if master[r * 9 + c] == "-" else 0
            tail = 1 if master[(9 + (r % 3)) * 9 + c] == "." else 0
            bits.append(str(body ^ tail))
        rows.append("".join(bits))
    return tuple(rows)


def common_stats(masters):
    surfaces = [xor_surface(m) for m in masters]
    keys = ["".join(s) for s in surfaces]
    invariant = 0
    for i in range(81):
        if len({k[i] for k in keys}) == 1:
            invariant += 1
    weights = [k.count("1") for k in keys]
    return {
        "candidate_count": len(masters),
        "distinct_xor_surfaces": len(set(keys)),
        "invariant_cells": invariant,
        "variable_cells": 81 - invariant,
        "_weights": weights,
        "_surfaces": surfaces,
    }


def observed_only_stats():
    with OBS.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    obs = {int(row["residue"]): row["symbol"] for row in rows}

    known = ones = 0
    for r in range(9):
        for c in range(9):
            body_residue = 1 + r * 9 + c
            tail_residue = 82 + (r % 3) * 9 + c
            if body_residue not in obs or tail_residue not in obs:
                continue
            body = 1 if obs[body_residue] == "-" else 0
            tail = 1 if obs[tail_residue] == "." else 0
            known += 1
            ones += body ^ tail

    return {
        "known_cells": known,
        "unknown_cells": 81 - known,
        "known_ones": ones,
        "known_zeros": known - ones,
    }


def block_weights(surface):
    return [
        sum(row.count("1") for row in surface[q * 3:(q + 1) * 3])
        for q in range(3)
    ]


def main():
    _summary, u2_rows, _unknown = build()
    u2 = [m for *_prefix, m in u2_rows]
    u3, u4, u5 = machine_layers()

    s2 = common_stats(u2)
    s3 = common_stats(u3)
    s4 = common_stats(u4)
    s5 = common_stats(u5)

    assert len(set(s2["_weights"])) == 12
    assert min(s2["_weights"]) == 28 and max(s2["_weights"]) == 39
    assert sorted(set(s3["_weights"])) == [28, 30, 32, 34, 36, 38]
    assert set(s4["_weights"]) == {36}
    assert set(s5["_weights"]) == {36}
    assert {tuple(block_weights(s)) for s in s4["_surfaces"]} == {(9, 12, 15)}
    assert {tuple(block_weights(s)) for s in s5["_surfaces"]} == {(9, 12, 15)}

    result = {
        "experiment": 419,
        "operation": {
            "layout": "12x9 serial rows",
            "body_rows": "1-9",
            "tail_rows": "10-12 repeated three times over body",
            "body_encoding": {"/": 0, "-": 1},
            "tail_encoding": {"/": 0, ".": 1},
            "combine": "XOR",
            "output": "9x9 binary surface",
        },
        "observed_only_surface": observed_only_stats(),
        "ensembles": {
            "U2": {
                "candidate_count": s2["candidate_count"],
                "distinct_xor_surfaces": s2["distinct_xor_surfaces"],
                "invariant_cells": s2["invariant_cells"],
                "variable_cells": s2["variable_cells"],
                "total_weight_range": [min(s2["_weights"]), max(s2["_weights"])],
            },
            "U3": {
                "candidate_count": s3["candidate_count"],
                "distinct_xor_surfaces": s3["distinct_xor_surfaces"],
                "invariant_cells": s3["invariant_cells"],
                "variable_cells": s3["variable_cells"],
                "total_weight_values": sorted(set(s3["_weights"])),
            },
            "U4": {
                "candidate_count": s4["candidate_count"],
                "distinct_xor_surfaces": s4["distinct_xor_surfaces"],
                "invariant_cells": s4["invariant_cells"],
                "variable_cells": s4["variable_cells"],
                "total_weight": 36,
                "q_block_weights": [9, 12, 15],
            },
            "U5": {
                "candidate_count": s5["candidate_count"],
                "distinct_xor_surfaces": s5["distinct_xor_surfaces"],
                "invariant_cells": s5["invariant_cells"],
                "variable_cells": s5["variable_cells"],
                "total_weight": 36,
                "q_block_weights": [9, 12, 15],
            },
        },
        "candidate_reduction": "none",
        "interpretation": (
            "The XOR overlay is a deterministic and visually useful tail-on-body representation. "
            "It does not collapse the candidate family. The clean U4/U5 9/12/15 block-weight "
            "staircase is exact but is algebraically implied by the existing exact-POS3 plus "
            "G5-validity assumptions, so it is not independent evidence for them."
        ),
        "four_by_27_note": (
            "4x27 is a natural direct geometry for the 81+27 split. The fourth row is binary "
            "slash/dot only, so literal printed-symbol Morse lacks a third separator/mark type "
            "and requires an independently specified binary timing convention before a Morse "
            "decode is licensed."
        ),
    }

    assert result["observed_only_surface"] == {
        "known_cells": 24,
        "unknown_cells": 57,
        "known_ones": 9,
        "known_zeros": 15,
    }
    assert [result["ensembles"][x]["candidate_count"] for x in ("U2","U3","U4","U5")] == [324,108,12,10]
    assert [result["ensembles"][x]["distinct_xor_surfaces"] for x in ("U2","U3","U4","U5")] == [324,108,12,10]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

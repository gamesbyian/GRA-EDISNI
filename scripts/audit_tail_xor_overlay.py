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

import json
from collections import Counter
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers

ROOT = Path(__file__).resolve().parents[1]
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


def summarize(masters):
    surfaces = [xor_surface(m) for m in masters]
    keys = ["".join(s) for s in surfaces]
    invariant = []
    for i in range(81):
        values = {k[i] for k in keys}
        if len(values) == 1:
            invariant.append({
                "row": i // 9 + 1,
                "column": i % 9 + 1,
                "value": next(iter(values)),
            })

    total_weights = Counter(k.count("1") for k in keys)
    q_block_weights = Counter(
        tuple(sum(row.count("1") for row in surface[q * 3:(q + 1) * 3]) for q in range(3))
        for surface in surfaces
    )

    return {
        "candidate_count": len(masters),
        "distinct_xor_surfaces": len(set(keys)),
        "invariant_cells": len(invariant),
        "variable_cells": 81 - len(invariant),
        "total_weight_histogram": dict(sorted(total_weights.items())),
        "q_block_weight_histogram": {
            "/".join(map(str, key)): value
            for key, value in sorted(q_block_weights.items())
        },
    }


def main():
    _summary, u2_rows, _unknown = build()
    u2 = [m for *_prefix, m in u2_rows]
    u3, u4, u5 = machine_layers()

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
        "ensembles": {
            "U2": summarize(u2),
            "U3": summarize(u3),
            "U4": summarize(u4),
            "U5": summarize(u5),
        },
        "interpretation": {
            "candidate_reduction": "none: every live master has a distinct XOR surface",
            "strongest_structure": "U4 and U5 all have total XOR weight 36 and q-block weights 9/12/15",
            "why_9_12_15_occurs": (
                "Under exact POS3 polarity the three 27-cell q blocks contain 15,12,9 body dashes. "
                "A G5-valid selector surface has exactly 3 selected dashes in each q block. "
                "XOR flips the 18 non-selected cells, giving 24-Tq = 9,12,15 output ones."
            ),
            "epistemic_status": (
                "Useful deterministic visualization / equivalent structural readout, "
                "not independent support for G5 because the clean 9/12/15 staircase is algebraically implied by G5 validity."
            ),
        },
        "four_by_27_note": (
            "4x27 is a natural direct geometry because rows 1-3 are the 81-cell slash/dash body and row 4 is the "
            "27-cell slash/dot tail. Literal printed-symbol Morse is not directly available on the fourth row because "
            "it contains only slash and dot; a Morse interpretation would need an independently licensed binary timing or separator convention."
        ),
    }

    assert [result["ensembles"][x]["candidate_count"] for x in ("U2","U3","U4","U5")] == [324,108,12,10]
    assert [result["ensembles"][x]["distinct_xor_surfaces"] for x in ("U2","U3","U4","U5")] == [324,108,12,10]
    assert result["ensembles"]["U4"]["total_weight_histogram"] == {36: 12}
    assert result["ensembles"]["U5"]["total_weight_histogram"] == {36: 10}
    assert result["ensembles"]["U4"]["q_block_weight_histogram"] == {"9/12/15": 12}
    assert result["ensembles"]["U5"]["q_block_weight_histogram"] == {"9/12/15": 10}

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

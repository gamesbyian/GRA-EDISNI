#!/usr/bin/env python3
"""Experiment 425: provenance of the number 23 in Experiment 419's U4 XOR surface."""

from __future__ import annotations

import json
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-425-xor-23-provenance.json"


def xor_surface(master: str) -> str:
    bits = []
    for r in range(9):
        for c in range(9):
            body = 1 if master[r * 9 + c] == "-" else 0
            tail = 1 if master[(9 + (r % 3)) * 9 + c] == "." else 0
            bits.append(str(body ^ tail))
    return "".join(bits)


def variable_residues(masters: list[str]) -> list[int]:
    return [
        r for r in range(1, 109)
        if len({m[r - 1] for m in masters}) > 1
    ]


def influence_cells(residue: int) -> list[tuple[int, int]]:
    if residue <= 81:
        i = residue - 1
        return [(i // 9, i % 9)]
    i = residue - 82
    tail_row, col = divmod(i, 9)
    return [(r, col) for r in range(tail_row, 9, 3)]


def layer_result(name: str, masters: list[str]) -> dict:
    vars_ = variable_residues(masters)
    body = [r for r in vars_ if r <= 81]
    tail = [r for r in vars_ if r >= 82]

    owners: dict[tuple[int, int], list[int]] = {}
    for residue in vars_:
        for cell in influence_cells(residue):
            owners.setdefault(cell, []).append(residue)

    overlap_cells = {
        f"{r + 1},{c + 1}": residues
        for (r, c), residues in sorted(owners.items())
        if len(residues) > 1
    }

    surfaces = [xor_surface(m) for m in masters]
    actual_variable_cells = sum(
        len({surface[i] for surface in surfaces}) > 1
        for i in range(81)
    )

    raw_influence_count = len(body) + 3 * len(tail)
    union_count = len(owners)

    assert union_count == actual_variable_cells
    assert raw_influence_count - union_count == sum(len(v) - 1 for v in overlap_cells.values())

    return {
        "candidate_count": len(masters),
        "variable_master_residues": vars_,
        "variable_body_residues": body,
        "variable_tail_residues": tail,
        "body_variable_count": len(body),
        "tail_variable_count": len(tail),
        "raw_xor_influence_count": raw_influence_count,
        "overlap_cell_count": len(overlap_cells),
        "overlap_cells_1_based": overlap_cells,
        "xor_variable_cell_count": union_count,
        "formula": f"{len(body)} + 3*{len(tail)} - {raw_influence_count - union_count} = {union_count}",
    }


def main() -> None:
    _summary, u2_rows, _unknown = build()
    u2 = [m for *_prefix, m in u2_rows]
    u3, u4, u5 = machine_layers()

    layers = {
        "U2": layer_result("U2", u2),
        "U3": layer_result("U3", u3),
        "U4": layer_result("U4", u4),
        "U5": layer_result("U5", u5),
    }

    assert layers["U2"]["xor_variable_cell_count"] == 29
    assert layers["U3"]["xor_variable_cell_count"] == 26
    assert layers["U4"]["xor_variable_cell_count"] == 23
    assert layers["U5"]["xor_variable_cell_count"] == 21
    assert layers["U4"]["formula"] == "5 + 3*7 - 3 = 23"
    assert layers["U4"]["overlap_cells_1_based"] == {
        "3,7": [25, 106],
        "7,1": [55, 82],
        "7,7": [61, 88],
    }

    result = {
        "experiment": 425,
        "question": "Why does Experiment 419 U4 have exactly 23 variable XOR cells?",
        "layers": layers,
        "u4_decomposition": {
            "body_variables": [22, 25, 55, 58, 61],
            "tail_variables": [82, 84, 88, 91, 100, 102, 106],
            "raw_supports": "5 body variables affect one XOR cell each; 7 tail variables affect three repeated cells each",
            "overlaps": {
                "body25_tail106": "XOR cell row 3, col 7",
                "body55_tail82": "XOR cell row 7, col 1",
                "body61_tail88": "XOR cell row 7, col 7",
            },
            "identity": "5 + (7*3) - 3 = 23",
        },
        "interpretation": (
            "The U4 value 23 is exact but not an additional machine invariant. "
            "It is the union size of the XOR influence supports of the particular "
            "residues still variable at U4. The neighboring layers yield 29, 26, 23, "
            "and 21 variable XOR cells, showing that 23 changes as completion constraints "
            "fix residues. The three support overlaps are consequences of the canonical "
            "body/tail registration and the identities of the surviving variable residues; "
            "there is no separate rule selecting 23."
        ),
        "relation_to_hollerith_23": (
            "Experiment 424's 12+8+3=23 and Experiment 419's U4 variable-cell count "
            "are mathematically independent constructions. Their numerical equality is "
            "therefore a genuine cross-experiment coincidence, but Experiment 425 finds "
            "no mechanical bridge between them."
        ),
    }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Observation-only replay of the simplest 9+3 tail-selector meanings.

The final three slash/dot cells select one of three positions. This script
compares two historically/simple spatial meanings for that position against
only data/observations.csv:

* row/chunk: choose one consecutive 3-cell chunk from the 3x3 body;
* column/rail: choose one physical column from the same 3x3 body.

Unknown observations remain '?'. No machine-spec, predicted cells, POS3,
recursive survival, route criteria, or terminal object is consulted.
"""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
CLASSES = "ABCDEFGHI"


def load_symbols() -> dict[int, str]:
    by_residue: dict[int, set[str]] = {}
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            by_residue.setdefault(int(row["residue"]), set()).add(row["symbol"])
    out = {}
    for residue, symbols in by_residue.items():
        if len(symbols) != 1:
            raise AssertionError(f"conflicting observations at {residue}: {symbols}")
        out[residue] = next(iter(symbols))
    return out


def compatible_slash_positions(tail: str) -> list[int]:
    out = []
    for pos in range(3):
        candidate = ["."] * 3
        candidate[pos] = "/"
        if all(obs == "?" or obs == cand for obs, cand in zip(tail, candidate)):
            out.append(pos)
    return out


def select(body: str, pos: int, mode: str) -> str:
    if mode == "row":
        return body[pos * 3 : pos * 3 + 3]
    if mode == "column":
        return "".join(body[pos + 3 * r] for r in range(3))
    raise ValueError(mode)


def residue_for(cls_index: int, body_index: int) -> int:
    return cls_index + 1 + 9 * body_index


def main() -> None:
    obs = load_symbols()
    classes = {}
    for ci, cls in enumerate(CLASSES):
        word = "".join(obs.get(ci + 1 + 9 * k, "?") for k in range(12))
        body, tail = word[:9], word[9:]
        positions = compatible_slash_positions(tail)
        if not positions:
            raise AssertionError(f"{cls}: no one-slash tail completion")
        classes[cls] = {"body": body, "tail": tail, "positions": positions}

    completions = list(itertools.product(*(classes[c]["positions"] for c in CLASSES)))
    assert len(completions) == 36

    modes = {}
    for mode in ("row", "column"):
        known_counts = []
        possible_outputs = {}
        for cls in CLASSES:
            body = classes[cls]["body"]
            possible_outputs[cls] = sorted(
                {select(body, p, mode) for p in classes[cls]["positions"]}
            )
        for completion in completions:
            words = [
                select(classes[c]["body"], p, mode)
                for c, p in zip(CLASSES, completion)
            ]
            known_counts.append(sum(ch != "?" for word in words for ch in word))
        modes[mode] = {
            "possible_outputs": possible_outputs,
            "known_selected_cells_range": [min(known_counts), max(known_counts)],
        }

    forced = {
        c: classes[c]["positions"][0]
        for c in CLASSES
        if len(classes[c]["positions"]) == 1
    }
    assert forced == {"B": 2, "E": 0, "F": 1, "H": 2, "I": 2}
    assert modes["row"]["known_selected_cells_range"] == [18, 22]
    assert modes["column"]["known_selected_cells_range"] == [18, 21]

    forced_discriminators = {}
    for cls, pos in forced.items():
        ci = CLASSES.index(cls)
        row_idx = list(range(pos * 3, pos * 3 + 3))
        col_idx = [pos + 3 * r for r in range(3)]
        row_res = [residue_for(ci, i) for i in row_idx]
        col_res = [residue_for(ci, i) for i in col_idx]
        forced_discriminators[cls] = {
            "tail_position": pos,
            "row_output": select(classes[cls]["body"], pos, "row"),
            "column_output": select(classes[cls]["body"], pos, "column"),
            "row_residues": row_res,
            "column_residues": col_res,
            "differing_support_residues": sorted(set(row_res) ^ set(col_res)),
        }

    print(json.dumps({
        "source": "data/observations.csv",
        "model_derived_inputs_used": False,
        "tail_completion_count": len(completions),
        "forced_tail_positions": forced,
        "modes": modes,
        "forced_discriminators": forced_discriminators,
    }, indent=2))


if __name__ == "__main__":
    main()

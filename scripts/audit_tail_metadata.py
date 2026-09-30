#!/usr/bin/env python3
"""Observation-only audit of the historical 9+3 tail-as-metadata idea.

Uses only data/observations.csv. It does not import machine-spec, predicted
foregrounds, POS3, route criteria, or recursive operations.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
CLASSES = "ABCDEFGHI"


def load_symbols() -> dict[int, str]:
    by_residue: dict[int, set[str]] = {}
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r = int(row["residue"])
            by_residue.setdefault(r, set()).add(row["symbol"])

    result: dict[int, str] = {}
    for residue, symbols in by_residue.items():
        if len(symbols) != 1:
            raise AssertionError(f"conflicting observations at residue {residue}: {symbols}")
        result[residue] = next(iter(symbols))
    return result


def compatible_positions(tail: str, exceptional: str) -> list[int]:
    background = "." if exceptional == "/" else "/"
    out: list[int] = []
    for pos in range(3):
        candidate = [background] * 3
        candidate[pos] = exceptional
        if all(obs == "?" or obs == cand for obs, cand in zip(tail, candidate)):
            out.append(pos)
    return out


def main() -> None:
    obs = load_symbols()
    rows = []
    one_slash_total = 1
    one_dot_total = 1

    for ci, cls in enumerate(CLASSES):
        symbols = "".join(obs.get(ci + 1 + 9 * k, "?") for k in range(12))
        body, tail = symbols[:9], symbols[9:]
        slash_positions = compatible_positions(tail, "/")
        dot_positions = compatible_positions(tail, ".")
        one_slash_total *= len(slash_positions)
        one_dot_total *= len(dot_positions)

        selected_chunks = {
            str(pos): body[pos * 3 : pos * 3 + 3] for pos in slash_positions
        }
        rows.append(
            {
                "class": cls,
                "body": body,
                "tail": tail,
                "one_slash_positions": slash_positions,
                "one_dot_positions": dot_positions,
                "one_slash_selected_body_chunks": selected_chunks,
            }
        )

    assert one_slash_total == 36, one_slash_total
    assert one_dot_total == 0, one_dot_total

    forced = {
        row["class"]: row["one_slash_positions"][0]
        for row in rows
        if len(row["one_slash_positions"]) == 1
    }
    assert forced == {"B": 2, "E": 0, "F": 1, "H": 2, "I": 2}, forced

    print(
        json.dumps(
            {
                "source": "data/observations.csv",
                "model_derived_inputs_used": False,
                "one_slash_completion_count": one_slash_total,
                "one_dot_completion_count": one_dot_total,
                "forced_one_slash_positions": forced,
                "classes": rows,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

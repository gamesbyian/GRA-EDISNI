#!/usr/bin/env python3
"""Experiment 348: observation-only census audit for historical twelve-square layout."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-348-historical-twelve-square-census.json"


def load() -> dict[int, str]:
    out: dict[int, str] = {}
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            residue = int(row["residue"])
            if residue > 81:
                continue
            symbol = row["symbol"]
            old = out.get(residue)
            if old is not None and old != symbol:
                raise AssertionError(f"conflict at residue {residue}: {old} vs {symbol}")
            out[residue] = symbol
    return out


def completion_count(slash: int, unknown: int, minority: int) -> int:
    total = 0
    for slash_total in {minority, 9 - minority}:
        needed = slash_total - slash
        if 0 <= needed <= unknown:
            total += math.comb(unknown, needed)
    return total


def main() -> None:
    obs = load()
    squares = []
    for frame in range(9):
        cells = [obs.get(frame * 9 + i + 1, "?") for i in range(9)]
        slash = cells.count("/")
        dash = cells.count("-")
        unknown = cells.count("?")
        counts = {
            str(w): completion_count(slash, unknown, w)
            for w in range(5)
        }
        squares.append({
            "square": frame + 1,
            "trace_serial_A_to_I": "".join(cells),
            "observed_slash": slash,
            "observed_dash": dash,
            "unknown": unknown,
            "compatible_completions_by_minority_count": counts,
        })

    survivors = []
    joint = {}
    for w in range(5):
        per = [s["compatible_completions_by_minority_count"][str(w)] for s in squares]
        if all(per):
            survivors.append(w)
            joint[str(w)] = math.prod(per)

    assert survivors == [3, 4], survivors
    assert joint == {"3": 12960, "4": 18000}, joint

    result = {
        "experiment": 348,
        "input": "data/observations.csv residues 1-81 only",
        "historical_representation": "nine first slash/dash rows reshaped by solved IAB/CDE/FGH background geometry",
        "tested_unordered_minorities": [0, 1, 2, 3, 4],
        "surviving_common_minority_counts": survivors,
        "joint_completion_counts": joint,
        "squares": squares,
        "interpretation": "raw observations narrow a common binary 3x3 census to 3/6 or 4/5; they do not uniquely select incumbent 3/6",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 324: observation-only 9x12 / 9x9 spatial-field audit.

Builds the foreground in both 12x9 and transposed 9x12 views from physical
observations only, then asks a deliberately cheap question: do the known
slash/dash cells in the 9x9 body show unusual orthogonal same-symbol
clustering? Unknown cells remain unknown and are never filled.

The permutation null holds the known-cell mask and slash/dash census fixed.
A deterministic seed makes the exploratory Monte Carlo reproducible.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

CLASSES = "ABCDEFGHI"
PHYSICAL_FLAT = "IABCDEFGH"  # IAB / CDE / FGH


def load_observations(path: Path) -> dict[int, str]:
    values: dict[int, str] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            residue = int(row["residue"])
            symbol = row["symbol"]
            old = values.get(residue)
            if old is not None and old != symbol:
                raise ValueError(f"conflict at residue {residue}: {old!r} vs {symbol!r}")
            values[residue] = symbol
    return values


def body_grid(values: dict[int, str], order: str) -> list[list[str]]:
    class_index = {c: i for i, c in enumerate(CLASSES)}
    cols = [class_index[c] for c in order]
    rows: list[list[str]] = []
    for body_layer in range(9):
        serial_order = [
            values.get(1 + class_i + 9 * body_layer, "?")
            for class_i in range(9)
        ]
        rows.append([serial_order[c] for c in cols])
    return rows


def tail_grid(values: dict[int, str], order: str) -> list[list[str]]:
    class_index = {c: i for i, c in enumerate(CLASSES)}
    rows: list[list[str]] = []
    for c in order:
        class_i = class_index[c]
        rows.append([
            values.get(82 + class_i + 9 * tail_layer, "?")
            for tail_layer in range(3)
        ])
    return rows


def adjacency_stat(grid: list[list[str]]) -> dict[str, int]:
    known = {
        (r, c): grid[r][c]
        for r in range(9)
        for c in range(9)
        if grid[r][c] in "/-"
    }
    edges = []
    for r, c in known:
        for dr, dc in ((1, 0), (0, 1)):
            q = (r + dr, c + dc)
            if q in known:
                edges.append(((r, c), q))
    same = sum(known[a] == known[b] for a, b in edges)
    slash = sum(v == "/" for v in known.values())
    return {
        "known": len(known),
        "slash": slash,
        "dash": len(known) - slash,
        "known_known_edges": len(edges),
        "same_symbol_edges": same,
    }


def permutation_null(
    grid: list[list[str]], iterations: int, seed: int
) -> dict[str, float]:
    known = [(r, c) for r in range(9) for c in range(9) if grid[r][c] in "/-"]
    edges = []
    known_set = set(known)
    for r, c in known:
        for dr, dc in ((1, 0), (0, 1)):
            q = (r + dr, c + dc)
            if q in known_set:
                edges.append(((r, c), q))

    slash = sum(grid[r][c] == "/" for r, c in known)
    labels = ["/"] * slash + ["-"] * (len(known) - slash)
    observed = adjacency_stat(grid)["same_symbol_edges"]

    rng = random.Random(seed)
    total = 0.0
    total2 = 0.0
    ge = 0
    le = 0
    for _ in range(iterations):
        rng.shuffle(labels)
        lab = dict(zip(known, labels))
        x = sum(lab[a] == lab[b] for a, b in edges)
        total += x
        total2 += x * x
        ge += x >= observed
        le += x <= observed

    mean = total / iterations
    variance = max(0.0, total2 / iterations - mean * mean)
    sd = variance ** 0.5
    return {
        "iterations": iterations,
        "seed": seed,
        "mean_same_symbol_edges": mean,
        "sd_same_symbol_edges": sd,
        "z": (observed - mean) / sd if sd else 0.0,
        "p_high": (ge + 1) / (iterations + 1),
        "p_low": (le + 1) / (iterations + 1),
    }


def rows_as_strings(grid: list[list[str]]) -> list[str]:
    return ["".join(row) for row in grid]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--observations", default="data/observations.csv")
    ap.add_argument("--iterations", type=int, default=200_000)
    ap.add_argument("--seed", type=int, default=324)
    args = ap.parse_args()

    values = load_observations(Path(args.observations))
    out = {
        "unique_observed_residues": len(values),
        "body_observed_residues": sum(r <= 81 for r in values),
        "tail_observed_residues": sum(r > 81 for r in values),
        "layouts": {},
    }

    for name, order in (
        ("serial_A_to_I", CLASSES),
        ("physical_flat_IAB_CDE_FGH", PHYSICAL_FLAT),
    ):
        grid = body_grid(values, order)
        tail = tail_grid(values, order)
        out["layouts"][name] = {
            "column_order": order,
            "body_9x9": rows_as_strings(grid),
            "tail_9x3_by_class": rows_as_strings(tail),
            "adjacency": adjacency_stat(grid),
            "permutation_null": permutation_null(grid, args.iterations, args.seed),
        }

    # Regression anchors from the 30 Sep 2026 corpus.
    assert out["unique_observed_residues"] == 65
    assert out["body_observed_residues"] == 54
    assert out["tail_observed_residues"] == 11
    assert out["layouts"]["serial_A_to_I"]["adjacency"] == {
        "known": 54, "slash": 32, "dash": 22,
        "known_known_edges": 64, "same_symbol_edges": 30,
    }
    assert out["layouts"]["physical_flat_IAB_CDE_FGH"]["adjacency"] == {
        "known": 54, "slash": 32, "dash": 22,
        "known_known_edges": 62, "same_symbol_edges": 29,
    }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

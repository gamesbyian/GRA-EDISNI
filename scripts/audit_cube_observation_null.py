#!/usr/bin/env python3
"""Observation-only cube-depth audit; no machine completion or semantic scoring.

Reads the physical CSV and compares Q4 no-double-slash compatibility with the
exact label-exchange null conditional on observed positions and slash census.
"""
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "observations.csv"


def read_residues(path=DATA):
    by_residue = {}
    records = 0
    with open(path, newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            records += 1
            residue = int(row["residue"])
            assert 1 <= residue <= 108
            symbol = row["symbol"]
            assert symbol in {"/", "-", "."}
            if residue in by_residue:
                assert by_residue[residue] == symbol, (residue, symbol)
            by_residue[residue] = symbol
    return records, by_residue


def cube_stacks(by_residue, quarter):
    assert quarter in range(4)
    return [
        [by_residue.get(1 + 27 * quarter + 9 * depth + xy) for depth in range(3)]
        for xy in range(9)
    ]


def q4_exact_null(stacks):
    # This conditional null treats observed slash positions as exchangeable
    # over the same observed locations, preserving slash and dot counts.
    observed = [(j, d, symbol) for j, stack in enumerate(stacks)
                for d, symbol in enumerate(stack) if symbol is not None]
    assert all(s in {"/", "."} for _, _, s in observed)
    slash_count = sum(s == "/" for _, _, s in observed)
    total = 0
    compatible = 0
    exact_one = 0
    for indices in itertools.combinations(range(len(observed)), slash_count):
        chosen = set(indices)
        counts = Counter(observed[i][0] for i in chosen)
        total += 1
        if all(v <= 1 for v in counts.values()):
            compatible += 1
            # With unobserved voxels, exactly one slash per stack is feasible
            # only when each stack has an available unobserved position.
            if all(counts.get(j, 0) == 1 or len(stacks[j]) -
                   sum(s is not None for s in stacks[j]) > 0 for j in range(9)):
                exact_one += 1
    observed_consistent = all(
        sum(s == "/" for s in stack) <= 1 and
        (sum(s == "/" for s in stack) == 1 or any(s is None for s in stack))
        for stack in stacks
    )
    return {
        "observed_sites": len(observed),
        "observed_slashes": slash_count,
        "observed_dots": len(observed) - slash_count,
        "observed_exact_one_feasible": observed_consistent,
        "null_assignments": total,
        "null_no_double_slash": compatible,
        "null_exact_one_feasible": exact_one,
        "fraction_no_double_slash": compatible / total,
        "fraction_exact_one_feasible": exact_one / total,
    }


def main():
    records, residues = read_residues()
    stacks = [cube_stacks(residues, q) for q in range(4)]
    result = {
        "method": "observation-only exact conditional label-exchange null",
        "physical_records": records,
        "unique_residues": len(residues),
        "cube_depth_stacks": [
            ["".join(symbol or "?" for symbol in stack) for stack in cube]
            for cube in stacks
        ],
        "q4": q4_exact_null(stacks[3]),
        "limitations": [
            "conditional null tests only label exchangeability over currently observed sites",
            "no model-filled cells; no claim of an independent prospective holdout",
            "cube D4 rotations permute XY stacks and cannot change this statistic",
            "historical discovery and selection effects prevent interpreting the fraction as confirmatory significance",
        ],
    }
    assert result["q4"]["observed_sites"] == 12
    assert result["q4"]["null_assignments"] == 495
    assert result["q4"]["null_no_double_slash"] == 280
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

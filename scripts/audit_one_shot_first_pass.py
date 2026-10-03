#!/usr/bin/env python3
"""Experiment 374: characterize the one-shot first-pass object after typed G5."""

from collections import Counter
from pathlib import Path
import json

from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-374-one-shot-first-pass.json"

def main():
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    first = []
    for payload in payloads:
        for selector in selectors:
            words = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, Q))
                for Q in range(3)
            )
            if None not in words:
                first.append(words)

    assert len(first) == 20
    counts = Counter(first)
    assert len(counts) == 6

    families = sorted(counts)
    invariant = {}
    variable = {}
    for Q in range(3):
        for col in range(3):
            vals = sorted({words[Q][col] for words in families})
            key = f"Q{Q}c{col}"
            if len(vals) == 1:
                invariant[key] = vals[0]
            else:
                variable[key] = vals

    middle_patterns = Counter(
        "".join(words[Q][1] for Q in range(3))
        for words in first
    )

    assert invariant == {
        "Q0c0":"1","Q0c2":"2",
        "Q1c0":"0","Q1c2":"2",
        "Q2c0":"1","Q2c2":"0",
    }
    assert set(middle_patterns) == {"002","010","020","110","112","220"}

    result = {
        "experiment": 374,
        "raw_candidate_machines": len(payloads) * len(selectors),
        "typed_g5_first_pass_survivors": len(first),
        "distinct_first_pass_objects": len(counts),
        "family_counts": {
            "/".join(words): n
            for words, n in sorted(counts.items())
        },
        "cellwise_invariants": invariant,
        "cellwise_variables": variable,
        "one_shot_normal_form": [
            ["1","x","2"],
            ["0","y","2"],
            ["1","z","0"]
        ],
        "middle_column_patterns": dict(sorted(middle_patterns.items())),
        "interpretation": (
            "Stopping after the type-preserving G5 selection does not leave unstructured noise. "
            "The 20 raw-compatible machines collapse to six 3x3 ternary objects sharing six of nine "
            "cells exactly. All remaining variation is confined to the middle column, whose six observed "
            "patterns are 002,010,020,110,112,220. This is the complete closed-corpus one-shot output "
            "before any cross-axis d-to-Q coercion or second selector use."
        )
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 345: observation-only 9x12 row-permutation boundary audit."""

from __future__ import annotations

import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-345-row-permutation-boundary-audit.json"
CLASSES = "ABCDEFGHI"
ORDERS = {
    "serial_ABCDEFGHI": tuple("ABCDEFGHI"),
    "physical_flat_IABCDEFGH": tuple("IABCDEFGH"),
}

def traces():
    t = {c: ["?"] * 12 for c in CLASSES}
    with OBS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            residue = int(row["residue"])
            c = row["image_class"]
            pos = (residue - 1) // 9
            symbol = row["symbol"]
            prev = t[c][pos]
            if prev != "?" and prev != symbol:
                raise AssertionError(f"conflict at {c}[{pos}]: {prev} vs {symbol}")
            t[c][pos] = symbol
    return t

def pair_metric(t, a, b, cols):
    matches = mismatches = known = 0
    for j in cols:
        x, y = t[a][j], t[b][j]
        if x == "?" or y == "?":
            continue
        known += 1
        if x == y:
            matches += 1
        else:
            mismatches += 1
    return matches - mismatches, matches, mismatches, known

def order_metric(order, pair):
    vals = []
    for a, b in zip(order, order[1:]):
        key = tuple(sorted((a, b)))
        vals.append(pair[key])
    return {
        "net": sum(v[0] for v in vals),
        "matches": sum(v[1] for v in vals),
        "mismatches": sum(v[2] for v in vals),
        "known": sum(v[3] for v in vals),
    }

def run():
    t = traces()
    result = {
        "experiment": 345,
        "input": "data/observations.csv",
        "principle": "physical observations only; no model-filled cells",
        "score": "sum over adjacent row pairs of (known equal symbols - known unequal symbols) at aligned columns",
        "spaces": {},
    }
    for name, cols in (("body", range(9)), ("tail", range(9, 12)), ("all", range(12))):
        pair = {
            (a, b): pair_metric(t, a, b, cols)
            for a, b in itertools.combinations(CLASSES, 2)
        }
        permutations = list(itertools.permutations(CLASSES))
        metrics = [order_metric(o, pair) for o in permutations]
        nets = [m["net"] for m in metrics]
        best = max(nets)
        best_orders = [
            "".join(o) for o, m in zip(permutations, metrics) if m["net"] == best
        ]
        named = {}
        for label, order in ORDERS.items():
            m = order_metric(order, pair)
            named[label] = {
                **m,
                "fraction_permutations_with_net_at_least_this": sum(v >= m["net"] for v in nets) / len(nets),
            }
        result["spaces"][name] = {
            "permutation_count": len(permutations),
            "net_min": min(nets),
            "net_max": max(nets),
            "best_net": best,
            "best_order_count": len(best_orders),
            "best_orders": best_orders,
            "named_orders": named,
            "net_histogram": {str(k): v for k, v in sorted(Counter(nets).items())},
        }

    # Frozen regression anchors for the observed corpus.
    assert result["spaces"]["all"]["named_orders"]["serial_ABCDEFGHI"]["net"] == 0
    assert result["spaces"]["all"]["named_orders"]["physical_flat_IABCDEFGH"]["net"] == -1
    assert result["spaces"]["all"]["best_net"] == 20
    assert result["spaces"]["all"]["best_order_count"] == 2
    assert result["spaces"]["all"]["best_orders"] == [
        "ACBEIGHDF", "FDHGIEBCA"
    ]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run()

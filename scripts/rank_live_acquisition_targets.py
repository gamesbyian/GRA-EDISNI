#!/usr/bin/env python3
"""Experiment 422: rank live missing H108 residues for acquisition value."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

from audit_completion_universe_layers import machine_layers

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-422-live-acquisition-priorities.json"


def observations():
    with OBS.open(newline="", encoding="utf-8") as fh:
        return {int(r["residue"]): r["symbol"] for r in csv.DictReader(fh)}


def distribution(masters, residue):
    return Counter(master[residue - 1] for master in masters)


def normalized_number(value):
    if abs(value) < 1e-15:
        return 0
    if abs(value - round(value)) < 1e-15:
        return int(round(value))
    return value


def entropy(counts, total):
    value = -sum(
        (n / total) * math.log2(n / total)
        for n in counts.values()
        if n
    )
    return normalized_number(value)


def tv_distance(a, na, b, nb):
    symbols = set(a) | set(b)
    value = 0.5 * sum(
        abs(a.get(s, 0) / na - b.get(s, 0) / nb)
        for s in symbols
    )
    return normalized_number(value)


def serial_family(residue, ceiling=648):
    return list(range(residue, ceiling + 1, 108))


def main():
    obs = observations()
    _u3, u4, u5 = machine_layers()
    assert len(u4) == 12
    assert len(u5) == 10

    rows = []
    for residue in range(1, 109):
        if residue in obs:
            continue
        d4 = distribution(u4, residue)
        d5 = distribution(u5, residue)
        impossible = sorted(set(d4) - set(d5))
        rows.append({
            "residue": residue,
            "serial_family_1_648": serial_family(residue),
            "u4_counts": dict(sorted(d4.items())),
            "u5_counts": dict(sorted(d5.items())),
            "u4_vs_u5_tv": tv_distance(d4, len(u4), d5, len(u5)),
            "u5_entropy_bits": entropy(d5, len(u5)),
            "values_allowed_u4_but_impossible_u5": impossible,
        })

    discriminator_rank = sorted(
        rows,
        key=lambda r: (-r["u4_vs_u5_tv"], -r["u5_entropy_bits"], r["residue"]),
    )
    u5_information_rank = sorted(
        rows,
        key=lambda r: (-r["u5_entropy_bits"], -r["u4_vs_u5_tv"], r["residue"]),
    )

    result = {
        "experiment": 422,
        "live_family_sizes": {"U4": len(u4), "U5": len(u5)},
        "strongest_u4_vs_u5_discriminators": discriminator_rank,
        "strongest_u5_state_resolvers": u5_information_rank,
        "key_results": {
            "decisive_fork_residue": 82,
            "residue_82": next(r for r in rows if r["residue"] == 82),
            "balanced_u5_one_bit_residues": [
                r["residue"]
                for r in rows
                if abs(r["u5_entropy_bits"] - 1.0) < 1e-12
            ],
            "forced_tail_validation": {
                "residue": 94,
                "predicted_symbol": "/",
                "serial_family_1_648": serial_family(94),
                "note": "forced by observed 85=dot and 103=dot under one-slash-per-depth-stack",
            },
        },
        "guardrail": (
            "TV distance ranks ability to separate the current U4 and U5 ensembles; "
            "U5 entropy ranks state-resolution value conditional on U5. Neither is a "
            "calibrated probability that the model family itself is correct."
        ),
    }

    r82 = result["key_results"]["residue_82"]
    assert r82["u4_counts"] == {".": 10, "/": 2}
    assert r82["u5_counts"] == {".": 10}
    assert r82["values_allowed_u4_but_impossible_u5"] == ["/"]
    assert result["key_results"]["balanced_u5_one_bit_residues"] == [84, 102]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

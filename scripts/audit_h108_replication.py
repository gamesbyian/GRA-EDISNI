#!/usr/bin/env python3
"""Experiment 421: empirical H108 physical-replication and bounded period scan."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-421-h108-replication-audit.json"


def load_rows():
    with OBS.open(newline="", encoding="utf-8") as fh:
        return [
            {
                "serial": int(r["serial"]),
                "residue": int(r["residue"]),
                "symbol": r["symbol"],
                "image_class": r["image_class"],
            }
            for r in csv.DictReader(fh)
        ]


def score_period(rows, period):
    groups = defaultdict(list)
    for row in rows:
        residue = ((row["serial"] - 1) % period) + 1
        groups[residue].append(row)

    pair_count = 0
    agreeing_pairs = 0
    repeated_groups = 0
    conflict_groups = 0
    for group in groups.values():
        if len(group) < 2:
            continue
        repeated_groups += 1
        if len({r["symbol"] for r in group}) > 1:
            conflict_groups += 1
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                pair_count += 1
                agreeing_pairs += group[i]["symbol"] == group[j]["symbol"]

    return {
        "period": period,
        "pair_count": pair_count,
        "agreeing_pairs": agreeing_pairs,
        "agreement_rate": agreeing_pairs / pair_count if pair_count else None,
        "repeated_groups": repeated_groups,
        "conflict_groups": conflict_groups,
    }


def main():
    rows = load_rows()
    by_residue = defaultdict(list)
    for row in rows:
        by_residue[row["residue"]].append(row)

    replicated = []
    total_pairs = 0
    for residue, group in sorted(by_residue.items()):
        if len(group) < 2:
            continue
        group = sorted(group, key=lambda x: x["serial"])
        pairs = []
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                pairs.append({
                    "serial_a": a["serial"],
                    "serial_b": b["serial"],
                    "delta": b["serial"] - a["serial"],
                    "periods_apart": (b["serial"] - a["serial"]) // 108,
                    "same_symbol": a["symbol"] == b["symbol"],
                })
        total_pairs += len(pairs)
        replicated.append({
            "residue": residue,
            "observations": group,
            "symbols": sorted({r["symbol"] for r in group}),
            "pair_count": len(pairs),
            "pairs": pairs,
        })

    scan = [score_period(rows, p) for p in range(2, 217)]
    zero_conflict = sorted(
        [s for s in scan if s["pair_count"] and s["conflict_groups"] == 0],
        key=lambda s: (-s["pair_count"], s["period"]),
    )

    result = {
        "experiment": 421,
        "physical_sticker_count": len(rows),
        "unique_h108_residue_count": len(by_residue),
        "replicated_residue_count": len(replicated),
        "same_residue_pair_count": total_pairs,
        "same_residue_foreground_disagreements": sum(
            1 for g in replicated for p in g["pairs"] if not p["same_symbol"]
        ),
        "replicated_residues": replicated,
        "bounded_period_scan": {
            "range": [2, 216],
            "h108": next(s for s in scan if s["period"] == 108),
            "zero_conflict_periods_ranked_by_pair_support": zero_conflict,
            "conclusion": (
                "Within candidate periods 2..216, period 108 is the unique zero-conflict "
                "period with 20 same-class pair comparisons; the next zero-conflict period "
                "is 216 with 8 pairs."
            ),
        },
        "guardrail": (
            "This is a descriptive replication and bounded-period comparison over the current "
            "physical corpus. It is independent of the completion-machine assumptions but is not "
            "a universal proof that no larger or more complicated periodic model exists."
        ),
    }

    assert len(rows) == 84
    assert len(by_residue) == 66
    assert len(replicated) == 16
    assert total_pairs == 20
    assert result["same_residue_foreground_disagreements"] == 0
    assert zero_conflict[0]["period"] == 108
    assert zero_conflict[0]["pair_count"] == 20

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

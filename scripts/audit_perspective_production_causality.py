#!/usr/bin/env python3
"""Observation-only manufacturing/generator identifiability audit (PX-16/PX-C1).

Competes small source-visible foreground address grammars and proves that
the observed labels alone do not orient print/pack causal arrows.
No missing physical symbol is ever filled or written to the corpus.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from csv import DictReader
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data/observations.csv"
ALLOWED = {"/", "-", "."}
EXPECTATIONS = {
    "class_only": (9, 9, 372, 190),
    "class_plus_zone": (16, 12, 280, 125),
    "class_plus_quarter": (33, 16, 87, 34),
    "mod_27": (26, 14, 127, 47),
    "mod_54": (46, 10, 54, 17),
    "mod_108": (66, 0, 20, 0),
}


def read_observations(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        values = list(DictReader(fh))
    records = []
    seen = set()
    for row in values:
        s, r, mark = int(row["serial"]), int(row["residue"]), row["symbol"]
        assert s > 0 and 1 <= r <= 108 and (s - 1) % 108 + 1 == r
        assert mark in ALLOWED and s not in seen
        seen.add(s)
        actual_class = row["image_class"]
        assert actual_class in ("", *"ABCDEFGHI")
        records.append({
            "serial": s, "residue": r, "symbol": mark,
            "image_class": actual_class,
            # Type this as a *mathematical* serial slot, not a claim
            # about a physically unreadable class on an individual seal.
            "phase": (s - 1) % 9,
            "zone": "body" if r <= 81 else "tail",
            "quarter": (r - 1) // 27,
        })
    assert records and len(records) == len(seen)
    return records


def key_of(r: dict, family: str) -> str:
    if family == "class_only":
        return str(r["phase"])
    if family == "class_plus_zone":
        return f'{r["phase"]}:{r["zone"]}'
    if family == "class_plus_quarter":
        return f'{r["phase"]}:{r["quarter"]}'
    if family.startswith("mod_"):
        mod = int(family[4:])
        return str((r["serial"] - 1) % mod)
    raise ValueError(family)


def fingerprint(records: list[dict], family: str) -> dict:
    groups = defaultdict(list)
    for r in records:
        groups[key_of(r, family)].append(r)
    colliding_pairs, disagreeing_pairs, conflict_groups = 0, 0, 0
    witness = None
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda r: r["serial"])
        colliding_pairs += len(group) * (len(group) - 1) // 2
        conflicts = [(a, b) for i, a in enumerate(group)
                     for b in group[i + 1:] if a["symbol"] != b["symbol"]]
        disagreeing_pairs += len(conflicts)
        if conflicts:
            conflict_groups += 1
            if witness is None:
                a, b = conflicts[0]
                witness = {
                    "address": key, "serials": [a["serial"], b["serial"]],
                    "symbols": [a["symbol"], b["symbol"]],
                }
    return {
        "distinct_addresses": len(groups),
        "addresses_with_conflicting_marks": conflict_groups,
        "colliding_physical_pairs": colliding_pairs,
        "pairs_with_conflicting_marks": disagreeing_pairs,
        "contradicting_witness": witness,
    }


def audit(records: list[dict]) -> dict:
    by_residue = defaultdict(list)
    for row in records:
        by_residue[row["residue"]].append(row)
    matched_physical_classes = [
        r for r in records if r["image_class"]
        and r["image_class"] == "ABCDEFGHI"[r["phase"]]
    ]
    mismatched_physical_classes = [
        r["serial"] for r in records if r["image_class"]
        and r["image_class"] != "ABCDEFGHI"[r["phase"]]
    ]
    families = tuple(EXPECTATIONS)
    fingerprints = {name: fingerprint(records, name) for name in families}
    cross_cycle = [
        group for group in by_residue.values() if len(group) > 1
    ]
    return {
        "mode": "DEVELOP_observation_only_competing_generator_fingerprints",
        "corpus": {
            "physical_records": len(records),
            "unique_residues": len(by_residue),
            "unknown_residues": 108 - len(by_residue),
            "visible_background_class_matches": len(matched_physical_classes),
            "visible_background_class_mismatches": mismatched_physical_classes,
            "unreadable_background_classes": len(records)
            - len(matched_physical_classes) - len(mismatched_physical_classes),
            "repeated_residue_groups": len(cross_cycle),
            "repeated_residue_pairs": sum(
                len(g) * (len(g) - 1) // 2 for g in cross_cycle
            ),
        },
        "family_fingerprints": fingerprints,
        "interpretation": {
            "class_only": "falsified as a deterministic mark rule on observed records",
            "class_plus_zone": "falsified as a deterministic mark rule on observed records",
            "class_plus_quarter": "falsified as a deterministic mark rule on observed records",
            "mod_27": "falsified as a deterministic mark rule on observed records",
            "mod_54": "falsified as a deterministic mark rule on observed records",
            "mod_108": "consistent with all observed marks; recurrence already tested by Experiment 421",
            "preprint_vs_on_demand_vs_packout":
                "not identifiable from serial/class/mark observations: "
                "all mechanisms can instantiate the same lookup on the observed records",
        },
        "reopen_with": [
            "dated primary print artwork and separations identifying which inks/layers were generated together",
            "physical label roll/sheet imposition or printer-job source, not inferred from code geometry",
            "single-order packout evidence with explicitly verified purchase and serial-assignment relation",
            "original packout or CE game-wrap images showing when seals entered the assembly line",
        ],
    }


def self_test() -> None:
    # Independent tiny oracle: the same phase can bear both marks,
    # while unique serial addresses never conflict.
    sample = [
        {"serial": 1, "phase": 0, "zone": "body", "quarter": 0,
         "symbol": "/", "residue": 1},
        {"serial": 10, "phase": 0, "zone": "body", "quarter": 0,
         "symbol": "-", "residue": 10},
    ]
    assert fingerprint(sample, "class_only")["pairs_with_conflicting_marks"] == 1
    assert fingerprint(sample, "class_plus_zone")["pairs_with_conflicting_marks"] == 1
    assert fingerprint(sample, "class_plus_quarter")["pairs_with_conflicting_marks"] == 1
    assert fingerprint(sample, "mod_108")["pairs_with_conflicting_marks"] == 0


def check_golden(result: dict) -> None:
    c = result["corpus"]
    assert (c["physical_records"], c["unique_residues"], c["unknown_residues"]) == (84, 66, 42)
    assert (c["visible_background_class_matches"],
            c["visible_background_class_mismatches"],
            c["unreadable_background_classes"]) == (82, [], 2)
    assert (c["repeated_residue_groups"], c["repeated_residue_pairs"]) == (16, 20)
    for family, expectation in EXPECTATIONS.items():
        f = result["family_fingerprints"][family]
        got = (f["distinct_addresses"], f["addresses_with_conflicting_marks"],
               f["colliding_physical_pairs"], f["pairs_with_conflicting_marks"])
        assert got == expectation, (family, got, expectation)
    assert result["family_fingerprints"]["class_plus_quarter"]["contradicting_witness"]
    assert result["family_fingerprints"]["mod_108"]["contradicting_witness"] is None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail if the pinned physical baseline has drifted")
    parser.add_argument("--json", action="store_true", help="write full JSON to stdout")
    args = parser.parse_args()
    self_test()
    result = audit(read_observations(OBSERVATIONS))
    if args.check:
        check_golden(result)
        print("PASS PX production causal fingerprint: 84 observations, 66 residues, 20 concordant repeat pairs; deterministic short address models rejected.")
    if args.json or not args.check:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

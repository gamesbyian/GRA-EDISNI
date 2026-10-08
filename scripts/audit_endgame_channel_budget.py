#!/usr/bin/env python3
"""Destination-first sticker carrier audit (observation-only; no model completions).

Reads the canonical physical ledger and reports information bounds, duplicate
replications, URL-digit properties and the known bunker-code control. It does
not infer missing symbols or select an endgame hypothesis.

Usage: python scripts/audit_endgame_channel_budget.py [--check-2026-10-08]
       python scripts/audit_endgame_channel_budget.py --output /tmp/audit.json
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"
H108 = 108
SECTOR_BOUNDARY = 81
CE_PATH = "dat/534brn9653f9j8mmd"
BUNKER_CODE = "UURLRRRUUURLLL"
LEVER = {"/": "U", "-": "R", ".": "L"}
ALPHABETS = (set("/-"), set("/."))
FROZEN_2026_10_08 = {
    "physical_records": 84,
    "distinct_residues": 66,
    "primary_observed_residues": 54,
    "tail_observed_residues": 12,
    "missing_residues": 42,
    "repeated_residue_groups": 16,
    "replication_pairs": 20,
    "replication_disagreements": 0,
    "forward_possible_starts": [],
    "reverse_possible_starts": [],
    "path_digits": "534965398",
}


def load_observations(path: Path) -> dict[int, list[str]]:
    by_residue: dict[int, list[str]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            serial = int(row["serial"])
            residue = int(row["residue"])
            symbol = row["symbol"]
            assert serial > 0
            assert residue == (serial - 1) % H108 + 1, (serial, residue)
            assert symbol in (ALPHABETS[0] if residue <= SECTOR_BOUNDARY
                              else ALPHABETS[1]), (serial, symbol)
            by_residue[residue].append(symbol)
    return by_residue


def possible_bunker_starts(word: str, by_residue: dict[int, list[str]]) -> list[int]:
    """Check each possible cyclic start without filling an unknown sticker."""
    result = []
    for start in range(1, H108 + 1):
        admissible = True
        for i, command in enumerate(word):
            residue = (start + i - 1) % H108 + 1
            legal = {"U", "R"} if residue <= SECTOR_BOUNDARY else {"U", "L"}
            observed = by_residue.get(residue, [])
            if command not in legal or (observed and LEVER[observed[0]] != command):
                admissible = False
                break
        if admissible:
            result.append(start)
    return result


def audit(path: Path) -> dict:
    obs = load_observations(path)
    conflict_groups = {
        residue: marks for residue, marks in obs.items() if len(set(marks)) > 1
    }
    if conflict_groups:
        raise AssertionError("physical repetitions disagree: " + repr(conflict_groups))
    collisions = [marks for marks in obs.values() if len(marks) > 1]
    number_pairs = sum(len(marks) * (len(marks) - 1) // 2 for marks in collisions)
    primary = sum(residue <= SECTOR_BOUNDARY for residue in obs)
    tail = len(obs) - primary
    all_marks = Counter(mark for marks in obs.values() for mark in marks)
    digits = "".join(c for c in CE_PATH if c.isdigit())
    duplicates = sorted(c for c, n in Counter(digits).items() if n > 1)
    monochrome_image_bits = 128 * 128
    info_upper_bound_bits = H108  # only conditional on exact two-symbol sectors
    result = {
        "scope": "raw observed foreground only; no predicted symbols or external assets",
        "physical_records": sum(len(marks) for marks in obs.values()),
        "distinct_residues": len(obs),
        "primary_observed_residues": primary,
        "tail_observed_residues": tail,
        "missing_residues": H108 - len(obs),
        "missing_primary_residues": SECTOR_BOUNDARY - primary,
        "missing_tail_residues": (H108 - SECTOR_BOUNDARY) - tail,
        "repeated_residue_groups": len(collisions),
        "replication_pairs": number_pairs,
        "replication_disagreements": 0,
        "observed_symbol_counts": dict(sorted(all_marks.items())),
        "alphabet_split": {"1..81": "/-", "82..108": "/."},
        "conditional_foreground_capacity_upper_bits": info_upper_bound_bits,
        "conditional_foreground_capacity_upper_bytes": info_upper_bound_bits / 8,
        "conditional_unobserved_capacity_upper_bits": H108 - len(obs),
        "monochrome_128x128_bitmap_bits": monochrome_image_bits,
        "bitmap_to_foreground_bit_ratio": monochrome_image_bits / info_upper_bound_bits,
        "path_digits": digits,
        "path_digit_distinct_count": len(set(digits)),
        "path_digit_repeated": duplicates,
        "path_digits_missing_from_1_to_9": [
            d for d in "123456789" if d not in digits
        ],
        "lever_legend": LEVER,
        "known_bunker_code": BUNKER_CODE,
        "forward_possible_starts": possible_bunker_starts(BUNKER_CODE, obs),
        "reverse_possible_starts": possible_bunker_starts(BUNKER_CODE[::-1], obs),
        "interpretation": (
            "Eliminates direct full-code contiguous lever replay and literal "
            "nine-class permutation. Does not reject encoded/subselected lever "
            "commands, externally cued artwork or generative/lookup solutions."
        ),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=OBSERVATIONS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-2026-10-08", action="store_true",
                        help="fail if the 2026-10-08 physical ledger census changes")
    args = parser.parse_args()
    result = audit(args.input)
    if args.check_2026_10_08:
        for key, expected in FROZEN_2026_10_08.items():
            actual = result[key]
            assert actual == expected, f"{key}: expected {expected!r}, got {actual!r}"
        assert result["observed_symbol_counts"] == {"-": 28, ".": 8, "/": 48}
        assert result["path_digit_repeated"] == ["3", "5", "9"]
        assert result["path_digits_missing_from_1_to_9"] == ["1", "2", "7"]
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 482 sensitivity: direct known password with physical H108 evidence.

Relax the proposed 81/27 exclusion entirely. Count original-code placements
that agree with every *observed* sticker mark, independent of whether unknown
marks respect the two-alphabet sector model. This does not authenticate any
hypothetical out-of-sector dot.
"""
from __future__ import annotations

import csv
from collections import Counter
from itertools import permutations
from pathlib import Path
import json

from audit_lever_six_mapping_rotations import (
    BUNKER, DIRECTIONS, STICKER_SYMBOLS, PERIOD, PRIMARY_END, orientations
)

OBSERVATIONS = Path(__file__).resolve().parents[1] / "data" / "observations.csv"


def load_observations(path: Path) -> tuple[int, dict[int, str]]:
    observed: dict[int, str] = {}
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        residue = int(row["residue"])
        symbol = row["symbol"]
        assert 1 <= residue <= PERIOD and symbol in STICKER_SYMBOLS
        if residue in observed:
            assert observed[residue] == symbol, (
                f"conflicting observations at residue {residue}"
            )
        observed[residue] = symbol
    return len(rows), observed


def run(path: Path = OBSERVATIONS) -> dict:
    records, observed = load_observations(path)
    assert records == 84 and len(observed) == 66

    matches = []
    tested = 0
    for assignment in permutations(STICKER_SYMBOLS):
        mapping = dict(zip(DIRECTIONS, assignment))
        for reversed_flag, rotation, word in orientations(BUNKER):
            for start in range(1, PERIOD + 1):
                tested += 1
                expected = tuple({
                    "residue": ((start - 1 + index) % PERIOD) + 1,
                    "symbol": mapping[command],
                } for index, command in enumerate(word))

                if any(cell["residue"] in observed and
                       observed[cell["residue"]] != cell["symbol"]
                       for cell in expected):
                    continue

                exceptions = [
                    cell for cell in expected
                    if (cell["residue"] <= PRIMARY_END and cell["symbol"] == ".")
                    or (cell["residue"] > PRIMARY_END and cell["symbol"] == "-")
                ]
                matches.append({
                    "mapping": mapping,
                    "reversed": reversed_flag,
                    "rotation": rotation,
                    "start_residue": start,
                    "rotated_direction_word": word,
                    "observed_support": sum(cell["residue"] in observed
                                            for cell in expected),
                    "required_sector_exceptions": exceptions,
                    "full_14_symbol_window": "".join(
                        cell["symbol"] for cell in expected),
                })

    assert tested == 18144
    assert len(matches) == 1
    candidate = matches[0]
    assert candidate["mapping"] == {"U": ".", "R": "/", "L": "-"}
    assert candidate["reversed"] is False
    assert candidate["rotation"] == 9 and candidate["start_residue"] == 49
    assert candidate["observed_support"] == 6
    assert candidate["rotated_direction_word"] == "URLLLUURLRRRUU"
    assert candidate["required_sector_exceptions"] == [
        {"residue": r, "symbol": "."} for r in (49, 54, 55, 61, 62)
    ]

    return {
        "experiment": 482,
        "mode": "conditional anomaly sensitivity with confirmed observations fixed",
        "corpus_records": records,
        "unique_observed_residues": len(observed),
        "placements_scanned": tested,
        "physically_observed_compatible_placements": len(matches),
        "minimum_out_of_sector_marks_needed": min(
            len(m["required_sector_exceptions"]) for m in matches
        ),
        "out_of_sector_exception_count_histogram": dict(
            sorted(Counter(len(m["required_sector_exceptions"])
                           for m in matches).items())
        ),
        "placements": matches,
        "interpretation": (
            "One tentative extra dot anywhere in positions 1..81 is insufficient "
            "to restore a direct known-password placement without contradicting "
            "the 66 confirmed residues. The only raw-compatible target instead "
            "requires five out-of-sector dots, all presently unobserved. "
            "These are necessary requirements, NOT predicted physical stickers."
        ),
        "limitations": [
            "Each unexplained exception is not independently documented or authenticated.",
            "All six bijective maps and 28 orientations were explored; these are not independent confirmation.",
            "This analysis only applies to the known normal 14-command bunker phrase.",
            "Newly confirmed stickers must be entered into the canonical observations and rerun.",
        ]
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

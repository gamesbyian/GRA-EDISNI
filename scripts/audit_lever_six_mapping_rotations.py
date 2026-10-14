#!/usr/bin/env python3
"""Experiment 482: all mappings of the known bunker lever code to the H108 zones.

This is a bounded alphabet-compatibility test, not a CE decoder. The observed
81/27 two-alphabet organization is an *assumption about missing residues*, not
proof about stickers that nobody has physically seen.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations
import json

BUNKER = "UURLRRRUUURLLL"
DIRECTIONS = "URL"
STICKER_SYMBOLS = "/-."
PERIOD = 108
PRIMARY_END = 81
SHORTEST_ZONE = 27


def allowed(residue: int) -> frozenset[str]:
    assert 1 <= residue <= PERIOD
    return frozenset("/-") if residue <= PRIMARY_END else frozenset("/.")


def orientations(word: str):
    for reverse in (False, True):
        oriented = word[::-1] if reverse else word
        for rotation in range(len(oriented)):
            yield reverse, rotation, oriented[rotation:] + oriented[:rotation]


def non_slash_switches(word: str, direction_to_symbol: dict[str, str]) -> int:
    """Count changes between the two directions mapped to non-slash marks."""
    shared = next(direction for direction, mark in direction_to_symbol.items()
                  if mark == "/")
    projection = [direction for direction in word if direction != shared]
    return sum(a != b for a, b in zip(projection, projection[1:]))


def fits(start: int, word: str, direction_to_symbol: dict[str, str]) -> bool:
    return all(
        direction_to_symbol[direction] in allowed(((start + index - 1) % PERIOD) + 1)
        for index, direction in enumerate(word)
    )


def run() -> dict:
    assert len(BUNKER) == 14 and Counter(BUNKER) == Counter(U=5, R=5, L=4)
    assert PERIOD - PRIMARY_END == SHORTEST_ZONE and len(BUNKER) < SHORTEST_ZONE

    variants = tuple(orientations(BUNKER))
    assert len(variants) == 28
    assert len({word for _reverse, _rotation, word in variants}) == 28

    reports = []
    total = 0
    matches = 0
    for assignment in permutations(STICKER_SYMBOLS):
        mapping = dict(zip(DIRECTIONS, assignment))
        shared = next(direction for direction, mark in mapping.items() if mark == "/")
        switches = [non_slash_switches(word, mapping)
                    for _reverse, _rotation, word in variants]
        assert min(switches) == 3 and max(switches) == 4

        count = sum(fits(start, word, mapping)
                    for _reverse, _rotation, word in variants
                    for start in range(1, PERIOD + 1))
        trials = len(variants) * PERIOD
        assert trials == 3024
        assert count == 0

        total += trials
        matches += count
        reports.append({
            "direction_to_symbol": mapping,
            "shared_slash_direction": shared,
            "orientations": len(variants),
            "starts_per_orientation": PERIOD,
            "candidate_placements": trials,
            "alphabet_compatible_placements": count,
            "non_slash_projection_min_linear_switches": min(switches),
            "non_slash_projection_max_linear_switches": max(switches),
        })

    assert len(reports) == 6
    assert total == 18144 and matches == 0
    return {
        "experiment": 482,
        "title": "complete secret-ending lever alphabet sensitivity audit",
        "mode": "VALIDATE (bounded negative under the observed-sector-alphabet assumption)",
        "original_bunker_sequence": BUNKER,
        "directed_symbol_counts": {"U": 5, "R": 5, "L": 4},
        "h108_sector_assumption": {
            "residues_1_through_81": ["/", "-"],
            "residues_82_through_108": ["/", "."],
        },
        "all_six_direction_symbol_bijections": 6,
        "orientations_per_bijection": len(variants),
        "distinct_password_dihedral_orientations": len({word for _, _, word in variants}),
        "cyclic_H108_starts": PERIOD,
        "total_placements_tested": total,
        "alphabet_compatible_placements": matches,
        "shortest_sector_length": SHORTEST_ZONE,
        "password_length": len(BUNKER),
        "proof": (
            "The fourteen-move word contains four circular alternating runs "
            "between either pair of directions after deleting the third direction. "
            "Each linear rotation/reversal retains at least three switches "
            "between those two directions. Under any bijection the two non-slash "
            "marks occupy disjoint H108 sectors. A 14-slot window is shorter "
            "than the 27-slot shorter sector and crosses at most one sector "
            "boundary, permitting at most one switch between the non-slash marks."
        ),
        "mappings": reports,
        "caveat": (
            "The sector alphabets constrain the unobserved 42 H108 positions as "
            "a conditional extrapolation from the observed carrier; a future "
            "physically confirmed out-of-sector mark would require rerunning "
            "and revising this result. No new consumer, decipherment, or "
            "physical sticker data is claimed."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

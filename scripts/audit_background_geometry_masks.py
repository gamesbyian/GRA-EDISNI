#!/usr/bin/env python3
"""Audit whether solved A-I background geometry canonically defines body masks.

This is deliberately an identifiability test, not an output search.

The solved background geometry indexes the nine image classes A-I.  The
foreground 9+3 representation indexes, within each image class, nine body
occurrences followed by three tail occurrences.  A geometry-derived 3-way
mask over the body therefore requires an additional bijection from body
position 0..8 to background class A..I.

No such bijection is supplied by data/observations.csv or by the serial/H108
arithmetic.  The script quantifies the resulting convention count and checks
that body positions stay within a single image class.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
CLASSES = "ABCDEFGHI"
GEOMETRY = (("I", "A", "B"), ("C", "D", "E"), ("F", "G", "H"))


def expected_class_for_residue(residue: int) -> str:
    return CLASSES[(residue - 1) % 9]


def main() -> None:
    with OBS.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    for row in rows:
        residue = int(row["residue"])
        expected = expected_class_for_residue(residue)
        actual = row["image_class"]
        assert actual == expected, (residue, actual, expected)

    body_domains = {}
    for cls_index, cls in enumerate(CLASSES):
        body_residues = [cls_index + 1 + 9 * k for k in range(9)]
        body_domains[cls] = {
            "body_residues": body_residues,
            "background_class_for_every_body_position": cls,
        }
        assert all(expected_class_for_residue(r) == cls for r in body_residues)

    # To project the fixed 3x3 A-I geometry onto nine within-class body
    # positions requires a bijection body_index -> background_class.
    full_bijections = math.factorial(9)

    # If we ignore within-row order and ask only for three labelled geometry
    # row masks, there are 9!/(3!^3) possible ordered 3+3+3 partitions.
    ordered_three_mask_partitions = math.factorial(9) // (math.factorial(3) ** 3)

    result = {
        "source": "data/observations.csv",
        "background_geometry": GEOMETRY,
        "body_position_domain": "within one fixed A-I image class across H108",
        "background_geometry_domain": "between the nine A-I image classes",
        "raw_body_to_background_bijection_supplied": False,
        "possible_full_bijections": full_bijections,
        "possible_ordered_three_mask_partitions": ordered_three_mask_partitions,
        "body_domains": body_domains,
        "conclusion": (
            "The solved A-I geometry does not canonically define three masks "
            "over the nine within-class body positions. Applying geometry "
            "masks requires an extra mapping convention before foreground "
            "outputs are inspected."
        ),
    }

    assert full_bijections == 362880
    assert ordered_three_mask_partitions == 1680
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

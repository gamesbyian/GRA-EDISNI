#!/usr/bin/env python3
"""Experiment 352: coordinate/gauge audit of the Experiment-350 one-per-column skeleton."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-352-pos3-coordinate-gauge.json"

ROWS = range(3)
COLS = range(3)
POLARITIES = ("/", "-")


def occupancy_from_coordinates(coords: tuple[int, int, int]) -> tuple[tuple[int, int], ...]:
    return tuple((coords[c], c) for c in COLS)


def coordinates_from_occupancy(occ: tuple[tuple[int, int], ...]) -> tuple[int, int, int]:
    by_col = {}
    for r, c in occ:
        if c in by_col:
            raise ValueError("more than one exceptional cell in a column")
        by_col[c] = r
    if set(by_col) != set(COLS):
        raise ValueError("not exactly one exceptional cell per column")
    return tuple(by_col[c] for c in COLS)


def main() -> None:
    coordinate_states = list(itertools.product(ROWS, repeat=3))
    occupancy_states = [occupancy_from_coordinates(v) for v in coordinate_states]

    assert len(coordinate_states) == 27
    assert len(set(occupancy_states)) == 27
    assert all(coordinates_from_occupancy(o) == v for v, o in zip(coordinate_states, occupancy_states))

    physical_states = [(polarity, coords) for polarity in POLARITIES for coords in coordinate_states]
    assert len(physical_states) == 54

    global_row_relabels = list(itertools.permutations(ROWS))
    independent_column_relabels = list(itertools.product(global_row_relabels, repeat=3))

    assert len(global_row_relabels) == 6
    assert len(independent_column_relabels) == 216

    # Every relabeling is a bijection over the same 27 physical occupancy states.
    for relabels in independent_column_relabels:
        encoded = {
            tuple(relabels[c][coords[c]] for c in COLS)
            for coords in coordinate_states
        }
        assert len(encoded) == 27

    result = {
        "experiment": 352,
        "input_family": "Experiment-350 one-minority-per-physical-column 3x3 skeleton",
        "occupancy_states_per_polarity": len(occupancy_states),
        "physical_states_with_free_binary_polarity": len(physical_states),
        "canonical_coordinate_space": "3^3 = 27 row-position triples",
        "coordinate_bijection": True,
        "global_shared_row_label_gauges": len(global_row_relabels),
        "independent_per_column_row_label_gauges": len(independent_column_relabels),
        "key_result": (
            "exceptional-row triple is a lossless coordinate system for the supported physical occupancy; "
            "numeric labels 0/1/2 are gauge until an external or downstream operation gives them semantics"
        ),
        "remaining_empirical_burden": (
            "why/how the three row coordinates are consumed, related across frames, or interpreted by a later operation"
        ),
        "not_established": [
            "top-to-bottom numeric orientation",
            "arithmetic meaning of 0/1/2",
            "cross-column equality of label orientation",
            "tail reuse",
            "selector semantics",
            "recursive address substitution"
        ]
    }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

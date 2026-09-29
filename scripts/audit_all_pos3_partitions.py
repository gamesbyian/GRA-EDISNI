#!/usr/bin/env python3
"""Experiment 264: broaden POS3 rail orientation to all 280 3+3+3 partitions.

Experiment 263 tested four natural parallel-line partitions of the physical
3x3 frame and found columns uniquely compatible with all nine full-corpus
frames.

This audit removes the line-geometry restriction. Enumerate every unlabeled
partition of the nine physical cells into three 3-cell rails:

    9! / (3!^3 * 3!) = 280

For each partition, each frame may choose either symbol polarity. A partition
survives if all nine primary frames admit at least one exact one-exception-
per-rail completion.

The goal is adversarial: determine whether raw POS3 compatibility itself
selects physical columns, or whether geometry remains an independent cue.
"""

from __future__ import annotations

from itertools import combinations

from audit_pos3_rail_orientation import (
    frame_completion_count,
    frame_observations,
)
from enumerate_raw_machine import load_rows


CELLS = tuple((row, col) for row in range(3) for col in range(3))
LETTERS = {
    (0, 0): "I", (0, 1): "A", (0, 2): "B",
    (1, 0): "C", (1, 1): "D", (1, 2): "E",
    (2, 0): "F", (2, 1): "G", (2, 2): "H",
}


def all_partitions():
    """Yield each unlabeled partition of 9 cells into three unlabeled triples."""
    first = CELLS[0]
    rest = CELLS[1:]
    seen = set()

    for partners in combinations(rest, 2):
        block1 = tuple(sorted((first,) + partners))
        remaining = tuple(cell for cell in rest if cell not in partners)

        first2 = remaining[0]
        for partners2 in combinations(remaining[1:], 2):
            block2 = tuple(sorted((first2,) + partners2))
            block3 = tuple(
                sorted(cell for cell in remaining[1:] if cell not in partners2)
            )
            partition = tuple(sorted((block1, block2, block3)))
            if partition not in seen:
                seen.add(partition)
                yield partition


def compatible_frames(observed_frames, partition):
    compatible = 0
    forced = 0
    for frame in range(9):
        counts = tuple(
            frame_completion_count(
                observed_frames[frame],
                partition,
                polarity,
            )
            for polarity in (False, True)
        )
        viable = sum(count > 0 for count in counts)
        compatible += int(viable > 0)
        forced += int(viable == 1)
    return compatible, forced


def rail_label(rail):
    return "".join(LETTERS[cell] for cell in rail)


def partition_label(partition):
    return "/".join(rail_label(rail) for rail in partition)


def is_vertical_columns(partition):
    expected = {
        frozenset((row, col) for row in range(3))
        for col in range(3)
    }
    return {frozenset(rail) for rail in partition} == expected


def main() -> None:
    partitions = tuple(all_partitions())
    assert len(partitions) == 280

    observed = frame_observations(load_rows())
    survivors = []

    for partition in partitions:
        compatible, forced = compatible_frames(observed, partition)
        if compatible == 9:
            survivors.append((partition, forced))

    assert len(survivors) == 4
    assert sorted(forced for _partition, forced in survivors) == [8, 8, 8, 9]

    column_survivors = [
        (partition, forced)
        for partition, forced in survivors
        if is_vertical_columns(partition)
    ]
    assert len(column_survivors) == 1
    assert column_survivors[0][1] == 8

    labels = sorted(
        (partition_label(partition), forced)
        for partition, forced in survivors
    )
    assert labels == sorted([
        ("IAF/BDE/CGH", 8),
        ("ICF/ADG/BEH", 8),
        ("ICH/ABD/EFG", 9),
        ("ICH/AFG/BDE", 8),
    ])

    print("Experiment 264")
    print("all 3+3+3 cell partitions:", len(partitions))
    print("partitions compatible with all 9 primary frames:", len(survivors))
    for label, forced in labels:
        marker = " [physical columns]" if label == "ICF/ADG/BEH" else ""
        print(f"  {label}: {forced}/9 polarities forced{marker}")
    print("RESULT: raw exact-POS3 compatibility alone leaves four rail partitions")
    print("RESULT: physical columns are the sole all-frame survivor made of the actual straight vertical rails")
    print("CAUTION: geometry is therefore a real model-selection input, not a theorem of symbol compatibility alone")


if __name__ == "__main__":
    main()

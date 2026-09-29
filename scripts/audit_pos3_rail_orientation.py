#!/usr/bin/env python3
"""Experiment 263: audit which natural 3x3 rail orientation reveals primary POS3.

Human-discovery question:
  once stickers are arranged into consecutive 9-residue physical 3x3 frames,
  why read exceptional positions down columns rather than across rows or along
  one of the two toroidal diagonal families?

Bounded orientation family:
  * 3 physical columns;
  * 3 physical rows;
  * 3 wraparound diagonals of slope +1;
  * 3 wraparound diagonals of slope -1.

For each frame and orientation, test whether either symbol polarity admits an
exact one-exception-per-rail POS3 completion.

This is run on both:
  * the full classified primary corpus;
  * the unique 34-residue minimum witness from Experiment 259.
"""

from __future__ import annotations

from functools import reduce
from operator import mul

from enumerate_raw_machine import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    load_rows,
)


WITNESS = frozenset({
    2, 3, 4, 5,
    12, 13, 17, 18,
    20, 21, 24,
    29, 30, 31, 32, 36,
    37, 39, 42, 44,
    46, 47, 48,
    56, 57, 59,
    66, 69, 70, 71,
    74, 75, 76, 79,
})

PARTITIONS = {
    "columns": tuple(
        tuple((row, col) for row in range(3))
        for col in range(3)
    ),
    "rows": tuple(
        tuple((row, col) for col in range(3))
        for row in range(3)
    ),
    "diag_plus": tuple(
        tuple((row, (row + offset) % 3) for row in range(3))
        for offset in range(3)
    ),
    "diag_minus": tuple(
        tuple((row, (offset - row) % 3) for row in range(3))
        for offset in range(3)
    ),
}


def frame_observations(rows, allowed_residues=None):
    result = {frame: {} for frame in range(9)}

    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        if allowed_residues is not None and residue not in allowed_residues:
            continue

        frame = (residue - 1) // 9
        j = (residue - 1) % 9
        position = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        result[frame][position] = record["symbol"]

    return result


def rail_options(observed, rail, minority_is_dash):
    minority = "-" if minority_is_dash else "/"
    majority = "/" if minority_is_dash else "-"

    options = []
    for exceptional_position in rail:
        valid = True
        for position in rail:
            symbol = observed.get(position)
            if symbol is None:
                continue
            expected = minority if position == exceptional_position else majority
            if symbol != expected:
                valid = False
                break
        if valid:
            options.append(exceptional_position)
    return tuple(options)


def frame_completion_count(observed, partition, minority_is_dash):
    options = tuple(
        rail_options(observed, rail, minority_is_dash)
        for rail in partition
    )
    return reduce(mul, (len(values) for values in options), 1)


def audit(observed_frames):
    summary = {}

    for name, partition in PARTITIONS.items():
        frame_counts = []
        compatible = 0
        forced = 0

        for frame in range(9):
            slash_minority = frame_completion_count(
                observed_frames[frame],
                partition,
                False,
            )
            dash_minority = frame_completion_count(
                observed_frames[frame],
                partition,
                True,
            )
            viable = int(slash_minority > 0) + int(dash_minority > 0)
            compatible += int(viable > 0)
            forced += int(viable == 1)
            frame_counts.append((slash_minority, dash_minority))

        summary[name] = {
            "compatible": compatible,
            "forced": forced,
            "frames": tuple(frame_counts),
        }

    return summary


def main() -> None:
    rows = load_rows()

    full = audit(frame_observations(rows))
    witness = audit(frame_observations(rows, WITNESS))

    assert {
        name: (result["compatible"], result["forced"])
        for name, result in full.items()
    } == {
        "columns": (9, 8),
        "rows": (5, 5),
        "diag_plus": (4, 4),
        "diag_minus": (4, 4),
    }

    assert {
        name: (result["compatible"], result["forced"])
        for name, result in witness.items()
    } == {
        "columns": (9, 8),
        "rows": (9, 4),
        "diag_plus": (9, 4),
        "diag_minus": (9, 3),
    }

    print("Experiment 263")
    print("orientation | full compatible/forced | witness compatible/forced")
    for name in PARTITIONS:
        f = full[name]
        w = witness[name]
        print(
            f"{name:>10} | "
            f"{f['compatible']}/9 compatible, {f['forced']}/9 forced | "
            f"{w['compatible']}/9 compatible, {w['forced']}/9 forced"
        )

    print("RESULT: columns are the only tested natural rail orientation fitting all 9 full-corpus frames")
    print("RESULT: on the 34-residue witness, columns still maximize polarity determinacy (8 vs 4/4/3)")
    print("CAUTION: the orientation family is bounded to four natural parallel-line partitions")


if __name__ == "__main__":
    main()

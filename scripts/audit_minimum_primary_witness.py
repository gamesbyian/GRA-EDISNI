#!/usr/bin/env python3
"""Experiment 259: exact minimum raw-primary witness for the 8/25 reconstruction.

Target reconstruction from Experiment 246:
  * 8 of 9 frame polarities are uniquely forced with polarity initially free;
  * under the established d<=q staircase, 25 of 27 primary trits are uniquely
    forced.

Question:
  what is the smallest set of DISTINCT observed primary H108 residues that
  preserves every one of those specific forced conclusions?

The nine (q,d) frames are independent for these constraints, so the global
minimum is the sum of nine exact per-frame subset searches. This is an exact
minimum, not a greedy reduction.

This does not claim that 34 stickers are sufficient to discover H108/POS3
from scratch. It isolates the minimum witness once that representation family
is being tested.
"""

from __future__ import annotations

from itertools import combinations

from audit_primary_leave_one_out import (
    allowed_rows,
    build_columns,
    load_rows,
)


def rows_by_residue(rows):
    result = {}
    for record in rows:
        residue = int(record["residue"])
        if residue <= 81:
            result.setdefault(residue, []).append(record)
    return result


def frame_of_residue(residue):
    offset = residue - 1
    return offset // 27, (offset % 27) // 9


def rows_for_residues(grouped, residues):
    return [
        record
        for residue in residues
        for record in grouped[residue]
    ]


def baseline_targets(rows):
    columns = build_columns(rows)
    polarities = {}
    trits = {}

    for q in range(3):
        for d in range(3):
            viable = []
            for minority_is_dash in (False, True):
                if all(
                    allowed_rows(columns, q, d, col, minority_is_dash)
                    for col in range(3)
                ):
                    viable.append(minority_is_dash)
            polarities[(q, d)] = viable[0] if len(viable) == 1 else None

            for col in range(3):
                allowed = allowed_rows(columns, q, d, col, d <= q)
                trits[(q, d, col)] = allowed[0] if len(allowed) == 1 else None

    assert sum(value is not None for value in polarities.values()) == 8
    assert sum(value is not None for value in trits.values()) == 25
    return polarities, trits


def frame_satisfies(rows, q, d, target_polarities, target_trits):
    columns = build_columns(rows)

    for col in range(3):
        target = target_trits[(q, d, col)]
        if target is None:
            continue
        if allowed_rows(columns, q, d, col, d <= q) != (target,):
            return False

    target_polarity = target_polarities[(q, d)]
    if target_polarity is not None:
        viable = []
        for minority_is_dash in (False, True):
            if all(
                allowed_rows(columns, q, d, col, minority_is_dash)
                for col in range(3)
            ):
                viable.append(minority_is_dash)
        if viable != [target_polarity]:
            return False

    return True


def main() -> None:
    rows = load_rows()
    grouped = rows_by_residue(rows)
    target_polarities, target_trits = baseline_targets(rows)

    frame_residues = {
        (q, d): sorted(
            residue
            for residue in grouped
            if frame_of_residue(residue) == (q, d)
        )
        for q in range(3)
        for d in range(3)
    }

    minima = {}
    for q in range(3):
        for d in range(3):
            candidates = frame_residues[(q, d)]
            winners = []

            for size in range(len(candidates) + 1):
                for subset in combinations(candidates, size):
                    subset_rows = rows_for_residues(grouped, subset)
                    if frame_satisfies(
                        subset_rows,
                        q,
                        d,
                        target_polarities,
                        target_trits,
                    ):
                        winners.append(subset)
                if winners:
                    minima[(q, d)] = (size, tuple(winners))
                    break

    # Every frame has a unique minimum witness.
    assert all(len(winners) == 1 for _size, winners in minima.values())

    expected = {
        (0, 0): (2, 3, 4, 5),
        (0, 1): (12, 13, 17, 18),
        (0, 2): (20, 21, 24),
        (1, 0): (29, 30, 31, 32, 36),
        (1, 1): (37, 39, 42, 44),
        (1, 2): (46, 47, 48),
        (2, 0): (56, 57, 59),
        (2, 1): (66, 69, 70, 71),
        (2, 2): (74, 75, 76, 79),
    }

    actual = {
        frame: winners[0]
        for frame, (_size, winners) in minima.items()
    }
    assert actual == expected

    global_witness = tuple(
        residue
        for frame in sorted(actual)
        for residue in actual[frame]
    )
    assert len(global_witness) == 34
    assert len(set(global_witness)) == 34

    # Verify the assembled minimum witness preserves the complete headline
    # reconstruction, not merely the independently checked frame pieces.
    witness_rows = rows_for_residues(grouped, global_witness)
    witness_polarities, witness_trits = baseline_targets(witness_rows)
    assert witness_polarities == target_polarities
    assert witness_trits == target_trits

    print("Experiment 259")
    print("distinct observed primary residues:", len(grouped))
    print("exact minimum witness size:", len(global_witness))
    print("minimum witness is unique within the per-frame factorized search")
    print("per-frame minima:")
    for frame in sorted(actual):
        print(" ", frame, "->", actual[frame])
    print("global witness:", global_witness)
    print("RESULT: 34 distinct residues are necessary and sufficient")
    print("RESULT: this witness preserves all 8 forced polarities and 25 forced trits")
    print("CAUTION: minimum is conditional on testing the established H108/POS3 representation")


if __name__ == "__main__":
    main()

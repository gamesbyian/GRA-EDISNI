#!/usr/bin/env python3
"""Experiment 257: replace exact primary POS3 with weaker frame-balance regularity.

Experiment 255 weakens each primary column to zero-or-one minority pulse and
finds 832 recursively closed machines. Exact POS3 is the 14-state occupied
subfamily.

Here the parent remains that 832-state closure family. Instead of requiring
one pulse in every column, impose only a much weaker count regularity:

    within each external quarter q, the three depth frames d=0,1,2 have equal
    total minority-pulse counts.

A frame may therefore contain 0..3 pulses and no column is individually
required to be occupied. This tests whether the exact one-pulse-per-column
family can be recovered from a coarser visual/count symmetry.
"""

from __future__ import annotations

from collections import Counter

from audit_primary_optional_pulse import (
    enumerate_primary,
    first_surface,
    optional_primary_candidates,
    terminal_surface,
)
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


def frame_weights(payload):
    """Minority-pulse count for the nine (q,d) frames in q-major order."""
    return tuple(
        sum(payload[(q, d, col)] is not None for col in range(3))
        for q in range(3)
        for d in range(3)
    )


def quarter_balanced(payload, q):
    weights = frame_weights(payload)[3 * q : 3 * q + 3]
    return len(set(weights)) == 1


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary(optional_primary_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    assert len(payloads) == 1536
    assert len(selectors) == 36

    survivors = []
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue

            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue

            missing = sum(value is None for value in payload.values())
            survivors.append((payload, selector, first, terminal, missing))

    assert len(survivors) == 832
    assert {item[3] for item in survivors} == {"100"}

    # Measure each quarter-balance condition separately and cumulatively.
    subset_counts = {}
    for mask in range(1, 8):
        quarters = tuple(q for q in range(3) if mask & (1 << q))
        selected = [
            item
            for item in survivors
            if all(quarter_balanced(item[0], q) for q in quarters)
        ]
        subset_counts[quarters] = (
            len(selected),
            Counter(item[4] for item in selected),
        )

    assert subset_counts[(0,)][0] == 352
    assert subset_counts[(1,)][0] == 104
    assert subset_counts[(2,)][0] == 256
    assert subset_counts[(0, 1)][0] == 44
    assert subset_counts[(0, 2)][0] == 112
    assert subset_counts[(1, 2)][0] == 32

    all_balanced = [
        item
        for item in survivors
        if all(quarter_balanced(item[0], q) for q in range(3))
    ]
    assert len(all_balanced) == 14
    assert all(item[4] == 0 for item in all_balanced)

    # The coarser balance rule therefore recovers exact POS3 without asking
    # for column occupancy directly.
    for payload, _selector, _first, _terminal, _missing in all_balanced:
        assert set(frame_weights(payload)) == {3}
        assert all(value is not None for value in payload.values())

    print("Experiment 257")
    print("optional-pulse recursive closure states:", len(survivors))
    print("quarter-balance survivor counts:")
    for quarters in sorted(subset_counts, key=lambda qs: (len(qs), qs)):
        count, missing = subset_counts[quarters]
        print(
            " ",
            quarters,
            "->",
            count,
            "missing-pulse distribution",
            dict(sorted(missing.items())),
        )
    print("all three quarters depth-balanced:", len(all_balanced))
    print("RESULT: quarter-local frame-weight balance recovers the exact 14-state family")
    print("RESULT: one-pulse-per-column need not be imposed directly inside this tested parent")
    print("CAUTION: frame-weight balance is a new grammar/simplicity assumption, not raw observation")


if __name__ == "__main__":
    main()

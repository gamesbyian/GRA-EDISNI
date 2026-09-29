#!/usr/bin/env python3
"""Experiment 258: prove quarter-local frame balance is cardinality-minimal.

Parent set: the 832 recursively closed optional-pulse states from Experiment
255. The canonical exact-POS3 subfamily contains 14 states.

Candidate constraints are deliberately simple:
    weight(frame_i) == weight(frame_j)

for any pair among the nine (q,d) primary frames. There are 36 possible
pairwise equalities.

Question:
  what is the minimum number of such equality constraints needed to exclude
  every noncanonical optional-pulse survivor while retaining the 14 exact-POS3
  states?

The Experiment-257 quarter-local rule uses six:
  within each q, d0=d1 and d0=d2.
"""

from __future__ import annotations

from itertools import combinations

from audit_primary_frame_balance import frame_weights
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


FRAME_PAIRS = tuple(combinations(range(9), 2))
QUARTER_BALANCE_PAIRS = (
    (0, 1), (0, 2),
    (3, 4), (3, 5),
    (6, 7), (6, 8),
)


def closure_survivors():
    rows = load_rows()
    payloads = enumerate_primary(optional_primary_candidates(rows))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

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
            survivors.append((payload, missing))
    return survivors


def exclusion_mask(weights_by_bad_state, pair):
    a, b = pair
    mask = 0
    for index, weights in enumerate(weights_by_bad_state):
        if weights[a] != weights[b]:
            mask |= 1 << index
    return mask


def main() -> None:
    survivors = closure_survivors()
    assert len(survivors) == 832

    canonical = [item for item in survivors if item[1] == 0]
    bad = [item for item in survivors if item[1] > 0]
    assert len(canonical) == 14
    assert len(bad) == 818

    # Every exact-POS3 state has frame weight 3 everywhere, so every candidate
    # equality preserves all 14 canonical states. We only need to cover/exclude
    # the 818 noncanonical states.
    assert all(set(frame_weights(payload)) == {3} for payload, _missing in canonical)

    bad_weights = [frame_weights(payload) for payload, _missing in bad]
    masks = {
        pair: exclusion_mask(bad_weights, pair)
        for pair in FRAME_PAIRS
    }
    full = (1 << len(bad)) - 1

    # Exhaustively prove no set of <=5 pairwise equalities rejects every
    # noncanonical survivor.
    for size in range(1, 6):
        for chosen in combinations(FRAME_PAIRS, size):
            union = 0
            for pair in chosen:
                union |= masks[pair]
            assert union != full

    # The natural within-quarter depth-balance rule uses six equalities and
    # does exclude every noncanonical state.
    union = 0
    for pair in QUARTER_BALANCE_PAIRS:
        union |= masks[pair]
    assert union == full

    print("Experiment 258")
    print("optional-pulse closure states:", len(survivors))
    print("canonical exact-POS3 states:", len(canonical))
    print("noncanonical states to exclude:", len(bad))
    print("candidate pairwise frame-weight equalities:", len(FRAME_PAIRS))
    print("exhaustive lower bound: no equality set of size <=5 is sufficient")
    print("quarter-local balance equalities:", QUARTER_BALANCE_PAIRS)
    print("quarter-local balance size:", len(QUARTER_BALANCE_PAIRS))
    print("RESULT: six is the exact minimum in the pairwise frame-weight-equality family")
    print("RESULT: the natural per-quarter balance rule is cardinality-minimal, though not claimed unique")


if __name__ == "__main__":
    main()

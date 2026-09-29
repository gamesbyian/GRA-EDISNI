#!/usr/bin/env python3
"""Experiment 244: broaden the second-pass selector-reuse family exactly.

Parent family (declared before output inspection):
    candidate terminal cell = B(f(S(j)), g(S(j)), j)

where f and g are independently chosen from all 27 maps {0,1,2}->{0,1,2}.
There are therefore 27^2 = 729 ordered coordinate-map pairs.

Acceptance criterion:
  * for every one of the 14 legal native states, the resulting 3x3 surface
    is a valid dash-POS3 object (one dash per column); and
  * the decoded ternary payload is identical across all 14 states.

The script reports the full family and then the permutation-preserving
subfamily. No terminal payload is hard-coded into the acceptance criterion.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from verify_native_model import (
    PHYSICAL_LAYOUT,
    SERIAL_ORDER,
    foreground_symbol,
    legal_native_states,
    selector_field,
)

TERNARY_MAPS = tuple(product(range(3), repeat=3))
PERMUTATIONS = frozenset(mapping for mapping in TERNARY_MAPS if len(set(mapping)) == 3)


def frame_symbol(state, q: int, d: int, row: int, col: int) -> str:
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return foreground_symbol(state, residue)


def candidate_surface(state, f, g):
    selector = selector_field(state)
    return tuple(
        tuple(
            frame_symbol(
                state,
                f[selector[row][col]],
                g[selector[row][col]],
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def decode_dash_pos3(surface):
    digits = []
    for col in range(3):
        rows = [row for row in range(3) if surface[row][col] == "-"]
        if len(rows) != 1:
            return None
        digits.append(str(rows[0]))
    return "".join(digits)


def label(mapping) -> str:
    return "".join(str(value) for value in mapping)


def main() -> None:
    states = legal_native_states()
    assert len(states) == 14

    winners = []
    for f in TERNARY_MAPS:
        for g in TERNARY_MAPS:
            outputs = [
                decode_dash_pos3(candidate_surface(state, f, g))
                for state in states
            ]
            if None not in outputs and len(set(outputs)) == 1:
                winners.append((f, g, outputs[0]))

    # Exact broad-family result.
    assert len(winners) == 25
    output_counts = Counter(output for _f, _g, output in winners)
    assert output_counts == Counter({
        "102": 6,
        "100": 6,
        "002": 6,
        "212": 4,
        "112": 2,
        "022": 1,
    })

    permutation_winners = [
        (f, g, output)
        for f, g, output in winners
        if f in PERMUTATIONS and g in PERMUTATIONS
    ]

    # The canonical-shell-preserving family has one exact survivor.
    assert permutation_winners == [((0, 1, 2), (0, 1, 2), "100")]

    print("Experiment 244")
    print("parent family: 729 ordered coordinate-map pairs")
    print(f"state-invariant POS3 survivors: {len(winners)}")
    print("payload counts:", dict(sorted(output_counts.items())))
    print("all survivors:")
    for f, g, output in winners:
        marker = "  [permutation pair]" if f in PERMUTATIONS and g in PERMUTATIONS else ""
        print(f"  f={label(f)} g={label(g)} -> {output}{marker}")

    print("OK: exactly one permutation-preserving pair survives")
    print("OK: f=012, g=012 (identity/identity) -> terminal 100")


if __name__ == "__main__":
    main()

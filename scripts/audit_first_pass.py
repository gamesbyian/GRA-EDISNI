#!/usr/bin/env python3
"""Experiment 245: broaden the first-pass address-substitution family.

Parent family (declared before output inspection):
    candidate surface_q(j) = B(f(q), g(S(j)), j)

where f and g range independently over all 27 ternary maps.

Acceptance criteria:
  * every surface for all 14 states and all three external q values is a
    valid dash-POS3 object; and
  * the ordered triple of decoded surfaces depends only on selector class p,
    not on the remaining physical-state freedom.

No expected payload strings are used as filters.

The permutation-preserving subfamily isolates genuine shell relabelings.
"""

from __future__ import annotations

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
IDENTITY = (0, 1, 2)


def frame_symbol(state, q: int, d: int, row: int, col: int) -> str:
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return foreground_symbol(state, residue)


def candidate_surface(state, f, g, q: int):
    selector = selector_field(state)
    return tuple(
        tuple(
            frame_symbol(
                state,
                f[q],
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

    survivors = []
    for f in TERNARY_MAPS:
        for g in TERNARY_MAPS:
            outputs_by_state = {}
            valid = True

            for state in states:
                outputs = tuple(
                    decode_dash_pos3(candidate_surface(state, f, g, q))
                    for q in range(3)
                )
                if None in outputs:
                    valid = False
                    break
                outputs_by_state[state] = outputs

            if not valid:
                continue

            by_p = {}
            for state, outputs in outputs_by_state.items():
                prior = by_p.setdefault(state.p, outputs)
                if prior != outputs:
                    valid = False
                    break

            if valid and len(by_p) == 3:
                survivors.append((f, g, by_p))

    assert len(survivors) == 49

    permutation_survivors = [
        (f, g, by_p)
        for f, g, by_p in survivors
        if f in PERMUTATIONS and g in PERMUTATIONS
    ]

    # Shell preservation forces selector-depth mapping g to identity.
    # The remaining six f values are exactly the six relabelings of external q.
    assert len(permutation_survivors) == 6
    assert {f for f, _g, _by_p in permutation_survivors} == set(PERMUTATIONS)
    assert {g for _f, g, _by_p in permutation_survivors} == {IDENTITY}

    # Once physical q labels are fixed, identity/identity is the sole survivor.
    fixed_q = [
        (f, g, by_p)
        for f, g, by_p in permutation_survivors
        if f == IDENTITY
    ]
    assert len(fixed_q) == 1
    f, g, by_p = fixed_q[0]
    assert f == IDENTITY
    assert g == IDENTITY

    print("Experiment 245")
    print("parent family: 729 ordered coordinate-map pairs")
    print(f"POS3 + p-factorized survivors: {len(survivors)}")
    print(f"permutation-preserving survivors: {len(permutation_survivors)}")
    print("permutation-preserving family:")
    for f, g, payloads in permutation_survivors:
        print(
            f"  f={label(f)} g={label(g)} "
            f"p0={payloads[0]} p1={payloads[1]} p2={payloads[2]}"
        )

    print("OK: shell preservation forces g=012")
    print("OK: remaining f freedom is exactly the six q relabelings")
    print("OK: fixing physical q labels leaves f=012, g=012 uniquely")


if __name__ == "__main__":
    main()

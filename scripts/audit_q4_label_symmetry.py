#!/usr/bin/env python3
"""Experiment 296: stress-test the residual Q4 physical codebook gauge by label symmetry.

Experiment 295 recovers seven of nine entries of a shared binary codebook
E[S,d] from the Experiment-294 selector family plus classified Q4 marks.  Four
codebooks survive, differing only at E[0,2] and E[1,2].

This experiment does not add observations.  Instead it asks exactly how much
ternary-label symmetry is needed to remove that two-bit physical gauge.

For every surviving codebook, test simultaneous relabelings of selector value
and physical depth:

    E[S,d] == E[pi(S), pi(d)]

for each permutation pi in S3.

This criterion is weaker than assuming the full cyclic rule
E[S,d] = h((d-S) mod 3): it can be imposed one permutation at a time.  The goal
is to expose which label asymmetry the two remaining bits represent, and to
distinguish a genuine observational result from an authoring-symmetry prior.
"""

from __future__ import annotations

from itertools import permutations

from audit_q4_physical_codebook import (
    CORE_WORDS,
    DOT,
    FIXED_SELECTOR,
    SERIAL_ORDER,
    SLASH,
    codeword,
    load_rows,
    symbol,
)


def recovered_codebooks():
    rows = load_rows()
    constraints = {}

    for record in rows:
        residue = int(record["residue"])
        if residue < 82:
            continue
        offset = residue - 82
        depth = offset // 9
        letter = SERIAL_ORDER[offset % 9]
        if letter not in FIXED_SELECTOR:
            continue
        constraints[(FIXED_SELECTOR[letter], depth)] = record["symbol"]

    fixed_compatible = [
        mask
        for mask in range(1 << 9)
        if all(
            symbol(mask, selector, depth) == observed
            for (selector, depth), observed in constraints.items()
        )
    ]

    selector_fields = []
    for c_gauge in (0, 2):
        for core in CORE_WORDS:
            selector_fields.append(
                {
                    "A": int(core[0]),
                    "D": int(core[1]),
                    "G": int(core[2]),
                    "B": 2,
                    "C": c_gauge,
                    "E": 0,
                    "F": 1,
                    "H": 2,
                    "I": 2,
                }
            )

    q4_observations = []
    for record in rows:
        residue = int(record["residue"])
        if residue < 82:
            continue
        offset = residue - 82
        q4_observations.append(
            (SERIAL_ORDER[offset % 9], offset // 9, record["symbol"])
        )

    compatible = [
        mask
        for mask in fixed_compatible
        if all(
            symbol(mask, field[letter], depth) == observed
            for field in selector_fields
            for letter, depth, observed in q4_observations
        )
    ]
    assert len(compatible) == 4
    return compatible


def invariant_under(mask: int, permutation: tuple[int, int, int]) -> bool:
    return all(
        symbol(mask, selector, depth)
        == symbol(mask, permutation[selector], permutation[depth])
        for selector in range(3)
        for depth in range(3)
    )


def rows(mask: int) -> tuple[str, str, str]:
    return tuple(codeword(mask, selector) for selector in range(3))


def main() -> None:
    compatible = recovered_codebooks()

    canonical_rows = ("/..", "./.", "../")
    canonical = next(mask for mask in compatible if rows(mask) == canonical_rows)

    all_permutations = tuple(permutations(range(3)))
    identity = (0, 1, 2)

    survivors = {
        permutation: [
            mask for mask in compatible if invariant_under(mask, permutation)
        ]
        for permutation in all_permutations
    }

    assert len(survivors[identity]) == 4

    # Four of the five non-identity simultaneous relabelings uniquely select
    # the canonical equality code.  The sole exception is swap(0,1), which
    # fixes label 2 and therefore cannot individually determine how values
    # 0/1 relate to physical depth 2.
    swap_01 = (1, 0, 2)
    assert len(survivors[swap_01]) == 2
    assert canonical in survivors[swap_01]

    for permutation in all_permutations:
        if permutation in (identity, swap_01):
            continue
        assert survivors[permutation] == [canonical]

    # Equivalently: every nontrivial simultaneous relabeling that moves label
    # 2 fixes both remaining gauge bits.  The two 3-cycles are transitive on
    # the ternary labels, so either single cycle already suffices.
    moving_two = [
        permutation
        for permutation in all_permutations
        if permutation != identity and permutation[2] != 2
    ]
    assert len(moving_two) == 4
    assert all(survivors[p] == [canonical] for p in moving_two)

    cycles = [(1, 2, 0), (2, 0, 1)]
    assert all(survivors[p] == [canonical] for p in cycles)

    print("Experiment 296")
    print("Experiment-295 compatible codebooks:", [rows(mask) for mask in compatible])
    for permutation in all_permutations:
        print(
            "simultaneous relabel",
            permutation,
            "->",
            [rows(mask) for mask in survivors[permutation]],
        )
    print("RESULT: identity leaves all four physical codebooks")
    print("RESULT: swap(0,1) leaves exactly two codebooks")
    print("RESULT: each of the other four nontrivial relabelings uniquely selects /.. ./ ../")
    print("RESULT: either ternary 3-cycle alone removes the full two-bit codebook gauge")
    print("RESULT: the residual gauge is exactly an asymmetry involving physical/selector label 2")
    print("CAUTION: label-equivariance is an authoring symmetry prior, not an additional observation")


if __name__ == "__main__":
    main()

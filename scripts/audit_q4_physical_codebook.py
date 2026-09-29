#!/usr/bin/env python3
"""Experiment 295: recover the physical Q4 POS3 code from holdout marks.

Experiment 294 recovers the abstract ternary Q4 selector without using any Q4
slash/dot observations. Its route-capable family fixes these selector values:

    B=2, E=0, F=1, H=2, I=2

while C is a 0/2 gauge and A/D/G form the variable control core.

This experiment now treats the physical Q4 marks as genuine holdout evidence.
Do NOT assume "one slash per stack" or exceptional-position POS3. Instead posit
only one shared binary codebook E[S,d] over selector value S and physical depth
d. Such a codebook has 9 independent slash/dot entries.

Use only observations at the Experiment-294 fixed scaffold positions B/E/F/H/I.
A/D/G are excluded because their selector value is state-dependent; C is
excluded because it is the surviving gauge.

Then test three deliberately simple completion criteria:
  1. equal Hamming weight for all three selector-value codewords;
  2. cyclic depth/value equivariance E[S,d] = h((d-S) mod 3);
  3. minimum total slash count (reported as a simplicity prior only).

Goal:
  determine whether the familiar one-slash positional code can be recovered
  from an independently reconstructed selector plus physical holdout marks,
  rather than supplied as the Q4 grammar from the start.
"""

from __future__ import annotations

from collections import Counter

from enumerate_raw_machine import SERIAL_ORDER, load_rows

SLASH = "/"
DOT = "."

# Recovered by Experiment 294 without reading Q4 symbol observations.
FIXED_SELECTOR = {
    "B": 2,
    "E": 0,
    "F": 1,
    "H": 2,
    "I": 2,
}
CORE_WORDS = ("110", "220", "212")


def code_bit(mask: int, selector: int, depth: int) -> int:
    return (mask >> (3 * selector + depth)) & 1


def symbol(mask: int, selector: int, depth: int) -> str:
    return SLASH if code_bit(mask, selector, depth) else DOT


def codeword(mask: int, selector: int) -> str:
    return "".join(symbol(mask, selector, depth) for depth in range(3))


def row_weight(mask: int, selector: int) -> int:
    return sum(code_bit(mask, selector, depth) for depth in range(3))


def is_cyclic_equivariant(mask: int) -> bool:
    # A simultaneous +1 relabeling of selector value and physical depth leaves
    # the symbol unchanged. Equivalently the code depends only on d-S mod 3.
    for selector in range(3):
        for depth in range(3):
            reference_depth = (depth - selector) % 3
            if code_bit(mask, selector, depth) != code_bit(
                mask, 0, reference_depth
            ):
                return False
    return True


def main() -> None:
    rows = load_rows()

    fixed_observations = []
    constraints = {}

    for record in rows:
        residue = int(record["residue"])
        if residue < 82:
            continue

        offset = residue - 82
        depth = offset // 9
        j = offset % 9
        letter = SERIAL_ORDER[j]

        if letter not in FIXED_SELECTOR:
            continue

        selector = FIXED_SELECTOR[letter]
        observed_symbol = record["symbol"]
        key = (selector, depth)

        if key in constraints:
            assert constraints[key] == observed_symbol
        else:
            constraints[key] = observed_symbol

        fixed_observations.append(
            (letter, selector, depth, observed_symbol)
        )

    # Nine physical observations at fixed scaffold cells collapse to six
    # distinct entries of the shared 3x3 selector/depth codebook.
    assert len(fixed_observations) == 9
    assert constraints == {
        (0, 0): SLASH,
        (0, 1): DOT,
        (1, 1): SLASH,
        (2, 0): DOT,
        (2, 1): DOT,
        (2, 2): SLASH,
    }

    fixed_compatible = [
        mask
        for mask in range(1 << 9)
        if all(
            symbol(mask, selector, depth) == observed_symbol
            for (selector, depth), observed_symbol in constraints.items()
        )
    ]
    assert len(fixed_compatible) == 8

    # Now reintroduce the state-dependent A/D/G positions without guessing a
    # hidden state. Experiment 294 recovered all three functional core words
    # and both C-gauge representatives, so a shared physical codebook that is
    # compatible with the full machine must reproduce every classified Q4 mark
    # for every recovered selector field.
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
            (
                SERIAL_ORDER[offset % 9],
                offset // 9,
                record["symbol"],
            )
        )

    compatible = []
    for mask in fixed_compatible:
        if all(
            symbol(mask, field[letter], depth) == observed_symbol
            for field in selector_fields
            for letter, depth, observed_symbol in q4_observations
        ):
            compatible.append(mask)

    assert len(q4_observations) == 11
    assert len(selector_fields) == 6
    assert len(compatible) == 4

    forced_entries = {}
    variable_entries = []
    for selector in range(3):
        for depth in range(3):
            values = {
                symbol(mask, selector, depth)
                for mask in compatible
            }
            if len(values) == 1:
                forced_entries[(selector, depth)] = next(iter(values))
            else:
                variable_entries.append((selector, depth))

    assert forced_entries == {
        (0, 0): SLASH,
        (0, 1): DOT,
        (1, 0): DOT,
        (1, 1): SLASH,
        (2, 0): DOT,
        (2, 1): DOT,
        (2, 2): SLASH,
    }
    assert variable_entries == [(0, 2), (1, 2)]

    # Basic ternary distinguishability is still too weak: all four full-family
    # compatible codebooks already have distinct, nonuniform physical rows.
    distinct_rows = [
        mask
        for mask in compatible
        if len({codeword(mask, selector) for selector in range(3)}) == 3
    ]
    assert len(distinct_rows) == 4

    nonuniform_rows = [
        mask
        for mask in compatible
        if all(row_weight(mask, selector) in (1, 2) for selector in range(3))
    ]
    assert len(nonuniform_rows) == 4

    equal_weight = [
        mask
        for mask in compatible
        if len({row_weight(mask, selector) for selector in range(3)}) == 1
    ]
    cyclic = [
        mask
        for mask in compatible
        if is_cyclic_equivariant(mask)
    ]

    total_slashes = {
        mask: sum(row_weight(mask, selector) for selector in range(3))
        for mask in compatible
    }
    minimum_slashes = min(total_slashes.values())
    minimum_weight = [
        mask
        for mask, count in total_slashes.items()
        if count == minimum_slashes
    ]

    canonical_rows = ("/..", "./.", "../")
    canonical = next(
        mask
        for mask in compatible
        if tuple(codeword(mask, selector) for selector in range(3))
        == canonical_rows
    )

    assert equal_weight == [canonical]
    assert cyclic == [canonical]
    assert minimum_slashes == 3
    assert minimum_weight == [canonical]

    # The recovered code is exactly slash-at-selected-depth / dot-elsewhere.
    for selector in range(3):
        for depth in range(3):
            assert symbol(canonical, selector, depth) == (
                SLASH if selector == depth else DOT
            )

    print("Experiment 295")
    print("Experiment-294 fixed scaffold selector values:", FIXED_SELECTOR)
    print("fixed-scaffold Q4 observations:", len(fixed_observations))
    print("distinct shared-codebook entries observed:", len(constraints))
    print("fixed-scaffold-compatible codebooks:", len(fixed_compatible))
    print("full recovered-family compatible codebooks:", len(compatible))
    print("forced shared-codebook entries:", forced_entries)
    print("remaining physical-codebook gauge entries:", variable_entries)
    print(
        "full-family compatible codebooks:",
        [
            tuple(codeword(mask, selector) for selector in range(3))
            for mask in compatible
        ],
    )
    print("pairwise-distinct-codeword survivors:", len(distinct_rows))
    print("all-nonuniform-codeword survivors:", len(nonuniform_rows))
    print(
        "equal-row-weight survivors:",
        [tuple(codeword(mask, s) for s in range(3)) for mask in equal_weight],
    )
    print(
        "cyclic-equivariant survivors:",
        [tuple(codeword(mask, s) for s in range(3)) for mask in cyclic],
    )
    print(
        "minimum-slash survivors:",
        [tuple(codeword(mask, s) for s in range(3)) for mask in minimum_weight],
    )
    print("RESULT: raw Q4 marks + the recovered selector family force 7/9 codebook entries")
    print("RESULT: only E[0,2] and E[1,2] remain as a two-bit physical-codebook gauge")
    print("RESULT: two independent symmetry criteria recover /.., ./., ../")
    print("RESULT: physical Q4 one-slash POS3 need not be supplied directly")
    print("RESULT: raw Q4 scaffold marks become holdout evidence after Experiment 294")
    print("CAUTION: shared-codebook/equal-weight or cyclic symmetry is an authoring grammar, not a new observation")


if __name__ == "__main__":
    main()

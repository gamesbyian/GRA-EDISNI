#!/usr/bin/env python3
"""Experiment 302: decompose the local-S3 route-max fork into gauge structure.

Experiment 301 broadens the reused local operation to an arbitrary selector
permutation g_j at every A-I cell. At the 14-state route maximum it finds four
64-operation equivalence classes. Two have invariant terminal 100:

    * the canonical physical 14-state family;
    * an A:102 sibling sharing only 10/14 physical states, but preserving the
      same three functional families, same route shell, and terminal 100.

This audit explains that apparently serious sibling.

Result in brief:
    * each invariant-100 class is a 2^6 operation-gauge orbit;
    * five gauge bits only permute selector values never exercised at a
      fixed-value Q4 position;
    * the sixth, C:210, is supported by exact d=0/d=2 symbol equality at C;
    * the A:102 coset replaces four canonical states only by changing physical
      selector A from 1 to 0;
    * those paired masters differ only at Q4 residues 82 and 91, both unobserved;
    * A:102 maps the sibling's physical A=0 back to effective depth 1 on the
      first pass;
    * on the second pass the residual source change (q,d)=(1,1)->(0,1) is
      symbol-identical at A for every raw-compatible primary payload, matching
      the already-known f1 recursion gauge.

Thus the invariant-100 fork is a coupled latent-label / operation gauge, not a
new functional machine. The raw corpus still cannot choose the printed A-stack
representative, because that stack is unobserved.
"""

from __future__ import annotations

from itertools import product

from audit_local_selector_permutations import (
    A_SWAP_01,
    IDENTITY,
    raw_candidates,
)
from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    frame_symbol,
    generate_master,
    load_rows,
)


GAUGE_GENERATORS = {
    # At B/E/F/H/I the selected S value is fixed across the canonical 14
    # states; these transpositions leave that exercised value fixed and only
    # exchange unused inputs.
    "B": (1, 0, 2),
    "E": (0, 2, 1),
    "F": (2, 1, 0),
    "H": (1, 0, 2),
    "I": (1, 0, 2),

    # C is different: S takes 0 and 2, but the primary symbol at physical C is
    # identical for depths 0 and 2 for every q and every raw primary payload.
    "C": (2, 1, 0),
}


def operation_maps(selected=(), *, a_swap=False):
    result = [IDENTITY] * 9
    if a_swap:
        result[SERIAL_ORDER.index("A")] = A_SWAP_01
    for letter in selected:
        result[SERIAL_ORDER.index(letter)] = GAUGE_GENERATORS[letter]
    return tuple(result)


def evaluate(candidates, local_maps):
    """Return exact survivor -> (first-pass tuple, terminal) mapping."""
    result = {}

    for index, (payload, selector) in enumerate(candidates):
        first = []
        valid = True

        for q in range(3):
            digits = []
            for col in range(3):
                dash_rows = []
                for row in range(3):
                    letter = PHYSICAL_LAYOUT[row][col]
                    j = SERIAL_ORDER.index(letter)
                    s = selector[j]
                    if frame_symbol(
                        payload,
                        q,
                        local_maps[j][s],
                        row,
                        col,
                    ) == "-":
                        dash_rows.append(row)
                if len(dash_rows) != 1:
                    valid = False
                    break
                digits.append(str(dash_rows[0]))
            if not valid:
                break
            first.append("".join(digits))

        if not valid:
            continue

        terminal_digits = []
        for col in range(3):
            dash_rows = []
            for row in range(3):
                letter = PHYSICAL_LAYOUT[row][col]
                j = SERIAL_ORDER.index(letter)
                s = selector[j]
                if frame_symbol(
                    payload,
                    s,
                    local_maps[j][s],
                    row,
                    col,
                ) == "-":
                    dash_rows.append(row)
            if len(dash_rows) != 1:
                valid = False
                break
            terminal_digits.append(str(dash_rows[0]))

        if valid:
            result[index] = (
                tuple(first),
                "".join(terminal_digits),
            )

    return result


def payload_key(payload):
    return tuple(sorted(payload.items()))


def selector_key_without_a(selector):
    return tuple(
        (j, selector[j])
        for j in range(1, 9)
    )


def main() -> None:
    rows = load_rows()
    candidates = raw_candidates(rows)

    canonical = evaluate(candidates, operation_maps())
    a_sibling = evaluate(candidates, operation_maps(a_swap=True))

    assert len(canonical) == 14
    assert len(a_sibling) == 14
    assert set(terminal for _first, terminal in canonical.values()) == {"100"}
    assert set(terminal for _first, terminal in a_sibling.values()) == {"100"}

    canonical_indices = frozenset(canonical)
    sibling_indices = frozenset(a_sibling)

    common = canonical_indices & sibling_indices
    removed = canonical_indices - sibling_indices
    added = sibling_indices - canonical_indices

    assert len(common) == 10
    assert len(removed) == 4
    assert len(added) == 4

    # Pair the four replaced states by identical primary payload and identical
    # selector everywhere except A.
    added_by_rest = {}
    for index in added:
        payload, selector = candidates[index]
        key = (
            payload_key(payload),
            selector_key_without_a(selector),
        )
        assert key not in added_by_rest
        added_by_rest[key] = index

    observed_residues = {
        int(record["residue"])
        for record in rows
    }
    assert 82 not in observed_residues
    assert 91 not in observed_residues

    paired = []
    for canonical_index in removed:
        payload, selector = candidates[canonical_index]
        key = (
            payload_key(payload),
            selector_key_without_a(selector),
        )
        sibling_index = added_by_rest[key]
        sibling_payload, sibling_selector = candidates[sibling_index]

        assert payload == sibling_payload
        assert selector[0] == 1
        assert sibling_selector[0] == 0
        assert all(
            selector[j] == sibling_selector[j]
            for j in range(1, 9)
        )

        # The functional machine output is exactly unchanged.
        assert canonical[canonical_index] == a_sibling[sibling_index]

        canonical_master = generate_master(payload, selector)
        sibling_master = generate_master(sibling_payload, sibling_selector)
        differences = [
            residue
            for residue, (left, right) in enumerate(
                zip(canonical_master, sibling_master),
                start=1,
            )
            if left != right
        ]
        assert differences == [82, 91]

        # The A transposition converts physical sibling S_A=0 back to effective
        # selected depth 1, matching the canonical state's S_A=1.
        assert IDENTITY[selector[0]] == 1
        assert A_SWAP_01[sibling_selector[0]] == 1

        paired.append((canonical_index, sibling_index))

    assert len(paired) == 4

    # The remaining second-pass source difference at A is q=1 -> q=0 while
    # selected depth remains 1. This source equality holds for every one of the
    # six raw-compatible primary payloads, not only the four paired states.
    unique_payloads = {
        payload_key(payload): payload
        for payload, _selector in candidates
    }
    assert len(unique_payloads) == 6

    a_row, a_col = PHYSICAL_POSITION["A"]
    for payload in unique_payloads.values():
        assert frame_symbol(payload, 0, 1, a_row, a_col) == frame_symbol(
            payload,
            1,
            1,
            a_row,
            a_col,
        )

    # Explain the 2^6 multiplicity of each invariant-100 route-max class from
    # Experiment 301. Every subset of these six local involutions leaves the
    # entire canonical survivor/output mapping unchanged.
    letters = tuple(GAUGE_GENERATORS)
    canonical_orbit = set()
    sibling_orbit = set()

    for bits in product((0, 1), repeat=len(letters)):
        selected = tuple(
            letter
            for letter, bit in zip(letters, bits)
            if bit
        )

        canonical_maps = operation_maps(selected)
        sibling_maps = operation_maps(selected, a_swap=True)

        assert evaluate(candidates, canonical_maps) == canonical
        assert evaluate(candidates, sibling_maps) == a_sibling

        canonical_orbit.add(canonical_maps)
        sibling_orbit.add(sibling_maps)

    assert len(canonical_orbit) == 64
    assert len(sibling_orbit) == 64
    assert canonical_orbit.isdisjoint(sibling_orbit)

    # Five generators are ordinary unused-input table gauges.
    fixed_support = {
        "B": {2},
        "E": {0},
        "F": {1},
        "H": {2},
        "I": {2},
    }
    for letter, expected_support in fixed_support.items():
        j = SERIAL_ORDER.index(letter)
        actual_support = {
            candidates[index][1][j]
            for index in canonical_indices
        }
        assert actual_support == expected_support
        mapping = GAUGE_GENERATORS[letter]
        assert all(mapping[value] == value for value in actual_support)

    # C:210 is the sixth independent bit. It swaps exercised depths 0<->2,
    # but those depths are symbol-identical at physical C for every q and every
    # raw primary payload.
    c_index = SERIAL_ORDER.index("C")
    c_support = {
        candidates[index][1][c_index]
        for index in canonical_indices
    }
    assert c_support == {0, 2}

    c_row, c_col = PHYSICAL_POSITION["C"]
    for payload in unique_payloads.values():
        for q in range(3):
            assert frame_symbol(payload, q, 0, c_row, c_col) == frame_symbol(
                payload,
                q,
                2,
                c_row,
                c_col,
            )

    print("Experiment 302")
    print("canonical / A-sibling overlap:", len(common), "/ 14")
    print("paired physical replacements:", len(paired))
    print("Q4 residues changed in every replacement: 82, 91")
    print("82 observed:", 82 in observed_residues)
    print("91 observed:", 91 in observed_residues)
    print("canonical operation-gauge orbit:", len(canonical_orbit))
    print("A-sibling operation-gauge orbit:", len(sibling_orbit))
    print("gauge generators:", sorted(GAUGE_GENERATORS))
    print("RESULT: each invariant-100 route-max class is exactly a 2^6 operation-gauge orbit")
    print("RESULT: five bits are unused selector-table entries; C:210 is an exact d0/d2 symbol equality")
    print("RESULT: A:102 changes only the unobserved A-stack representative for four states")
    print("RESULT: its first-pass depth is restored by the A transposition")
    print("RESULT: its residual second-pass q shift is hidden by the existing f1 q0/d1 = q1/d1 equality")
    print("RESULT: the Experiment-301 invariant-100 fork is a coupled gauge, not a new functional machine")


if __name__ == "__main__":
    main()

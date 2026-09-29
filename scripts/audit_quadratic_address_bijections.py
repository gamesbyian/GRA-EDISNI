#!/usr/bin/env python3
"""Experiment 303: exhaust quadratic bijections of the ternary address plane.

Earlier recursion audits broadened the canonical selector substitution through:

- independent coordinate permutations (Experiments 244/245/253);
- affine bijections of the joint (q,S) plane (Experiment 266);
- selector-fiber-preserving nonlinear bijections (Experiments 268/269).

This experiment tests a different global algebraic family: every coordinate is
an arbitrary polynomial of total degree <= 2 over F3,

    q' = P(q,S)
    d' = Q(q,S)

with basis

    1, q, S, q^2, qS, S^2.

There are 3^6 = 729 coordinate functions and 729^2 = 531,441 ordered pairs.
Exactly 3,888 induce bijections of the 9-point address plane. Of those, 432
are affine and 3,456 are genuinely quadratic in this canonical basis.

The SAME map F(q,S) is reused on both passes:

    first pass:  B(F(q,S(j)), j)
    second pass: B(F(S(j),S(j)), j)

Parent machine space:
    all 216 raw-compatible primary x Q4 candidates from Experiment 250.

Acceptance:
    all three first-pass surfaces and the reused-operation second-pass surface
    must decode as dash-POS3.

Model-selection bookkeeping:
    * retained raw-machine count;
    * terminal cardinality;
    * distinct first-pass functional families;
    * Experiment-278 reversible three-route criterion.

No target state count, expected terminal, expected route words, or canonical
master set is used as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)


BASIS_POINTS = tuple((q, s) for q in range(3) for s in range(3))
ADDRESS_PAIRS = BASIS_POINTS
IDENTITY_OUTPUTS = tuple(range(9))
Q_SWAP_01_OUTPUTS = (3, 4, 5, 0, 1, 2, 6, 7, 8)


def poly_value(coeff, q, s):
    c0, cq, cs, cqq, cqs, css = coeff
    return (
        c0
        + cq * q
        + cs * s
        + cqq * q * q
        + cqs * q * s
        + css * s * s
    ) % 3


def polynomial_functions():
    result = []
    for coeff in product(range(3), repeat=6):
        values = tuple(
            poly_value(coeff, q, s)
            for q, s in BASIS_POINTS
        )
        result.append((values, coeff))
    assert len(result) == 729
    assert len({values for values, _coeff in result}) == 729
    return tuple(result)


def polynomial_degree(coeff):
    if any(coeff[index] for index in (3, 4, 5)):
        return 2
    if any(coeff[index] for index in (1, 2)):
        return 1
    return 0


def quadratic_bijections(functions):
    result = []
    for q_values, q_coeff in functions:
        for d_values, d_coeff in functions:
            outputs = tuple(
                3 * q_values[index] + d_values[index]
                for index in range(9)
            )
            if len(set(outputs)) == 9:
                result.append((outputs, q_coeff, d_coeff))
    assert len(result) == 3888
    return tuple(result)


def raw_candidates(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    candidates = [
        (payload, selector)
        for payload in payloads
        for selector in selectors
    ]
    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(candidates) == 216
    return candidates


def physical_columns():
    return tuple(
        tuple(
            SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col])
            for row in range(3)
        )
        for col in range(3)
    )


def precompute_symbols(candidates):
    symbols = []
    selectors = []

    for payload, selector in candidates:
        machine = [
            [
                [None] * 9
                for _d in range(3)
            ]
            for _q in range(3)
        ]
        for q in range(3):
            for d in range(3):
                for j, letter in enumerate(SERIAL_ORDER):
                    row, col = PHYSICAL_POSITION[letter]
                    machine[q][d][j] = frame_symbol(
                        payload,
                        q,
                        d,
                        row,
                        col,
                    )
        symbols.append(machine)
        selectors.append(tuple(selector[j] for j in range(9)))

    return tuple(symbols), tuple(selectors)


def row_signature_tables(symbols, selectors):
    """Decode every possible map S -> one of 9 addresses.

    A row key contains three output-address indices, one for S=0/1/2.
    The same decoder is usable for each external-q first-pass row and for the
    diagonal second-pass input triple.
    """
    columns = physical_columns()
    words = {}
    valid_masks = {}

    for key in product(range(9), repeat=3):
        decoded = [None] * len(symbols)
        mask = 0

        for index, machine in enumerate(symbols):
            selector = selectors[index]
            digits = []
            valid = True

            for js in columns:
                dash_rows = []
                for row, j in enumerate(js):
                    output_index = key[selector[j]]
                    q, d = ADDRESS_PAIRS[output_index]
                    if machine[q][d][j] == "-":
                        dash_rows.append(row)

                if len(dash_rows) != 1:
                    valid = False
                    break
                digits.append(str(dash_rows[0]))

            if valid:
                decoded[index] = "".join(digits)
                mask |= 1 << index

        words[key] = tuple(decoded)
        valid_masks[key] = mask

    assert len(words) == 729
    return words, valid_masks


def set_bits(mask):
    while mask:
        low = mask & -mask
        index = low.bit_length() - 1
        yield index
        mask ^= low


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    if len(families) != 3:
        return []

    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(
            families[index][choices[index]]
            for index in range(3)
        )
        if not all(is_permutation(word) for word in routes):
            continue
        if len(set(routes)) != 3:
            continue
        result.append((choices, routes))
    return result


def evaluate_map(outputs, words, valid_masks):
    row0 = outputs[0:3]
    row1 = outputs[3:6]
    row2 = outputs[6:9]
    diagonal = (outputs[0], outputs[4], outputs[8])

    survivor_mask = (
        valid_masks[row0]
        & valid_masks[row1]
        & valid_masks[row2]
        & valid_masks[diagonal]
    )
    indices = tuple(set_bits(survivor_mask))

    families = {
        (
            words[row0][index],
            words[row1][index],
            words[row2][index],
        )
        for index in indices
    }
    terminals = Counter(
        words[diagonal][index]
        for index in indices
    )

    return (
        survivor_mask,
        frozenset(families),
        terminals,
        route_shells(families),
    )


def main() -> None:
    candidates = raw_candidates(load_rows())
    symbols, selectors = precompute_symbols(candidates)
    words, valid_masks = row_signature_tables(symbols, selectors)

    functions = polynomial_functions()
    bijections = quadratic_bijections(functions)

    degree_counts = Counter(
        max(polynomial_degree(q_coeff), polynomial_degree(d_coeff))
        for _outputs, q_coeff, d_coeff in bijections
    )
    assert degree_counts == Counter({1: 432, 2: 3456})

    outcomes = []
    for outputs, q_coeff, d_coeff in bijections:
        survivor_mask, families, terminals, shells = evaluate_map(
            outputs,
            words,
            valid_masks,
        )
        outcomes.append({
            "outputs": outputs,
            "q_coeff": q_coeff,
            "d_coeff": d_coeff,
            "degree": max(
                polynomial_degree(q_coeff),
                polynomial_degree(d_coeff),
            ),
            "survivor_mask": survivor_mask,
            "states": survivor_mask.bit_count(),
            "families": families,
            "terminals": terminals,
            "shells": shells,
        })

    assert len(outcomes) == 3888

    distribution_by_degree = {
        degree: Counter(
            (item["states"], len(item["terminals"]))
            for item in outcomes
            if item["degree"] == degree
        )
        for degree in (1, 2)
    }

    assert distribution_by_degree[1] == Counter({
        (0, 0): 411,
        (1, 1): 1,
        (5, 1): 4,
        (5, 2): 5,
        (7, 1): 3,
        (7, 2): 2,
        (8, 2): 1,
        (8, 3): 1,
        (10, 1): 3,
        (14, 1): 1,
    })
    assert distribution_by_degree[2] == Counter({
        (0, 0): 3312,
        (1, 1): 1,
        (2, 1): 24,
        (3, 1): 11,
        (3, 2): 10,
        (4, 1): 4,
        (4, 2): 6,
        (4, 3): 2,
        (5, 1): 10,
        (5, 2): 14,
        (6, 1): 8,
        (6, 2): 11,
        (6, 3): 4,
        (7, 1): 6,
        (7, 2): 5,
        (7, 3): 2,
        (8, 1): 2,
        (8, 2): 4,
        (8, 3): 1,
        (9, 1): 2,
        (9, 2): 1,
        (9, 3): 1,
        (10, 1): 8,
        (10, 2): 2,
        (12, 1): 1,
        (12, 2): 1,
        (12, 3): 1,
        (13, 3): 1,
        (18, 1): 1,
    })

    nonempty = [item for item in outcomes if item["states"]]
    assert len(nonempty) == 165
    assert Counter(item["degree"] for item in nonempty) == Counter({
        1: 21,
        2: 144,
    })

    invariant = [
        item for item in nonempty
        if len(item["terminals"]) == 1
    ]
    assert len(invariant) == 90
    assert Counter(item["degree"] for item in invariant) == Counter({
        1: 12,
        2: 78,
    })

    canonical = next(
        item for item in outcomes
        if item["outputs"] == IDENTITY_OUTPUTS
    )
    assert canonical["states"] == 14
    assert canonical["terminals"] == Counter({"100": 14})
    assert canonical["shells"] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    # The global retention winner is a genuinely quadratic 18-state machine
    # with invariant terminal 102. It has only two functional families and no
    # three-route shell.
    maximum_states = max(item["states"] for item in outcomes)
    assert maximum_states == 18
    maxima = [
        item for item in outcomes
        if item["states"] == maximum_states
    ]
    assert len(maxima) == 1
    quadratic_sibling = maxima[0]
    assert quadratic_sibling["degree"] == 2
    assert quadratic_sibling["q_coeff"] == (1, 1, 0, 0, 0, 0)
    assert quadratic_sibling["d_coeff"] == (1, 2, 1, 1, 0, 0)
    assert quadratic_sibling["terminals"] == Counter({"102": 18})
    assert quadratic_sibling["families"] == frozenset({
        ("212", "102", "102"),
        ("212", "122", "102"),
    })
    assert not quadratic_sibling["shells"]

    # Across all 3,888 quadratic bijections, only two retain the independently
    # derived reversible three-route structure. Neither is genuinely quadratic.
    route_capable = [
        item for item in outcomes
        if item["shells"]
    ]
    assert len(route_capable) == 2
    assert all(item["degree"] == 1 for item in route_capable)

    route_summary = {
        item["outputs"]: (
            item["states"],
            item["terminals"],
            item["shells"],
        )
        for item in route_capable
    }
    assert route_summary == {
        IDENTITY_OUTPUTS: (
            14,
            Counter({"100": 14}),
            [((2, 1, 0), ("120", "012", "102"))],
        ),
        Q_SWAP_01_OUTPUTS: (
            7,
            Counter({"100": 7}),
            [((2, 0, 1), ("120", "012", "102"))],
        ),
    }

    assert canonical["states"] == max(
        item["states"] for item in route_capable
    )

    genuinely_quadratic_route = [
        item
        for item in route_capable
        if item["degree"] == 2
    ]
    assert not genuinely_quadratic_route

    print("Experiment 303")
    print("quadratic coordinate functions:", len(functions))
    print("quadratic coordinate-map pairs:", len(functions) ** 2)
    print("bijective address maps:", len(bijections))
    print("affine / genuinely quadratic bijections:", dict(sorted(degree_counts.items())))
    print("bijections with any recursively closed raw machine:", len(nonempty))
    print("bijections with invariant terminal:", len(invariant))
    print("maximum retained raw states:", maximum_states)
    print("maximum-retention sibling terminal:", dict(quadratic_sibling["terminals"]))
    print("maximum-retention sibling families:", sorted(quadratic_sibling["families"]))
    print("route-capable bijections:", len(route_capable))
    print("route-capable state counts:", sorted(item["states"] for item in route_capable))
    print("genuinely quadratic route-capable bijections:", len(genuinely_quadratic_route))
    print("RESULT: raw-state retention alone prefers an 18-state quadratic sibling")
    print("RESULT: that sibling collapses the intermediate computation to two route-degenerate families")
    print("RESULT: no genuinely quadratic bijection preserves the reversible route layer")
    print("RESULT: canonical uniquely maximizes retention among all route-capable quadratic bijections")


if __name__ == "__main__":
    main()

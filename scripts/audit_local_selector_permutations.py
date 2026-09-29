#!/usr/bin/env python3
"""Experiment 311: exhaust arbitrary cell-local selector permutations.

Experiment 310 closed the family of cyclic local depth offsets reused on both
passes. This experiment broadens each cell from the three cyclic shifts to ALL
six permutations of the selector value.

At each physical A-I cell choose independently:

    g_j in S3
    F_j(q, S) = (q, g_j(S))

and reuse the same F_j on both passes:

    first pass:  F_j(q, S(j))
    second pass: F_j(S(j), S(j))

Family size:
    6^9 = 10,077,696 local same-operation rules.

The enumeration is exact but quotient-compressed by physical column. Each
column has 6^3 = 216 local permutation triples. Collapsing those triples by
their exact 216-candidate q0/q1/q2/terminal signature leaves only:

    24 x 216 x 17 = 88,128

column-signature combinations, with multiplicities preserving the full 6^9
physical operation count.

Parent machine space:
    all 216 raw-compatible primary x Q4 candidates from Experiment 250.

Acceptance:
    all three first-pass surfaces and the reused-operation terminal surface
    decode as dash-POS3.

Model-selection bookkeeping:
    retained raw-machine count, terminal cardinality, distinct first-pass
    functional families, and the Experiment-278 reversible route criterion.

No target state count, terminal value, expected physical family, route words,
or operation identity is used as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product

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


PERMS = tuple(permutations(range(3)))
IDENTITY = (0, 1, 2)
A_SWAP_01 = (1, 0, 2)
D_SWAP_02 = (2, 1, 0)


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


def physical_columns():
    return tuple(
        tuple(
            SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col])
            for row in range(3)
        )
        for col in range(3)
    )


def raw_candidates(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    result = [
        (payload, selector)
        for payload in payloads
        for selector in selectors
    ]
    assert len(result) == 216
    return result


def column_signature(candidates, js, local_perms):
    """Per candidate: q0,q1,q2,terminal row digits; 3 marks invalid."""
    result = []

    for payload, selector in candidates:
        digits = []

        for q in range(3):
            dash_rows = []
            for row, (j, mapping) in enumerate(zip(js, local_perms)):
                physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
                s = selector[j]
                if frame_symbol(
                    payload,
                    q,
                    mapping[s],
                    physical_row,
                    physical_col,
                ) == "-":
                    dash_rows.append(row)
            digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        dash_rows = []
        for row, (j, mapping) in enumerate(zip(js, local_perms)):
            physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            s = selector[j]
            if frame_symbol(
                payload,
                s,
                mapping[s],
                physical_row,
                physical_col,
            ) == "-":
                dash_rows.append(row)
        digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        result.append(tuple(digits))

    return tuple(result)


def signature_counts(candidates, js):
    result = Counter()
    for local_perms in product(PERMS, repeat=3):
        result[column_signature(candidates, js, local_perms)] += 1
    assert sum(result.values()) == 6 ** 3
    return result


def direct_evaluate(candidates, local_maps):
    """Evaluate one explicit 9-cell operation for route-class representatives."""
    survivors = []
    families = set()
    terminals = []

    for index, (payload, selector) in enumerate(candidates):
        words = []
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
            words.append("".join(digits))

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

        if not valid:
            continue

        first = tuple(words)
        terminal = "".join(terminal_digits)
        survivors.append(index)
        families.add(first)
        terminals.append(terminal)

    return (
        frozenset(survivors),
        frozenset(families),
        Counter(terminals),
        route_shells(families),
    )


def representative_maps(*changes):
    result = [IDENTITY] * 9
    for letter, mapping in changes:
        result[SERIAL_ORDER.index(letter)] = mapping
    return tuple(result)


def main() -> None:
    candidates = raw_candidates(load_rows())
    columns = physical_columns()

    per_column = [
        signature_counts(candidates, js)
        for js in columns
    ]

    assert [len(counts) for counts in per_column] == [24, 216, 17]

    distribution = Counter()
    route_state_distribution = Counter()
    route_state_terminal_cardinality = Counter()
    route_max_classes = Counter()

    total_operations = 0
    route_operations = 0
    maximum_states = -1
    maximum_operations = 0
    maximum_route_states = -1
    maximum_route_operations = 0

    canonical = direct_evaluate(
        candidates,
        representative_maps(),
    )
    canonical_survivors = canonical[0]
    assert len(canonical_survivors) == 14
    assert canonical[2] == Counter({"100": 14})
    assert canonical[3] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    exact_canonical_operations = 0
    exact_canonical_route_operations = 0
    exact_canonical_terminal_profiles = Counter()

    for sig0, count0 in per_column[0].items():
        for sig1, count1 in per_column[1].items():
            for sig2, count2 in per_column[2].items():
                multiplicity = count0 * count1 * count2
                total_operations += multiplicity

                survivors = []
                families = set()
                terminals = []

                for index in range(len(candidates)):
                    column_sigs = (sig0[index], sig1[index], sig2[index])
                    if any(3 in sig for sig in column_sigs):
                        continue

                    first = tuple(
                        "".join(str(sig[q]) for sig in column_sigs)
                        for q in range(3)
                    )
                    terminal = "".join(
                        str(sig[3])
                        for sig in column_sigs
                    )

                    survivors.append(index)
                    families.add(first)
                    terminals.append(terminal)

                states = len(survivors)
                terminal_counts = Counter(terminals)
                terminal_cardinality = len(terminal_counts)
                survivor_set = frozenset(survivors)
                shells = route_shells(families)

                distribution[(states, terminal_cardinality)] += multiplicity

                if states > maximum_states:
                    maximum_states = states
                    maximum_operations = multiplicity
                elif states == maximum_states:
                    maximum_operations += multiplicity

                if shells:
                    route_operations += multiplicity
                    route_state_distribution[states] += multiplicity
                    route_state_terminal_cardinality[
                        (states, terminal_cardinality)
                    ] += multiplicity

                    if states > maximum_route_states:
                        maximum_route_states = states
                        maximum_route_operations = multiplicity
                    elif states == maximum_route_states:
                        maximum_route_operations += multiplicity

                    if states == 14:
                        route_max_classes[(
                            survivor_set,
                            tuple(sorted(terminal_counts.items())),
                            tuple(sorted(families)),
                            tuple(shells),
                        )] += multiplicity

                if survivor_set == canonical_survivors:
                    exact_canonical_operations += multiplicity
                    if shells:
                        exact_canonical_route_operations += multiplicity
                    exact_canonical_terminal_profiles[
                        tuple(sorted(terminal_counts.items()))
                    ] += multiplicity

    assert total_operations == 6 ** 9 == 10_077_696
    assert [len(counts) for counts in per_column] == [24, 216, 17]
    assert 24 * 216 * 17 == 88_128

    assert maximum_states == 22
    assert maximum_operations == 384

    assert route_operations == 5_760
    assert route_state_distribution == Counter({
        4: 640,
        5: 1_408,
        6: 1_280,
        7: 512,
        8: 320,
        10: 704,
        12: 640,
        14: 256,
    })
    assert maximum_route_states == 14
    assert maximum_route_operations == 256

    # Four observational route-max classes remain, each represented by 64
    # physical local maps. The explicit representatives below reveal their
    # simplest member.
    assert len(route_max_classes) == 4
    assert set(route_max_classes.values()) == {64}

    canonical_rep = direct_evaluate(
        candidates,
        representative_maps(),
    )
    a_swap_rep = direct_evaluate(
        candidates,
        representative_maps(("A", A_SWAP_01)),
    )
    d_swap_rep = direct_evaluate(
        candidates,
        representative_maps(("D", D_SWAP_02)),
    )
    ad_swap_rep = direct_evaluate(
        candidates,
        representative_maps(
            ("A", A_SWAP_01),
            ("D", D_SWAP_02),
        ),
    )

    representative_results = {
        "canonical": canonical_rep,
        "A:102": a_swap_rep,
        "D:210": d_swap_rep,
        "A:102+D:210": ad_swap_rep,
    }

    representative_keys = {
        (
            result[0],
            tuple(sorted(result[2].items())),
            tuple(sorted(result[1])),
            tuple(result[3]),
        )
        for result in representative_results.values()
    }
    assert representative_keys == set(route_max_classes)

    # The A-only transposition is the important near-rival: it keeps the same
    # 14-state count, invariant 100, same functional families, and same route
    # shell, but swaps four physical raw-compatible states.
    assert len(a_swap_rep[0]) == 14
    assert len(a_swap_rep[0] & canonical_survivors) == 10
    assert a_swap_rep[2] == Counter({"100": 14})
    assert a_swap_rep[1] == canonical_rep[1]
    assert a_swap_rep[3] == canonical_rep[3]

    # D-only and A+D representatives retain 14 but change both terminal profile
    # and the route family.
    assert d_swap_rep[2] == Counter({"100": 10, "110": 4})
    assert ad_swap_rep[2] == Counter({"100": 10, "110": 4})
    assert len(d_swap_rep[0] & canonical_survivors) == 10
    assert len(ad_swap_rep[0] & canonical_survivors) == 6

    assert exact_canonical_operations == 192
    assert exact_canonical_route_operations == 64
    assert exact_canonical_terminal_profiles == Counter({
        (("102", 14),): 128,
        (("100", 14),): 64,
    })

    print("Experiment 311")
    print("arbitrary local selector-permutation family:", total_operations)
    print("exact signature quotient:", [len(x) for x in per_column])
    print("quotient combinations evaluated:", 24 * 216 * 17)
    print("maximum retained raw states:", maximum_states)
    print("operations attaining global maximum:", maximum_operations)
    print("route-capable physical operations:", route_operations)
    print("route-capable state distribution:", dict(sorted(route_state_distribution.items())))
    print("maximum route-capable states:", maximum_route_states)
    print("operations attaining route maximum:", maximum_route_operations)
    print("route-max equivalence classes:", len(route_max_classes))
    print("route-max class multiplicities:", sorted(route_max_classes.values()))
    print("exact canonical physical-family operations:", exact_canonical_operations)
    print("exact canonical + route operations:", exact_canonical_route_operations)
    print("A:102 overlap with canonical:", len(a_swap_rep[0] & canonical_survivors), "/ 14")
    print("RESULT: arbitrary local S3 relabeling breaks strict uniqueness at the 14-state route maximum")
    print("RESULT: the nearest invariant-100 rival is one A-cell transposition, A:102")
    print("RESULT: A:102 preserves the same functional families and route shell while replacing four raw-compatible states")
    print("RESULT: canonical remains the unique zero-exception / globally uniform representative")
    print("RESULT: this residual fork must be classified as local-label gauge or simplicity choice, not observation-forced uniqueness")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 305: exhaust every bijection of the nine ternary addresses.

Experiment 303 closes degree<=2 polynomial bijections. This experiment removes
the algebraic restriction entirely.

The ternary address plane has nine cells:

    (q,d) in F3 x F3.

Enumerate every one of its 9! = 362,880 permutations F. Reuse the SAME F on
both recursive passes:

    first pass:  B(F(q,S(j)), j)
    second pass: B(F(S(j),S(j)), j)

Parent machine space:
    all 216 raw-compatible primary x Q4 candidates from Experiment 250.

Acceptance:
    all three first-pass surfaces and the reused-operation terminal surface
    decode as dash-POS3.

For every operation record:
    * retained raw-machine count;
    * terminal cardinality;
    * distinct first-pass functional families;
    * Experiment-278 reversible three-route criterion.

No polynomial form, target state count, expected terminal, expected route,
canonical master set, or preferred operation is used as a filter.

This is the complete carrier-preserving global address-relabel family.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations

from audit_quadratic_address_bijections import (
    IDENTITY_OUTPUTS,
    precompute_symbols,
    raw_candidates,
    route_shells,
    row_signature_tables,
    set_bits,
)
from enumerate_raw_machine import load_rows


F1_GAUGE_OUTPUTS = (0, 4, 2, 3, 1, 5, 6, 7, 8)


def main() -> None:
    candidates = raw_candidates(load_rows())
    symbols, selectors = precompute_symbols(candidates)
    words, valid_masks = row_signature_tables(symbols, selectors)

    total = 0
    nonempty = 0
    invariant_terminal = 0

    distribution = Counter()
    route_state_distribution = Counter()
    route_terminal_distribution = Counter()
    route_capable = []

    maximum_states = -1
    maximum_maps = []

    for outputs in permutations(range(9)):
        total += 1

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
        states = survivor_mask.bit_count()

        if not states:
            distribution[(0, 0)] += 1
            continue

        nonempty += 1
        indices = tuple(set_bits(survivor_mask))
        terminals = Counter(
            words[diagonal][index]
            for index in indices
        )
        terminal_cardinality = len(terminals)
        distribution[(states, terminal_cardinality)] += 1

        if terminal_cardinality == 1:
            invariant_terminal += 1

        if states > maximum_states:
            maximum_states = states
            maximum_maps = [(outputs, survivor_mask, terminals)]
        elif states == maximum_states:
            maximum_maps.append((outputs, survivor_mask, terminals))

        families = {
            (
                words[row0][index],
                words[row1][index],
                words[row2][index],
            )
            for index in indices
        }
        shells = route_shells(families)
        if not shells:
            continue

        route_capable.append({
            "outputs": outputs,
            "survivor_mask": survivor_mask,
            "states": states,
            "families": frozenset(families),
            "terminals": terminals,
            "shells": shells,
        })
        route_state_distribution[states] += 1
        route_terminal_distribution[(states, terminal_cardinality)] += 1

    assert total == 362_880
    assert nonempty == 11_166
    assert invariant_terminal == 6_786

    # Raw-state retention alone is again misleading. One bijection retains 32
    # states, but its three functional families have no reversible route shell.
    assert maximum_states == 32
    assert len(maximum_maps) == 1
    maximum_outputs, maximum_mask, maximum_terminals = maximum_maps[0]
    assert maximum_outputs == (0, 5, 3, 4, 1, 8, 7, 6, 2)
    assert maximum_terminals == Counter({
        "102": 16,
        "122": 10,
        "112": 6,
    })

    maximum_indices = tuple(set_bits(maximum_mask))
    max_row0 = maximum_outputs[0:3]
    max_row1 = maximum_outputs[3:6]
    max_row2 = maximum_outputs[6:9]
    maximum_families = {
        (
            words[max_row0][index],
            words[max_row1][index],
            words[max_row2][index],
        )
        for index in maximum_indices
    }
    assert maximum_families == {
        ("212", "100", "102"),
        ("212", "100", "112"),
        ("212", "100", "122"),
    }
    assert not route_shells(maximum_families)

    # The route criterion is highly selective over the full symmetric group.
    assert len(route_capable) == 30
    assert route_state_distribution == Counter({
        3: 3,
        4: 1,
        5: 3,
        6: 11,
        7: 6,
        8: 1,
        9: 1,
        12: 2,
        14: 2,
    })

    maximum_route_states = max(
        item["states"]
        for item in route_capable
    )
    assert maximum_route_states == 14

    route_maxima = [
        item
        for item in route_capable
        if item["states"] == maximum_route_states
    ]
    assert len(route_maxima) == 2
    assert {
        item["outputs"]
        for item in route_maxima
    } == {
        IDENTITY_OUTPUTS,
        F1_GAUGE_OUTPUTS,
    }

    canonical = next(
        item
        for item in route_maxima
        if item["outputs"] == IDENTITY_OUTPUTS
    )
    f1_gauge = next(
        item
        for item in route_maxima
        if item["outputs"] == F1_GAUGE_OUTPUTS
    )

    expected_families = frozenset({
        ("102", "002", "120"),
        ("102", "012", "100"),
        ("102", "022", "100"),
    })
    expected_shell = [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    assert canonical["survivor_mask"] == f1_gauge["survivor_mask"]
    assert canonical["families"] == expected_families
    assert f1_gauge["families"] == expected_families
    assert canonical["terminals"] == Counter({"100": 14})
    assert f1_gauge["terminals"] == Counter({"100": 14})
    assert canonical["shells"] == expected_shell
    assert f1_gauge["shells"] == expected_shell

    # The only co-maximal bijection is exactly the known f1 gauge:
    # swap q=0 and q=1 only on the d/S=1 fiber.
    differences = [
        index
        for index, (left, right) in enumerate(
            zip(IDENTITY_OUTPUTS, F1_GAUGE_OUTPUTS)
        )
        if left != right
    ]
    assert differences == [1, 4]
    assert F1_GAUGE_OUTPUTS[1] == 4   # (0,1) -> (1,1)
    assert F1_GAUGE_OUTPUTS[4] == 1   # (1,1) -> (0,1)

    print("Experiment 305")
    print("all global address bijections:", total)
    print("bijections with any recursively closed raw machine:", nonempty)
    print("bijections with invariant terminal:", invariant_terminal)
    print("unrestricted maximum retained states:", maximum_states)
    print("route-capable bijections:", len(route_capable))
    print("route-capable state distribution:", dict(sorted(route_state_distribution.items())))
    print("maximum route-capable states:", maximum_route_states)
    print("route-maximal bijections:", len(route_maxima))
    print("route-maximal representatives: identity, f1 gauge")
    print("RESULT: raw retention alone prefers a unique 32-state route-degenerate permutation")
    print("RESULT: reversible routing cuts the complete 9! carrier-preserving family to 30 candidates")
    print("RESULT: only identity and the known f1 equality gauge retain 14 routed states")
    print("RESULT: those two are behaviorally identical on all 14 legal states")
    print("RESULT: modulo the independently explained f1 gauge, canonical is unique among every global address bijection")


if __name__ == "__main__":
    main()

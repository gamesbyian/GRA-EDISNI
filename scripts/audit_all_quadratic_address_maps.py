#!/usr/bin/env python3
"""Experiment 304: drop bijectivity in the quadratic address family.

Experiment 303 searches the 3,888 bijections among all degree<=2 polynomial
maps F3^2 -> F3^2. This negative control removes the bijectivity restriction
and enumerates every one of the 729^2 = 531,441 quadratic coordinate-map pairs.

The purpose is not to advocate singular address maps. Experiment 267 already
showed that unrestricted retention can be gamed by information-destroying
affine maps. Here we ask a sharper question:

    does the independently derived reversible three-route criterion itself
    eliminate non-bijective quadratic maps, or is preservation of the full
    nine-address carrier still doing real work?

The same global map F(q,S) is reused on both passes. Parent machine space,
POS3 closure, and route criterion are exactly the same as Experiment 303.
"""

from __future__ import annotations

from collections import Counter

from audit_quadratic_address_bijections import (
    IDENTITY_OUTPUTS,
    Q_SWAP_01_OUTPUTS,
    polynomial_functions,
    precompute_symbols,
    raw_candidates,
    row_signature_tables,
    route_shells,
    set_bits,
)
from enumerate_raw_machine import load_rows


def main() -> None:
    candidates = raw_candidates(load_rows())
    symbols, selectors = precompute_symbols(candidates)
    words, valid_masks = row_signature_tables(symbols, selectors)
    functions = polynomial_functions()

    total_maps = 0
    nonempty_maps = 0
    maximum_states = -1
    maximum_maps = []

    route_maps = []
    route_image_distribution = Counter()
    route_state_distribution = Counter()
    route_terminal_cardinality = Counter()

    for q_values, q_coeff in functions:
        for d_values, d_coeff in functions:
            total_maps += 1
            outputs = tuple(
                3 * q_values[index] + d_values[index]
                for index in range(9)
            )

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

            if states > maximum_states:
                maximum_states = states
                maximum_maps = [(outputs, q_coeff, d_coeff, survivor_mask)]
            elif states == maximum_states:
                maximum_maps.append((outputs, q_coeff, d_coeff, survivor_mask))

            if not states:
                continue

            nonempty_maps += 1
            indices = tuple(set_bits(survivor_mask))
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

            terminals = Counter(
                words[diagonal][index]
                for index in indices
            )
            image_size = len(set(outputs))

            route_maps.append({
                "outputs": outputs,
                "q_coeff": q_coeff,
                "d_coeff": d_coeff,
                "states": states,
                "families": frozenset(families),
                "terminals": terminals,
                "shells": shells,
                "image_size": image_size,
            })
            route_image_distribution[image_size] += 1
            route_state_distribution[states] += 1
            route_terminal_cardinality[(states, len(terminals))] += 1

    assert total_maps == 531_441
    assert nonempty_maps == 34_288

    # Unrestricted retention is badly gamed. Eight singular maps retain all 216
    # raw candidates; six are constant address maps and two have image size 2.
    assert maximum_states == 216
    assert len(maximum_maps) == 8
    assert Counter(
        len(set(outputs))
        for outputs, _q_coeff, _d_coeff, _mask in maximum_maps
    ) == Counter({1: 6, 2: 2})

    # Reversible routing is highly selective but does NOT by itself imply a
    # full nine-address map.
    assert len(route_maps) == 38
    assert route_image_distribution == Counter({
        5: 12,
        6: 16,
        7: 8,
        9: 2,
    })
    assert route_state_distribution == Counter({
        3: 1,
        5: 1,
        6: 5,
        7: 1,
        8: 5,
        10: 12,
        12: 6,
        14: 1,
        20: 6,
    })

    invariant_route_maps = [
        item
        for item in route_maps
        if len(item["terminals"]) == 1
    ]
    assert len(invariant_route_maps) == 13

    # Six singular maps beat canonical raw-state retention while preserving a
    # reversible three-route shell. Every one collapses the nine address cells
    # to only five outputs.
    maximum_route_states = max(item["states"] for item in route_maps)
    assert maximum_route_states == 20
    route_maxima = [
        item
        for item in route_maps
        if item["states"] == maximum_route_states
    ]
    assert len(route_maxima) == 6
    assert {item["image_size"] for item in route_maxima} == {5}
    assert Counter(len(item["terminals"]) for item in route_maxima) == Counter({
        1: 2,
        2: 2,
        3: 2,
    })

    # Full carrier preservation is the exact separator. Among all 531,441
    # degree<=2 maps, only two route-capable maps use all nine addresses:
    # canonical identity (14 states) and one q-label transposition (7 states).
    full_image_route = [
        item
        for item in route_maps
        if item["image_size"] == 9
    ]
    assert len(full_image_route) == 2

    full_image_summary = {
        item["outputs"]: (
            item["states"],
            item["terminals"],
            item["shells"],
        )
        for item in full_image_route
    }
    assert full_image_summary == {
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

    canonical = next(
        item for item in full_image_route
        if item["outputs"] == IDENTITY_OUTPUTS
    )
    assert canonical["states"] == max(
        item["states"] for item in full_image_route
    )

    print("Experiment 304")
    print("all quadratic coordinate-map pairs:", total_maps)
    print("maps with any recursively closed raw machine:", nonempty_maps)
    print("unrestricted maximum retained states:", maximum_states)
    print("maps attaining unrestricted maximum:", len(maximum_maps))
    print("route-capable maps:", len(route_maps))
    print("route-capable image-size distribution:", dict(sorted(route_image_distribution.items())))
    print("route-capable state distribution:", dict(sorted(route_state_distribution.items())))
    print("route-capable maps with invariant terminal:", len(invariant_route_maps))
    print("maximum route-capable states without carrier preservation:", maximum_route_states)
    print("singular route maxima:", len(route_maxima))
    print("address image size of every route maximum:", 5)
    print("route-capable maps preserving all nine addresses:", len(full_image_route))
    print("full-image route state counts:", sorted(item["states"] for item in full_image_route))
    print("RESULT: reversible routing alone does not prevent singular quadratic maps from gaming retention")
    print("RESULT: six five-address maps retain 20 routed states, beating canonical 14")
    print("RESULT: preserving the full nine-address carrier reduces the entire 531,441-map family to two routed candidates")
    print("RESULT: canonical uniquely maximizes retention among those full-carrier routed maps")


if __name__ == "__main__":
    main()

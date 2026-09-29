#!/usr/bin/env python3
"""Experiment 278: derive the Q3 route-shell orientation.

Start from the three first-pass functional output families reconstructed from
raw constraints. Do not assume the existing route reindex q=2-p.

For each functional family choose one of its three q-indexed ternary outputs.
There are 3^3 = 27 possible choice triples.

Minimal route-shell criterion:
  * every selected ternary word is a permutation of 0,1,2 (a reversible route);
  * the three functional classes select three distinct route maps.

No expected route words, q choices, cycle types, or q=2-p formula are used as
filters.
"""

from __future__ import annotations

from itertools import product

from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    terminal_surface,
)


def is_permutation(word: str) -> bool:
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    final_survivors = []
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue

            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue
            final_survivors.append((payload, selector, first, terminal))

    assert len(final_survivors) == 14
    families = tuple(sorted({item[2] for item in final_survivors}))
    assert families == (
        ("102", "002", "120"),
        ("102", "012", "100"),
        ("102", "022", "100"),
    )

    candidates = []
    for choices in product(range(3), repeat=3):
        routes = tuple(
            families[family_index][choices[family_index]]
            for family_index in range(3)
        )
        if not all(is_permutation(route) for route in routes):
            continue
        if len(set(routes)) != 3:
            continue
        candidates.append((choices, routes))

    assert candidates == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    choices, routes = candidates[0]
    cycle_fixed_points = tuple(
        sum(int(route[i]) == i for i in range(3))
        for route in routes
    )
    assert cycle_fixed_points == (0, 3, 1)

    print("Experiment 278")
    print("first-pass functional families:")
    for family in families:
        print(" ", family)
    print("route-choice assignments tested:", 27)
    print("distinct all-permutation route shells:", len(candidates))
    print("unique q choices:", choices)
    print("unique route shell:", routes)
    print("fixed-point counts:", cycle_fixed_points)
    print("RESULT: reversible + distinct route maps uniquely select q choices (2,1,0)")
    print("RESULT: q=2-p and route shell 120/012/102 are derived inside this bounded family")
    print("RESULT: the resulting shell contains one derangement, identity, and transposition")


if __name__ == "__main__":
    main()

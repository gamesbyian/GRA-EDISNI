#!/usr/bin/env python3
"""Experiment 292: remove globally shared Q4 polarity as a functional premise.

Parent Q4 grammar:
  each of the nine depth stacks is a three-position nonuniform POS3 code;
  each stack independently chooses whether slash or dot is the exceptional
  symbol.

Raw observations permit 256 of the 2^9 polarity words.

For each raw-compatible polarity word:
  1. enumerate every compatible exceptional depth at every stack;
  2. combine with all six raw-compatible primary payloads;
  3. apply canonical first and second recursive POS3 closure;
  4. measure final state count / terminal;
  5. for maximum 14-state families, apply Experiment 278's Q3 criterion:
       choose one q-indexed word from each functional family such that all
       three are distinct permutations of 0,1,2.

No shared-polarity premise, expected polarity word, expected route shell, or
terminal target is supplied.

Goal:
  determine how much Q4 polarity is functionally forced once recursive closure
  and the independently derived reversible-route requirement are both used.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_q4_polarity_gauge import A, C, FI, mask_for
from audit_q4_pos3_polarity import DOT, SLASH, local_options, q4_observations
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    terminal_surface,
)


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    result = []
    if len(families) != 3:
        return result
    for choices in product(range(3), repeat=3):
        routes = tuple(
            families[i][choices[i]]
            for i in range(3)
        )
        if not all(is_permutation(route) for route in routes):
            continue
        if len(set(routes)) != 3:
            continue
        result.append((choices, routes))
    return result


def main() -> None:
    rows = load_rows()
    options = local_options(q4_observations(rows))
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    assert len(payloads) == 6

    records = []
    for polarity in product((SLASH, DOT), repeat=9):
        depth_choices = []
        compatible = True
        for j, exceptional_symbol in enumerate(polarity):
            depths = tuple(sorted({
                depth
                for depth, symbol, _pattern in options[j]
                if symbol == exceptional_symbol
            }))
            if not depths:
                compatible = False
                break
            depth_choices.append(depths)
        if not compatible:
            continue

        final = []
        for values in product(*depth_choices):
            selector = dict(enumerate(values))
            for payload in payloads:
                first = tuple(
                    decode_dash_pos3(first_pass_surface(payload, selector, q))
                    for q in range(3)
                )
                if None in first:
                    continue
                terminal = decode_dash_pos3(terminal_surface(payload, selector))
                if terminal is None:
                    continue
                final.append((payload, selector, first, terminal))

        families = {item[2] for item in final}
        shells = route_shells(families)
        records.append(
            (
                mask_for(polarity),
                len(final),
                Counter(item[3] for item in final),
                families,
                shells,
            )
        )

    assert len(records) == 256

    closure = [record for record in records if record[1] > 0]
    assert len(closure) == 16

    max_states = max(record[1] for record in records)
    assert max_states == 14
    maximal = [record for record in records if record[1] == max_states]
    assert len(maximal) == 8
    assert all(record[2] == Counter({"100": 14}) for record in maximal)

    routed = [record for record in maximal if record[4]]
    assert len(routed) == 4
    routed_masks = {record[0] for record in routed}
    assert routed_masks == {0, A, C, A | C}

    for mask, count, terminals, families, shells in routed:
        assert count == 14
        assert terminals == Counter({"100": 14})
        assert shells == [
            ((2, 1, 0), ("120", "012", "102")),
        ]

    route_dead_maximal = [record for record in maximal if not record[4]]
    assert {record[0] for record in route_dead_maximal} == {
        FI, A | FI, C | FI, A | C | FI
    }

    print("Experiment 292")
    print("raw-compatible independent Q4 polarity words:", len(records))
    print("recursive-closure polarity words:", len(closure))
    print("maximum-retention state count:", max_states)
    print("maximum-retention polarity words:", len(maximal))
    print("route-capable maximum-retention words:", len(routed))
    print("route-capable masks:", sorted(routed_masks))
    print("route-degenerate maximum masks:", sorted(record[0] for record in route_dead_maximal))
    print("RESULT: shared Q4 polarity is not required for the functional machine")
    print("RESULT: closure + maximum retention + reversible route shell force all Q4 polarities except A/C gauges")
    print("RESULT: the four exact words are 0, A, C, A+C and share the same route shell")
    print("RESULT: all-slash is a preferred physical gauge representative, not a necessary transition premise")


if __name__ == "__main__":
    main()

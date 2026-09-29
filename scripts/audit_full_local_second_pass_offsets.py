#!/usr/bin/env python3
"""Experiment 299: exhaust the full cell-local second-pass address family.

Experiments 296-298 closed local deviations in the first selector pass while
keeping the second pass canonical. This audit holds the first pass canonical and
allows the SECOND pass to rewrite both address coordinates independently at
every physical A-I cell.

At cell j with selector value S(j), choose:

    q' = S(j) + q_offset[j] mod 3
    d' = S(j) + d_offset[j] mod 3

with q_offset,d_offset independently in {0,1,2}.

There are 9 choices per cell and therefore:

    9^9 = 387,420,489

second-pass operations.

A naive loop over all operations is unnecessary. POS3 terminal validity
factorizes by the three physical columns. Each column contains three cells, so
it has only 9^3 = 729 local address-choice triples. We collapse those 729
choices to their exact 20-candidate output signatures, retain multiplicities,
then combine the three columns. The resulting exact quotient contains only
10 * 270 * 4 = 10,800 signature combinations while accounting for every one
of the 387,420,489 physical operations.

Parent machine space:
    the 20 raw-compatible machines surviving canonical first-pass POS3 closure
    from Experiment 250.

Acceptance:
    second-pass surface decodes as dash-POS3.

Model-selection bookkeeping:
    * retained raw-machine count;
    * terminal payload cardinality;
    * first-pass functional families of retained machines;
    * Experiment-278 reversible three-route criterion.

No target state count, terminal value, expected master set, or route orientation
is used as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    first_pass_surface,
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
    terminal_surface,
)


OFFSET_PAIRS = tuple(product(range(3), repeat=2))


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


def first_pass_candidates(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(raw) == 216

    result = []
    for payload, selector in raw:
        first = tuple(
            decode_dash_pos3(first_pass_surface(payload, selector, q))
            for q in range(3)
        )
        if None not in first:
            result.append((payload, selector, first))

    assert len(result) == 20
    return result


def canonical_indices(candidates):
    indices = []
    terminals = Counter()

    for index, (payload, selector, _first) in enumerate(candidates):
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is not None:
            indices.append(index)
            terminals[terminal] += 1

    assert len(indices) == 14
    assert terminals == Counter({"100": 14})
    return frozenset(indices)


def physical_columns():
    return tuple(
        tuple(
            SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col])
            for row in range(3)
        )
        for col in range(3)
    )


def column_signature(candidates, js, local_choices):
    """Return one decoded digit (0/1/2) or 3=invalid for every candidate."""
    result = []

    for payload, selector, _first in candidates:
        dash_rows = []
        for row, (j, (q_offset, d_offset)) in enumerate(
            zip(js, local_choices)
        ):
            physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            s = selector[j]
            symbol = frame_symbol(
                payload,
                (s + q_offset) % 3,
                (s + d_offset) % 3,
                physical_row,
                physical_col,
            )
            if symbol == "-":
                dash_rows.append(row)

        result.append(dash_rows[0] if len(dash_rows) == 1 else 3)

    return tuple(result)


def column_signature_counts(candidates, js):
    counts = Counter()
    for local_choices in product(OFFSET_PAIRS, repeat=3):
        counts[column_signature(candidates, js, local_choices)] += 1

    assert sum(counts.values()) == 9 ** 3
    return counts


def main() -> None:
    rows = load_rows()
    candidates = first_pass_candidates(rows)
    first_words = tuple(item[2] for item in candidates)
    canonical = canonical_indices(candidates)

    signature_counts = [
        column_signature_counts(candidates, js)
        for js in physical_columns()
    ]

    # The exact quotient is tiny compared with the 9^9 physical operation set.
    assert [len(counts) for counts in signature_counts] == [10, 270, 4]

    outcome_distribution = Counter()
    route_state_distribution = Counter()
    route_state_terminal_cardinality = Counter()

    total_operations = 0
    route_operations = 0
    exact_canonical_operations = 0
    exact_canonical_route_operations = 0
    exact_canonical_terminal_profiles = Counter()

    maximum_states = -1
    maximum_operations = 0
    maximum_route_states = -1
    maximum_route_operations = 0

    for sig0, count0 in signature_counts[0].items():
        for sig1, count1 in signature_counts[1].items():
            for sig2, count2 in signature_counts[2].items():
                multiplicity = count0 * count1 * count2
                total_operations += multiplicity

                survivors = []
                terminals = []
                for index in range(len(candidates)):
                    digits = (sig0[index], sig1[index], sig2[index])
                    if 3 in digits:
                        continue
                    survivors.append(index)
                    terminals.append("".join(str(digit) for digit in digits))

                survivor_set = frozenset(survivors)
                terminal_counts = Counter(terminals)
                terminal_cardinality = len(terminal_counts)
                states = len(survivors)

                outcome_distribution[(states, terminal_cardinality)] += multiplicity

                if states > maximum_states:
                    maximum_states = states
                    maximum_operations = multiplicity
                elif states == maximum_states:
                    maximum_operations += multiplicity

                families = {
                    first_words[index]
                    for index in survivors
                }
                shells = route_shells(families)

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

                if survivor_set == canonical:
                    exact_canonical_operations += multiplicity
                    if shells:
                        exact_canonical_route_operations += multiplicity
                    exact_canonical_terminal_profiles[
                        tuple(sorted(terminal_counts.items()))
                    ] += multiplicity

    assert total_operations == 9 ** 9 == 387_420_489

    assert outcome_distribution == Counter({
        (0, 0): 256_667_049,
        (1, 1): 6_855_840,
        (2, 1): 9_091_440,
        (2, 2): 5_067_360,
        (3, 1): 6_855_840,
        (3, 2): 12_072_240,
        (3, 3): 298_080,
        (4, 1): 7_445_520,
        (4, 2): 12_836_880,
        (4, 3): 1_788_480,
        (5, 1): 4_620_240,
        (5, 2): 15_351_120,
        (5, 3): 1_192_320,
        (6, 1): 3_427_920,
        (6, 2): 11_680_200,
        (6, 3): 1_412_640,
        (7, 1): 1_490_400,
        (7, 2): 7_302_960,
        (7, 3): 1_043_280,
        (8, 1): 1_950_480,
        (8, 2): 5_611_680,
        (8, 3): 1_023_840,
        (9, 2): 447_120,
        (9, 3): 298_080,
        (10, 1): 1_104_840,
        (10, 2): 3_670_920,
        (10, 3): 434_160,
        (12, 1): 427_680,
        (12, 2): 2_102_760,
        (12, 3): 320_760,
        (14, 1): 356_400,
        (14, 2): 1_746_360,
        (14, 3): 249_480,
        (16, 1): 142_560,
        (16, 2): 677_160,
        (16, 3): 142_560,
        (18, 2): 106_920,
        (18, 3): 71_280,
        (20, 3): 35_640,
    })

    assert maximum_states == 20
    assert maximum_operations == 35_640

    assert route_operations == 17_359_920
    assert route_state_distribution == Counter({
        3: 2_980_800,
        4: 2_533_680,
        5: 5_663_520,
        6: 2_501_280,
        7: 1_043_280,
        8: 605_880,
        10: 1_354_320,
        12: 427_680,
        14: 249_480,
    })
    assert maximum_route_states == 14
    assert maximum_route_operations == 249_480

    # Every maximum-retention route-capable second pass selects the same
    # canonical 14 physical candidates. Conversely, every operation selecting
    # exactly that 14-state set is route-capable because the first pass itself
    # is unchanged.
    assert exact_canonical_operations == 249_480
    assert exact_canonical_route_operations == 249_480

    # Pass-specific terminal rewriting is extremely non-identifiable. Even
    # inside the exact canonical 14-state family, 27 terminal profiles occur.
    assert len(exact_canonical_terminal_profiles) == 27
    assert sum(exact_canonical_terminal_profiles.values()) == 249_480

    # 178,200 exact-canonical operations have an invariant terminal; only
    # 4,320 of those preserve terminal 100.
    invariant_exact = sum(
        multiplicity
        for profile, multiplicity in exact_canonical_terminal_profiles.items()
        if len(profile) == 1
    )
    terminal_100_exact = exact_canonical_terminal_profiles[
        (("100", 14),)
    ]
    assert invariant_exact == 178_200
    assert terminal_100_exact == 4_320

    print("Experiment 299")
    print("full second-pass local address family:", total_operations)
    print("exact column-signature quotient:", [len(x) for x in signature_counts])
    print("quotient combinations evaluated:", 10 * 270 * 4)
    print("maximum retained first-pass states:", maximum_states)
    print("operations attaining 20 states:", maximum_operations)
    print("route-capable physical operations:", route_operations)
    print("route-capable state distribution:", dict(sorted(route_state_distribution.items())))
    print("maximum route-capable states:", maximum_route_states)
    print("operations attaining route maximum:", maximum_route_operations)
    print("exact canonical-14 operations:", exact_canonical_operations)
    print("exact canonical terminal profiles:", len(exact_canonical_terminal_profiles))
    print("exact canonical operations with invariant terminal:", invariant_exact)
    print("exact canonical operations with terminal 100:", terminal_100_exact)
    print("RESULT: arbitrary second-pass local rewrites are massively underdetermined")
    print("RESULT: maximum route-capable retention still selects the canonical 14 physical states")
    print("RESULT: it does NOT identify a unique terminal address rule")
    print("RESULT: 4,320 distinct local second-pass rules reproduce the canonical 14 states and terminal 100")
    print("RESULT: uniform same-operation reuse must do real explanatory work; endpoint agreement alone cannot")


if __name__ == "__main__":
    main()

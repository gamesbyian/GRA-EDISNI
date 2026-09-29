#!/usr/bin/env python3
"""Experiment 298: close the full cell-local first-pass offset family.

Experiments 296-297 probe one and two cell-local deviations from the canonical
first-pass depth selection. This experiment removes the defect-count bound.

At each of the nine physical A-I cells independently choose:

    d' = S(j) + offset[j] mod 3
    offset[j] in {0,1,2}

External q is preserved. The second pass remains canonical.

Family size:
    3^9 = 19,683 first-pass operations.

Parent machine space:
    the same 216 raw-compatible primary x Q4 candidates from Experiment 250.

Acceptance:
    all three first-pass surfaces and the canonical second-pass terminal must
    decode as dash-POS3.

For every operation record:
    * retained raw-machine count;
    * distinct first-pass functional families;
    * whether the Experiment-278 three-distinct-permutation route shell exists.

No target state count, terminal word, expected master set, or route orientation
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
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
    terminal_surface,
)


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


def label(offsets):
    parts = [
        f"{SERIAL_ORDER[j]}{delta}"
        for j, delta in enumerate(offsets)
        if delta
    ]
    return "+".join(parts) if parts else "canonical"


def terminal_valid_raw(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(raw) == 216

    result = []
    terminals = Counter()
    for payload, selector in raw:
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is None:
            continue
        result.append((payload, selector))
        terminals[terminal] += 1

    # With canonical second-pass addressing, 96 raw candidates have a POS3
    # terminal and all of them already terminate at 100. The first-pass family
    # therefore tests which of those 96 survive as a coherent routed machine.
    assert len(result) == 96
    assert terminals == Counter({"100": 96})
    return result


def precompute_symbols(raw):
    positions = [
        PHYSICAL_POSITION[SERIAL_ORDER[j]]
        for j in range(9)
    ]
    table = []
    for payload, selector in raw:
        machine = []
        for q in range(3):
            q_table = []
            for j, (row, col) in enumerate(positions):
                s = selector[j]
                q_table.append(tuple(
                    frame_symbol(
                        payload,
                        q,
                        (s + offset) % 3,
                        row,
                        col,
                    )
                    for offset in range(3)
                ))
            machine.append(q_table)
        table.append(machine)
    return table


def evaluate_offsets(symbols, offsets):
    families = []
    survivor_indices = []

    for machine_index, machine in enumerate(symbols):
        words = []
        valid = True

        for q in range(3):
            digits = []
            for col in range(3):
                dash_rows = []
                for row in range(3):
                    letter = PHYSICAL_LAYOUT[row][col]
                    j = SERIAL_ORDER.index(letter)
                    if machine[q][j][offsets[j]] == "-":
                        dash_rows.append(row)

                if len(dash_rows) != 1:
                    valid = False
                    break
                digits.append(str(dash_rows[0]))

            if not valid:
                break
            words.append("".join(digits))

        if valid:
            survivor_indices.append(machine_index)
            families.append(tuple(words))

    return tuple(survivor_indices), frozenset(families)


def main() -> None:
    rows = load_rows()
    raw = terminal_valid_raw(rows)
    symbols = precompute_symbols(raw)

    results = []
    for offsets in product(range(3), repeat=9):
        survivors, families = evaluate_offsets(symbols, offsets)
        results.append(
            (
                offsets,
                survivors,
                families,
                route_shells(families),
            )
        )

    assert len(results) == 19683

    distribution = Counter(
        len(survivors)
        for _offsets, survivors, _families, _shells in results
    )
    assert distribution == Counter({
        0: 19059,
        1: 16,
        2: 88,
        3: 48,
        4: 72,
        5: 32,
        6: 88,
        7: 16,
        8: 64,
        9: 16,
        10: 64,
        12: 48,
        14: 8,
        16: 24,
        18: 8,
        20: 24,
        24: 8,
    })

    canonical = next(
        result
        for result in results
        if result[0] == (0,) * 9
    )
    canonical_survivors = set(canonical[1])
    assert len(canonical_survivors) == 14
    assert canonical[3] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    # Exactly eight operations retain 14 states, and all eight retain exactly
    # the same 14 raw physical machines. Only canonical preserves a route shell.
    fourteen = [
        result for result in results
        if len(result[1]) == 14
    ]
    assert len(fourteen) == 8
    assert all(set(result[1]) == canonical_survivors for result in fourteen)
    assert sum(bool(result[3]) for result in fourteen) == 1

    fourteen_labels = {label(result[0]) for result in fourteen}
    assert fourteen_labels == {
        "canonical",
        "F2+I1",
        "B1+H1",
        "B1+F2+H1+I1",
        "B1+E1+H2",
        "B1+E1+F2+H2+I1",
        "B2+H2",
        "B2+F2+H2+I1",
    }

    # The entire family contains only six route-capable operations.
    route_capable = [
        result for result in results
        if result[3]
    ]
    assert len(route_capable) == 6

    route_summary = {
        label(offsets): (
            len(survivors),
            shells,
        )
        for offsets, survivors, _families, shells in route_capable
    }
    assert route_summary == {
        "canonical": (
            14,
            [((2, 1, 0), ("120", "012", "102"))],
        ),
        "C1": (
            7,
            [((2, 1, 0), ("120", "012", "102"))],
        ),
        "C2": (
            7,
            [((2, 1, 0), ("120", "012", "102"))],
        ),
        "A1+B2+G2+H2": (
            12,
            [((2, 1, 0), ("102", "012", "120"))],
        ),
        "A1+B2+C1+G2+H2": (
            6,
            [((2, 1, 0), ("102", "012", "120"))],
        ),
        "A1+B2+C2+G2+H2": (
            6,
            [((2, 1, 0), ("102", "012", "120"))],
        ),
    }

    # Canonical is the unique maximum-retention route-capable operation.
    route_maximum = max(len(result[1]) for result in route_capable)
    assert route_maximum == 14
    assert [
        label(result[0])
        for result in route_capable
        if len(result[1]) == route_maximum
    ] == ["canonical"]

    # The best noncanonical route sibling is genuinely a different 12-state
    # physical family, not merely a subset of canonical.
    route12 = next(
        result
        for result in route_capable
        if label(result[0]) == "A1+B2+G2+H2"
    )
    route12_survivors = set(route12[1])
    assert len(route12_survivors & canonical_survivors) == 2
    assert len(route12_survivors - canonical_survivors) == 10
    assert len(canonical_survivors - route12_survivors) == 12

    # Global maximum retention reaches 24 states but never preserves a route.
    maximum = max(len(result[1]) for result in results)
    assert maximum == 24
    maxima = [
        result for result in results
        if len(result[1]) == maximum
    ]
    assert len(maxima) == 8
    assert all(not result[3] for result in maxima)

    print("Experiment 298")
    print("full cell-local first-pass offset family:", len(results))
    print("terminal-valid raw candidates before first-pass closure:", len(raw))
    print("survivor distribution:")
    for states in sorted(distribution):
        print(" ", states, "->", distribution[states])
    print("14-state operations:", sorted(fourteen_labels))
    print("route-capable operations:")
    for name, (states, shells) in route_summary.items():
        print(" ", name, "states=", states, "shell=", shells[0])
    print("maximum retained states anywhere:", maximum)
    print("maximum-retention operations:", len(maxima))
    print("RESULT: all eight 14-state operations select the same physical masters")
    print("RESULT: only canonical among those eight preserves a reversible route shell")
    print("RESULT: canonical uniquely maximizes retention among all route-capable operations")
    print("RESULT: the best alternate route machine has 12 states and only 2 masters in common with canonical")
    print("RESULT: unrestricted cell-local offset freedom is exhaustively closed at 3^9 configurations")


if __name__ == "__main__":
    main()

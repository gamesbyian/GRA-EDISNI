#!/usr/bin/env python3
"""Experiment 314: selector-controlled local q-shear under same-operation reuse.

At each physical A-I cell choose one coefficient c_j in F3 and define

    F_j(q,S) = (q + c_j*S, S) mod 3.

The same F_j is reused on both recursive passes:

    first pass:  F_j(q,S(j))
    second pass: F_j(S(j),S(j)).

This is a minimal state-dependent coordinate coupling.  It is not a constant
translation (Experiment 313) and does not alter selector depth (Experiments
310-312).

Full family:
    3^9 = 19,683 operations.

No target terminal, state count, route word, survivor set, or canonical
operation is used as a filter.
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


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    if len(families) != 3:
        return []
    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(families[index][choices[index]] for index in range(3))
        if all(is_permutation(word) for word in routes) and len(set(routes)) == 3:
            result.append((choices, routes))
    return result


def raw_candidates(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    result = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(result) == 216
    return result, payloads, selectors


def physical_columns():
    return tuple(
        tuple(SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col]) for row in range(3))
        for col in range(3)
    )


def column_signature(candidates, js, coefficients):
    signatures = []
    for payload, selector in candidates:
        digits = []

        for q in range(3):
            dash_rows = []
            for row, (j, coefficient) in enumerate(zip(js, coefficients)):
                physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
                s = selector[j]
                if frame_symbol(
                    payload,
                    (q + coefficient * s) % 3,
                    s,
                    physical_row,
                    physical_col,
                ) == "-":
                    dash_rows.append(row)
            digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        dash_rows = []
        for row, (j, coefficient) in enumerate(zip(js, coefficients)):
            physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            s = selector[j]
            if frame_symbol(
                payload,
                ((1 + coefficient) * s) % 3,
                s,
                physical_row,
                physical_col,
            ) == "-":
                dash_rows.append(row)
        digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        signatures.append(tuple(digits))
    return tuple(signatures)


def label(coefficients):
    parts = [
        f"{SERIAL_ORDER[j]}:{coefficient}"
        for j, coefficient in enumerate(coefficients)
        if coefficient
    ]
    return "+".join(parts) if parts else "canonical"


def main() -> None:
    candidates, payloads, selectors = raw_candidates(load_rows())
    columns = physical_columns()

    tables = []
    for js in columns:
        table = {}
        for coefficients in product(range(3), repeat=3):
            table[coefficients] = column_signature(candidates, js, coefficients)
        tables.append(table)

    assert [len(set(table.values())) for table in tables] == [9, 27, 6]

    outcomes = []
    for coefficients0, sig0 in tables[0].items():
        for coefficients1, sig1 in tables[1].items():
            for coefficients2, sig2 in tables[2].items():
                coefficients = [0] * 9
                for js, local in zip(
                    columns,
                    (coefficients0, coefficients1, coefficients2),
                ):
                    for j, value in zip(js, local):
                        coefficients[j] = value

                survivors = []
                families = set()
                terminals = []

                for index in range(len(candidates)):
                    signatures = (sig0[index], sig1[index], sig2[index])
                    if any(3 in signature for signature in signatures):
                        continue

                    first = tuple(
                        "".join(str(signature[q]) for signature in signatures)
                        for q in range(3)
                    )
                    terminal = "".join(
                        str(signature[3]) for signature in signatures
                    )

                    survivors.append(index)
                    families.add(first)
                    terminals.append(terminal)

                outcomes.append({
                    "coefficients": tuple(coefficients),
                    "survivors": frozenset(survivors),
                    "families": frozenset(families),
                    "terminals": Counter(terminals),
                    "shells": route_shells(families),
                })

    assert len(outcomes) == 3 ** 9 == 19_683

    state_distribution = Counter(len(item["survivors"]) for item in outcomes)
    assert state_distribution == Counter({
        0: 16_578,
        2: 648,
        4: 594,
        5: 324,
        6: 432,
        7: 324,
        8: 324,
        10: 189,
        12: 108,
        14: 81,
        16: 54,
        20: 27,
    })

    maximum_states = max(state_distribution)
    assert maximum_states == 20
    assert all(
        not item["shells"]
        for item in outcomes
        if len(item["survivors"]) > 14
    )

    route_capable = [item for item in outcomes if item["shells"]]
    assert len(route_capable) == 99
    assert Counter(len(item["survivors"]) for item in route_capable) == Counter({
        6: 36,
        7: 36,
        12: 18,
        14: 9,
    })

    route_max = [
        item for item in route_capable
        if len(item["survivors"]) == 14
    ]
    assert len(route_max) == 9

    canonical = next(
        item for item in outcomes
        if item["coefficients"] == (0,) * 9
    )
    assert len(canonical["survivors"]) == 14
    assert canonical["terminals"] == Counter({"100": 14})
    assert canonical["shells"] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    # Every route-max operation is exactly observationally canonical.
    for item in route_max:
        assert item["survivors"] == canonical["survivors"]
        assert item["families"] == canonical["families"]
        assert item["terminals"] == canonical["terminals"]
        assert item["shells"] == canonical["shells"]

    assert {
        label(item["coefficients"])
        for item in route_max
    } == {
        "canonical",
        "E:1", "E:2",
        "F:1", "F:2",
        "E:1+F:1", "E:1+F:2",
        "E:2+F:1", "E:2+F:2",
    }

    # Explain the two gauge coefficients directly from the raw parent.
    e_j = SERIAL_ORDER.index("E")
    f_j = SERIAL_ORDER.index("F")
    assert {selector[e_j] for selector in selectors} == {0}
    assert {selector[f_j] for selector in selectors} == {1}

    for letter, depth in (("E", 0), ("F", 1)):
        row, col = PHYSICAL_POSITION[letter]
        assert {
            tuple(frame_symbol(payload, q, depth, row, col) for q in range(3))
            for payload in payloads
        } == {("/", "/", "/")}

    print("Experiment 314")
    print("selector-controlled local shear family:", len(outcomes))
    print("column signature cardinalities:", [len(set(t.values())) for t in tables])
    print("maximum retained raw states:", maximum_states)
    print("route-capable operations:", len(route_capable))
    print("route-capable state distribution:", dict(sorted(Counter(
        len(item["survivors"]) for item in route_capable
    ).items())))
    print("route-max operations:", len(route_max))
    print("route-max labels:", sorted(label(item["coefficients"]) for item in route_max))
    print("RESULT: every >14-state shear is route-degenerate")
    print("RESULT: all nine route-max shears are exactly observationally canonical")
    print("RESULT: the only shear freedom is independent E/F coefficients")
    print("RESULT: E is invisible because S_E=0; F is invisible because q0/q1/q2 at depth 1 are all slash")
    print("RESULT: selector-controlled local q shear introduces only exact gauges, not a rival machine")


if __name__ == "__main__":
    main()

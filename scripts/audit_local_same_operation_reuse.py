#!/usr/bin/env python3
"""Experiment 310: exhaust cell-local depth offsets under same-operation reuse.

Experiment 309 shows that if the second selector pass is allowed its own
arbitrary cell-specific q/d rewrites, the terminal operation becomes massively
underidentified. That grammar quietly abandons a central property of the
mechanical model: the same selector-address operation is reused recursively.

This audit therefore tests a hostile but genuinely recursive local family.

At each physical A-I cell independently choose:

    F_j(q, S) = (q, S + offset[j] mod 3)
    offset[j] in {0,1,2}

and reuse THE SAME F_j on both passes:

    first pass:  F_j(q, S(j))
    second pass: F_j(S(j), S(j))

There are exactly 3^9 = 19,683 local operators.

Parent machine space:
    all 216 raw-compatible primary x Q4 candidates from Experiment 250.

Acceptance:
    * all three first-pass surfaces decode as dash-POS3;
    * the reused-operation second-pass surface decodes as dash-POS3.

For every operation record:
    * retained raw-machine count;
    * terminal cardinality;
    * distinct first-pass functional families;
    * Experiment-278 reversible three-route criterion.

No target state count, terminal value, expected master set, or route orientation
is used as a filter.

The enumeration is factored by physical column. Each column has three cells and
therefore only 3^3 = 27 local offset triples; combining the three columns gives
the exact 27^3 = 3^9 family.
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


def label(offsets):
    parts = [
        f"{SERIAL_ORDER[j]}{offset}"
        for j, offset in enumerate(offsets)
        if offset
    ]
    return "+".join(parts) if parts else "canonical"


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


def column_signature(candidates, js, offsets):
    """Per candidate: q0,q1,q2,terminal row digits; 3 marks invalid."""
    signatures = []

    for payload, selector in candidates:
        digits = []

        # First pass: q is external, selected depth is locally offset.
        for q in range(3):
            dash_rows = []
            for row, (j, offset) in enumerate(zip(js, offsets)):
                physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
                s = selector[j]
                symbol = frame_symbol(
                    payload,
                    q,
                    (s + offset) % 3,
                    physical_row,
                    physical_col,
                )
                if symbol == "-":
                    dash_rows.append(row)
            digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        # Second pass: the same local operator is reused on input (S,S).
        dash_rows = []
        for row, (j, offset) in enumerate(zip(js, offsets)):
            physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            s = selector[j]
            symbol = frame_symbol(
                payload,
                s,
                (s + offset) % 3,
                physical_row,
                physical_col,
            )
            if symbol == "-":
                dash_rows.append(row)
        digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        signatures.append(tuple(digits))

    return tuple(signatures)


def main() -> None:
    candidates = raw_candidates(load_rows())
    columns = physical_columns()

    column_tables = []
    for js in columns:
        table = {}
        for offsets in product(range(3), repeat=3):
            table[offsets] = column_signature(candidates, js, offsets)
        assert len(table) == 27
        column_tables.append(table)

    outcomes = []
    for offsets0, sig0 in column_tables[0].items():
        for offsets1, sig1 in column_tables[1].items():
            for offsets2, sig2 in column_tables[2].items():
                offsets = [0] * 9
                for js, local in zip(columns, (offsets0, offsets1, offsets2)):
                    for j, offset in zip(js, local):
                        offsets[j] = offset

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

                outcomes.append({
                    "offsets": tuple(offsets),
                    "states": len(survivors),
                    "survivors": frozenset(survivors),
                    "families": frozenset(families),
                    "terminals": Counter(terminals),
                    "shells": route_shells(families),
                })

    assert len(outcomes) == 3 ** 9 == 19_683

    distribution = Counter(
        (item["states"], len(item["terminals"]))
        for item in outcomes
    )
    assert distribution == Counter({
        (0, 0): 19_338,
        (2, 1): 24,
        (4, 1): 54,
        (4, 2): 36,
        (5, 1): 12,
        (5, 2): 36,
        (6, 2): 36,
        (7, 1): 12,
        (7, 2): 36,
        (8, 1): 12,
        (8, 2): 9,
        (8, 3): 12,
        (9, 2): 12,
        (10, 1): 3,
        (10, 2): 9,
        (11, 2): 12,
        (12, 2): 9,
        (14, 1): 3,
        (14, 2): 9,
        (16, 3): 3,
        (18, 2): 3,
        (22, 2): 3,
    })

    canonical = next(
        item for item in outcomes
        if item["offsets"] == (0,) * 9
    )
    assert canonical["states"] == 14
    assert canonical["terminals"] == Counter({"100": 14})
    assert canonical["shells"] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    route_capable = [
        item for item in outcomes
        if item["shells"]
    ]
    assert len(route_capable) == 18
    assert Counter(item["states"] for item in route_capable) == Counter({
        4: 2,
        5: 4,
        6: 4,
        7: 2,
        8: 1,
        10: 2,
        12: 2,
        14: 1,
    })

    # Canonical is now unique at the maximum route-capable state count.
    maximum_route_states = max(item["states"] for item in route_capable)
    assert maximum_route_states == 14
    route_maxima = [
        item for item in route_capable
        if item["states"] == maximum_route_states
    ]
    assert len(route_maxima) == 1
    assert route_maxima[0] is canonical

    # The strongest route-capable siblings retain only 12 states.
    route_twelve = {
        label(item["offsets"]): item["terminals"]
        for item in route_capable
        if item["states"] == 12
    }
    assert route_twelve == {
        "B2+G2+H2": Counter({"122": 6, "102": 6}),
        "A2+B2+G2+H2": Counter({"122": 6, "102": 6}),
    }

    # Several operations retain more raw states than canonical, but all of them
    # are route-degenerate. The global maximum reaches 22.
    maximum_states = max(item["states"] for item in outcomes)
    assert maximum_states == 22
    maxima = [
        item for item in outcomes
        if item["states"] == maximum_states
    ]
    assert {label(item["offsets"]) for item in maxima} == {
        "D2",
        "B1+D2+H1",
        "B2+D2+H2",
    }
    assert all(not item["shells"] for item in maxima)

    # Two noncanonical rules recover the exact same 14 physical candidates as
    # canonical, but both terminate at 102 and destroy the route shell.
    same_fourteen = [
        item for item in outcomes
        if item["survivors"] == canonical["survivors"]
    ]
    assert {
        label(item["offsets"])
        for item in same_fourteen
    } == {
        "canonical",
        "B1+H1",
        "B2+H2",
    }
    assert all(
        not item["shells"]
        for item in same_fourteen
        if item is not canonical
    )
    assert all(
        item["terminals"] == Counter({"102": 14})
        for item in same_fourteen
        if item is not canonical
    )

    print("Experiment 310")
    print("same-operation local depth-offset family:", len(outcomes))
    print("route-capable operations:", len(route_capable))
    print("route-capable state distribution:", dict(sorted(Counter(
        item["states"] for item in route_capable
    ).items())))
    print("maximum route-capable states:", maximum_route_states)
    print("unique route maximum:", label(route_maxima[0]["offsets"]))
    print("best route-capable siblings:", sorted(route_twelve))
    print("global maximum retained states:", maximum_states)
    print("global maxima:", sorted(label(item["offsets"]) for item in maxima))
    print("same-14 physical families:", sorted(label(item["offsets"]) for item in same_fourteen))
    print("RESULT: pass-specific second-pass freedom collapses once the local rule must actually be reused")
    print("RESULT: canonical is the unique maximum-retention route-capable same-operation local rule")
    print("RESULT: every operation retaining more than 14 raw states is route-degenerate")
    print("RESULT: exact 14-master recovery alone still admits two terminal-102 siblings, both route-degenerate")


if __name__ == "__main__":
    main()

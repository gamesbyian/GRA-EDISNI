#!/usr/bin/env python3
"""Experiment 253: select the two-pass recursion from the raw candidate space.

Parent machine space:
    the 216 raw-compatible primary x Q4 candidates from Experiment 250.

Parent operation family:
    first pass  B(f(q), g(S), j)
    second pass B(h(S), k(S), j)

where f,g,h,k independently range over the six ternary permutations.
Total operation pairs: 6^4 = 1296.

For each operation tuple, retain raw candidate machines whose first-pass three
surfaces and second-pass terminal are valid dash-POS3 objects.

Then ask, without targeting a state count or terminal payload:
  * which operation tuples yield a completion-invariant terminal?
  * among those, which preserve the largest raw-compatible state family?

This "maximal survivor" criterion penalizes operations that manufacture
invariance by silently discarding more raw-compatible physical states.
"""

from __future__ import annotations

from itertools import permutations

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
)

PERMS = tuple(permutations(range(3)))
IDENTITY = (0, 1, 2)


def first_surface(payload, selector, q, f, g):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                f[q],
                g[selector_at_physical_cell(selector, row, col)],
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def second_surface(payload, selector, h, k):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                h[selector_at_physical_cell(selector, row, col)],
                k[selector_at_physical_cell(selector, row, col)],
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]

    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(raw) == 216

    invariant_operations = []

    for f in PERMS:
        for g in PERMS:
            for h in PERMS:
                for k in PERMS:
                    terminals = []
                    survivor_count = 0

                    for payload, selector in raw:
                        first = tuple(
                            decode_dash_pos3(
                                first_surface(payload, selector, q, f, g)
                            )
                            for q in range(3)
                        )
                        if None in first:
                            continue

                        terminal = decode_dash_pos3(
                            second_surface(payload, selector, h, k)
                        )
                        if terminal is None:
                            continue

                        survivor_count += 1
                        terminals.append(terminal)

                    if survivor_count and len(set(terminals)) == 1:
                        invariant_operations.append(
                            (f, g, h, k, survivor_count, terminals[0])
                        )

    assert len(invariant_operations) == 42

    max_survivors = max(item[4] for item in invariant_operations)
    maximal = [
        item for item in invariant_operations
        if item[4] == max_survivors
    ]

    assert max_survivors == 14
    assert len(maximal) == 6

    assert {item[0] for item in maximal} == set(PERMS)
    assert {item[1] for item in maximal} == {IDENTITY}
    assert {item[2] for item in maximal} == {IDENTITY}
    assert {item[3] for item in maximal} == {IDENTITY}
    assert {item[5] for item in maximal} == {"100"}

    fixed_q = [item for item in maximal if item[0] == IDENTITY]
    assert len(fixed_q) == 1
    assert fixed_q[0][:4] == (
        IDENTITY,
        IDENTITY,
        IDENTITY,
        IDENTITY,
    )

    print("Experiment 253")
    print("raw candidate machines:", len(raw))
    print("shell-preserving operation tuples:", len(PERMS) ** 4)
    print("operation tuples with invariant nonempty POS3 terminal:", len(invariant_operations))
    print("maximum retained raw-compatible states:", max_survivors)
    print("maximal operation tuples:", len(maximal))
    print("maximal terminal payloads:", sorted({item[5] for item in maximal}))
    print("OK: every maximal solution forces g=h=k=identity")
    print("OK: remaining f freedom is exactly external-q relabeling")
    print("OK: fixing physical q labels leaves the all-identity recursion uniquely")
    print("OK: terminal 100 emerges for every maximal operation tuple")


if __name__ == "__main__":
    main()

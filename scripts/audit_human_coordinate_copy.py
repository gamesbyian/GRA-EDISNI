#!/usr/bin/env python3
"""Experiment 290: audit the four simplest human coordinate-copy operations.

The primary is addressed by (q,d,j). Q4 supplies one ternary selector value
S(j). Before searching arbitrary coordinate maps, a human has four literal
ways to fill the two source coordinates using only external quarter q and
selector S:

    (q,q), (q,S), (S,q), (S,S)

For each operation, start from the full 6 raw-compatible primary payloads ×
36 raw-compatible canonical Q4 selectors = 216 machines. Require only that all
three external-q output surfaces decode as dash-POS3.

Measure:
  * number of surviving raw machines;
  * number of distinct three-surface output families;
  * whether output actually depends on external q;
  * whether changing S can matter.

Then, only for the canonical nondegenerate (q,S) branch, apply the ordinary
second selector reuse (S,S) and record the final closure count.

No expected first-pass words, hidden-state relation, state count, or terminal
payload is used to choose the first operation.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

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
    terminal_surface,
)


OPS = (
    ("q", "q"),
    ("q", "S"),
    ("S", "q"),
    ("S", "S"),
)


def copied_surface(payload, selector, external_q, op):
    left, right = op

    return tuple(
        tuple(
            frame_symbol(
                payload,
                external_q if left == "q" else selector_at_physical_cell(selector, row, col),
                external_q if right == "q" else selector_at_physical_cell(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def selector_sensitive(op):
    return "S" in op


def external_q_preserved(op):
    return "q" in op


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]

    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(raw) == 216

    records = {}
    for op in OPS:
        survivors = []
        for payload, selector in raw:
            outputs = tuple(
                decode_dash_pos3(
                    copied_surface(payload, selector, q, op)
                )
                for q in range(3)
            )
            if None in outputs:
                continue
            survivors.append((payload, selector, outputs))

        families = Counter(item[2] for item in survivors)
        records[op] = (survivors, families)

    assert len(records[("q", "q")][0]) == 216
    assert records[("q", "q")][1] == Counter({
        ("112", "002", "100"): 216,
    })

    assert len(records[("S", "q")][0]) == 0

    assert len(records[("S", "S")][0]) == 96
    assert records[("S", "S")][1] == Counter({
        ("100", "100", "100"): 96,
    })

    qS_survivors, qS_families = records[("q", "S")]
    assert len(qS_survivors) == 20
    assert len(qS_families) == 6

    # (q,S) is the only literal copy operation that both uses S and preserves
    # nontrivial external-q structure.
    nondegenerate = [
        op
        for op in OPS
        if records[op][0]
        and selector_sensitive(op)
        and external_q_preserved(op)
        and len(records[op][1]) > 1
    ]
    assert nondegenerate == [("q", "S")]

    # Reuse the same selector on q as well: canonical second pass.
    final = []
    for payload, selector, outputs in qS_survivors:
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is not None:
            final.append((payload, selector, outputs, terminal))

    assert len(final) == 14
    assert {item[3] for item in final} == {"100"}

    print("Experiment 290")
    for op in OPS:
        survivors, families = records[op]
        print(
            op,
            "survivors=", len(survivors),
            "families=", len(families),
            "selector_sensitive=", selector_sensitive(op),
            "q_preserved=", external_q_preserved(op),
        )
        print(" ", dict(families))
    print("nondegenerate literal-copy operations:", nondegenerate)
    print("(q,S) second-pass survivors:", len(final))
    print("(q,S) second-pass terminals:", sorted({item[3] for item in final}))
    print("RESULT: (q,S) is the unique selector-sensitive, q-preserving nondegenerate literal copy")
    print("RESULT: the other three simplest address copies are trivial or impossible")
    print("RESULT: human discovery can begin with four coordinate-copy trials, not arbitrary map search")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 291: derive second selector reuse from four simple q choices.

Experiment 290 derives the first address substitution (q,S) inside the four
literal coordinate-copy rules. It leaves 20 raw-compatible machines whose
three q-indexed output surfaces are all valid POS3.

At that point depth is already selected. One outer q axis remains. A
paper-and-pencil solver has four simplest ways to obtain one surface:
  * read fixed q=0;
  * read fixed q=1;
  * read fixed q=2;
  * use the same selector value q=S(j).

For each choice, measure:
  * how many of the 20 first-pass machines still decode as POS3;
  * how many distinct output payloads remain.

No target terminal word or expected state count is supplied.
"""

from __future__ import annotations

from collections import Counter

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
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
)


CHOICES = (0, 1, 2, "S")


def selected_surface(payload, selector, choice):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                (
                    selector_at_physical_cell(selector, row, col)
                    if choice == "S"
                    else choice
                ),
                selector_at_physical_cell(selector, row, col),
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

    first_survivors = []
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None not in first:
                first_survivors.append((payload, selector, first))

    assert len(first_survivors) == 20

    records = {}
    for choice in CHOICES:
        outputs = []
        for payload, selector, _first in first_survivors:
            word = decode_dash_pos3(
                selected_surface(payload, selector, choice)
            )
            if word is not None:
                outputs.append(word)
        records[choice] = Counter(outputs)

    assert records[0] == Counter({
        "102": 14,
        "112": 4,
        "122": 2,
    })
    assert records[1] == Counter({
        "022": 8,
        "012": 8,
        "002": 4,
    })
    assert records[2] == Counter({
        "100": 14,
        "120": 6,
    })
    assert records["S"] == Counter({
        "100": 14,
    })

    # Fixed-q reads do not filter the first-pass family at all. Reusing S is
    # uniquely both selective and completion-invariant.
    assert all(sum(records[q].values()) == 20 for q in (0, 1, 2))
    assert sum(records["S"].values()) == 14
    assert len(records["S"]) == 1
    # Fixed-q reads are all non-invariant, but q=2 has two distinct outputs
    # while q=0 and q=1 each have three. The previous blanket "== 3"
    # assertion contradicted the exact q=2 Counter asserted immediately above.
    assert {q: len(records[q]) for q in (0, 1, 2)} == {0: 3, 1: 3, 2: 2}

    print("Experiment 291")
    print("first-pass machines:", len(first_survivors))
    for choice in CHOICES:
        print(
            "q choice", choice,
            "valid=", sum(records[choice].values()),
            "outputs=", dict(records[choice]),
        )
    print("RESULT: fixed q=0/1/2 merely read one existing plane and keep all 20 states")
    print("RESULT: q=S is the unique simple choice that performs further selection")
    print("RESULT: q=S reduces 20->14 and independently collapses every survivor to one payload")
    print("RESULT: the terminal payload 100 emerges without being supplied as a target")


if __name__ == "__main__":
    main()

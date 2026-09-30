#!/usr/bin/env python3
"""Experiment 322 exploratory audit: all 27 one-shot q=f(S) consumers after G5.

Experiment 291 tested only q=0,1,2 and q=S. This exhausts every deterministic
map f:{0,1,2}->{0,1,2}. No expected terminal, state count, route shell, or
identity map is supplied as a target.

For each map, report:
- how many of the 20 G5 first-pass machines still decode as POS3;
- how many distinct output words remain;
- whether f is constant, bijective, or identity.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
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


def selected_surface(payload, selector, fmap):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                fmap[selector_at_physical_cell(selector, row, col)],
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

    records = []
    for fmap in product(range(3), repeat=3):
        outputs = []
        for payload, selector, _first in first_survivors:
            word = decode_dash_pos3(selected_surface(payload, selector, fmap))
            if word is not None:
                outputs.append(word)
        counts = Counter(outputs)
        record = {
            "map": "".join(map(str, fmap)),
            "valid": sum(counts.values()),
            "distinct_outputs": len(counts),
            "outputs": dict(sorted(counts.items())),
            "constant": len(set(fmap)) == 1,
            "bijective": set(fmap) == {0, 1, 2},
            "identity": fmap == (0, 1, 2),
        }
        records.append(record)

    records.sort(key=lambda r: (r["valid"], -r["distinct_outputs"], r["map"]), reverse=True)

    invariant = [r for r in records if r["valid"] and r["distinct_outputs"] == 1]
    selective = [r for r in records if r["valid"] < 20]
    bijective = [r for r in records if r["bijective"]]
    max_invariant_retention = max(r["valid"] for r in invariant)
    optimal = [r for r in invariant if r["valid"] == max_invariant_retention]

    assert len(records) == 27
    assert len(invariant) == 8
    assert max_invariant_retention == 14
    assert [(r["map"], r["outputs"]) for r in optimal] == [
        ("002", {"100": 14}),
        ("012", {"100": 14}),
    ]

    # The two optimal maps differ only at S=1. Their accepted machine set is
    # identical; this is the already-known f1 observational gauge.
    accepted = {}
    for fmap in ((0, 0, 2), (0, 1, 2)):
        keys = []
        for payload, selector, _first in first_survivors:
            word = decode_dash_pos3(selected_surface(payload, selector, fmap))
            if word is not None:
                keys.append((tuple(sorted(payload.items())), tuple(sorted(selector.items()))))
        accepted[fmap] = set(keys)
    assert accepted[(0, 0, 2)] == accepted[(0, 1, 2)]
    assert len(accepted[(0, 0, 2)]) == 14

    print("Experiment 322")
    print("first-pass machines:", len(first_survivors))
    print("selector maps tested:", len(records))
    print("selective maps (<20 survivors):", len(selective))
    print("completion-invariant maps:", len(invariant))
    print("maximum invariant retention:", max_invariant_retention)
    print("optimal invariant maps:", [(r["map"], r["outputs"]) for r in optimal])
    print("bijective maps:", len(bijective))
    print("RESULT: only 002 and 012 retain 14 machines with one invariant output")
    print("RESULT: both give terminal 100 and accept the identical 14-machine set")
    print("RESULT: their sole difference is the established S=1 f1 observational gauge")
    print("INVARIANT")
    for r in invariant:
        print(r)
    print("BIJECTIVE")
    for r in bijective:
        print(r)
    print("ALL")
    for r in sorted(records, key=lambda x: x["map"]):
        print(r)


if __name__ == "__main__":
    main()

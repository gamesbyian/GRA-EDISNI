#!/usr/bin/env python3
"""Experiment 267: negative control for raw-state retention under singular affine maps.

Experiment 266 restricts the coupled (q,S) address transform to affine
bijections. This script deliberately removes that safeguard and enumerates all
3^6 = 729 affine maps:

    q' = a*q + b*S + u  (mod 3)
    d' = c*q + d*S + v  (mod 3)

including singular and constant maps.

Acceptance is again only first-pass dash-POS3 validity for all three external
q outputs over each of the 216 raw-compatible candidate machines.

Purpose:
    show whether maximum raw-state retention by itself is a meaningful model
    selection objective once information-destroying address maps are allowed.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_affine_first_pass import candidate_surface
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)


def determinant(mapping):
    a, b, c, d, _u, _v = mapping
    return (a * d - b * c) % 3


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(raw) == 216

    mappings = tuple(product(range(3), repeat=6))
    assert len(mappings) == 729

    results = []
    for mapping in mappings:
        survivors = 0
        for payload, selector in raw:
            decoded = tuple(
                decode_dash_pos3(
                    candidate_surface(payload, selector, mapping, q)
                )
                for q in range(3)
            )
            if None not in decoded:
                survivors += 1
        results.append((survivors, mapping))

    distribution = Counter(count for count, _mapping in results)
    assert distribution == Counter({
        0: 601,
        1: 6,
        7: 6,
        10: 12,
        20: 12,
        22: 6,
        24: 13,
        26: 1,
        34: 1,
        36: 3,
        38: 13,
        40: 1,
        48: 4,
        52: 1,
        54: 1,
        64: 2,
        68: 1,
        72: 10,
        76: 1,
        80: 1,
        90: 1,
        96: 5,
        104: 1,
        108: 1,
        144: 1,
        216: 24,
    })

    maximum = max(distribution)
    assert maximum == 216
    winners = [mapping for count, mapping in results if count == maximum]
    assert len(winners) == 24

    # Every perfect-retention winner completely ignores selector S.
    # In q'=a*q+b*S+u and d'=c*q+d*S+v, both S coefficients vanish.
    assert all(mapping[1] == 0 and mapping[3] == 0 for mapping in winners)
    assert all(determinant(mapping) == 0 for mapping in winners)

    # Conversely, no affine bijection exceeds the canonical 20-state
    # first-pass closure from Experiment 266.
    bijective_counts = [
        count for count, mapping in results if determinant(mapping) != 0
    ]
    assert len(bijective_counts) == 432
    assert max(bijective_counts) == 20

    print("Experiment 267")
    print("all affine maps:", len(results))
    print("survivor-count distribution:", dict(sorted(distribution.items())))
    print("maximum retained raw states:", maximum)
    print("perfect-retention maps:", len(winners))
    print("OK: every perfect-retention map erases selector S from both output coordinates")
    print("OK: every perfect-retention map is singular")
    print("OK: affine bijections are bounded at 20 retained states")
    print("RESULT: naked raw-state retention rewards information destruction")
    print("RESULT: shell/address preservation is a substantive model-selection requirement")


if __name__ == "__main__":
    main()

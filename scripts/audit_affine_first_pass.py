#!/usr/bin/env python3
"""Experiment 266: broaden first-pass recursion to coupled affine address maps.

Experiment 253 allowed independent permutations of q and selector depth S.
This audit allows the two ternary coordinates to MIX.

Parent family:
    (q', d') = M * (q, S(j)) + t  over F3

where M is any invertible 2x2 matrix over F3 and t is any translation.
There are |AGL(2,3)| = 48 * 9 = 432 affine bijections.

For each affine map, apply it cellwise to every one of the 216 raw-compatible
machines from Experiment 250. Acceptance criterion is only:
    all three external-q first-pass surfaces decode as valid dash-POS3.

No target state count, expected payloads, p labels, terminal, or solved state
family are used as filters.

Question:
    can coupled q/S mixing preserve more raw-compatible machines than the
    canonical address substitution, or does maximal retention force the
    selector depth coordinate to remain literally S?
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
    load_rows,
    primary_column_candidates,
    primary_symbol,
    q4_selector_candidates,
)


def affine_maps():
    result = []
    for a, b, c, d in product(range(3), repeat=4):
        if (a * d - b * c) % 3 == 0:
            continue
        for u, v in product(range(3), repeat=2):
            result.append((a, b, c, d, u, v))
    assert len(result) == 432
    return tuple(result)


def apply_affine(mapping, q, s):
    a, b, c, d, u, v = mapping
    return (
        (a * q + b * s + u) % 3,
        (c * q + d * s + v) % 3,
    )


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return primary_symbol(payload, residue)


def candidate_surface(payload, selector, mapping, external_q):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                *apply_affine(
                    mapping,
                    external_q,
                    selector_at(selector, row, col),
                ),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def label(mapping):
    a, b, c, d, u, v = mapping
    return f"[[{a},{b}],[{c},{d}]]+({u},{v})"


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]

    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(raw) == 216

    results = []
    for mapping in affine_maps():
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
        0: 402,
        1: 6,
        7: 6,
        10: 12,
        20: 6,
    })

    maximum = max(distribution)
    assert maximum == 20
    winners = [mapping for count, mapping in results if count == maximum]
    assert len(winners) == 6

    # Every maximum-retention map has:
    #   d' = S exactly
    #   q' = a*q + u, where a in {1,2}, u in {0,1,2}
    # i.e. the six affine permutations of the external q labels.
    expected = {
        (a, 0, 0, 1, u, 0)
        for a in (1, 2)
        for u in range(3)
    }
    assert set(winners) == expected

    print("Experiment 266")
    print("coupled affine address maps:", len(results))
    print("raw candidate machines per map:", len(raw))
    print("first-pass survivor-count distribution:", dict(sorted(distribution.items())))
    print("maximum retained raw states:", maximum)
    print("maximum-retention maps:", len(winners))
    for mapping in winners:
        print(" ", label(mapping))
    print("RESULT: no q/S mixing survives at maximum retention")
    print("RESULT: maximal maps force d'=S exactly")
    print("RESULT: remaining freedom is precisely the six affine relabelings of external q")
    print("RESULT: fixing physical q labels leaves the canonical identity map")


if __name__ == "__main__":
    main()

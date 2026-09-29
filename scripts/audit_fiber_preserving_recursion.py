#!/usr/bin/env python3
"""Experiment 268: nonlinear fiber-preserving recursive-operation audit.

Broaden Experiment 266 beyond affine mixing while retaining a clear shell:

    d' = g(S)
    q' = f_S(q)

where:
  * g is any permutation of the three selector-depth labels;
  * each selector value S has its own arbitrary permutation f_S of q.

This is the wreath-product-style family of 6 * 6^3 = 1296 bijections that
preserve selector-depth fibers but allow nonlinear selector-dependent quarter
relabeling.

Crucially, REUSE THE SAME OPERATION on the second pass:
    input pair becomes (S,S), then the same (f_S, g) map is applied.

Filters:
  1. all three first-pass surfaces must decode as dash-POS3;
  2. the reused-operation terminal must decode as dash-POS3.

No target state count or terminal payload is supplied.

Goal:
  determine whether the canonical 14-state family and terminal remain unique
  once selector-dependent q rewrites are admitted.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    generate_master,
    load_rows,
    primary_column_candidates,
    primary_symbol,
    q4_selector_candidates,
)


PERMS = tuple(permutations(range(3)))
IDENTITY = (0, 1, 2)
SWAP_01 = (1, 0, 2)
SWAP_02 = (2, 1, 0)


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return primary_symbol(payload, residue)


def mapped_pair(g, fs, q, s):
    return fs[s][q], g[s]


def first_surface(payload, selector, g, fs, external_q):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                *mapped_pair(
                    g,
                    fs,
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


def terminal_surface(payload, selector, g, fs):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                *mapped_pair(
                    g,
                    fs,
                    selector_at(selector, row, col),
                    selector_at(selector, row, col),
                ),
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
    assert len(raw) == 216

    results = []

    for g in PERMS:
        for fs in product(PERMS, repeat=3):
            first_survivors = []
            for payload, selector in raw:
                first = tuple(
                    decode_dash_pos3(
                        first_surface(payload, selector, g, fs, q)
                    )
                    for q in range(3)
                )
                if None not in first:
                    first_survivors.append((payload, selector, first))

            final = []
            for payload, selector, first in first_survivors:
                terminal = decode_dash_pos3(
                    terminal_surface(payload, selector, g, fs)
                )
                if terminal is not None:
                    final.append((payload, selector, first, terminal))

            results.append((g, fs, first_survivors, final))

    assert len(results) == 1296

    outcome_distribution = Counter(
        (
            len(final),
            len({item[3] for item in final}),
        )
        for _g, _fs, _first, final in results
    )
    assert outcome_distribution == Counter({
        (0, 0): 1080,
        (5, 1): 52,
        (5, 2): 52,
        (7, 1): 36,
        (7, 3): 8,
        (8, 2): 12,
        (8, 3): 8,
        (10, 1): 40,
        (13, 3): 4,
        (14, 1): 4,
    })

    maximum = max(len(final) for _g, _fs, _first, final in results)
    assert maximum == 14

    winners = [
        (g, fs, first, final)
        for g, fs, first, final in results
        if len(final) == maximum
    ]
    assert len(winners) == 4

    expected_fs = {
        (IDENTITY, IDENTITY, IDENTITY),
        (IDENTITY, IDENTITY, SWAP_02),
        (IDENTITY, SWAP_01, IDENTITY),
        (IDENTITY, SWAP_01, SWAP_02),
    }
    assert {g for g, _fs, _first, _final in winners} == {IDENTITY}
    assert {fs for _g, fs, _first, _final in winners} == expected_fs

    # All four operations select exactly the same physical 14-master family.
    master_sets = []
    for _g, _fs, _first, final in winners:
        master_sets.append({
            generate_master(payload, selector)
            for payload, selector, _outputs, _terminal in final
        })
    assert all(len(masters) == 14 for masters in master_sets)
    assert all(masters == master_sets[0] for masters in master_sets[1:])

    # f_1 = swap(0,1) is transition-invisible on the selected physical family.
    # f_2 = swap(0,2) toggles the invariant terminal 100 -> 102.
    terminals_by_fs = {
        fs: {item[3] for item in final}
        for _g, fs, _first, final in winners
    }
    assert terminals_by_fs[(IDENTITY, IDENTITY, IDENTITY)] == {"100"}
    assert terminals_by_fs[(IDENTITY, SWAP_01, IDENTITY)] == {"100"}
    assert terminals_by_fs[(IDENTITY, IDENTITY, SWAP_02)] == {"102"}
    assert terminals_by_fs[(IDENTITY, SWAP_01, SWAP_02)] == {"102"}

    print("Experiment 268")
    print("fiber-preserving nonlinear bijections:", len(results))
    print("outcome distribution (final states, terminal cardinality):")
    for key in sorted(outcome_distribution):
        print(" ", key, "->", outcome_distribution[key])
    print("maximum retained final states:", maximum)
    print("maximum-retention operations:", len(winners))
    for _g, fs, first, final in winners:
        terminals = sorted({item[3] for item in final})
        print(
            "  f_S =",
            fs,
            "first-pass states =",
            len(first),
            "terminal =",
            terminals,
        )
    print("OK: all four winners select the identical canonical 14 physical masters")
    print("RESULT: physical-state reconstruction is robust to this nonlinear family")
    print("RESULT: terminal is not unique without preserving outer q on the first pass")
    print("RESULT: one nonlinear branch toggles the invariant endpoint 100 <-> 102")
    print("RESULT: f_1 swap(0,1) is transition-invisible on the canonical 14-state family")


if __name__ == "__main__":
    main()

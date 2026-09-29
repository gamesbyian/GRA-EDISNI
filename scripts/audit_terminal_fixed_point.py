#!/usr/bin/env python3
"""Experiment 279: select the endpoint by terminal fixed-point stability.

Experiment 268 finds four maximum-retention operations in the 1,296-member
nonlinear selector-fiber-preserving same-operation family. All four recover the
same 14 physical masters:
  * two terminate at 100;
  * two terminate at 102.

Experiment 269 selects the identity operation by requiring address-map
idempotence everywhere. This experiment asks for less.

Behavioral terminal criterion:
  after the second pass produces an invariant POS3 surface, apply the same
  selector-conditioned q rewrite once more to that resulting address. A true
  terminal surface should remain unchanged.

No target payload is supplied. We test only surface fixed-point behavior.
"""

from __future__ import annotations

from itertools import product

from audit_fiber_preserving_recursion import (
    IDENTITY,
    PERMS,
    first_surface,
    frame_symbol,
    mapped_pair,
    selector_at,
    terminal_surface,
)
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    generate_master,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)


def third_surface(payload, selector, g, fs):
    """Apply the same q rewrite once more after the second-pass address."""
    return tuple(
        tuple(
            frame_symbol(
                payload,
                # Second pass begins at q=s and maps to q2=f_s(s).
                # Third pass maps that resulting q2 once more.
                fs[selector_at(selector, row, col)][
                    fs[selector_at(selector, row, col)][
                        selector_at(selector, row, col)
                    ]
                ],
                g[selector_at(selector, row, col)],
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
                second = terminal_surface(payload, selector, g, fs)
                terminal = decode_dash_pos3(second)
                if terminal is None:
                    continue
                final.append((payload, selector, first, terminal, second))

            results.append((g, fs, first_survivors, final))

    maximum = max(len(final) for _g, _fs, _first, final in results)
    assert maximum == 14
    winners = [
        (g, fs, first, final)
        for g, fs, first, final in results
        if len(final) == maximum
    ]
    assert len(winners) == 4

    stable = []
    unstable = []
    for g, fs, first, final in winners:
        transitions = []
        surface_stable = True
        for payload, selector, _outputs, terminal, second in final:
            third = third_surface(payload, selector, g, fs)
            third_payload = decode_dash_pos3(third)
            transitions.append((terminal, third_payload))
            if third != second:
                surface_stable = False

        record = (g, fs, first, final, tuple(transitions))
        (stable if surface_stable else unstable).append(record)

    assert len(stable) == 2
    assert len(unstable) == 2

    # Stable branches have invariant 100 and identical physical masters.
    assert all({item[3] for item in final} == {"100"} for _g, _fs, _first, final, _t in stable)
    stable_master_sets = [
        {
            generate_master(payload, selector)
            for payload, selector, _first, _terminal, _surface in final
        }
        for _g, _fs, _first, final, _t in stable
    ]
    assert stable_master_sets[0] == stable_master_sets[1]
    assert len(stable_master_sets[0]) == 14

    # Unstable branches are exactly the 102 siblings, and another application
    # sends every state to 100.
    assert all({item[3] for item in final} == {"102"} for _g, _fs, _first, final, _t in unstable)
    assert all(
        set(transitions) == {("102", "100")}
        for _g, _fs, _first, _final, transitions in unstable
    )

    # The two stable operations differ only in the already-known f_1 gauge,
    # which is transition-invisible on the selected 14-master family.
    assert {g for g, _fs, _first, _final, _t in stable} == {IDENTITY}
    stable_fs = {fs for _g, fs, _first, _final, _t in stable}
    assert len(stable_fs) == 2
    assert all(fs[0] == IDENTITY and fs[2] == IDENTITY for fs in stable_fs)

    print("Experiment 279")
    print("nonlinear fiber-preserving operations:", len(results))
    print("maximum-retention operations:", len(winners))
    print("surface-stable maximum-retention operations:", len(stable))
    print("surface-unstable maximum-retention operations:", len(unstable))
    print("stable terminals:", sorted({item[3] for _g,_fs,_first,final,_t in stable for item in final}))
    print("unstable second->third transitions:", sorted({pair for _g,_fs,_first,_final,t in unstable for pair in t}))
    print("RESULT: terminal fixed-point stability rejects both 102 endpoint branches")
    print("RESULT: both stable branches terminate at 100 and differ only by transition-invisible f_1 gauge")
    print("RESULT: full address-map idempotence is stronger than needed to select endpoint 100")


if __name__ == "__main__":
    main()

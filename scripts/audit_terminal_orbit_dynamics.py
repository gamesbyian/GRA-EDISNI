#!/usr/bin/env python3
"""Experiment 284: classify repeated-recursion terminal orbits.

Experiment 279 shows that among Experiment 268's four maximum-retention
selector-fiber-preserving operations:
  * two produce terminal 100 and are surface-stable on one extra application;
  * two produce terminal 102 and move to 100 on one extra application.

A tempting interpretation is that all four might converge to 100 under repeated
application. This experiment tests that explicitly.

For each of the four maximum-retention operations, iterate the selector-
conditioned q rewrite after the second pass and decode the resulting surface for
six further steps. No target cycle is supplied.
"""

from __future__ import annotations

from itertools import product

from audit_fiber_preserving_recursion import (
    IDENTITY,
    PERMS,
    first_surface,
    frame_symbol,
    selector_at,
    terminal_surface,
)
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)


def iterated_surface(payload, selector, g, fs, steps_after_second):
    """Surface after second pass plus N further q rewrites.

    Second-pass address starts from (s,s) and applies q'=f_s(s), d'=g(s).
    Each further step applies the same f_s to q while d remains g(s).
    """
    def q_after(s):
        q = fs[s][s]
        for _ in range(steps_after_second):
            q = fs[s][q]
        return q

    return tuple(
        tuple(
            frame_symbol(
                payload,
                q_after(selector_at(selector, row, col)),
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

    winners = []
    for g in PERMS:
        for fs in product(PERMS, repeat=3):
            final = []
            for payload, selector in raw:
                first = tuple(
                    decode_dash_pos3(first_surface(payload, selector, g, fs, q))
                    for q in range(3)
                )
                if None in first:
                    continue
                second = decode_dash_pos3(terminal_surface(payload, selector, g, fs))
                if second is not None:
                    final.append((payload, selector, first, second))
            if len(final) == 14:
                winners.append((g, fs, final))

    assert len(winners) == 4
    assert {g for g, _fs, _final in winners} == {IDENTITY}

    orbit_signatures = {}
    for _g, fs, final in winners:
        state_orbits = set()
        for payload, selector, _first, second in final:
            orbit = [second]
            for extra in range(1, 7):
                surface = iterated_surface(payload, selector, IDENTITY, fs, extra)
                orbit.append(decode_dash_pos3(surface))
            state_orbits.add(tuple(orbit))
        assert len(state_orbits) == 1
        orbit_signatures[fs] = next(iter(state_orbits))

    fixed = {
        fs: orbit
        for fs, orbit in orbit_signatures.items()
        if len(set(orbit)) == 1
    }
    cycling = {
        fs: orbit
        for fs, orbit in orbit_signatures.items()
        if len(set(orbit)) > 1
    }

    assert len(fixed) == 2
    assert len(cycling) == 2
    assert set(fixed.values()) == {("100",) * 7}
    assert set(cycling.values()) == {
        ("102", "100", "102", "100", "102", "100", "102")
    }

    print("Experiment 284")
    print("maximum-retention operations:", len(winners))
    print("fixed operations:", len(fixed))
    print("cycling operations:", len(cycling))
    for fs, orbit in orbit_signatures.items():
        print(" ", fs, "->", orbit)
    print("RESULT: 100 branches are genuine fixed points under repeated recursion")
    print("RESULT: 102 branches lie on an exact period-2 orbit 102<->100")
    print("RESULT: repeated application does not make the wider family converge")
    print("CAUTION: fixed-point stability, not asymptotic convergence, selects endpoint 100")


if __name__ == "__main__":
    main()

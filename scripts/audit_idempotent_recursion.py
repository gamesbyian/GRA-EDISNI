#!/usr/bin/env python3
"""Experiment 269: idempotent-retraction audit in the nonlinear recursion family.

Experiment 268 finds four maximum-retention same-operation recursions over the
1296 selector-fiber-preserving bijections

    d' = g(S)
    q' = f_S(q).

All four recover the same 14 physical masters, but two terminate at 100 and
two at 102.

Experiment 223 characterized the intended first selector pass as a coordinate
RETRACTION/reset. A reset is idempotent: applying the same selector reset
again at the same j must not further alter the address.

This experiment declares idempotence BEFORE examining terminal values and
asks which members of the full 1296-map parent satisfy it and recursive POS3
closure.

Important: idempotence is a structural operation grammar, not a new physical
sticker observation.
"""

from __future__ import annotations

from itertools import product

from audit_fiber_preserving_recursion import (
    IDENTITY,
    PERMS,
    first_surface,
    mapped_pair,
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


def is_idempotent(g, fs):
    """Check F_s(F_s(q)) = F_s(q) for every q,s in the address pair."""
    for q in range(3):
        for s in range(3):
            q1, d1 = mapped_pair(g, fs, q, s)
            # Selector value remains the externally supplied s at fixed j.
            q2, d2 = mapped_pair(g, fs, q1, s)
            if (q2, d2) != (q1, d1):
                return False
    return True


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(raw) == 216

    family = [
        (g, fs)
        for g in PERMS
        for fs in product(PERMS, repeat=3)
    ]
    assert len(family) == 1296

    idempotent = [(g, fs) for g, fs in family if is_idempotent(g, fs)]

    # With f_S restricted to permutations, an idempotent f_S must be identity.
    # g can still be any depth-label permutation, so six maps remain.
    assert len(idempotent) == 6
    assert all(fs == (IDENTITY, IDENTITY, IDENTITY) for _g, fs in idempotent)

    survivors = []
    for g, fs in idempotent:
        final = []
        for payload, selector in raw:
            first = tuple(
                decode_dash_pos3(first_surface(payload, selector, g, fs, q))
                for q in range(3)
            )
            if None in first:
                continue
            terminal = decode_dash_pos3(
                terminal_surface(payload, selector, g, fs)
            )
            if terminal is not None:
                final.append((payload, selector, first, terminal))
        if final:
            survivors.append((g, fs, final))

    assert len(survivors) == 1
    g, fs, final = survivors[0]
    assert g == IDENTITY
    assert fs == (IDENTITY, IDENTITY, IDENTITY)
    assert len(final) == 14
    assert {item[3] for item in final} == {"100"}
    assert len({
        generate_master(payload, selector)
        for payload, selector, _first, _terminal in final
    }) == 14

    print("Experiment 269")
    print("nonlinear fiber-preserving parent:", len(family))
    print("idempotent address resets:", len(idempotent))
    print("idempotent maps with nonempty two-pass POS3 closure:", len(survivors))
    print("surviving operation: g=id, f_0=f_1=f_2=id")
    print("surviving physical masters:", len(final))
    print("terminal:", sorted({item[3] for item in final}))
    print("RESULT: retraction/idempotence selects the canonical operation uniquely")
    print("RESULT: the 102 sibling is excluded because its conditional q swap oscillates")
    print("CAUTION: idempotence is an operation-grammar premise, not independent sticker evidence")


if __name__ == "__main__":
    main()

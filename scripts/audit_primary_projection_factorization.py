#!/usr/bin/env python3
"""Experiment 275: compare primary-coordinate preservation across the 14+14 fork.

Experiment 273 isolated two equally large recursively closed branches inside the
frame-weight-three + horizontal-centroid parent:
  * 14 canonical exact-column-POS3 states;
  * 14 center-column-pileup siblings differing only at q=1,d=0.

Before recursion, the centroid parent contains six raw-compatible primary
payloads in each branch. Those six are naturally indexed by the two unresolved
primary coordinates:
    x = row of (q=0,d=2,col=1) in {1,2}
    y = row of (q=2,d=0,col=1) in {0,1,2}

So each branch begins with the complete 2x3 Cartesian product.

This experiment asks whether recursive closure preserves that primary
projection or forces an otherwise unsupported cross-layer exclusion.
"""

from __future__ import annotations

from collections import Counter

from audit_primary_centroid_sibling import centered_horizontally
from audit_primary_frame_weight_three import (
    exact_column_pos3,
    first_surface,
    frame_candidates,
    enumerate_primary,
    terminal_surface,
)
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


def xy(payload):
    x_rows = [row for row in range(3) if (row, 1) in payload[(0, 2)]]
    y_rows = [row for row in range(3) if (row, 1) in payload[(2, 0)]]
    assert len(x_rows) == 1
    assert len(y_rows) == 1
    return x_rows[0], y_rows[0]


def payload_signature(payload):
    return tuple(
        tuple(sorted(payload[(q, d)]))
        for q in range(3)
        for d in range(3)
    )


def main() -> None:
    rows = load_rows()
    payloads = [
        payload
        for payload in enumerate_primary(frame_candidates(rows))
        if centered_horizontally(payload)
    ]
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    assert len(payloads) == 12

    raw_exact = [payload for payload in payloads if exact_column_pos3(payload)]
    raw_sibling = [payload for payload in payloads if not exact_column_pos3(payload)]
    assert len(raw_exact) == 6
    assert len(raw_sibling) == 6

    full_product = {
        (x, y)
        for x in (1, 2)
        for y in (0, 1, 2)
    }
    assert {xy(payload) for payload in raw_exact} == full_product
    assert {xy(payload) for payload in raw_sibling} == full_product

    survivors = []
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue
            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue
            survivors.append(
                (
                    payload,
                    selector,
                    first,
                    terminal,
                    exact_column_pos3(payload),
                )
            )

    assert len(survivors) == 28

    canonical = [item for item in survivors if item[4]]
    sibling = [item for item in survivors if not item[4]]
    assert len(canonical) == 14
    assert len(sibling) == 14

    canonical_payloads = {
        payload_signature(item[0]): item[0]
        for item in canonical
    }
    sibling_payloads = {
        payload_signature(item[0]): item[0]
        for item in sibling
    }

    assert len(canonical_payloads) == 6
    assert len(sibling_payloads) == 5

    canonical_projection = {xy(payload) for payload in canonical_payloads.values()}
    sibling_projection = {xy(payload) for payload in sibling_payloads.values()}

    assert canonical_projection == full_product
    assert sibling_projection == full_product - {(1, 2)}

    canonical_multiplicity = Counter(xy(item[0]) for item in canonical)
    sibling_multiplicity = Counter(xy(item[0]) for item in sibling)

    assert canonical_multiplicity == Counter({
        (1, 0): 2,
        (1, 1): 2,
        (1, 2): 2,
        (2, 0): 2,
        (2, 1): 2,
        (2, 2): 4,
    })
    assert sibling_multiplicity == Counter({
        (1, 0): 2,
        (1, 1): 2,
        (2, 0): 4,
        (2, 1): 4,
        (2, 2): 2,
    })

    # Both branches have 14 total states and the same terminal. The difference
    # is therefore not a trivial cardinality or endpoint discriminator.
    assert {item[3] for item in canonical} == {"100"}
    assert {item[3] for item in sibling} == {"100"}

    print("Experiment 275")
    print("raw centroid primary payloads:", len(payloads))
    print("raw canonical primary projection:", sorted({xy(p) for p in raw_exact}))
    print("raw sibling primary projection:", sorted({xy(p) for p in raw_sibling}))
    print("canonical recursive states:", len(canonical))
    print("sibling recursive states:", len(sibling))
    print("canonical surviving primary projection:", sorted(canonical_projection))
    print("sibling surviving primary projection:", sorted(sibling_projection))
    print("canonical (x,y) multiplicities:", dict(sorted(canonical_multiplicity.items())))
    print("sibling (x,y) multiplicities:", dict(sorted(sibling_multiplicity.items())))
    print("RESULT: canonical closure preserves the complete raw 2x3 primary product")
    print("RESULT: sibling closure deletes exactly (x=1,y=2)")
    print("RESULT: sibling recovers 14 total states only by redistributing multiplicity")
    print("CAUTION: projection preservation is a structural simplicity criterion, not a raw observation")


if __name__ == "__main__":
    main()

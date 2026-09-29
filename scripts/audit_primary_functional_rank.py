#!/usr/bin/env python3
"""Experiment 276: compare functional rank across the 14+14 primary fork.

Experiments 273-275 isolate two equally large recursively closed branches:
  * canonical distributed-column branch;
  * q=1,d=0 center-column-pileup sibling.

Both have 14 physical states and terminal 100. This experiment asks whether
they preserve the same nontrivial first-pass transducer structure.

No target first-pass payload is supplied. We simply count distinct first-pass
outputs and surviving selector-coordinate variation in each branch.
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
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


def selector_signature(selector):
    return tuple(selector[j] for j in range(9))


def variable_selector_positions(items):
    selectors = [item[1] for item in items]
    return tuple(
        j
        for j in range(9)
        if len({selector[j] for selector in selectors}) > 1
    )


def main() -> None:
    rows = load_rows()
    payloads = [
        payload
        for payload in enumerate_primary(frame_candidates(rows))
        if centered_horizontally(payload)
    ]
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

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

    canonical_outputs = Counter(item[2] for item in canonical)
    sibling_outputs = Counter(item[2] for item in sibling)

    assert canonical_outputs == Counter({
        ("102", "002", "120"): 4,
        ("102", "012", "100"): 4,
        ("102", "022", "100"): 6,
    })
    assert sibling_outputs == Counter({
        ("102", "022", "100"): 14,
    })

    canonical_selector_positions = variable_selector_positions(canonical)
    sibling_selector_positions = variable_selector_positions(sibling)

    assert canonical_selector_positions == (0, 2, 3, 6)
    assert sibling_selector_positions == (2, 6)

    assert tuple(SERIAL_ORDER[j] for j in canonical_selector_positions) == (
        "A", "C", "D", "G"
    )
    assert tuple(SERIAL_ORDER[j] for j in sibling_selector_positions) == (
        "C", "G"
    )

    canonical_selectors = {
        selector_signature(item[1])
        for item in canonical
    }
    sibling_selectors = {
        selector_signature(item[1])
        for item in sibling
    }
    assert len(canonical_selectors) == 6
    assert len(sibling_selectors) == 4

    assert {item[3] for item in canonical} == {"100"}
    assert {item[3] for item in sibling} == {"100"}

    print("Experiment 276")
    print("canonical physical states:", len(canonical))
    print("sibling physical states:", len(sibling))
    print("canonical first-pass rank:", len(canonical_outputs))
    print("canonical first-pass outputs:", dict(canonical_outputs))
    print("sibling first-pass rank:", len(sibling_outputs))
    print("sibling first-pass outputs:", dict(sibling_outputs))
    print(
        "canonical variable selector positions:",
        tuple(SERIAL_ORDER[j] for j in canonical_selector_positions),
    )
    print(
        "sibling variable selector positions:",
        tuple(SERIAL_ORDER[j] for j in sibling_selector_positions),
    )
    print("canonical selector fields:", len(canonical_selectors))
    print("sibling selector fields:", len(sibling_selectors))
    print("RESULT: canonical branch preserves nontrivial first-pass rank 3")
    print("RESULT: sibling branch collapses all 14 states to first-pass rank 1")
    print("RESULT: sibling loses A/D selector-control variation")
    print("CAUTION: preferring nondegenerate transition rank is a structural criterion, not a raw observation")


if __name__ == "__main__":
    main()

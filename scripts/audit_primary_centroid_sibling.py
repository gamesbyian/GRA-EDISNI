#!/usr/bin/env python3
"""Experiment 273: isolate the centered-column primary sibling.

Parent: Experiment 272's 1548 recursively closed machines from the broader
frame-weight-three grammar.

Additional weak directional rule:
  in every primary 3x3 frame, the horizontal first moment of the three
  minority cells is centered:
      sum(column_index) == 3

This permits both:
  * one minority pulse in each of columns 0,1,2;
  * all three minority pulses stacked in the center column.

So it is strictly weaker than exact column POS3.

Question:
  how much ambiguity remains after adding only this centroid constraint?
"""

from __future__ import annotations

from collections import Counter

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


def centered_horizontally(payload):
    return all(
        sum(col for _row, col in payload[(q, d)]) == 3
        for q in range(3)
        for d in range(3)
    )


def bad_frames(payload):
    result = []
    for q in range(3):
        for d in range(3):
            if any(
                sum((row, col) in payload[(q, d)] for row in range(3)) != 1
                for col in range(3)
            ):
                result.append((q, d))
    return tuple(result)


def column_occupancy(payload, q, d):
    return tuple(
        sum((row, col) in payload[(q, d)] for row in range(3))
        for col in range(3)
    )


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary(frame_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    survivors = []
    for payload in payloads:
        if not centered_horizontally(payload):
            continue

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
    assert {item[3] for item in survivors} == {"100"}

    exact = [item for item in survivors if item[4]]
    sibling = [item for item in survivors if not item[4]]
    assert len(exact) == 14
    assert len(sibling) == 14

    assert Counter(bad_frames(item[0]) for item in sibling) == Counter({
        ((1, 0),): 14,
    })
    assert Counter(
        column_occupancy(item[0], 1, 0)
        for item in sibling
    ) == Counter({(0, 3, 0): 14})

    # The only raw cells distinguishing the centered pileup from the canonical
    # q=1,d=0 frame are four currently unobserved residues.
    distinguishing = {28, 33, 34, 35}
    observed_residues = {int(record["residue"]) for record in rows}
    assert distinguishing.isdisjoint(observed_residues)

    print("Experiment 273")
    print("centered first-moment recursive survivors:", len(survivors))
    print("exact column-POS3 states:", len(exact))
    print("center-column sibling states:", len(sibling))
    print("sibling defective frame:", (1, 0))
    print("sibling column occupancy:", (0, 3, 0))
    print("publicly unobserved distinguishing residues:", sorted(distinguishing))
    print("terminal payloads:", sorted({item[3] for item in survivors}))
    print("RESULT: a weak centroid rule collapses the 1548-state parent to a 14+14 fork")
    print("RESULT: the noncanonical fork differs only by center-column pileup in q=1,d=0")
    print("RESULT: the fork is hidden entirely in four currently unobserved primary residues")
    print("CAUTION: centroid symmetry is a bounded grammar, not direct physical evidence")


if __name__ == "__main__":
    main()

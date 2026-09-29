#!/usr/bin/env python3
"""Experiment 274: use raw-supported repeated frames to kill the 14-state sibling.

Experiment 273 reduces the weak frame-weight-three + horizontal-centroid parent
to 28 recursively closed states:
  * 14 canonical exact-column-POS3 states;
  * 14 siblings with a center-column pileup in q=1,d=0.

This experiment asks whether raw observations independently suggest any exact
frame repeats before looking at that fork.

Normalize each observed primary cell to minority/majority using the established
frame polarity. For every pair among the nine (q,d) frames, measure:
  * number of physical cells observed in both frames;
  * number of normalized conflicts on that overlap;
  * union coverage across the two frames.

Among conflict-free frame pairs, select the lexicographically strongest raw
support: maximum overlap, then maximum union coverage.

Question:
  do those raw-nominated repeat hypotheses discriminate the 28-state fork?
"""

from __future__ import annotations

from itertools import combinations

from audit_primary_centroid_sibling import centered_horizontally
from audit_primary_frame_weight_three import (
    exact_column_pos3,
    first_surface,
    frame_candidates,
    enumerate_primary,
    terminal_surface,
)
from enumerate_raw_machine import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


FRAMES = tuple((q, d) for q in range(3) for d in range(3))


def normalized_observations(rows):
    result = {frame: {} for frame in FRAMES}
    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        offset = residue - 1
        q = offset // 27
        d = (offset % 27) // 9
        j = offset % 9
        row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        minority_symbol = "-" if d <= q else "/"
        result[(q, d)][(row, col)] = record["symbol"] == minority_symbol
    return result


def pair_support(observed, left, right):
    left_cells = observed[left]
    right_cells = observed[right]
    overlap = set(left_cells) & set(right_cells)
    conflicts = sum(
        left_cells[cell] != right_cells[cell]
        for cell in overlap
    )
    union = set(left_cells) | set(right_cells)
    return len(overlap), conflicts, len(union)


def frame_mask(payload, frame):
    return payload[frame]


def main() -> None:
    rows = load_rows()
    observed = normalized_observations(rows)

    pair_records = []
    for left, right in combinations(FRAMES, 2):
        overlap, conflicts, union = pair_support(observed, left, right)
        pair_records.append((left, right, overlap, conflicts, union))

    conflict_free = [record for record in pair_records if record[3] == 0]
    assert conflict_free

    max_overlap = max(record[2] for record in conflict_free)
    overlap_best = [record for record in conflict_free if record[2] == max_overlap]
    max_union = max(record[4] for record in overlap_best)
    strongest = [
        record
        for record in overlap_best
        if record[4] == max_union
    ]

    assert max_overlap == 4
    assert max_union == 8
    assert {
        (record[0], record[1])
        for record in strongest
    } == {
        ((0, 1), (1, 0)),
        ((1, 2), (2, 2)),
    }

    payloads = list(enumerate_primary(frame_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    centroid_survivors = []
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
            centroid_survivors.append(
                (payload, selector, first, terminal, exact_column_pos3(payload))
            )

    assert len(centroid_survivors) == 28

    repeated = [
        item
        for item in centroid_survivors
        if all(
            frame_mask(item[0], left) == frame_mask(item[0], right)
            for left, right, _overlap, _conflicts, _union in strongest
        )
    ]

    assert len(repeated) == 14
    assert all(item[4] for item in repeated)
    assert {item[3] for item in repeated} == {"100"}

    siblings = [item for item in centroid_survivors if not item[4]]
    assert len(siblings) == 14
    assert all(
        frame_mask(item[0], (0, 1)) != frame_mask(item[0], (1, 0))
        for item in siblings
    )
    assert all(
        frame_mask(item[0], (1, 2)) == frame_mask(item[0], (2, 2))
        for item in siblings
    )

    print("Experiment 274")
    print("conflict-free normalized frame pairs:", len(conflict_free))
    print("maximum shared observed cells:", max_overlap)
    print("maximum union coverage at that overlap:", max_union)
    print("strongest raw-supported repeat pairs:")
    for record in strongest:
        print(" ", record)
    print("centroid-recursive parent:", len(centroid_survivors))
    print("states satisfying all strongest raw-supported repeats:", len(repeated))
    print("exact POS3 among repeat-selected states:", sum(item[4] for item in repeated))
    print("RESULT: raw observations nominate exactly two strongest repeated-frame motifs")
    print("RESULT: enforcing both motifs selects the canonical 14 states from the 14+14 fork")
    print("RESULT: the center-column sibling is rejected by q0,d1 == q1,d0")
    print("CAUTION: promoting compatible partial repeats to exact frame equality remains a grammar inference")


if __name__ == "__main__":
    main()

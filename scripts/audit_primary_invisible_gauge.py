#!/usr/bin/env python3
"""Experiment 280: isolate the transition-invisible primary completion gauge.

Parent: Experiment 272's frame-weight-three primary grammar plus raw Q4
selectors and canonical two-pass recursion.

The broad parent contains many non-POS3 machines, so this audit does NOT claim
global uniqueness. Instead it asks a narrower adversarial question:

  Which occupancy-signature families reproduce the canonical machine's
  operational invariants simultaneously?
    * 14 recursively closed physical states;
    * the same three first-pass functional outputs with 4/4/6 multiplicities;
    * six distinct selector fields;
    * the complete six-element raw primary (x,y) projection;
    * terminal 100 for all states.

Then inspect whether the surviving alternatives alter cells that recursion can
ever address.

This intentionally distinguishes "same transducer" from "same physical master."
"""

from __future__ import annotations

from collections import Counter, defaultdict

from audit_primary_frame_weight_three import (
    exact_column_pos3,
    first_surface,
    frame_candidates,
    enumerate_primary,
    terminal_surface,
)
from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


CANONICAL_FIRST = Counter({
    ("102", "002", "120"): 4,
    ("102", "012", "100"): 4,
    ("102", "022", "100"): 6,
})
REGISTER_RESIDUES = (
    22, 25, 55, 58, 61, 84, 88, 91, 94, 100, 102, 103, 106
)


def occupancy_signature(payload):
    return tuple(
        tuple(
            sum((row, col) in payload[(q, d)] for row in range(3))
            for col in range(3)
        )
        for q in range(3)
        for d in range(3)
    )


def payload_signature(payload):
    return tuple(
        tuple(sorted(payload[(q, d)]))
        for q in range(3)
        for d in range(3)
    )


def xy(payload):
    x_rows = [row for row in range(3) if (row, 1) in payload[(0, 2)]]
    y_rows = [row for row in range(3) if (row, 1) in payload[(2, 0)]]
    if len(x_rows) != 1 or len(y_rows) != 1:
        return None
    return x_rows[0], y_rows[0]


def selector_signature(selector):
    return tuple(selector[j] for j in range(9))


def primary_symbol(payload, residue):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    minority = (row, col) in payload[(q, d)]
    if minority:
        return "-" if d <= q else "/"
    return "/" if d <= q else "-"


def q4_symbol(selector, residue):
    offset = residue - 82
    depth = offset // 9
    j = offset % 9
    return "/" if selector[j] == depth else "."


def master(payload, selector):
    return "".join(
        primary_symbol(payload, residue)
        if residue <= 81
        else q4_symbol(selector, residue)
        for residue in range(1, 109)
    )


def defect_frames(signature):
    return tuple(
        (divmod(index, 3), occupancy)
        for index, occupancy in enumerate(signature)
        if occupancy != (1, 1, 1)
    )


def residue_for(q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    return 1 + 27 * q + 9 * d + j


def main() -> None:
    rows = load_rows()
    observed_residues = {int(record["residue"]) for record in rows}
    payloads = list(enumerate_primary(frame_candidates(rows)))
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
            survivors.append((payload, selector, first, terminal))

    assert len(survivors) == 1548

    by_occupancy = defaultdict(list)
    for item in survivors:
        by_occupancy[occupancy_signature(item[0])].append(item)
    assert len(by_occupancy) == 84

    full_xy = {(x, y) for x in (1, 2) for y in (0, 1, 2)}
    equivalent = []

    for signature, items in by_occupancy.items():
        first_counts = Counter(item[2] for item in items)
        selector_fields = {selector_signature(item[1]) for item in items}
        unique_payloads = {
            payload_signature(item[0]): item[0]
            for item in items
        }
        projection = {
            xy(payload)
            for payload in unique_payloads.values()
        }

        if (
            len(items) == 14
            and first_counts == CANONICAL_FIRST
            and len(selector_fields) == 6
            and len(unique_payloads) == 6
            and projection == full_xy
            and {item[3] for item in items} == {"100"}
        ):
            equivalent.append((signature, items))

    assert len(equivalent) == 4

    defect_sets = {defect_frames(signature) for signature, _items in equivalent}
    assert defect_sets == {
        (),
        (((0, 0), (2, 1, 0)),),
        (((1, 1), (0, 1, 2)),),
        (
            ((0, 0), (2, 1, 0)),
            ((1, 1), (0, 1, 2)),
        ),
    }

    canonical_items = next(
        items
        for signature, items in equivalent
        if not defect_frames(signature)
    )
    canonical_payloads = {
        xy(payload): payload
        for payload in {
            payload_signature(item[0]): item[0]
            for item in canonical_items
        }.values()
    }

    # Compare each gauge setting to the canonical payload at fixed (x,y).
    changed_residues = set()
    changed_cells = set()
    for signature, items in equivalent:
        payload_map = {
            xy(payload): payload
            for payload in {
                payload_signature(item[0]): item[0]
                for item in items
            }.values()
        }
        assert set(payload_map) == full_xy

        for key in full_xy:
            canonical = canonical_payloads[key]
            alternate = payload_map[key]
            for q in range(3):
                for d in range(3):
                    symmetric = canonical[(q, d)] ^ alternate[(q, d)]
                    for row, col in symmetric:
                        changed_cells.add((q, d, row, col))
                        changed_residues.add(residue_for(q, d, row, col))

    assert changed_residues == {6, 8, 41, 45}
    assert changed_residues.isdisjoint(observed_residues)

    # The two independent gauge flips are:
    #   q0,d0: move the minority pulse H -> F (residue 8 -> 6)
    #   q1,d1: move the minority pulse I -> E (residue 45 -> 41)
    assert changed_cells == {
        (0, 0, 2, 0),  # F -> residue 6
        (0, 0, 2, 2),  # H -> residue 8
        (1, 1, 0, 0),  # I -> residue 45
        (1, 1, 1, 2),  # E -> residue 41
    }

    # Prove that every changed cell is unreachable by the selector at that
    # frame. Selector values at F/H are never 0; at I/E they are never 1.
    selector_values = {
        (row, col): {
            selector[SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col])]
            for selector in selectors
        }
        for row in range(3)
        for col in range(3)
    }
    assert selector_values[(2, 0)] == {1}       # F
    assert selector_values[(2, 2)] == {2}       # H
    assert selector_values[(0, 0)] == {2}       # I
    assert selector_values[(1, 2)] == {0}       # E

    for q, d, row, col in changed_cells:
        assert d not in selector_values[(row, col)]

    # Every gauge setting keeps the same 13 variable state-register residues,
    # same global symbol census, and 14 distinct masters.
    branch_master_sets = []
    for _signature, items in equivalent:
        masters = [master(payload, selector) for payload, selector, _f, _t in items]
        assert len(set(masters)) == 14
        variable = [
            residue
            for residue in range(1, 109)
            if len({word[residue - 1] for word in masters}) > 1
        ]
        assert tuple(variable) == REGISTER_RESIDUES
        assert all(
            Counter(word) == Counter({"/": 54, "-": 36, ".": 18})
            for word in masters
        )
        branch_master_sets.append(set(masters))

    assert len(set.union(*branch_master_sets)) == 56

    union_masters = set.union(*branch_master_sets)
    union_variable = [
        residue
        for residue in range(1, 109)
        if len({word[residue - 1] for word in union_masters}) > 1
    ]
    assert union_variable == [
        6, 8,
        22, 25,
        41, 45,
        55, 58, 61,
        84, 88, 91, 94, 100, 102, 103, 106,
    ]

    print("Experiment 280")
    print("frame-weight-three recursively closed states:", len(survivors))
    print("occupancy-signature families:", len(by_occupancy))
    print("operationally canonical-equivalent families:", len(equivalent))
    for signature, _items in sorted(equivalent, key=lambda item: repr(defect_frames(item[0]))):
        print(" ", defect_frames(signature))
    print("gauge-affected residues:", sorted(changed_residues))
    print("observed among gauge residues:", sorted(changed_residues & observed_residues))
    print("complete masters across four gauge settings:", len(union_masters))
    print("within-setting variable register:", list(REGISTER_RESIDUES))
    print("across-gauge variable residues:", union_variable)
    print("RESULT: the preferred transducer has a two-bit transition-invisible primary completion gauge")
    print("RESULT: gauge flips are H<->F at q0,d0 and I<->E at q1,d1")
    print("RESULT: all four changed residues are unobserved and unreachable by every raw-compatible selector")
    print("RESULT: exact column POS3 fixes this physical gauge but is not required for the transducer behavior")


if __name__ == "__main__":
    main()

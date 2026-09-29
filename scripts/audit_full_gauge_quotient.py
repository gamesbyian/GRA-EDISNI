#!/usr/bin/env python3
"""Experiment 286: compose the remaining transition-invisible gauges.

By Experiment 285 the preferred transducer has three independent gauge layers:

Physical primary gauge (Experiment 280):
  * 2 bits -> 4 settings
  * swaps fixed minority pulses at residues 6<->8 and 41<->45

Physical Q4 polarity gauge (Experiment 260):
  * 3 bits -> 8 settings
  * generators A, C, and coupled F+I stack-polarity flips

Recursive operation gauge (Experiment 285):
  * 1 bit -> identity vs f_1 swap(0,1)
  * no physical-master change

This experiment composes the physical gauges explicitly over all 14 legal
hidden states, checks corpus compatibility, counts distinct masters, and then
adds the operation bit algebraically.

The goal is to state the machine as a quotient: one functional transducer
modulo transition-invisible representation freedoms.
"""

from __future__ import annotations

from itertools import product

from audit_q4_polarity_gauge import A, C, FI, xor_span
from enumerate_raw_machine import load_rows
from generate_master import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    legal_states,
    primary_payload_lattice,
    q4_selector_field,
)


PRIMARY_SETTINGS = tuple(product((False, True), repeat=2))
Q4_MASKS = tuple(sorted(xor_span((A, C, FI))))


def primary_cells(state, q, d, primary_setting):
    g0, g1 = primary_setting
    word = primary_payload_lattice(state)[q][d]
    cells = {(int(word[col]), col) for col in range(3)}

    if g0 and (q, d) == (0, 0):
        cells.remove((2, 2))  # H
        cells.add((2, 0))     # F

    if g1 and (q, d) == (1, 1):
        cells.remove((0, 0))  # I
        cells.add((1, 2))     # E

    return frozenset(cells)


def primary_symbol_gauged(state, residue, primary_setting):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]

    minority = (row, col) in primary_cells(state, q, d, primary_setting)
    minority_is_dash = d <= q
    if minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def q4_symbol_gauged(state, residue, polarity_mask):
    offset = residue - 82
    depth = offset // 9
    j = offset % 9
    letter = SERIAL_ORDER[j]
    row, col = PHYSICAL_POSITION[letter]
    selected = q4_selector_field(state)[row][col]

    dot_exception = bool(polarity_mask & (1 << j))
    exceptional = "." if dot_exception else "/"
    background = "/" if dot_exception else "."
    return exceptional if depth == selected else background


def master(state, primary_setting, polarity_mask):
    return "".join(
        primary_symbol_gauged(state, residue, primary_setting)
        if residue <= 81
        else q4_symbol_gauged(state, residue, polarity_mask)
        for residue in range(1, 109)
    )


def main() -> None:
    states = legal_states()
    rows = load_rows()
    assert len(states) == 14
    assert len(PRIMARY_SETTINGS) == 4
    assert len(Q4_MASKS) == 8

    physical_settings = tuple(product(PRIMARY_SETTINGS, Q4_MASKS))
    assert len(physical_settings) == 32

    masters_by_setting = {}
    for primary_setting, polarity_mask in physical_settings:
        masters = {
            master(state, primary_setting, polarity_mask)
            for state in states
        }
        assert len(masters) == 14

        # Every physical gauge setting remains compatible with the classified
        # public corpus.
        for record in rows:
            residue = int(record["residue"])
            symbol = record["symbol"]
            assert all(word[residue - 1] == symbol for word in masters)

        masters_by_setting[(primary_setting, polarity_mask)] = masters

    # Supports are disjoint and every setting yields a distinct physical family.
    assert len({
        frozenset(masters)
        for masters in masters_by_setting.values()
    }) == 32

    union_masters = set().union(*masters_by_setting.values())
    assert len(union_masters) == 32 * 14 == 448

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
        82, 84, 87, 88, 90, 91, 93, 94, 96, 99, 100, 102, 103, 105, 106, 108,
    ]

    physical_gauge_bits = 5
    operation_gauge_bits = 1
    total_gauge_settings = 2 ** (physical_gauge_bits + operation_gauge_bits)
    assert total_gauge_settings == 64

    # The f_1 bit changes only the recursive address rule, not the physical
    # master, so it doubles machine representations but not master count.
    machine_state_representations = len(union_masters) * 2
    assert machine_state_representations == 896

    print("Experiment 286")
    print("primary physical gauge settings:", len(PRIMARY_SETTINGS))
    print("Q4 physical gauge settings:", len(Q4_MASKS))
    print("combined physical gauge settings:", len(physical_settings))
    print("distinct complete masters:", len(union_masters))
    print("union-variable residues:", union_variable)
    print("operation gauge settings:", 2)
    print("total six-bit gauge settings:", total_gauge_settings)
    print("state-operation representations:", machine_state_representations)
    print("RESULT: remaining freedoms compose as a six-bit gauge")
    print("RESULT: five physical bits yield 32 x 14 = 448 corpus-compatible masters")
    print("RESULT: the f1 operation bit doubles representations without changing physical masters")
    print("RESULT: closed-corpus uniqueness is naturally stated modulo this gauge quotient")


if __name__ == "__main__":
    main()

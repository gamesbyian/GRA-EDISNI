#!/usr/bin/env python3
"""Experiment 287: correct Experiment 286 by auditing cross-gauge coupling.

Experiment 286 incorrectly assumed the primary physical gauge and Q4 polarity
gauge composed as an independent direct product while keeping canonical
selector depths fixed.

That is false. Alternate Q4 polarity words can require different exceptional
depths to remain raw-compatible, so the selector field must be re-enumerated
for each polarity word.

This correction jointly enumerates:
  * 4 primary completion settings from Experiment 280;
  * 8 transition-preserving Q4 polarity words from Experiment 260;
  * all raw-compatible selector-depth completions for each polarity;
  * canonical two-pass recursive POS3 closure.

It then measures:
  * which 4x8 physical combinations actually survive;
  * which preserve the exact canonical first-pass transducer;
  * whether the f_1 operation gauge remains invisible across the joint family;
  * the number of distinct corpus-compatible physical masters.

Experiment 286's six-bit direct-product claim is superseded by this audit.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_primary_frame_weight_three import first_surface, terminal_surface
from audit_q4_polarity_gauge import A, C, FI, xor_span
from audit_q4_pos3_polarity import DOT, SLASH, local_options, q4_observations
from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    load_rows,
)


CANONICAL_FIRST = Counter({
    ("102", "002", "120"): 4,
    ("102", "012", "100"): 4,
    ("102", "022", "100"): 6,
})
FI_FIRST = Counter({
    ("102", "202", "120"): 4,
    ("102", "212", "100"): 4,
    ("102", "222", "100"): 6,
})


def payload(x, y, flip_q0d0, flip_q1d1):
    words = (
        ("112", "212", f"0{x}0"),
        ("212", "002", "100"),
        (f"1{y}2", "022", "100"),
    )
    result = {}
    for q in range(3):
        for d in range(3):
            cells = {(int(words[q][d][col]), col) for col in range(3)}
            if flip_q0d0 and (q, d) == (0, 0):
                cells.remove((2, 2))  # H
                cells.add((2, 0))     # F
            if flip_q1d1 and (q, d) == (1, 1):
                cells.remove((0, 0))  # I
                cells.add((1, 2))     # E
            result[(q, d)] = frozenset(cells)
    return result


def polarity(mask):
    return tuple(
        DOT if mask & (1 << j) else SLASH
        for j in range(9)
    )


def selector_candidates(options, polarity_word):
    depth_choices = []
    for j, exceptional_symbol in enumerate(polarity_word):
        depths = tuple(sorted({
            depth
            for depth, symbol, _pattern in options[j]
            if symbol == exceptional_symbol
        }))
        assert depths
        depth_choices.append(depths)
    return tuple(
        dict(enumerate(values))
        for values in product(*depth_choices)
    )


def primary_symbol(payload_map, residue):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    minority = (row, col) in payload_map[(q, d)]
    minority_is_dash = d <= q
    if minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def q4_symbol(selector, polarity_word, residue):
    offset = residue - 82
    depth = offset // 9
    j = offset % 9
    exceptional = polarity_word[j]
    background = DOT if exceptional == SLASH else SLASH
    return exceptional if depth == selector[j] else background


def master(payload_map, selector, polarity_word):
    return "".join(
        primary_symbol(payload_map, residue)
        if residue <= 81
        else q4_symbol(selector, polarity_word, residue)
        for residue in range(1, 109)
    )


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def f1_first_surface(payload_map, selector, external_q):
    result = []
    for row in range(3):
        line = []
        for col in range(3):
            s = selector_at(selector, row, col)
            q = external_q
            if s == 1 and q in (0, 1):
                q = 1 - q
            # Inline the frame read used by first_surface.
            letter = PHYSICAL_LAYOUT[row][col]
            j = SERIAL_ORDER.index(letter)
            residue = 1 + 27 * q + 9 * s + j
            line.append(primary_symbol(payload_map, residue))
        result.append(tuple(line))
    return tuple(result)


def f1_terminal_surface(payload_map, selector):
    result = []
    for row in range(3):
        line = []
        for col in range(3):
            s = selector_at(selector, row, col)
            q = 0 if s == 1 else s  # f_1 swaps input q=1 -> 0
            letter = PHYSICAL_LAYOUT[row][col]
            j = SERIAL_ORDER.index(letter)
            residue = 1 + 27 * q + 9 * s + j
            line.append(primary_symbol(payload_map, residue))
        result.append(tuple(line))
    return tuple(result)


def main() -> None:
    rows = load_rows()
    observed = {int(record["residue"]): record["symbol"] for record in rows}
    options = local_options(q4_observations(rows))

    primary_settings = tuple(product((False, True), repeat=2))
    q4_masks = tuple(sorted(xor_span((A, C, FI))))
    assert len(primary_settings) == 4
    assert len(q4_masks) == 8

    records = {}
    physical_master_sets = {}

    for primary_setting in primary_settings:
        payloads = [
            payload(x, y, *primary_setting)
            for x in (1, 2)
            for y in (0, 1, 2)
        ]

        for mask in q4_masks:
            pword = polarity(mask)
            selectors = selector_candidates(options, pword)
            final = []

            for payload_map in payloads:
                for selector in selectors:
                    first = tuple(
                        decode_dash_pos3(first_surface(payload_map, selector, q))
                        for q in range(3)
                    )
                    if None in first:
                        continue
                    terminal = decode_dash_pos3(
                        terminal_surface(payload_map, selector)
                    )
                    if terminal is None:
                        continue
                    final.append((payload_map, selector, first, terminal))

            records[(primary_setting, mask)] = final

            if final:
                masters = {
                    master(payload_map, selector, pword)
                    for payload_map, selector, _first, _terminal in final
                }
                physical_master_sets[(primary_setting, mask)] = masters

                assert len(final) == 14
                assert len(masters) == 14
                assert {item[3] for item in final} == {"100"}

                for residue, symbol in observed.items():
                    assert all(word[residue - 1] == symbol for word in masters)

    viable = {
        key: final
        for key, final in records.items()
        if final
    }
    dead = {
        key
        for key, final in records.items()
        if not final
    }

    assert len(viable) == 24
    assert len(dead) == 8

    # The only forbidden cross-gauge combination is:
    # primary q0,d0 H->F flip ON together with Q4 F+I polarity gauge ON.
    expected_dead = {
        (primary_setting, mask)
        for primary_setting in primary_settings
        for mask in q4_masks
        if primary_setting[0] and (mask & FI) == FI
    }
    assert dead == expected_dead

    exact = {}
    altered = {}
    for key, final in viable.items():
        first_counts = Counter(item[2] for item in final)
        mask = key[1]
        if (mask & FI) == FI:
            assert first_counts == FI_FIRST
            altered[key] = final
        else:
            assert first_counts == CANONICAL_FIRST
            exact[key] = final

    assert len(exact) == 16
    assert len(altered) == 8

    # f_1 remains exactly invisible across every viable physical setting.
    for (primary_setting, mask), final in viable.items():
        for payload_map, selector, first, terminal in final:
            f1_first = tuple(
                decode_dash_pos3(
                    f1_first_surface(payload_map, selector, q)
                )
                for q in range(3)
            )
            f1_terminal = decode_dash_pos3(
                f1_terminal_surface(payload_map, selector)
            )
            assert f1_first == first
            assert f1_terminal == terminal

    assert len({
        frozenset(masters)
        for masters in physical_master_sets.values()
    }) == 24

    union_masters = set().union(*physical_master_sets.values())
    assert len(union_masters) == 336

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
        82, 84, 88, 91, 93, 94, 99, 100, 102, 103, 105, 106,
    ]

    # Exact canonical-transducer gauge:
    # primary two bits + Q4 A/C two bits + f1 operation bit = five bits.
    exact_physical_settings = len(exact)
    assert exact_physical_settings == 16
    exact_physical_masters = set().union(
        *(physical_master_sets[key] for key in exact)
    )
    assert len(exact_physical_masters) == 224

    exact_representation_settings = exact_physical_settings * 2
    assert exact_representation_settings == 32

    # Broader recursive family adds the coupled F+I branch.
    all_representation_settings = len(viable) * 2
    assert all_representation_settings == 48
    state_operation_representations = len(union_masters) * 2
    assert state_operation_representations == 672

    print("Experiment 287 (corrects Experiment 286)")
    print("primary settings:", len(primary_settings))
    print("Q4 transition-preserving polarity settings:", len(q4_masks))
    print("joint physical combinations:", len(records))
    print("viable combinations:", len(viable))
    print("dead combinations:", len(dead))
    print("exact canonical-first-pass physical settings:", len(exact))
    print("coupled F+I alternative physical settings:", len(altered))
    print("distinct viable complete masters:", len(union_masters))
    print("exact-transducer physical masters:", len(exact_physical_masters))
    print("exact-transducer representation settings incl f1:", exact_representation_settings)
    print("all viable representation settings incl f1:", all_representation_settings)
    print("all viable state-operation representations:", state_operation_representations)
    print("union-variable residues:", union_variable)
    print("RESULT: Experiment 286's six-bit direct product is false")
    print("RESULT: primary q0,d0 flip and Q4 F+I polarity flip are mutually incompatible")
    print("RESULT: exact canonical transducer has a five-bit gauge (four physical + f1)")
    print("RESULT: eight extra F+I settings preserve 14 states/rank/100 but alter first-pass words")


if __name__ == "__main__":
    main()

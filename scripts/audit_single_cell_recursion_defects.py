#!/usr/bin/env python3
"""Experiment 296: audit one-cell defects around the canonical recursion.

Purpose
-------
Probe the smallest pass-specific deviations from the established two-pass
selector operation without changing the primary code, Q4 code, carrier, or raw
candidate family.

Parent machine space:
    216 raw-compatible primary x Q4 candidates from Experiment 250.

Canonical operation:
    first pass:  (q, S(j), j)
    second pass: (S(j), S(j), j)

Defect family:
    choose exactly one physical A-I cell j and one nonzero ternary offset
    delta in {+1,+2}; apply it to exactly one coordinate role:

    1. first_d:  first-pass selected depth S(j)+delta
    2. second_q: second-pass quarter S(j)+delta
    3. second_d: second-pass depth S(j)+delta

That is 9 cells x 2 offsets x 3 roles = 54 one-defect operations.

Filters:
    * all three first-pass surfaces must decode as dash-POS3;
    * the second-pass surface must decode as dash-POS3.

No target state count, terminal value, route shell, or expected master set is
used as a filter.

Questions:
    * can any one-cell defect retain more raw-compatible states than canonical?
    * can a defect preserve the exact canonical 14-state transducer?
    * if exact mimics exist, are they true symbol-equality gauges?
    * does any higher-retention sibling preserve the reversible route structure?
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    generate_master,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
)


KINDS = ("first_d", "second_q", "second_d")
DELTAS = (1, 2)


def apply_offset(value, delta):
    return (value + delta) % 3


def first_surface(payload, selector, external_q, defect=None):
    rows = []
    for row in range(3):
        line = []
        for col in range(3):
            letter = PHYSICAL_LAYOUT[row][col]
            j = SERIAL_ORDER.index(letter)
            s = selector_at_physical_cell(selector, row, col)
            d = s
            if defect is not None:
                kind, defect_j, delta = defect
                if kind == "first_d" and j == defect_j:
                    d = apply_offset(d, delta)
            line.append(frame_symbol(payload, external_q, d, row, col))
        rows.append(tuple(line))
    return tuple(rows)


def second_surface(payload, selector, defect=None):
    rows = []
    for row in range(3):
        line = []
        for col in range(3):
            letter = PHYSICAL_LAYOUT[row][col]
            j = SERIAL_ORDER.index(letter)
            s = selector_at_physical_cell(selector, row, col)
            q = s
            d = s
            if defect is not None:
                kind, defect_j, delta = defect
                if j == defect_j:
                    if kind == "second_q":
                        q = apply_offset(q, delta)
                    elif kind == "second_d":
                        d = apply_offset(d, delta)
            line.append(frame_symbol(payload, q, d, row, col))
        rows.append(tuple(line))
    return tuple(rows)


def evaluate(raw, defect=None):
    final = []
    for payload, selector in raw:
        first = tuple(
            decode_dash_pos3(first_surface(payload, selector, q, defect))
            for q in range(3)
        )
        if None in first:
            continue
        terminal_surface = second_surface(payload, selector, defect)
        terminal = decode_dash_pos3(terminal_surface)
        if terminal is None:
            continue
        final.append((payload, selector, first, terminal, terminal_surface))
    return final


def machine_key(item):
    payload, selector = item[:2]
    return (
        tuple(sorted(payload.items())),
        tuple(sorted(selector.items())),
    )


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]

    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(raw) == 216

    canonical = evaluate(raw)
    assert len(canonical) == 14
    assert Counter(item[3] for item in canonical) == Counter({"100": 14})
    canonical_keys = {machine_key(item) for item in canonical}
    canonical_masters = {
        generate_master(item[0], item[1])
        for item in canonical
    }
    assert len(canonical_masters) == 14

    results = []
    for kind in KINDS:
        for j in range(9):
            for delta in DELTAS:
                defect = (kind, j, delta)
                final = evaluate(raw, defect)
                terminal_counts = Counter(item[3] for item in final)
                keys = {machine_key(item) for item in final}
                results.append({
                    "defect": defect,
                    "final": final,
                    "states": len(final),
                    "terminal_counts": terminal_counts,
                    "terminal_cardinality": len(terminal_counts),
                    "exact_machine_family": keys == canonical_keys,
                })

    assert len(results) == 54

    # Coarse robustness anatomy by coordinate role.
    survivor_distributions = {}
    for kind in KINDS:
        survivor_distributions[kind] = Counter(
            result["states"]
            for result in results
            if result["defect"][0] == kind
        )

    assert survivor_distributions == {
        "first_d": Counter({0: 10, 10: 2, 7: 2, 16: 1, 4: 1, 8: 1, 6: 1}),
        "second_q": Counter({14: 6, 0: 5, 8: 2, 7: 2, 10: 1, 18: 1, 16: 1}),
        "second_d": Counter({0: 9, 6: 2, 14: 2, 4: 2, 10: 1, 7: 1, 8: 1}),
    }

    # Seven local defects preserve exactly the same 14 physical machines,
    # identical terminal surface, and terminal 100.
    exact = [
        result
        for result in results
        if result["exact_machine_family"]
        and result["terminal_counts"] == Counter({"100": 14})
    ]
    exact_specs = {
        (kind, SERIAL_ORDER[j], delta)
        for result in exact
        for kind, j, delta in (result["defect"],)
    }
    assert exact_specs == {
        ("second_q", "E", 1),
        ("second_q", "E", 2),
        ("second_q", "F", 1),
        ("second_q", "F", 2),
        ("second_q", "I", 1),
        ("second_d", "C", 1),
        ("second_d", "I", 1),
    }

    canonical_by_key = {machine_key(item): item for item in canonical}
    for result in exact:
        defect = result["defect"]
        for item in result["final"]:
            key = machine_key(item)
            canonical_item = canonical_by_key[key]
            assert item[4] == canonical_item[4]

    # Explain those exact mimics as equality-locus gauges: at the one changed
    # terminal address, the alternate source symbol equals the canonical source
    # symbol for every one of the 14 machines.
    equality_support = {}
    for result in exact:
        kind, j, delta = result["defect"]
        letter = SERIAL_ORDER[j]
        row, col = PHYSICAL_POSITION[letter]
        support = Counter()
        for payload, selector, _first, _terminal, _surface in canonical:
            s = selector[j]
            q0 = d0 = s
            q1, d1 = q0, d0
            if kind == "second_q":
                q1 = apply_offset(q1, delta)
            else:
                d1 = apply_offset(d1, delta)
            before = frame_symbol(payload, q0, d0, row, col)
            after = frame_symbol(payload, q1, d1, row, col)
            assert before == after
            support[(s, before)] += 1
        equality_support[(kind, letter, delta)] = support

    assert equality_support == {
        ("second_q", "E", 1): Counter({(0, "/"): 14}),
        ("second_q", "E", 2): Counter({(0, "/"): 14}),
        ("second_q", "F", 1): Counter({(1, "/"): 14}),
        ("second_q", "F", 2): Counter({(1, "/"): 14}),
        ("second_q", "I", 1): Counter({(2, "/"): 14}),
        ("second_d", "C", 1): Counter({(0, "-"): 7, (2, "-"): 7}),
        ("second_d", "I", 1): Counter({(2, "/"): 14}),
    }

    # Only one first-pass one-cell defect beats canonical state retention while
    # still producing an invariant terminal: A depth +1 retains 16 states, all
    # terminal 100. But it expands the functional quotient from 3 to 5 first-
    # pass families, and one family has no reversible ternary word at any q.
    # It therefore cannot supply a reversible route for every functional class.
    higher_invariant = [
        result
        for result in results
        if result["states"] > len(canonical)
        and result["terminal_cardinality"] == 1
    ]
    assert len(higher_invariant) == 1
    sibling = higher_invariant[0]
    assert sibling["defect"] == ("first_d", SERIAL_ORDER.index("A"), 1)
    assert sibling["states"] == 16
    assert sibling["terminal_counts"] == Counter({"100": 16})

    sibling_families = sorted({item[2] for item in sibling["final"]})
    assert sibling_families == [
        ("102", "012", "100"),
        ("102", "022", "100"),
        ("112", "012", "100"),
        ("112", "012", "120"),
        ("122", "022", "100"),
    ]
    reversible_choices = [
        tuple(word for word in family if is_permutation(word))
        for family in sibling_families
    ]
    assert reversible_choices == [
        ("102", "012"),
        ("102",),
        ("012",),
        ("012", "120"),
        (),
    ]

    print("Experiment 296")
    print("raw candidate machines:", len(raw))
    print("one-cell defect operations:", len(results))
    print("survivor distributions by role:")
    for kind in KINDS:
        print(" ", kind, dict(sorted(survivor_distributions[kind].items())))
    print("exact canonical-transducer local gauges:", len(exact))
    for spec in sorted(exact_specs):
        print(" ", spec, dict(equality_support[spec]))
    print("higher-retention invariant-terminal siblings:", len(higher_invariant))
    print("  A first-depth +1 states:", sibling["states"])
    print("  A first-depth +1 terminal:", dict(sibling["terminal_counts"]))
    print("  A first-depth +1 first-pass families:", sibling_families)
    print("RESULT: no one-cell first-pass defect preserves the exact canonical machine")
    print("RESULT: seven second-pass defects are true symbol-equality gauges")
    print("RESULT: the sole invariant sibling with >14 states is route-degenerate")
    print("RESULT: allowing cell-specific pass exceptions creates gauge freedom faster than explanatory gain")


if __name__ == "__main__":
    main()

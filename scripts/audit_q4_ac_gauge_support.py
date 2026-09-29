#!/usr/bin/env python3
"""Experiment 289: explain the exact Q4 A/C polarity gauges by support.

Corrected Experiment 287 shows that the exact canonical-transducer physical
gauge contains Q4 polarity bits A and C, but not the coupled F+I branch.

This experiment asks why A/C are exact gauges.

For polarity masks 0, A, C, and A+C:
  * re-enumerate raw-compatible selector depths;
  * run canonical two-pass closure;
  * compare the surviving selector-depth fields and first/terminal outputs.

It also verifies that the A and C Q4 stacks have no public observations and
identifies their physical residue support.

If selector depths are unchanged, these are pure physical symbol-polarity
gauges: they alter printed slash/dot marks but not the address consumed by the
transition.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_q4_polarity_gauge import A, C
from audit_q4_pos3_polarity import DOT, SLASH, local_options, q4_observations
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    terminal_surface,
)


SERIAL_ORDER = "ABCDEFGHI"
MASKS = (0, A, C, A | C)


def polarity(mask):
    return tuple(
        DOT if mask & (1 << j) else SLASH
        for j in range(9)
    )


def selectors_for(options, mask):
    word = polarity(mask)
    depth_choices = []
    for j, exceptional_symbol in enumerate(word):
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


def selector_signature(selector):
    return tuple(selector[j] for j in range(9))


def q4_stack_residues(letter):
    j = SERIAL_ORDER.index(letter)
    return tuple(82 + 9 * depth + j for depth in range(3))


def main() -> None:
    rows = load_rows()
    observed = {int(record["residue"]) for record in rows}
    q4obs = q4_observations(rows)
    options = local_options(q4obs)
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))

    a_j = SERIAL_ORDER.index("A")
    c_j = SERIAL_ORDER.index("C")
    assert q4obs[a_j] == {}
    assert q4obs[c_j] == {}

    a_residues = q4_stack_residues("A")
    c_residues = q4_stack_residues("C")
    assert a_residues == (82, 91, 100)
    assert c_residues == (84, 93, 102)
    assert set(a_residues + c_residues).isdisjoint(observed)

    records = {}
    for mask in MASKS:
        selectors = selectors_for(options, mask)
        final = []
        for payload in payloads:
            for selector in selectors:
                first = tuple(
                    decode_dash_pos3(first_pass_surface(payload, selector, q))
                    for q in range(3)
                )
                if None in first:
                    continue
                terminal = decode_dash_pos3(terminal_surface(payload, selector))
                if terminal is None:
                    continue
                final.append((payload, selector, first, terminal))

        assert len(final) == 14
        records[mask] = final

    canonical_selector_fields = {
        selector_signature(item[1])
        for item in records[0]
    }
    canonical_first = Counter(item[2] for item in records[0])
    canonical_terminals = Counter(item[3] for item in records[0])

    assert len(canonical_selector_fields) == 6
    assert canonical_terminals == Counter({"100": 14})

    for mask in MASKS:
        final = records[mask]
        selector_fields = {
            selector_signature(item[1])
            for item in final
        }
        assert selector_fields == canonical_selector_fields
        assert Counter(item[2] for item in final) == canonical_first
        assert Counter(item[3] for item in final) == canonical_terminals

    # A/C polarity does not alter any surviving selector depth, despite
    # complementing all three printed symbols on the toggled stack.
    for mask in (A, C, A | C):
        assert {
            selector_signature(item[1])
            for item in records[mask]
        } == canonical_selector_fields

    print("Experiment 289")
    print("A stack observed Q4 cells:", q4obs[a_j])
    print("C stack observed Q4 cells:", q4obs[c_j])
    print("A gauge residue support:", a_residues)
    print("C gauge residue support:", c_residues)
    print("surviving selector fields per mask:", len(canonical_selector_fields))
    print("RESULT: A/C polarity flips leave the complete surviving selector-depth set unchanged")
    print("RESULT: A/C alter only entirely unobserved Q4 stack symbols")
    print("RESULT: A/C are exact physical-polarity gauges because the transition consumes depth, not printed polarity")
    print("CAUTION: all-slash remains the preferred authoring representative by Experiments 270/281")


if __name__ == "__main__":
    main()

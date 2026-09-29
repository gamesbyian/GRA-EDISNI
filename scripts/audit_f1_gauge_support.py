#!/usr/bin/env python3
"""Experiment 285: explain the transition-invisible f_1 recursion gauge.

Experiments 279/284 leave two stable maximum-retention recursive operations.
They differ only by f_1:
    identity  vs  swap(q=0,q=1) when selector value S=1.

Both produce the same 14 physical masters and fixed terminal 100.

This experiment identifies the exact support of that gauge and asks why the
swap is behaviorally invisible.

For every legal hidden state:
  1. find physical cells whose Q4 selector can equal 1;
  2. compare the primary symbol read at (q=0,d=1,j) and (q=1,d=1,j).

If those symbols are equal at every S=1-reachable cell, f_1 is a genuine
observational gauge: it changes addresses only where stored symbols coincide.
"""

from __future__ import annotations

from generate_master import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    legal_states,
    primary_symbol,
    q4_selector_field,
)


def residue(q, d, j):
    return 1 + 27 * q + 9 * d + j


def selector_by_letter(state):
    field = q4_selector_field(state)
    result = {}
    for letter in SERIAL_ORDER:
        row, col = PHYSICAL_POSITION[letter]
        result[letter] = field[row][col]
    return result


def primary_at(state, q, d, letter):
    j = SERIAL_ORDER.index(letter)
    return primary_symbol(state, residue(q, d, j))


def main() -> None:
    states = legal_states()
    assert len(states) == 14

    support = {
        letter
        for state in states
        for letter, value in selector_by_letter(state).items()
        if value == 1
    }
    assert support == {"A", "D", "F"}

    equality_locus = {
        letter
        for letter in SERIAL_ORDER
        if all(
            primary_at(state, 0, 1, letter)
            == primary_at(state, 1, 1, letter)
            for state in states
        )
    }
    assert equality_locus == {"I", "A", "D", "F"}
    assert support <= equality_locus

    comparisons = {
        letter: {
            (
                primary_at(state, 0, 1, letter),
                primary_at(state, 1, 1, letter),
            )
            for state in states
        }
        for letter in support
    }
    assert comparisons == {
        "A": {("-", "-")},
        "D": {("/", "/")},
        "F": {("/", "/")},
    }

    # I is also q0/q1-equal at depth 1, but S(I)=2 in every legal state, so it
    # is outside the support of f_1.
    assert {
        selector_by_letter(state)["I"]
        for state in states
    } == {2}

    print("Experiment 285")
    print("S=1 reachable physical cells:", sorted(support))
    print("q0/q1 depth-1 equality locus:", sorted(equality_locus))
    print("support comparisons:", comparisons)
    print("RESULT: f_1 acts only at A/D/F")
    print("RESULT: q0,d1 and q1,d1 store identical symbols at every A/D/F support cell")
    print("RESULT: the surviving f_1 recursion ambiguity is an exact observational gauge")
    print("CAUTION: identity f_1 remains the simpler address rule, but behavior cannot distinguish it")


if __name__ == "__main__":
    main()

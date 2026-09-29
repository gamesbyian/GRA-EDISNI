#!/usr/bin/env python3
"""Experiment 260: factor the Q4 polarity closure family into gauge and branch bits.

Experiment 256 found 16 raw-compatible polarity words with recursive closure:
  * 8 retain 14 states and terminate at 100;
  * 8 retain 12 states and terminate at 110.

This experiment asks whether those words have a simple algebraic structure in
the nine binary stack-polarity bits (slash-exception=0, dot-exception=1).

No new closure filtering is introduced. We independently recompute the family
and then factor the surviving bitmasks.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

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


def mask_for(polarity):
    mask = 0
    for j, symbol in enumerate(polarity):
        if symbol == DOT:
            mask |= 1 << j
    return mask


def label(mask):
    return "".join(
        SERIAL_ORDER[j]
        for j in range(9)
        if mask & (1 << j)
    ) or "(none)"


def closure_count(payloads, options, polarity):
    depth_choices = []
    for j, exceptional_symbol in enumerate(polarity):
        depths = tuple(sorted({
            depth
            for depth, symbol, _pattern in options[j]
            if symbol == exceptional_symbol
        }))
        if not depths:
            return 0, Counter()
        depth_choices.append(depths)

    total = 0
    terminals = Counter()
    for values in product(*depth_choices):
        selector = dict(enumerate(values))
        for payload in payloads:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue
            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue
            total += 1
            terminals[terminal] += 1
    return total, terminals


def xor_span(generators):
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return values


def main() -> None:
    rows = load_rows()
    options = local_options(q4_observations(rows))
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    assert len(payloads) == 6

    maximal = set()
    sibling = set()

    for polarity in product((SLASH, DOT), repeat=9):
        count, terminals = closure_count(payloads, options, polarity)
        if count == 14:
            assert terminals == Counter({"100": 14})
            maximal.add(mask_for(polarity))
        elif count == 12:
            assert terminals == Counter({"110": 12})
            sibling.add(mask_for(polarity))
        else:
            assert count == 0

    assert len(maximal) == 8
    assert len(sibling) == 8

    A = 1 << SERIAL_ORDER.index("A")
    C = 1 << SERIAL_ORDER.index("C")
    D = 1 << SERIAL_ORDER.index("D")
    FI = (
        (1 << SERIAL_ORDER.index("F"))
        | (1 << SERIAL_ORDER.index("I"))
    )

    gauge = xor_span((A, C, FI))
    assert len(gauge) == 8
    assert maximal == gauge
    assert sibling == {mask ^ D for mask in gauge}

    # Gauge generators are independent over GF(2).
    assert len(xor_span((A, C))) == 4
    assert len(xor_span((A, FI))) == 4
    assert len(xor_span((C, FI))) == 4

    print("Experiment 260")
    print("14-state/100 polarity masks:")
    for mask in sorted(maximal):
        print(" ", f"{mask:09b}", label(mask))
    print("12-state/110 polarity masks:")
    for mask in sorted(sibling):
        print(" ", f"{mask:09b}", label(mask))
    print("gauge generators:", label(A), label(C), label(FI))
    print("functional branch flip:", label(D))
    print("RESULT: maximal Q4 polarity freedom is exactly a 3-bit XOR gauge cube")
    print("RESULT: generators are A, C, and coupled F+I polarity flips")
    print("RESULT: D toggles the whole gauge cube to the 12-state/110 sibling")


if __name__ == "__main__":
    main()

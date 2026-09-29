#!/usr/bin/env python3
"""Experiment 256: map the full Q4 polarity-assignment closure boundary.

Experiment 254 compared two extremes:
  * one globally shared exceptional-symbol polarity;
  * nine independently free stack polarities.

This experiment enumerates the intermediate object directly: all 2^9
slash-exception/dot-exception polarity assignments over the nine A-I stacks.
For every assignment compatible with the raw Q4 marks, enumerate all allowed
selector-depth maps, combine them with the six raw-compatible primary POS3
payloads, and run the canonical two-pass POS3 closure.

No target state count or terminal payload is used as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_q4_pos3_polarity import (
    DOT,
    SLASH,
    local_options,
    q4_observations,
)
from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    terminal_surface,
)

SERIAL_ORDER = "ABCDEFGHI"


def polarity_word(bits):
    return "".join("/" if symbol == SLASH else "." for symbol in bits)


def main() -> None:
    rows = load_rows()
    options = local_options(q4_observations(rows))
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    assert len(payloads) == 6

    records = []

    for polarity in product((SLASH, DOT), repeat=9):
        depth_choices = []
        raw_physical_count = 1
        compatible = True

        for j, exceptional_symbol in enumerate(polarity):
            depths = tuple(sorted({
                depth
                for depth, symbol, _pattern in options[j]
                if symbol == exceptional_symbol
            }))
            if not depths:
                compatible = False
                break
            depth_choices.append(depths)
            raw_physical_count *= len(depths)

        if not compatible:
            continue

        first_count = 0
        final_count = 0
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

                first_count += 1
                terminal = decode_dash_pos3(terminal_surface(payload, selector))
                if terminal is None:
                    continue

                final_count += 1
                terminals[terminal] += 1

        records.append(
            (
                polarity,
                raw_physical_count,
                first_count,
                final_count,
                terminals,
            )
        )

    # Exactly half of the 2^9 polarity words survive raw marks.
    assert len(records) == 256
    assert sum(record[1] for record in records) == 7776

    closure = [record for record in records if record[3]]
    assert len(closure) == 16

    final_count_distribution = Counter(record[3] for record in records)
    assert final_count_distribution == Counter({0: 240, 14: 8, 12: 8})

    canonical = [record for record in closure if record[3] == 14]
    alternate = [record for record in closure if record[3] == 12]

    assert all(record[4] == Counter({"100": 14}) for record in canonical)
    assert all(record[4] == Counter({"110": 12}) for record in alternate)

    # Across the eight maximal 14-state polarity words, B,D,E,G,H are forced
    # slash-exception. A,C,F,I may independently vary in the surviving set,
    # though raw compatibility correlates F/I choices into the eight exact
    # words actually present.
    forced = {}
    for j, letter in enumerate(SERIAL_ORDER):
        values = {record[0][j] for record in canonical}
        if len(values) == 1:
            forced[letter] = next(iter(values))

    assert forced == {
        "B": SLASH,
        "D": SLASH,
        "E": SLASH,
        "G": SLASH,
        "H": SLASH,
    }

    # The 12-state sibling differs at the decisive D stack: its closure words
    # force D to dot-exception while B/E/G/H remain slash-exception.
    alternate_forced = {}
    for j, letter in enumerate(SERIAL_ORDER):
        values = {record[0][j] for record in alternate}
        if len(values) == 1:
            alternate_forced[letter] = next(iter(values))

    assert alternate_forced == {
        "B": SLASH,
        "D": DOT,
        "E": SLASH,
        "G": SLASH,
        "H": SLASH,
    }

    print("Experiment 256")
    print("raw-compatible Q4 polarity words:", len(records))
    print("closure-compatible polarity words:", len(closure))
    print("final-state-count distribution:", dict(sorted(final_count_distribution.items())))
    print("14-state / terminal-100 polarity words:")
    for record in canonical:
        print(" ", polarity_word(record[0]))
    print("12-state / terminal-110 sibling words:")
    for record in alternate:
        print(" ", polarity_word(record[0]))
    print("forced polarities in maximal 14-state family:", {
        key: ("slash" if value == SLASH else "dot")
        for key, value in forced.items()
    })
    print("RESULT: global shared Q4 polarity is stronger than necessary")
    print("RESULT: B,D,E,G,H slash polarity is the closure-critical spine")
    print("RESULT: D polarity separates the 14-state/100 family from a 12-state/110 sibling")


if __name__ == "__main__":
    main()

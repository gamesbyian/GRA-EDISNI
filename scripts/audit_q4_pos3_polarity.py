#!/usr/bin/env python3
"""Experiment 254: weaken Q4 one-slash grammar to shared-polarity POS3.

Broader local grammar:
    each Q4 depth stack is any nonuniform slash/dot triple;
    the selector value is the depth of the exceptional symbol.

Two levels are audited:

1. Per-stack polarity free: each stack may independently use slash-exception
   or dot-exception.
2. One shared exceptional-symbol polarity across all nine stacks.

The raw Q4 observations alone decide whether a shared polarity can be slash or
dot. The recursive machine is also run on the fully local-polarity-free family
to measure what breaks when the shared-orientation assumption is removed.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    terminal_surface,
)

SLASH = "/"
DOT = "."


def q4_observations(rows):
    by_j = {j: {} for j in range(9)}
    for record in rows:
        residue = int(record["residue"])
        if residue < 82:
            continue
        offset = residue - 82
        depth = offset // 9
        j = offset % 9
        by_j[j][depth] = record["symbol"]
    return by_j


def pattern(exception_depth, exception_symbol):
    background = DOT if exception_symbol == SLASH else SLASH
    return tuple(
        exception_symbol if depth == exception_depth else background
        for depth in range(3)
    )


def local_options(observed):
    result = {}
    for j in range(9):
        options = []
        for exception_symbol in (SLASH, DOT):
            for exception_depth in range(3):
                candidate = pattern(exception_depth, exception_symbol)
                if all(
                    candidate[depth] == symbol
                    for depth, symbol in observed[j].items()
                ):
                    options.append((exception_depth, exception_symbol, candidate))
        result[j] = tuple(options)
    return result


def selector_depth_map(choices):
    return {j: choice[0] for j, choice in enumerate(choices)}


def main() -> None:
    rows = load_rows()
    observed = q4_observations(rows)
    options = local_options(observed)

    local_physical_count = 1
    for j in range(9):
        local_physical_count *= len(options[j])
    assert local_physical_count == 7776

    # Distinct selector-address maps ignore which symbol was exceptional.
    depth_choices = {
        j: tuple(sorted({depth for depth, _symbol, _pattern in options[j]}))
        for j in range(9)
    }
    logical_selector_count = 1
    for j in range(9):
        logical_selector_count *= len(depth_choices[j])
    assert logical_selector_count == 1944

    shared_counts = {}
    for exceptional_symbol in (SLASH, DOT):
        count = 1
        for j in range(9):
            matching = [
                option
                for option in options[j]
                if option[1] == exceptional_symbol
            ]
            count *= len(matching)
        shared_counts[exceptional_symbol] = count

    # Raw observations force the shared exceptional symbol to slash.
    assert shared_counts == {SLASH: 36, DOT: 0}

    # Measure the consequence of dropping shared polarity entirely. Recursion
    # depends only on exceptional depth, so use the 1,944 distinct logical
    # selector maps rather than counting symbol-polarity duplicates.
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = [
        dict(zip(range(9), values))
        for values in product(*(depth_choices[j] for j in range(9)))
    ]

    assert len(payloads) == 6
    assert len(selectors) == 1944

    first_survivors = []
    final_survivors = []

    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue

            first_survivors.append((payload, selector, first))
            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is not None:
                final_survivors.append((payload, selector, first, terminal))

    assert len(first_survivors) == 72
    assert len(final_survivors) == 52
    terminal_counts = Counter(item[3] for item in final_survivors)
    assert terminal_counts == Counter({"100": 28, "110": 24})

    print("Experiment 254")
    print("local-polarity-free Q4 physical completions:", local_physical_count)
    print("local-polarity-free distinct selector maps:", logical_selector_count)
    print("shared slash-exception completions:", shared_counts[SLASH])
    print("shared dot-exception completions:", shared_counts[DOT])
    print("local-free recursion: first-pass survivors:", len(first_survivors))
    print("local-free recursion: second-pass survivors:", len(final_survivors))
    print("local-free terminal counts:", dict(sorted(terminal_counts.items())))
    print("OK: a shared Q4 polarity is structurally necessary for the tight family")
    print("OK: raw observations force shared exceptional symbol to slash")
    print("RESULT: replace 'one slash per stack' premise with weaker shared-polarity POS3")


if __name__ == "__main__":
    main()

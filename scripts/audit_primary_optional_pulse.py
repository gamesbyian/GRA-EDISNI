#!/usr/bin/env python3
"""Experiment 255: weaken primary POS3 to an optional-pulse column grammar.

Broader primary grammar:
    within each slash/dash column, under the established frame polarity,
    there may be ZERO or ONE minority-symbol cell.

Exact POS3 is the occupied subfamily (exactly one minority cell per column).
A zero-minority column is a uniform-majority "missing pulse".

Raw observations determine the allowed zero/one-minority states independently
for all 27 primary columns. These are combined with the 36 raw Q4 selectors
and passed through the canonical two recursive operations.

Filters:
  * all three first-pass surfaces must be valid dash-POS3;
  * second-pass terminal must be valid dash-POS3.

No target state count or terminal payload is supplied.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


def build_primary_observations(rows):
    by_column = defaultdict(list)
    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        offset = residue - 1
        q = offset // 27
        d = (offset % 27) // 9
        j = offset % 9
        row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        by_column[(q, d, col)].append((row, record["symbol"]))
    return by_column


def predicted_symbol(row, minority_row, minority_is_dash):
    # minority_row=None means a uniform-majority column.
    if minority_row is None:
        return "/" if minority_is_dash else "-"
    if row == minority_row:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def optional_primary_candidates(rows):
    observed = build_primary_observations(rows)
    candidates = {}

    for q in range(3):
        for d in range(3):
            minority_is_dash = d <= q
            for col in range(3):
                allowed = []
                for minority_row in (None, 0, 1, 2):
                    if all(
                        predicted_symbol(
                            row,
                            minority_row,
                            minority_is_dash,
                        )
                        == symbol
                        for row, symbol in observed[(q, d, col)]
                    ):
                        allowed.append(minority_row)
                if not allowed:
                    raise AssertionError(
                        f"no optional-pulse completion for {(q, d, col)}"
                    )
                candidates[(q, d, col)] = tuple(allowed)

    return candidates


def enumerate_primary(candidates):
    keys = tuple(sorted(candidates))
    for values in product(*(candidates[key] for key in keys)):
        yield dict(zip(keys, values))


def primary_symbol(payload, residue):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    return predicted_symbol(
        row,
        payload[(q, d, col)],
        d <= q,
    )


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    return primary_symbol(payload, 1 + 27 * q + 9 * d + j)


def first_surface(payload, selector, q):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                q,
                selector_at(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def terminal_surface(payload, selector):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                selector_at(selector, row, col),
                selector_at(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def main() -> None:
    rows = load_rows()
    primary_candidates = optional_primary_candidates(rows)
    payloads = list(enumerate_primary(primary_candidates))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    assert len(payloads) == 1536
    assert len(selectors) == 36
    assert len(payloads) * len(selectors) == 55296

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

            missing_pulses = sum(value is None for value in payload.values())
            survivors.append(
                (payload, selector, first, terminal, missing_pulses)
            )

    assert len(survivors) == 832
    assert {item[3] for item in survivors} == {"100"}

    missing_distribution = Counter(item[4] for item in survivors)
    assert missing_distribution == Counter({
        0: 14,
        1: 80,
        2: 192,
        3: 250,
        4: 190,
        5: 84,
        6: 20,
        7: 2,
    })

    exact_pos3 = [item for item in survivors if item[4] == 0]
    assert len(exact_pos3) == 14

    selector_signatures = {
        tuple(selector[j] for j in range(9))
        for _payload, selector, _first, _terminal, _missing in survivors
    }
    assert len(selector_signatures) == 6

    first_families = {item[2] for item in survivors}
    assert len(first_families) == 3

    print("Experiment 255")
    print("raw optional-pulse primary completions:", len(payloads))
    print("raw Q4 selectors:", len(selectors))
    print("raw candidate machines:", len(payloads) * len(selectors))
    print("recursive POS3-closure survivors:", len(survivors))
    print("terminal payloads:", sorted({item[3] for item in survivors}))
    print("missing-pulse distribution:", dict(sorted(missing_distribution.items())))
    print("exact-POS3 survivors:", len(exact_pos3))
    print("surviving selector fields:", len(selector_signatures))
    print("surviving first-pass functional families:", len(first_families))
    print("RESULT: exact primary POS3 is needed for the 14-state family")
    print("RESULT: terminal 100 is invariant over the much broader 832-state closure family")


if __name__ == "__main__":
    main()

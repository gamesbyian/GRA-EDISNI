#!/usr/bin/env python3
"""Experiment 272: weaken primary columns to frame-weight-three only.

Experiment 255 allowed zero-or-one minority pulse per physical column.
Experiment 257 then recovered exact POS3 by quarter-local frame-weight balance.

This experiment drops the column grammar entirely. For each of the nine
primary 3x3 frames, require only:
  * consistency with the classified raw marks under the established polarity;
  * exactly three minority-symbol cells somewhere in the 3x3 frame.

The three pulses may share columns. This parent therefore preserves the visible
frame-level 3-of-9 count while removing directional POS3 occupancy.

Combine every raw-compatible frame-weight-three primary completion with the 36
raw Q4 selectors and apply the canonical two recursive POS3-closure tests.
No target state count or terminal payload is supplied.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


def frame_observations(rows):
    observed = defaultdict(dict)
    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        offset = residue - 1
        q = offset // 27
        d = (offset % 27) // 9
        j = offset % 9
        row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        minority_symbol = "-" if d <= q else "/"
        observed[(q, d)][(row, col)] = record["symbol"] == minority_symbol
    return observed


def frame_candidates(rows):
    observed = frame_observations(rows)
    result = {}
    cells = tuple((row, col) for row in range(3) for col in range(3))
    for q in range(3):
        for d in range(3):
            candidates = []
            for chosen in combinations(cells, 3):
                minority = frozenset(chosen)
                if all(
                    ((cell in minority) == value)
                    for cell, value in observed[(q, d)].items()
                ):
                    candidates.append(minority)
            assert candidates
            result[(q, d)] = tuple(candidates)
    return result


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
    minority = (row, col) in payload[(q, d)]
    if minority:
        return "-" if d <= q else "/"
    return "/" if d <= q else "-"


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


def exact_column_pos3(payload):
    return all(
        sum((row, col) in payload[(q, d)] for row in range(3)) == 1
        for q in range(3)
        for d in range(3)
        for col in range(3)
    )


def nonpos3_column_count(payload):
    return sum(
        sum((row, col) in payload[(q, d)] for row in range(3)) != 1
        for q in range(3)
        for d in range(3)
        for col in range(3)
    )


def main() -> None:
    rows = load_rows()
    candidates = frame_candidates(rows)
    payloads = list(enumerate_primary(candidates))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    frame_counts = {key: len(value) for key, value in candidates.items()}
    assert frame_counts == {
        (0, 0): 3,
        (0, 1): 1,
        (0, 2): 3,
        (1, 0): 6,
        (1, 1): 2,
        (1, 2): 1,
        (2, 0): 6,
        (2, 1): 1,
        (2, 2): 2,
    }
    assert len(payloads) == 1296
    assert len(selectors) == 36

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
            survivors.append(
                (
                    payload,
                    selector,
                    first,
                    terminal,
                    exact_column_pos3(payload),
                    nonpos3_column_count(payload),
                )
            )

    assert len(survivors) == 1548
    assert {item[3] for item in survivors} == {"100"}

    exact = [item for item in survivors if item[4]]
    assert len(exact) == 14

    defect_distribution = Counter(item[5] for item in survivors)
    assert defect_distribution == Counter({
        0: 14,
        2: 124,
        3: 14,
        4: 380,
        5: 52,
        6: 506,
        7: 58,
        8: 308,
        9: 20,
        10: 72,
    })

    print("Experiment 272")
    print("raw frame-weight-three primary completions:", len(payloads))
    print("raw Q4 selectors:", len(selectors))
    print("raw candidate machines:", len(payloads) * len(selectors))
    print("recursive POS3-closure survivors:", len(survivors))
    print("terminal payloads:", sorted({item[3] for item in survivors}))
    print("exact column-POS3 survivors:", len(exact))
    print("non-POS3-column distribution:", dict(sorted(defect_distribution.items())))
    print("RESULT: frame-level weight three is insufficient to recover the 14-state family")
    print("RESULT: exact column POS3 remains the unique zero-defect 14-state subfamily")
    print("RESULT: terminal 100 survives across all 1548 broader recursively closed states")
    print("CAUTION: fixed frame weight is a bounded grammar, not a direct raw observation")


if __name__ == "__main__":
    main()

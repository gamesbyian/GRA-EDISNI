#!/usr/bin/env python3
"""Experiment 250: reconstruct the legal machine family from raw constraints.

This implementation deliberately does not import either existing generator.

Parent space:
  * primary: all POS3 payload completions consistent with classified residues
    under the established d<=q polarity staircase;
  * Q4: all one-slash-per-depth-stack selector completions consistent with the
    classified slash/dot residues.

The resulting raw-compatible Cartesian product is filtered only by recursive
structural closure:

  1. first selector application must yield valid dash-POS3 surfaces for all
     three external q values;
  2. second selector reuse must yield a valid dash-POS3 terminal surface.

No expected first-pass payload, hidden-state relation, Q4 formula, state count,
or terminal payload is used as a filter.
"""

from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / os.environ.get("GRA_EDISNI_OBSERVATIONS_FILE", "data/observations.csv")

SERIAL_ORDER = "ABCDEFGHI"
PHYSICAL_LAYOUT = (
    ("I", "A", "B"),
    ("C", "D", "E"),
    ("F", "G", "H"),
)
PHYSICAL_POSITION = {
    letter: (row, col)
    for row, line in enumerate(PHYSICAL_LAYOUT)
    for col, letter in enumerate(line)
}


def load_rows():
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def predicted_primary_symbol(row, minority_row, minority_is_dash):
    on_minority = row == minority_row
    if on_minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def primary_column_candidates(rows):
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

    candidates = {}
    for q in range(3):
        for d in range(3):
            minority_is_dash = d <= q
            for col in range(3):
                allowed = tuple(
                    minority_row
                    for minority_row in range(3)
                    if all(
                        predicted_primary_symbol(
                            row,
                            minority_row,
                            minority_is_dash,
                        )
                        == symbol
                        for row, symbol in by_column[(q, d, col)]
                    )
                )
                if not allowed:
                    raise AssertionError(
                        f"no primary POS3 completion for {(q, d, col)}"
                    )
                candidates[(q, d, col)] = allowed

    return candidates


def enumerate_primary_payloads(candidates):
    keys = tuple(sorted(candidates))
    for values in product(*(candidates[key] for key in keys)):
        yield dict(zip(keys, values))


def q4_selector_candidates(rows):
    # Selector value at serial/letter position j is the unique slash depth.
    candidates = {j: set(range(3)) for j in range(9)}

    for record in rows:
        residue = int(record["residue"])
        if residue < 82:
            continue

        offset = residue - 82
        depth = offset // 9
        j = offset % 9
        symbol = record["symbol"]

        if symbol == "/":
            candidates[j].intersection_update({depth})
        elif symbol == ".":
            candidates[j].discard(depth)
        else:
            raise AssertionError(f"unexpected Q4 symbol: {symbol}")

    result = {j: tuple(sorted(values)) for j, values in candidates.items()}
    if any(not values for values in result.values()):
        raise AssertionError("raw Q4 observations admit no selector completion")
    return result


def enumerate_selectors(candidates):
    keys = tuple(range(9))
    for values in product(*(candidates[j] for j in keys)):
        yield dict(zip(keys, values))


def primary_symbol(payload, residue):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    minority_row = payload[(q, d, col)]
    return predicted_primary_symbol(row, minority_row, d <= q)


def q4_symbol(selector, residue):
    offset = residue - 82
    depth = offset // 9
    j = offset % 9
    return "/" if selector[j] == depth else "."


def foreground_symbol(payload, selector, residue):
    if 1 <= residue <= 81:
        return primary_symbol(payload, residue)
    if 82 <= residue <= 108:
        return q4_symbol(selector, residue)
    raise ValueError("residue must be in 1..108")


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return primary_symbol(payload, residue)


def selector_at_physical_cell(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def first_pass_surface(payload, selector, q):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                q,
                selector_at_physical_cell(selector, row, col),
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
                selector_at_physical_cell(selector, row, col),
                selector_at_physical_cell(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def decode_dash_pos3(surface):
    digits = []
    for col in range(3):
        rows = [row for row in range(3) if surface[row][col] == "-"]
        if len(rows) != 1:
            return None
        digits.append(str(rows[0]))
    return "".join(digits)


def generate_master(payload, selector):
    return "".join(
        foreground_symbol(payload, selector, residue)
        for residue in range(1, 109)
    )


def compact_primary_signature(payload):
    # Report only positions that were raw-variable in Experiment 246.
    return (
        payload[(0, 2, 1)],
        payload[(2, 0, 1)],
    )


def compact_selector_signature(selector):
    # Human-readable A,C,D,G values are the raw-variable selector positions.
    return tuple(
        selector[SERIAL_ORDER.index(letter)]
        for letter in ("A", "C", "D", "G")
    )


def main():
    rows = load_rows()

    primary_candidates = primary_column_candidates(rows)
    primary_payloads = list(enumerate_primary_payloads(primary_candidates))
    selector_candidates = q4_selector_candidates(rows)
    selectors = list(enumerate_selectors(selector_candidates))

    assert len(primary_payloads) == 6
    assert len(selectors) == 18

    raw_pairs = [
        (payload, selector)
        for payload in primary_payloads
        for selector in selectors
    ]
    assert len(raw_pairs) == 108

    first_pass_survivors = []
    for payload, selector in raw_pairs:
        decoded = tuple(
            decode_dash_pos3(first_pass_surface(payload, selector, q))
            for q in range(3)
        )
        if None not in decoded:
            first_pass_survivors.append((payload, selector, decoded))

    assert len(first_pass_survivors) == 12

    final_survivors = []
    for payload, selector, first_decoded in first_pass_survivors:
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is not None:
            final_survivors.append(
                (payload, selector, first_decoded, terminal)
            )

    assert len(final_survivors) == 10
    assert {terminal for *_prefix, terminal in final_survivors} == {"100"}

    masters = [
        generate_master(payload, selector)
        for payload, selector, _first, _terminal in final_survivors
    ]
    assert len(set(masters)) == 10

    # The fully reconstructed raw-constraint family independently recovers the
    # familiar invariant/variable split and global symbol census.
    variable = [
        residue
        for residue in range(1, 109)
        if len({master[residue - 1] for master in masters}) > 1
    ]
    assert variable == [22, 25, 55, 58, 61, 84, 88, 91, 100, 102, 106]
    assert all(
        Counter(master) == Counter({"/": 54, "-": 36, ".": 18})
        for master in masters
    )

    # Every classified physical observation remains satisfied.
    for record in rows:
        residue = int(record["residue"])
        symbol = record["symbol"]
        assert all(master[residue - 1] == symbol for master in masters)

    print("Experiment 250")
    print("raw-compatible primary payloads:", len(primary_payloads))
    print("raw-compatible Q4 selectors:", len(selectors))
    print("raw candidate machines:", len(raw_pairs))
    print("after first-pass POS3 closure:", len(first_pass_survivors))
    print("after second-pass POS3 closure:", len(final_survivors))
    print("terminal payloads:", sorted({x[3] for x in final_survivors}))
    print("survivor signatures: x y | A C D G | first-pass | terminal")
    for payload, selector, first_decoded, terminal in final_survivors:
        x, y = compact_primary_signature(payload)
        A, C, D, G = compact_selector_signature(selector)
        print(
            f"  {x} {y} | {A} {C} {D} {G} | "
            f"{'/'.join(first_decoded)} | {terminal}"
        )

    print("OK: raw constraints + recursive POS3 closure recover exactly 10 states")
    print("OK: terminal 100 emerges without being used as a filter")
    print("OK: reconstructed masters reproduce corpus, 97/11 split, and 54/36/18 census")


if __name__ == "__main__":
    main()

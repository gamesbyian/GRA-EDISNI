#!/usr/bin/env python3
"""Score withheld known sticker residues against raw-machine reconstruction.

This is a representation-conditional prediction test.  It keeps the current
H108 registration, primary POS3 grammar, derived primary polarity staircase,
Q4 one-slash selector representation, and canonical two-pass recursion fixed,
then withholds observations and reconstructs the surviving raw machine family.

Crucially, every physical record at a withheld H108 residue is removed together,
so repeated sticker serials cannot leak the answer.

Default mode is leave-one-residue-out over all 65 observed H108 residues.
Optional grouped modes are provided for stronger, potentially less constrained
tests.

This script does NOT claim premise-level blindness: premises historically
derived using the full corpus remain fixed.  See docs/sticker-prediction-validation.md.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"
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
                            row, minority_row, minority_is_dash
                        ) == symbol
                        for row, symbol in by_column[(q, d, col)]
                    )
                )
                if not allowed:
                    return None
                candidates[(q, d,col)] = allowed
    return candidates


def enumerate_primary_payloads(candidates):
    keys = tuple(sorted(candidates))
    for values in product(*(candidates[key] for key in keys)):
        yield dict(zip(keys, values))


def q4_selector_candidates(rows):
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
            return None
    result = {j: tuple(sorted(v)) for j, v in candidates.items()}
    if any(not v for v in result.values()):
        return None
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
    return (
        primary_symbol(payload, residue)
        if residue <= 81
        else q4_symbol(selector, residue)
    )


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return primary_symbol(payload, residue)


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def first_surface(payload, selector, q):
    return tuple(
        tuple(
            frame_symbol(
                payload, q, selector_at(selector, row, col), row, col
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


def decode_dash_pos3(surface):
    digits = []
    for col in range(3):
        rows = [row for row in range(3) if surface[row][col] == "-"]
        if len(rows) != 1:
            return None
        digits.append(str(rows[0]))
    return "".join(digits)


def reconstruct(rows):
    pc = primary_column_candidates(rows)
    qc = q4_selector_candidates(rows)
    if pc is None or qc is None:
        return []

    payloads = list(enumerate_primary_payloads(pc))
    selectors = list(enumerate_selectors(qc))
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
            survivors.append((payload, selector, first, terminal))
    return survivors


def groups(rows, mode):
    residues = sorted({int(r["residue"]) for r in rows})
    if mode == "residue":
        return [(f"r{r}", {r}) for r in residues]

    if mode == "primary-frame":
        out = []
        for q in range(3):
            for d in range(3):
                cells = {
                    r for r in residues
                    if r <= 81
                    and (r - 1) // 27 == q
                    and ((r - 1) % 27) // 9 == d
                }
                if cells:
                    out.append((f"q{q}d{d}", cells))
        return out

    if mode == "q4-stack":
        out = []
        for j, letter in enumerate(SERIAL_ORDER):
            cells = {
                r for r in residues
                if r >= 82 and (r - 82) % 9 == j
            }
            if cells:
                out.append((f"q4-{letter}", cells))
        return out

    raise ValueError(mode)


def actual_by_residue(rows):
    values = defaultdict(set)
    for row in rows:
        values[int(row["residue"])].add(row["symbol"])
    assert all(len(v) == 1 for v in values.values())
    return {r: next(iter(v)) for r, v in values.items()}


def classify(predicted, actual):
    if not predicted:
        return "no-survivor"
    if len(predicted) == 1:
        only = next(iter(predicted))
        return "forced-correct" if only == actual else "forced-wrong"
    return (
        "ambiguous-includes-actual"
        if actual in predicted
        else "ambiguous-excludes-actual"
    )


def run(mode):
    rows = load_rows()
    actual = actual_by_residue(rows)
    output = []

    for group_name, withheld in groups(rows, mode):
        reduced = [
            row for row in rows
            if int(row["residue"]) not in withheld
        ]
        survivors = reconstruct(reduced)

        for residue in sorted(withheld):
            if residue not in actual:
                continue
            counts = Counter(
                foreground_symbol(payload, selector, residue)
                for payload, selector, _first, _terminal in survivors
            )
            predicted = set(counts)
            output.append({
                "group": group_name,
                "residue": residue,
                "background": SERIAL_ORDER[(residue - 1) % 9],
                "actual": actual[residue],
                "survivors": len(survivors),
                "predicted_symbols": "".join(sorted(predicted)),
                "actual_support": counts[actual[residue]],
                "status": classify(predicted, actual[residue]),
            })
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("residue", "primary-frame", "q4-stack"),
        default="residue",
    )
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    rows = run(args.mode)
    fields = (
        "group", "residue", "background", "actual", "survivors",
        "predicted_symbols", "actual_support", "status",
    )

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    counts = Counter(row["status"] for row in rows)
    print(f"mode={args.mode} scored_residues={len(rows)}")
    for status in (
        "forced-correct",
        "forced-wrong",
        "ambiguous-includes-actual",
        "ambiguous-excludes-actual",
        "no-survivor",
    ):
        print(f"{status}: {counts[status]}")

    print(",".join(fields))
    for row in rows:
        print(",".join(str(row[field]) for field in fields))

    if counts["forced-wrong"] or counts["ambiguous-excludes-actual"]:
        raise SystemExit("FAIL: at least one holdout excludes the true symbol")


if __name__ == "__main__":
    main()

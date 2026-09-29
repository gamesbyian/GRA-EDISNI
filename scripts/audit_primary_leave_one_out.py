#!/usr/bin/env python3
"""Experiment 249: leave-one-residue-out robustness of raw primary reconstruction.

The unit of deletion is a distinct H108 residue, not an individual physical
sticker, because repeated serials can represent the same structural evidence.

For each of the 54 observed primary residues, remove every physical sticker at
that residue and recompute Experiment 246's two headline observability metrics:
  * number of frame polarities uniquely forced with polarity initially free;
  * number of primary payload trits uniquely forced under d<=q polarity.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"

SERIAL_ORDER = "ABCDEFGHI"
PHYSICAL_POSITION = {
    "I": (0, 0),
    "A": (0, 1),
    "B": (0, 2),
    "C": (1, 0),
    "D": (1, 1),
    "E": (1, 2),
    "F": (2, 0),
    "G": (2, 1),
    "H": (2, 2),
}


def load_rows():
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build_columns(rows):
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
    on_minority = row == minority_row
    if on_minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def allowed_rows(columns, q, d, col, minority_is_dash):
    return tuple(
        minority_row
        for minority_row in range(3)
        if all(
            predicted_symbol(row, minority_row, minority_is_dash) == symbol
            for row, symbol in columns[(q, d, col)]
        )
    )


def metrics(rows):
    columns = build_columns(rows)

    forced_polarities = 0
    for q in range(3):
        for d in range(3):
            viable = 0
            for minority_is_dash in (False, True):
                if all(
                    allowed_rows(columns, q, d, col, minority_is_dash)
                    for col in range(3)
                ):
                    viable += 1
            if viable == 1:
                forced_polarities += 1

    forced_trits = 0
    for q in range(3):
        for d in range(3):
            for col in range(3):
                if len(allowed_rows(columns, q, d, col, d <= q)) == 1:
                    forced_trits += 1

    return forced_polarities, forced_trits


def main() -> None:
    rows = load_rows()
    primary_residues = sorted({
        int(record["residue"])
        for record in rows
        if int(record["residue"]) <= 81
    })

    assert len(primary_residues) == 54
    assert metrics(rows) == (8, 25)

    effects = []
    for residue in primary_residues:
        reduced = [
            record
            for record in rows
            if int(record["residue"]) != residue
        ]
        result = metrics(reduced)
        if result != (8, 25):
            effects.append((residue, *result))

    assert len(effects) == 30
    classes = Counter((polarities, trits) for _r, polarities, trits in effects)
    assert classes == Counter({
        (8, 24): 24,
        (7, 25): 4,
        (7, 24): 2,
    })

    polarity_only = [
        residue
        for residue, polarities, trits in effects
        if polarities == 7 and trits == 25
    ]
    both = [
        residue
        for residue, polarities, trits in effects
        if polarities == 7 and trits == 24
    ]

    assert polarity_only == [12, 18, 66, 69]
    assert both == [2, 5]

    print("Experiment 249")
    print("observed primary residues:", len(primary_residues))
    print("single-residue deletions changing headline reconstruction:", len(effects))
    print("effect classes:", dict(sorted(classes.items())))
    print("polarity-only load-bearing residues:", polarity_only)
    print("polarity+trit load-bearing residues:", both)
    print("trit-only load-bearing residue count:", classes[(8, 24)])
    print("OK: no single residue deletion destroys the POS3 reconstruction")
    print("OK: worst deletion changes metrics only from 8/25 to 7/24")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 424: literal IBM 029 / Hollerith transform of the H108 sticker alphabet."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-424-hollerith-punch-card.json"

ROW_ORDER = ("12", "11", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

# IBM 029 special-character card code:
#   -  -> 11
#   /  -> 0-1
#   .  -> 12-8-3
PUNCHES = {
    "-": frozenset(("11",)),
    "/": frozenset(("0", "1")),
    ".": frozenset(("12", "8", "3")),
}


def load_unique_residues() -> dict[int, str]:
    seen: dict[int, str] = {}
    with OBS.open(newline="", encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            residue = int(rec["residue"])
            symbol = rec["symbol"]
            if symbol not in PUNCHES:
                raise AssertionError(f"unsupported sticker symbol {symbol!r}")
            old = seen.get(residue)
            if old is not None and old != symbol:
                raise AssertionError(
                    f"foreground conflict at H108 residue {residue}: {old!r} vs {symbol!r}"
                )
            seen[residue] = symbol
    return seen


def main() -> None:
    observed = load_unique_residues()
    counts = Counter(observed.values())

    row_vectors: dict[str, list[str]] = {row: [] for row in ROW_ORDER}
    for residue in range(1, 109):
        symbol = observed.get(residue)
        for row in ROW_ORDER:
            if symbol is None:
                # Rows unused by every member of the three-symbol alphabet are
                # still known zeros even when the sticker residue is unknown.
                used_by_any = any(row in punches for punches in PUNCHES.values())
                row_vectors[row].append("?" if used_by_any else "0")
            else:
                row_vectors[row].append("1" if row in PUNCHES[symbol] else "0")

    always_zero_rows = [
        row for row in ROW_ORDER if all(row not in punches for punches in PUNCHES.values())
    ]

    # Equality here is an alphabet-level invariant, not a coincidence of the
    # currently observed sample.
    signatures = {
        row: tuple(int(row in PUNCHES[s]) for s in ("-", "/", "."))
        for row in ROW_ORDER
    }
    groups: dict[tuple[int, int, int], list[str]] = {}
    for row, signature in signatures.items():
        groups.setdefault(signature, []).append(row)
    duplicate_active_groups = [
        rows
        for signature, rows in groups.items()
        if signature != (0, 0, 0) and len(rows) > 1
    ]

    holes_by_observed_symbol = {
        symbol: counts[symbol] * len(PUNCHES[symbol]) for symbol in ("-", "/", ".")
    }
    observed_hole_count = sum(holes_by_observed_symbol.values())

    result = {
        "experiment": 424,
        "title": "Literal IBM 029 Hollerith transform of sticker foreground symbols",
        "input": "data/observations.csv",
        "historical_mapping": {
            "-": ["11"],
            "/": ["0", "1"],
            ".": ["12", "8", "3"],
            "row_order": list(ROW_ORDER),
            "source_note": "IBM 029 card-code mapping; period is 12-8-3, slash is 0-1, hyphen is 11",
        },
        "observed_unique_residues": len(observed),
        "unknown_residues": 108 - len(observed),
        "observed_symbol_counts": {
            "-": counts["-"],
            "/": counts["/"],
            ".": counts["."],
        },
        "observed_hole_count": observed_hole_count,
        "observed_holes_by_symbol": holes_by_observed_symbol,
        "alphabet_level_invariants": {
            "always_zero_rows": always_zero_rows,
            "active_rows": [row for row in ROW_ORDER if row not in always_zero_rows],
            "duplicate_active_row_groups": duplicate_active_groups,
            "distinct_nonzero_row_signatures": sorted(
                {
                    signature
                    for signature in signatures.values()
                    if signature != (0, 0, 0)
                }
            ),
            "maximum_independent_occupancy_patterns": 3,
            "symbolwise_transform_is_injective": len(set(PUNCHES.values())) == len(PUNCHES),
            "information_gain_bits": 0,
        },
        "partial_row_vectors": {
            row: "".join(bits) for row, bits in row_vectors.items()
        },
        "interpretation": (
            "The literal IBM 029 transform is a lossless but redundant recoding of the "
            "same ternary sticker foreground. Six of twelve punch rows are structurally "
            "blank for every possible completion; rows 0 and 1 are exact duplicates; "
            "rows 12, 8 and 3 are exact duplicates; row 11 is the remaining independent "
            "pattern. Therefore the transform cannot by itself create a rich 12-row "
            "bitmap, add entropy, choose a 9x12/12x9 orientation, or supply a row order. "
            "Keep it as a historically motivated representation candidate, but require "
            "an independent punch-card-specific consumer or layout cue before extending it."
        ),
    }

    # Current physical corpus invariant after confirmed 427=dot and /043 repeat.
    assert len(observed) == 66, len(observed)
    assert counts == Counter({"/": 36, "-": 22, ".": 8}), counts
    assert always_zero_rows == ["2", "4", "5", "6", "7", "9"]
    assert duplicate_active_groups == [["12", "3", "8"], ["0", "1"]]
    assert observed_hole_count == 118

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

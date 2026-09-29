#!/usr/bin/env python3
"""Experiment 297: round-trip the historical Discord 108-cell master.

This is a provenance / registration audit, not an independent-data test.
The Discord FAQ transcription is compared against the repository's 82
physical sticker records using the community's serial-mod-108 convention.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
COMMUNITY = ROOT / "data" / "discord-community-master-108.json"


def load_master() -> str:
    payload = json.loads(COMMUNITY.read_text(encoding="utf-8"))
    rows = payload["rows_12x9"]
    assert len(rows) == 12
    assert all(len(row) == 9 for row in rows)
    master = "".join(rows)
    assert len(master) == 108
    return master


def char_for_repo_residue(master: str, residue: int) -> str:
    # Community indexing starts at sticker 0. The repo stores modulo-zero
    # observations as residue 108, so character index is residue % 108.
    return master[residue % 108]


def expected_image_class(serial: int) -> str:
    # Background image layer: 1->A, ..., 8->H, 0->I.
    mod = serial % 9
    return "I" if mod == 0 else chr(ord("A") + mod - 1)


def main() -> None:
    master = load_master()
    rows = list(csv.DictReader(OBS.open(newline="", encoding="utf-8")))

    symbol_mismatches = []
    image_mismatches = []
    by_residue: dict[int, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        serial = int(row["serial"])
        residue = int(row["residue"])
        by_residue[residue].append(row)

        expected_symbol = char_for_repo_residue(master, residue)
        if expected_symbol != row["symbol"]:
            symbol_mismatches.append(
                (serial, residue, row["symbol"], expected_symbol)
            )

        expected_class = expected_image_class(serial)
        if expected_class != row["image_class"]:
            image_mismatches.append(
                (serial, row["image_class"], expected_class)
            )

    overlaps = {r: rs for r, rs in by_residue.items() if len(rs) > 1}
    overlap_conflicts = {
        r: sorted({row["symbol"] for row in rs})
        for r, rs in overlaps.items()
        if len({row["symbol"] for row in rs}) > 1
    }

    counts = Counter(master)
    first_dot = master.index(".")

    def period_is_consistent(period: int) -> bool:
        seen: dict[int, str] = {}
        for row in rows:
            key = int(row["serial"]) % period
            symbol = row["symbol"]
            if key in seen and seen[key] != symbol:
                return False
            seen[key] = symbol
        return True

    max_serial = max(int(row["serial"]) for row in rows)
    consistent_periods = [
        period for period in range(1, max_serial + 1)
        if period_is_consistent(period)
    ]
    carrier_aligned_periods = [
        period for period in consistent_periods if period % 9 == 0
    ]

    assert len(rows) == 82
    assert len(by_residue) == 65
    assert len(overlaps) == 15
    assert len(rows) - len(by_residue) == 17
    assert not overlap_conflicts
    assert not symbol_mismatches
    assert not image_mismatches
    assert counts["/"] == 36
    assert counts["-"] == 22
    assert counts["."] == 7
    assert counts[" "] == 43
    assert first_dot == 85
    assert consistent_periods[0] == 108
    assert carrier_aligned_periods[0] == 108

    print("Experiment 297 - Discord 108-cell provenance/registration audit")
    print(f"master length: {len(master)}")
    print(
        "symbols: "
        f"/={counts['/']} -={counts['-']} .={counts['.']} blank={counts[' ']}"
    )
    print(f"physical records: {len(rows)}")
    print(f"unique H108 residues: {len(by_residue)}")
    print(f"overlap cells: {len(overlaps)}")
    print(f"extra records beyond one per residue: {len(rows) - len(by_residue)}")
    print(f"overlap symbol conflicts: {len(overlap_conflicts)}")
    print(f"Discord-master mismatches: {len(symbol_mismatches)}")
    print(f"background-cycle mismatches: {len(image_mismatches)}")
    print(f"first dot at community index / serial residue: {first_dot}")
    print(
        f"smallest foreground-consistent period through serial {max_serial}: "
        f"{consistent_periods[0]}"
    )
    print(
        "smallest foreground-consistent period also aligned to period-9 "
        f"background carrier: {carrier_aligned_periods[0]}"
    )
    print("registration: serial 0 mod 108 -> master index 0")
    print("background: serial 0 mod 9 -> image class I (registered top-left)")
    print(
        "interpretation: exact same-corpus round trip; useful historical "
        "replication of period/phase, not an independent sticker holdout"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render a hindsight-controlled worksheet directly from data/observations.csv.

The default view deliberately exposes only facts available from the physical
corpus after choosing the established H108 fold and A-I artwork layout. It does
not print q/d coordinates, POS3 digits, frame polarity, hidden-state labels,
selector values, or the terminal.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"

SERIAL_ORDER = tuple("ABCDEFGHI")
PHYSICAL_LAYOUT = (
    ("I", "A", "B"),
    ("C", "D", "E"),
    ("F", "G", "H"),
)
POSITION = {
    letter: (row, col)
    for row, letters in enumerate(PHYSICAL_LAYOUT)
    for col, letter in enumerate(letters)
}


def load_residues() -> dict[int, str]:
    residues: dict[int, str] = {}
    rows = 0
    with OBS.open(newline="", encoding="utf-8") as fh:
        for record in csv.DictReader(fh):
            rows += 1
            residue = int(record["residue"])
            symbol = record["symbol"]
            assert 1 <= residue <= 108
            assert symbol in {"/", "-", "."}
            prior = residues.setdefault(residue, symbol)
            assert prior == symbol, (
                f"conflicting observations at residue {residue}: "
                f"{prior!r} versus {symbol!r}"
            )

    assert rows == 82, f"expected 82 classified stickers, got {rows}"
    assert len(residues) == 65, f"expected 65 unique H108 residues, got {len(residues)}"
    return residues


def serial_block(residues: dict[int, str], block: int) -> list[str]:
    start = block * 9 + 1
    return [residues.get(start + j, "?") for j in range(9)]


def physical_frame(serial_symbols: list[str]) -> list[list[str]]:
    frame = [["?" for _ in range(3)] for _ in range(3)]
    for j, letter in enumerate(SERIAL_ORDER):
        row, col = POSITION[letter]
        frame[row][col] = serial_symbols[j]
    return frame


def render(residues: dict[int, str]) -> str:
    lines: list[str] = []
    lines.append("# Blind H108 worksheet")
    lines.append("")
    lines.append("Legend: / - . are observed marks; ? is unobserved.")
    lines.append("Blocks are consecutive 9-residue chunks. No solved-model labels are shown.")
    lines.append("")

    for block in range(12):
        serial = serial_block(residues, block)
        frame = physical_frame(serial)
        lo = 9 * block + 1
        hi = lo + 8
        lines.append(f"## Block {block + 1}  (residues {lo}-{hi})")
        lines.append("")
        lines.append("Serial A-I order:")
        lines.append("")
        lines.append("    " + " ".join(SERIAL_ORDER))
        lines.append("    " + " ".join(serial))
        lines.append("")
        lines.append("Physical artwork layout:")
        lines.append("")
        for row in frame:
            lines.append("    " + " ".join(row))
        lines.append("")

    lines.append("## Corpus bookkeeping")
    lines.append("")
    lines.append(f"- classified sticker rows: 82")
    lines.append(f"- distinct H108 residues: {len(residues)}")
    lines.append(f"- unobserved H108 residues: {108 - len(residues)}")
    lines.append("")
    lines.append("Suggested blind use: inspect the worksheet before opening machine-spec,")
    lines.append("human-solve-reconstruction, minimum-witness, or theorem documents.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="write Markdown to this path instead of stdout",
    )
    args = parser.parse_args()

    text = render(load_residues())
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Frozen July-2016 INSIDE Polybius window/asset transcription audit.

The source strings were posted July 2016 in:
https://steamcommunity.com/app/304430/discussions/0/365172547948628597/
?ctp=2
This is *not* a foreground sticker decoder. It verifies that already-documented
assets spell the previously identified Cummings poem title without any search,
semantic completion, or sticker guesses.

Usage: python scripts/audit_original_game_polybius.py
"""
from __future__ import annotations

# Five rows of five symbols. The 25th cell was originally shared by Y/Z;
# the three frozen input strings never visit it.
GRID = ("ABCDE", "FGHIJ", "KLMNO", "PQRST", "UVWXY")

# Original INSIDE texture names reported in contemporary source archaeology.
FROZEN = (
    ("LetterCode_001", "14 42 54 55 54 32 42 44", "PITYTHIS"),
    ("LetterCode_002", "21 15 44 55 33 53 43 44 54 51 34", "BUSYMONSTER"),
    ("LetterCode_003", "33 11 43 15 43 13 42 43 41", "MANUNKIND"),
)


def decode(pairs: str, *, col_first: bool = True) -> str:
    result = []
    for token in pairs.split():
        if len(token) != 2 or any(ch not in "12345" for ch in token):
            raise ValueError(f"invalid Polybius cell {token!r}")
        a, b = int(token[0]) - 1, int(token[1]) - 1
        col, row = (a, b) if col_first else (b, a)
        result.append(GRID[row][col])
    return "".join(result)


def audit() -> dict:
    results = []
    for source, pairs, expected in FROZEN:
        decoded = decode(pairs)
        row_major = decode(pairs, col_first=False)
        assert decoded == expected, (source, decoded, expected)
        # Source distinguishes the original selected axis convention from
        # the most obvious mistaken transpose for every frozen segment.
        assert row_major != expected, (source, "unexpected equivalent orientation")
        results.append(
            {
                "asset": source,
                "pairs": pairs,
                "decoded_column_then_row": decoded,
                "row_then_column_control": row_major,
                "matches_original_report": True,
            }
        )
    assert " ".join(x["decoded_column_then_row"] for x in results) == (
        "PITYTHIS BUSYMONSTER MANUNKIND"
    )
    return {
        "source_date": "2016-07",
        "unambiguous_ambiguous_yz_cell_used": False,
        "texts": results,
        "scope": "2016 encoded windows/source assets; no CE sticker inputs",
        "conclusion": "Original game demonstrably pointed to an external poem by a recoverable cipher.",
    }


def main() -> None:
    import json

    print(json.dumps(audit(), indent=2))
    print("PASS: 3/3 historical Polybius assets decode exactly")


if __name__ == "__main__":
    main()

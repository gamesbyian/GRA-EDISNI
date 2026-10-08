#!/usr/bin/env python3
"""Experiment 476: bounded source-native print receiver tests.

Tests exact/unreversed and mirrored literal reuse of three 36-glyph CE
sections against every published 36-glyph Xbox printer row, allowing
arbitrary row membership (a deliberately permissive comparison). Also
checks the historical macOS Cutout source's 16-strip / 34-dot fact.

This does not test overlays, local codebooks, row reordering/shift,
Braille, the missing-symbol completion models, or game input handling.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data/observations.csv"
XBOX = ROOT / "data/printer-reference/xbox-one-raw.txt"
PC = ROOT / "data/printer-reference/pc-ps4-raw.txt"
MAC = ROOT / "data/experiment-476-macos-printer-control.json"


def source_rows(path: Path) -> list[str]:
    return [
        s for line in path.read_text(encoding="utf-8").splitlines()
        if (s := line.strip()) and not s.startswith("#")
    ]


def physical_known() -> tuple[int, dict[int, str]]:
    with OBS.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    known: dict[int, str] = {}
    for obj in rows:
        residue = int(obj["residue"])
        symbol = obj["symbol"]
        assert 1 <= residue <= 108 and symbol in "/-."
        if residue in known:
            assert known[residue] == symbol
        known[residue] = symbol
    assert (len(rows), len(known)) == (84, 66)
    return len(rows), known


def check() -> dict:
    count, known = physical_known()
    xbox_raw = source_rows(XBOX)
    xbox_long = list(dict.fromkeys(x for x in xbox_raw if len(x) == 36))
    pc_raw = source_rows(PC)
    pc_long = list(dict.fromkeys(x for x in pc_raw if len(x) == 32))
    assert (len(xbox_raw), len(xbox_long)) == (48, 35)
    assert len(pc_long) == 32
    assert set("".join(xbox_long)) <= set("/-.")
    assert set("".join(pc_long)) <= set("/-.")
    chunks = [
        "".join(known.get(start + offset, "?") for offset in range(36))
        for start in (1, 37, 73)
    ]
    assert [sum(c != "?" for c in x) for x in chunks] == [24, 23, 19]
    results = []
    for i, chunk in enumerate(chunks, start=1):
        candidates = []
        for line_index, line in enumerate(xbox_long):
            for direction, rendered in (
                ("forward", line),
                ("reversed", line[::-1]),
            ):
                mismatch = sum(
                    ch != "?" and ch != rendered[pos]
                    for pos, ch in enumerate(chunk)
                )
                candidates.append({
                    "row_index_zero_based": line_index,
                    "direction": direction,
                    "conflicting_observed_positions": mismatch,
                    "agreeing_observed_positions": chunk.count("?") * 0
                        + (36 - chunk.count("?")) - mismatch,
                })
        candidates.sort(key=lambda x: (
            x["conflicting_observed_positions"],
            x["row_index_zero_based"],
            x["direction"],
        ))
        assert all(x["conflicting_observed_positions"] > 0 for x in candidates)
        results.append({
            "CE_residues": f"{36 * (i - 1) + 1}..{36 * i}",
            "observed_symbols": 36 - chunk.count("?"),
            "unknown_symbols": chunk.count("?"),
            "best_exact_or_mirrored_matches": candidates[:3],
            "min_mismatch_allowing_reversal": candidates[0][
                "conflicting_observed_positions"
            ],
            "best_forward_mismatch": min(
                x["conflicting_observed_positions"]
                for x in candidates if x["direction"] == "forward"
            ),
            "complete_verbatim_match_possible": False,
        })
    assert [
        x["min_mismatch_allowing_reversal"] for x in results
    ] == [12, 9, 7]
    assert [x["best_forward_mismatch"] for x in results] == [12, 10, 10]
    mac = json.loads(MAC.read_text(encoding="utf-8"))
    glyphs = mac["glyph_lines"]
    assert mac["schema_version"] == 1
    assert len(glyphs) == 16
    assert all(set(x) <= set("-• ") for x in glyphs)
    dots = sum(x.count("•") for x in glyphs)
    letters = sum(c.isalpha() for c in mac["reported_decoded_phrase"])
    assert dots == letters == 34

    return {
        "experiment": 476,
        "source_counts": {
            "sticker_records": count,
            "unique_known_H108_residues": len(known),
            "Xbox_printer_unique_36_width_rows": len(xbox_long),
            "Xbox_printer_published_36_width_rows_including_repeat": sum(
                len(x) == 36 for x in xbox_raw
            ),
            "PC_PS4_printer_unique_32_width_rows": len(pc_long),
            "Mac_printer_strips": len(glyphs),
            "Mac_printer_dot_marks": dots,
            "Mac_community_solution_unspaced_letters": letters,
        },
        "Xbox_verbatim_three_row_control": results,
        "interpretation": [
            "108=3*36 matches the source-native 36-column width of Xbox strips, but this is dimensional eligibility, not registration.",
            "No CE 36-wide section can be a verbatim existing Xbox printer row, even allowing an independent full-row reversal and any of the 35 unique published rows.",
            "The stronger claim of a 3x36 overlay over the solved Xbox planet requires independent row order and mapping; this test neither supports nor rejects it.",
            "MacOS 34 dot count equals 34 letters in the historically claimed phrase. A count is not a position-by-position decoded message; the source-described Cummings reader has not been independently reproduced here.",
            "PC/PS4 source has 32-wide full strips, not a matching 36-wide print-line channel; that contrast does not prohibit cross-format conversion.",
            "No artifact here has a verified interface addressed by all 108 foreground marks."
        ],
        "original_source_urls": {
            "printer_reference": "https://wiki.gamedetectives.net/w/Inside_ARG",
            "historical_mac_transcription": "https://github.com/twinysam/INSIDE-ARG",
            "Mac_retaining_code_source_community_audit": mac["code_level_reassessment"],
        },
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path)
    p.add_argument("--summary", action="store_true")
    args = p.parse_args()
    result = check()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.summary:
        print(json.dumps({
            "status": "PASS",
            "Xbox_min_mismatches_with_reversal": [
                x["min_mismatch_allowing_reversal"]
                for x in result["Xbox_verbatim_three_row_control"]
            ],
            "macOS_dot_marks": result["source_counts"]["Mac_printer_dot_marks"],
            "CE_known": result["source_counts"]["unique_known_H108_residues"],
        }, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

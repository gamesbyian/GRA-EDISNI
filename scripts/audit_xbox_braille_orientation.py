#!/usr/bin/env python3
"""Experiment 369: test how orientation-dependent the Xbox nine-digit residual is."""

from collections import Counter
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-369-xbox-braille-orientation-audit.json"

ROWS = [
    "9N879763",
    "087E894W26",
    "09817986469",
    "PL663AN79ET",
    "976828'9126",
    "7DI89829812",
    "!CO792412-",
    "984VE3229",
    "679RED6",
]

# Braille-ASCII dot masks, bits are dots 1..6.
# Only characters present in the published Xbox transcription are needed here.
MASK = {
    "!": "011101", "'": "001000", "-": "001001",
    "0": "001011", "1": "010000", "2": "011000", "3": "010010",
    "4": "010011", "5": "010001", "6": "011010", "7": "011011",
    "8": "011001", "9": "001010",
    "A": "100000", "C": "100100", "D": "100110", "E": "100010",
    "I": "010100", "L": "111000", "N": "101110", "O": "101010",
    "P": "111100", "R": "111010", "T": "011110", "V": "111001",
    "W": "010111",
}
DIGIT_BY_MASK = {MASK[str(i)]: str(i) for i in range(10)}

SYMMETRIES = {
    "identity": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "left_right_mirror": {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3},
    "top_bottom_mirror": {1: 3, 2: 2, 3: 1, 4: 6, 5: 5, 6: 4},
    "rotate_180": {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1},
}


def transform(mask: str, perm: dict[int, int]) -> str:
    dots = {i for i, bit in enumerate(mask, 1) if bit == "1"}
    moved = {perm[i] for i in dots}
    return "".join("1" if i in moved else "0" for i in range(1, 7))


def digit_readout(perm: dict[int, int]) -> list[str]:
    out = []
    for ch in "".join(ROWS):
        remapped = transform(MASK[ch], perm)
        digit = DIGIT_BY_MASK.get(remapped)
        if digit is not None:
            out.append(digit)
    return out


def summarize(digits: list[str]) -> dict:
    counts = Counter(digits)
    observed = "".join(d for d in "0123456789" if counts[d])
    missing = "".join(d for d in "0123456789" if not counts[d])
    return {
        "digit_cells": len(digits),
        "distinct_digits": len(observed),
        "observed_digits": observed,
        "missing_digits": missing,
        "counts": {d: counts[d] for d in "0123456789"},
    }


def main() -> None:
    symmetry_results = {name: summarize(digit_readout(perm)) for name, perm in SYMMETRIES.items()}

    permutation_hist = Counter()
    nine_state_missing = Counter()
    at_least_nine = 0
    ten_state = 0

    for tup in itertools.permutations(range(1, 7)):
        perm = {i + 1: tup[i] for i in range(6)}
        summary = summarize(digit_readout(perm))
        d = summary["distinct_digits"]
        permutation_hist[d] += 1
        if d >= 9:
            at_least_nine += 1
        if d == 10:
            ten_state += 1
        if d == 9:
            nine_state_missing[summary["missing_digits"]] += 1

    result = {
        "experiment": 369,
        "source": "published Xbox Braille-ASCII transcription preserved in data/printer-reference/metadata.json",
        "question": "Is the nine-of-ten decimal-glyph residual merely invariant under Braille-cell orientation?",
        "correct_orientation_basis": "The identity orientation is independently fixed by the readable NEWPLANETDISCOVERED message.",
        "braille_ascii_digit_masks": {str(i): MASK[str(i)] for i in range(10)},
        "missing_5_mask": MASK["5"],
        "missing_5_dots": [i for i, bit in enumerate(MASK["5"], 1) if bit == "1"],
        "rectangular_cell_symmetries": symmetry_results,
        "all_720_dot_permutations_descriptive_null": {
            "distinct_digit_histogram": {str(k): permutation_hist[k] for k in sorted(permutation_hist)},
            "permutations_with_9_distinct_digits": permutation_hist[9],
            "permutations_with_10_distinct_digits": ten_state,
            "permutations_with_at_least_9_distinct_digits": at_least_nine,
            "fraction_with_at_least_9_distinct_digits": at_least_nine / 720,
            "missing_digit_among_9_state_permutations": dict(sorted(nine_state_missing.items())),
            "warning": "The 720 dot permutations are a descriptive relabeling null, not a historical operation family.",
        },
        "interpretation": (
            "The nine-state decimal residual is orientation-sensitive rather than a trivial invariant of the same Braille cells. "
            "Among the four geometry-preserving symmetries of a 2x3 Braille cell, only the independently established correct "
            "orientation yields nine distinct ASCII digit glyphs. Across all 720 arbitrary dot relabelings, only 20 yield at "
            "least nine distinct digits. This makes the 9-state observation more structurally specific, but still does not "
            "supply a mapping to CE A-I or show authorial intent."
        ),
    }

    identity = symmetry_results["identity"]
    if identity["distinct_digits"] != 9 or identity["missing_digits"] != "5":
        raise SystemExit("identity orientation no longer reproduces Experiment 368")
    if any(symmetry_results[name]["distinct_digits"] >= 9 for name in SYMMETRIES if name != "identity"):
        raise SystemExit("unexpected geometry-preserving symmetry also reaches nine digits")
    if at_least_nine != 20 or ten_state != 4:
        raise SystemExit("dot-permutation null changed unexpectedly")

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

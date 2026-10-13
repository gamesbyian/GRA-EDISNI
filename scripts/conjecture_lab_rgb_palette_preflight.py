#!/usr/bin/env python3
"""Closed-corpus RGB palette preflight. DISCOVER/DEVELOP, not a CE decode.

Enumerate compatible positional words in the first nine sticker frames and
one-slash-per-image-class depth selectors in the last three frames. Test eight
declared literal RGB-packing orders, each under six RGB permutations.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "conjecture-lab-h108-66-residue-freeze-2026-10-09.csv"
# Colours retrospectively recovered from the historical gate-98 puzzle.
GATE98_PALETTE = ((3, 1, 1), (1, 4, 1), (3, 3, 3),
                  (5, 1, 5), (3, 3, 0), (2, 2, 6))
# In serial A..I order, physical columns of solved IAB/CDE/FGH layout.
PHYSICAL_COLUMNS = ((8, 2, 5), (0, 3, 6), (1, 4, 7))
EXPECTED_COUNTS = {
    "physical_records": 84, "unique_residues": 66,
    "primary_completions": 18, "tail_completions": 18,
    "joint_completions": 324, "readouts": 15552,
    "score_histogram": {"0": 15276, "1": 276}, "max_matches": 1,
}


def load_observations(path: Path) -> tuple[dict[int, str], int]:
    observed = {}
    count = 0
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            count += 1
            serial, residue, symbol = int(row["serial"]), int(row["residue"]), row["symbol"]
            if not 1 <= residue <= 108 or residue != (serial - 1) % 108 + 1:
                raise ValueError(f"Bad serial/residue row: {row!r}")
            expected = ("/", "-") if residue <= 81 else ("/", ".")
            if symbol not in expected:
                raise ValueError(f"Unexpected physical alphabet: {row!r}")
            if residue in observed and observed[residue] != symbol:
                raise ValueError(f"Conflicting observations at residue {residue}")
            observed[residue] = symbol
    return observed, count


def primary_frame_candidates(obs: dict[int, str], frame: int) -> list[tuple[int, int, int]]:
    choices = []
    for minority, majority in (("/", "-"), ("-", "/")):
        columns = []
        for physical_column in PHYSICAL_COLUMNS:
            columns.append([
                depth for depth in range(3)
                if all(obs.get(frame * 9 + position + 1,
                               minority if i == depth else majority)
                       == (minority if i == depth else majority)
                       for i, position in enumerate(physical_column))
            ])
        choices.extend(itertools.product(*columns))
    return sorted(set(choices))


def tail_selector_candidates(obs: dict[int, str], image_class: int) -> list[int]:
    """Q4 uses one slash per A..I depth stack; the other marks are dots."""
    return [
        chosen_depth for chosen_depth in range(3)
        if all(obs.get(82 + 9 * depth + image_class,
                       "/" if depth == chosen_depth else ".")
               == ("/" if depth == chosen_depth else ".")
               for depth in range(3))
    ]


def six_colors(trits: tuple[int, ...], layout: str, digit_order: str,
               channel_perm: tuple[int, int, int]) -> tuple[tuple[int, int, int], ...]:
    if len(trits) != 36 or any(t not in (0, 1, 2) for t in trits):
        raise ValueError("Expected exactly 36 ternary digits")

    def value(first: int, second: int) -> int:
        return 3 * first + second if digit_order == "high" else first + 3 * second

    result = []
    for color in range(6):
        if layout == "color_major":
            channels = [value(trits[6 * color + 2 * channel],
                              trits[6 * color + 2 * channel + 1])
                        for channel in range(3)]
        elif layout == "channel_major":
            channels = [value(trits[12 * channel + 2 * color],
                              trits[12 * channel + 2 * color + 1])
                        for channel in range(3)]
        else:
            raise ValueError(layout)
        result.append(tuple(channels[channel] for channel in channel_perm))
    return tuple(result)


def rgb_positive_control() -> None:
    """36 free ternary digits can represent six RGB triples in range 0..8."""
    trits = tuple(x for color in GATE98_PALETTE for component in color
                  for x in divmod(component, 3))
    assert len(trits) == 36
    assert six_colors(trits, "color_major", "high", (0, 1, 2)) == GATE98_PALETTE


def audit(obs: dict[int, str], record_count: int) -> dict:
    rgb_positive_control()
    frames = [primary_frame_candidates(obs, i) for i in range(9)]
    selectors = [tail_selector_candidates(obs, i) for i in range(9)]
    if any(not choices for choices in frames + selectors):
        raise ValueError("Physical observations contradict the declared grammar")
    frame_count = 1
    tail_count = 1
    for choices in frames:
        frame_count *= len(choices)
    for choices in selectors:
        tail_count *= len(choices)

    palette = set(GATE98_PALETTE)
    histogram = Counter()
    by_layout = {}
    best = 0
    best_witness = None
    perms = tuple(itertools.permutations(range(3)))
    for frame_words in itertools.product(*frames):
        frame_major = tuple(x for word in frame_words for x in word)
        column_major = tuple(frame_words[i][j] for j in range(3) for i in range(9))
        for depth_words in itertools.product(*selectors):
            for primary_order, primary in (("frame_major", frame_major),
                                           ("column_major", column_major)):
                trits = primary + depth_words  # Q4 A..I selector depths.
                for layout in ("color_major", "channel_major"):
                    for digit_order in ("high", "low"):
                        family = f"{primary_order}/{layout}/{digit_order}"
                        for perm in perms:
                            output = six_colors(trits, layout, digit_order, perm)
                            matches = len(palette.intersection(output))
                            histogram[matches] += 1
                            by_layout[family] = max(by_layout.get(family, 0), matches)
                            if matches > best:
                                best = matches
                                best_witness = {
                                    "primary_order": primary_order,
                                    "layout": layout, "digit_order": digit_order,
                                    "channel_permutation": perm,
                                    "rgb_values": output,
                                    "matched": sorted(palette.intersection(output)),
                                }
    return {
        "physical_records": record_count, "unique_residues": len(obs),
        "primary_frame_options": list(map(len, frames)),
        "tail_class_options": list(map(len, selectors)),
        "primary_completions": frame_count, "tail_completions": tail_count,
        "joint_completions": frame_count * tail_count,
        "readouts": sum(histogram.values()),
        "score_histogram": dict(sorted((str(k), v) for k, v in histogram.items())),
        "max_matches": best, "full_palette_matches": histogram.get(6, 0),
        "family_max_matches": dict(sorted(by_layout.items())),
        "first_best_witness": best_witness,
        "interpretation": "Retrospective RGB-packing negative only; no CE receiver established.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--check-frozen", action="store_true",
                        help="assert exact 2026-10-09 snapshot results")
    parser.add_argument("--output", type=Path, help="write JSON results")
    args = parser.parse_args()
    observed, count = load_observations(args.csv)
    result = audit(observed, count)
    if args.check_frozen:
        for key, expected in EXPECTED_COUNTS.items():
            if result[key] != expected:
                raise AssertionError(f"{key}: got {result[key]!r}, expected {expected!r}")
    body = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()

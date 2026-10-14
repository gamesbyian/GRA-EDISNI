#!/usr/bin/env python3
"""CL-BAR-01: Code 128 width-pattern compatibility and matched controls.

DISCOVER, not a decoded message. Uses only original observed sticker marks.
No non-standard packages, network, assumed symbol completions, or machine model.

Run: python scripts/conjecture_lab_code128_widths.py --controls 120 \
       --output data/conjecture-lab-code128-widths-2026-10-13.json
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"
ALPHABET = ("-", "/", ".")
# Published Code 128 width table, symbol values 0..105; each six digits
# alternates three bars and three spaces, widths 1..4 totaling 11.
# Last three entries 103/104/105 are the start A/B/C characters.
# Source: Code 128 / ISO 15417 symbol assignments, e.g. GS1 General Specifications.
CODE128_WIDTHS = """
212222 222122 222221 121223 121322 131222 122213 122312 132212 221213
221312 231212 112232 122132 122231 113222 123122 123221 223211 221132
221231 213212 223112 312131 311222 321122 321221 312212 322112 322211
212123 212321 232121 111323 131123 131321 112313 132113 132311 211313
231113 231311 112133 112331 132131 113123 113321 133121 313121 211331
231131 213113 213311 213131 311123 311321 331121 312113 312311 332111
314111 221411 431111 111224 111422 121124 121421 141122 141221 112214
112412 122114 122411 142112 142211 241211 221114 413111 241112 134111
111242 121142 121241 114212 124112 124211 411212 421112 421211 212141
214121 412121 111143 111341 131141 114113 114311 411113 411311 113141
114131 311141 411131 211412 211214 211232
""".split()
WIDTH_TUPLES = tuple(tuple(int(ch) for ch in p) for p in CODE128_WIDTHS)
assert len(WIDTH_TUPLES) == len(set(WIDTH_TUPLES)) == 106
assert all(len(p) == 6 and sum(p) == 11 and sum(p[::2]) % 2 == 0 for p in WIDTH_TUPLES)
assert CODE128_WIDTHS[103:106] == ["211412", "211214", "211232"]


@lru_cache(maxsize=20_000)
def compatible_codewords(known_widths: tuple[int, ...]) -> int:
    """Count matching Code 128 patterns; zero denotes genuine incompatibility.

    Each zero is an unobserved cell (not a presumed fourth width).
    """
    assert len(known_widths) == 6
    return sum(all(a == 0 or a == b for a, b in zip(known_widths, p)) for p in WIDTH_TUPLES)


def source_stream(path: Path) -> tuple[list[str | None], dict]:
    observed: dict[int, str] = {}
    physical_records = 0
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = int(row["residue"])
            mark = row["symbol"]
            if not 1 <= r <= 108 or mark not in ALPHABET:
                raise ValueError(f"Unexpected raw sticker record: {row}")
            if r in observed and observed[r] != mark:
                raise ValueError(f"Contradictory observations for residue {r}")
            observed[r] = mark
            physical_records += 1
    # The period's 0 position is residue 108, so serial 1..108 is explicit.
    seq = [observed.get(r) for r in range(1, 109)]
    assert len(seq) == 108
    counts = dict(Counter(c for c in seq if c))
    return seq, {"physical_records": physical_records, "unique_residues": len(observed),
                 "unobserved_residues": 108 - len(observed), "observed_symbol_counts": counts}


def arrangements(seq: list[str | None]):
    # Deliberately strong, permissive exploration. Each glyph must map to a
    # distinct element width; choose three of 1..4. Reverse and allow one of
    # six width-element reading phases. Every alternative is counted as fitted.
    for widths in itertools.permutations((1, 2, 3, 4), 3):
        mapping = dict(zip(ALPHABET, widths))
        for direction in ("serial_ascending", "serial_descending"):
            ordered = seq if direction == "serial_ascending" else seq[::-1]
            for phase in range(6):
                complete = [ordered[i:i+6] for i in range(phase, len(ordered)-5, 6)]
                compatible = []
                score = 0.0
                for chunk in complete:
                    w = tuple(mapping.get(c, 0) for c in chunk)
                    n = compatible_codewords(w)
                    compatible.append(n)
                    # Uniform 4-width null at known sites. This ratio is a
                    # *descriptive* likelihood of a hand-picked model, not proof.
                    if n:
                        score += math.log2(n / 106) + 2 * sum(x > 0 for x in w)
                failures = sum(n == 0 for n in compatible)
                yield {
                    "glyph_to_width": mapping, "direction": direction, "phase": phase,
                    "chunks": len(complete), "incompatible_chunks": failures,
                    "compatible_chunks": len(complete) - failures,
                    "log2_ratio_if_compatible": round(score, 6) if failures == 0 else None,
                    "compatible_patterns_per_chunk": compatible,
                }


def evaluate(seq: list[str | None], *, retain_candidates: bool = False):
    # Rank by contradiction count only (not by language-looking values).
    # Equal rankings are maintained to expose search freedom.
    best = 10**6
    models = []
    histogram = Counter()
    for model in arrangements(seq):
        err = model["incompatible_chunks"]
        histogram[err] += 1
        if err < best:
            best, models = err, []
        if err == best:
            models.append(model)
    # These are full post-selection counts, not independent discoveries.
    top = sorted(models, key=lambda m: (-float(m["log2_ratio_if_compatible"] or -1e9),
                                           m["direction"], m["phase"],
                                           tuple(m["glyph_to_width"][x] for x in ALPHABET)))
    out = {"min_incompatible_chunks": best, "models_tying_minimum": len(models),
           "fully_compatible_models": histogram[0], "total_models": sum(histogram.values()),
           "incompatible_chunk_histogram": {str(k): v for k, v in sorted(histogram.items())}}
    if retain_candidates:
        out["best_fitted_examples"] = top[:5]
    return out


def frame_preserving_shuffle(seq: list[str | None], rng: random.Random):
    """Keep the nine residue blocks and each block's exact observation mask.

    The 108 cells are 12 consecutive nine-sticker blocks. Shuffle *only* the
    observed labels inside each block, retaining slash/dot tail distinctions,
    within-block mark counts, and all missing positions.
    """
    shuffled = seq[:]
    for i in range(0, 108, 9):
        indices = [j for j in range(i, i + 9) if seq[j] is not None]
        marks = [seq[j] for j in indices]
        rng.shuffle(marks)
        for j, value in zip(indices, marks):
            shuffled[j] = value
    return shuffled


def region_preserving_shuffle(seq: list[str | None], rng: random.Random):
    # First 81 and last 27 are physically different alphabets. Keep each
    # position's observation mask, the region and its total symbol counts.
    shuffled = seq[:]
    for lo, hi in ((0, 81), (81, 108)):
        indices = [i for i in range(lo, hi) if seq[i] is not None]
        marks = [seq[i] for i in indices]
        rng.shuffle(marks)
        for i, value in zip(indices, marks):
            shuffled[i] = value
    return shuffled


def generate_report(path: Path, controls: int, seed: int):
    seq, provenance = source_stream(path)
    actual = evaluate(seq, retain_candidates=True)
    rng = random.Random(seed)
    nulls = {}
    for name, shuffler in (("frame_preserving", frame_preserving_shuffle),
                          ("region_preserving", region_preserving_shuffle)):
        values = [evaluate(shuffler(seq, rng)) for _ in range(controls)]
        errors = [p["min_incompatible_chunks"] for p in values]
        nulls[name] = {
            "iterations": controls,
            "minimum_incompatibility_histogram": dict(sorted(Counter(errors).items())),
            "controls_at_least_as_compatible": sum(v <= actual["min_incompatible_chunks"] for v in errors),
            "fraction_at_least_as_compatible": round(
                sum(v <= actual["min_incompatible_chunks"] for v in errors) / controls, 6)
            if controls else None,
            "zero_incompatibility_control_count": errors.count(0),
        }
    return {
        "schema_version": 1, "research_mode": "DISCOVER", "source": str(path.name),
        "provenance": provenance,
        "model": "Three glyphs injectively mapped to three of four Code128 element widths; permute 24 maps, two directions, six phases; ignore unmatched leading/trailing elements",
        "fitted_parameter_count": 24 * 2 * 6,
        "null_seed": seed, "actual": actual, "null_controls": nulls,
        "physical_length_rejections": {
            "raw_108_modules_full_code128_without_quiet_zone":
                "108 != 35 + 11*N for any nonnegative integer N",
            "raw_108_modules_full_gs1_128_without_quiet_zone":
                "108 != 46 + 11*N for any nonnegative integer N",
            "note": "Includes start, modulo-103 check, stop; GS1 additionally FNC1. Quiet zones add at least 20 modules and also do not rescue 108."
        },
        "limitations": [
            "Not a full Code128 validation; segments lack mandated start/stop/checksum.",
            "The class-to-width, phase, and direction are fitted post hoc; report matched controls.",
            "Unobserved cells may admit many completions; zero incompatible chunks is weak evidence.",
            "A 108-entry symbol dictionary, keying, or actual photographed barcode is a distinct hypothesis.",
            "No barcode from the Discord discussion was supplied for decoding; screenshot contains specification text only.",
        ],
    }


def selftest():
    assert len(WIDTH_TUPLES) == 106 and len(set(WIDTH_TUPLES)) == 106
    assert compatible_codewords((2, 1, 1, 2, 1, 4)) == 1  # Start B
    assert compatible_codewords((4, 4, 4, 4, 4, 4)) == 0
    assert compatible_codewords((0,) * 6) == 106
    assert compatible_codewords((2, 1, 1, 2, 1, 0)) >= 1
    sample = ["/" if i % 3 else "-" if i % 5 else None for i in range(108)]
    rng = random.Random(42)
    for shuffle in (frame_preserving_shuffle, region_preserving_shuffle):
        s = shuffle(sample, rng)
        assert all((a is None) == (b is None) for a, b in zip(sample, s))
        assert Counter(x for x in sample if x is not None) == Counter(x for x in s if x is not None)
        assert len(list(arrangements(sample))) == 288
    assert (108-35) % 11 and (108-46) % 11
    print("Code128 catalogue, feasibility, null controls and lengths: OK")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--observations", type=Path, default=OBSERVATIONS)
    p.add_argument("--output", type=Path)
    p.add_argument("--controls", type=int, default=120)
    p.add_argument("--seed", type=int, default=128108)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest:
        selftest()
        return
    if args.controls < 0:
        p.error("--controls must be >= 0")
    result = generate_report(args.observations, args.controls, args.seed)
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(raw, encoding="utf-8")
    else:
        print(raw, end="")


if __name__ == "__main__":
    main()
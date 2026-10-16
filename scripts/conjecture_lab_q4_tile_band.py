#!/usr/bin/env python3
"""DISCOVER: compare native Q4 depths to band darkness in preserved A-I artwork.

Requires Pillow (CI pins it). Scores are computed from historically sourced
846shEE A-I evidence masters, *never* from inpainted pixels. Four fixed
axis/polarity readers and one coverage control; an exact 9! class-shuffle
test reports each reader and the four-reader familywise maximum.

Run: python scripts/conjecture_lab_q4_tile_band.py --out-json /tmp/result.json
"""
import argparse
import itertools
import json
from pathlib import Path

from PIL import Image

from conjecture_lab_native_q4_receiver import ROOT, q4_choices, source_data

ART = ROOT / "artifacts/background-tile-evidence-masters"
CLASSES = "ABCDEFGHI"
METHODS = ("row_dark", "row_light", "column_dark", "column_light")
CONTROL = "row_coverage"


def band_scores(tile, mask, axis):
    assert tile.size == mask.size == (512, 512)
    rgb = tile.convert("RGBA")
    evidence = mask.convert("L")
    dark = [0.0] * 3
    valid = [0] * 3
    total = [0] * 3
    width, height = tile.size
    pix = rgb.load()
    mpix = evidence.load()
    for y in range(height):
        for x in range(width):
            band = 3 * (y if axis == "row" else x) // 512
            total[band] += 1
            red, green, blue, alpha = pix[x, y]
            if alpha < 128 or mpix[x, y] < 128:
                continue
            valid[band] += 1
            luminance = (299 * red + 587 * green + 114 * blue) / 1000
            dark[band] += 255 - luminance
    assert all(valid), (axis, valid)
    return [dark[k] / valid[k] for k in range(3)], [
        valid[k] / total[k] for k in range(3)
    ]


def choose(values, take_max):
    # Tie-breakers are source-independent and fixed before inspecting images.
    order = max if take_max else min
    chosen = order(values)
    return next(k for k, value in enumerate(values) if value == chosen)


def bands_from_image():
    predicted = {method: [] for method in METHODS + (CONTROL,)}
    diagnostics = {}
    for letter in CLASSES:
        tile_path = ART / (letter + ".png")
        mask_path = ART / (letter + "-known-mask.png")
        assert tile_path.exists() and mask_path.exists(), (tile_path, mask_path)
        with Image.open(tile_path) as t, Image.open(mask_path) as m:
            row_ink, row_coverage = band_scores(t, m, "row")
            col_ink, col_coverage = band_scores(t, m, "column")
        predicted["row_dark"].append(choose(row_ink, True))
        predicted["row_light"].append(choose(row_ink, False))
        predicted["column_dark"].append(choose(col_ink, True))
        predicted["column_light"].append(choose(col_ink, False))
        predicted[CONTROL].append(choose(row_coverage, True))
        diagnostics[letter] = {
            "mean_darkness_by_row": row_ink,
            "mean_darkness_by_column": col_ink,
            "observed_fraction_by_row": row_coverage,
            "observed_fraction_by_column": col_coverage,
        }
    return predicted, diagnostics


def direct_hits(bands, depth_options, permutation):
    return sum(
        bands[permutation[class_index]] in depth_options[class_index]
        for class_index in range(9)
    )


def exact_null(predicted, choices):
    observed = {
        method: direct_hits(predicted[method], choices, tuple(range(9)))
        for method in METHODS + (CONTROL,)
    }
    methods = METHODS + (CONTROL,)
    ge = dict.fromkeys(methods, 0)
    ge["any_of_four"] = 0
    hist = {method: [0] * 10 for method in methods + ("any_of_four",)}
    observed_max = max(observed[m] for m in METHODS)
    total = 0
    for perm in itertools.permutations(range(9)):
        total += 1
        values = {m: direct_hits(predicted[m], choices, perm) for m in methods}
        for m, hit in values.items():
            hist[m][hit] += 1
            ge[m] += hit >= observed[m]
        worst = max(values[m] for m in METHODS)
        hist["any_of_four"][worst] += 1
        ge["any_of_four"] += worst >= observed_max
    assert total == 362880
    return {
        "observed_hits": observed,
        "observed_four_reader_maximum": observed_max,
        "null_permutations": total,
        "count_as_good_or_better": ge,
        "exact_upper_tail_fraction": {key: val / total for key, val in ge.items()},
        "null_hit_histograms": hist,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-json", type=Path, required=False)
    args = parser.parse_args()
    observed, _ = source_data()
    choices = q4_choices(observed)
    assert tuple(len(c) for c in choices) == (3,1,3,1,1,1,2,1,1)
    predictions, diagnostic = bands_from_image()
    test = exact_null(predictions, choices)
    print("Source: evidence-preserving 846shEE A-I 512x512 known-mask masters.")
    print("Q4 accepted depth sets:", list(zip(CLASSES, choices)))
    for method in METHODS + (CONTROL,):
        print(method, "predicted", predictions[method],
              "matches", test["observed_hits"][method],
              "exact shuffle upper-tail fraction",
              test["exact_upper_tail_fraction"][method])
    print("Familywise four-reader max hits:",
          test["observed_four_reader_maximum"],
          "exact class-shuffle fraction:",
          test["exact_upper_tail_fraction"]["any_of_four"])
    payload = {
        "research_mode": "DISCOVER",
        "source_kind": "historical 846shEE evidence-preserving community composite",
        "inferences_not_verified": ["sticker-to-image-registration", "authored band selection"],
        "readers_tried": list(METHODS),
        "coverage_negative_control": CONTROL,
        "q4_allowed_depths_by_A_to_I": [list(v) for v in choices],
        "per_class_band_measurements": diagnostic,
        "predicted_A_to_I": predictions,
        "null": test,
    }
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(payload, indent=2) + "\n")
        print("Wrote", args.out_json)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 346: preregistered replicated perimeter-feature audit.

Dependencies: numpy, opencv-python-headless, pillow.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFile

from audit_full_photo_perimeter_support import classify, geometry_metrics
from build_background_tile_masters import detect_sticker_quad, warp_sticker

ImageFile.LOAD_TRUNCATED_IMAGES = False

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data" / "perimeter-support-exp344-photos.csv"
SIDES = ("top", "right", "bottom", "left")
BANDS = (
    ("0-2", 0.00, 0.02),
    ("2-4", 0.02, 0.04),
    ("4-8", 0.04, 0.08),
    ("8-16", 0.08, 0.16),
)
PERIMETER_BANDS = {"0-2", "2-4", "4-8"}
CONTROL_BAND = "8-16"
N = 512
PROFILE_N = 256
CORNER_CROP = 0.10
EPS = 1e-6


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    sa = float(a.std())
    sb = float(b.std())
    if sa < EPS or sb < EPS:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def normalize_profile(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=np.float64)
    med = float(np.median(v))
    mad = float(np.median(np.abs(v - med)))
    z = (v - med) / max(mad, EPS)
    x = np.linspace(0.0, 1.0, num=z.size, endpoint=True)
    xi = np.linspace(0.0, 1.0, num=PROFILE_N, endpoint=True)
    return np.interp(xi, x, z)


def extract_profile(gray: np.ndarray, side: str, a: float, b: float) -> np.ndarray:
    n = gray.shape[0]
    lo = int(round(a * n))
    hi = max(lo + 1, int(round(b * n)))
    long_lo = int(round(CORNER_CROP * n))
    long_hi = int(round((1.0 - CORNER_CROP) * n))
    if side == "top":
        v = gray[lo:hi, long_lo:long_hi].mean(axis=0)
    elif side == "bottom":
        v = gray[n-hi:n-lo, long_lo:long_hi].mean(axis=0)
    elif side == "left":
        v = gray[long_lo:long_hi, lo:hi].mean(axis=1)
    elif side == "right":
        v = gray[long_lo:long_hi, n-hi:n-lo].mean(axis=1)
    else:
        raise ValueError(side)
    return normalize_profile(v)


def load_frozen() -> list[dict[str, str]]:
    with FROZEN.open(newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["status"] == "usable"]
    assert len(rows) == 35, len(rows)
    return rows


def class_side_band_medians(records, profiles, excluded_serial=None, excluded_side=None):
    by_class = defaultdict(lambda: defaultdict(list))
    for tile in "ABCDEFGHI":
        photo_rows = [r for r in records if r["tile"] == tile and int(r["serial"]) != excluded_serial]
        for side in SIDES:
            if side == excluded_side:
                continue
            for band, _, _ in BANDS:
                vals = []
                for a, b in itertools.combinations(photo_rows, 2):
                    vals.append(pearson(profiles[(int(a["serial"]), side, band)], profiles[(int(b["serial"]), side, band)]))
                if vals:
                    by_class[tile][(side, band)] = vals
    medians = {}
    for tile in "ABCDEFGHI":
        d = by_class[tile]
        if not d:
            continue
        cell_medians = {k: float(np.median(v)) for k, v in d.items()}
        perim = [v for (side, band), v in cell_medians.items() if band in PERIMETER_BANDS]
        control = [v for (side, band), v in cell_medians.items() if band == CONTROL_BAND]
        if perim and control:
            medians[tile] = {
                "perimeter": float(np.median(perim)),
                "control": float(np.median(control)),
                "side_band_medians": {f"{s}:{b}": v for (s, b), v in sorted(cell_medians.items())},
            }
    return medians


def experiment_stat(class_scores):
    vals = [v["perimeter"] for v in class_scores.values()]
    return float(np.median(vals)) if vals else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, required=True)
    ap.add_argument("--pairs-csv", type=Path, required=True)
    args = ap.parse_args()

    records = load_frozen()
    profiles = {}
    methods = {}
    for row in records:
        serial = int(row["serial"])
        path = ROOT / row["path"]
        with Image.open(path) as src:
            rgb = np.asarray(src.convert("RGB"))
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        h, w = bgr.shape[:2]
        quad, method = detect_sticker_quad(bgr)
        if quad is None:
            raise RuntimeError(f"corpus drift: no quad for {serial}")
        usable, status = classify(geometry_metrics(quad, w, h))
        if not usable or status != "usable":
            raise RuntimeError(f"corpus drift: serial {serial} now {status}")
        methods[serial] = method
        sticker = warp_sticker(bgr, quad, size=N)
        gray = cv2.cvtColor(sticker, cv2.COLOR_BGR2GRAY).astype(np.float64)
        for side in SIDES:
            for band, a, b in BANDS:
                profiles[(serial, side, band)] = extract_profile(gray, side, a, b)

    pair_rows = []
    within = []
    shifted = []
    between = []
    for side in SIDES:
        for band, _, _ in BANDS:
            for a, b in itertools.combinations(records, 2):
                sa, sb = int(a["serial"]), int(b["serial"])
                pa, pb = profiles[(sa, side, band)], profiles[(sb, side, band)]
                corr = pearson(pa, pb)
                relation = "within" if a["tile"] == b["tile"] else "between"
                row = {
                    "serial_a": sa,
                    "serial_b": sb,
                    "tile_a": a["tile"],
                    "tile_b": b["tile"],
                    "side": side,
                    "band": band,
                    "relation": relation,
                    "correlation": corr,
                    "shifted_correlation": "",
                }
                if relation == "within":
                    sc = pearson(pa, np.roll(pb, 32))
                    row["shifted_correlation"] = sc
                    within.append((band, corr))
                    shifted.append((band, sc))
                else:
                    between.append((band, corr))
                pair_rows.append(row)

    class_scores = class_side_band_medians(records, profiles)
    primary = experiment_stat(class_scores)

    positive_classes = sum(v["perimeter"] > 0 for v in class_scores.values())
    perimeter_gt_control = sum(v["perimeter"] > v["control"] for v in class_scores.values())

    within_perim = [v for band, v in within if band in PERIMETER_BANDS]
    shifted_perim = [v for band, v in shifted if band in PERIMETER_BANDS]
    between_perim = [v for band, v in between if band in PERIMETER_BANDS]
    within_median = float(np.median(within_perim))
    shifted_median = float(np.median(shifted_perim))
    between_median = float(np.median(between_perim))

    side_jackknife = {}
    for side in SIDES:
        sc = class_side_band_medians(records, profiles, excluded_side=side)
        side_jackknife[side] = experiment_stat(sc)

    photo_jackknife = {}
    for row in records:
        serial = int(row["serial"])
        sc = class_side_band_medians(records, profiles, excluded_serial=serial)
        photo_jackknife[str(serial)] = experiment_stat(sc)

    gates = {
        "positive_in_at_least_7_classes": positive_classes >= 7,
        "perimeter_gt_control_in_at_least_7_classes": perimeter_gt_control >= 7,
        "within_perimeter_median_gt_between_class_null": within_median > between_median,
        "positive_after_every_side_jackknife": all(v is not None and v > 0 for v in side_jackknife.values()),
        "positive_after_every_photo_jackknife": all(v is not None and v > 0 for v in photo_jackknife.values()),
    }
    passed = all(gates.values())

    summary = {
        "experiment": 346,
        "corpus": {"usable_photos": len(records), "serials": [int(r["serial"]) for r in records]},
        "rectification_methods": {str(k): v for k, v in sorted(methods.items())},
        "frozen_parameters": {
            "rectified_size": N,
            "profile_bins": PROFILE_N,
            "corner_crop_fraction_each_end": CORNER_CROP,
            "bands": [{"name": name, "from": a, "to": b} for name, a, b in BANDS],
            "registration_null_shift_bins": 32,
        },
        "class_scores": class_scores,
        "primary_experiment_statistic": primary,
        "positive_class_count": positive_classes,
        "perimeter_gt_control_class_count": perimeter_gt_control,
        "pooled_medians": {
            "within_class_perimeter": within_median,
            "within_class_perimeter_shifted_32": shifted_median,
            "between_class_perimeter": between_median,
        },
        "side_jackknife_primary": side_jackknife,
        "photo_jackknife_primary": photo_jackknife,
        "gates": gates,
        "candidate_perimeter_signal": passed,
        "interpretation": (
            "positive result licenses localization/characterization only"
            if passed
            else "negative result closes this preregistered grayscale edge-profile channel"
        ),
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    args.pairs_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.pairs_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(pair_rows[0]))
        writer.writeheader()
        writer.writerows(pair_rows)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

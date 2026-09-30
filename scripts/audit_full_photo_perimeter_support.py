#!/usr/bin/env python3
"""Experiment 344 exploratory: full-photo physical-perimeter support audit.

This does NOT search for edge symbols.

It asks whether manifest-authorized original photographs preserve enough of the
physical sticker quadrilateral to support a later preregistered margin/check-bit
analysis. The test deliberately returns "unusable" on uncertain geometry.

Dependencies: numpy, opencv-python-headless, pillow.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFile, UnidentifiedImageError

from build_background_tile_masters import detect_sticker_quad, tile_for_serial

ImageFile.LOAD_TRUNCATED_IMAGES = False

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "archive" / "stickers" / "manifest.csv"
TILES = "ABCDEFGHI"


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return [
            row
            for row in csv.DictReader(fh)
            if row.get("canonical_input", "").lower() == "yes"
            and row.get("category") == "community-original"
        ]


def geometry_metrics(quad: np.ndarray, w: int, h: int) -> dict[str, float | bool]:
    q = np.asarray(quad, dtype=np.float64).reshape(4, 2)
    sides = [
        float(np.linalg.norm(q[(i + 1) % 4] - q[i]))
        for i in range(4)
    ]
    min_side = min(sides)
    max_side = max(sides)
    area = float(abs(cv2.contourArea(q.astype(np.float32))))
    scale = float(min(w, h))

    clearances = []
    for x, y in q:
        clearances.append(min(x, y, (w - 1) - x, (h - 1) - y))
    min_clearance = float(min(clearances))

    return {
        "area_fraction": area / float(w * h),
        "side_ratio": max_side / max(min_side, 1e-9),
        "min_corner_clearance_fraction": min_clearance / max(scale, 1.0),
        "min_side_pixels": min_side,
        "not_source_clipped": min_clearance >= 0.005 * scale,
        "sufficient_edge_resolution": min_side >= 160,
    }


def classify(metrics: dict[str, float | bool]) -> tuple[bool, str]:
    if not metrics["not_source_clipped"]:
        return False, "source-border-risk"
    if not metrics["sufficient_edge_resolution"]:
        return False, "edge-resolution-low"
    if metrics["side_ratio"] > 1.35:
        return False, "quadrilateral-aspect-risk"
    if not (0.12 <= metrics["area_fraction"] <= 0.98):
        return False, "quadrilateral-area-risk"
    return True, "usable"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--csv", type=Path)
    args = ap.parse_args()

    records = []
    for row in load_manifest():
        serial = int(row["serial"])
        tile = row["tile"]
        path = ROOT / row["path"]
        assert tile == tile_for_serial(serial)

        rec = {
            "serial": serial,
            "tile": tile,
            "path": row["path"],
            "status": "",
            "rectification": "",
            "area_fraction": "",
            "side_ratio": "",
            "min_corner_clearance_fraction": "",
            "min_side_pixels": "",
        }

        try:
            with Image.open(path) as probe:
                probe.verify()
            with Image.open(path) as src:
                rgb = np.asarray(src.convert("RGB"))
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
            rec["status"] = f"decode-reject:{type(exc).__name__}"
            records.append(rec)
            continue

        img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        h, w = img.shape[:2]
        quad, method = detect_sticker_quad(img)
        rec["rectification"] = method
        if quad is None:
            rec["status"] = "no-confident-quadrilateral"
            records.append(rec)
            continue

        metrics = geometry_metrics(quad, w, h)
        usable, status = classify(metrics)
        rec["status"] = status
        for key in (
            "area_fraction",
            "side_ratio",
            "min_corner_clearance_fraction",
            "min_side_pixels",
        ):
            rec[key] = round(float(metrics[key]), 6)
        records.append(rec)

    assert len(records) == 82, len(records)

    by_tile = defaultdict(list)
    for rec in records:
        by_tile[rec["tile"]].append(rec)

    tile_summary = {}
    for tile in TILES:
        rows = by_tile[tile]
        usable = [r for r in rows if r["status"] == "usable"]
        tile_summary[tile] = {
            "original_photos": len(rows),
            "usable_full_perimeter_photos": len(usable),
            "replicated_perimeter_support": len(usable) >= 2,
            "status_counts": dict(sorted(Counter(r["status"] for r in rows).items())),
        }

    usable_total = sum(r["status"] == "usable" for r in records)
    replicated_tiles = [t for t in TILES if tile_summary[t]["replicated_perimeter_support"]]

    summary = {
        "experiment": 344,
        "purpose": "observability only; no edge-symbol search",
        "manifest_originals": len(records),
        "usable_full_perimeter_photos": usable_total,
        "tiles_with_two_or_more_usable_photos": replicated_tiles,
        "replicated_tile_count": len(replicated_tiles),
        "all_nine_tiles_replicated": len(replicated_tiles) == 9,
        "preregistered_geometry_rules": {
            "minimum_corner_clearance_fraction_of_short_image_axis": 0.005,
            "minimum_detected_side_pixels": 160,
            "maximum_side_ratio": 1.35,
            "accepted_area_fraction": [0.12, 0.98],
        },
        "tiles": tile_summary,
        "interpretation_rule": (
            "A later stable-edge-feature test is justified only for tiles with "
            "at least two independently usable full-perimeter photographs. "
            "Unreplicated tiles remain untestable rather than negative."
        ),
    }

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        fields = list(records[0])
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

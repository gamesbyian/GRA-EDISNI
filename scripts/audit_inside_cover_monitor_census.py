#!/usr/bin/env python3
"""Observation-only colour component census for existing INSIDE cover scans.

Read only prior source-audit A-overview.jpg and B-overview.jpg (both 2200x1692)
from a supplied archival ZIP. The ROI was manually selected from the visible
monitor region, and the thresholds are robustness checks, not discovery tests.

Usage: python scripts/audit_inside_cover_monitor_census.py /path/to/inside-cover-source-audit.zip
Requires: OpenCV (cv2) and numpy. The image task justifies these dependencies.
Does not decode stickers or register source artwork pixel-for-pixel.
"""
from __future__ import annotations

import argparse
import json
import zipfile

import cv2
import numpy as np

REGION = (300, 900, 1550, 1250)  # x0,y0,x1,y1, 2200x1692 image only
# Frozen red thresholds and red:green contrast ratios.
CONDITIONS = [
    (75, 1.3), (75, 1.4), (75, 1.5),
    (90, 1.3), (90, 1.4), (90, 1.5),
    (110, 1.3), (110, 1.4),
]


def measure(image: np.ndarray, threshold: int, ratio: float) -> list[dict]:
    x0, y0, x1, y1 = REGION
    roi = image[y0:y1, x0:x1]
    b, g, r = cv2.split(roi)
    mask = np.uint8((r > threshold) & (r > g * ratio) & (r > b * 1.12)) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    _, _, stats, _ = cv2.connectedComponentsWithStats(mask)
    found = [
        {"x": int(x + x0), "y": int(y + y0),
         "width": int(w), "height": int(h), "orange_area_pixels": int(area)}
        for x, y, w, h, area in stats[1:] if area > 50
    ]
    return sorted(found, key=lambda component: component["x"])


def audit(archive: str) -> dict:
    with zipfile.ZipFile(archive) as source:
        images = {}
        for side in ("A", "B"):
            raw = source.read(f"{side}-overview.jpg")
            images[side] = cv2.imdecode(
                np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            if images[side] is None or images[side].shape[:2] != (1692, 2200):
                raise AssertionError(f"Unexpected {side} dimensions")

    controls = []
    for threshold, ratio in CONDITIONS:
        a = measure(images["A"], threshold, ratio)
        b = measure(images["B"], threshold, ratio)
        assert len(a) == 4 and len(b) == 0, (threshold, ratio, len(a), len(b))
        controls.append({
            "threshold": threshold,
            "red_to_green_ratio": ratio,
            "A_orange_displays": len(a),
            "B_orange_displays": len(b),
        })
    return {
        "source": "Earlier 2200x1692 source-audit scans; NOT full untouched 6552 originals",
        "region_xyxy": REGION,
        "tests_passed": len(controls),
        "threshold_controls": controls,
        "anchors": measure(images["A"], 110, 1.3),
        "limitation": (
            "ROI selected after scene inspection; threshold variation tests "
            "stability, not prospective semantic evidence. Four orange screens "
            "are observed; no sticker mapping, transform, or hidden message."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="source-audit ZIP containing A/B overview images")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    result = json.dumps(audit(args.archive), indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(result)
    print(result, end="")


if __name__ == "__main__":
    main()

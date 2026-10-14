#!/usr/bin/env python3
"""DISCOVER-mode sensitivity of red-mark counts in a watermarked SecretMap repost.

Source: 2018 9game derivative image, not the original 2016 DDS.
No sticker completions, projective registration or source-native coordinates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

EXPECTED = "5cf2c46ac98397bb47a16974317a5ee730c5ce48826f75c481322bd9ac8da3b9"
THRESHOLDS = (12, 16, 20, 24, 28, 32, 36, 40)
AREAS = (2, 4, 8)

def components(mask: bytearray, width: int, height: int) -> list[dict]:
    seen = bytearray(width * height)
    result = []
    for i, bit in enumerate(mask):
        if not bit or seen[i]:
            continue
        seen[i] = 1
        stack, members = [i], []
        while stack:
            at = stack.pop()
            members.append(at)
            y, x = divmod(at, width)
            for ny in range(max(0, y - 1), min(height, y + 2)):
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    j = ny * width + nx
                    if mask[j] and not seen[j]:
                        seen[j] = 1
                        stack.append(j)
        n = len(members)
        result.append({"area": n,
                       "cx": round(sum(j % width for j in members) / n, 2),
                       "cy": round(sum(j // width for j in members) / n, 2)})
    return result

def analyze(path: Path, strict: bool = True) -> dict:
    source = path.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if strict and digest != EXPECTED:
        raise ValueError(f"Wrong source: {digest}")
    with Image.open(path) as im:
        im = im.convert("RGB")
        width, height = im.size
        if strict and (width, height) != (480, 240):
            raise ValueError(f"Wrong dimensions: {(width, height)}")
        data = im.tobytes()
    ch = iter(data)
    pixels = list(zip(ch, ch, ch))
    rows = []
    for threshold in THRESHOLDS:
        mask = bytearray(width * height)
        for i, (r, g, b) in enumerate(pixels):
            # y=165 is an after-inspection crop excluding the orange watermark.
            if i // width < 165 and r > 35 and r - g > threshold and r - b > threshold:
                mask[i] = 1
        clusters = components(mask, width, height)
        rows.append({
            "threshold": threshold,
            "red_pixels": sum(mask),
            "counts": {str(area): sum(c["area"] >= area for c in clusters) for area in AREAS},
            "centroids_area_ge_8": sorted(
                [c for c in clusters if c["area"] >= 8], key=lambda c: (c["cx"], c["cy"]))
        })
    return {
        "source_sha256": digest, "source_size": [width, height],
        "source_type": "low resolution, watermarked 2018 repost, not native DDS",
        "method": "R>35, R-G>t and R-B>t, 8-neighbor components; min areas 2,4,8",
        "cutoff": "y<165, chosen after inspection to exclude orange lower-right watermark",
        "mode": "DISCOVER: retrospectively configured sensitivity screen, not holdout",
        "rows": rows
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("image", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--accept-other-source", action="store_true")
    args = p.parse_args()
    d = analyze(args.image, strict=not args.accept_other_source)
    print("threshold | minimum area 2, 4, 8: component counts")
    for row in d["rows"]:
        print(f'{row["threshold"]:9} | ' +
              ", ".join(str(row["counts"][str(a)]) for a in AREAS))
    if args.out:
        args.out.write_text(json.dumps(d, indent=2) + "\n")

if __name__ == "__main__":
    main()

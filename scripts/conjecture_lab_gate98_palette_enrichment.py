#!/usr/bin/env python3
"""CL-04b: recover possible original gate-98 exact-color marker codebook.

Never choose colors for producing a pre-known text. Candidates arise from
their **independently measurable spatial enrichment** at the published 16px
lattice versus the other 255/256 pixels, not from a sticker output.

Speculative codebook only. A seven-color historical claim is not itself a
source-fixed enumeration of the six other exact RGB triples.
"""
import argparse
from collections import Counter
from hashlib import sha1
from io import BytesIO
import json
from pathlib import Path

from PIL import Image
from conjecture_lab_gate98_real_pixels import (
    load_bytes, SAMPLE_STEP, EXPECTED_DIMENSIONS,
    PIXELS_PER_ROW, PIXELS_PER_COL, EXPECTED_GIT_SHA1
)


def human_color(rgb):
    return "#" + "".join(f"{x:02X}" for x in rgb)


def run(local):
    payload, gitsha = load_bytes(local)
    with Image.open(BytesIO(payload)) as src:
        assert src.size == EXPECTED_DIMENSIONS
        mode = src.mode
        original = src.convert("RGBA")
    assert SAMPLE_STEP == 16

    grid_rgba = [
        tuple(original.getpixel((16*x, 16*y)))
        for y in range(PIXELS_PER_COL) for x in range(PIXELS_PER_ROW)
    ]
    rgb = Counter(x[:3] for x in grid_rgba)
    alpha = Counter(x[3] for x in grid_rgba)
    # Threshold declared without inspecting desirable extracted glyphs:
    # at least 8 repeats on the regular sample grid (twice mean repeat
    # rate for the exact-source 32768 / 19742 full-sample palette).
    candidates = {color for color, n in rgb.items() if n >= 8}
    # Only count an RGBA pixel's RGB in a candidate's total frequency;
    # avoid the memory expense of a full 8.4M-entry RGB histogram.
    total_occurrences = Counter()
    # getdata() iterates the intact image in row-major order.
    for (r, g, b, a) in original.getdata():
        c = (r, g, b)
        if c in candidates:
            total_occurrences[c] += 1

    entries = []
    for color in candidates:
        sampled = rgb[color]
        full = total_occurrences[color]
        offgrid = full - sampled
        assert offgrid >= 0
        cells = [divmod(i, PIXELS_PER_ROW)[::-1]
                 for i, c in enumerate(grid_rgba)
                 if c[:3] == color]
        xs = [x for x, y in cells]
        ys = [y for x, y in cells]
        # enrichment = (grid occurrences per grid site) /
        #              (offgrid occurrences per offgrid site).
        ratio = (
            (sampled / (PIXELS_PER_ROW*PIXELS_PER_COL)) /
            (offgrid / (EXPECTED_DIMENSIONS[0]*EXPECTED_DIMENSIONS[1]
                        - PIXELS_PER_ROW*PIXELS_PER_COL))
            if offgrid else None
        )
        entries.append({
            "rgb": list(color),
            "hex": human_color(color),
            "sampled_grid_hits": sampled,
            "off_grid_hits": offgrid,
            "whole_image_hits": full,
            "enrichment_over_off_grid": round(ratio, 4) if ratio is not None else None,
            "only_on_grid": offgrid == 0,
            "sampled_grid_bbox_xyxy": [min(xs), min(ys), max(xs), max(ys)],
            "top_left_sampled_count_y0_63": sum(y < 64 for x, y in cells),
            "alpha_values_at_sampled_color": {
                str(k): v for k,v in Counter(
                    c[3] for c in grid_rgba if c[:3]==color
                ).most_common(6)
            },
        })

    assert len(grid_rgba) == 32768
    sample_grid_rgba_colors = len(set(grid_rgba))
    ordered = sorted(entries, key=lambda z: (
        -z["sampled_grid_hits"], z["hex"]))
    enriched = sorted(entries, key=lambda z: (
        -(z["enrichment_over_off_grid"] if z["enrichment_over_off_grid"] is not None else 1e20),
        -z["sampled_grid_hits"],
        z["hex"]))
    result = {
        "status": "CL04b source-color enrichment, candidate markers NOT an authorial decoder",
        "source_sha1": gitsha,
        "source_mode": mode,
        "sample_lattice_origin": [0,0],
        "sample_lattice_stride":16,
        "source_dimensions": list(EXPECTED_DIMENSIONS),
        "sampled_grid_size": [PIXELS_PER_ROW, PIXELS_PER_COL],
        "sampled_rgb_unique": len(rgb),
        "sampled_rgba_unique": sample_grid_rgba_colors,
        "sampled_alpha_top_20": [{"alpha":k,"n":v} for k,v in alpha.most_common(20)],
        "candidate_threshold_sampled_hits":8,
        "candidate_color_count":len(candidates),
        "candidate_colors_exclusive_to_grid":sum(x["only_on_grid"] for x in entries),
        "candidate_colors_sorted_by_grid_hits":ordered,
        "top_30_enriched_colors":enriched[:30],
        "black_on_grid":rgb[(0,0,0)],
        "expected_random_grid_fraction":1/256,
        "limitations":[
          "The historical seven source-selected RGB triples are not completely documented by this experiment.",
          "Enrichment and its threshold were chosen to discover potential marker palettes, not to test a precommitted solved message.",
          "No color with an aesthetically pleasing downstream output may be promoted without verifying the original hidden path from source coordinates first.",
          "This source predates the CE stickers; foreground-to-source registration remains invented.",
          "Alpha may be transparent on an RGBA PNG; the exact source-byte/mode report preserves that distinction.",
        ],
    }
    assert gitsha == EXPECTED_GIT_SHA1
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source")
    p.add_argument("--output")
    args=p.parse_args()
    x=run(args.source)
    if args.output:
        Path(args.output).write_text(json.dumps(x,indent=2)+"\n",encoding="utf8")
    print(json.dumps({
        "source_gitsha":x["source_sha1"],
        "source_mode":x["source_mode"],
        "sampled_alpha_top":x["sampled_alpha_top_20"][:8],
        "colors_sampled_at_least_eight":x["candidate_color_count"],
        "exclusive_to_lattice":x["candidate_colors_exclusive_to_grid"],
        "top_12_enriched":x["top_30_enriched_colors"][:12],
        "top_12_repeated":x["candidate_colors_sorted_by_grid_hits"][:12],
    }, indent=2))

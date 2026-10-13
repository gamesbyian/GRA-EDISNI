#!/usr/bin/env python3
"""Source-native nine-position image registration preflight for the 534brn page.

Uses only original captured page/XMP bytes and the already verified JPEG
dimension/MCU-domain fixture. No lost JPEG byte, pixel, or CE sticker is filled.
DISCOVER/DEVELOP with narrow source-forensic assertions, not a decoded receiver.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B_PATH = ROOT / "archive/external/terminal41-534brn/B-original-capture.bin"
XMP_PATH = ROOT / "archive/external/terminal41-534brn/X-xmp-fragment.bin"
MCU_PATH = ROOT / "data/experiment-423-534brn-mcu-constraint.json"
B_BLOB = "f12c02c49f4c3f7589419fe8e20d655f7b95a9f4"
XMP_BLOB = "b6f5ffed946d9d19dfd0a5d90a8b18759a90c496"
CHECK = {
    "dimension_pairs": 16384,
    "dimension_values_per_axis": 128,
    "equal_pixel_thirds_pairs": 1849,
    "equal_mcu_thirds_pairs": 2304,
    "both_pixel_and_mcu_aligned_pairs": 9,
    "equal_pixel_thirds_axis_values": 43,
    "equal_mcu_thirds_axis_values": 48,
    "both_aligned_axis_values": [144, 192, 240],
    "distinct_mcu_products": 43,
    "at_128": {
        "axis_pixels": 128, "axis_mcus": 8,
        "pixel_third_centres": [21, 64, 106],
        "mcu_third_centres": [24, 72, 104],
        "equal_pixel_thirds": False, "equal_mcu_thirds": False,
    },
}


def git_blob_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def assert_origin(path: Path, expected_sha: str) -> bytes:
    data = path.read_bytes()
    actual = git_blob_hash(data)
    if actual != expected_sha:
        raise ValueError(f"Source provenance failure: {path}: {actual} != {expected_sha}")
    return data


def stable_source_evidence(page: bytes, xmp: bytes) -> dict:
    """Scan only intact, source-delimited spans; no JPEG-entropy tag search."""
    if page.count(b"JFIF") != 1 or page.count(b"pe^!02un") != 1:
        raise ValueError("Page did not preserve single JFIF and 128-footer anchors")
    preamble = page[:page.index(b"JFIF")]
    if not preamble.startswith(b"<!DOCTYPE html>") or not re.search(
        rb"<pre>\[\]\s*</pre>", preamble
    ):
        raise ValueError("Unexpected previously authenticated HTML wrapper")
    if not re.search(rb"<title>\s*/emergency terminal link \[41\]/\s*</title>", preamble):
        raise ValueError("Unexpected Terminal41 title")
    control_tags = [tag.decode("ascii") for tag in
                    (b"<input", b"<canvas", b"<form", b"<img", b"<svg", b"<script")
                    if tag in preamble.lower()]
    if control_tags:
        raise ValueError(f"New interactive element in intact preamble: {control_tags!r}")
    footer = page.split(b"pe^!02un", 1)[1]
    if not re.match(rb"\s*\.{8}\r?\n\.{2}\r?\n\.\r?\n", footer):
        raise ValueError("Upside-down 128 UNSOLVED dot-run structure changed")
    if not re.search(rb"sys/\r?\nterminate terminal/\r?\n41/\r?\n\[conf\.\]", footer):
        raise ValueError("Expected suffix path and [conf.] absent")
    dates = re.findall(rb"<xmp:CreateDate>(.*?)</xmp:CreateDate>", xmp)
    creators = re.findall(rb"<rdf:li>(.*?)</rdf:li>", xmp)
    if dates != [b"2016-12-16T14:12:24.351"] or creators != [b"AnSet"]:
        raise ValueError("Source XMP annotation has changed")
    return {
        "page_git_blob_sha": B_BLOB,
        "xmp_git_blob_sha": XMP_BLOB,
        "html_preamble_has_native_input_canvas_image_or_script": False,
        "preamble_visible_marker": "[]",
        "footer_dot_run_lengths": [8, 2, 1],
        "footer_system_route": "sys/terminate terminal/41/[conf.]",
        "xmp_creator": "AnSet",
        "xmp_created": "2016-12-16T14:12:24.351",
        "scope": "Only the intact HTML preamble, visible footer and preserved XMP; "
                 "not a proof of absent design in corrupt JPEG bytes.",
    }


def axis_options(low: int, high: int) -> dict:
    values = range(low, high + 1)
    px = [d for d in values if d % 3 == 0]
    mcus = [d for d in values if math.ceil(d / 16) % 3 == 0]
    aligned = [d for d in values if d % 48 == 0]
    assert set(px).intersection(mcus) == set(aligned)
    return {"values": len(values),
            "pixel_equal": px,
            "mcu_equal": mcus,
            "pixel_and_mcu_equal": aligned}


def pixel_centre_triplet(d: int) -> list[int]:
    """One explicit source-footprint-only *candidate*, not a source-authored rule."""
    return [((2 * j + 1) * d) // 6 for j in range(3)]


def mcu_centre_triplet(d: int) -> list[int]:
    """Different, equally plausible candidate: centres of 3 logical MCU bands."""
    count = math.ceil(d / 16)
    return [min(d - 1, 16 * (((2 * j + 1) * count) // 6) + 8)
            for j in range(3)]


def build_report(page: bytes, xmp: bytes, fixture: dict) -> dict:
    md = fixture["independent_dimension_domain"]
    if md["pixel_width"] != [128, 255] or md["pixel_height"] != [128, 255]:
        raise ValueError("Original-source dimension domain drift")
    if fixture["decoder_model"]["scan_components"] != "Y 2x2 + Cb 1x1 + Cr 1x1 => 6 blocks/MCU":
        raise ValueError("JPEG native sampling contract changed")
    if not md["all_possible_products_survive"]:
        raise ValueError("MCU feasibility domain has narrowed")
    possible_products = {math.ceil(x / 16) * math.ceil(y / 16)
                         for x in range(128, 256) for y in range(128, 256)}
    if possible_products != set(fixture["independent_dimension_domain"]["possible_mcu_products"]):
        raise ValueError("Derived MCU products disagree with source-bound verifier")
    axis = axis_options(128, 255)
    if len(axis["pixel_and_mcu_equal"]) != 3:
        raise ValueError("Unexpected native grid dimensions")
    p128 = pixel_centre_triplet(128)
    m128 = mcu_centre_triplet(128)
    if p128 == m128:
        raise ValueError("Supposed distinct native sampling models collapsed")
    return {
        "mode": "DISCOVER/DEVELOP, source-static geometry preflight",
        "carrier": stable_source_evidence(page, xmp),
        "dimension_values_per_axis": axis["values"],
        "dimension_pairs": axis["values"] ** 2,
        "possible_mcu_axis_counts": list(range(8, 17)),
        "distinct_mcu_products": len(possible_products),
        "all_43_native_mcu_totals_survive_known_entropy": True,
        "equal_pixel_thirds_axis_values": len(axis["pixel_equal"]),
        "equal_pixel_thirds_pairs": len(axis["pixel_equal"]) ** 2,
        "equal_mcu_thirds_axis_values": len(axis["mcu_equal"]),
        "equal_mcu_thirds_pairs": len(axis["mcu_equal"]) ** 2,
        "both_aligned_axis_values": axis["pixel_and_mcu_equal"],
        "both_pixel_and_mcu_aligned_pairs": len(axis["pixel_and_mcu_equal"]) ** 2,
        "at_128": {
            "axis_pixels": 128, "axis_mcus": 8,
            "pixel_third_centres": p128,
            "mcu_third_centres": m128,
            "equal_pixel_thirds": 128 % 3 == 0,
            "equal_mcu_thirds": 8 % 3 == 0,
        },
        "jpeg_component_native_blocks_per_mcu": [4, 1, 1],
        "jpeg_component_note": "The intact header supports luma/chroma sampling 4:2:0. "
                               "It does not supply an equal-footprint native R/G/B 3x3 array.",
        "nine_position_consumer_found": False,
        "result_scope": "No *source-fixed* nine-slot RGB sampling rule identified in the "
                        "preserved HTML/XMP and verified JPEG structure. Pixel-level "
                        "nine-grid readings remain untestable without a decoded source.",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check-frozen", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = build_report(assert_origin(B_PATH, B_BLOB), assert_origin(XMP_PATH, XMP_BLOB),
                          json.loads(MCU_PATH.read_text(encoding="utf-8")))
    if args.check_frozen:
        for k, expected in CHECK.items():
            if result[k] != expected:
                raise AssertionError(f"{k} changed: {result[k]!r}, expected {expected!r}")
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()

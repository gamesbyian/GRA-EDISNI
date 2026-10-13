#!/usr/bin/env python3
"""Offline barcode payload/GS1 forensic intake, with optional ZXing-C++ image scan.

No claim a barcode is an ARG cipher. Never guess a symbology from numeric text.

Examples:
 python scripts/inspect_arg_barcodes.py --payload '4006381333931' --format EAN-13
 python scripts/inspect_arg_barcodes.py --payload ']C1010400638133393121A37' --format GS1-128
 python scripts/inspect_arg_barcodes.py --image /path/to/original-photo.png

Install zxing-cpp and Pillow *only* for --image; validation requires stdlib alone.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

GS = "\x1d"  # Scanner-decoded GS1 FNC1/group separator
FIXED_AI = {"00": 18, "01": 14, "02": 14, "11": 6, "13": 6, "15": 6, "17": 6}
VARIABLE_AI = {"10": 20, "21": 20, "37": 8}
AI_NAMES = {"00": "SSCC", "01": "GTIN", "02": "CONTAINED_GTIN", "10": "BATCH_LOT",
            "11": "PRODUCTION_DATE", "13": "PACKAGING_DATE", "15": "BEST_BEFORE",
            "17": "EXPIRATION", "21": "SERIAL", "37": "COUNT"}


def gtin_check_digit(body: str) -> str:
    if not body.isascii() or not body.isdigit():
        raise ValueError("GTIN digits must be ASCII 0-9")
    return str((-sum(int(ch) * (3 if i % 2 == 0 else 1)
                     for i, ch in enumerate(reversed(body)))) % 10)


def verify_gtin(value: str) -> dict:
    if not value.isascii() or not value.isdigit() or len(value) not in (8, 12, 13, 14):
        return {"input": value, "status": "invalid_format", "expected_lengths": [8, 12, 13, 14]}
    expected = gtin_check_digit(value[:-1])
    return {"input": value, "status": "valid_check_digit" if expected == value[-1] else "invalid_check_digit",
            "expected_check_digit": expected, "provided_check_digit": value[-1],
            "note": "Check-digit validity does not establish registration, manufacturer, or ARG intent."}


def parse_gs1_ai(text: str) -> dict:
    """Conservative GS1 subset parser for *already confirmed* GS1 content.

    FNC1 is represented by a leading ]C1 symbology identifier and internal GS.
    Parentheses in human-readable print are not barcode bytes; this function
    deliberately does not parse them, avoiding fictitious symbol structure.
    """
    if text.startswith("]C1"):
        text = text[3:]
    result = []
    while text:
        if text[0] == GS:
            return {"status": "malformed", "fields": result, "remaining": repr(text),
                    "reason": "Unexpected group separator at field boundary"}
        ai = text[:2]
        if ai not in FIXED_AI and ai not in VARIABLE_AI:
            return {"status": "unsupported_ai", "fields": result,
                    "remaining": text.encode("unicode_escape").decode("ascii")}
        data = text[2:]
        if ai in FIXED_AI:
            width = FIXED_AI[ai]
            if len(data) < width or not data[:width].isascii() or not data[:width].isdigit():
                return {"status": "malformed", "fields": result, "remaining": text,
                        "reason": f"AI {ai} expects {width} ASCII digits"}
            value, text = data[:width], data[width:]
        else:
            end = data.find(GS)
            value = data if end < 0 else data[:end]
            text = "" if end < 0 else data[end + 1:]
            if not 1 <= len(value) <= VARIABLE_AI[ai]:
                return {"status": "malformed", "fields": result,
                        "reason": f"AI {ai} data length outside 1..{VARIABLE_AI[ai]}"}
            if ai == "37" and (not value.isascii() or not value.isdigit()):
                return {"status": "malformed", "fields": result, "reason": "AI 37 must be numeric"}
        field = {"ai": ai, "name": AI_NAMES[ai], "value": value}
        if ai in ("01", "02"):
            field["gtin_validation"] = verify_gtin(value)
        result.append(field)
    return {"status": "parsed_supported_subsets_only", "fields": result}


def inspect(payload: str, symbology: str | None = None) -> dict:
    out = {"raw_codepoints": len(payload), "payload_escaped": payload.encode("unicode_escape").decode("ascii"),
           "raw_utf8_hex": payload.encode("utf-8").hex(),
           "declared_format": symbology, "gtin": None, "gs1": None,
           "warnings": []}
    norm = (symbology or "").upper().replace("_", "-")
    if payload.startswith("]C1"):
        if norm and norm not in ("GS1-128", "CODE-128", "CODE128"):
            out["warnings"].append("Declared format conflicts with scanner's ]C1 GS1-128 identifier")
        out["gs1"] = parse_gs1_ai(payload)
    elif norm == "GS1-128":
        out["warnings"].append("GS1-128 declared; leading FNC1 must be verified from source or scanner metadata")
        out["gs1"] = parse_gs1_ai(payload)
    elif norm in ("EAN-8", "EAN-13", "UPC-A", "ITF-14"):
        if len(payload) != {"EAN-8": 8, "EAN-13": 13, "UPC-A": 12, "ITF-14": 14}[norm]:
            out["warnings"].append("Declared symbology and digit length disagree")
        out["gtin"] = verify_gtin(payload)
    else:
        out["warnings"].append("No verified GS1 symbology: arbitrary text/number is not a GTIN or GS1 AI stream")
    return out


def normalise_scanner_format(name: str) -> str:
    """Handle ZXing enum labels across current/recent Python binding releases."""
    token = name.rsplit(".", 1)[-1].upper().replace("_", "").replace("-", "")
    return {"EAN8": "EAN-8", "EAN13": "EAN-13", "UPCA": "UPC-A",
            "ITF14": "ITF-14", "CODE128": "CODE-128"}.get(token, name)


def scan_image(path: pathlib.Path) -> list[dict]:
    try:
        import zxingcpp  # type: ignore
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("For --image install optional zxing-cpp and Pillow; payload-only needs no dependencies") from exc
    results = []
    with Image.open(path) as img:
        for found in zxingcpp.read_barcodes(img.convert("RGB")):
            fmt = normalise_scanner_format(str(found.format))
            text = found.text
            scanner_id = getattr(found, "symbology_identifier", None)
            raw = bytes(found.bytes) if hasattr(found, "bytes") else None
            # ]C1 is an AIM scanner symbology identifier for GS1-128. ZXing
            # commonly returns it as metadata rather than embedded payload.
            recognized = (f"]C1{text}" if scanner_id == "]C1" and not text.startswith("]C1")
                          else text)
            result = {"format": fmt, "scanner_symbology_identifier": scanner_id,
                      "decoder": "zxing-cpp", "decoded": inspect(recognized, fmt),
                      "decoder_raw_bytes_hex": raw.hex() if raw is not None else None,
                      "source_filename": path.name,
                      "warning": "Not independently verified with another decoder or against printed human-readable value."}
            results.append(result)
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sources = p.add_mutually_exclusive_group(required=True)
    sources.add_argument("--payload", help="Literal scanner-decoded text; use shell quoting for control chars")
    sources.add_argument("--image", type=pathlib.Path, help="Original local barcode image; optional zxing-cpp")
    p.add_argument("--format", help="Format independently observed, e.g. EAN-13, UPC-A, CODE-128, GS1-128")
    p.add_argument("--source-url", help="Public provenance URL, not proof of scan accuracy")
    args = p.parse_args()
    data = scan_image(args.image) if args.image else [inspect(args.payload, args.format)]
    print(json.dumps({"source_url": args.source_url, "results": data}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
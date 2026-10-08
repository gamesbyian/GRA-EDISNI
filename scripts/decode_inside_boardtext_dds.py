#!/usr/bin/env python3
"""Read the alpha plane of archived INSIDE BoardText DDS (BC3/DXT5).

The original 2016 asset is preserved upstream as:
gamesbyian/playdead-unofficial-exports/assets/BoardText_13309-b0922098d7c08dbe.dds
Git blob SHA d8e19793cb3b09764728fb2fc3cf4aaa4e1d32e8.

Usage:
 python scripts/decode_inside_boardtext_dds.py /path/to/BoardText.dds output.pgm
 python scripts/decode_inside_boardtext_dds.py --self-test

Produces a standard binary PGM (P5), no sticker-decoding operations.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

SOURCE_SHA = "d8e19793cb3b09764728fb2fc3cf4aaa4e1d32e8"


def get32(blob: bytes, offset: int) -> int:
    return struct.unpack_from("<I", blob, offset)[0]


def source_descriptor(blob: bytes) -> dict:
    assert blob[:4] == b"DDS " and get32(blob, 4) == 124
    assert get32(blob, 76) == 32 and blob[84:88] == b"DXT5"
    width, height, mips = get32(blob, 16), get32(blob, 12), get32(blob, 28)
    assert (width, height, mips, len(blob)) == (256, 32, 8, 11152)
    sha = hashlib.sha1(b"blob " + str(len(blob)).encode("ascii") + b"\0" + blob).hexdigest()
    assert sha == SOURCE_SHA, sha
    levels = []
    cursor = 128
    for i in range(9):  # base + 8 additional levels, exactly all available bytes
        w, h = max(1, width >> i), max(1, height >> i)
        n = ((w + 3) // 4) * ((h + 3) // 4) * 16
        levels.append(dict(level=i, width=w, height=h, start=cursor, bytes=n))
        cursor += n
    assert cursor == len(blob), (cursor, len(blob))
    return dict(width=width, height=height, mip_count_field=mips,
                total_levels=len(levels), levels=levels, git_blob_sha=sha)


def decode_alpha(block: bytes) -> list[int]:
    assert len(block) == 16
    a0, a1 = block[0], block[1]
    values = [a0, a1]
    if a0 > a1:
        values += [round(((7 - k) * a0 + k * a1) / 7) for k in range(1, 7)]
    else:
        values += [round(((5 - k) * a0 + k * a1) / 5) for k in range(1, 5)]
        values += [0, 255]
    word = int.from_bytes(block[2:8], "little")
    return [values[(word >> (3 * i)) & 7] for i in range(16)]


def decode_base_alpha(blob: bytes) -> tuple[int, int, bytes]:
    desc = source_descriptor(blob)
    width, height = desc["width"], desc["height"]
    pixels = bytearray(width * height)
    for by in range(height // 4):
        for bx in range(width // 4):
            base = 128 + 16 * (by * (width // 4) + bx)
            alpha = decode_alpha(blob[base:base + 16])
            for iy in range(4):
                for ix in range(4):
                    pixels[(by * 4 + iy) * width + bx * 4 + ix] = alpha[iy * 4 + ix]
    assert sum(bool(x) for x in pixels) == 2061
    return width, height, bytes(pixels)


def self_test() -> None:
    block = bytes([255, 0, 0, 0, 0, 0, 0, 0] + [0] * 8)
    assert decode_alpha(block) == [255] * 16
    block = bytes([0, 255, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff] + [0] * 8)
    assert decode_alpha(block) == [255] * 16
    print("PASS: synthetic DXT5 alpha interpolation checks")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path, nargs="?")
    p.add_argument("output", type=Path, nargs="?")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
        return
    if not a.source or not a.output:
        p.error("source DDS and output PGM are required without --self-test")
    source = a.source.read_bytes()
    w, h, pixels = decode_base_alpha(source)
    a.output.write_bytes(f"P5\n{w} {h}\n255\n".encode("ascii") + pixels)
    print(json.dumps({"dds": str(a.source), "pgm": str(a.output),
                      "pixel_dimensions": [w, h], "alpha_nonzero": 2061,
                      "source": source_descriptor(source)}, indent=2))


if __name__ == "__main__":
    main()

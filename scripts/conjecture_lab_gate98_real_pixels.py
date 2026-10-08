#!/usr/bin/env python3
"""CL-04: one completely specified, deliberately speculative real-image reader.

Recover an upstream archived Terminal41 gate-98 PNG by exact Git blob SHA,
replay the HISTORICALLY ATTESTED 16-pixel sampling lattice, and apply the
INVENTED 512-address x three-colour-channel Q4 candidate.

This is research instrumentation, NOT evidence that gate-98 consumes CE
stickers. Never report the best of 64 banks as a blind decode.
Requires Pillow and network only if --source is omitted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha1, sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
from urllib.request import Request, urlopen

from generate_master import legal_states, generate_master, SERIAL_ORDER
from enumerate_sticker_completion_ensembles import observations

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow required for historical source image inspection") from exc

UPSTREAM_PATH = (
    "terminal41.link/comms/gate/98/"
    "transmission_id41786174541g1f561f4186454544fdrfd532430980980000000000000000k.png"
)
UPSTREAM_RAW = (
    "https://raw.githubusercontent.com/twinysam/INSIDE-ARG/master/" + UPSTREAM_PATH
)
EXPECTED_SIZE = 19360240
EXPECTED_GIT_SHA1 = "127d8772912ffc499e5afaffe321d5bab7e920df"
EXPECTED_DIMENSIONS = (2048, 4096)
SAMPLE_STEP = 16
PIXELS_PER_ROW = EXPECTED_DIMENSIONS[0] // SAMPLE_STEP  # 128
PIXELS_PER_COL = EXPECTED_DIMENSIONS[1] // SAMPLE_STEP  # 256
BANK_SIZE = 512
BANKS = PIXELS_PER_ROW * PIXELS_PER_COL // BANK_SIZE


def class_addresses(master: str):
    """9-bit forward slash=1 in original A..I class order."""
    result = []
    for j in range(9):
        word = [master[9*f+j] for f in range(9)]
        assert set(word) <= {"/", "-"}
        result.append(sum((mark == "/") << (8-k) for k, mark in enumerate(word)))
    return result


def q4_depths(master: str):
    result = []
    for j in range(9):
        marks = [master[81+9*d+j] for d in range(3)]
        assert sorted(marks) == [".", ".", "/"]
        result.append(marks.index("/"))
    return result


def load_bytes(src: str | None):
    if src:
        payload = Path(src).read_bytes()
    else:
        req = Request(UPSTREAM_RAW, headers={"User-Agent": "GRA-EDISNI-conjecture-research/1"})
        with urlopen(req, timeout=45) as resp:
            payload = resp.read(EXPECTED_SIZE+1)
    assert len(payload) == EXPECTED_SIZE, (
        f"Source byte count changed: {len(payload)}; not a valid frozen sample")
    git_hash = sha1(
        f"blob {len(payload)}\0".encode("ascii") + payload
    ).hexdigest()
    assert git_hash == EXPECTED_GIT_SHA1, (
        f"Source Git blob changed from {EXPECTED_GIT_SHA1} to {git_hash}")
    assert payload[:8] == b"\x89PNG\r\n\x1a\n"
    return payload, git_hash


def sample_image(payload):
    with Image.open(BytesIO(payload)) as source:
        assert source.size == EXPECTED_DIMENSIONS, source.size
        source_mode = source.mode
        im = source.convert("RGB")
    assert PIXELS_PER_ROW == 128 and PIXELS_PER_COL == 256 and BANKS == 64
    # No post-hoc tuning of the origin or stride. This origin is a conjectured
    # implementation of the published "top-left, every 16 pixels" operation.
    colours = [
        tuple(im.getpixel((SAMPLE_STEP*x, SAMPLE_STEP*y)))
        for y in range(PIXELS_PER_COL)
        for x in range(PIXELS_PER_ROW)
    ]
    return source_mode, colours


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="Local byte-exact source PNG (optional)")
    ap.add_argument("--output", help="Write result JSON to file, if provided")
    args = ap.parse_args()

    n, obs = observations()
    assert n == 84 and len(obs) == 66
    payload, git_hash = load_bytes(args.source)
    mode, lattice = sample_image(payload)
    assert len(lattice) == BANKS*BANK_SIZE == 32768
    colours = Counter(lattice)
    state_pairs = []
    for state in legal_states():
        master = generate_master(state)
        if all(master[k-1] == v for k, v in obs.items()):
            state_pairs.append((state, master))
    assert len(state_pairs) == 10
    balanced = [
        (state, master) for state, master in state_pairs
        if state.p == 0 and state.G == 0
    ]
    assert len(balanced) == 2

    # Source provides a pixel lattice. Everything after that point is
    # *invented* and therefore is enumerated, not tuned for attractive text.
    registers = []
    for state, master in balanced:
        addresses = class_addresses(master)
        depths = q4_depths(master)
        assert max(addresses) < 512
        readings = []
        for bank in range(BANKS):
            rgb = [
                lattice[bank*BANK_SIZE + address] for address in addresses
            ]
            channel_bytes = [rgb[j][depths[j]] for j in range(9)]
            readings.append({
                "bank": bank,
                "byte_hex": bytes(channel_bytes).hex(),
                "rgb_hex": [bytes(c).hex() for c in rgb],
                "ascii_escaped": "".join(
                    chr(x) if 32 <= x <= 126 else "." for x in channel_bytes
                ),
                "printable_byte_count": sum(32 <= x <= 126
                                            for x in channel_bytes),
            })
        registers.append({
            "state": f"{state.X}{state.Y}{state.Z}{state.G}",
            "class_addresses": addresses,
            "q4_channel_depths": depths,
            "bank_readouts": readings,
        })

    # CL-02's 189,252,315 row outputs do not all fit as coordinate values
    # on EITHER independently measured sampled axis (128 or 256).
    cl02 = [189, 252, 315]
    result = {
        "status": "CL-04 conditional real-source replay, not solution evidence",
        "source": {
            "upstream_blob_repo": "twinysam/INSIDE-ARG",
            "upstream_path": UPSTREAM_PATH,
            "source_git_sha1": git_hash,
            "source_sha256": sha256(payload).hexdigest(),
            "source_bytes": len(payload),
            "dimensions": EXPECTED_DIMENSIONS,
            "png_mode": mode,
        },
        "historically_reported_operation": {
            "step": SAMPLE_STEP,
            "origin": [0, 0],
            "origin_assumption": "Top-left grid origin; not a recovered user key",
            "grid_dimensions": [PIXELS_PER_ROW, PIXELS_PER_COL],
            "grid_sites": len(lattice),
            "distinct_exact_sampled_rgb_colors": len(colours),
            "top_20_exact_sampled_rgb_colors": [
                {"rgb": list(color), "count": count}
                for color, count in colours.most_common(20)
            ],
            "black_sample_count": colours[(0,0,0)],
            "white_sample_count": colours[(255,255,255)],
        },
        "candidate_reader": {
            "schema": "9 addresses in 0..511, one RGB channel per class from Q4",
            "record_order": "128 sampled pixels per row, consecutive rows",
            "bank_grid": "64 consecutive 128x4 sampled-pixel bands",
            "unfixed_bank_count": BANKS,
            "unfixed_channel_label_maps": 6,
            "unfixed_other_registrations": "at least alternative origins and traversals; not searched",
            "native_source_supports_this_reader": False,
            "blind_candidate_selection": False,
        },
        "actual_observed_h108_live_states": len(state_pairs),
        "conditionally_selected_states": registers,
        "CL02_three_row_numbers": cl02,
        "CL02_direct_sampled_x_in_range": all(v < PIXELS_PER_ROW for v in cl02),
        "CL02_direct_sampled_y_in_range": all(v < PIXELS_PER_COL for v in cl02),
        "interpretation": (
            "Acquiring exact original source bytes and replaying the historical "
            "16-pixel grid yields a real pixel corpus. The 512-bin addressing, "
            "64-bank grouping and 0/1/2-to-R/G/B mapping are invented. No "
            "single bank or plaintext may be declared a solution without an "
            "independent source-selected bank and a withheld verification."
        ),
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf8")
    else:
        print(text)
    # Keep actions log compact when --output is set.
    if args.output:
        print(json.dumps({
            "original_git_sha1": git_hash,
            "source_size": len(payload),
            "source_dimensions": EXPECTED_DIMENSIONS,
            "sampled_grid": [PIXELS_PER_ROW, PIXELS_PER_COL],
            "distinct_exact_colors": len(colours),
            "top_colors": result["historically_reported_operation"]
                        ["top_20_exact_sampled_rgb_colors"][:12],
            "per_branch_64_bank_max_printable": [
                {"state": x["state"],
                 "max": max(z["printable_byte_count"]
                            for z in x["bank_readouts"]),
                 "all_nine_printable_banks": [
                     z["bank"] for z in x["bank_readouts"]
                     if z["printable_byte_count"] == 9
                 ]}
                for x in registers
            ],
            "CL02_three_positions_fall_within_sampled_grid_y":
                result["CL02_direct_sampled_y_in_range"],
        }, indent=2))


if __name__ == "__main__":
    main()

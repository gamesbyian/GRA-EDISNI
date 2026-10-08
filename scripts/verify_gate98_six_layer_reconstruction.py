#!/usr/bin/env python3
"""CL-07: complete historical gate-98 six-colour white-layer positive control.

No sticker data are loaded. Alignment was found AFTER viewing the independently
dated 2019 solved image, so this is an exact retrospective historical replay,
not a blind test or a CE sticker decoder.

Fixture-only mode uses stdlib. With --source and --witness, it verifies both
byte-pinned original PNGs, projects every exact-RGB source point through a
translation onto a 916x913 receiving canvas (out-of-image coordinates are
simply empty), and compares the *bright binary mask* bit-for-bit.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FIXTURE = BASE / "data" / "conjecture-lab-gate98-six-layer-complete-2026-10-08.json"
ORIGINAL_SHA256 = "db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded"
WITNESS_SHA256 = "ae685557122be8562028d8a1c4384c954a760bc4e42e6877c29391d810892d12"
MASK_SHA256 = "e730cd817bfdb952dad01d8a55a9684ca4114746e2398fce5418395527a0f5ff"

def fixture():
    d = json.loads(FIXTURE.read_text(encoding="utf8"))
    assert d["source_png_sha256"] == ORIGINAL_SHA256
    assert d["witness_png_sha256"] == WITNESS_SHA256
    assert d["witness_binary_mask_sha256"] == MASK_SHA256
    assert d["witness_binary_mask_shape"] == [913, 916]
    assert d["target_assisted_offsets"] is True
    assert d["ce_sticker_data_used"] is False
    assert d["historical_color_legend_independently_recovered"] is False
    assert d["source_color_layers_total"] == 6
    layers = d["layers"]
    assert len(layers) == 6 and len({x["rgb_hex"] for x in layers}) == 6
    assert [x["registration_xy"] for x in layers] == [
        [16,36], [1045,57], [14,851], [18,1638], [1121,787], [1155,1755]
    ]
    assert [x["exact_mark_count"] for x in layers] == [309,463,431,324,590,560]
    assert [x["new_mark_count"] for x in layers] == [309,458,420,324,559,507]
    assert sum(x["new_mark_count"] for x in layers) == 2577
    assert sum(x["exact_mark_count"] for x in layers) == 2677
    assert d["previously_rejected_offset_xy"] == [1123,1755]
    assert d["previously_rejected_offset_false_positives"] == 309
    assert d["final_offset_xy"] == [1155,1755]
    assert d["final_offset_overhang_right_px"] == 23
    assert d["total_white_count"] == 2577
    assert d["false_white"] == 0 and d["missing_white"] == 0
    return d

def full_replay(d, source_path, witness_path, png_output=None):
    from PIL import Image
    import numpy as np

    source_raw = Path(source_path).read_bytes()
    witness_raw = Path(witness_path).read_bytes()
    assert sha256(source_raw).hexdigest() == ORIGINAL_SHA256
    assert sha256(witness_raw).hexdigest() == WITNESS_SHA256
    original = np.asarray(Image.open(source_path).convert("RGB"))
    historical = np.asarray(Image.open(witness_path).convert("RGB"))
    assert original.shape == (4096,2048,3)
    assert historical.shape == (913,916,3)
    historic_bright = historical[:,:,0] > 200
    assert int(historic_bright.sum()) == 2577
    result = np.zeros_like(historic_bright)

    rows = []
    for obj in d["layers"]:
        ox, oy = obj["registration_xy"]
        rgb = tuple(bytes.fromhex(obj["rgb_hex"]))
        sy,sx = np.where(np.all(original == rgb, axis=2))
        # Project ALL exact source-color coordinates, supporting a receiving
        # window extending 23 pixels beyond the right border of the source.
        tx = sx - ox
        ty = sy - oy
        keep = (0 <= tx)&(tx < 916)&(0 <= ty)&(ty < 913)
        layer = np.zeros_like(historic_bright)
        layer[ty[keep],tx[keep]] = True
        n = int(layer.sum())
        new = int((layer & ~result).sum())
        bad = int((layer & ~historic_bright).sum())
        assert (n,new,bad) == (obj["exact_mark_count"],
                              obj["new_mark_count"],0), (obj,n,new,bad)
        result |= layer
        rows.append({"rgb_hex":obj["rgb_hex"],"source_offset":[ox,oy],
                     "marks":n,"new":new,"outside_reference":bad})

    total = int(result.sum())
    false = int((result & ~historic_bright).sum())
    missing = int((historic_bright & ~result).sum())
    assert (total,false,missing) == (2577,0,0)
    packed = np.packbits(result.astype(np.uint8),axis=None).tobytes()
    assert len(packed) == 104539
    packed_sha = sha256(packed).hexdigest()
    assert packed_sha == MASK_SHA256
    historic_packed = np.packbits(historic_bright.astype(np.uint8),axis=None).tobytes()
    assert packed == historic_packed
    # Negative control: keep the earlier legal-rectangle crop and failure.
    old = np.all(original[1755:1755+913,1123:1123+916,:] == (2,2,6),axis=2)
    assert int(old.sum()) == 560
    assert int((old & ~historic_bright).sum()) == 309
    if png_output:
        Image.fromarray((result*255).astype(np.uint8),mode="L").save(png_output)
    return {
        "status":"PASS: exact six-colour historical bright-mask reconstruction",
        "recovered_bright_pixels":total,
        "source_false_positives":false,
        "witness_false_negatives":missing,
        "mask_sha256":packed_sha,
        "layers":rows,
        "notes":"Does not reproduce historical witness dark-gray pixels or original 18-value RGB palette."
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",help="original 2048x4096 gate-98 source PNG")
    p.add_argument("--witness",help="2019 Game Detectives 916x913 PNG")
    p.add_argument("--png-output",help="write reconstructed binary bright-layer image")
    args=p.parse_args()
    d=fixture()
    assert bool(args.source) == bool(args.witness), "source and witness supplied together"
    if args.png_output and not args.source:
        p.error("--png-output requires --source and --witness")
    if args.source:
        result=full_replay(d,args.source,args.witness,args.png_output)
    else:
        result={"status":"PASS: frozen CL07 fixture verified (source pixel replay requires source and witness)",
                "total":d["total_white_count"],"missing":d["missing_white"],
                "false":d["false_white"],"mask_sha256":MASK_SHA256}
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()

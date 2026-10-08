#!/usr/bin/env python3
"""Recreate and validate canonical partial 534brn token constraints locally.

No network or image guessing. Inputs are preserved research captures. The A
input is explicitly a 12,150-byte *connector rendition* of the 12,140-byte
upstream Git blob; do not label it a byte-identical original capture.

Each '??' is an unknown token, not a legal byte of a repaired JPEG.
The original Exp 337 edit alignment is a heuristic: recovered positions are
alignment-supported, not proven uniquely placed across all optimal alignments.

Run: python scripts/rebuild_534brn_partial_evidence.py
Optionally: --emit /tmp/534brn-constraints.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_534brn_loss_map import (
    UNKNOWN, TERMINAL, find_ascii, make_map, tokenize
)

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "archive/external/terminal41-534brn"
INPUTS = {
    "A": ("A-connector-rendition-not-original.bin", "f9cdbd18bbd8713adee89ad93a3551b6310fd7ba", 12150),
    "B": ("B-original-capture.bin", "f12c02c49f4c3f7589419fe8e20d655f7b95a9f4", 16922),
    "P": ("P-partial-capture.bin", "9580913d043ca3efd54a01a38a9cff5767ea8ee7", 8760),
    "X": ("X-xmp-fragment.bin", "b6f5ffed946d9d19dfd0a5d90a8b18759a90c496", 2804),
}
FROZEN = ROOT / "data/534brn-canonical-partial-evidence-2026-10-08.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def regenerate() -> dict:
    raw = {}
    for label, (name, sha, size) in INPUTS.items():
        payload = (CAPTURE / name).read_bytes()
        assert len(payload) == size and git_blob_sha(payload) == sha, (label, "source identity")
        raw[label] = payload

    A, B, P = (tokenize(raw[label], label) for label in ("A", "B", "P"))
    a_j = find_ascii(A, b"JFIF")
    b_j = find_ascii(B, b"JFIF")
    a_end = find_ascii(A, TERMINAL) + len(TERMINAL)
    b_end = find_ascii(B, TERMINAL) + len(TERMINAL)
    p_end = find_ascii(P, TERMINAL) + len(TERMINAL)
    mapping_a = make_map(A, B, a_j, a_end, b_j, b_end)
    mapping_p = make_map(P, B, 0, p_end, 7387, b_end)

    codes: list[str] = []
    hexes: list[str] = []
    conflicts: list[dict] = []
    recovered: list[dict] = []
    counts = dict.fromkeys("BAPDUC", 0)

    for index in range(b_j, b_end):
        base = B[index]
        aidx = mapping_a.get(index)
        pidx = mapping_p.get(index)
        av = A[aidx] if aidx is not None else UNKNOWN
        pv = P[pidx] if pidx is not None else UNKNOWN

        if base != UNKNOWN:
            tag, val = "B", base
        elif av != UNKNOWN and pv != UNKNOWN and av != pv:
            tag, val = "C", UNKNOWN
            conflicts.append({"offset": index - b_j,
                              "a": f"{av:02x}", "p": f"{pv:02x}"})
        elif av != UNKNOWN and pv != UNKNOWN:
            tag, val = "D", av
        elif av != UNKNOWN:
            tag, val = "A", av
        elif pv != UNKNOWN:
            tag, val = "P", pv
        else:
            tag, val = "U", UNKNOWN

        counts[tag] += 1
        codes.append(tag)
        hexes.append("??" if val == UNKNOWN else f"{val:02x}")
        if tag in "APD":
            recovered.append({"offset": index - b_j, "byte": f"{val:02x}", "source": tag})

    assert len(codes) == 12052
    assert counts == {"B": 10057, "A": 149, "P": 10, "D": 79, "U": 1747, "C": 10}
    assert len(recovered) == 238 and len(conflicts) == 10

    return {
        "counts": counts, "conflicts": conflicts, "recovered_sites": recovered,
        "hex_pairs_64_per_line": [
            "".join(hexes[i:i + 64]) for i in range(0, len(hexes), 64)],
        "source_flags_64_per_line": [
            "".join(codes[i:i + 64]) for i in range(0, len(codes), 64)]
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--emit", type=Path, help="save regenerated full JSON (same envelope as frozen)")
    args = p.parse_args()
    doc = json.loads(FROZEN.read_text(encoding="utf-8"))
    calculated = regenerate()
    for key, expected in calculated.items():
        assert doc[key] == expected, f"drift in {key}"
    assert doc["summary"] == {
        "B_unknown_initial": 1995, "alignment_supported_fill": 238,
        "remaining_unknown": 1757, "conflicting_positions": 10
    }
    if args.emit:
        args.emit.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print("PASS: all 12,052 token values/flags; 238 candidate fills; 1,757 unknown; 10 conflicts")
    print("NOTE: A is connector-rendered, not byte-identical to its original upstream Git blob.")


if __name__ == "__main__":
    main()

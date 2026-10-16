#!/usr/bin/env python3
"""DISCOVER/DEVELOP: gate cross-capture JPEG-byte hypotheses against erasure types.

This is an offline *type-consistency* audit, not a JPEG reconstruction.
The frozen Exp 337 B/A/P alignment is provisional, and the Exp 423 P-only
constraint decoder adopts one lost high byte (0x80..0xff) per U+FFFD token.

Those contracts MUST NOT be mechanically combined: source-channel and
alignment uncertainty may cause a low-valued alternate-capture candidate to
appear over a B unknown. This script quantifies that exact discrepancy.

Run: python scripts/conjecture_lab_534brn_capture_type_gate.py
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIAL = ROOT / "data/534brn-canonical-partial-evidence-2026-10-08.json"
EX423 = ROOT / "data/experiment-423-534brn-mcu-constraint.json"
XMP = ROOT / "archive/external/terminal41-534brn/X-xmp-fragment.bin"
SOS = "????200c03012002110311203f20"
FOOTER = "70655e213032756e"  # pe^!02un


def get_tokens(data):
    line_hex = data["hex_pairs_64_per_line"]
    line_flags = data["source_flags_64_per_line"]
    chars = "".join(line_hex)
    flags = "".join(line_flags)
    assert len(chars) == 2 * data["token_length"] == 24104
    assert len(flags) == data["token_length"] == 12052
    assert re.fullmatch(r"(?:[0-9a-f]{2}|\?\?)+", chars)
    assert set(flags) <= set("BAPDUC")
    tokens = [chars[2*i:2*i+2] for i in range(len(flags))]
    for flag, token in zip(flags, tokens):
        if flag in "UC":
            assert token == "??"
        else:
            assert token != "??"
    return tokens, flags


def status(positions, tokens, flags):
    counts = collections.Counter(flags[i] for i in positions)
    filled = collections.Counter()
    samples = []
    for i in positions:
        if flags[i] not in "APD":
            continue
        val = int(tokens[i], 16)
        typed = "high" if val >= 0x80 else "low"
        filled[(flags[i], typed)] += 1
        if len(samples) < 10 and val < 0x80:
            samples.append({"jfif_offset": i, "flag": flags[i],
                            "candidate_value_hex": tokens[i]})
    return {
        "source_flag_counts": {k: counts.get(k, 0) for k in "BAPDUC"},
        "proposed_fill_high_only_compatible": sum(
            n for (flag, tag), n in filled.items() if tag == "high"),
        "proposed_fill_outside_high_erasure_domain": sum(
            n for (flag, tag), n in filled.items() if tag == "low"),
        "proposed_by_channel_and_domain": {
            f"{flag}_{typ}": filled[(flag, typ)]
            for flag in "APD" for typ in ("low", "high")
        },
        "low_candidate_examples": samples
    }


def main():
    partial = json.loads(PARTIAL.read_text())
    old = json.loads(EX423.read_text())
    tokens, flags = get_tokens(partial)
    assert partial["counts"] == {
        "B": 10057, "A": 149, "P": 10, "D": 79, "U": 1747, "C": 10
    }
    assert old["feasible_complete_mcu_counts"] == {
        "min": 16, "max": 300, "count": 285, "contiguous": True
    }

    sos = [i for i in range(len(tokens)) if
           "".join(tokens[i:i+14]) == SOS]
    assert sos == [7733]
    start = sos[0] + 14
    assert "".join(tokens[-8:]) == FOOTER
    assert tokens[-10:-8] == ["??", "??"]  # conditional EOI-shaped pair
    end = len(tokens) - 10
    assert (start, end, end-start) == (7747, 12042, 4295)

    whole = status(range(len(tokens)), tokens, flags)
    scan = status(range(start, end), tokens, flags)
    assert whole["proposed_fill_outside_high_erasure_domain"] == 231
    assert whole["proposed_fill_high_only_compatible"] == 7
    assert scan["proposed_fill_outside_high_erasure_domain"] == 231
    assert scan["proposed_fill_high_only_compatible"] == 7
    assert scan["source_flag_counts"] == {
        "B": 2503, "A": 149, "P": 10, "D": 79, "U": 1544, "C": 10
    }

    # File contains only attribution/create-time metadata, no exact dimensions.
    xmp = XMP.read_bytes()
    assert len(xmp) == 2804
    assert b"AnSet" in xmp and b"2016-12-16T14:12:24.351" in xmp
    dimensional_tags = (
        b"PixelXDimension", b"PixelYDimension", b"ImageWidth",
        b"ImageLength", b"tiff:ImageWidth", b"tiff:ImageLength",
        b"ExifImageWidth", b"ExifImageHeight",
    )
    matched = [tag.decode() for tag in dimensional_tags if tag in xmp]
    assert not matched

    geometrically_possible = old["independent_dimension_domain"][
        "possible_mcu_products"]
    assert len(geometrically_possible) == 43
    assert old["independent_dimension_domain"][
        "surviving_mcu_products"] == geometrically_possible
    assert 64 in geometrically_possible and not old["only_64_in_dimension_domain"]

    result = {
        "status": "source-type consistency and stopping-gate audit",
        "baseline_experiment": 423,
        "canonical_cross_capture_fixture": PARTIAL.name,
        "full_JFIF_through_footer": whole,
        "aligned_B_entropy_tokens": {
            "start_offset_from_JFIF": start,
            "end_exclusive_offset_from_JFIF": end,
            "span": end-start,
            **scan
        },
        "conditional_erasure_domain": "0x80..0xff for one U+FFFD",
        "cross_capture_interpretation": (
            "231 of 238 proposed B-unknown fills are low-valued ASCII/control "
            "bytes, outside the conditional high-byte erasure domain. This "
            "proves the *combined interpretation* is inconsistent at those "
            "positions if alignment and the B high-only model are both "
            "asserted. It does not prove any particular alternate capture "
            "is wrong; edit alignment and source transformation differ."
        ),
        "recovered_xmp": {
            "source": str(XMP.relative_to(ROOT)),
            "authored_create_date": "2016-12-16T14:12:24.351",
            "dimension_field_names_seen": matched,
            "has_verified_dimensions": False,
        },
        "mcu_model": {
            "P_only_decoder_existing_experiment": 423,
            "domain_feasible_products": len(geometrically_possible),
            "domain_products_surviving": len(
                old["independent_dimension_domain"]["surviving_mcu_products"]),
            "64_feasible_but_not_unique": True,
        },
        "must_not_promote": [
            "238 alignment-dependent fills to independently verified bytes",
            "231 typed-inconsistent fills to one-high-byte replacements",
            "128 UNSOLVED to proved 128x128 pixel dimensions",
            "128 image dimension to a 128-character Steam beta credential"
        ],
        "next_reopening_condition": (
            "independent less-lossy JPEG source, exact same-byte alignment "
            "and channel model, or independent dimension metadata/geometry"
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

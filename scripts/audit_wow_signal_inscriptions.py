#!/usr/bin/env python3
"""Bounded 2026-10-09 Wow!-encoding test on 2016 INSIDE signs.

The four strings were fixed from historical sources before testing.
The test does not assume any relationship to Collector's Edition stickers.
"""
import json
from itertools import product

SAMPLES = {
    "Wow! 1977 positive reference": "6EQUJ5",
    "INSIDE station sign (2016)": "A10N7",
    "INSIDE wrecked train (2016)": "L08",
    "INSIDE lab label suffix (2016)": "B02",
}


def code_value(character):
    if character in "123456789":
        return int(character)
    if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return ord(character) - ord("A") + 10
    if character == " ":
        return 0
    raise ValueError("Not representable on authentic Big Ear printout: %r" % character)


def is_single_hump(values):
    # Allows a peak at either endpoint: deliberately generous to candidate codes.
    return any(
        all(values[i] <= values[i + 1] for i in range(p))
        and all(values[i] >= values[i + 1] for i in range(p, len(values) - 1))
        for p in range(len(values))
    )


def analyze(s):
    strict = None
    try:
        strict = [code_value(c) for c in s]
    except ValueError:
        pass
    # Deliberately NON-AUTHENTIC: zero printed as digit instead of a blank.
    tolerant = [0 if c == "0" else code_value(c) for c in s]
    return {
        "literal": s,
        "authentic_printout_valid": strict is not None,
        "non_authentic_zero_tolerant_values": tolerant,
        "zero_as_glyph_count": s.count("0"),
        "single_hump_including_endpoint_peaks": is_single_hump(tolerant),
        "strict_interior_peak": (
            is_single_hump(tolerant)
            and max(tolerant) > max(tolerant[0], tolerant[-1])
        ),
        "absolute_adjacent_differences": [
            abs(b - a) for a, b in zip(tolerant, tolerant[1:])
        ],
        "character_class_pattern": "".join(
            "L" if c.isalpha() else "D" for c in s
        ),
    }


def glyph_readings(s):
    """Explore only visually confusable 0/O and 1/I, with no claim of source ambiguity."""
    options = [
        (c, "O") if c == "0" else (c, "I") if c == "1" else (c,)
        for c in s
    ]
    return ["".join(chars) for chars in product(*options)]


def main():
    result = {name: analyze(value) for name, value in SAMPLES.items()}
    assert result["Wow! 1977 positive reference"]["authentic_printout_valid"]
    assert result["Wow! 1977 positive reference"]["strict_interior_peak"]
    for name in list(SAMPLES)[1:]:
        assert not result[name]["authentic_printout_valid"]
        assert not result[name]["single_hump_including_endpoint_peaks"]
    assert result["INSIDE station sign (2016)"]["non_authentic_zero_tolerant_values"] == [10, 1, 0, 23, 7]
    assert result["INSIDE wrecked train (2016)"]["non_authentic_zero_tolerant_values"] == [21, 0, 8]
    assert result["INSIDE lab label suffix (2016)"]["non_authentic_zero_tolerant_values"] == [11, 0, 2]
    # An *exploratory*, after-inspection visual ambiguity model: 0/O and 1/I.
    # Across 2+1+1 ambiguous positions there are exactly 16 joint readings.
    ambiguous = {
        name: [
            analyze(s) for s in glyph_readings(original)
            if analyze(s)["authentic_printout_valid"]
            and analyze(s)["strict_interior_peak"]
        ]
        for name, original in list(SAMPLES.items())[1:]
    }
    assert [x["literal"] for x in ambiguous["INSIDE station sign (2016)"]] == ["AION7"]
    assert [x["literal"] for x in ambiguous["INSIDE wrecked train (2016)"]] == ["LO8"]
    assert [x["literal"] for x in ambiguous["INSIDE lab label suffix (2016)"]] == ["BO2"]
    assert 4 * 2 * 2 == 16  # total joint possibilities for the narrow ambiguity model
    result["exploratory_glyph_confusion_after_inspection"] = ambiguous
    result["glyph_confusion_joint_readings"] = 16
    result["glyph_confusion_joint_readings_all_single_interior_peak"] = (
        len(ambiguous["INSIDE station sign (2016)"])
        * len(ambiguous["INSIDE wrecked train (2016)"])
        * len(ambiguous["INSIDE lab label suffix (2016)"])
    )
    # Negative control added after inspecting the appealing AION7 curve.
    # Every A?ON7 (where ? is ANY Big Ear letter) is strictly interior-peaked:
    # A=10 <= ?; O=24 > N=23 > terminal 7. A letter above O merely
    # moves the peak one position earlier. The observed hump is thus forced
    # by this post-hoc glyph reinterpretation + alphabet ranks.
    replacement_controls = [
        "A" + chr(ord("A") + offset) + "ON7" for offset in range(26)
    ]
    assert len(replacement_controls) == 26
    assert all(
        analyze(word)["authentic_printout_valid"]
        and analyze(word)["strict_interior_peak"]
        for word in replacement_controls
    )
    assert analyze("LO8")["strict_interior_peak"]
    assert analyze("BO2")["strict_interior_peak"]
    result["matched_null_A_any_letter_O_N_7"] = {
        "total_letter_replacements": len(replacement_controls),
        "single_interior_peak": sum(
            analyze(word)["strict_interior_peak"]
            for word in replacement_controls
        ),
        "interpretation": (
            "The AION7 hump has no discriminating power against "
            "the matched character-class null once 1/I and 0/O are adopted."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bounded 2026-10-09 Wow!-encoding test on 2016 INSIDE signs.

The four strings were fixed from historical sources before testing.
The test does not assume any relationship to Collector's Edition stickers.
"""
import json

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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

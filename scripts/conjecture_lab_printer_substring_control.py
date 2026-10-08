#!/usr/bin/env python3
"""CL-02: answer-assisted candidate readout vs original printer substrings.

The candidate readout was selected using TWO speculative grammar assumptions:
globally balanced Q4 selector depths and the selected-surface one-dash-per-
physical-column constraint.  No claimed native printer bridge exists.

Compare the selected 27-bit output with all 27-wide substrings of authentic
saved PC/PS4 (32) and Xbox One (36) long printer rows. The same four
orientation/polarity variants are granted to 4,000 seeded random 9-dash words.
"""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READOUT = "-/-////-/" + "-//////--" + "/--///-//"
ALL_MASK = (1 << 27) - 1


def source_rows(filename, width):
    lines = (ROOT / filename).read_text(encoding="utf8").splitlines()
    rows = [s for s in lines if len(s) == width and not s.startswith("#")]
    return rows


def bitmask(s, char="-"):
    return sum(1 << i for i, v in enumerate(s) if v == char)


def reverse27(bits):
    return sum(((bits >> i) & 1) << (26-i) for i in range(27))


def source_windows():
    sources = (
        ("pc", source_rows("data/printer-reference/pc-ps4-raw.txt", 32)),
        ("xbox", source_rows("data/printer-reference/xbox-one-raw.txt", 36)),
    )
    assert [len(rows) for _, rows in sources] == [32, 36]
    output = []
    for name, rows in sources:
        for row_index, row in enumerate(rows, 1):
            for offset in range(len(row)-26):
                word = row[offset:offset+27]
                output.append({
                    "source": name,
                    "row": row_index,
                    "offset": offset,
                    "dash_mask": bitmask(word, "-"),
                    "dot_mask": bitmask(word, "."),
                })
    assert len(output) == 552
    return output


def min_distance4(bits, windows):
    rev = reverse27(bits)
    variants = (bits, rev, (~bits) & ALL_MASK, (~rev) & ALL_MASK)
    return min(
        window["dot_mask"].bit_count()
        + ((v ^ window["dash_mask"])
           & (~window["dot_mask"]) & ALL_MASK).bit_count()
        for v in variants for window in windows
    )


def control(windows):
    seed = 101934552
    hist = Counter()
    for _ in range(4000):
        order = list(range(27))
        for j in range(26, 0, -1):
            seed = (1664525 * seed + 1013904223) & 0xffffffff
            k = seed % (j+1)
            order[j], order[k] = order[k], order[j]
        bits = sum(1 << x for x in order[:9])
        hist[min_distance4(bits, windows)] += 1
    return dict(sorted(hist.items()))


def run():
    assert len(READOUT) == 27 and READOUT.count("-") == 9
    windows = source_windows()
    obs = min_distance4(bitmask(READOUT), windows)
    hist = control(windows)
    assert obs == 6
    assert sum(hist.values()) == 4000
    assert hist == {2: 2, 3: 31, 4: 223, 5: 860,
                    6: 1589, 7: 1162, 8: 133}, hist
    n_le = sum(n for d, n in hist.items() if d <= obs)
    assert n_le == 2705
    return {
        "research_status": "ANSWER-ASSISTED EXPLORATION; no native consumer",
        "readout": READOUT,
        "dash_count": READOUT.count("-"),
        "printer_windows": len(windows),
        "variants": [
            "forward", "reversed", "inverted", "inverted_reversed"
        ],
        "minimum_hamming_distance": obs,
        "exact_matches": 0,
        "same_dashes_shuffle_controls": 4000,
        "seed": 101934552,
        "control_distance_histogram": hist,
        "control_at_least_as_close": n_le,
        "control_fraction_at_least_as_close": n_le/4000,
        "scope": (
            "Only unmodified contiguous 27-wide slices of the published "
            "PC/PS4 and Xbox printer long rows, with four orientation/"
            "polarity variants. Does not reject spatial overlays, row "
            "sorting, keyed encoding, pixel filters or other source "
            "artifacts. Randomized distance frequency is exploratory, "
            "not a post-selection significance test."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

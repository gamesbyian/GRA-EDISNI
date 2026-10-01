#!/usr/bin/env python3
"""Experiment 351: identifiability of the historical 9+3 nested-index proposal."""

from __future__ import annotations

import csv
import itertools
import json
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
OUT = ROOT / "data" / "experiment-351-historical-nested-index-identifiability.json"
CLASSES = "ABCDEFGHI"


def load():
    vals = {}
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            residue = int(row["residue"])
            symbol = row["symbol"]
            old = vals.get(residue)
            if old is not None and old != symbol:
                raise AssertionError(f"conflict at residue {residue}")
            vals[residue] = symbol
    return vals


def class_trace(vals, j):
    body = [vals.get(1 + j + 9*k, "?") for k in range(9)]
    tail = [vals.get(82 + j + 9*k, "?") for k in range(3)]
    return body, tail


def binary_words(trace, slash_bit):
    out = []
    unknown = [i for i, x in enumerate(trace) if x == "?"]
    for fill in itertools.product((0, 1), repeat=len(unknown)):
        bits = [None] * len(trace)
        fi = 0
        for i, sym in enumerate(trace):
            if sym == "?":
                bits[i] = fill[fi]
                fi += 1
            elif sym == "/":
                bits[i] = slash_bit
            elif sym == "-":
                bits[i] = 1 - slash_bit
            else:
                raise AssertionError(sym)
        value = 0
        for bit in bits:
            value = (value << 1) | bit
        out.append(value)
    return sorted(set(out))


def tail_indexes(trace):
    # Independently supported tail family from Experiment 317:
    # exactly one slash among the three positions, remaining cells dots.
    out = []
    for exceptional in range(3):
        candidate = [".", ".", "."]
        candidate[exceptional] = "/"
        if all(obs == "?" or obs == want for obs, want in zip(trace, candidate)):
            out.append(exceptional)
    return out


def main():
    vals = load()
    rows = []
    body_joint_per_polarity = 1
    tail_joint = 1

    for j, cls in enumerate(CLASSES):
        body, tail = class_trace(vals, j)
        words_slash1 = binary_words(body, 1)
        words_slash0 = binary_words(body, 0)
        indexes = tail_indexes(tail)
        assert len(words_slash1) == 2 ** body.count("?")
        assert words_slash0 == sorted(511 - value for value in words_slash1)
        assert indexes

        body_joint_per_polarity *= len(words_slash1)
        tail_joint *= len(indexes)
        rows.append({
            "class": cls,
            "body_trace": "".join(body),
            "body_unknowns": body.count("?"),
            "body_word_count_per_global_polarity": len(words_slash1),
            "slash_equals_1_min": min(words_slash1),
            "slash_equals_1_max": max(words_slash1),
            "tail_trace": "".join(tail),
            "tail_index_domain": indexes,
            "tail_index_count": len(indexes),
        })

    result = {
        "experiment": 351,
        "historical_model": "first 9 class-trace symbols encode a binary larger-domain value; last 3 encode a smaller index",
        "body_read_order": "chronological within each A-I class trace, most-significant bit first",
        "body_global_polarities": 2,
        "tail_family": "exactly one slash among three positions, from Experiment 317",
        "classes": rows,
        "body_joint_assignments_per_global_polarity": body_joint_per_polarity,
        "tail_joint_assignments": tail_joint,
        "joint_body_tail_assignments_including_two_global_body_polarities": body_joint_per_polarity * tail_joint * 2,
        "fixed_body_words_before_polarity": [r["class"] for r in rows if r["body_word_count_per_global_polarity"] == 1],
        "fixed_tail_indexes": [r["class"] for r in rows if r["tail_index_count"] == 1],
        "interpretation": "literal historical binary-body plus three-way-tail nested index is structurally admissible but massively underidentified without an external consumer/codebook"
    }

    assert body_joint_per_polarity == 134_217_728
    assert tail_joint == 36
    assert result["joint_body_tail_assignments_including_two_global_body_polarities"] == 9_663_676_416
    assert result["fixed_body_words_before_polarity"] == ["C"]
    assert result["fixed_tail_indexes"] == ["B", "E", "F", "H", "I"]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

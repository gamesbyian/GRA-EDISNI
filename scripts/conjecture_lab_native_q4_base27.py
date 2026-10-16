#!/usr/bin/env python3
"""Exact nine-A-I-class base27 projection under the conditional Q4 depth rule.

Enumerates compatible *output classes* without testing any live password
interface or claiming that base27 is the intended CE interpretation.
Run: python scripts/conjecture_lab_native_q4_base27.py
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from conjecture_lab_native_q4_receiver import (
    SIGNS, class_options, core_groups, min_disagreements,
    q4_choices, requested_cells, source_data,
)


def compatible_outputs(groups, choices):
    allowed = class_options(groups, choices)
    cartesian = itertools.product(*(allowed[c] for c in "ABCDEFGHI"))
    requests = tuple(
        requested_cells(sel) for sel in itertools.product(*choices)
    )
    checked = 0
    accepted = []
    for class_words in cartesian:
        checked += 1
        panel = tuple(
            "".join(word[q] for word in class_words) for q in range(3)
        )
        if any(min_disagreements(panel, groups, req, bound=0) == 0
               for req in requests):
            accepted.append(class_words)
    return checked, tuple(accepted), allowed


def alphabetic_counts(words):
    summary = []
    for mapping in itertools.permutations(SIGNS):
        decoder = dict(zip(mapping, range(3)))
        a0 = a1 = 0
        for line in words:
            codes = tuple(
                sum(decoder[c] * weight for c, weight in zip(w, (9,3,1)))
                for w in line
            )
            a0 += all(0 <= n <= 25 for n in codes)
            a1 += all(1 <= n <= 26 for n in codes)
            assert codes[4] == codes[5] == 13 * decoder["/"]
        summary.append(("".join(mapping), a0, a1))
    return tuple(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-primary-dots", action="store_true")
    parser.add_argument("--out-json", type=Path,
                        help="Write exact mask bank for an authenticated downstream artifact")
    args = parser.parse_args()
    observed, _ = source_data()
    primary_alphabet = SIGNS if args.allow_primary_dots else "/-"
    groups = core_groups(observed, primary_alphabet)
    print("Assumed primary alphabet:", primary_alphabet)
    choices = q4_choices(observed)
    assert all(choices)
    total, outputs, class_sets = compatible_outputs(groups, choices)
    assert total == (6480 if args.allow_primary_dots else 384)
    assert len(outputs) == (5808 if args.allow_primary_dots else 364)
    print("Raw independent class-word Cartesian product:", total)
    print("Exactly compatible nine-class words:", len(outputs))
    print("Rejected by cross-class primary triplet dependence:", total - len(outputs))
    print("Per-class option counts:", {k:len(v) for k,v in class_sets.items()})
    assert all(w[4] == w[5] == "///" for w in outputs)
    layout = ("IAB", "CDE", "FGH")
    fixed = tuple(
        tuple("".join(
            (next(iter(signs)) if len(signs) == 1 else "?")
            for char in row
            for signs in [{out["ABCDEFGHI".index(char)][quarter]
                           for out in outputs}]
        ) for row in layout)
        for quarter in range(3)
    )
    if not args.allow_primary_dots:
        assert fixed == (("/?/", "-//", "/?-"),
                         ("??/", "///", "/?-"),
                         ("/?-", "??/", "/?/"))
        assert sum(row.count("?") for quarter in fixed for row in quarter) == 9
    print("Forced/unknown 3x3 quarter masks in physical IAB/CDE/FGH layout:")
    for quarter, rows in enumerate(fixed):
        print("quarter", quarter, *rows, sep=" | ")
    if args.out_json:
        from conjecture_lab_native_q4_receiver import ROOT
        raw_source = (ROOT / "data/observations.csv").read_bytes()
        payload = {
            "schema": "inside-ce-native-q4-mask-bank-v1",
            "research_mode": "DISCOVER / conditional",
            "observation_csv_sha256": hashlib.sha256(raw_source).hexdigest(),
            "observed_unique_residues": 66,
            "assumed_primary_alphabet": primary_alphabet,
            "layout_rows": list(layout),
            "fixed_masks": [list(rows) for rows in fixed],
            "q4_depth_options": [list(s) for s in choices],
            "output_count": len(outputs),
            "outputs": [
                {
                    "class_symbols_A_to_I": list(words),
                    "physical_3x3_by_quarter": [
                        ["".join(words["ABCDEFGHI".index(char)][q] for char in row)
                         for row in layout]
                        for q in range(3)
                    ],
                }
                for words in outputs
            ],
        }
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(payload, indent=2) + "\n")
        print("Wrote exact conditional output bank:", args.out_json)

    rows = alphabetic_counts(outputs)
    expected = (
        (("./-", 5464, 5808), (".-/", 0, 5808),
         ("/.-", 5464, 0), ("/-.", 5808, 0),
         ("-./", 0, 5464), ("-/.", 5808, 5464))
        if args.allow_primary_dots else
        (("./-", 320, 364), (".-/", 0, 364),
         ("/.-", 320, 0), ("/-.", 364, 0),
         ("-./", 0, 320), ("-/.", 364, 320))
    )
    assert rows == expected, (rows, expected)
    print("Trit digit 0/1/2 | A=0 nine-letter outputs | A=1 nine-letter outputs")
    for digits, a0, a1 in rows:
        print(digits, a0, a1, sep=" | ")
    print("Every viable direct nine-character mapping has positions E and F equal.")
    print("If a global ternary map is used, /// codes as 0, 13 or 26.")
    print("These are model-conditioned counts, not candidate credentials.")


if __name__ == "__main__":
    main()

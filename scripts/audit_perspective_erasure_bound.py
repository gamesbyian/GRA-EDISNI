#!/usr/bin/env python3
"""Exact erasure identifiability boundary from physically observed CE stickers.

Only the observed 108-repeat and provisional 81/27 two-symbol sector grammar
are assumed. No POS3, selector, error-correcting or semantic grammar is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data/observations.csv"


def audit(path: Path) -> dict:
    records = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    marks = defaultdict(set)
    for r in records:
        serial, res, symbol = int(r["serial"]), int(r["residue"]), r["symbol"]
        assert (serial - 1) % 108 + 1 == res
        marks[res].add(symbol)
    assert all(len(v) == 1 for v in marks.values()), "physical repeat contradiction"
    body_known = {k: next(iter(v)) for k, v in marks.items() if k <= 81}
    tail_known = {k: next(iter(v)) for k, v in marks.items() if k > 81}
    assert all(v in "/-" for v in body_known.values())
    assert all(v in "/." for v in tail_known.values())
    body_missing = [x for x in range(1, 82) if x not in body_known]
    tail_missing = [x for x in range(82, 109) if x not in tail_known]
    unseen = len(body_missing) + len(tail_missing)
    # Product-of-choices proof: each unseen site has exactly two available
    # symbols in this *minimal conditional* 81/27 sector grammar.
    return {
        "mode": "DEVELOP_exact_observation_only_erasure_lower_bound",
        "physical_records": len(records),
        "known_distinct_residues": len(marks),
        "known_body": len(body_known),
        "known_tail": len(tail_known),
        "missing_body": body_missing,
        "missing_tail": tail_missing,
        "all_missing_count": unseen,
        "zone_conditional_possible_full_foregrounds": 2 ** unseen,
        "three_symbol_no_zone_possible_full_foregrounds": 3 ** unseen,
        "zone_conditional_symbol_ranges": {
            "body_slash": [
                sum(v == "/" for v in body_known.values()),
                sum(v == "/" for v in body_known.values()) + len(body_missing),
            ],
            "tail_slash": [
                sum(v == "/" for v in tail_known.values()),
                sum(v == "/" for v in tail_known.values()) + len(tail_missing),
            ],
        },
        "unforced_sites_under_this_grammar": body_missing + tail_missing,
        "full_word_forced": unseen == 0,
        "scope": "Counts distinct 108-cell assignments consistent with directly "
                 "observed glyphs and *conditional* binary 81/27 sectors only; "
                 "no model-relative or semantic completion is promoted.",
    }


def self_test() -> None:
    # Tiny independent cardinality oracle for freely varying binary erased sites.
    possible = {(a, b) for a in "/-" for b in "/."}
    assert len(possible) == 2 ** 2 == 4


def check_golden(a: dict) -> None:
    assert (a["physical_records"], a["known_distinct_residues"]) == (84, 66)
    assert (a["known_body"], a["known_tail"]) == (54, 12)
    assert (len(a["missing_body"]), len(a["missing_tail"])) == (27, 15)
    assert a["zone_conditional_possible_full_foregrounds"] == 4398046511104
    assert a["zone_conditional_symbol_ranges"] == {
        "body_slash": [32, 59], "tail_slash": [4, 19]}
    assert not a["full_word_forced"]
    assert len(set(a["unforced_sites_under_this_grammar"])) == 42


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    self_test()
    a = audit(OBS)
    if args.check:
        check_golden(a)
        print("PASS PX-08 minimal zoned erasure bound: 27+15 unknown, 2^42 full candidate foregrounds.")
    if args.json or not args.check:
        print(json.dumps(a, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

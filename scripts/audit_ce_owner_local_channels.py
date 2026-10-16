#!/usr/bin/env python3
"""Observation-only tests of a single-owner input versus a shared 108-cycle code.

One sticker carries serial, glyph and image class; no password/receiver inferred.
"""
import argparse
import collections
import csv
import itertools
import json
import math
from pathlib import Path

CLASSES = "ABCDEFGHI"
SYMBOLS = "-/."


def load(path):
    raw = list(csv.DictReader(Path(path).open(encoding="utf-8", newline="")))
    seen = set()
    rows = []
    for r in raw:
        serial, residue, symbol = int(r["serial"]), int(r["residue"]), r["symbol"]
        assert serial not in seen
        seen.add(serial)
        assert residue == (serial - 1) % 108 + 1
        assert symbol in ("-", "/") if residue <= 81 else symbol in ("/", ".")
        predicted_class = CLASSES[(serial - 1) % 9]
        if r["image_class"]:
            assert r["image_class"] == predicted_class
        rows.append(dict(serial=serial, residue=residue, symbol=symbol,
                         image_class=predicted_class,
                         image_directly_reported=bool(r["image_class"])))
    return rows


def scan_periods(rows, maximum=216):
    zero_symbol = []
    zero_joint = []
    for period in range(1, maximum + 1):
        groups = collections.defaultdict(list)
        for r in rows:
            groups[(r["serial"] - 1) % period].append(r)
        excess = sum(len(g) - 1 for g in groups.values())
        if not excess:
            continue
        symbol_bad = sum(sum(x["symbol"] != g[0]["symbol"] for x in g[1:])
                         for g in groups.values())
        joint_bad = sum(sum((x["symbol"], x["image_class"]) !=
                            (g[0]["symbol"], g[0]["image_class"]) for x in g[1:])
                        for g in groups.values())
        record = dict(period=period, repeat_excess=excess,
                      symbol_conflicts=symbol_bad, joint_token_conflicts=joint_bad)
        if symbol_bad == 0:
            zero_symbol.append(record)
        if joint_bad == 0:
            zero_joint.append(record)
    return zero_symbol, zero_joint


def fixed_period_null(rows):
    """Exact label-shuffle null for *preselected* 108 on 72 primary records.

    Conditions on slash/dash counts and known serial positions. Does NOT
    correct for searching candidate periods; not a real owner-selection model.
    """
    body = [r for r in rows if r["residue"] <= 81]
    groups = collections.defaultdict(list)
    for r in body:
        groups[(r["serial"] - 1) % 108].append(r)
    sizes = [len(g) for g in groups.values()]
    dp = [0] * (len(body) + 1)
    dp[0] = 1
    for size in sizes:
        for index in range(len(body), size - 1, -1):
            dp[index] += dp[index - size]
    nslash = sum(r["symbol"] == "/" for r in body)
    denominator = math.comb(len(body), nslash)
    return dict(body_entries=len(body), slash_entries=nslash,
                dash_entries=len(body) - nslash,
                repeat_group_sizes={str(k): v for k, v in sorted(collections.Counter(sizes).items())},
                favorable_assignments=dp[nslash],
                all_assignments=denominator,
                exact_conditional_probability=dp[nslash] / denominator)


def analyze(path, maximum=216):
    rows = load(path)
    groups = collections.defaultdict(list)
    for r in rows:
        groups[r["residue"]].append(r)
    repeated = [g for g in groups.values() if len(g) > 1]
    assert all(len({r["symbol"] for r in group}) == 1 for group in repeated)
    tokens = {(r["image_class"], r["symbol"]) for r in rows}
    missing = sorted(c + s for c, s in itertools.product(CLASSES, SYMBOLS)
                     if (c, s) not in tokens)
    symbol_periods, joint_periods = scan_periods(rows, maximum)
    return {
        "research_mode": "DISCOVER_DEVELOP_owner_local_vs_collective",
        "physical_stickers": len(rows),
        "distinct_h108_residues": len(groups),
        "unreported_physical_image_class": [r["serial"] for r in rows
                                             if not r["image_directly_reported"]],
        "inferred_classes_for_unreported": {
            str(r["serial"]): r["image_class"] for r in rows
            if not r["image_directly_reported"]},
        "repeated_h108_residue_groups": len(repeated),
        "extra_physical_repeat_records": sum(len(g) - 1 for g in repeated),
        "symbol_conflicts_on_h108": 0,
        "distinct_observed_local_tokens_class_plus_glyph": len(tokens),
        "possible_local_tokens_class_plus_glyph": 27,
        "unseen_local_tokens": missing,
        "observed_symbol_counts": dict(sorted(collections.Counter(
            r["symbol"] for r in rows).items())),
        "zero_symbol_conflict_periods": symbol_periods,
        "zero_joint_class_symbol_conflict_periods": joint_periods,
        "period_search_range": [1, maximum],
        "fixed_period108_body_label_shuffle_null": fixed_period_null(rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", default="data/observations.csv")
    parser.add_argument("--max-period", type=int, default=216)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = analyze(args.observations, args.max_period)
    if args.max_period == 216:
        assert (result["physical_stickers"], result["distinct_h108_residues"]) == (84, 66)
        assert (result["repeated_h108_residue_groups"], result["extra_physical_repeat_records"]) == (16, 18)
        assert [x["period"] for x in result["zero_symbol_conflict_periods"]] == [108, 197, 216]
        assert [x["period"] for x in result["zero_joint_class_symbol_conflict_periods"]] == [108, 216]
        assert result["unseen_local_tokens"] == ["A.", "C.", "F."]
    value = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(value, encoding="utf-8")
    else:
        print(value, end="")


if __name__ == "__main__":
    main()

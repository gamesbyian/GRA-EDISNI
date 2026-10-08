#!/usr/bin/env python3
"""Conjecture Lab CL-01/CL-02 second-pass counterfactual controls.

CL-01 asks whether the 9-bit class-address idea can directly index
74 preserved Terminal41 routes without *any* completion grammar.

CL-02 adopts another unproved conjecture: Q4 one-slash depths are
balanced 3/3/3 across three positions; compares with the existing
conditional physical-column / selected-surface / row-exception families.

Neither assumption is presented as an independently justified decoder.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path

from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, primary_columns, q4_choices,
    make_master, simple_row_exception, selected_columns,
)

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHI"


def raw_address_bounds(observed, reverse, slash_bit):
    """All unknown primary foregrounds unconstrained binary wildcards."""
    rows = []
    for j, letter in enumerate(LETTERS):
        marks = [observed.get(1 + 9*f + j, "?") for f in range(9)]
        bits = marks[::-1] if reverse else marks
        low = high = 0
        for mark in bits:
            low = low * 2 + (
                0 if mark == "?" else
                (slash_bit if mark == "/" else 1-slash_bit)
            )
            high = high * 2 + (
                1 if mark == "?" else
                (slash_bit if mark == "/" else 1-slash_bit)
            )
        rows.append({
            "class": letter,
            "original_mask": "".join(marks),
            "observed_marks": 9 - marks.count("?"),
            "min": low,
            "max": high,
            "incompatible_with_74_zero_based": low >= 74,
        })
    strongest = max(row["min"] for row in rows)
    return {
        "direction": "reverse" if reverse else "forward",
        "slash_bit": slash_bit,
        "minimum_required_zero_based_entries": strongest + 1,
        "classes_attaining_bound": [row["class"] for row in rows
                                     if row["min"] == strongest],
        "classes_already_above_74": [row["class"] for row in rows
                                    if row["incompatible_with_74_zero_based"]],
        "per_class": rows,
    }


def balance_probe(observed):
    frame_choices = [
        [f for f in primary_frame_choices(observed, idx)
         if primary_columns(f)]
        for idx in range(9)
    ]
    bodies = list(product(*frame_choices))
    depth_codes = list(product(*q4_choices(observed)))
    assert len(bodies) == 18 and len(depth_codes) == 18

    groups = Counter()
    depth_balance_codes = set()
    selected_balanced = []
    for d in depth_codes:
        depth_counts = Counter(d)
        balanced = all(depth_counts[x] == 3 for x in (0, 1, 2))
        if balanced:
            depth_balance_codes.add("".join(map(str, d)))
        for frames in bodies:
            m = make_master(frames, d)
            selected = selected_columns(m, d)
            row = simple_row_exception(m, d)
            groups["all"] += 1
            if selected:
                groups["selected"] += 1
            if row:
                groups["row"] += 1
            if row and selected:
                groups["both"] += 1
            if balanced:
                groups["balanced"] += 1
                if row:
                    groups["row_balanced"] += 1
                if selected:
                    groups["selected_balanced"] += 1
                    selected_balanced.append((m, d))
                if selected and row:
                    groups["both_balanced"] += 1

    assert groups == {
        "all": 324, "balanced": 36, "selected": 12,
        "selected_balanced": 2, "row": 108,
        "row_balanced": 0, "both": 6, "both_balanced": 0,
    }, groups
    assert sorted(depth_balance_codes) == [
        "021101022", "120101022"
    ]
    assert len(selected_balanced) == 2
    assert {"".join(map(str, d)) for _, d in selected_balanced} == {
        "120101022"
    }
    exact_differences = [
        residue for residue in range(1, 109)
        if selected_balanced[0][0][residue-1] !=
           selected_balanced[1][0][residue-1]
    ]
    assert exact_differences == [22, 25]

    readouts = set()
    for m, d in selected_balanced:
        readouts.add(tuple(
            "".join(m[27*q + 9*d[j] + j] for j in range(9))
            for q in range(3)
        ))
    assert readouts == {(
        "-/-////-/", "-//////--", "/--///-//"
    )}
    conditional_predictions = {
        str(residue): selected_balanced[0][0][residue-1]
        for residue in range(1, 109)
        if residue not in observed and
        all(m[residue-1] == selected_balanced[0][0][residue-1]
            for m, _ in selected_balanced)
    }
    return {
        "assumption": "Exactly three of nine Q4 slash selectors on each of three depths (3/3/3)",
        "status": "EXPLORATORY, selected after seeing corpus; not evidence of intended balance",
        "tail_one_slash_codes": len(depth_codes),
        "balanced_codes": sorted(depth_balance_codes),
        "family_intersections": dict(groups),
        "selected_balanced_code": "120101022",
        "selected_balanced_survivors": len(selected_balanced),
        "survivor_differences": exact_differences,
        "common_selected_readout": next(iter(readouts)),
        "selected_balanced_unobserved_predictions": conditional_predictions,
        "warning": (
            "Balance is an invented criterion, not a physical fact. "
            "The one-dash selected-surface family is a conditional model. "
            "Rejecting the simple row-exception intersection does not "
            "reject every possible row selector."
        ),
    }


def run():
    n, observed = observations()
    assert n == 84 and len(observed) == 66
    with (ROOT / "data/terminal41-source-tree.json").open(
        encoding="utf8"
    ) as source:
        inventory = json.load(source)
    assert inventory["count"] == len(inventory["files"]) == 74
    addr = [
        raw_address_bounds(observed, rev, slash_bit)
        for rev, slash_bit in product((False, True), (1, 0))
    ]
    assert [
        s["minimum_required_zero_based_entries"] for s in addr
    ] == [383, 454, 467, 328]
    assert all(s["minimum_required_zero_based_entries"] > 74 for s in addr)

    return {
        "mode": "DISCOVER/DEVELOP, not VALIDATE",
        "physical_records": n,
        "unique_residues": len(observed),
        "unknown_residues": 108 - len(observed),
        "CL01_raw_only_address_bound": {
            "source_inventory_size": inventory["count"],
            "schemes": addr,
            "scope": (
                "The directly observed bits alone reject the four "
                "unmodified zero-based direct nine-bit lookup methods "
                "against a list of 74 entries. Does not reject a bigger "
                "historical table, modulo/offset/keyed decoder or "
                "different class grouping."
            ),
        },
        "CL02_tail_balance_counterfactual": balance_probe(observed),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

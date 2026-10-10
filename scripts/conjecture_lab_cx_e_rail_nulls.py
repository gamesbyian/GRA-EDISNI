#!/usr/bin/env python3
"""CX-E observed-only 4x27 slash rails and two EXACT conditional nulls.

A: shuffle labels independently within observed cells of each quarter;
   preserve quarter slash totals and the observation mask.
B: body 3x3 frames each have one minority per vertical three-cell stack,
   with either polarity, conditioning on observed-site slash counts per
   frame; tail has exactly one slash per image class across its three
   occurrences, conditioning on three tail-row observed-site slash counts.

Both models are retrospective calibrations, NOT significance tests for a
predeclared decoding clue. They do not impute unknown H108 observations.
"""
import argparse
import csv
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    marks = {}
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for r in csv.DictReader(stream):
            n, mark = int(r["residue"]), r["symbol"].strip()
            assert 1 <= n <= 108 and mark in ("/", "-", ".")
            assert n not in marks or marks[n] == mark
            marks[n] = mark
    return marks


def falling(n, k):
    out = 1
    for i in range(k):
        out *= n - i
    return out if k <= n else 0


def quarter_shuffle_null(q, cols):
    """Exact inclusion-exclusion P(at least 2 all-slash columns)."""
    moments = {}
    probability = Fraction(0)
    for k in range(1, len(cols) + 1):
        event = Fraction(1)
        for row in q:
            observed = [x for x in row if x != "?"]
            event *= Fraction(falling(observed.count("/"), k),
                              falling(len(observed), k))
        moments[k] = event
        if k >= 2:
            probability += (-1)**k * (k - 1) * comb(len(cols), k) * event
    return probability, moments


def body_frame_options(observed):
    options = []
    for minority in ("/", "-"):
        for where in product(range(3), repeat=3):
            cells = ["-" if minority == "/" else "/"] * 9
            for column, row in enumerate(where):
                cells[3 * row + column] = minority
            if sum(cells[i] == "/" for i, x in enumerate(observed)
                   if x != "?") == observed.count("/"):
                options.append(cells)
    assert options, "Conditional body grammar has no matched options"
    return options


def typed_grammar_null(q, cols):
    """Exact 32-state DP with nine body frames and enumerated Q4 tail."""
    allbits = (1 << len(cols)) - 1
    masses = [Fraction(0)] * (1 << len(cols))
    masses[allbits] = Fraction(1)
    body_option_counts = []
    for quarter in range(3):
        for frame in range(3):
            seen = q[quarter][9*frame:9*(frame+1)]
            opts = body_frame_options(seen)
            body_option_counts.append(len(opts))
            option_masks = []
            for cells in opts:
                mask = allbits
                for j, column in enumerate(cols):
                    if (column - 1)//9 == frame and cells[(column - 1)%9] != "/":
                        mask &= ~(1 << j)
                option_masks.append(mask)
            nxt = [Fraction(0)] * (1 << len(cols))
            for mask, mass in enumerate(masses):
                if mass:
                    for allowed in option_masks:
                        nxt[mask & allowed] += mass / len(opts)
            masses = nxt

    tail_rows = [q[3][9*j:9*(j+1)] for j in range(3)]
    counts = [row.count("/") for row in tail_rows]
    tail_masks = Counter()
    for assignment in product(range(3), repeat=9):
        # One slash in the three Q4 rows for each of nine picture classes.
        seen_slashes = [0, 0, 0]
        for cls, row in enumerate(assignment):
            if tail_rows[row][cls] != "?":
                seen_slashes[row] += 1
        if seen_slashes != counts:
            continue
        mask = allbits
        for j, col in enumerate(cols):
            if assignment[(col - 1)%9] != (col - 1)//9:
                mask &= ~(1 << j)
        tail_masks[mask] += 1
    total = sum(tail_masks.values())
    assert total, "Conditional tail grammar has no matched options"
    final = [Fraction(0)] * (1 << len(cols))
    for mask, mass in enumerate(masses):
        for tailmask, count in tail_masks.items():
            final[mask & tailmask] += mass * Fraction(count, total)
    assert sum(final) == 1
    return (sum(p for mask, p in enumerate(final) if mask.bit_count() >= 2),
            final, body_option_counts, total)


def run(path):
    marks = load(path)
    quarters = [[marks.get(27*q + j + 1, "?") for j in range(27)]
                for q in range(4)]
    full = [j+1 for j in range(27) if all(row[j] != "?" for row in quarters)]
    rails = [j for j in full if all(row[j-1] == "/" for row in quarters)]
    simple, moments = quarter_shuffle_null(quarters, full)
    conditional, states, frame_counts, tail_count = typed_grammar_null(quarters, full)
    pairmask = sum(1 << full.index(col) for col in rails) if len(rails) == 2 else None
    return {
        "classification": "retrospective exploratory: no preregistered significance",
        "observed_unique_residues": len(marks), "unknown_residues": 108 - len(marks),
        "four_quarters_27_each": ["".join(row) for row in quarters],
        "quarter_observed_slash_counts": [
            [sum(x != "?" for x in row), row.count("/")] for row in quarters],
        "fully_observed_columns_1_based": full,
        "all_slash_columns_1_based": rails,
        "quarter_shuffle_any_two": float(simple),
        "quarter_shuffle_named_pair": float(moments[2]) if pairmask is not None else None,
        "typed_grammar_any_two": float(conditional),
        "typed_grammar_named_pair": float(sum(p for m, p in enumerate(states)
                      if pairmask is not None and (m & pairmask) == pairmask))
                      if pairmask is not None else None,
        "body_frame_options": frame_counts,
        "tail_options_after_row_census": tail_count,
        "note": "All comparisons keep observation mask/counts fixed. The typed grammar is conjectural; a post-hoc pair probability is not independent evidence."
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--observations", type=Path, default=ROOT/"data/observations.csv")
    args = p.parse_args()
    print(json.dumps(run(args.observations), indent=2))

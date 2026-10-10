#!/usr/bin/env python3
"""CX-E2: speculate that slash rails at columns 5 and 15 delimit 4/9/12.

Conditional on treating the nine internal marks as one A-I cycle, place
each quarter's nine cells on the physically known IAB/CDE/FGH grid.
Enumerate a short alternative grammar: exactly one minority mark in
each physical ROW of that grid (polarity uniform within a quarter).
All H108 unknowns remain unknown in the input. Predictions are
after-data conjectures; only later independent symbols can test them.
"""
import argparse
import csv
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = "FGHIABCDE"
PHYSICAL = ("IAB", "CDE", "FGH")


def load(path):
    marks = {}
    with Path(path).open(newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            res = int(row["residue"])
            sym = row["symbol"].strip()
            assert 1 <= res <= 108 and sym in "/-."
            assert row.get("image_class", "").strip() in ("", "ABCDEFGHI"[(res-1)%9])
            assert res not in marks or marks[res] == sym
            marks[res] = sym
    return marks


def three_by_three_options(source_grid, symbols, axis):
    """Generate all 2 * 3**3 one-minority-per-row/column patterns."""
    output = []
    for minority in symbols:
        majority = symbols.replace(minority, "")
        assert len(majority) == 1
        for pos in product(range(3), repeat=3):
            g = [[majority]*3 for _ in range(3)]
            for j, choice in enumerate(pos):
                if axis == "row":
                    g[j][choice] = minority
                else:
                    g[choice][j] = minority
            if all(source_grid[r][c] in ("?", g[r][c])
                   for r in range(3) for c in range(3)):
                output.append((minority, g))
    return output


def prior_frame_choices(marks, res):
    """Existing *conditional* 9-sticker frame grammar or Q4 class tail."""
    if res >= 82:
        cls = (res - 82) % 9
        ids = [82+cls, 91+cls, 100+cls]
        return sorted(set(vals[ids.index(res)] for which in range(3)
            for vals in [["/" if i == which else "." for i in range(3)]]
            if all(marks.get(n, v) == v for n, v in zip(ids, vals))))
    frame = (res-1)//9
    pos = (res-1)%9
    out = set()
    for minority in "/-":
        majority = "-" if minority == "/" else "/"
        for row_choices in product(range(3), repeat=3):
            cells = [majority]*9
            for column, row in enumerate(row_choices):
                cells[column+3*row] = minority
            if all(marks.get(frame*9+j+1, v) == v for j,v in enumerate(cells)):
                out.add(cells[pos])
    return sorted(out)


def nine_site_window_control(marks):
    """All 19 possible contiguous nine-site fields within each quarter.

    Each naturally covers all A-I classes because serial image classes
    repeat every nine; this is not special to the rail-selected window.
    """
    out = []
    for start in range(1, 20):
        counts = []
        for q in range(4):
            by_class = {
                "ABCDEFGHI"[(27*q + start + j - 1) % 9]:
                marks.get(27*q + start + j, "?")
                for j in range(9)}
            grid = [[by_class[c] for c in line] for line in PHYSICAL]
            counts.append(len(three_by_three_options(
                grid, "/." if q == 3 else "/-", "row")))
        total = 1
        for n in counts:
            total *= n
        out.append({"first_column": start, "last_column": start+8,
                    "quarter_option_counts": counts, "joint_completions": total})
    return out


def run(path):
    marks = load(path)
    quarters = [[marks.get(27*q+j+1, "?") for j in range(27)] for q in range(4)]
    rails = [j+1 for j in range(27) if all(row[j] == "/" for row in quarters)]
    assert 5 in rails and 15 in rails, "Observed separator premise changed"
    result = []
    all_forced = {}
    compatible_total = 1
    for q, row in enumerate(quarters):
        mid = row[5:14]
        class_to = dict(zip(ORDER, mid))
        class_to_res = dict(zip(ORDER, range(27*q+6, 27*q+15)))
        grid = [[class_to[c] for c in s] for s in PHYSICAL]
        opts = three_by_three_options(grid, "/." if q == 3 else "/-", "row")
        column_opts = three_by_three_options(grid, "/." if q == 3 else "/-", "column")
        compatible_total *= len(opts)
        forced = {}
        for r in range(3):
            for c in range(3):
                cls = PHYSICAL[r][c]
                res = class_to_res[cls]
                values = {g[r][c] for _,g in opts}
                if res not in marks and len(values) == 1:
                    forced[res] = next(iter(values))
                    all_forced[res] = forced[res]
        result.append({
            "quarter": q+1,
            "prefix_4": "".join(row[:4]),
            "rail_E": row[4],
            "middle_9_class_order": ORDER,
            "middle_9_symbols": "".join(mid),
            "middle_9_physical_grid": ["".join(x) for x in grid],
            "rail_F": row[14],
            "suffix_12": "".join(row[15:]),
            "one_minority_per_physical_row_completions": len(opts),
            "row_rule_minority_polarities": sorted({p for p,_ in opts}),
            "one_minority_per_physical_column_completions": len(column_opts),
            "new_row_rule_forced_symbols": {str(k):v for k,v in sorted(forced.items())}
        })
    windows = nine_site_window_control(marks)
    comparator = []
    for res, val in sorted(all_forced.items()):
        prior = prior_frame_choices(marks, res)
        comparator.append({
            "residue": res, "image_class": "ABCDEFGHI"[(res-1)%9],
            "cx_e2_row_forecast": val,
            "separate_frame_grammar_allowed": prior,
            "mutually_incompatible": val not in prior
        })
    return {
        "status": "DEVELOP, frozen from 66 observed H108 residues; not validation",
        "rail_positions_1_based": [5,15],
        "one_full_class_cycle_between_rails": ORDER,
        "total_row_rule_middle_field_completions": compatible_total,
        "quarters": result,
        "frozen_conditional_forecasts": comparator,
        "window_look_elsewhere": {
            "n_tested": len(windows),
            "n_all_four_quarters_survive": sum(x["joint_completions"] > 0 for x in windows),
            "surviving_windows": [x for x in windows if x["joint_completions"] > 0]},
        "original_frame_grammar_is_only_a_rival_hypothesis": True
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--observations", type=Path, default=ROOT/"data/observations.csv")
    args = p.parse_args()
    print(json.dumps(run(args.observations), indent=2))

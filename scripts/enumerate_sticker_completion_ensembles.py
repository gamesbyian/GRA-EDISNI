#!/usr/bin/env python3
"""Exact, observation-anchored sticker completion ensemble.

Three nested H108 foreground completion classes:
  A: 3-of-9 minority per each of the first nine frames (either polarity);
     one slash along each Q4 A-I depth stack.
  B: A plus exactly one minority per physical column of every primary frame.
  C: A plus each Q4-selected primary 3x3 surface has exactly one dash
     per physical column; report both A∩C and A∩B∩C.

No generated machine completions, plaintext scoring, or knowledge of the
incumbent transducer is used. These are conditional, not probabilistic.
"""
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHI"
PHYSICAL = ("IAB", "CDE", "FGH")
COLS = tuple(tuple(LETTERS.index(PHYSICAL[row][col]) for row in range(3))
             for col in range(3))


def observations():
    observed = {}
    records = 0
    with (ROOT / "data/observations.csv").open(newline="", encoding="utf8") as fh:
        for item in csv.DictReader(fh):
            records += 1
            r = int(item["residue"])
            value = item["symbol"]
            assert 1 <= r <= 108 and value in ("/", "-", ".")
            assert r not in observed or observed[r] == value
            observed[r] = value
    return records, observed


def primary_frame_choices(observed, frame):
    output = []
    for positions in itertools.combinations(range(9), 3):
        for minority in "/-":
            majority = "-" if minority == "/" else "/"
            cells = tuple(minority if j in positions else majority
                          for j in range(9))
            if all(observed.get(1 + 9*frame + j, cells[j]) == cells[j]
                   for j in range(9)):
                output.append(cells)
    return output


def q4_choices(observed):
    choices = []
    for j in range(9):
        depth_choices = []
        for selected in range(3):
            if all(observed.get(82 + 9*d + j,
                                "/" if d == selected else ".")
                   == ("/" if d == selected else ".")
                   for d in range(3)):
                depth_choices.append(selected)
        choices.append(depth_choices)
    return choices


def primary_columns(frame):
    # Exactly one occurrence of the MINORITY symbol in each column.
    # A 3-of-9 frame has a unique minority; this tests its distribution.
    for col in COLS:
        count_slash = sum(frame[j] == "/" for j in col)
        if count_slash not in (1, 2):
            return False
    return True


def simple_row_exception(master, depths):
    # The selected quarter contains exactly one minority symbol across depths.
    for j, selected_q in enumerate(depths):
        slash = sum(master[27*selected_q + 9*d + j] == "/" for d in range(3))
        if slash not in (1, 2):
            return False
    return True


def make_master(frames, depths):
    symbols = tuple(itertools.chain.from_iterable(frames))
    tail = tuple("/" if d == depths[j] else "."
                 for d in range(3) for j in range(9))
    return symbols + tail


def selected_columns(master, depths):
    for q in range(3):
        surface = tuple(master[27*q + 9*depths[j] + j]
                        for j in range(9))
        for col in COLS:
            if sum(surface[j] == "-" for j in col) != 1:
                return False
    return True


def invariant_summary(masters):
    if not masters:
        return {"masters": 0, "invariants": 0, "variable_residues": []}
    variable = [r for r in range(1, 109)
                if len({master[r-1] for master in masters}) > 1]
    return {"masters": len(masters), "invariants": 108 - len(variable),
            "variable_residues": variable}


def primary_neighbour_matches(master):
    # Primary cubes only, to avoid the known alphabet shift at Q4.
    xy = depth = 0
    for q in range(3):
        for d in range(3):
            start = 27*q + 9*d
            for row in range(3):
                for c in range(2):
                    xy += (master[start+COLS[c][row]]
                           == master[start+COLS[c+1][row]])
            for c in range(3):
                for row in range(2):
                    xy += (master[start+COLS[c][row]]
                           == master[start+COLS[c][row+1]])
        for j in range(9):
            for d in range(2):
                depth += (master[27*q+9*d+j]
                          == master[27*q+9*(d+1)+j])
    # XY: 108 edges (three quarters * three layers * 12)
    # Z: 54 edges (three quarters * nine columns * two depth gaps)
    return xy, depth


def main():
    records, observed = observations()
    assert records == 84 and len(observed) == 66, (
        "Corpus changed: re-audit the family counts before updating assertions")
    primary = [primary_frame_choices(observed, f) for f in range(9)]
    tail = q4_choices(observed)
    assert all(primary) and all(tail)
    tail_codes = list(itertools.product(*tail))

    counts = Counter()
    column_masters = []
    selected_masters = []
    column_selected_masters = []
    selected_depth_patterns = Counter()
    for frames in itertools.product(*primary):
        valid_columns = all(primary_columns(frame) for frame in frames)
        for depths in tail_codes:
            master = make_master(frames, depths)
            assert all(master[r-1] == v for r, v in observed.items())
            counts["all"] += 1
            if valid_columns:
                counts["column"] += 1
                column_masters.append(master)
            row_ok = simple_row_exception(master, depths)
            if row_ok:
                counts["row_exception"] += 1
                if valid_columns:
                    counts["column_row_exception"] += 1
            if selected_columns(master, depths):
                counts["selected"] += 1
                selected_masters.append(master)
                selected_depth_patterns["".join(map(str, depths))] += 1
                if row_ok:
                    counts["row_and_selected"] += 1
                if valid_columns:
                    counts["column_selected"] += 1
                    if row_ok:
                        counts["column_row_and_selected"] += 1
                    column_selected_masters.append(master)
            if Counter(master) == Counter({"/": 54, "-": 36, ".": 18}):
                counts["census_54_36_18"] += 1

    assert counts == {
        "all": 233280, "column": 324, "selected": 4528,
        "column_selected": 12, "census_54_36_18": 116640,
        "row_exception": 62640, "column_row_exception": 108,
        "row_and_selected": 1656, "column_row_and_selected": 6
    }, counts

    def neighbour_summary(masters):
        edges = [primary_neighbour_matches(m) for m in masters]
        return {
            "xy_edges_total": 108, "z_edges_total": 54,
            "xy_matches_min": min(x for x, _ in edges),
            "xy_matches_max": max(x for x, _ in edges),
            "z_matches_min": min(z for _, z in edges),
            "z_matches_max": max(z for _, z in edges),
            "xy_matches_histogram": dict(sorted(Counter(x for x, _ in edges).items())),
            "z_matches_histogram": dict(sorted(Counter(z for _, z in edges).items()))
        }

    result = {
        "physical_records": records,
        "observed_unique_residues": len(observed),
        "unobserved_residues": 108-len(observed),
        "primary_frame_candidate_counts": [len(o) for o in primary],
        "q4_depth_choices": dict(zip(LETTERS, tail)),
        "q4_tail_codes": len(tail_codes),
        "family_counts": dict(counts),
        "column_family": invariant_summary(column_masters),
        "column_selected_family": invariant_summary(column_selected_masters),
        "column_primary_3d_neighbours": neighbour_summary(column_masters),
        "column_selected_primary_3d_neighbours": neighbour_summary(column_selected_masters),
        "selected_depth_patterns": dict(sorted(selected_depth_patterns.items())),
        "limits": [
            "exact enumeration is conditional on chosen structural rules",
            "A∩B∩C is a slice of the incumbent selector grammar, not independent confirmation",
            "retrospectively learned rules cannot be scored as preregistered predictive evidence",
            "3D visual pattern searches need independent operation cues and matched nulls",
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

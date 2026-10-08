#!/usr/bin/env python3
"""Experiment 435: fair depth-axis vs quarter-axis Q4 selector consumers.

The physical sticker data supplies Q=0,1,2 primary quarters, d=0,1,2
depths and j=A-I foreground positions. Tail slash position S(j) has native
depth type. Compare identical one-dash-per-physical-column constraints:

  depth:   across all Q=0,1,2, read (Q, d=pi[S(j)], j)
  quarter: across all d=0,1,2, read (Q=pi[S(j)], d, j)

pi ranges over six globally shared coordinate relabelings. These are
alternative structural grammars, not evidence of a solved 3D puzzle.
"""
from collections import Counter
from itertools import permutations, product
from pathlib import Path
import json

from enumerate_sticker_completion_ensembles import (
    LETTERS, COLS, observations, primary_frame_choices,
    primary_columns, q4_choices, make_master,
)

PERMS = tuple(permutations(range(3)))
IDENTITY = (0, 1, 2)


def valid_axis(master, selector, axis, permutation=IDENTITY):
    for fixed in range(3):
        for col in COLS:
            dash = 0
            for j in col:
                address = permutation[selector[j]]
                if axis == "depth":
                    quarter, depth = fixed, address
                elif axis == "quarter":
                    quarter, depth = address, fixed
                else:
                    raise ValueError(axis)
                dash += master[27*quarter + 9*depth + j] == "-"
            if dash != 1:
                return False
    return True


def candidate_masters(observed, hidden_frame=None):
    frames = [
        [
            frame for frame in primary_frame_choices(
                {r:v for r,v in observed.items()
                 if hidden_frame is None or (r-1)//9 != hidden_frame}, f
            )
            if primary_columns(frame)
        ]
        for f in range(9)
    ]
    assert all(frames)
    tail_codes = tuple(product(*q4_choices(observed)))
    for primary in product(*frames):
        for selector in tail_codes:
            yield make_master(primary, selector), selector


def family_members(observed):
    results = {("depth", p): set() for p in PERMS}
    results.update({("quarter", p): set() for p in PERMS})
    for master, selector in candidate_masters(observed):
        for axis in ("depth", "quarter"):
            for perm in PERMS:
                if valid_axis(master, selector, axis, perm):
                    results[axis, perm].add(master)
    return results


def symbol_sets(masters):
    if not masters:
        return {}
    return {
        r: set(master[r-1] for master in masters)
        for r in range(1,109)
    }


def holdout_frame_summary(observed):
    totals = {
        "depth_identity": Counter(),
        "quarter_identity": Counter(),
        "quarter_any_global_relabel": Counter(),
    }
    by_frame = []
    for frame in range(9):
        withheld = {
            r:v for r,v in observed.items()
            if r <= 81 and (r-1)//9 == frame
        }
        training = {
            r:v for r,v in observed.items() if r not in withheld
        }
        memberships = {
            "depth_identity": [],
            "quarter_identity": [],
            "quarter_any_global_relabel": [],
        }
        for master, selector in candidate_masters(training):
            dep = valid_axis(master, selector, "depth", IDENTITY)
            quarter0 = valid_axis(master, selector, "quarter", IDENTITY)
            q_any = any(valid_axis(master, selector, "quarter", pi)
                        for pi in PERMS)
            if dep:
                memberships["depth_identity"].append(master)
            if quarter0:
                memberships["quarter_identity"].append(master)
            if q_any:
                memberships["quarter_any_global_relabel"].append(master)
        frame_result = {"frame":frame, "heldout_residues":sorted(withheld),
                        "families":{}}
        for name, masters in memberships.items():
            possible = {
                r:{master[r-1] for master in masters} for r in withheld
            }
            forced = {
                r:next(iter(symbols))
                for r,symbols in possible.items() if len(symbols) == 1
            }
            excluded = sorted(
                r for r,truth in withheld.items() if truth not in possible[r]
            )
            frame_result["families"][name] = {
                "surviving_masters":len(masters),
                "forced_correct":sum(withheld[r] == v for r,v in forced.items()),
                "forced_wrong":sum(withheld[r] != v for r,v in forced.items()),
                "forced_residues":sorted(forced),
                "excluded_truth_residues":excluded,
            }
            totals[name].update({
                "heldout":len(withheld),
                "forced":len(forced),
                "correct":sum(withheld[r] == v for r,v in forced.items()),
                "excluded":len(excluded),
            })
        by_frame.append(frame_result)
    assert sum(x["heldout"] for x in totals.values()) == 162
    assert totals["depth_identity"] == {
        "heldout":54,"forced":4,"correct":4,"excluded":0}
    assert totals["quarter_any_global_relabel"] == {
        "heldout":54,"forced":0,"correct":0,"excluded":0}
    return {"totals":{k:dict(v) for k,v in totals.items()},
            "by_frame":by_frame}


def main():
    physical_count, observed = observations()
    assert physical_count == 84 and len(observed) == 66
    families = family_members(observed)
    counts = {
        "%s_%s" % (axis,"".join(map(str, pi))):len(masters)
        for (axis, pi),masters in families.items()
    }
    assert {pi:len(families["depth",pi]) for pi in PERMS} == {
        (0,1,2):12,(0,2,1):0,(1,0,2):0,(1,2,0):0,
        (2,0,1):0,(2,1,0):0
    }
    assert {pi:len(families["quarter",pi]) for pi in PERMS} == {
        (0,1,2):0,(0,2,1):0,(1,0,2):0,(1,2,0):8,
        (2,0,1):0,(2,1,0):4
    }
    depth = families["depth", IDENTITY]
    quarter = set.union(*(families["quarter",pi] for pi in PERMS))
    assert len(depth) == 12 and len(quarter) == 10
    assert len(depth & quarter) == 0
    assert len(families["quarter",(1,2,0)] &
               families["quarter",(2,1,0)]) == 2

    depth_symbols = symbol_sets(depth)
    quarter_symbols = symbol_sets(quarter)
    differences = []
    for r in range(1,109):
        d,q = depth_symbols[r],quarter_symbols[r]
        if d == q:
            continue
        differences.append({
            "residue":r,
            "letter":LETTERS[(r-1)%9],
            "depth_symbols":"".join(sorted(d)),
            "quarter_symbols":"".join(sorted(q)),
            "disjoint":not bool(d & q),
            "depth_counts":dict(Counter(m[r-1] for m in depth)),
            "quarter_counts":dict(Counter(m[r-1] for m in quarter)),
        })
    assert [x["residue"] for x in differences] == [
        49,50,52,54,84,93,102
    ]
    assert [
        (x["residue"],x["depth_symbols"],x["quarter_symbols"])
        for x in differences if x["disjoint"]
    ] == [(50,"-","/"),(54,"-","/"),(93,".","/")]
    frozen = json.loads((Path(__file__).resolve().parents[1] /
                         "data/frozen-q4-axis-consumer-discriminators.json")
                        .read_text(encoding="utf8"))
    expected = [(x["residue"],x["depth"],x["quarter"])
                for x in frozen["mutually_exclusive_forecasts"]]
    actual = [(x["residue"],x["depth_symbols"],x["quarter_symbols"])
              for x in differences if x["disjoint"]]
    assert actual == expected, "Frozen physical prediction drift"

    holdout = holdout_frame_summary(observed)
    print(json.dumps({
        "physical_records":physical_count,
        "unique_observed_residues":len(observed),
        "starting_physical_column_and_tail_family":324,
        "candidate_counts_by_axis_and_shared_global_label_permutation":counts,
        "depth_identity_masters":len(depth),
        "quarter_any_label_masters":len(quarter),
        "shared_complete_masters":len(depth & quarter),
        "distinct_foreground_prediction_sets":differences,
        "three_opposite_forced_missing_residues":[50,54,93],
        "single_frame_leave_out":holdout,
        "epistemic_limits":[
            "Native tail position has type depth; mapping it to quarter adds a coordinate-type change.",
            "Satisfying a postulated one-dash-per-column output is not evidence of intended output.",
            "Global label permutations fitted to the present corpus are retrospectively selected.",
            "Correct forced holdouts are guaranteed by full-corpus survivor compatibility.",
            "The three disagreements are conditional prospective discriminators, not calibrated probabilities."
        ]
    },indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 474: demonstrate partial Q4 recovery vs full Q4 erasure.

Standard-library only. All candidate strings are generated from
canonical raw sticker observations and the same 3-of-9/physical
column and one-slash-per-depth-stack rules. No Q4 truth is used
in the all-Q4-hidden candidate family. Counts are exact.
"""
from collections import Counter
import json

from enumerate_sticker_completion_ensembles import observations
from audit_q4_axis_consumer_comparison import (
    PERMS, IDENTITY, candidate_masters, valid_axis,
)


def compatible(master, selector, axis):
    if axis == "depth":
        return valid_axis(master, selector, "depth", IDENTITY)
    if axis == "quarter":
        return any(valid_axis(master, selector, "quarter", p)
                   for p in PERMS)
    if axis == "uniform":
        return True
    raise ValueError(axis)


def score_probabilities(truth, counts, total):
    q4 = sorted(truth)
    probs = {
        r: counts[r] / total for r in q4
    }
    correct = sum(
        (probs[r] >= 0.5) == (truth[r] == "/") for r in q4
    )
    brier = sum(
        (probs[r] - (truth[r] == "/")) ** 2 for r in q4
    ) / len(q4)
    return {
        "correct": correct,
        "tested": len(q4),
        "brier": brier,
        "slash_probability_by_residue": probs,
    }


def depth_stack_erasures(observed, axis):
    q4 = {r:mark for r,mark in observed.items() if r > 81}
    slash_by_residue = Counter()
    legal_counts = []
    for j in range(9):
        target = [r for r in q4 if (r - 82) % 9 == j]
        if not target:
            continue
        training = {r:mark for r,mark in observed.items()
                    if r not in target}
        matches = Counter()
        total = 0
        for master,selector in candidate_masters(training):
            if not compatible(master, selector, axis):
                continue
            total += 1
            for r in target:
                matches[r] += master[r-1] == "/"
        assert total > 0
        legal_counts.append((j,len(target),total))
        for r in target:
            slash_by_residue[r] = matches[r] / total

    correct = sum(
        (slash_by_residue[r] >= 0.5) == (q4[r] == "/")
        for r in q4
    )
    brier = sum(
        (slash_by_residue[r] - (q4[r] == "/")) ** 2
        for r in q4
    ) / len(q4)
    return {
        "correct": correct, "tested": len(q4),
        "brier": brier,
        "stack_coverage": legal_counts,
        "slash_probability_by_residue": dict(sorted(slash_by_residue.items())),
    }


def full_q4_erasure(observed, axis):
    q4 = {r:mark for r,mark in observed.items() if r > 81}
    training = {r:mark for r,mark in observed.items() if r <= 81}
    total, pass_count = 0,0
    slash_counts = Counter()
    for master,selector in candidate_masters(training):
        total += 1
        if not compatible(master, selector, axis):
            continue
        pass_count += 1
        for r in q4:
            slash_counts[r] += master[r-1] == "/"
    assert total == 18 * 3**9 == 354294
    assert pass_count > 0
    return {
        "complete_masters_before_consumer": total,
        "complete_masters_after_consumer": pass_count,
        **score_probabilities(q4,slash_counts,pass_count),
    }


def main():
    physical,obs=observations()
    assert physical==84 and len(obs)==66
    output={}
    for axis in ("uniform","depth","quarter"):
        output[axis]={
            "erase_one_Q4_letter_stack_at_a_time":
                depth_stack_erasures(obs,axis),
            "erase_all_Q4_known_marks":
                full_q4_erasure(obs,axis),
        }
    assert [
        output[axis]["erase_one_Q4_letter_stack_at_a_time"]["correct"]
        for axis in ("uniform","depth","quarter")
    ] == [8,11,6]
    assert [
        output[axis]["erase_all_Q4_known_marks"]["correct"]
        for axis in ("uniform","depth","quarter")
    ] == [8,8,8]
    assert [
        output[axis]["erase_all_Q4_known_marks"]
            ["complete_masters_after_consumer"]
        for axis in ("uniform","depth","quarter")
    ] == [354294,948,7824]
    print(json.dumps({
        "physical_records": physical,
        "unique_residues": len(obs),
        "q4_known": sum(r>81 for r in obs),
        "results": output,
        "interpretation": (
            "One-stack erasure 11/12 for the native depth rule reflects "
            "conditioning on other known Q4 stacks; all-Q4 erasure "
            "eliminates that advantage. This does not establish nor "
            "refute a Playdead-authored Q4 instruction."
        )
    }, indent=2))


if __name__ == "__main__":
    main()

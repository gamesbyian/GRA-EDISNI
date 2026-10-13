#!/usr/bin/env python3
"""Exact selection-aware H108 class-coverage imbalance control.

With 66 of 108 distinct H108 positions observed, each of 9 A-I classes owns
12 sites. Test how surprising A+G's combined 9/24 coverage would be under
(a) a *pre-specified* pair and (b) the *post-selected two least-covered
classes*. Conditioning on 66 observed logical sites approximates uniform
physical serial sampling but does not model real acquisition/provenance.

Run: python scripts/audit_class_coverage_selection_null.py
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

from audit_finite_receiver_invariance import physical_observations, ROOT

LETTERS = "ABCDEFGHI"
SITES_PER_CLASS = 12
TOTAL_POSITIONS = 108
KNOWN_POSITIONS = 66
RESULT_PAIR = ("A", "G")
OBSERVED_PAIR_SUM = 9


def occupancy_distribution(total_observed: int, classes: int = 9,
                           capacity: int = 12) -> dict[tuple[int, int], int]:
    """Count masks by lowest and second-lowest class occupancies, exactly.

    A DP state tracks (total allocated occupied slots, smallest count,
    second-smallest count). For a class with x occupied of 12, number of
    specific subsets is C(12,x). All observations remain unordered.
    """
    dp = {(0, capacity+1, capacity+1): 1}
    for _ in range(classes):
        nxt = defaultdict(int)
        for (used, minimum, second), ways in dp.items():
            for count in range(capacity+1):
                if used + count > total_observed:
                    continue
                lo, hi = sorted((minimum, second, count))[:2]
                nxt[(used+count, lo, hi)] += ways*comb(capacity, count)
        dp = nxt
    totals = {(lo,hi): ways for (n,lo,hi),ways in dp.items()
              if n == total_observed}
    assert sum(totals.values()) == comb(classes*capacity,total_observed)
    return totals


def audit() -> dict:
    obs = physical_observations()
    class_counts = Counter(LETTERS[(r-1)%9] for r in obs)
    counts = {ch: class_counts[ch] for ch in LETTERS}
    assert counts == {
        "A":4, "B":10, "C":9, "D":7, "E":7,
        "F":8, "G":5, "H":8, "I":8,
    }
    assert sum(counts.values()) == KNOWN_POSITIONS
    # A/G are the two sparsest classes, but they were identified *after*
    # observing the same corpus and readout frontier.
    order = sorted(counts, key=lambda k:(counts[k],k))
    assert order[:2] == ["A","G"]
    assert sum(counts[x] for x in order[:2]) == OBSERVED_PAIR_SUM

    den = comb(TOTAL_POSITIONS, KNOWN_POSITIONS)
    pair_count = sum(
        comb(2*SITES_PER_CLASS, take)
        * comb(TOTAL_POSITIONS-2*SITES_PER_CLASS, KNOWN_POSITIONS-take)
        for take in range(OBSERVED_PAIR_SUM+1)
    )
    cases = occupancy_distribution(KNOWN_POSITIONS)
    post_selected_count = sum(
        ways for (min1,min2), ways in cases.items()
        if min1+min2 <= OBSERVED_PAIR_SUM
    )
    specific_probability = pair_count / den
    postselected_probability = post_selected_count / den
    assert abs(specific_probability - 0.007518815421679606) < 1e-14
    assert abs(postselected_probability - 0.1884501057910052) < 1e-14
    assert postselected_probability >= specific_probability
    # Exhaustive small independent positive control: 3 groups of 2 sites,
    # sampling 2/6, exactly 3 of 15 masks have only one occupied group.
    tiny = occupancy_distribution(total_observed=2,classes=3,capacity=2)
    assert sum(tiny.values()) == comb(6,2)
    assert sum(v for (a,b),v in tiny.items() if a+b <= 1) == 3

    return {
        "mode":"DEVELOP: exact combinatorial null, not source-authored CE coding",
        "observed_108_positions":len(obs),
        "by_image_class_A_to_I":counts,
        "postselected_sparse_classes":order[:2],
        "combined_known_of_24":OBSERVED_PAIR_SUM,
        "reference_sample":"uniform 66 occupied sites among 108, with nine 12-site classes",
        "probability_a_preregistered_AG_pair_has_9_or_fewer":specific_probability,
        "probability_any_two_sparsest_classes_have_9_or_fewer":postselected_probability,
        "ratio_postselected_to_specific":postselected_probability/specific_probability,
        "interpretation":(
            "A/G are indeed the least physically sampled classes, but "
            "choosing the two least sampled classes after inspecting the "
            "same evidence makes 9/24 coverage a ~18.85% event under this "
            "reference null. The ~0.75% fixed-A/G figure is the wrong "
            "significance report for the post-hoc observation."
        ),
        "limitations":[
            "Real owner discovery is not uniform across serials; these are reference nulls.",
            "Conditioning on 66 logical residues ignores modest 5-vs-6 physical copy multiplicities.",
            "A/G selection also arose via a fitted U5 decoder, compounding selection history.",
            "Observed class asymmetry neither validates nor refutes any receiving artifact."
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    args = p.parse_args()
    result = audit()
    payload=json.dumps(result,indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
        print(f"saved {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()

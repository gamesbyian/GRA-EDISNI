#!/usr/bin/env python3
"""Experiment 434: conditional missing-mask sensitivity of cross-cube matches.

Enumerates every 3-of-9 primary-body completion, and the subset where
each 3x3 physical column has one minority mark. The tail (Q4) is not
needed. No missing stickers or candidate completions are treated as
physical observations or drawn from calibrated probabilities.
"""
from collections import Counter
from itertools import product
import json
from enumerate_sticker_completion_ensembles import (
    LETTERS, observations, primary_frame_choices, primary_columns,
)


def primary_pairs():
    return [(27*q+i, 27*q2+i)
            for q in range(3) for q2 in range(q+1,3) for i in range(27)]


def summarize_family(frame_options, observed):
    scorehist = Counter()
    by_class = {j: Counter() for j in range(9)}
    pairs = primary_pairs()
    for frames in product(*frame_options):
        symbols = tuple(symbol for frame in frames for symbol in frame)
        scorehist[sum(symbols[a] == symbols[b] for a,b in pairs)] += 1
        for j in range(9):
            by_class[j][sum(
                symbols[27*q+9*d+j] == symbols[27*q2+9*d+j]
                for d in range(3) for q in range(3) for q2 in range(q+1,3)
            )] += 1
    n = sum(scorehist.values())
    return {
        "completions": n,
        "complete_primary_match_counts": dict(sorted(scorehist.items())),
        "mean_full_matches_out_of_81":
            sum(score*count for score,count in scorehist.items())/n,
        "minimum_full_matches": min(scorehist),
        "maximum_full_matches": max(scorehist),
        "fraction_with_at_least_49_of_81_matches":
            sum(count for score,count in scorehist.items() if score>=49)/n,
        "per_letter_full_9_pair_histograms": {
            LETTERS[j]: dict(sorted(scores.items()))
            for j,scores in by_class.items()
        }
    }


def observation_only_limits(observed):
    # Each of the 27 (d,j) positions has three primary-quarter symbols.
    # With two binary marks, the three pair comparisons contribute 1
    # when not all three agree or 3 when they all do.
    lo = hi = 0
    for j in range(27):
        fixed = [observed.get(1 + 27*q + j) for q in range(3)]
        options = set()
        for vals in product("/-", repeat=3):
            if all(v is None or vals[i] == v for i,v in enumerate(fixed)):
                options.add(sum(vals[q] == vals[q2]
                                for q in range(3) for q2 in range(q+1,3)))
        assert options
        lo += min(options)
        hi += max(options)
    return [lo,hi]


def main():
    count, observed = observations()
    assert count == 84 and len(observed) == 66
    all_primary = [primary_frame_choices(observed, f) for f in range(9)]
    columns = [[frame for frame in choices if primary_columns(frame)]
               for choices in all_primary]
    observed_pairs = [
        (a,b) for a,b in primary_pairs() if a+1 in observed and b+1 in observed
    ]
    matches = sum(observed[a+1] == observed[b+1] for a,b in observed_pairs)
    assert len(observed_pairs) == 40 and matches == 24
    broad = summarize_family(all_primary, observed)
    column = summarize_family(columns, observed)
    assert broad["completions"] == 12960
    assert column["completions"] == 18
    assert broad["minimum_full_matches"] == 37
    assert broad["maximum_full_matches"] == 53
    assert column["complete_primary_match_counts"] == {
        43:4, 45:4, 47:6, 49:2, 51:2
    }
    assert column["per_letter_full_9_pair_histograms"]["E"] == {5:18}
    assert observation_only_limits(observed) == [35,63]

    print(json.dumps({
        "observed_primary_same_position": {
            "matches":matches,
            "pairs":len(observed_pairs),
            "match_fraction":matches/len(observed_pairs)
        },
        "observation_only_global_possible_match_range_out_of_81":
            observation_only_limits(observed),
        "broad_three_of_nine_primary_family":broad,
        "physical_column_primary_family":column,
        "mask_sensitivity_example": (
            "Known E comparisons are 3/3 matches, while every physical-"
            "column completion gives only 5/9 E comparisons matching."
        ),
        "cautions":[
            "Completions are conditional on assumptions inferred from the same corpus.",
            "The 40 observed pair comparisons are not a uniform independent sample.",
            "Agreement under a selected family is not evidence that the family is true.",
            "Do not infer probabilities of unseen physical symbols from uniform completion weights."
        ]
    }, indent=2))


if __name__ == "__main__":
    main()

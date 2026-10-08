#!/usr/bin/env python3
"""Conjecture Lab CL-02: nine Q4 commands within a known 14-move word.

Exploratory *answer-assisted* subsequence test, explicitly not a decoder
validation. Six ternary codebooks, 18 current one-slash tail assignments,
and both command directions make 216 attempted hypotheses. Freeze the
reported scope; a 9-of-14 subsequence is not the historically documented
native 14-move receiver.
"""
import json
from itertools import permutations, product
from pathlib import Path

from enumerate_sticker_completion_ensembles import observations, q4_choices

ROOT = Path(__file__).resolve().parents[1]


def subsequence_positions(word, target):
    matched = []
    j = 0
    for k, c in enumerate(target, start=1):
        if j < len(word) and word[j] == c:
            matched.append(k)
            j += 1
    return matched if j == len(word) else None


def all_candidates(depth_choices):
    result = []
    for depths in product(*depth_choices):
        for book in permutations("URL"):
            mapping = dict(enumerate(book))
            forward = "".join(mapping[d] for d in depths)
            for direction, word in (
                ("forward", forward), ("reverse", forward[::-1])
            ):
                result.append({
                    "depths": "".join(str(x) for x in depths),
                    "codebook": "".join(book),
                    "direction": direction,
                    "word": word,
                })
    return result


def shuffled_target(target, lcg):
    a = list(target)
    for i in range(len(a) - 1, 0, -1):
        # Deterministic LCG for a reproducible *exploratory* comparison.
        lcg[0] = (1664525 * lcg[0] + 1013904223) & 0xffffffff
        j = lcg[0] % (i + 1)
        a[i], a[j] = a[j], a[i]
    return "".join(a)


def run():
    n, observed = observations()
    assert n == 84 and len(observed) == 66
    with (ROOT / "data/sticker-lever-cue.json").open(encoding="utf8") as fh:
        cue = json.load(fh)
    target = cue["known_normal_bunker_code"]
    assert target == "UURLRRRUUURLLL" and len(target) == 14
    options = q4_choices(observed)
    candidates = all_candidates(options)
    assert len(candidates) == 216
    matches = [
        dict(row, matched_positions=subsequence_positions(row["word"], target))
        for row in candidates
        if subsequence_positions(row["word"], target) is not None
    ]
    assert [(r["depths"], r["codebook"], r["direction"], r["word"])
            for r in matches] == [
                ("021101222", "URL", "forward", "ULRRURLLL"),
                ("121101222", "URL", "forward", "RLRRURLLL"),
            ]
    # Historical known 14-action input and nine derived commands are not
    # the same operation. Random rearrangements illustrate permissiveness.
    lcg = [813925]
    histogram = {}
    for _ in range(4000):
        random_target = shuffled_target(target, lcg)
        hits = sum(subsequence_positions(c["word"], random_target)
                   is not None for c in candidates)
        histogram[hits] = histogram.get(hits, 0) + 1
    assert sum(histogram.values()) == 4000
    assert sum(n for k, n in histogram.items() if k <= 2) == 1729
    assert sum(k*n for k, n in histogram.items()) == 22403
    return {
        "status": "EXPLORATORY / ANSWER-ASSISTED; not blind validation",
        "depth_codes": len(list(product(*options))),
        "codebooks": 6,
        "directions": 2,
        "searches": len(candidates),
        "unique_forward_words": len({c["word"] for c in candidates
                                    if c["direction"] == "forward"}),
        "unique_words_with_reversal": len({c["word"] for c in candidates}),
        "known_password": target,
        "matching_candidates": matches,
        "shuffle_control": {
            "n": 4000,
            "initial_lcg_seed": 813925,
            "same_command_census": True,
            "mean_matching_candidates": 22403/4000,
            "fraction_two_or_fewer": 1729/4000,
            "fraction_two_or_more": (4000 - 1729 + histogram[2])/4000,
            "notice": "Deterministic exploratory shuffle is not a formal "
                      "post-selection familywise probability",
        },
        "interpretation": (
            "Two answer-assisted subsequence fits are easy to imagine but "
            "not independently significant. No authentic nine-command "
            "consumer, subset-selection rule or prior fixed codebook exists."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

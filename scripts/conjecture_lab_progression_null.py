#!/usr/bin/env python3
"""CL-02 progression audit: conditional numerology vs matching grammar null.

Three 9-bit selected-depth surfaces under a deliberately chosen balanced
Q4 assumption happen to encode 189, 252, 315 (slash=1, A-I class order).
Test what is forced by the one-dash-per-physical-column grammar and the
exact entire 12-master *selected* parent before asserting significance.
"""
from collections import Counter
from itertools import product
import json

from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, primary_columns, q4_choices,
    make_master, selected_columns, COLS,
)


def binval(surface):
    assert len(surface) == 9 and set(surface) <= {"/", "-"}
    return sum((mark == "/") << (8-j)
               for j, mark in enumerate(surface))


def all_selected_surfaces():
    result = []
    for js in product(*COLS):
        dash = set(js)
        result.append("".join("-" if j in dash else "/"
                              for j in range(9)))
    assert len(set(result)) == 27
    return sorted(result)


def candidate_readout(master, depths):
    return tuple(
        "".join(master[27*q + 9*depths[j] + j] for j in range(9))
        for q in range(3)
    )


def run():
    n, observed = observations()
    assert n == 84 and len(observed) == 66
    groups = [
        [f for f in primary_frame_choices(observed, x)
         if primary_columns(f)]
        for x in range(9)
    ]
    tail = list(product(*q4_choices(observed)))
    values = sorted({binval(surface)
                     for surface in all_selected_surfaces()})
    assert len(values) == 27 and all(v % 7 == 0 for v in values)

    # Exactly one minority dash per physical column => three dash weights
    # are one from each exponent-congruence class mod 3. Because
    # 2^3 == 1 (mod 7), their sum is 1+2+4 == 0 (mod 7).
    # All-slash 9-bit 511 is also 0 (mod 7).
    null = Counter()
    for a, b, c in product(values, repeat=3):
        if a + c == 2*b:
            null[b-a] += 1
    assert sum(null.values()) == 191
    assert null[0] == 27
    assert null[63] == 8 and null[-63] == 8

    selected_words = []
    balanced_selected_words = []
    for frames in product(*groups):
        for depths in tail:
            m = make_master(frames, depths)
            if not selected_columns(m, depths):
                continue
            words = candidate_readout(m, depths)
            numbers = tuple(map(binval, words))
            balanced = all(depths.count(x) == 3 for x in (0, 1, 2))
            selected_words.append(numbers)
            if balanced:
                balanced_selected_words.append((numbers, words, depths))
    assert len(selected_words) == 12
    assert len(balanced_selected_words) == 2

    ap_selected = [v for v in selected_words
                   if v[0] + v[2] == 2*v[1]]
    assert len(ap_selected) == 4
    assert set(ap_selected) == {(189, 252, 315)}
    assert {n for n, _, _ in balanced_selected_words} == {
        (189, 252, 315)
    }

    original = balanced_selected_words[0][1]
    assert original == (
        "-/-////-/", "-//////--", "/--///-//"
    )
    return {
        "status": "EXPLORATORY; numerical relation discovered after choosing a candidate family",
        "source_grammar": "Each 9-bit selected row has exactly one dash per IAB/CDE/FGH physical column",
        "possible_one_dash_column_surfaces": len(values),
        "nine_bit_values": values,
        "every_value_divisible_by_7": True,
        "explanation": "2^3=1 mod 7; physical columns cover exponent classes 0,1,2 mod 3; the dash sum is 1+2+4=0 mod 7; 511=0 mod 7",
        "uniform_independent_surface_triples": len(values)**3,
        "exact_ap_triples": sum(null.values()),
        "exact_nonconstant_ap_triples": sum(null.values()) - null[0],
        "ap_positive_step_63_triples": null[63],
        "AP_entire_grammar_frequency": sum(null.values()) / len(values)**3,
        "matched_A_B_selected_masters": len(selected_words),
        "matched_A_B_selected_masters_with_AP": len(ap_selected),
        "matched_A_B_selected_AP_frequency": len(ap_selected)/len(selected_words),
        "matched_A_B_selected_unique_outputs": len(set(selected_words)),
        "matched_balanced_selected_masters": len(balanced_selected_words),
        "candidate_three_strings": original,
        "candidate_three_binary_numbers": (189, 252, 315),
        "difference": 63,
        "numbers_divided_by_seven": (27, 36, 45),
        "warning": (
            "The eye-catching 189,252,315 progression is present in 4 "
            "of the 12 A+B+selected complete masters, so the more permissive "
            "191/19683 independent-surface rate is not the correct "
            "post-selection evidence rate. Divisibility by seven is "
            "forced by the chosen one-dash-per-column coding grammar."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

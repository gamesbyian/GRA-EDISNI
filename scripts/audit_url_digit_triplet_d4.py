#!/usr/bin/env python3
"""Bounded nine-digit URL ↔ A-I triplet equality across all eight physical D4 views.

RESEARCH MODE: DISCOVER / DEVELOP. NOT an authorial cue and not a decoder.
Source: CE background's established path '534brn9653f9j8mmd', with exactly
nine decimal digits. The trial, *invented explicitly for falsification*, says
successive source digits correspond to the nine stickers in a D4-oriented
physical 3x3 IAB/CDE/FGH layout, and duplicate digits must share identical
selected three-mark A-I class values. This is one simple hypothetical codebook.

Run: python scripts/audit_url_digit_triplet_d4.py
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from math import prod
from pathlib import Path

from audit_finite_receiver_invariance import (
    ROOT, populations, selected_read, LETTERS, LAYOUT,
)
from audit_observation_first_class_triplets import audit as raw_triplet_audit

PATH_NAME = "534brn9653f9j8mmd"
DIGITS = "".join(x for x in PATH_NAME if x.isdigit())
assert DIGITS == "534965398"
EXPECTED_ORIENTATIONS = (
    "IABCDEFGH", "FCIGDAHEB", "HGFEDCBAI", "BEHADGICF",
    "BAIEDCHGF", "HEBGDAFCI", "FGHCDEIAB", "ICFADGBEH"
)
EXPECTED_COUNTS = {
    "weak_raw_tail": (2, 0, 0, 4, 0, 8, 16, 0),
    "U2": (2, 0, 0, 8, 0, 3, 28, 0),
    "U3": (0, 0, 0, 0, 0, 0, 6, 0),
    "U4": (0, 0, 0, 0, 0, 0, 6, 0),
    "U5": (0, 0, 0, 0, 0, 0, 6, 0),
}


def d4_orientation(flip: bool, quarter_turns: int) -> str:
    grid = [[""]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            a,b=r,2-c if flip else c
            for _ in range(quarter_turns):
                a,b=b,2-a
            grid[a][b]=LAYOUT[r][c]
    return "".join("".join(row) for row in grid)


def digit_groups(orientation: str) -> dict[str, list[str]]:
    assert len(orientation)==9 and set(orientation)==set(LETTERS)
    mapping={}
    for digit,ch in zip(DIGITS,orientation):
        mapping.setdefault(digit,[]).append(ch)
    return mapping


def class_words(selected27: str) -> dict[str,str]:
    assert len(selected27)==27
    return {
        letter:"".join(selected27[q*9+j] for q in range(3))
        for j,letter in enumerate(LETTERS)
    }


def passes(words: dict[str,str], group: dict[str,list[str]]) -> bool:
    return all(len(set(words[ch] for ch in letters))==1
               for letters in group.values())


def weak_count(allowed: dict[str,set[str]],group:dict[str,list[str]]) -> tuple[int,dict]:
    local={}
    for digit,classes in group.items():
        possible=set.intersection(*(allowed[ch] for ch in classes))
        local[digit]=sorted(possible)
    return prod(map(len,local.values())),local


def audit() -> dict:
    raw=raw_triplet_audit()["class_readouts"]
    allowed={ch:set(row["possible_three_character_words"])
             for ch,row in raw.items()}
    assert prod(map(len,allowed.values())) == 768
    models=populations()
    selected={family:[selected_read(word) for word in masters]
              for family,masters in models.items()}

    layouts=[]
    for flip in (False,True):
        for rot in range(4):
            orient=d4_orientation(flip,rot)
            groups=digit_groups(orient)
            low,compatible_by_digit=weak_count(allowed,groups)
            row={
                "flip_before_rotation":flip,"clockwise_quarter_turns":rot,
                "physical_layout_in_URL_digit_order":orient,
                "source_path_digits":DIGITS,
                "duplicate_digit_groups":{
                    digit:letters for digit,letters in groups.items()
                    if len(letters)>1
                },
                "observation_first_one_slash_Q4":{
                    "distinct_compatible_triplet_readouts":low,
                    "per_digit_compatible_words":compatible_by_digit
                },
                "models":{}
            }
            for family,words in selected.items():
                surviving=[readout for readout in words
                           if passes(class_words(readout),groups)]
                row["models"][family]={
                    "compatible_physical_masters":len(surviving),
                    "distinct_compatible_readouts":len(set(surviving)),
                    "surviving_readouts":sorted(set(surviving)),
                }
            layouts.append(row)
    assert tuple(row["physical_layout_in_URL_digit_order"] for row in layouts)==EXPECTED_ORIENTATIONS
    assert {model:tuple(
        row["observation_first_one_slash_Q4"]["distinct_compatible_triplet_readouts"]
        if model=="weak_raw_tail"
        else row["models"][model]["compatible_physical_masters"]
        for row in layouts)
        for model in EXPECTED_COUNTS}==EXPECTED_COUNTS

    assert all(row["models"]["U5"]["compatible_physical_masters"]==0
               for i,row in enumerate(layouts) if i!=6)
    assert layouts[6]["models"]["U5"]["compatible_physical_masters"]==6
    assert layouts[6]["models"]["U5"]["distinct_compatible_readouts"]==1

    return {
        "research_mode":"DISCOVER/DEVELOP; post-selected hypothetical equal-digit codebook",
        "source_path":f"dat/{PATH_NAME}/",
        "nine_path_digits":DIGITS,
        "origin_layout":"IAB/CDE/FGH",
        "transforms":"exact D4 orbit: optional mirror, then 0-3 clockwise rotations",
        "extra_unsupported_rule":"same URL digit must map to equal 3-char Q4-selected class readout",
        "weak_raw_onehot_distinct_class_words_before_equality":768,
        "model_population_counts":{k:len(v) for k,v in models.items()},
        "orientation_results":layouts,
        "interpretation":(
            "Four of eight D4 layouts permit this equal-digit codebook at the "
            "weak one-slash-only level. U2 has survivors on the same four "
            "orientations; U3/U4/U5 retain physical masters only in the "
            "vertical-flip orientation FGH/CDE/IAB. There, six of ten U5 "
            "masters share one selected 27-mark readout. This is a "
            "retrospective, parameter-chosen outcome, NOT a validated code."
        ),
        "limitations":[
            "No historical instruction links the nine path digits to a 3-character triplet codebook.",
            "No historical source specifies which of the eight D4 orientations, if any, to use.",
            "Counts of surviving physical masters are combinatorial, not evidence likelihood.",
            "The weak-level factorization counts distinct class readouts, not full 108-cell masters.",
            "A different digit function, source page address role, or traversal falls outside this test.",
            "Do not promote a surviving vertical flip to an authored clue without a source-fixed registration."
        ]
    }


def self_test():
    assert d4_orientation(False,0)=="IABCDEFGH"
    assert d4_orientation(True,2)=="FGHCDEIAB"
    assert digit_groups("IABCDEFGH")["9"]==["C","G"]
    assert passes({ch:"///" for ch in LETTERS},digit_groups("IABCDEFGH"))
    x={ch:"///" for ch in LETTERS};x["C"]="--/"
    assert not passes(x,digit_groups("IABCDEFGH"))
    print("D4 and duplicate-codebook synthetic controls: pass")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    self_test()
    if args.self_test:return
    result=audit()
    content=json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content,encoding="utf8")
        print("saved",args.output)
    else:print(content)


if __name__=="__main__":
    main()

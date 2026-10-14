#!/usr/bin/env python3
"""Observation-first nine-class selected-triplet inventory.

NO primary minority census, column-occupancy, polarity staircase, selected-
surface validity, recursive closure, or intended decoder is assumed.

The only structural hypothesis is exactly one slash among each A-I class's
three final-Q4 cells. All 9 primary body cells per class are left free where
not physically observed. This exact local enumeration asks which 3-symbol
selected body words are forced by existing physical observations.

Run: python scripts/audit_observation_first_class_triplets.py
     python scripts/audit_observation_first_class_triplets.py --output /tmp/triplets.json
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from audit_finite_receiver_invariance import physical_observations, ROOT

LETTERS = "ABCDEFGHI"
LAYOUT = ("IAB", "CDE", "FGH")
POS = {ch:(r,c) for r,row in enumerate(LAYOUT) for c,ch in enumerate(row)}
EXPECTED_COUNTS = {
    "A":8,"B":1,"C":2,"D":2,"E":1,"F":1,"G":6,"H":1,"I":4,
}
EXPECTED_FORCED = {
    "B":"//-","E":"///","F":"///","H":"--/",
}


def choices_for_letter(observations:dict[int,str], j:int) -> dict:
    ch=LETTERS[j]
    depths=[]
    for selected in range(3):
        if all(observations.get(82+9*d+j, "/" if selected==d else ".")
               == ("/" if selected==d else ".")
               for d in range(3)):
            depths.append(selected)
    assert depths, ch
    outcomes=set()
    detail=[]
    for depth in depths:
        addresses=tuple(q*27+9*depth+j+1 for q in range(3))
        possibilities=[(observations.get(r),) if r in observations
                       else ("-","/") for r in addresses]
        words=set("".join(p) for p in itertools.product(*possibilities))
        outcomes |= words
        detail.append({
            "depth_0_based":depth,
            "selected_primary_residues":list(addresses),
            "physically_known_selected_marks":[r in observations for r in addresses],
            "possible_three_character_words":sorted(words),
        })
    row,col=POS[ch]
    return {
        "class":ch,
        "physical_row_col_1_based":[row+1,col+1],
        "conditional_one_slash_Q4_choices":depths,
        "possible_three_character_words":sorted(outcomes),
        "number_of_readouts":len(outcomes),
        "invariant_three_character_readout":next(iter(outcomes)) if len(outcomes)==1 else None,
        "by_tail_depth":detail,
    }


def audit()->dict:
    observed=physical_observations()
    classes={ch:choices_for_letter(observed,j)
             for j,ch in enumerate(LETTERS)}
    assert {k:v["number_of_readouts"] for k,v in classes.items()}==EXPECTED_COUNTS
    assert {k:v["invariant_three_character_readout"] for k,v in classes.items()
            if v["invariant_three_character_readout"] is not None} == EXPECTED_FORCED
    assert classes["B"]["by_tail_depth"][0]["selected_primary_residues"]==[20,47,74]
    assert classes["E"]["by_tail_depth"][0]["selected_primary_residues"]==[5,32,59]
    assert classes["F"]["by_tail_depth"][0]["selected_primary_residues"]==[15,42,69]
    assert classes["H"]["by_tail_depth"][0]["selected_primary_residues"]==[26,53,80]
    assert all(
        all(detail["physically_known_selected_marks"])
        for k in ("B","E","F","H")
        for detail in classes[k]["by_tail_depth"]
    )
    # A deliberately narrow original-CE-background source check: if the
    # nine digits of the real 534brn path were a direct A-I codebook with
    # identical digits requiring identical selected three-mark words,
    # the D/H (digit 9) pair is already impossible before invoking U2.
    # Digit-to-class *alignment* is stipulated, not independently proved.
    url_digits="".join(c for c in "534brn9653f9j8mmd" if c.isdigit())
    assert url_digits=="534965398"
    digit_groups={}
    for j,ch in enumerate(LETTERS):
        digit_groups.setdefault(url_digits[j],[]).append(ch)
    repeated_equal_word_test={}
    for digit,group in sorted(digit_groups.items()):
        if len(group)<2:continue
        possibilities=[set(classes[ch]["possible_three_character_words"])
                       for ch in group]
        intersection=set.intersection(*possibilities)
        repeated_equal_word_test[digit]={
            "class_group":group,
            "common_possible_triplets":sorted(intersection),
            "compatible_with_literal_equal_digit_equal_triplet":bool(intersection),
        }
    assert repeated_equal_word_test["9"]["class_group"]==["D","H"]
    assert not repeated_equal_word_test["9"]["common_possible_triplets"]
    assert repeated_equal_word_test["5"]["common_possible_triplets"]==["///"]
    assert repeated_equal_word_test["3"]["common_possible_triplets"]==["//-"]

    # Ensure the local one-hot/no-body-grammar spaces strictly contain the
    # U2-selected output class supports; a separate enumerator owns U2.
    return {
        "research_mode":"DEVELOP; observation-only body plus a single declared Q4 one-slash prior",
        "observed_records":84,"unique_residues":66,
        "conditional_Q4_hypothesis":"one slash and two dots per A-I class stack",
        "class_readouts":classes,
        "literal_A_I_path_digit_equivalence_test":{
            "source_path_digits":"534965398",
            "alignment_assumption":"sequential digits correspond exactly to A,B,C,D,E,F,G,H,I",
            "requirement":"same source digit implies same selected 3-mark class word",
            "duplicate_digit_groups":repeated_equal_word_test,
            "verdict":"contradicted for digit 9 (D/H), even in weak one-hot-only model",
        },
        "already_fixed_classes_without_primary_code":"BEFH",
        "fully_physically_seen_body_sites_of_these_classes":{
            k:classes[k]["by_tail_depth"][0]["selected_primary_residues"]
            for k in ("B","E","F","H")
        },
        "limitations":[
            "One slash per class tail is a structural hypothesis, not an observed printed law for every unseen cell.",
            "A class being completely determined is not evidence it is supposed to be read as a triplet.",
            "No U2 occupancy rule, recursion or receiver content was used.",
            "This is exact marginal class enumeration. Combined nine-class outputs are not assumed independent of future source rules."
        ]
    }


def self_test():
    blank={}
    all_words=choices_for_letter(blank,0)["possible_three_character_words"]
    assert len(all_words)==8 and all_words[0]=="---" and all_words[-1]=="///"
    fake={20:"/",47:"/",74:"-",101:"/"}
    assert choices_for_letter(fake,1)["possible_three_character_words"]==["//-"]
    print("synthetic raw-mask and tail-selector controls: pass")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    self_test()
    if a.self_test:return
    result=audit()
    payload=json.dumps(result,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf8")
        print("saved",a.output)
    else:
        print(payload)


if __name__=="__main__":
    main()

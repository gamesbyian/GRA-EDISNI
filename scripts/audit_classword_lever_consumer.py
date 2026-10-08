#!/usr/bin/env python3
"""Experiment 479: registered twelve-step A-I class-word lever replay.

Read H108 vertically as nine class words of twelve positions each,
using only alphabetical ABCDEFGHI or solved physical IABCDEFGH order,
either read direction, and the independently historical sleeve
/=U, -=R, .=L mapping. Check the known 14-move original bunker
password in canonical and all cyclically rotated/reversed forms.

The 324-member candidate universe is the raw-compatible primary
one-minority-per-physical-column plus Q4 one-slash-stack family,
not the completed recursive machine.

No newly invented lever password or in-game second handler is tested.
"""
from collections import Counter
from itertools import product
import json

from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, primary_columns,
    q4_choices, make_master,
)

LETTERS = "ABCDEFGHI"
ORDERS = ("ABCDEFGHI", "IABCDEFGH")
DIRECTIONS = ("forward", "reverse")
LEVER = {"/":"U", "-":"R", ".":"L"}
BUNKER = "UURLRRRUUURLLL"


def class_index_stream(order, direction):
    assert sorted(order) == sorted(LETTERS)
    residues = tuple(
        9*t + LETTERS.index(letter) + 1
        for letter in order
        for t in range(12)
    )
    assert len(residues)==108 and len(set(residues))==108
    if direction=="reverse":
        residues=residues[::-1]
    return residues


def password_variants():
    assert len(BUNKER)==14 and set(BUNKER)=={"U","R","L"}
    return tuple(
        base[k:]+base[:k]
        for base in (BUNKER, BUNKER[::-1])
        for k in range(len(BUNKER))
    )


def candidate_masters(obs):
    frames = [
        [f for f in primary_frame_choices(obs,i) if primary_columns(f)]
        for i in range(9)
    ]
    selector_options = tuple(product(*q4_choices(obs)))
    count=0
    for ff in product(*frames):
        for depth in selector_options:
            count+=1
            yield make_master(ff,depth)
    assert count==324


def visible_placements(observed, positions, variants):
    possibilities=[]
    canonical=0
    for variant_index, word in enumerate(variants):
        for start in range(108):
            support=conflicts=0
            for j,command in enumerate(word):
                r=positions[(start+j)%108]
                if r not in observed:
                    continue
                support+=1
                conflicts+= LEVER[observed[r]] != command
            if conflicts==0:
                possibilities.append({
                    "password_variant_index":variant_index,
                    "start_zero_based":start,"known_symbol_support":support
                })
                if variant_index==0:
                    canonical+=1
    return possibilities,canonical


def type_compatible_placements(positions, variants):
    """Direct H108 native order only: 1..81 never L, 82..108 never R."""
    cases = []
    for variant_index, word in enumerate(variants):
        for start in range(108):
            typed = all(
                (cmd != "L" if positions[(start+i)%108] <= 81
                 else cmd != "R")
                for i, cmd in enumerate(word)
            )
            if typed:
                cases.append((variant_index,start))
    return cases


def full_placements(masters, positions, variants):
    found=0
    members=0
    for master in masters:
        text = "".join(LEVER[x] for x in master)
        hits_this_master=0
        for start in range(108):
            word = "".join(
                text[positions[(start+j)%108]-1] for j in range(14))
            hits_this_master+=sum(word==v for v in variants)
        found+=hits_this_master
        members+=hits_this_master>0
    return {"full_matching_placements":found,
            "complete_masters_with_any_match":members}


def main():
    records,obs=observations()
    assert records==84 and len(obs)==66
    variants=password_variants()
    assert len(variants)==28
    masters=list(candidate_masters(obs))
    assert len(masters)==324
    reports=[]
    for order in ORDERS:
        for direction in DIRECTIONS:
            positions=class_index_stream(order,direction)
            possibles,canonical=visible_placements(obs,positions,variants)
            type_cases=type_compatible_placements(positions,variants)
            full=full_placements(masters,positions,variants)
            report={
                "class_order":order,
                "reading_direction":direction,
                "canonical_password_physical_compatible_starts":canonical,
                "alphabet_only_compatible_starts_all_28_variants":
                    len(type_cases),
                "compatible_rotated_or_reversed_partial_starts":
                    len(possibles),
                "raw_compatible_placements":possibles,
                **full,
            }
            reports.append(report)
    assert all(r["canonical_password_physical_compatible_starts"]==0
               for r in reports)
    assert all(r["compatible_rotated_or_reversed_partial_starts"]==3
               for r in reports)
    assert all(sorted(p["known_symbol_support"] for p in
                      r["raw_compatible_placements"])==[5,5,6]
               for r in reports)
    assert all(r["alphabet_only_compatible_starts_all_28_variants"]==0
               for r in reports)
    assert all(r["full_matching_placements"]==0 for r in reports)
    print(json.dumps({
        "experiment":477,
        "physical_records":records,
        "unique_residues":len(obs),
        "complete_structural_masters":len(masters),
        "native_class_orders":list(ORDERS),
        "reading_directions":list(DIRECTIONS),
        "bunker_password":BUNKER,
        "password_orientation_variants":len(variants),
        "cyclic_H108_starts_per_variant":108,
        "results":reports,
        "interpretation":(
            "A whole A-I twelve-cell class word can contain U/R/L, but "
            "the original specific fourteen-command bunker password has "
            "zero placements across both native class orders even when "
            "all 42 unknown sticker labels are freely completed within "
            "their original sector alphabets. Therefore the 3 weak "
            "physical-only placements already violate the sector grammar; "
            "no full 324-master check is needed for this negative."
        ),
        "scope_limits":[
            "The four tests are not independent because reversing both the word and stream is symmetrical.",
            "Only the original known bunker code is being tested, not an unobserved second handler.",
            "Class-word reading order is historically suggested by the physical layout, not confirmed as a CE command sequence.",
            "Raw five/six-observation partial coincidences are not completed-code evidence.",
            "No guess is promoted to a physical sticker observation."
        ]
    },indent=2))


if __name__=="__main__":
    main()

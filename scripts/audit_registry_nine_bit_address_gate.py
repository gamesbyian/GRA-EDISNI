#!/usr/bin/env python3
"""Bounded physical-only nine-bit class-address test for source-authentic 133 rows.

Question: could EACH of the nine A-I native 9-cell *body* class strips, as
a straightforward binary integer, directly index a line in the original
Terminal41 breach-contribution registry? Test four simple conventions:
serial/reverse order x slash=1/dash=1, and both zero- and one-based
row indexing. No completed missing stickers, U2/POS3 or decoding guessed.

Run: python scripts/audit_registry_nine_bit_address_gate.py
     python scripts/audit_registry_nine_bit_address_gate.py --output /tmp/registry-address.json
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from audit_terminal41_marked_recovery import ROOT, SOURCE, parse

OBS = ROOT / "data/observations.csv"
LETTERS = "ABCDEFGHI"


def observed_body() -> dict[int, str]:
    seen = {}
    physical = set()
    with OBS.open(newline="", encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==84
    for row in rows:
        serial=int(row["serial"])
        residue=int(row["residue"])
        mark=row["symbol"]
        assert serial not in physical
        physical.add(serial)
        assert (serial-1)%108+1==residue
        assert mark in ("/","-") if residue<=81 else mark in ("/",".")
        assert residue not in seen or seen[residue]==mark
        seen[residue]=mark
    assert len(seen)==66
    return {residue:mark for residue,mark in seen.items() if residue<=81}


def class_word(observations:dict[int,str], j:int)->str:
    return "".join(observations.get(1+j+9*f,"?") for f in range(9))


def exact_binary_extrema(word9:str, slash_is_one:bool,
                         reverse:bool)->tuple[int,int]:
    assert len(word9)==9 and set(word9)<=set("/-?")
    w=word9[::-1] if reverse else word9
    positive="/" if slash_is_one else "-"
    lo="".join("0" if c=="?" else "1" if c==positive else "0" for c in w)
    hi="".join("1" if c=="?" else "1" if c==positive else "0" for c in w)
    return int(lo,2),int(hi,2)


def audit()->dict:
    first81=observed_body()
    source_rows,_=parse(SOURCE.read_text(encoding="utf-8"))
    capacity=len(source_rows)
    assert capacity==133
    choices={}
    expected={
        "serial_slash1":["B","D","E","F","G","I"],
        "serial_dash1":["A","C","D","E"],
        "reverse_slash1":["B","C","D","F","G","H","I"],
        "reverse_dash1":["B","C","H"],
    }
    for reverse in (False,True):
        for slash_is_one in (True,False):
            key=(("reverse" if reverse else "serial") + "_" +
                 ("slash1" if slash_is_one else "dash1"))
            cells={}
            for j,ch in enumerate(LETTERS):
                native=class_word(first81,j)
                minimum,maximum=exact_binary_extrema(
                    native,slash_is_one,reverse
                )
                cells[ch]={
                    "physically_observed_9_mark_body_word":native,
                    "known_positions":9-native.count("?"),
                    "unknown_positions":native.count("?"),
                    "min_9bit_value_all_unknown_bits_zero":minimum,
                    "max_9bit_value_all_unknown_bits_one":maximum,
                    "any_zero_based_0_to_132_index_possible":minimum<capacity,
                    "any_one_based_1_to_133_index_possible":(
                        maximum>=1 and minimum<=capacity
                    ),
                }
            zero_impossible=[
                ch for ch,row in cells.items()
                if not row["any_zero_based_0_to_132_index_possible"]
            ]
            one_impossible=[
                ch for ch,row in cells.items()
                if not row["any_one_based_1_to_133_index_possible"]
            ]
            assert zero_impossible==expected[key], (key,zero_impossible)
            assert one_impossible==expected[key], (key,one_impossible)
            choices[key]={
                "orientation":"reverse" if reverse else "serial",
                "one_bit_symbol":"/" if slash_is_one else "-",
                "indices_zero_based":[0,capacity-1],
                "indices_one_based":[1,capacity],
                "class_results":cells,
                "provably_out_of_range_classes_zero_based":zero_impossible,
                "provably_out_of_range_classes_one_based":one_impossible,
                "all_nine_class_values_can_fit_as_direct_native_registry_indices":
                    not zero_impossible and not one_impossible,
            }
    # Give the parity interpretation every cheap shared-bit position:
    # drop any one of the nine primary sites from EACH class before viewing
    # the remaining eight as a raw 0..255 index. The omitted bit position
    # is GLOBAL across all A-I classes, not tuned per class. Exact lowest
    # 8-bit values still prove at least one impossible class every time.
    dropped_bit_controls={}
    expected_min_failures={
        "serial_slash1":2,"serial_dash1":1,
        "reverse_slash1":2,"reverse_dash1":1,
    }
    for reverse in (False,True):
        for slash_is_one in (True,False):
            key=(("reverse" if reverse else "serial")+"_"+
                 ("slash1" if slash_is_one else "dash1"))
            trials=[]
            for removed_index in range(9):
                out_of_range=[]
                minima={}
                for j,ch in enumerate(LETTERS):
                    word=class_word(first81,j)
                    oriented=word[::-1] if reverse else word
                    eight=oriented[:removed_index]+oriented[removed_index+1:]
                    assert len(eight)==8
                    one="/" if slash_is_one else "-"
                    lo=int("".join("0" if mark=="?" else
                                   "1" if mark==one else "0"
                                   for mark in eight),2)
                    minima[ch]=lo
                    if lo>=capacity:
                        out_of_range.append(ch)
                trials.append({
                    "removed_bit_position_1_based_in_read_order":
                        removed_index+1,
                    "provably_out_of_range_classes":out_of_range,
                    "minimum_8bit_values":minima,
                    "all_nine_class_8bit_indices_fit":not out_of_range,
                })
            assert len(trials)==9
            assert min(len(x["provably_out_of_range_classes"])
                       for x in trials)==expected_min_failures[key]
            assert all(x["provably_out_of_range_classes"] for x in trials)
            dropped_bit_controls[key]={
                "total_shared_omission_positions_tested":9,
                "minimum_out_of_range_classes":expected_min_failures[key],
                "trials":trials,
            }
    assert sum(len(x["trials"]) for x in dropped_bit_controls.values())==36

    return {
        "mode":"DEVELOP: physically observed sticker index bounds; no structural model",
        "physical_records":84,"physical_unique_residues":66,
        "native_original_registry_row_count":capacity,
        "native_original_registry_unique_hex_values":118,
        "source":"archive/external/twinysam-inside-arg/terminal41.link/dat/breach_contribution_reg.html",
        "hypothesized_join":"nine physical class body bit words -> nine raw registry row addresses",
        "four_source_simple_read_conventions":choices,
        "single_common_parity_bit_discarded_controls":dropped_bit_controls,
        "verdict":"All four raw 9-bit and all 36 shared one-bit-discarded 8-bit conventions leave at least one A-I class outside the 133-row source domain, irrespective of missing marks.",
        "limitations":[
            "The direct 9-bit index role is a declared cheap trial, not Playdead-authored source instruction.",
            "This excludes ONLY raw nine-bit values as full row indices in this 133-row registry, without transforming/modulo/masking/discarding bits.",
            "An independent source cue could specify such a transform or partial subset of A-I; this test does not rule those out.",
            "The historical page's registry entry ordering and the CE class-to-row interpretation are unverified.",
            "No POS3 completion or parity hypothesis was used to force missing physical marks.",
        ],
    }


def self_test()->None:
    assert exact_binary_extrema("?????????",True,False)==(0,511)
    assert exact_binary_extrema("---------",True,False)==(0,0)
    assert exact_binary_extrema("/////////",True,False)==(511,511)
    assert exact_binary_extrema("/--------",True,False)==(256,256)
    assert exact_binary_extrema("/--------",True,True)==(1,1)
    assert exact_binary_extrema("/?-------",True,False)==(256,384)
    print("synthetic 9-bit direction and unknown-bit extrema controls: pass")


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    self_test()
    if args.self_test:return
    data=audit()
    payload=json.dumps(data,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
        print("saved",args.output)
    else:
        print(payload)


if __name__=="__main__":
    main()

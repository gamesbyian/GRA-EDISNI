#!/usr/bin/env python3
"""Source-matched opaque-token controls for a speculative CE nine-digit reader.

Research mode DEVELOP: no foreground decoder, accepted CE code or Playdead
instruction is claimed.

Original CE background URL's digit string (534965398) has three duplicate
pairs. Prior hypothetical trial imposed equality of Q4-selected class
triplets for matching digits under any physical D4 orientation. Compare that
exact finite trial against two *other genuine source identifiers* before
calling the appearance selective. For longer controls a separate, explicitly
more flexible stress test tries all ordered nine-digit subsequences.

Run: python scripts/audit_terminal41_opaque_token_controls.py
     python scripts/audit_terminal41_opaque_token_controls.py --output /tmp/opaque.json

The script only reads source metadata and existing exact H108 model
enumerators; it does not fetch websites, infer missing sticker observations,
or post candidate credentials to any endpoint.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

from audit_completion_universe_layers import machine_layers

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/terminal41-source-tree.json"
URL_SEGMENT = "534brn9653f9j8mmd"
PROTOCOL_SEGMENT = "PROT6y723g90ty9r80234"
SAF_FIELD = "38546uy754j9j6tuk5fi34"  # documented original 22-char ASCII island
LAYOUT = ("IAB", "CDE", "FGH")
LETTERS = "ABCDEFGHI"
CE_DIGITS = "534965398"

SOURCE_PATHS = {
    "ce":f"terminal41.link/dat/{URL_SEGMENT}/index.html",
    "protocol":f"terminal41.link/sys/activate_shutdown_protocol/{PROTOCOL_SEGMENT}.html",
}
SOURCE_TOKENS = {"ce":URL_SEGMENT,"protocol":PROTOCOL_SEGMENT,"saf_ascii_field":SAF_FIELD}


def source_preflight() -> None:
    inventory = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert inventory["source_tree_sha"] == "4de72d7c2f21bd9eb4144fda51281c84cbcb90c4"
    assert inventory["count"] == 74 and len(inventory["files"]) == 74
    paths = {entry["path"] for entry in inventory["files"]}
    assert all(path in paths for path in SOURCE_PATHS.values())
    assert len(URL_SEGMENT)==17 and len(PROTOCOL_SEGMENT)==21 and len(SAF_FIELD)==22


def digit_string(token: str) -> str:
    return "".join(c for c in token if c.isdigit())


def multiplicity_pattern(digits: str) -> str:
    return "".join(str(n) for n in sorted(Counter(digits).values()))


def d4(flip: bool, turns: int) -> str:
    grid=[[""]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            a,b=r,2-c if flip else c
            for _ in range(turns):
                a,b=b,2-a
            grid[a][b]=LAYOUT[r][c]
    return "".join("".join(row) for row in grid)


ORIENTATIONS = tuple(d4(flip, turn) for flip in (False,True) for turn in range(4))
assert ORIENTATIONS == (
    "IABCDEFGH","FCIGDAHEB","HGFEDCBAI","BEHADGICF",
    "BAIEDCHGF","HEBGDAFCI","FGHCDEIAB","ICFADGBEH",
)


def selector_readout(master:str)->str:
    assert len(master)==108
    tail=[]
    for j in range(9):
        sites=[d for d in range(3) if master[81+9*d+j]=="/"]
        assert len(sites)==1
        tail.append(sites[0])
    return "".join(master[27*q+9*tail[j]+j] for q in range(3) for j in range(9))


def class_words(word27:str)->dict[str,str]:
    return {c:"".join(word27[9*q+j] for q in range(3))
            for j,c in enumerate(LETTERS)}


def accepted_count(digits:str, classes:dict[str,str], orientation:str) -> bool:
    values={}
    for number,letter in zip(digits,orientation):
        word=classes[letter]
        if number in values and values[number]!=word:
            return False
        values[number]=word
    return True


def best_survival(digits:str, word_counts:dict[str,int]) -> dict:
    assert len(digits)==9 and digits.isdigit()
    by_view={}
    for orientation in ORIENTATIONS:
        survivors=sum(multiplicity
                      for word,multiplicity in word_counts.items()
                      if accepted_count(digits,class_words(word),orientation))
        if survivors:
            by_view[orientation]=survivors
    return {"surviving_views":by_view,
            "number_of_surviving_views":len(by_view),
            "maximum_surviving_masters":max(by_view.values(),default=0)}


def candidate_digests(token_digits:str, source_name:str, word_counts:dict[str,int])->dict:
    assert len(token_digits)>=9
    pool=[]
    for inds in itertools.combinations(range(len(token_digits)),9):
        digits="".join(token_digits[i] for i in inds)
        if multiplicity_pattern(digits)!="111222":
            continue
        r=best_survival(digits,word_counts)
        pool.append((inds,digits,r))
    hits=[(ix,val,scores) for ix,val,scores in pool
          if scores["maximum_surviving_masters"]>0]
    high=[(ix,val,scores) for ix,val,scores in pool
          if scores["maximum_surviving_masters"]>=6]
    return {
        "source_name":source_name,
        "native_digit_length":len(token_digits),
        "all_order_preserving_9_digit_subsequences":math.comb(len(token_digits),9),
        "subsequences_with_CE_three_pairs_three_singles_pattern":len(pool),
        "subsequences_admitting_a_U5_completion_under_any_D4_view":len(hits),
        "subsequences_with_at_least_six_U5_survivors":len(high),
        "examples_at_least_six_U5_survivors":[
            {"digits":v,"zero_based_positions":list(indices),
             "surviving_views":scores["surviving_views"]}
            for indices,v,scores in high[:4]
        ],
        "nonindependent_sampling_warning":(
            "Subsequences share most digits and are NOT 1:1 random independent trials. "
            "Unlike the CE path, these longer tokens have NO native nine-digit segmentation; "
            "the comparisons are deliberately overflexible negative controls."
        ),
    }


def binary_baselines()->dict:
    """Two illustrative assumptions, neither a calibrated source null."""
    n=17;k=9;p_uniform=10/36
    base36=math.comb(n,k)*p_uniform**k*(1-p_uniform)**(n-k)
    p_others=(len(digit_string(PROTOCOL_SEGMENT))+
              len(digit_string(SAF_FIELD)))/(len(PROTOCOL_SEGMENT)+len(SAF_FIELD))
    conditional=math.comb(n,k)*p_others**k*(1-p_others)**(n-k)
    # IID decimal draws; select which three digits have multiplicity 2,
    # which three other digits occur once, and assign positions.
    three_pairs=(math.comb(10,3)*math.comb(7,3)*math.factorial(9)
                 // 2**3)/10**9
    assert abs(base36-0.017718592883732866)<1e-15
    assert abs(conditional-0.17396478026997247)<1e-14
    assert abs(three_pairs-0.190512)<1e-15
    return {
        "iid_uniform_base36_probability_exactly_9_digits_of_17":base36,
        "numeral_fraction_in_two_comparison_tokens":p_others,
        "illustrative_pooled_source_digit_rate_probability_exactly_9_of_17":conditional,
        "iid_uniform_decimal_probability_3_double_digits_and_3_singles_in_9":three_pairs,
        "warning":"Not calibrated probabilities for Playdead's token generation. Heterogeneous tokens, n=2 comparisons, retrospective source selection and unknown generation rules."
    }


def audit()->dict:
    source_preflight()
    tokens={}
    for name,token in SOURCE_TOKENS.items():
        digits=digit_string(token)
        tokens[name]={
            "original_source_segment_or_field":token,
            "character_length":len(token),"digit_count":len(digits),
            "digits_in_source_order":digits,
            "digit_frequency_pattern":multiplicity_pattern(digits),
            "fraction_numeric":len(digits)/len(token),
        }
    assert [(tokens[k]["character_length"],tokens[k]["digit_count"])
            for k in SOURCE_TOKENS]==[(17,9),(21,12),(22,13)]
    assert tokens["ce"]["digits_in_source_order"]==CE_DIGITS
    assert tokens["ce"]["digit_frequency_pattern"]=="111222"

    _u3,_u4,u5=machine_layers()
    assert len(u5)==10
    counts=Counter(selector_readout(master) for master in u5)
    assert sorted(counts.values())==[4,6]
    control={}
    for name,token in SOURCE_TOKENS.items():
        control[name]=candidate_digests(digit_string(token),name,counts)
    assert (
        control["ce"]["subsequences_with_CE_three_pairs_three_singles_pattern"],
        control["protocol"]["subsequences_with_CE_three_pairs_three_singles_pattern"],
        control["saf_ascii_field"]["subsequences_with_CE_three_pairs_three_singles_pattern"],
    ) == (1,64,186)
    assert [control[name]["subsequences_admitting_a_U5_completion_under_any_D4_view"]
            for name in SOURCE_TOKENS]==[1,2,6]
    assert [control[name]["subsequences_with_at_least_six_U5_survivors"]
            for name in SOURCE_TOKENS]==[1,1,3]
    actual=best_survival(CE_DIGITS,counts)
    assert actual["surviving_views"] == {"FGHCDEIAB":6}
    assert control["ce"]["all_order_preserving_9_digit_subsequences"]==1
    return {
        "mode":"DISCOVER/DEVELOP source-native identifier calibration; no solved CE foreground",
        "physical_H108_U5_master_count":len(u5),
        "U5_two_selected_readout_frequencies":dict(counts),
        "archived_source_paths":SOURCE_PATHS,
        "control_token_metadata":tokens,
        "iid_example_reference_calculations":binary_baselines(),
        "exact_order_preserving_9_digit_subsequence_controls":control,
        "source_CE_literal_9_digits_best_D4_survival":actual,
        "limits":[
            "The independent source of the 22-character SAF field is a static ASCII island, not a URL; the contrast is morphological, not a matched process.",
            "Only one source-matched protocol token exists in this bounded archive; no generative distribution is known.",
            "Choosing nine digits from longer tokens is deliberately an extra freedom not required by the CE path.",
            "U5 readout, digit-equality premise, nine-digit extraction and D4 scan have all been historically fitted or inspired, not authorially licensed.",
            "Codebook survival is not acceptance by a historical Playdead consumer.",
        ],
    }


def self_test()->None:
    assert digit_string("a1B2c3")=="123"
    assert multiplicity_pattern("113355789")=="111222"
    assert d4(False,0)=="IABCDEFGH"
    assert d4(True,2)=="FGHCDEIAB"
    assert best_survival("123456789",{"-"*27:1})["maximum_surviving_masters"]==1
    bad_words={c:"" for c in LETTERS}
    bad_words["A"]="x";bad_words["F"]="y"
    assert not accepted_count("534965398",bad_words,"IABCDEFGH")
    print("synthetic string, orientation and duplicate-equality controls: pass")


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    self_test()
    if a.self_test:return
    data=audit()
    out=json.dumps(data,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(out,encoding="utf-8")
        print("saved",a.output)
    else:
        print(out)


if __name__=="__main__":
    main()

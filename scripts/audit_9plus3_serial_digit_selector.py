#!/usr/bin/env python3
"""Experiment 410: in-domain 9+3 serial-digit selector.

Historically proposed 9+3 semantics:
- first nine marks => large number
- last three marks => smaller selector

Sticker-native consumer:
- render the 9-bit number as the same three-digit decimal format used by CE serials
- use the tail's one-of-three physical position to select one decimal digit
- concatenate one selected digit per A-I class

This is bounded and consumer-first; no language scoring follows.
"""

from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-410-9plus3-serial-digit-selector.json"
SERIAL="ABCDEFGHI"
AI_ORDER=tuple(range(9))
NATIVE_ORDER=(8,0,1,2,3,4,5,6,7)  # IABCDEFGH

def body_value(master,j):
    value=0
    for k in range(9):
        value=(value<<1)+(1 if master[j+9*k]=="/" else 0)
    return value

def tail_depth(master,j):
    hits=[d for d in range(3) if master[81+d*9+j]=="/"]
    assert len(hits)==1
    return hits[0]

def selected_digit(master,j):
    serial_like=f"{body_value(master,j):03d}"
    return serial_like[tail_depth(master,j)]

def sequence(master,order):
    return "".join(selected_digit(master,j) for j in order)

def summarize(masters,order):
    counts={}
    for master in masters:
        value=sequence(master,order)
        counts[value]=counts.get(value,0)+1
    return {
        "candidate_count":len(masters),
        "distinct_outputs":len(counts),
        "output_counts":dict(sorted(counts.items())),
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    result={
        "experiment":410,
        "operation":{
            "body":"slash=1, non-slash=0; 9-bit integer",
            "format":"zero-pad body integer to three decimal digits, matching CE serial presentation",
            "selector":"one-slash tail depth 0/1/2 selects the corresponding decimal digit",
        },
        "A_to_I":{
            "U2":summarize(u2,AI_ORDER),
            "U4":summarize(u4,AI_ORDER),
            "U5":summarize(u5,AI_ORDER),
            "E2":summarize(e2,AI_ORDER),
        },
        "native_IABCDEFGH":{
            "U2":summarize(u2,NATIVE_ORDER),
            "U4":summarize(u4,NATIVE_ORDER),
            "U5":summarize(u5,NATIVE_ORDER),
            "E2":summarize(e2,NATIVE_ORDER),
        },
    }

    assert result["A_to_I"]["U2"]["distinct_outputs"]==318
    assert result["A_to_I"]["U4"]["distinct_outputs"]==16
    assert result["A_to_I"]["U5"]["distinct_outputs"]==12
    assert result["A_to_I"]["E2"]["output_counts"]=={
        "320130397":1,
        "328130397":1,
    }
    assert result["native_IABCDEFGH"]["E2"]["output_counts"]=={
        "732013039":1,
        "732813039":1,
    }

    result["interpretation"]=(
        "The historically proposed large-number/small-selector idea admits a sticker-native decimal consumer: "
        "three-digit serial formatting plus tail-position digit selection. The operation sharply compresses U2 "
        "(648 -> 318 distinct strings) and E2 leaves only two outputs, differing at one class-C digit, but no "
        "independent artifact is currently known to consume either nine-digit result. Preserve as a frozen "
        "in-domain interface; do not feed it into additional numeric transforms without a new cue."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Experiment 397: direct 534brn DTMF selector replay against the primary body.

The nine 534brn digits are already registered to native serial classes and the
May-2026 historical cue licenses DTMF row/column as the two cheapest ternary
coordinates. This experiment asks whether either coordinate can act directly as
the body-depth selector d for each class, independently of the sticker tail.
"""

from __future__ import annotations
import json
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-397-534brn-direct-selector-replay.json"
SERIAL="ABCDEFGHI"
LAYOUT=("IAB","CDE","FGH")
NATIVE_LETTERS="IABCDEFGH"
DIGITS="534965398"

def keypad_row(ch):
    d=int(ch)
    return 0 if d<=3 else (1 if d<=6 else 2)

def keypad_col(ch):
    d=int(ch)
    return (d-1)%3

def selector_map(fn):
    return {
        letter:fn(digit)
        for letter,digit in zip(NATIVE_LETTERS,DIGITS)
    }

def decode_dash_pos3(surface):
    out=[]
    for col in range(3):
        rows=[row for row in range(3) if surface[row][col]=="-"]
        if len(rows)!=1:
            return None
        out.append(str(rows[0]))
    return "".join(out)

def symbol_at(master,q,d,row,col):
    letter=LAYOUT[row][col]
    j=SERIAL.index(letter)
    residue=1+27*q+9*d+j
    return master[residue-1]

def external_words(master,selector):
    words=[]
    for q in range(3):
        surface=tuple(
            tuple(
                symbol_at(master,q,selector[LAYOUT[row][col]],row,col)
                for col in range(3)
            )
            for row in range(3)
        )
        words.append(decode_dash_pos3(surface))
    return tuple(words)

def summarize(masters,selector):
    per_q=[0,0,0]
    complete={}
    for master in masters:
        words=external_words(master,selector)
        for q,w in enumerate(words):
            if w is not None:
                per_q[q]+=1
        if None not in words:
            key="/".join(words)
            complete[key]=complete.get(key,0)+1
    return {
        "candidate_count":len(masters),
        "valid_pos3_by_q":per_q,
        "valid_all_three":sum(complete.values()),
        "distinct_complete_outputs":len(complete),
        "complete_output_counts":dict(sorted(complete.items())),
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    selectors={
        "DTMF_row":selector_map(keypad_row),
        "DTMF_column":selector_map(keypad_col),
    }
    ensembles={"U2":u2,"U4":u4,"U5":u5,"E2":e2}

    result={
        "experiment":397,
        "operation":"use registered 534brn DTMF coordinate directly as d selector for each A-I class on each primary Q layer",
        "selectors":selectors,
        "ensembles":{},
    }

    for sname,selector in selectors.items():
        result["ensembles"][sname]={
            name:summarize(masters,selector)
            for name,masters in ensembles.items()
        }

    for selector_result in result["ensembles"].values():
        for ensemble in selector_result.values():
            assert ensemble["valid_pos3_by_q"]==[0,0,0]
            assert ensemble["valid_all_three"]==0

    result["conclusion"]=(
        "Both independently licensed DTMF coordinates are hard negatives as direct body-depth selectors. "
        "Across U2, U4, U5 and the externally selected pair, not even one primary Q surface decodes as "
        "valid dash-POS3 under either external selector. The 534brn digits therefore do not simply replace "
        "the sticker tail S(j) in G5. Preserve their stronger role as an external coordinate relation, and "
        "do not widen into arbitrary digit-derived selectors."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

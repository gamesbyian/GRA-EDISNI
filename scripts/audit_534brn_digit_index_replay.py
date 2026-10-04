#!/usr/bin/env python3
"""Experiment 398: replay the historical 'nine 534brn digits as indices' idea.

The 2025 discussion explicitly noticed nine digits in the solved 534brn path and
suggested they might act as indices for the nine sticker sections. This test
uses exactly that one-based indexing rule against the native class words.
"""

from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-398-534brn-digit-index-replay.json"

DIGITS="534965398"
NATIVE_CLASSES="IABCDEFGH"
SERIAL="ABCDEFGHI"
LEVER={"/":"U","-":"R",".":"L"}

def selected_residue(letter, digit):
    j=SERIAL.index(letter)
    k=int(digit)-1
    return j+1+9*k

def indexed_sequence(master):
    chars=[]
    for letter,digit in zip(NATIVE_CLASSES,DIGITS):
        chars.append(master[selected_residue(letter,digit)-1])
    return "".join(chars)

def summarize(masters):
    counts={}
    for master in masters:
        s=indexed_sequence(master)
        counts[s]=counts.get(s,0)+1
    stable=[]
    for i in range(9):
        stable.append("".join(sorted({s[i] for s in counts for _ in [0]})))
    # stable above is wrong because it only inspects unique output keys; rebuild properly.
    stable=[]
    outputs=[indexed_sequence(m) for m in masters]
    for i in range(9):
        stable.append("".join(sorted({o[i] for o in outputs})))
    return {
        "candidate_count":len(masters),
        "distinct_outputs":len(counts),
        "output_counts":dict(sorted(counts.items())),
        "per_position_symbol_support":stable,
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    selected=[
        {
            "ordinal":i+1,
            "class":letter,
            "digit":int(digit),
            "residue":selected_residue(letter,digit),
        }
        for i,(letter,digit) in enumerate(zip(NATIVE_CLASSES,DIGITS))
    ]

    result={
        "experiment":398,
        "historical_operation":"use the nine decimal digits of 534brn9653f9j8mmd as one-based indices into the nine native sticker class words",
        "digits":DIGITS,
        "native_class_order":NATIVE_CLASSES,
        "selected_positions":selected,
        "ensembles":{
            "U2":summarize(u2),
            "U3":summarize(u3),
            "U4":summarize(u4),
            "U5":summarize(u5),
            "E2":summarize(e2),
        },
    }

    assert result["ensembles"]["U2"]["distinct_outputs"]==2
    assert result["ensembles"]["U3"]["output_counts"]=={"--/--/-/-":216}
    assert result["ensembles"]["U4"]["output_counts"]=={"--/--/-/-":20}
    assert result["ensembles"]["U5"]["output_counts"]=={"--/--/-/-":14}
    assert result["ensembles"]["E2"]["output_counts"]=={"--/--/-/-":2}

    sequence="--/--/-/-"
    result["stable_U4_sequence"]=sequence
    result["lever_projection"]="".join(LEVER[ch] for ch in sequence)
    result["interpretation"]=(
        "The historically proposed digit-as-index operation is unexpectedly stable already at U3: all 216 U3 masters, "
        "all 20 one-shot masters, "
        "all 14 U5 masters, and both external E2 masters produce the same nine-symbol sequence --/--/-/-. U2 has only "
        "two outputs, differing at the fifth selected symbol. However, because digits 1-9 only index the nine-cell primary "
        "body, this operation can never select the dot-bearing tail positions; under the historical lever mapping it is "
        "therefore structurally binary and yields RRURRURUR. No independent nine-command lever consumer is known. Preserve "
        "the sequence as a robust derived feature, not a decode."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Experiment 403: direct serial-order Fractionated Morse hard negative."""

from itertools import permutations
from pathlib import Path
import json

from build_completion_universe import build

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-403-fractionated-morse-direct.json"

SYMBOLS=("-", "/", ".")
FM_SYMBOLS=(".", "-", "x")

TRIGRAMS=[
    a+b+c
    for a in FM_SYMBOLS
    for b in FM_SYMBOLS
    for c in FM_SYMBOLS
    if a+b+c!="xxx"
]
TRIGRAM_TO_LETTER={t:chr(ord("A")+i) for i,t in enumerate(TRIGRAMS)}

def decode(master,mapping):
    out=[]
    for i in range(0,108,3):
        tri="".join(mapping[ch] for ch in master[i:i+3])
        if tri=="xxx":
            return None
        out.append(TRIGRAM_TO_LETTER[tri])
    return "".join(out)

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]

    configs=[]
    for values in permutations(FM_SYMBOLS):
        mapping=dict(zip(SYMBOLS,values))
        valid=[decode(master,mapping) for master in u2]
        valid=[x for x in valid if x is not None]
        configs.append({
            "mapping":mapping,
            "valid_u2_completions":len(valid),
            "distinct_outputs":len(set(valid)),
        })

    assert len(configs)==6
    assert all(x["valid_u2_completions"]==0 for x in configs)

    invariant_uniform_triples={}
    for symbol in SYMBOLS:
        starts=[]
        target=symbol*3
        for i in range(0,108,3):
            if all(master[i:i+3]==target for master in u2):
                starts.append(i+1)
        invariant_uniform_triples[symbol]=starts

    assert invariant_uniform_triples["-"]==[10,70,73]
    assert invariant_uniform_triples["/"]==[28,40,46,64,67,76,79]
    assert invariant_uniform_triples["."]==[97]

    result={
        "experiment":403,
        "historical_cue":"May-2026 Fractionated Morse proposal; proposer already noted serial layout mismatch and suggested rearrangement might be needed",
        "tested_family":"direct serial-order grouping into 36 consecutive triples; standard unkeyed Fractionated Morse trigram table; all 6 sticker-symbol to dot/dash/separator bijections",
        "configurations":configs,
        "invariant_uniform_triples":invariant_uniform_triples,
        "classification":"hard negative",
        "interpretation":(
            "Every symbol assignment fails for every U2 completion. Fractionated Morse excludes the separator "
            "trigram xxx. The serial sticker stream contains U2-invariant triples of all three sticker symbols, "
            "so whichever sticker symbol is assigned to separator x, at least one fixed triple becomes xxx. "
            "Direct serial-order Fractionated Morse is therefore structurally impossible before plaintext. "
            "Reopen only if an independent rearrangement/registration is supplied."
        ),
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

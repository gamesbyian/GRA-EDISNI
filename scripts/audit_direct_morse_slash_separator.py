#!/usr/bin/env python3
"""Experiment 404: direct slash-separated Morse replay over U2."""

from pathlib import Path
import json

from build_completion_universe import build

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-404-direct-morse-slash-separator.json"

VALID={
    ".-","-...","-.-.","-..",".","..-.","--.","....","..",".---",
    "-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-",
    "..-","...-",".--","-..-","-.--","--..",
    "-----",".----","..---","...--","....-",".....","-....","--...",
    "---..","----.",
}

def decode_tokens(master,dot_symbol,dash_symbol):
    tokens=[]
    for raw in [x for x in master.split("/") if x]:
        token="".join("." if ch==dot_symbol else "-" for ch in raw)
        tokens.append(token)
    return tokens

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]

    configs=[]
    for dot_symbol,dash_symbol in ((".","-"),("-",".")):
        valid=0
        min_bad=999
        for master in u2:
            tokens=decode_tokens(master,dot_symbol,dash_symbol)
            bad=sum(t not in VALID for t in tokens)
            min_bad=min(min_bad,bad)
            if bad==0:
                valid+=1
        configs.append({
            "dot_symbol":dot_symbol,
            "dash_symbol":dash_symbol,
            "valid_U2_completions":valid,
            "minimum_invalid_tokens":min_bad,
        })

    assert all(x["valid_U2_completions"]==0 for x in configs)

    # Stronger invariant witness: residues 69 and 76 are slash in all U2
    # completions, while 70..75 are invariant dash.
    for master in u2:
        assert master[68:76]=="/------/"

    result={
        "experiment":404,
        "historical_cue":"Sep-2026 community explicitly asked whether slashes are intended as spaces/separators for Morse",
        "tested_operation":"serial H108 order; slash-run as separator; remaining dot/dash symbols mapped to Morse dot/dash in both possible ways; A-Z and 0-9 International Morse tokens",
        "configs":configs,
        "invariant_witness":{
            "residues":"69..76",
            "pattern":"/------/",
            "consequence":"slash-separated token has length 6 under every U2 completion, which is not any A-Z or 0-9 Morse code regardless of polarity",
        },
        "classification":"hard negative",
        "interpretation":(
            "Direct slash-separated serial-order Morse is impossible across U2. The fixed /------/ witness alone "
            "forces a six-mark token, longer than any A-Z Morse letter and not a digit code. This closes the cheap "
            "historical separator reading without language scoring. Reopen only if an independent artifact supplies "
            "a different traversal, grouping, or meaning for repeated slashes."
        ),
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

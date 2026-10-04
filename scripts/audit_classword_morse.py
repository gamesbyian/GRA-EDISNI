#!/usr/bin/env python3
"""Experiment 405: slash-separated Morse inside the native 12-cell class words."""

from pathlib import Path
import json

from build_completion_universe import build

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-405-classword-morse.json"
SERIAL="ABCDEFGHI"

VALID={
    ".-","-...","-.-.","-..",".","..-.","--.","....","..",".---",
    "-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-",
    "..-","...-",".--","-..-","-.--","--..",
    "-----",".----","..---","...--","....-",".....","-....","--...",
    "---..","----.",
}

def class_word(master,j):
    return "".join(master[j+9*k] for k in range(12))

def parse(word,dot_symbol,dash_symbol):
    tokens=[]
    for raw in [x for x in word.split("/") if x]:
        tokens.append("".join("." if ch==dot_symbol else "-" for ch in raw))
    return tokens

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]

    result={
        "experiment":405,
        "historical_cues":[
            "game assets use MORSE_Dot/MORSE_Dash/MORSE_Slash names",
            "Sep-2026 community asked whether slash acts as Morse separator",
            "native 9x12 representation supplies nine independent 12-cell words",
        ],
        "configs":[],
    }

    for dot_symbol,dash_symbol in ((".","-"),("-",".")):
        valid_all=0
        bad_by_class={letter:0 for letter in SERIAL}
        for master in u2:
            ok=True
            for j,letter in enumerate(SERIAL):
                tokens=parse(class_word(master,j),dot_symbol,dash_symbol)
                if not all(token in VALID for token in tokens):
                    bad_by_class[letter]+=1
                    ok=False
            if ok:
                valid_all+=1
        result["configs"].append({
            "dot_symbol":dot_symbol,
            "dash_symbol":dash_symbol,
            "valid_all_nine_classwords":valid_all,
            "bad_completion_count_by_class":bad_by_class,
        })

    assert all(x["valid_all_nine_classwords"]==0 for x in result["configs"])
    assert all(x["bad_completion_count_by_class"]["H"]==648 for x in result["configs"])
    assert {class_word(m,7) for m in u2}=={"-/------/../"}

    result["invariant_witness"]={
        "class":"H",
        "word":"-/------/../",
        "slash_split_raw_tokens":["-","------",".."],
        "consequence":"middle token has six Morse marks under either polarity and is invalid as A-Z/0-9",
    }
    result["classification"]="hard negative"
    result["interpretation"]=(
        "Rearranging the stream into the independently native nine 12-cell class words does not rescue ordinary "
        "slash-separated Morse. Class H is fixed across all U2 completions as -/------/../, forcing a six-mark "
        "Morse token under either polarity. Thus both direct serial Morse and native-class-word Morse are closed "
        "without any missing-sticker dependence."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

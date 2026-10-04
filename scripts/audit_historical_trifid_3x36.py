#!/usr/bin/env python3
"""Experiment 402: replay the historical 3x36 Trifid proposal against U2.

The Dec-2022 discussion explicitly arranged the 108 sticker symbols as 3x36,
treated each column as a Trifid coordinate, and reported the partial plaintext
"--cus------------h--b--ts-----------".

This audit exhausts the cheap standard direct-cube family:
- all 6 bijections from sticker symbols to coordinate digits 1..3;
- all 6 permutations of the three coordinate axes;
- all 648 coherent U2 completions.

No keyworded alphabets or semantic scoring are admitted.
"""

from itertools import permutations
from pathlib import Path
import json

from build_completion_universe import build

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-402-trifid-3x36-replay.json"

SYMBOLS=("-", "/", ".")
LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZ#"
CLAIMS={3:"C",4:"U",5:"S",18:"H",21:"B",24:"T",25:"S"}

def coord_letter(coord):
    a,b,c=coord
    idx=(a-1)*9+(b-1)*3+(c-1)
    return LETTERS[idx]

def column_triple(master,col):
    i=col-1
    return (master[i],master[i+36],master[i+72])

def decode_col(master,col,symbol_map,axis_perm):
    raw=tuple(symbol_map[ch] for ch in column_triple(master,col))
    coord=tuple(raw[i] for i in axis_perm)
    return coord_letter(coord)

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]

    configs=[]
    for digits in permutations((1,2,3)):
        symbol_map=dict(zip(SYMBOLS,digits))
        for axis_perm in permutations((0,1,2)):
            survivors=[]
            for idx,master in enumerate(u2):
                if all(
                    decode_col(master,pos,symbol_map,axis_perm)==letter
                    for pos,letter in CLAIMS.items()
                ):
                    survivors.append(idx)
            configs.append({
                "symbol_map":symbol_map,
                "axis_permutation":axis_perm,
                "survivors":len(survivors),
            })

    assert len(configs)==36
    assert max(x["survivors"] for x in configs)==0

    # The first two historically claimed letters C,U alone uniquely force a
    # single cheap config. Under that config, current U2 fixes col 5 to the
    # 27th cube cell (#), contradicting the historical S before later letters.
    first_two=[]
    for digits in permutations((1,2,3)):
        symbol_map=dict(zip(SYMBOLS,digits))
        for axis_perm in permutations((0,1,2)):
            ok=True
            for pos,letter in ((3,"C"),(4,"U")):
                if not all(decode_col(m,pos,symbol_map,axis_perm)==letter for m in u2):
                    ok=False
                    break
            if ok:
                first_two.append((symbol_map,axis_perm))
    assert len(first_two)==1
    sm,ap=first_two[0]
    pos5={decode_col(m,5,sm,ap) for m in u2}
    assert pos5=={"#"}

    result={
        "experiment":402,
        "historical_partial":"--cus------------h--b--ts-----------",
        "cheap_family":{
            "symbol_to_digit_bijections":6,
            "axis_permutations":6,
            "total_decoder_configs":36,
            "U2_completions":648,
        },
        "full_partial_match_survivors":0,
        "first_two_CU_unique_config":{
            "symbol_map":sm,
            "axis_permutation":ap,
            "U2_position_5":sorted(pos5),
            "historical_position_5":"S",
        },
        "classification":"hard negative for standard unkeyed direct-cube Trifid over the historical 3x36 registration",
        "interpretation":(
            "The original Trifid idea was specific enough to replay, but the cheap standard family cannot "
            "coexist with the current broad physical completion universe and the old seven-letter partial. "
            "Matching C/U already forces one decoder and that decoder makes column 5 invariantly the 27th "
            "cube cell, not S. Reopen only if the historical solver's exact keyed alphabet or a different "
            "Trifid period/fractionation rule is recovered; do not search arbitrary keys."
        ),
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

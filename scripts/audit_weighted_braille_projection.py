#!/usr/bin/env python3
"""Experiment 394: bounded Braille projection over coherent sticker completions."""

from __future__ import annotations
import json
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-394-weighted-braille-projection.json"
SERIAL="ABCDEFGHI"

LETTER_DOTS={
    "a":{1},"b":{1,2},"c":{1,4},"d":{1,4,5},"e":{1,5},
    "f":{1,2,4},"g":{1,2,4,5},"h":{1,2,5},"i":{2,4},"j":{2,4,5},
    "k":{1,3},"l":{1,2,3},"m":{1,3,4},"n":{1,3,4,5},"o":{1,3,5},
    "p":{1,2,3,4},"q":{1,2,3,4,5},"r":{1,2,3,5},"s":{2,3,4},
    "t":{2,3,4,5},"u":{1,3,6},"v":{1,2,3,6},"w":{2,4,5,6},
    "x":{1,3,4,6},"y":{1,3,4,5,6},"z":{1,3,5,6},
}
MASK_TO_LETTER={
    sum(1<<(d-1) for d in dots):letter
    for letter,dots in LETTER_DOTS.items()
}

def project(master,row_order,complement=False):
    # Natural 9x12 carrier: one row per A-I class, one column per class-word position.
    values=[
        [1 if master[SERIAL.index(letter)+9*k]=="/" else 0 for k in range(12)]
        for letter in row_order
    ]
    masks=[]
    for row0 in range(0,9,3):
        for col0 in range(0,12,2):
            bits=(
                [values[row0+i][col0] for i in range(3)]
                +[values[row0+i][col0+1] for i in range(3)]
            )
            if complement:
                bits=[1-b for b in bits]
            masks.append(sum(bit<<i for i,bit in enumerate(bits)))
    return tuple(masks)

def summarize(masters,row_order,complement):
    outputs=[project(m,row_order,complement) for m in masters]
    stable=[
        i for i in range(18)
        if len({o[i] for o in outputs})==1
    ]
    stable_letters=[
        {"cell":i,"letter":MASK_TO_LETTER[outputs[0][i]]}
        for i in stable
        if outputs[0][i] in MASK_TO_LETTER
    ]

    longest=0; run=0
    for i in range(18):
        good=i in stable and outputs[0][i] in MASK_TO_LETTER
        run=run+1 if good else 0
        longest=max(longest,run)

    alphabetic_counts=[
        sum(mask in MASK_TO_LETTER for mask in output)
        for output in outputs
    ]
    return {
        "stable_cells":len(stable),
        "stable_cell_indices":stable,
        "stable_alphabetic_cells":stable_letters,
        "longest_consecutive_stable_alphabetic_run":longest,
        "alphabetic_cells_per_completion_min":min(alphabetic_counts),
        "alphabetic_cells_per_completion_max":max(alphabetic_counts),
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,_u5=machine_layers()

    configs={
        "serial_A_to_I_slash_raised":("ABCDEFGHI",False),
        "serial_A_to_I_slash_empty":("ABCDEFGHI",True),
        "physical_IAB_CDE_FGH_slash_raised":("IABCDEFGH",False),
        "physical_IAB_CDE_FGH_slash_empty":("IABCDEFGH",True),
    }
    result={
        "experiment":394,
        "operation_family":"standard six-dot Braille over the natural complete 9x12 class-word carrier",
        "binary_projection":"slash versus non-slash; complement tested as the only binary polarity control",
        "ensembles":{},
    }
    for name,masters in (("U2",u2),("U4",u4)):
        result["ensembles"][name]={}
        for cfg,(order,comp) in configs.items():
            result["ensembles"][name][cfg]=summarize(masters,order,comp)

    # Regression values from the exact enumeration.
    assert result["ensembles"]["U2"]["serial_A_to_I_slash_raised"]["stable_cells"]==6
    assert result["ensembles"]["U4"]["serial_A_to_I_slash_raised"]["stable_cells"]==8
    assert max(
        cfg["longest_consecutive_stable_alphabetic_run"]
        for ens in result["ensembles"].values()
        for cfg in ens.values()
    )<=2

    result["conclusion"]=(
        "The historical Xbox puzzle licenses Braille as an operation family, and the completed 9x12 sticker "
        "carrier admits a natural 3x2 Braille tiling. Across broad U2 and one-shot U4 coherent completions, "
        "however, no tested natural row order/polarity yields a stable alphabetic run longer than two cells. "
        "The projection produces scattered letter-like cells but no ensemble-stable message. Close this cheap "
        "Braille projection unless a new artifact independently specifies a different registration."
    )
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

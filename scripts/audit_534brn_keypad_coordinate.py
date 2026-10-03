#!/usr/bin/env python3
"""Experiment 380: test the historically cued DTMF-keypad coordinates of 534brn digits."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-380-534brn-keypad-coordinate.json"

DIGITS = "534965398"
ONE_SHOT = {
    "102/002/120",
    "102/012/100",
    "102/022/100",
    "112/012/100",
    "112/012/120",
    "122/022/100",
}

# Standard DTMF telephone layout, exactly as in the historical archive image:
# 1 2 3
# 4 5 6
# 7 8 9
KEYPAD = {
    "1": (0,0), "2": (0,1), "3": (0,2),
    "4": (1,0), "5": (1,1), "6": (1,2),
    "7": (2,0), "8": (2,1), "9": (2,2),
}

def as_grid(seq):
    return tuple(tuple(seq[r*3+c] for c in range(3)) for r in range(3))

def rot90_cw(g):
    return tuple(tuple(g[2-r][c] for r in range(3)) for c in range(3))

def mirror_lr(g):
    return tuple(tuple(reversed(row)) for row in g)

def d4(g):
    out=[]
    cur=g
    names=("identity","rot90_cw","rot180","rot270_cw")
    for name in names:
        out.append((name,cur))
        out.append((name+"_mirror_lr",mirror_lr(cur)))
        cur=rot90_cw(cur)
    seen=set()
    uniq=[]
    for name,x in out:
        if x not in seen:
            seen.add(x)
            uniq.append((name,x))
    return uniq

def fmt(g):
    return "/".join("".join(map(str,row)) for row in g)

def main():
    row_stream = [KEYPAD[d][0] for d in DIGITS]
    col_stream = [KEYPAD[d][1] for d in DIGITS]
    row_grid = as_grid(row_stream)
    col_grid = as_grid(col_stream)

    row_hits=[{"orientation":name,"state":fmt(g)} for name,g in d4(row_grid) if fmt(g) in ONE_SHOT]
    col_hits=[{"orientation":name,"state":fmt(g)} for name,g in d4(col_grid) if fmt(g) in ONE_SHOT]

    assert row_hits == [{"orientation":"rot270_cw","state":"112/012/120"}]
    assert col_hits == []

    result={
        "experiment":380,
        "historical_cue":{
            "date":"2026-05-22",
            "source":"Playdead Unofficial solving-breakout archive",
            "proposal":"old-phone / DTMF keypad as a sticker-puzzle model; a DTMF keypad image was attached before the current machine work",
            "layout":["123","456","789"]
        },
        "external_artifact":"dat/534brn9653f9j8mmd",
        "digit_stream":DIGITS,
        "keypad_coordinates":{
            "row_stream":"".join(map(str,row_stream)),
            "column_stream":"".join(map(str,col_stream)),
            "row_grid":[ "".join(map(str,row)) for row in row_grid ],
            "column_grid":[ "".join(map(str,row)) for row in col_grid ]
        },
        "one_shot_family":sorted(ONE_SHOT),
        "d4_results":{
            "row_coordinate_hits":row_hits,
            "column_coordinate_hits":col_hits
        },
        "interpretation":(
            "Experiment 378's 1-3/4-6/7-9 ternary map is exactly the row coordinate of the historically proposed "
            "DTMF keypad, not merely an arbitrary numeric binning. The alternative coordinate supplied by the same "
            "keypad, column, does not hit the preregistered one-shot family under any D4 symmetry. Thus the historical "
            "keypad cue selectively supports the successful transform. Sequence-to-3x3 registration and the exact "
            "90-degree direction remain not independently specified."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Experiment 382: test whether the solved CE 3x3 fixes the 534brn digit-to-cell registration."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-382-534brn-native-cell-registration.json"

DIGITS = "534965398"
PHYSICAL_LAYOUT = (
    ("I","A","B"),
    ("C","D","E"),
    ("F","G","H"),
)
LETTER_ORDER = "ABCDEFGHI"
ONE_SHOT = {
    "102/002/120",
    "102/012/100",
    "102/022/100",
    "112/012/100",
    "112/012/120",
    "122/022/100",
}

KEYPAD_ROW = {
    "1":0,"2":0,"3":0,
    "4":1,"5":1,"6":1,
    "7":2,"8":2,"9":2,
}

def rot90_cw(g):
    return tuple(tuple(g[2-r][c] for r in range(3)) for c in range(3))

def mirror_lr(g):
    return tuple(tuple(reversed(row)) for row in g)

def d4(g):
    out=[]
    cur=g
    for name in ("identity","rot90_cw","rot180","rot270_cw"):
        out.append((name,cur))
        out.append((name+"_mirror_lr",mirror_lr(cur)))
        cur=rot90_cw(cur)
    seen=set()
    uniq=[]
    for name,g in out:
        if g not in seen:
            seen.add(g)
            uniq.append((name,g))
    return uniq

def fmt(g):
    return "/".join("".join(map(str,row)) for row in g)

def physical_from_native_mod9():
    # Serial-number residue classes mod 9 are:
    # 0=I, 1=A, 2=B, ... 8=H.
    # Therefore the solved physical layout IAB/CDE/FGH is exactly 0..8 row-major.
    vals={}
    native_letters=("I","A","B","C","D","E","F","G","H")
    for k,letter in enumerate(native_letters):
        vals[letter]=KEYPAD_ROW[DIGITS[k]]
    return tuple(tuple(vals[x] for x in row) for row in PHYSICAL_LAYOUT)

def physical_from_letter_order():
    # Natural control: assign URL digits to community labels A..I in alphabetic order,
    # then render those values in the solved physical layout.
    vals={letter:KEYPAD_ROW[DIGITS[k]] for k,letter in enumerate(LETTER_ORDER)}
    return tuple(tuple(vals[x] for x in row) for row in PHYSICAL_LAYOUT)

def hits(g):
    return [
        {"orientation":name,"state":fmt(x)}
        for name,x in d4(g)
        if fmt(x) in ONE_SHOT
    ]

def main():
    native=physical_from_native_mod9()
    letter=physical_from_letter_order()

    assert fmt(native) == "101/211/022"
    assert hits(native) == [{"orientation":"rot270_cw","state":"112/012/120"}]

    # The alphabetic A..I registration is an equally obvious but physically
    # different control; it should not hit the one-shot family.
    assert fmt(letter) == "210/121/102"
    assert hits(letter) == []

    result={
        "experiment":382,
        "source_geometry":{
            "solved_background_layout":["IAB","CDE","FGH"],
            "native_serial_mod9_classes":{
                "0":"I","1":"A","2":"B","3":"C","4":"D",
                "5":"E","6":"F","7":"G","8":"H"
            },
            "consequence":"The solved physical layout is exactly native serial residue classes 0..8 in row-major order."
        },
        "historical_support":{
            "date":"2026-08-10",
            "finding":"community explicitly noted that the first class should be 000/I rather than 001/A because I is the top-left tile in the first sticker puzzle"
        },
        "digit_stream":DIGITS,
        "keypad_row_registered_by_native_mod9":{
            "grid":["101","211","022"],
            "hits":hits(native)
        },
        "control_alphabetic_A_to_I_registration":{
            "grid":["210","121","102"],
            "hits":hits(letter)
        },
        "interpretation":(
            "Experiment 378's digit-string ordinal -> 3x3 cell registration is not arbitrary once the solved "
            "background geometry is expressed in native serial-number modulo-9 classes. The physical layout "
            "IAB/CDE/FGH is exactly 0,1,2/3,4,5/6,7,8, so assigning the 1st through 9th URL digits to those "
            "positions in sequence is the native serial registration. The competing alphabetic A-I assignment "
            "does not hit the one-shot family under D4. This removes the ordinal-to-cell mapping as a major free "
            "parameter; the remaining unresolved registration is the quarter-turn direction."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

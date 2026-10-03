#!/usr/bin/env python3
"""Experiment 383: classify the remaining 534brn orientation burden after native registration."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-383-534brn-orientation-burden.json"

SOURCE = (
    (1,0,1),
    (2,1,1),
    (0,2,2),
)

TARGETS = {
    "102/002/120",
    "102/012/100",
    "102/022/100",
    "112/012/100",
    "112/012/120",
    "122/022/100",
}

def rot90_cw(g):
    return tuple(tuple(g[2-r][c] for r in range(3)) for c in range(3))

def mirror_lr(g):
    return tuple(tuple(reversed(row)) for row in g)

def fmt(g):
    return "/".join("".join(map(str,row)) for row in g)

def transforms():
    out=[]
    cur=SOURCE
    for name in ("identity","rot90_cw","rot180","rot90_ccw"):
        out.append((name,cur))
        out.append((name+"_mirror_lr",mirror_lr(cur)))
        cur=rot90_cw(cur)
    # Keep unique in first-named order.
    seen=set()
    unique=[]
    for name,g in out:
        if g not in seen:
            seen.add(g)
            unique.append((name,g))
    return unique

def swaps_axes(name):
    # In this naming convention, quarter-turns and diagonal reflections swap axes.
    return name in {
        "rot90_cw",
        "rot90_ccw",
        "identity_mirror_lr_rotated_equiv_placeholder"
    }

def classify(name):
    # Explicit D4 classification, avoiding ambiguity from generated names.
    table={
        "identity":"axis_preserving",
        "identity_mirror_lr":"axis_preserving",
        "rot90_cw":"axis_swapping",
        "rot90_cw_mirror_lr":"axis_swapping",
        "rot180":"axis_preserving",
        "rot180_mirror_lr":"axis_preserving",
        "rot90_ccw":"axis_swapping",
        "rot90_ccw_mirror_lr":"axis_swapping",
    }
    return table[name]

def main():
    records=[]
    for name,g in transforms():
        state=fmt(g)
        records.append({
            "transform":name,
            "class":classify(name),
            "state":state,
            "one_shot_hit":state in TARGETS,
        })

    hits=[r for r in records if r["one_shot_hit"]]
    assert hits == [{
        "transform":"rot90_ccw",
        "class":"axis_swapping",
        "state":"112/012/120",
        "one_shot_hit":True,
    }]

    axis_preserving=[r for r in records if r["class"]=="axis_preserving"]
    axis_swapping=[r for r in records if r["class"]=="axis_swapping"]
    assert sum(r["one_shot_hit"] for r in axis_preserving)==0
    assert sum(r["one_shot_hit"] for r in axis_swapping)==1

    cw=[r for r in records if r["transform"]=="rot90_cw"][0]
    ccw=[r for r in records if r["transform"]=="rot90_ccw"][0]
    assert not cw["one_shot_hit"] and ccw["one_shot_hit"]

    result={
        "experiment":383,
        "source_grid":["101","211","022"],
        "d4_records":records,
        "summary":{
            "axis_preserving_hits":0,
            "axis_swapping_hits":1,
            "unique_hit":"rot90_ccw -> 112/012/120",
            "exact_xbox_direction_control":"rot90_cw does not hit"
        },
        "coordinate_typing":{
            "source_axes":"background physical row r x physical column c",
            "one_shot_axes":"outer layer Q x physical column c; cell value is minority row r",
            "important_consequence":"The source and one-shot surfaces share a physical-column coordinate. Therefore the successful quarter-turn is not pure gauge: it swaps axes rather than preserving the shared c axis."
        },
        "historical_provenance":{
            "quarter_turn_family":"Playdead-authored Xbox printer solution requires a 90-degree clockwise rotation before Braille readout",
            "sticker_specific_axis_rearrangement":"Nov 2025 community discussion proposed transposing/reorganizing sticker 3x3 cells in relation to 534brn",
            "direction_problem":"The exact demonstrated Xbox direction is clockwise, while the 534brn candidate requires counter-clockwise."
        },
        "interpretation":"Native cell registration removes the row-major-placement concern, but the final 90-degree CCW operation remains substantive rather than a harmless orientation gauge because it swaps the shared physical-column axis with the other grid axis. The historical corpus licenses quarter-turn/transpose as an operation family, but exact reuse of the documented Xbox clockwise direction fails. The candidate therefore has one clean unresolved bit of directional/axis-registration evidence remaining."
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

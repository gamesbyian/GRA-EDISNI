#!/usr/bin/env python3
"""Experiment 327: literal-stroke Pigpen compatibility audit.

This intentionally tests only the strongest literal interpretation:
printed slash and dash marks are treated as strokes, and only D4
rotations/reflections are allowed. It does not test categorical encodings
where one mark means blank/filled or where a separate rule synthesizes edges.
"""

from __future__ import annotations
import argparse, csv, json
from pathlib import Path

CLASSES="ABCDEFGHI"

def load(path: Path) -> dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s:
                raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    rows={}
    mixed=[]
    for i,c in enumerate(CLASSES):
        body=[obs.get(1+i+9*k,"?") for k in range(9)]
        known=[x for x in body if x in "/-"]
        rows[c]={"body":"".join(body),"slash":known.count("/"),"dash":known.count("-"),
                 "has_both":"/" in known and "-" in known}
        if rows[c]["has_both"]: mixed.append(c)

    out={
      "orientation_families":{
        "dash_under_D4":["horizontal","vertical"],
        "slash_under_D4":["diagonal_forward","diagonal_back"],
        "standard_pigpen_tic_tac_toe_family":"orthogonal_only",
        "standard_pigpen_x_family":"diagonal_only",
      },
      "classes":rows,
      "classes_with_both_observed_body_marks":mixed,
      "literal_both_marks_as_ink_compatible_classes":[],
      "note":"D4 preserves orthogonal-vs-diagonal orientation families. A body containing both literal dash and slash strokes cannot become a single standard Pigpen glyph, whose tic-tac-toe and X families do not mix those orientation families."
    }
    assert mixed==list(CLASSES)
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()

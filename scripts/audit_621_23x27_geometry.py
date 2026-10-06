#!/usr/bin/env python3
"""Experiment 427: test the two natural 621 = 23*27 serial rectangles.

No decoding is attempted. The audit asks only which orientation preserves the
already-established period-108, 27-cell quarter, and period-9 background
boundaries when serials are written consecutively.
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-427-621-23x27-geometry.json"

TOTAL=621

def analyze(rows:int, cols:int)->dict:
    assert rows*cols==TOTAL
    row_starts=[1+r*cols for r in range(rows)]
    row_h108=[((s-1)%108)+1 for s in row_starts]
    row_bg=[((s-1)%9)+1 for s in row_starts]
    boundaries_27=sum(1 for s in row_starts if (s-1)%27==0)
    boundaries_9=sum(1 for s in row_starts if (s-1)%9==0)
    boundaries_108=sum(1 for s in row_starts if (s-1)%108==0)
    return {
        "rows":rows,"cols":cols,
        "row_width_mod_108":cols%108,
        "row_width_mod_27":cols%27,
        "row_width_mod_9":cols%9,
        "row_start_h108_residues":row_h108,
        "row_start_background_phases":row_bg,
        "rows_start_on_27_boundary":boundaries_27,
        "rows_start_on_9_boundary":boundaries_9,
        "rows_start_on_108_boundary":boundaries_108,
    }

def main():
    a=analyze(23,27)
    b=analyze(27,23)
    assert a["row_width_mod_27"]==0
    assert a["row_width_mod_9"]==0
    assert a["row_start_h108_residues"]==[1,28,55,82]*5+[1,28,55]
    assert a["rows_start_on_27_boundary"]==23
    assert a["rows_start_on_9_boundary"]==23
    assert b["row_width_mod_27"]==23
    assert b["row_width_mod_9"]==5
    assert b["rows_start_on_27_boundary"]==1
    assert b["rows_start_on_9_boundary"]==3

    serial597={
      "serial":597,
      "row_23x27":(597-1)//27+1,
      "col_23x27":(597-1)%27+1,
      "h108_residue":(597-1)%108+1,
    }
    assert serial597=={"serial":597,"row_23x27":23,"col_23x27":3,"h108_residue":57}

    result={
      "experiment":427,
      "total":621,
      "factorizations":["23x27","27x23"],
      "orientation_23_rows_27_columns":a,
      "orientation_27_rows_23_columns":b,
      "serial_597_location":serial597,
      "interpretation":(
        "The 23x27 orientation is canonically compatible with the pre-existing carrier: "
        "every row is one complete 27-cell quarter and three complete period-9 background cycles; "
        "row starts cycle through H108 residues 1,28,55,82 and repeat every four rows. "
        "Across 23 rows this gives five full H108 cycles followed by the three primary quarters. "
        "The transposed 27x23 orientation has no such alignment. This privileges 23 rows of 27 "
        "if 621 is independently established, but it does not establish 621 as the production total."
      )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

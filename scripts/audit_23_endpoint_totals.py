#!/usr/bin/env python3
"""Experiment 426: bounded 23-sensitive production-total audit.

Compare only endpoint/total candidates already present in the research program
before the Hollerith-23 observation. Score no free-form arithmetic. Report
pre-existing carrier relations to 9, 27, 81, 108 plus divisibility by 23.
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-426-23-endpoint-audit.json"

CANDIDATES=(598,600,603,612,621,630,639,648)

def row(n:int)->dict:
    return {
        "total":n,
        "divisible_by_9":n%9==0,
        "divisible_by_23":n%23==0,
        "divisible_by_27":n%27==0,
        "divisible_by_81":n%81==0,
        "divisible_by_108":n%108==0,
        "h108_remainder":n%108,
        "h108_boundary_0_or_81":n%108 in (0,81),
        "quotient_23": n//23 if n%23==0 else None,
        "quotient_27": n//27 if n%27==0 else None,
        "quotient_108": n//108 if n%108==0 else None,
    }

def main():
    rows=[row(n) for n in CANDIDATES]
    by={r["total"]:r for r in rows}
    assert by[598]["divisible_by_23"] and by[598]["quotient_23"]==26
    assert by[621]["divisible_by_23"] and by[621]["quotient_23"]==27
    assert by[621]["divisible_by_27"] and by[621]["quotient_27"]==23
    assert by[621]["h108_remainder"]==81
    assert by[648]["divisible_by_108"] and by[648]["quotient_108"]==6
    assert [r["total"] for r in rows if r["divisible_by_23"]]==[598,621]
    assert [r["total"] for r in rows if r["divisible_by_23"] and r["divisible_by_27"]]==[621]
    result={
      "experiment":426,
      "candidate_totals":list(CANDIDATES),
      "candidate_set_provenance":"frozen from endpoint totals already considered before Experiment 424's Hollerith-23 observation",
      "features":{
        "legacy_carrier":[9,27,81,108],
        "new_number":[23],
        "guardrail":"No arbitrary sums/products or post-hoc nearby totals are scored."
      },
      "rows":rows,
      "findings":{
        "598":"23×26. No alignment with 9, 27, 81, or 108 as a total.",
        "621":"23×27 = 27×23; also 69×9; and 621 mod 108 = 81, so a 1-based run through 621 ends exactly after the 81-cell primary region of cycle 6, before its 27-cell tail.",
        "648":"6×108 = 24×27 = 8×81 = 72×9; strongest pre-23 carrier-aligned endpoint, but not divisible by 23."
      },
      "interpretation":"621 is uniquely enriched for the newly salient 23 while also respecting independently established 27 and 81/108 structure. 648 remains more strongly aligned to the legacy H108 carrier. 598 gains only a 23 factor and otherwise lacks established carrier alignment. None is production evidence.",
      "numbering_caution":"A total of 598 is not implied by observed serial 597 unless the physical serial run is known to be zero-based and contiguous; current evidence does not establish that. A 001..621 interpretation of total 621 is likewise a hypothesis, not a manufacturing fact."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

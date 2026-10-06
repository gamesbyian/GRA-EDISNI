#!/usr/bin/env python3
"""Experiment 426: bounded 23-aware endpoint audit.

Compare only historically discussed / directly motivated total-count candidates
against structural quantities established before the Hollerith observation.
No free search over arbitrary totals and no weighted score.
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-426-endpoint-23-audit.json"

CANDIDATES = [598, 600, 603, 612, 621, 630, 639, 648]
STRUCTURAL = [9, 23, 27, 81, 108]


def features(n: int) -> dict:
    return {
        "total": n,
        "distance_above_highest_observed_597": n - 597,
        "divisible_by": [d for d in STRUCTURAL if n % d == 0],
        "h108_remainder": n % 108,
        "ends_on_h108_primary_boundary_81": n % 108 == 81,
        "ends_on_h108_cycle_boundary_0": n % 108 == 0,
        "exact_23_blocks": n // 23 if n % 23 == 0 else None,
        "exact_27_blocks": n // 27 if n % 27 == 0 else None,
        "as_23_times_27": n == 23 * 27,
        "as_6_times_108": n == 6 * 108,
    }


def main() -> None:
    rows = [features(n) for n in CANDIDATES]

    assert 23 * 26 == 598
    assert 23 * 27 == 621
    assert 621 == 5 * 108 + 81
    assert 648 == 6 * 108

    by_total = {r["total"]: r for r in rows}
    assert by_total[621]["divisible_by"] == [9, 23, 27]
    assert by_total[621]["ends_on_h108_primary_boundary_81"]
    assert by_total[648]["divisible_by"] == [9, 27, 81, 108]
    assert by_total[648]["ends_on_h108_cycle_boundary_0"]
    assert by_total[598]["divisible_by"] == [23]

    result = {
        "experiment": 426,
        "candidate_totals": CANDIDATES,
        "preexisting_structural_quantities": {
            "9": "background / class period",
            "23": "newly salient only through the IBM 029 period-code arithmetic echo; not previously established as a sticker-carrier dimension",
            "27": "native H108 tail / q-block scale",
            "81": "native primary region",
            "108": "established foreground period",
        },
        "rows": rows,
        "exact_observations": {
            "598": "23*26; otherwise no exact alignment to 9/27/81/108",
            "621": "23*27 = 5*108+81; exactly 23 blocks of 27 and 27 blocks of 23; ends at the 81/27 H108 boundary",
            "648": "6*108 = 8*81 = 24*27; closes six complete H108 cycles but is not divisible by 23",
        },
        "pareto_note": (
            "Within the frozen candidate set, 621 and 648 are the two structurally exceptional totals. "
            "621 uniquely combines the newly salient factor 23 with the pre-existing 27 and H108 residue-81 boundary. "
            "648 uniquely closes the full 108-period carrier and is also divisible by 81 and 27. "
            "No weighted score is assigned because the features are nested and not independent."
        ),
        "manufacturing_guardrail": (
            "Serial 597 proves only that 597 exists. It does not establish a total production count, "
            "a zero-based serial 000, or a contiguous run. Historical ~600-copy claims remain speculation."
        ),
        "interpretation": (
            "If 23 later receives an independent authorial cue, 621 becomes a notably economical endpoint because "
            "it simultaneously equals 23*27 and terminates at the established 81/27 boundary of H108. "
            "Without such a cue, 648 remains at least as natural from the carrier alone because it closes six complete cycles."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

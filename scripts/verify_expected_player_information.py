#!/usr/bin/env python3
"""Validate the R6 expected-player-information summary."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "expected-player-information.json"

def main() -> None:
    data=json.loads(DATA.read_text(encoding="utf-8"))
    assert data["experiment"] == 324
    tiers={x["tier"]:x for x in data["information_tiers"]}
    assert "single_owner" in tiers
    assert tiers["current_archive"]["corpus_size_physical_records"] == 82
    assert tiers["current_archive"]["distinct_h108_residues"] == 65
    assert tiers["current_archive"]["missing_h108_residues"] == 43
    assert tiers["current_archive"]["one_slash_tail_completions"] == 36
    inf={x["inference"]:x for x in data["design_inferences"]}
    assert inf["communal pooling was required"]["confidence"] == "high"
    assert inf["near-complete ~600 physical collection was required"]["confidence"] == "unsupported"
    assert inf["near-complete 108 unique foreground cells were required"]["confidence"] == "unsupported"
    print(json.dumps({
        "tiers": list(tiers),
        "current_archive": tiers["current_archive"],
        "design_inferences": data["design_inferences"],
    }, indent=2))

if __name__ == "__main__":
    main()

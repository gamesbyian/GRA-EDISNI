#!/usr/bin/env python3
"""Validate the epistemic-reset R4 premise classification."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "reset-premise-classification.json"

def main() -> None:
    data=json.loads(PATH.read_text(encoding="utf-8"))
    nodes=data["transition_premises"]
    ids=[n["id"] for n in nodes]
    assert ids == ["O1","O2","G1","G3","G5","G6","G7"], ids
    assert len(nodes)==7
    by_id={n["id"]:n for n in nodes}
    assert by_id["O1"]["primary_evidentiary_type"]=="directly_observed"
    assert by_id["O2"]["primary_evidentiary_type"]=="mixed"
    assert by_id["G3"]["primary_evidentiary_type"]=="historically_motivated"
    assert {n["id"] for n in nodes if n["primary_evidentiary_type"]=="selected_because_it_preserves_the_machine"}=={"G6","G7"}
    assert data["summary"]["independently_derived_transition_grammar_nodes"]==[]
    assert data["summary"]["highest_priority_circularity_targets"]==["G7","G6","G5"]
    print(json.dumps(data["summary"], indent=2))

if __name__=="__main__":
    main()

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
    assert by_id["G1"]["primary_evidentiary_type"]=="mixed"
    assert by_id["G3"]["primary_evidentiary_type"]=="historically_motivated"
    assert {n["id"] for n in nodes if n["primary_evidentiary_type"]=="selected_because_it_preserves_the_machine"}==set()
    assert {n["id"] for n in nodes if n["primary_evidentiary_type"]=="generic_simplicity_prior"}=={"G5","G6","G7"}
    assert data["summary"]["mixed_grammar_nodes"]==["G1"]
    assert data["summary"]["independently_derived_transition_grammar_nodes"]==[]
    assert data["summary"]["machine_preservation_risk_nodes"]==[]
    assert data["summary"]["highest_priority_circularity_targets"]==["G6"]
    g1_components={c["claim"]:c["type"] for c in by_id["G1"]["components"]}
    assert g1_components["minority row gives a three-valued coordinate"]=="genuinely_derived_from_independent_evidence"
    assert g1_components["shared row-label orientation / arithmetic or address semantics for those coordinates"]=="generic_simplicity_prior"
    assert data["last_updated_experiment"]==356
    print(json.dumps(data["summary"], indent=2))

if __name__=="__main__":
    main()

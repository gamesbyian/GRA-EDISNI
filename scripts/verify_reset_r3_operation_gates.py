#!/usr/bin/env python3
"""Validate the R3 operation evidence-gate matrix."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "reset-r3-operation-gates.json"

def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    gates = data["gates"]
    ids = [g["id"] for g in gates]
    assert len(ids) == len(set(ids)) == 10
    valid = set(data["statuses"])
    assert valid == {
        "licensed_now",
        "pending_specific_evidence",
        "closed_until_cue",
        "already_tested",
    }
    assert all(g["status"] in valid for g in gates)
    by_status = {
        status: [g["id"] for g in gates if g["status"] == status]
        for status in valid
    }
    for status, expected in data["summary"].items():
        assert by_status[status] == expected, (status, by_status[status], expected)

    assert set(data["summary"]["licensed_now"]) == {
        "geometry_then_secondary_read",
        "code_as_operation",
    }
    assert "externally_cued_generative_transform" in data["summary"]["closed_until_cue"]
    assert "prior_stage_output_as_selector" in data["summary"]["pending_specific_evidence"]
    print(json.dumps(data["summary"], indent=2))

if __name__ == "__main__":
    main()

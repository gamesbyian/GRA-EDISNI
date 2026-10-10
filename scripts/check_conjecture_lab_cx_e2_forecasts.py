#!/usr/bin/env python3
"""Compare *frozen* CX-E2 row-rail predictions with later physical records.

Do not recompute the guessed rule after new stickers appear. Conflicting
observations are useful falsifications and are reported (exit status 0);
a data-integrity error or modified fixture is not a physics discovery.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/conjecture-lab-cx-e2-rail-predictions-2026-10-09.json"


def audit(physical_file, frozen_file):
    model = json.loads(Path(frozen_file).read_text(encoding="utf8"))
    assert model["id"] == "CX-E2-v1"
    forecasts = model["forecasts"]
    assert len(forecasts) == 6
    assert [x["residue"] for x in forecasts] == [6,8,11,41,64,91]
    original = {}
    with Path(physical_file).open(newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            residue = int(row["residue"])
            symbol = row["symbol"].strip()
            assert 1 <= residue <= 108 and symbol in "/-."
            assert original.get(residue, symbol) == symbol, "physical ledger conflict"
            original[residue] = symbol
    outcome = []
    for item in forecasts:
        residue = item["residue"]
        observed = original.get(residue)
        expected = item["predicted_symbol"]
        outcome.append({
            "residue": residue,
            "image_class": item["image_class"],
            "frozen_predicted_symbol": expected,
            "competing_frame_grammar": item["competing_frame_grammar"],
            "physical_observation": observed,
            "status": "unobserved" if observed is None else
                      ("matched" if observed == expected else "falsified"),
            "discriminator": item["discriminator"]
        })
    return {
        "frozen_model": model["id"],
        "frozen_unique_residue_count": model["observed_unique_residues_at_freeze"],
        "current_unique_residue_count": len(original),
        "all_six_unknown_at_freeze_snapshot":
            len(original) == model["observed_unique_residues_at_freeze"] and
            all(x["status"] == "unobserved" for x in outcome),
        "frozen_predicted_residues": outcome,
        "matches": sum(x["status"] == "matched" for x in outcome),
        "falsifications": sum(x["status"] == "falsified" for x in outcome),
        "unobserved": sum(x["status"] == "unobserved" for x in outcome),
        "interpretation": "post-selection conjecture; only truly new independent observations are prospective tests"
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--observations", type=Path, default=ROOT/"data/observations.csv")
    ap.add_argument("--frozen", type=Path, default=DEFAULT)
    args = ap.parse_args()
    print(json.dumps(audit(args.observations, args.frozen), indent=2))

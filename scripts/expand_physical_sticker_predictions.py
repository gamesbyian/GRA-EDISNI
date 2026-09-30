#!/usr/bin/env python3
"""Expand H108 sticker predictions to physical serial numbers.

The physical foreground repeats every 108 serials and the A-I background repeats
every 9.  This utility classifies each serial by evidentiary confidence rather
than pretending every preferred completion has the same status.

Default range is 1..600 because the current question is about the approximately
600 Collector's Edition serial space.  Use --max-serial 597, 630, 648, etc. to
inspect alternative production-range hypotheses without changing the H108 model.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"
PREDICTIONS = ROOT / "data" / "unobserved-sticker-predictions.csv"
SERIAL_ORDER = "ABCDEFGHI"

# These 22 unobserved residues are invariant even across the broader physical
# family currently retained after primary/Q4 gauge analysis.
BROAD_INVARIANT = {
    1, 11, 16, 27, 28, 33, 34, 35, 49, 50, 52, 54,
    62, 64, 67, 68, 73, 77, 83, 87, 104, 107,
}

PRIMARY_GAUGE = {6, 8, 41, 45}
Q4_AC_GAUGE = {82, 84, 91, 93, 100, 102}
BROADER_FI_BRANCH = {99, 105}


def read_observations():
    by_serial = {}
    by_residue = {}
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            serial = int(row["serial"])
            residue = int(row["residue"])
            symbol = row["symbol"]
            by_serial[serial] = symbol
            prior = by_residue.setdefault(residue, symbol)
            if prior != symbol:
                raise AssertionError(f"conflict at residue {residue}")
    return by_serial, by_residue


def read_predictions():
    out = {}
    with PREDICTIONS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[int(row["residue"])] = row
    return out


def residue_for(serial):
    return ((serial - 1) % 108) + 1


def background_for(serial):
    return SERIAL_ORDER[(serial - 1) % 9]


def classify(residue, observed_by_residue, prediction):
    if residue in observed_by_residue:
        return "observed_residue_repeat"

    if residue in BROAD_INVARIANT:
        return "broad_family_invariant"

    if residue in PRIMARY_GAUGE:
        return "canonical_invariant_primary_gauge"

    if residue in BROADER_FI_BRANCH:
        return "canonical_invariant_broader_branch"

    if residue in Q4_AC_GAUGE:
        # Some A/C cells are state-dependent within canonical polarity too.
        if prediction["canonical_class"] == "state-dependent":
            return "state_dependent_plus_q4_gauge"
        return "canonical_invariant_q4_gauge"

    if prediction["canonical_class"] == "state-dependent":
        return "state_dependent"

    raise AssertionError(f"unclassified residue {residue}")


def confidence_tier(category):
    if category in {"observed_residue_repeat", "broad_family_invariant"}:
        return "A"
    if category.startswith("canonical_invariant_"):
        return "B"
    if category.startswith("state_dependent"):
        return "C"
    raise AssertionError(category)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-serial", type=int, default=600)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--unknown-only", action="store_true")
    args = parser.parse_args()

    observed_by_serial, observed_by_residue = read_observations()
    predictions = read_predictions()

    rows = []
    for serial in range(1, args.max_serial + 1):
        residue = residue_for(serial)
        background = background_for(serial)
        physical_observed = serial in observed_by_serial

        if residue in observed_by_residue:
            preferred = observed_by_residue[residue]
            alternate = ""
            support = "physical residue observed"
            pred = None
        else:
            pred = predictions[residue]
            preferred = pred["preferred_guess"]
            alternate = pred["alternate_symbol"]
            support = (
                f'{pred["support_of_14"]}/14 canonical states'
                if pred["canonical_class"] == "state-dependent"
                else "14/14 canonical states"
            )

        category = (
            "physical_observation"
            if physical_observed
            else classify(residue, observed_by_residue, pred)
        )
        tier = "OBSERVED" if physical_observed else confidence_tier(category)

        if args.unknown_only and physical_observed:
            continue

        rows.append({
            "serial": serial,
            "residue": residue,
            "background": background,
            "foreground_preferred": preferred,
            "foreground_alternate": alternate,
            "tier": tier,
            "category": category,
            "support": support,
        })

    fields = list(rows[0])
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    unknown = [r for r in rows if r["tier"] != "OBSERVED"]
    from collections import Counter
    counts = Counter(r["tier"] for r in unknown)
    print(f"range=1..{args.max_serial}")
    print(f"physical_observations_in_range={sum(1 for s in observed_by_serial if s <= args.max_serial)}")
    print(f"unknown_physical_serials={len(unknown)}")
    for tier in ("A", "B", "C"):
        print(f"tier_{tier}={counts[tier]}")
    if unknown:
        print(f"tier_A_pct={100*counts['A']/len(unknown):.3f}")
        print(f"tier_A_plus_B_pct={100*(counts['A']+counts['B'])/len(unknown):.3f}")


if __name__ == "__main__":
    main()

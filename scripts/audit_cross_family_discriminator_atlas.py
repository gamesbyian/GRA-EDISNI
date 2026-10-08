#!/usr/bin/env python3
"""Frozen common-mask prospective hypothesis discrimination atlas.

All model projections use the SAME deduplicated 84-record/66-residue
observation snapshot and score ONLY the same 42 currently unseen H108
residues. Models are neither independent evidence votes nor calibrated
probabilities. Abstention (domain not modeled / no unanimous prediction)
is distinguished from a two-symbol prediction.

No semantic search, readout optimization or unseen symbol imputation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path

from enumerate_sticker_completion_ensembles import observations
from audit_q4_axis_consumer_comparison import (
    IDENTITY, PERMS, candidate_masters, family_members,
)
from audit_sticker_prediction_holdouts import (
    foreground_symbol, reconstruct,
)
from audit_row_selector_holdouts import selectors, hidden_possibilities
from audit_cube_transfer_holdouts import peer_prediction

ROOT = Path(__file__).resolve().parents[1]
OBS_PATH = ROOT / "data" / "observations.csv"
ROW_FROZEN = ROOT / "data" / "frozen-row-selector-predictions.json"
AXIS_FROZEN = ROOT / "data" / "frozen-q4-axis-consumer-discriminators.json"
COPY_FROZEN = ROOT / "data" / "frozen-cube-transfer-discriminators.json"
EXPECTED_OBS_BLOB = "2bf9f1352c1632986e5c672b4832848fde1e6d0c"
NAMES = (
    "primary_u2", "depth_identity", "recursive_u5", "quarter_relabel",
    "tail_only", "selected_row", "identity_copy",
)
FAMILY_PROVENANCE = {
    "primary_u2": "one-per-physical-column 3/6 plus one-slash-tail; ancestor of depth/quarter",
    "depth_identity": "selected output one dash per physical column; native depth",
    "recursive_u5": "canonical two-pass POS3 transducer; descendant of depth-grammar",
    "quarter_relabel": "alternate Cube 4 consumer, global pi=120/210 fitted retrospectively",
    "tail_only": "one slash per A-I tail only; abstains on primary-body cells",
    "selected_row": "one-exception selected row, post-hoc selected then frozen",
    "identity_copy": "literal cross-cube raw coordinate copy, weaker than majority in Experiment 454",
}
DEPENDENCE = {
    "primary_u2": "column_tail_ancestry",
    "depth_identity": "column_tail_ancestry",
    "recursive_u5": "column_tail_ancestry",
    "quarter_relabel": "column_tail_ancestry",
    "tail_only": "tail_constraint_shared",
    "selected_row": "tail_constraint_shared",
    "identity_copy": "raw_cross_cube_copy",
}
ALPHABETS = (set("/-"), set("/."))


def physical_rows() -> list[dict[str, str]]:
    with OBS_PATH.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def allowed_set(masters: set[str], residue: int) -> set[str]:
    return {master[residue - 1] for master in masters}


def calc() -> dict:
    source_bytes = OBS_PATH.read_bytes()
    source_sha = git_blob_sha(source_bytes)
    assert source_sha == EXPECTED_OBS_BLOB, (
        f"Original frozen corpus changed: {source_sha}. Do not refit forecasts; "
        "preserve the old freeze and explicitly version the new physical evidence."
    )
    count, known = observations()
    assert count == 84 and len(known) == 66
    raw_rows = physical_rows()
    assert len(raw_rows) == count
    missing = [r for r in range(1, 109) if r not in known]
    assert len(missing) == 42

    u2 = {master for master, _ in candidate_masters(known)}
    conditional = family_members(known)
    depth = conditional["depth", IDENTITY]
    quarter = set().union(*(conditional["quarter", pi] for pi in PERMS))
    rec = reconstruct(raw_rows)
    recursive = {
        "".join(foreground_symbol(payload, selector, r) for r in range(1, 109))
        for payload, selector, _first, _terminal in rec
    }
    assert (len(u2), len(depth), len(quarter), len(recursive)) == (324, 12, 10, 10)
    assert depth <= u2 and quarter <= u2
    for group in (u2, depth, quarter, recursive):
        assert all(all(master[r-1] == s for r, s in known.items()) for master in group)
    row_configs = selectors(known)
    assert row_configs
    tail_options = [
        [d for d in range(3)
         if all(known.get(82 + d2 * 9 + j, "/" if d == d2 else ".")
                == ("/" if d == d2 else ".")
                for d2 in range(3))]
        for j in range(9)
    ]
    assert all(tail_options)

    all_predictions = {}
    for r in missing:
        possibilities = {
            "primary_u2": allowed_set(u2, r),
            "depth_identity": allowed_set(depth, r),
            "recursive_u5": allowed_set(recursive, r),
            "quarter_relabel": allowed_set(quarter, r),
            "tail_only": set(),
            "selected_row": set(),
            "identity_copy": set(),
        }
        if r >= 82:
            d, j = divmod(r - 82, 9)
            possibilities["tail_only"] = {
                "/" if depth0 == d else "." for depth0 in tail_options[j]
            }
            letter = "ABCDEFGHI"[j]
            possibilities["selected_row"] = {
                "/" if selection[letter] == d else "." for selection in row_configs
            }
        else:
            possibilities["selected_row"] = hidden_possibilities(known, r)
            copy = peer_prediction(known, r, "identity")
            if copy is not None:
                possibilities["identity_copy"] = {copy}
        alphabet = ALPHABETS[0 if r <= 81 else 1]
        assert all(value <= alphabet for value in possibilities.values())
        all_predictions[r] = possibilities

    # Before any new sticker is viewed, freeze exact existing source predictions.
    frozen_axis = json.loads(AXIS_FROZEN.read_text(encoding="utf-8"))
    target = {}
    for obj in frozen_axis["mutually_exclusive_forecasts"]:
        r = obj["residue"]
        target[r] = (obj["depth"], obj["quarter"])
        assert all_predictions[r]["depth_identity"] == {obj["depth"]}
        assert all_predictions[r]["quarter_relabel"] == {obj["quarter"]}
    hard = {
        r for r in missing
        if len(all_predictions[r]["depth_identity"]) == 1
        and len(all_predictions[r]["quarter_relabel"]) == 1
        and all_predictions[r]["depth_identity"].isdisjoint(
            all_predictions[r]["quarter_relabel"]
        )
    }
    assert hard == set(target) == {50, 54, 93}

    frozen_row = json.loads(ROW_FROZEN.read_text(encoding="utf-8"))
    for residue, val in frozen_row["prospective_residue_predictions"].items():
        assert all_predictions[int(residue)]["selected_row"] == {val}
    frozen_copy = json.loads(COPY_FROZEN.read_text(encoding="utf-8"))
    for obj in frozen_copy["disagreement_predictions"]:
        r = obj["residue"]
        assert all_predictions[r]["identity_copy"] == {obj["copy"]}
        assert all_predictions[r]["primary_u2"] == {obj["column"]}

    pair_rows = []
    for a, b in itertools.combinations(NAMES, 2):
        active = [
            r for r in missing
            if all_predictions[r][a] and all_predictions[r][b]
        ]
        contradictions = [
            r for r in active
            if not all_predictions[r][a].intersection(all_predictions[r][b])
        ]
        jointly_forced_agreements = [
            r for r in active
            if len(all_predictions[r][a]) == 1
            and all_predictions[r][a] == all_predictions[r][b]
        ]
        pair_rows.append({
            "a": a,
            "b": b,
            "shared_unobserved_residues": len(active),
            "opposite_forced_residues": contradictions,
            "same_forced_residues": jointly_forced_agreements,
            "shared_parent_assumptions": (
                DEPENDENCE[a] == DEPENDENCE[b]
                or {a, b} & {"tail_only", "selected_row"} != set()
                   and {a, b} & {"primary_u2", "depth_identity", "recursive_u5", "quarter_relabel"} != set()
            ),
        })

    catalogue = []
    for r in missing:
        options = all_predictions[r]
        incompatible = [
            f"{p['a']} != {p['b']}"
            for p in pair_rows
            if r in p["opposite_forced_residues"]
        ]
        frozen = {
            symbol: [name for name in NAMES if options[name] == {symbol}]
            for symbol in sorted(ALPHABETS[0 if r <= 81 else 1])
        }
        frozen = {symbol: names for symbol, names in frozen.items() if names}
        catalogue.append({
            "residue": r,
            "serials_up_to_600": list(range(r, 601, 108)),
            "known_sector": "body" if r <= 81 else "tail",
            "allowed_by_model": {
                name: "".join(sorted(options[name])) if options[name] else None
                for name in NAMES
            },
            "opposite_forced_pairs": incompatible,
            "forced_symbols_by_models": frozen,
            "has_hard_conflict": bool(incompatible),
            "caution": "Conditional frozen predictions, not posterior odds.",
        })

    conflicts = [row for row in catalogue if row["has_hard_conflict"]]
    assert [row["residue"] for row in catalogue] == missing
    return {
        "research_phase": "common-mask prospective discriminator atlas, pre-observation freeze",
        "snapshot_observation_git_blob": source_sha,
        "physical_records": count,
        "physically_observed_residues": len(known),
        "unobserved_residues": len(missing),
        "completed_master_counts": {
            "primary_u2": len(u2),
            "depth_identity": len(depth),
            "recursive_u5": len(recursive),
            "quarter_relabel": len(quarter),
        },
        "row_selector_assignments": len(row_configs),
        "hypothesis_provenance": FAMILY_PROVENANCE,
        "assumption_dependencies": DEPENDENCE,
        "hard_conflict_residues": [x["residue"] for x in conflicts],
        "head_to_head": pair_rows,
        "prospective_unobserved_residue_catalogue": catalogue,
        "limits": [
            "All candidate grammars were developed on some of the same physical corpus.",
            "Common-mask comparison is prospective *readiness*, not independent fit validation.",
            "U2/depth/U5/quarter share a parent and should not be counted as separate confirmations.",
            "Row-one-exception was selected after seeing the full prior corpus.",
            "Identity copy underperformed a majority baseline and may make wrong forced forecasts.",
            "The number of conflicting pairs is an operational triage aid, not a probability or Bayesian model score.",
            "No next-stage interface or decrypted output is established."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="optional JSON output file")
    parser.add_argument("--summary", action="store_true", help="compact CI/log output")
    args = parser.parse_args()
    result = calc()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    if args.summary:
        print(json.dumps({
            "status": "passed all frozen-prediction and source checks",
            "corpus": [result["physical_records"], result["physically_observed_residues"]],
            "master_counts": result["completed_master_counts"],
            "row_selector_assignments": result["row_selector_assignments"],
            "hard_conflict_residues": result["hard_conflict_residues"],
            "pairwise_hard": {
                p["a"] + ":" + p["b"]: p["opposite_forced_residues"]
                for p in result["head_to_head"] if p["opposite_forced_residues"]
            },
        }, sort_keys=True))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()

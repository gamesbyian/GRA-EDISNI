#!/usr/bin/env python3
"""Experiment 350: chronological replay of spatial occupancy models inside 3/6 frames."""

from __future__ import annotations

import csv
import itertools
import json
import math
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
LEDGER = ROOT / "archive" / "external" / "twinysam-inside-arg" / "stickers.md"
OUT = ROOT / "data" / "experiment-350-chronological-frame-occupancy.json"

SERIAL_ORDER = "ABCDEFGHI"
PHYSICAL_LAYOUT = ("IAB", "CDE", "FGH")
PHYSICAL_POSITION = {
    letter: (row, col)
    for row, line in enumerate(PHYSICAL_LAYOUT)
    for col, letter in enumerate(line)
}
ENTRY_RE = re.compile(r"^- \[(\d{3})\]", re.M)
DATE_RE = re.compile(r"(?<!\d)(\d{1,2})\.(\d{1,2})\.(\d{2}|\d{4})(?!\d)")


def parse_date(text: str) -> date | None:
    m = DATE_RE.search(text)
    if not m:
        return None
    d, mth, y = map(int, m.groups())
    if y < 100:
        y += 2000
    return date(y, mth, d)


def ledger_dates() -> dict[int, date]:
    text = LEDGER.read_text(encoding="utf-8")
    matches = list(ENTRY_RE.finditer(text))
    out = {}
    for i, match in enumerate(matches):
        block = text[match.start() : matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        when = parse_date(block)
        if when is not None:
            out[int(match.group(1))] = when
    return out


def earliest_first81() -> dict[int, dict]:
    dates = ledger_dates()
    rows = []
    missing = []
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            serial = int(row["serial"])
            residue = int(row["residue"])
            if serial not in dates:
                missing.append(serial)
                continue
            if residue <= 81:
                rows.append({
                    "serial": serial,
                    "residue": residue,
                    "symbol": row["symbol"],
                    "date": dates[serial],
                })
    if missing:
        raise RuntimeError(f"missing ledger dates: {sorted(set(missing))}")
    earliest = {}
    for row in sorted(rows, key=lambda r: (r["date"], r["serial"])):
        r = row["residue"]
        if r not in earliest:
            earliest[r] = row
        else:
            assert earliest[r]["symbol"] == row["symbol"]
    return earliest


def assignment_model(bits: tuple[int, ...], model: str) -> bool:
    # bits=1 means minority symbol. Exactly three bits are 1.
    coords = [
        PHYSICAL_POSITION[SERIAL_ORDER[j]]
        for j, bit in enumerate(bits)
        if bit
    ]
    row_counts = [sum(r == rr for r, _ in coords) for rr in range(3)]
    col_counts = [sum(c == cc for _, c in coords) for cc in range(3)]
    if model == "unrestricted":
        return True
    if model == "one_per_row":
        return row_counts == [1, 1, 1]
    if model == "one_per_column":
        return col_counts == [1, 1, 1]
    if model == "permutation_matrix":
        return row_counts == [1, 1, 1] and col_counts == [1, 1, 1]
    raise ValueError(model)


def model_assignments() -> dict[str, list[tuple[str, ...]]]:
    names = ("unrestricted", "one_per_row", "one_per_column", "permutation_matrix")
    result = {name: [] for name in names}
    for minority_positions in itertools.combinations(range(9), 3):
        bits = tuple(int(j in minority_positions) for j in range(9))
        for model in names:
            if not assignment_model(bits, model):
                continue
            # Both frame polarities: minority can be slash or dash.
            for minority_symbol in ("/", "-"):
                major = "-" if minority_symbol == "/" else "/"
                result[model].append(tuple(minority_symbol if bit else major for bit in bits))
    assert {k: len(v) for k, v in result.items()} == {
        "unrestricted": 168,
        "one_per_row": 54,
        "one_per_column": 54,
        "permutation_matrix": 12,
    }
    return result


ASSIGNMENTS = model_assignments()


def compatible_count(known: dict[int, str], frame: int, model: str) -> int:
    constraints = {}
    for pos in range(9):
        residue = frame * 9 + pos + 1
        if residue in known:
            constraints[pos] = known[residue]
    return sum(
        all(assignment[pos] == sym for pos, sym in constraints.items())
        for assignment in ASSIGNMENTS[model]
    )


def main() -> None:
    earliest = earliest_first81()
    batches = defaultdict(list)
    for row in earliest.values():
        batches[row["date"]].append(row)

    models = tuple(ASSIGNMENTS)
    states = {
        model: {"alive": True, "surprise_bits": 0.0, "eliminated_on": None, "history": []}
        for model in models
    }
    known = {}
    row_col_shifts = []

    for when in sorted(batches):
        batch = sorted(batches[when], key=lambda r: r["residue"])
        affected = sorted({(r["residue"] - 1) // 9 for r in batch})
        before_known = dict(known)
        for row in batch:
            known[row["residue"]] = row["symbol"]

        events = {}
        for model, state in states.items():
            if not state["alive"]:
                events[model] = None
                continue
            before = after = 1
            per_frame = {}
            for frame in affected:
                b = compatible_count(before_known, frame, model)
                a = compatible_count(known, frame, model)
                if b <= 0:
                    raise AssertionError(f"alive model {model} has zero before count")
                before *= b
                after *= a
                per_frame[str(frame + 1)] = {"before": b, "after": a}
            p = after / before
            bits = None
            if after == 0:
                state["alive"] = False
                state["eliminated_on"] = when.isoformat()
            else:
                bits = -math.log2(p)
                state["surprise_bits"] += bits
            event = {
                "date": when.isoformat(),
                "new_residues": [r["residue"] for r in batch],
                "new_serials": [r["serial"] for r in batch],
                "conditional_probability": p,
                "surprise_bits": bits,
                "per_frame_counts": per_frame,
            }
            state["history"].append(event)
            events[model] = event

        er, ec = events["one_per_row"], events["one_per_column"]
        if er and ec and er["conditional_probability"] > 0 and ec["conditional_probability"] > 0:
            row_col_shifts.append({
                "date": when.isoformat(),
                "new_residues": er["new_residues"],
                "log2_p_column_over_p_row": math.log2(
                    ec["conditional_probability"] / er["conditional_probability"]
                ),
                "p_row": er["conditional_probability"],
                "p_column": ec["conditional_probability"],
            })

    final_states = {
        model: {
            "alive": s["alive"],
            "eliminated_on": s["eliminated_on"],
            "cumulative_surprise_bits": s["surprise_bits"] if s["alive"] else None,
        }
        for model, s in states.items()
    }
    survivors = [m for m, s in states.items() if s["alive"]]

    pairwise = {}
    for a, b in itertools.combinations(survivors, 2):
        delta = states[b]["surprise_bits"] - states[a]["surprise_bits"]
        pairwise[f"{a}_vs_{b}"] = {
            "bits_b_minus_a": delta,
            "likelihood_ratio_p_a_over_p_b": 2 ** delta,
        }

    result = {
        "experiment": 350,
        "chronology_source": "archive/external/twinysam-inside-arg/stickers.md ledger-received dates",
        "physical_layout": list(PHYSICAL_LAYOUT),
        "unique_first81_residues_scored": len(earliest),
        "date_batches": len(batches),
        "model_complete_assignment_counts_per_frame": {k: len(v) for k, v in ASSIGNMENTS.items()},
        "final_states": final_states,
        "survivors": survivors,
        "pairwise_survivor_likelihood_ratios": pairwise,
        "largest_absolute_row_vs_column_shifts": sorted(
            row_col_shifts,
            key=lambda x: abs(x["log2_p_column_over_p_row"]),
            reverse=True,
        )[:10],
        "histories": {model: s["history"] for model, s in states.items()},
        "interpretation_guardrail": "retrospective bounded evidence for occupancy geometry only; no ternary semantics or recursion",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

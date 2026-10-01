#!/usr/bin/env python3
"""Experiment 349: chronological prequential score for 3x3 census families."""

from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "observations.csv"
LEDGER = ROOT / "archive" / "external" / "twinysam-inside-arg" / "stickers.md"
OUT = ROOT / "data" / "experiment-349-chronological-census-prequential.json"

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
    out: dict[int, date] = {}
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        serial = int(match.group(1))
        when = parse_date(block)
        if when is not None:
            out[serial] = when
    return out


def observations() -> list[dict]:
    dates = ledger_dates()
    rows = []
    missing_dates = []
    with OBS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            serial = int(row["serial"])
            residue = int(row["residue"])
            if serial not in dates:
                missing_dates.append(serial)
                continue
            rows.append({
                "serial": serial,
                "residue": residue,
                "symbol": row["symbol"],
                "date": dates[serial],
            })
    if missing_dates:
        raise RuntimeError(f"missing ledger dates for observation serials: {sorted(set(missing_dates))}")
    return rows


def count_assignments(known: dict[int, str], frame: int, w: int) -> int:
    # Count labeled slash/dash assignments to this 9-cell frame compatible
    # with known physical symbols and the unordered census {w, 9-w}.
    slash = dash = 0
    for pos in range(9):
        sym = known.get(frame * 9 + pos + 1)
        if sym == "/":
            slash += 1
        elif sym == "-":
            dash += 1
        elif sym is not None:
            raise AssertionError(f"unexpected symbol in first-81 frame: {sym}")
    unknown = 9 - slash - dash
    total = 0
    for slash_total in {w, 9 - w}:
        needed = slash_total - slash
        if 0 <= needed <= unknown:
            total += math.comb(unknown, needed)
    return total


def main() -> None:
    rows = observations()

    # First ledger-received physical observation for each H108 residue.
    earliest: dict[int, dict] = {}
    for row in sorted(rows, key=lambda r: (r["date"], r["serial"])):
        residue = row["residue"]
        if residue > 81:
            continue
        if residue not in earliest:
            earliest[residue] = row
        else:
            assert earliest[residue]["symbol"] == row["symbol"], (
                residue, earliest[residue], row
            )

    batches: dict[date, list[dict]] = defaultdict(list)
    for row in earliest.values():
        batches[row["date"]].append(row)

    known: dict[int, str] = {}
    states = {
        w: {
            "alive": True,
            "surprise_bits": 0.0,
            "eliminated_on": None,
            "history": [],
        }
        for w in range(5)
    }

    ratio_history = []
    for when in sorted(batches):
        batch = sorted(batches[when], key=lambda r: r["residue"])
        affected = sorted({(r["residue"] - 1) // 9 for r in batch})
        before_known = dict(known)

        for row in batch:
            known[row["residue"]] = row["symbol"]

        per_w = {}
        for w, state in states.items():
            if not state["alive"]:
                per_w[w] = None
                continue
            before = 1
            after = 1
            per_frame = {}
            for frame in affected:
                b = count_assignments(before_known, frame, w)
                a = count_assignments(known, frame, w)
                if b <= 0:
                    raise AssertionError(f"alive family {w} had zero pre-batch assignments")
                before *= b
                after *= a
                per_frame[str(frame + 1)] = {"before": b, "after": a}
            probability = after / before
            if after == 0:
                state["alive"] = False
                state["eliminated_on"] = when.isoformat()
                bits = math.inf
            else:
                bits = -math.log2(probability)
                state["surprise_bits"] += bits
            event = {
                "date": when.isoformat(),
                "new_residues": [r["residue"] for r in batch],
                "new_serials": [r["serial"] for r in batch],
                "affected_squares": [f + 1 for f in affected],
                "conditional_probability": probability,
                "surprise_bits": None if math.isinf(bits) else bits,
                "per_square_counts": per_frame,
            }
            state["history"].append(event)
            per_w[w] = event

        # Record batch likelihood ratio only while both final surviving candidates live.
        e3, e4 = per_w[3], per_w[4]
        if e3 is not None and e4 is not None and e3["conditional_probability"] > 0 and e4["conditional_probability"] > 0:
            shift = math.log2(e4["conditional_probability"] / e3["conditional_probability"])
            ratio_history.append({
                "date": when.isoformat(),
                "new_residues": e3["new_residues"],
                "log2_p4_over_p3": shift,
                "p_3_6": e3["conditional_probability"],
                "p_4_5": e4["conditional_probability"],
            })

    final = {}
    for w, state in states.items():
        final[str(w)] = {
            "alive": state["alive"],
            "eliminated_on": state["eliminated_on"],
            "cumulative_surprise_bits": state["surprise_bits"] if state["alive"] else None,
            "scored_batches_before_elimination_or_end": len(state["history"]),
        }

    alive = [w for w, state in states.items() if state["alive"]]
    assert alive == [3, 4], alive

    ranked_shifts = sorted(ratio_history, key=lambda x: abs(x["log2_p4_over_p3"]), reverse=True)
    result = {
        "experiment": 349,
        "chronology_source": "archive/external/twinysam-inside-arg/stickers.md ledger-received dates",
        "unique_first81_residues_scored": len(earliest),
        "date_batches": len(batches),
        "candidate_minorities": [0, 1, 2, 3, 4],
        "final_states": final,
        "surviving_candidates": alive,
        "three_vs_four": {
            "surprise_3_6_bits": states[3]["surprise_bits"],
            "surprise_4_5_bits": states[4]["surprise_bits"],
            "bits_4_5_minus_3_6": states[4]["surprise_bits"] - states[3]["surprise_bits"],
            "likelihood_ratio_p3_over_p4": 2 ** (states[4]["surprise_bits"] - states[3]["surprise_bits"]),
        },
        "largest_absolute_batch_log_likelihood_ratio_shifts": ranked_shifts[:10],
        "histories": {str(w): state["history"] for w, state in states.items()},
        "interpretation_guardrail": "retrospective bounded prequential evidence, not prospective confirmation",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

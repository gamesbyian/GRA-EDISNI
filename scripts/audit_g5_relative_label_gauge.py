#!/usr/bin/env python3
"""Experiment 354: audit relative tail/body label gauges for G5."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-354-g5-relative-label-gauge.json"


def surface(payload, selector, external_q, perm):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                external_q,
                perm[selector_at_physical_cell(selector, row, col)],
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(p, s) for p in payloads for s in selectors]

    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(raw) == 216

    records = []
    for perm in itertools.permutations(range(3)):
        survivors = []
        for payload, selector in raw:
            decoded = tuple(
                decode_dash_pos3(surface(payload, selector, q, perm))
                for q in range(3)
            )
            if None not in decoded:
                survivors.append((payload, selector, decoded))

        families = Counter(x[2] for x in survivors)
        q_varying = sum(len(set(fam)) > 1 for fam in families)
        selector_outputs = {}
        for _payload, selector, decoded in survivors:
            key = tuple(selector[j] for j in range(9))
            selector_outputs.setdefault(key, set()).add(decoded)

        records.append({
            "perm": "".join(map(str, perm)),
            "identity": perm == (0, 1, 2),
            "survivors": len(survivors),
            "distinct_output_families": len(families),
            "q_varying_output_family_count": q_varying,
            "selector_completion_count_represented": len(selector_outputs),
            "output_family_counts": {
                "/".join(k): v for k, v in sorted(families.items())
            },
        })

    best = max(r["survivors"] for r in records)
    winners = [r["perm"] for r in records if r["survivors"] == best]

    result = {
        "experiment": 354,
        "family": "shared S3 relabeling pi before literal G5 depth substitution (q,S)->(q,pi(S))",
        "raw_primary_payloads": len(payloads),
        "raw_selectors": len(selectors),
        "raw_candidate_machines": len(raw),
        "records": records,
        "max_survivors": best,
        "max_survivor_permutations": winners,
        "guardrail": "first-pass positional validity only; no terminal, route, final-state-count, or semantic target",
    }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

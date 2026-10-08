#!/usr/bin/env python3
"""Experiment 449: independent Q4 depth-selector / Q1-Q3 cube agreement audit.

Only physical observations. Compare the Q4 slash-selected primary-depth cells
against an exact 3^9 independent uniform-depth baseline. No machine completion.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]


def load():
    marks = {}
    records = 0
    with (ROOT / "data" / "observations.csv").open(newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            records += 1
            r = int(row["residue"])
            assert 1 <= r <= 108 and row["symbol"] in "/-."
            assert r not in marks or marks[r] == row["symbol"]
            marks[r] = row["symbol"]
    return records, marks


def evaluate():
    records, marks = load()
    choices, pair_tables, tail_words = [], [], []
    for j in range(9):
        tail = [marks.get(82 + 9*d + j) for d in range(3)]
        assert not any(s == "-" for s in tail)
        assert sum(s == "/" for s in tail) <= 1
        allowed = [d for d in range(3)
                   if tail[d] == "/" or (tail[d] is None and "/" not in tail)]
        assert allowed
        choices.append(allowed)
        tail_words.append("".join(s or "?" for s in tail))
        table = []
        for d in range(3):
            known = [marks.get(1 + 27*q + 9*d + j) for q in range(3)]
            known = [s for s in known if s is not None]
            pairs = [known[a] == known[b] for a in range(len(known))
                     for b in range(a+1, len(known))]
            table.append((sum(pairs), len(pairs)))
        pair_tables.append(table)

    def score(addresses):
        agree = pairs = 0
        for j, depth in enumerate(addresses):
            a, p = pair_tables[j][depth]
            agree += a
            pairs += p
        return agree, pairs

    legal = [score(x) for x in product(*choices)]
    null = [score(x) for x in product(*([[0, 1, 2]]*9))]
    assert records == 84 and len(marks) == 66, "Corpus changed: recalculate audit"
    assert len(legal) == 18 and len(null) == 19683
    assert Counter(legal) == {(10, 16): 6, (11, 17): 6, (10, 17): 6}
    assert sum(a/p >= 10/17 for a,p in null) == 10608
    assert sum(a/p >= 11/17 for a,p in null) == 6753
    return {
        "physical_records": records,
        "unique_residues": len(marks),
        "q4_depth_words": dict(zip("ABCDEFGHI", tail_words)),
        "q4_depth_choices": dict(zip("ABCDEFGHI", choices)),
        "feasible_q4_depth_codes": len(legal),
        "legal_cross_cube_concordance": [
            {"agreements": a, "observed_pairs": p, "count": count}
            for (a,p), count in sorted(Counter(legal).items())
        ],
        "null_depth_assignments": len(null),
        "null_at_least_worst_legal_fraction": 10608/19683,
        "null_at_least_best_legal_fraction": 6753/19683,
        "interpretation": "No discriminating cross-cube symbol agreement under the frozen direct-depth read.",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))

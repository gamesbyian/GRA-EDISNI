#!/usr/bin/env python3
"""Experiment 366: selection-aware null for the Experiment-323 Q4 holdout comparison.

Experiment 323 reported that, hiding each of the 11 observed Q4 (slash/dot)
residues in turn, the incumbent reconstruction forces 10/11 symbols while the
tail-index-only family forces 3/11.  Experiment 365 noted that the incumbent's
grammar was fitted to the full corpus, so (by Experiment 340's argument) its
forced predictions cannot be wrong and "10/11" needs calibration.

Preregistered design (fixed before inspecting outputs):

  Null datasets: keep all 54 real body observations; permute the 11 observed
  Q4 symbols (4 slash, 7 dot) over the same 11 residues.  All C(11,4) = 330
  assignments are enumerated exactly.

  Selection condition: the dataset is retained only if the incumbent's fixed
  grammar (as implemented in audit_sticker_prediction_holdouts.reconstruct)
  admits at least one machine, i.e. "the incumbent would still fit".

  Statistic: leave-one-residue-out over the 11 Q4 residues; count forced
  predictions for the incumbent and for the tail-only family (one slash per
  A-I stack, no recursion).  Report the null distribution of the incumbent
  count and of the incumbent-minus-tail difference, and the tail probability
  of the observed values (10 and 7).

The script asserts that no forced prediction is ever wrong (Experiment 340's
guarantee) and that the real data reproduce Experiment 323's 10/11 and 3/11.
"""
from __future__ import annotations

import csv
import itertools
import sys
from collections import Counter
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import audit_sticker_prediction_holdouts as H  # noqa: E402

Q4_RESIDUES = (85, 86, 89, 90, 92, 95, 96, 97, 98, 101, 108)


def stack_depth(residue):
    off = residue - 82
    return off % 9, off // 9


def selector_ok(selector, q4obs):
    for r, sym in q4obs.items():
        j, d = stack_depth(r)
        if (selector[j] == d) != (sym == "/"):
            return False
    return True


def tail_only_options(q4obs):
    """Per-stack set of allowed slash depths under one-slash-per-stack."""
    opts = {j: {0, 1, 2} for j in range(9)}
    for r, sym in q4obs.items():
        j, d = stack_depth(r)
        if sym == "/":
            opts[j] &= {d}
        else:
            opts[j].discard(d)
    return opts


def tail_only_prediction(q4obs, residue):
    opts = tail_only_options(q4obs)
    if any(not v for v in opts.values()):
        return None
    j, d = stack_depth(residue)
    return {"/" if s == d else "." for s in opts[j]}


def main():
    rows = H.load_rows()
    body_rows = [r for r in rows if int(r["residue"]) <= 81]
    real_q4 = {int(r["residue"]): r["symbol"] for r in rows if int(r["residue"]) > 81}
    assert tuple(sorted(real_q4)) == Q4_RESIDUES
    n_slash = sum(1 for s in real_q4.values() if s == "/")
    assert n_slash == 4 and len(real_q4) == 11

    # Precompute every recursion-valid (payload, selector) pair for the real body.
    pc = H.primary_column_candidates(body_rows)
    payloads = list(H.enumerate_primary_payloads(pc))
    all_selectors = [dict(enumerate(v)) for v in itertools.product(range(3), repeat=9)]
    valid = []
    for p in payloads:
        for s in all_selectors:
            first = [H.decode_dash_pos3(H.first_surface(p, s, q)) for q in range(3)]
            if None in first:
                continue
            if H.decode_dash_pos3(H.terminal_surface(p, s)) is None:
                continue
            valid.append((p, s))
    print(f"body payloads: {len(payloads)}; recursion-valid (payload, selector) pairs: {len(valid)}")

    def incumbent_prediction(q4obs, residue):
        preds = {H.foreground_symbol(p, s, residue) for p, s in valid if selector_ok(s, q4obs)}
        return preds

    def score(q4obs):
        if not any(selector_ok(s, q4obs) for _, s in valid):
            return None  # incumbent does not fit: dataset not retained
        inc = tail = 0
        for r in Q4_RESIDUES:
            reduced = {k: v for k, v in q4obs.items() if k != r}
            pi = incumbent_prediction(reduced, r)
            pt = tail_only_prediction(reduced, r)
            assert pi and q4obs[r] in pi, ("incumbent excludes truth", r, pi)
            assert pt and q4obs[r] in pt, ("tail-only excludes truth", r, pt)
            inc += len(pi) == 1
            tail += len(pt) == 1
        return inc, tail

    real = score(real_q4)
    print(f"real data: incumbent forced {real[0]}/11, tail-only forced {real[1]}/11")
    assert real == (10, 3), real

    dist = Counter()
    total = 0
    for slash_pos in itertools.combinations(Q4_RESIDUES, 4):
        total += 1
        q4obs = {r: ("/" if r in slash_pos else ".") for r in Q4_RESIDUES}
        sc = score(q4obs)
        if sc is not None:
            dist[sc] += 1
    assert total == comb(11, 4) == 330

    kept = sum(dist.values())
    inc_dist = Counter()
    diff_dist = Counter()
    for (i, t), c in dist.items():
        inc_dist[i] += c
        diff_dist[i - t] += c
    p_inc = sum(c for i, c in inc_dist.items() if i >= real[0]) / kept
    p_diff = sum(c for d, c in diff_dist.items() if d >= real[0] - real[1]) / kept
    print(f"null datasets: {total}; retained (incumbent fits): {kept}")
    print("incumbent forced-count distribution:", dict(sorted(inc_dist.items())))
    print("incumbent-minus-tail distribution:  ", dict(sorted(diff_dist.items())))
    print(f"P(incumbent forced >= {real[0]} | fits) = {p_inc:.4f}")
    print(f"P(difference >= {real[0]-real[1]} | fits) = {p_diff:.4f}")
    print("OK: no forced prediction was ever wrong in any retained dataset")
    return {"kept": kept, "inc": inc_dist, "diff": diff_dist, "p_inc": p_inc, "p_diff": p_diff}


if __name__ == "__main__":
    main()

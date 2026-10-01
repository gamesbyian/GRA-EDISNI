#!/usr/bin/env python3
"""Experiment 368: rerun of Experiment 15 (printer-stream reuse) on all 65 residues.

Experiment 15 compared the H108 master with contiguous segments of the PC and
Xbox printer streams but parsed only 64 of the 65 known residues and flagged a
rerun.  The label-ordered [001]/[101] tables are not available offline, so this
rerun uses the two printer tables preserved as Discord attachments:

  data/printer-strings/pc-32-long-acorn-order.txt   (32 long PC strings, solved acorn order)
  data/printer-strings/xbox-47-master-morse-36.txt  (all 47 unique Xbox strings, file order)

Preregistered design (fixed before inspecting outputs):

  Data: all 65 observed H108 residues (82 records) from data/observations.csv.
  Transformations: forward/reversed comparison x all 6 bijections of / - . .
  Family A (order-free): slide each individual printer string along the cyclic
    H108 at every offset.  Statistic A = longest perfectly agreeing window,
    measured in known residues covered (zero mismatches).
  Family B (concatenated): concatenate each table in file order and compare
    the full 108-cycle at every offset.  Statistic B = best match count out of
    65 known residues.
  Null: 1,000 datasets permuting observed symbols among observed residues
    within each zone (1-81 and 82-108), preserving positions, zone symbol
    counts and the established 81/27 alphabet split.  Seed 368.
  Report the fraction of null datasets scoring >= real for each statistic.
"""
from __future__ import annotations

import csv
import itertools
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SYM = {"/": 0, "-": 1, ".": 2}
PERMS = list(itertools.permutations(range(3)))
N_NULL = 1000


def load_master():
    m = np.full(108, -1, dtype=np.int8)
    for row in csv.DictReader(open(ROOT / "data" / "observations.csv")):
        r = int(row["residue"]) - 1
        v = SYM[row["symbol"]]
        assert m[r] in (-1, v)
        m[r] = v
    assert (m >= 0).sum() == 65
    return m


def load_table(name):
    lines = [l.strip() for l in open(ROOT / "data" / "printer-strings" / name)]
    lines = [l for l in lines if l and set(l) <= set("/-.")]
    return [np.array([SYM[c] for c in l], dtype=np.int8) for l in lines]


def variants(arr):
    for seq in (arr, arr[::-1]):
        for p in PERMS:
            yield np.array(p, dtype=np.int8)[seq]


def stat_a(master, strings):
    """Longest zero-mismatch window, counted in known residues covered."""
    known = master >= 0
    best = 0
    idx = np.arange(108)
    for s in strings:
        L = len(s)
        win = (idx[:, None] + np.arange(L)[None, :]) % 108  # offsets x L
        mvals = master[win]
        kn = known[win]
        for v in variants(s):
            mism = (kn & (mvals != v[None, :])).sum(1)
            ok = mism == 0
            if ok.any():
                best = max(best, int(kn[ok].sum(1).max()))
    return best


def stat_b(master, strings):
    """Best match count (of 65) for the full 108-cycle against a concatenated stream."""
    known = master >= 0
    kidx = np.nonzero(known)[0]
    kval = master[kidx]
    best = 0
    stream = np.concatenate(strings)
    n = len(stream)
    offs = np.arange(n)
    for v in variants(stream):
        cyc = v[(offs[:, None] + kidx[None, :]) % n]
        best = max(best, int((cyc == kval[None, :]).sum(1).max()))
    return best


def null_masters(master, rng):
    out = []
    for _ in range(N_NULL):
        m = master.copy()
        for lo, hi in ((0, 81), (81, 108)):
            pos = np.nonzero(m[lo:hi] >= 0)[0] + lo
            m[pos] = rng.permutation(m[pos])
        out.append(m)
    return out


def main():
    master = load_master()
    pc = load_table("pc-32-long-acorn-order.txt")
    xb = load_table("xbox-47-master-morse-36.txt")
    assert len(pc) == 32 and len(xb) == 47
    rng = np.random.default_rng(368)
    nulls = null_masters(master, rng)
    results = {}
    for name, table in (("PC", pc), ("Xbox", xb)):
        for label, fn in (("A longest perfect window", stat_a), ("B concatenated best/65", stat_b)):
            real = fn(master, table)
            null = np.array([fn(m, table) for m in nulls])
            p = float((null >= real).mean())
            results[(name, label)] = (real, p)
            print(f"{name:5s} {label:26s} real={real:3d}  null median={int(np.median(null)):3d} "
                  f"95th={int(np.percentile(null, 95)):3d}  P(null>=real)={p:.3f}")
    return results


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Experiment 360: three-position (trit) readout vs. two externally supplied targets.

Bounded parent family, stated before inspecting outputs:

  Readout R: each primary frame (rows 1-9 of the 12x9 master, in the physical
  I A B / C D E / F G H layout) yields three trits = row of the single
  exceptional mark in each physical column; the tail (rows 10-12) yields nine
  trits = which of the three tail rows carries the slash for each A-I class.
  This gives 27 + 9 = 36 trits / 12 trigrams.  Variants: per-frame column
  order mirrored, body+tail or tail+body, forward/reverse/cyclic.

  Target 1 (lever cue, Exp 342/343): the normal secret-ending bunker password
  UURLRRRUUURLLL, tested mapping-agnostically (any bijection of the three
  trit values onto U/R/L), forward and reversed.

  Target 2 (LIFEDETECTED): the only accepted Playdead-site phrase whose
  derivation from its source puzzle was never found; it has exactly 12
  letters, matching the 12 trigrams.  Any monoalphabetic reading needs one
  trigram value to occur 4 times (the four Es) plus two further pairs.

Both targets are run across all 14 legal completions.  The script fails
loudly if the readout premise (exactly one exception per column / stack)
breaks, and asserts the recorded negative results.
"""
import collections
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LETTERS = "ABCDEFGHI"
PHYS = ["IAB", "CDE", "FGH"]
PASSWORD = "UURLRRRUUURLLL"
PHRASE = "LIFEDETECTED"


def load_masters():
    out = subprocess.run([sys.executable, str(ROOT / "generate_master.py")],
                         capture_output=True, text=True, check=True).stdout
    masters = {}
    for line in out.splitlines():
        if line.strip():
            parts = line.split()
            masters[parts[0]] = parts[-1]
    assert len(masters) == 14, len(masters)
    return masters


def readout(master, mirror=False):
    body = []
    for row in range(9):
        grid = [[master[row * 9 + LETTERS.index(c)] for c in line] for line in PHYS]
        counts = collections.Counter(x for r in grid for x in r)
        minority = min(counts, key=counts.get)
        assert counts[minority] == 3, (row, counts)
        cols = range(2, -1, -1) if mirror else range(3)
        for c in cols:
            col = [grid[r][c] for r in range(3)]
            assert col.count(minority) == 1, (row, c, col)
            body.append(col.index(minority))
    tail = []
    for j in range(9):
        stack = [master[81 + d * 9 + j] for d in range(3)]
        assert stack.count("/") == 1, (j, stack)
        tail.append(stack.index("/"))
    return "".join(map(str, body)), "".join(map(str, tail))


def isomorphic(a, b):
    fwd, rev = {}, {}
    for x, y in zip(a, b):
        if fwd.setdefault(x, y) != y or rev.setdefault(y, x) != x:
            return False
    return True


def streams(master):
    for mirror in (False, True):
        body, tail = readout(master, mirror)
        for name, s in (("body", body), ("tail", tail),
                        ("body+tail", body + tail), ("tail+body", tail + body)):
            yield mirror, name, s


def main():
    masters = load_masters()

    # Target 1: bunker password, mapping-agnostic.
    lever_hits = []
    windows = 0
    for state, m in masters.items():
        for mirror, name, s in streams(m):
            for seq, how in ((s, "fwd"), (s[::-1], "rev"), (s + s[:13], "cyc")):
                for i in range(len(seq) - 13):
                    windows += 1
                    for target in (PASSWORD, PASSWORD[::-1]):
                        if isomorphic(seq[i:i + 14], target):
                            lever_hits.append((state, mirror, name, how, i))
    print(f"lever: {windows} windows tested, {len(lever_hits)} isomorphic hits")

    # Target 2: LIFEDETECTED as a 12-trigram monoalphabetic reading.
    need = max(collections.Counter(PHRASE).values())
    best = 0
    phrase_hits = []
    for state, m in masters.items():
        for mirror, name, s in streams(m):
            if len(s) != 36:
                continue
            for rev_tri in (False, True):
                tris = [s[k:k + 3] for k in range(0, 36, 3)]
                if rev_tri:
                    tris = [t[::-1] for t in tris]
                best = max(best, max(collections.Counter(tris).values()))
                for order in (tris, tris[::-1]):
                    for rot in range(12):
                        cand = order[rot:] + order[:rot]
                        if isomorphic(cand, PHRASE):
                            phrase_hits.append((state, mirror, name, rev_tri, rot))
    print(f"LIFEDETECTED: needs a trigram repeated {need}x; "
          f"max trigram multiplicity over all readouts = {best}; hits = {len(phrase_hits)}")

    # Recorded negative results: fail loudly if they ever change.
    assert not lever_hits, lever_hits
    assert best < need and not phrase_hits, (best, phrase_hits)
    print("OK: both externally supplied targets are excluded under readout R")


if __name__ == "__main__":
    main()

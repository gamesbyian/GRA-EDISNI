#!/usr/bin/env python3
"""Experiment 362: CEO-door nameplate string vs. four-sticker groups.

Community proposal (solving-breakout, 3-4 Jan 2026): read the 108-cell master
in groups of four, one group per character of the in-game CEO door text
"Fordsjh Gjfhdfdjfhd Ujhdfr" (27 characters with a trailing space = 108/4).

Necessary condition for any letter-per-group reading: every occurrence of the
same character must map to the same four-symbol group.  Tested on raw
observations only (unknown cells are wildcards), at all 108 cyclic starts,
for four spelling variants.  No completion or machine assumption is used.
"""
import csv
import pathlib

OBS = pathlib.Path(__file__).resolve().parent.parent / "data" / "observations.csv"
VARIANTS = ["Fordsjh Gjfhdfdjfhd Ujhdfr ", "Fordsjh Gjfhdfdjfhd Ujhdfr",
            "Fordsjh Gjfhdfdjfhd Ujhdfr B02", "FordsjhGjfhdfdjfhdUjhdfr"]


def load():
    obs = {}
    for row in csv.DictReader(open(OBS)):
        cell = int(row["residue"]) - 1
        assert obs.setdefault(cell, row["symbol"]) == row["symbol"]
    assert len(obs) == 65
    return obs


def compatible(text, start, obs):
    seen = {}
    for i, ch in enumerate(text.lower()):
        group = [obs.get((start + 4 * i + k) % 108) for k in range(4)]
        prev = seen.setdefault(ch, [None] * 4)
        for k, sym in enumerate(group):
            if sym is None:
                continue
            if prev[k] is not None and prev[k] != sym:
                return False
            prev[k] = sym
    return True


def main():
    obs = load()
    for text in VARIANTS:
        starts = [s for s in range(108) if compatible(text, s, obs)]
        print(f"{text!r} ({len(text)} chars): raw-compatible starts = {starts}")
        assert not starts, (text, starts)
    # The specific contradiction at the proposed alignment (start 0):
    assert obs[2] == "-" and obs[42] == "/"  # 'f' at chars 0 and 10, third symbol
    print("OK: CEO-door string is excluded by raw observations at every start")


if __name__ == "__main__":
    main()

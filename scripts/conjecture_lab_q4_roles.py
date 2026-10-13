#!/usr/bin/env python3
"""Closed-corpus positional-readout comparison for CE foreground symbols.

Reports compatible *sets*, not reconstructed text or a unique decode.
Run: python scripts/conjecture_lab_q4_roles.py
"""
import csv
import itertools
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get_observed():
    with (ROOT / "data/observations.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    seen = {}
    for row in rows:
        i, symbol = int(row["residue"]), row["symbol"]
        assert 1 <= i <= 108 and symbol in "./-"
        assert i not in seen or seen[i] == symbol
        seen[i] = symbol
    assert len(rows) == 84 and len(seen) == 66
    return seen


def minority_positions(observed, cells):
    accepted = set()
    for trip in itertools.product("./-", repeat=3):
        if len(set(trip)) != 2:
            continue
        if any(observed.get(cell, sym) != sym
               for cell, sym in zip(cells, trip)):
            continue
        accepted.add(next(i for i in range(3) if trip.count(trip[i]) == 1))
    return sorted(accepted)


def letters(triples, origin=0):
    output = set()
    for a, b, c in triples:
        code = 9*a + 3*b + c
        if origin <= code <= origin+25:
            output.add(chr(65+code-origin))
    return "".join(sorted(output))


def main():
    obs = get_observed()
    core = [
        [minority_positions(obs, [9*f+j+1, 9*f+j+4, 9*f+j+7])
         for j in range(3)]
        for f in range(9)
    ]
    assert all(all(options for options in frame) for frame in core)
    selector = [
        [depth for depth in range(3)
         if all(not obs.get(cell) or
                (obs[cell] == "/" if k == depth else obs[cell] != "/")
                for k, cell in enumerate([82+j, 91+j, 100+j]))]
        for j in range(9)
    ]
    assert math.prod(len(s) for s in selector) == 18
    assert not minority_positions(obs, [92,95,98])

    print("physical records=84, unique residues=66, unobserved=42")
    print("Q4 slash-depth choices per stack:", selector)
    print("Q4 completions of slash-index words:", math.prod(map(len,selector)))

    for origin in (0,1):
        body = [letters(itertools.product(*frame), origin) for frame in core]
        tail = [letters(itertools.product(*selector[3*i:3*i+3]),origin)
                for i in range(3)]
        picked = [
            sorted({v for k in selector[i] for v in core[i][k]})
            for i in range(9)
        ]
        selected = [
            letters(itertools.product(*picked[3*i:3*i+3]), origin)
            for i in range(3)
        ]
        rotated = []
        for f in range(9):
            choices = set()
            for tup in itertools.product(*core[f]):
                for amount in selector[f]:
                    tmp = tup[amount:]+tup[:amount]
                    choices.add(tmp)
            rotated.append(letters(sorted(choices),origin))
        count = lambda parts: math.prod(map(len, parts))
        print("A=",origin,sep="")
        print("  body:",body," count=",count(body))
        print("  appended-tail:",tail," count=",count(tail))
        print("  appended-total:",count(body)*count(tail))
        print("  selected:",selected," count=",count(selected))
        print("  rotated lengths:",list(map(len,rotated)),
              " count=",count(rotated))
    print("All outputs are conditional compatibility classes, not discovered plaintext.")


if __name__ == "__main__":
    main()

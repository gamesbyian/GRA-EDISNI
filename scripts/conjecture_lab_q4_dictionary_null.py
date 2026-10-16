#!/usr/bin/env python3
"""Adversarial dictionary control for a deliberately speculative positional reader.

Requires: numpy, cmudict==1.1.3. Uses the canonical closed observation corpus.
No web requests are made. Run from repository root:
    python scripts/conjecture_lab_q4_dictionary_null.py
"""
import itertools
import math

import cmudict
import numpy as np
from conjecture_lab_q4_roles import get_observed, minority_positions


def compute_core_and_selector():
    obs = get_observed()
    core = [
        [minority_positions(obs, [9*f+j+1, 9*f+j+4, 9*f+j+7])
         for j in range(3)]
        for f in range(9)
    ]
    q4 = [
        [depth for depth in range(3)
         if all(not obs.get(p) or
                (obs[p] == "/" if k == depth else obs[p] != "/")
                for k, p in enumerate((82+j, 91+j, 100+j)))]
        for j in range(9)
    ]
    assert math.prod(map(len, q4)) == 18
    return core, q4


def layouts():
    outputs = set()
    for base in (list(range(9)), [8, 0, 1, 2, 3, 4, 5, 6, 7]):
        matrix = np.asarray(base).reshape(3, 3)
        for reflected in (False, True):
            for rotation in range(4):
                changed = np.fliplr(matrix) if reflected else matrix
                outputs.add(tuple(np.rot90(changed, rotation).ravel().tolist()))
    assert len(outputs) == 16
    return sorted(outputs)


def code_masks(core, q4):
    masks = np.zeros((2, 6, 9), dtype=np.uint32)
    for conv, origin in enumerate((0, 1)):
        for pp, columns in enumerate(itertools.permutations(range(3))):
            for frame in range(9):
                for digits in itertools.product(*(core[frame][j] for j in columns)):
                    for amount in q4[frame]:
                        tr = digits[amount:] + digits[:amount]
                        code = 9*tr[0] + 3*tr[1] + tr[2]
                        letter = code-origin
                        if 0 <= letter < 26:
                            masks[conv, pp, frame] |= np.uint32(1 << letter)
    return masks


def main():
    core, q4 = compute_core_and_selector()
    masks = code_masks(core, q4)
    vocab = sorted({w.upper() for w in cmudict.words()
                    if len(w) == 9 and w.isascii() and w.isalpha()})
    bits = np.asarray([[1 << (ord(c)-65) for c in w] for w in vocab],
                      dtype=np.uint32)
    orderings = layouts()
    assert len(vocab) == 13124, "Wordlist changed: pin cmudict==1.1.3"

    def count_word_matches(permutation):
        count = 0
        permutation = np.asarray(permutation)
        for origin in range(2):
            for column_order in range(6):
                for ordering in orderings:
                    codes = masks[origin, column_order, permutation[list(ordering)]]
                    accepted = np.ones(len(vocab), dtype=bool)
                    for at in range(9):
                        accepted &= (codes[at] & bits[:, at]) != 0
                        if not accepted.any():
                            break
                    count += int(accepted.sum())
        return count

    observed = count_word_matches(np.arange(9))
    rng = np.random.default_rng(20261012)
    counts = [count_word_matches(rng.permutation(9)) for _ in range(250)]
    histogram = {v: counts.count(v) for v in sorted(set(counts))}
    print("dictionary size:", len(vocab))
    print("observed dictionary hits:", observed)
    print("shuffle count: 250; RNG seed: 20261012")
    print("null histogram:", histogram)
    print("null P(hit count >= observed):",
          sum(v >= observed for v in counts) / len(counts))
    assert observed == 1 and histogram == {0: 134, 1: 88, 2: 22, 3: 4, 4: 2}
    print("The observed one-word match is not unusual under this null.")


if __name__ == "__main__":
    main()

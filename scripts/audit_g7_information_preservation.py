#!/usr/bin/env python3
"""Experiment 321: weaken G7 from route semantics to information preservation.

Start from the same three first-pass functional families used by Experiment 278.

Test two generic non-collapse conditions only:
1. each selected q-indexed word contains all three ternary symbols exactly once;
2. the three functional families collectively select all three q indices exactly once.

Do not require the three selected words to be mutually distinct and do not use
route vocabulary, cycle type, terminal value, expected shell, or q=2-p.
"""

from __future__ import annotations

from itertools import product

FAMILIES = (
    ("102", "002", "120"),
    ("102", "012", "100"),
    ("102", "022", "100"),
)


def preserves_ternary_alphabet(word: str) -> bool:
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def main() -> None:
    all_candidates = []
    word_preserving = []
    q_balanced = []
    both = []

    for choices in product(range(3), repeat=3):
        words = tuple(FAMILIES[i][choices[i]] for i in range(3))
        row = (choices, words)
        all_candidates.append(row)

        preserves_words = all(preserves_ternary_alphabet(w) for w in words)
        uses_all_q = set(choices) == {0, 1, 2}

        if preserves_words:
            word_preserving.append(row)
        if uses_all_q:
            q_balanced.append(row)
        if preserves_words and uses_all_q:
            both.append(row)

    assert len(all_candidates) == 27
    assert len(word_preserving) == 4
    assert len(q_balanced) == 6
    assert both == [((2, 1, 0), ("120", "012", "102"))]

    print("Experiment 321")
    print("choice assignments tested:", len(all_candidates))
    print("all-selected-words preserve ternary alphabet:", len(word_preserving))
    print("q choices use 0/1/2 exactly once:", len(q_balanced))
    print("intersection:", len(both))
    print("unique choices:", both[0][0])
    print("unique words:", both[0][1])
    print("RESULT: canonical shell follows without a mutual-distinctness criterion")
    print("RESULT: G7 can be weakened to two generic information-preservation priors")


if __name__ == "__main__":
    main()

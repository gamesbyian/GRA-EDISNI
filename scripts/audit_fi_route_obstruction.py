#!/usr/bin/env python3
"""Experiment 288: test the coupled Q4 F+I branch against the Q3 route theorem.

Experiment 287 finds eight viable physical settings with the Q4 F+I polarity
branch. They retain:
  * 14 physical states;
  * first-pass rank 3;
  * terminal 100;
but change the three first-pass functional families from

    102/002/120
    102/012/100
    102/022/100

to

    102/202/120
    102/212/100
    102/222/100.

Experiment 278 derives Q3 without assuming q=2-p by choosing one q-indexed
word from each functional family and requiring:
  * every chosen word is a permutation of 0,1,2;
  * the three chosen route maps are mutually distinct.

This experiment applies exactly that preregistered route-shell criterion to the
F+I branch. It also checks invariance under global ternary relabeling: a symbol
permutation preserves whether a word is bijective and whether two words are
equal.
"""

from __future__ import annotations

from itertools import permutations, product


CANONICAL = (
    ("102", "002", "120"),
    ("102", "012", "100"),
    ("102", "022", "100"),
)

FI_BRANCH = (
    ("102", "202", "120"),
    ("102", "212", "100"),
    ("102", "222", "100"),
)


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(
            families[i][choices[i]]
            for i in range(3)
        )
        if not all(is_permutation(route) for route in routes):
            continue
        if len(set(routes)) != 3:
            continue
        result.append((choices, routes))
    return tuple(result)


def relabel_word(word, perm):
    return "".join(str(perm[int(ch)]) for ch in word)


def relabel_families(families, perm):
    return tuple(
        tuple(relabel_word(word, perm) for word in family)
        for family in families
    )


def main():
    canonical_shells = route_shells(CANONICAL)
    fi_shells = route_shells(FI_BRANCH)

    assert canonical_shells == (
        ((2, 1, 0), ("120", "012", "102")),
    )
    assert fi_shells == ()

    # Diagnose the obstruction directly.
    canonical_perms = tuple(
        tuple(word for word in family if is_permutation(word))
        for family in CANONICAL
    )
    fi_perms = tuple(
        tuple(word for word in family if is_permutation(word))
        for family in FI_BRANCH
    )
    assert canonical_perms == (
        ("102", "120"),
        ("102", "012"),
        ("102",),
    )
    assert fi_perms == (
        ("102", "120"),
        ("102",),
        ("102",),
    )

    # No global relabeling of ternary symbols can rescue the F+I branch.
    # Bijectivity and equality are invariant under such a relabeling.
    relabel_results = {}
    for perm in permutations(range(3)):
        relabeled = relabel_families(FI_BRANCH, perm)
        shells = route_shells(relabeled)
        relabel_results[perm] = shells
        assert shells == ()

    print("Experiment 288")
    print("canonical route shells:", canonical_shells)
    print("F+I route shells:", fi_shells)
    print("canonical reversible words by family:", canonical_perms)
    print("F+I reversible words by family:", fi_perms)
    print("global ternary relabelings tested:", len(relabel_results))
    print("RESULT: F+I branch admits no three-distinct-permutation Q3 route shell")
    print("RESULT: functional families 1 and 2 are both forced to the same route 102")
    print("RESULT: no global ternary relabeling can remove this obstruction")
    print("RESULT: F+I is a genuine nearby transducer branch, not an exact representation gauge")


if __name__ == "__main__":
    main()

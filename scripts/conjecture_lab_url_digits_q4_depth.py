#!/usr/bin/env python3
"""DISCOVER: exact URL-digit-to-Q4-depth compatibility and matched digit shuffles.

The nine source digits come from the independently recovered CE-background
Terminal41 route 534brn9653f9j8mmd. The target Q4 depth options are determined
only by physical sticker observations. No Steam or website requests are made.

Run: python scripts/conjecture_lab_url_digits_q4_depth.py
"""
import collections
import csv
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL_DIGITS = tuple(map(int, "534965398"))
NATIVE_CLASSES = "IABCDEFGH"
ALPHABETIC_CLASSES = "ABCDEFGHI"


def observed_q4():
    with (ROOT / "data/observations.csv").open(newline="") as stream:
        records = list(csv.DictReader(stream))
    obs = {}
    for row in records:
        residue, mark = int(row["residue"]), row["symbol"]
        assert 1 <= residue <= 108 and mark in "./-"
        assert residue not in obs or obs[residue] == mark
        obs[residue] = mark
    assert len(records) == 84 and len(obs) == 66
    allowed = {}
    for j, cls in enumerate(ALPHABETIC_CLASSES):
        allowed[cls] = tuple(
            depth for depth in range(3)
            if all(
                (82 + j + 9 * k not in obs)
                or ((obs[82 + j + 9 * k] == "/") == (k == depth))
                for k in range(3)
            )
        )
    assert list(allowed.values()) == [
        (0, 1, 2), (2,), (0, 1, 2), (1,), (0,), (1,),
        (0, 2), (2,), (2,)
    ]
    assert len(tuple(itertools.product(*allowed.values()))) == 18
    return allowed


def d4_indices():
    """Eight distinct square-rigid transformations of row-major positions."""
    transforms = []
    for reflection in (False, True):
        for quarter_turns in range(4):
            matrix = [list(range(r * 3, r * 3 + 3)) for r in range(3)]
            if reflection:
                matrix = [row[::-1] for row in matrix]
            for _ in range(quarter_turns):
                matrix = [
                    [matrix[2 - c][r] for c in range(3)]
                    for r in range(3)
                ]
            transforms.append((
                reflection, quarter_turns,
                tuple(index for row in matrix for index in row)
            ))
    assert len({entry[2] for entry in transforms}) == 8
    return transforms


def lookup_compatible(digits, classes, allowed):
    """Does *any* deterministic lookup digit -> one of three depths exist?"""
    common = {}
    for digit, cls in zip(digits, classes):
        common[digit] = (common[digit].intersection(allowed[cls])
                         if digit in common else set(allowed[cls]))
    return all(common.values()), common


def monotone_tables():
    """All increasing/decreasing 3-bin partitions of digits 1...9."""
    tables = []
    for c1 in range(1, 9):
        for c2 in range(c1 + 1, 9):
            for reverse in (False, True):
                values = tuple(
                    ((2 if d <= c1 else 1 if d <= c2 else 0)
                     if reverse else
                     (0 if d <= c1 else 1 if d <= c2 else 2))
                    for d in range(1, 10)
                )
                tables.append((reverse, c1, c2, values))
    assert len(tables) == 56
    return tuple(tables)


def compatible_monotone(digits, classes, allowed, maps, symmetries):
    """The complete list of matches, with inspected parameters disclosed."""
    matches = []
    for reverse, c1, c2, table in maps:
        values = tuple(table[d - 1] for d in digits)
        for reflected, rotated, indices in symmetries:
            if all(
                values[indices[i]] in allowed[cls]
                for i, cls in enumerate(classes)
            ):
                matches.append((reverse, c1, c2, reflected, rotated))
    return matches


def exact_shuffle_control(allowed, transforms, maps):
    """Uniform null over all 9!/(2!2!2!) distinct permutations of URL digits."""
    distinct = set(itertools.permutations(URL_DIGITS))
    assert len(distinct) == 45360
    arbitrary_hist = collections.Counter()
    monotone_hist = collections.Counter()
    expected_choices = tuple(set(allowed[c]) for c in NATIVE_CLASSES)
    index_maps = tuple(entry[2] for entry in transforms)
    unique_tables = tuple(row[3] for row in maps)
    for arrangement in distinct:
        rotated = tuple(
            tuple(arrangement[k] for k in index_map)
            for index_map in index_maps
        )
        arbitrary = 0
        for trial in rotated:
            assignments = {}
            for digit, choices in zip(trial, expected_choices):
                if digit not in assignments:
                    assignments[digit] = choices.copy()
                else:
                    assignments[digit].intersection_update(choices)
            arbitrary += all(assignments.values())
        arbitrary_hist[arbitrary] += 1

        monotone = 0
        for table in unique_tables:
            for trial in rotated:
                if all(
                    table[digit - 1] in choices
                    for digit, choices in zip(trial, expected_choices)
                ):
                    monotone += 1
        monotone_hist[monotone] += 1
    assert arbitrary_hist == {0: 4680, 1: 15552, 2: 18720,
                               3: 4608, 4: 1800}, arbitrary_hist
    assert monotone_hist == {0: 41952, 1: 1824, 2: 792, 3: 456,
                              4: 192, 5: 96, 6: 24, 7: 24}, monotone_hist
    return arbitrary_hist, monotone_hist


def main():
    q4 = observed_q4()
    orientations = d4_indices()
    mappings = monotone_tables()
    print("Observed Q4 depths:", q4)
    print("Source URL digits, physical row-major I/A/B C/D/E F/G/H:",
          "".join(map(str, URL_DIGITS)))

    compatible, lookup = lookup_compatible(URL_DIGITS, NATIVE_CLASSES, q4)
    assert not compatible
    assert lookup[5] == set()  # I requires 2; E requires 0.
    print("Unrotated native digit lookup: IMPOSSIBLE (digit 5 at I and E)")

    for classes in (NATIVE_CLASSES, ALPHABETIC_CLASSES):
        free = []
        native_row_column = []
        for flip, rotation, indices in orientations:
            digits = tuple(URL_DIGITS[i] for i in indices)
            works, _ = lookup_compatible(digits, classes, q4)
            if works:
                free.append((flip, rotation))
            row = tuple((d - 1) // 3 for d in digits)
            col = tuple((d - 1) % 3 for d in digits)
            native_row_column.append((
                flip, rotation,
                sum(n not in q4[cls] for n, cls in zip(row, classes)),
                sum(n not in q4[cls] for n, cls in zip(col, classes))
            ))
        winners = compatible_monotone(
            URL_DIGITS, classes, q4, mappings, orientations
        )
        print("Class order:", classes)
        print("  D4 transforms permitting any digit lookup:", free)
        print("  Exact DTMF row/column mismatch counts:", native_row_column)
        print("  Monotone partition D4 matches:", winners)
        if classes == NATIVE_CLASSES:
            assert len(free) == 4
            assert winners == [(True, 5, 8, True, 0)]
        else:
            assert len(free) == 0 and not winners

    # Preserve the sole retrospectively fitted monotone variant as a frozen,
    # distinctly NON-BLIND physical discriminator, not evidence of intent.
    mirror = next(indices for flip, turns, indices in orientations
                  if flip and turns == 0)
    digits = tuple(URL_DIGITS[i] for i in mirror)
    depths = tuple(2 if d <= 5 else 1 if d <= 8 else 0 for d in digits)
    fitted_depths = dict(zip(NATIVE_CLASSES, depths))
    assert fitted_depths == {
        "I": 2, "A": 2, "B": 2, "C": 2, "D": 1,
        "E": 0, "F": 1, "G": 0, "H": 2
    }
    variant = {
        82 + ALPHABETIC_CLASSES.index(cls) + 9 * depth:
        "/" if depth == fitted_depths[cls] else "."
        for cls in "ACG" for depth in range(3)
    }
    assert variant == {82: ".", 91: ".", 100: "/",
                       84: ".", 93: ".", 102: "/",
                       88: "/", 97: ".", 106: "."}
    print("Fitted native depth assignment:", fitted_depths)
    print("Conditional A/C/G Q4 predictions, r97 already confirmed:",
          dict(sorted(variant.items())))

    arbitrary, monotone = exact_shuffle_control(q4, orientations, mappings)
    total = sum(arbitrary.values())
    assert total == sum(monotone.values()) == 45360
    p_4 = sum(k >= 4 and n or 0 for k, n in arbitrary.items()) / total
    p_monotone = sum(k >= 1 and n or 0 for k, n in monotone.items()) / total
    print("Matched digit-permutation null cardinality:", total)
    print("Number of compatible arbitrary-lookup D4 orientations:", dict(sorted(arbitrary.items())))
    print("Fraction with >=4 compatible orientations:", p_4)
    print("Number of matching monotone-codebook x D4 choices:", dict(sorted(monotone.items())))
    print("Fraction with >=1 monotone match:", p_monotone)
    assert sum(n for k, n in arbitrary.items() if k >= 4) == 1800
    assert sum(n for k, n in monotone.items() if k >= 1) == 3408
    print("Results are post-search descriptive controls, not CE decoder validation.")


if __name__ == "__main__":
    main()

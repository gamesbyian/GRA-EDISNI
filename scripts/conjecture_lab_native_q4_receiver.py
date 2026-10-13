#!/usr/bin/env python3
"""Speculative native A-I/Q4 selector versus a recovered INSIDE printer image.

No network or live password submission. Uses repo fixtures, missing cells stay
unknown. Run: python scripts/conjecture_lab_native_q4_receiver.py
"""
import csv
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNS = "./-"
PRINT_LAYOUT = ("IAB", "CDE", "FGH")


def source_data():
    with (ROOT / "data/observations.csv").open(newline="") as source:
        rows = list(csv.DictReader(source))
    known = {}
    for row in rows:
        residue, symbol = int(row["residue"]), row["symbol"]
        assert 1 <= residue <= 108 and symbol in SIGNS
        assert residue not in known or known[residue] == symbol
        known[residue] = symbol
    assert len(rows) == 84 and len(known) == 66
    lines = (ROOT / "data/printer-reference/pc-ps4-acorn-order.txt").read_text().splitlines()
    acorn = tuple(s for s in lines if len(s) == 32 and set(s) <= set(SIGNS))
    assert len(acorn) == 32
    return known, acorn


def core_groups(known):
    """All admissible raw triplets at positions 1-4-7, 2-5-8, 3-6-9."""
    patterns = ("".join(s) for s in itertools.product(SIGNS, repeat=3))
    patterns = tuple(s for s in patterns if len(set(s)) == 2)
    output = []
    for frame in range(9):
        groups = []
        for col in range(3):
            sites = [1 + 9 * frame + col + 3*k for k in range(3)]
            allowed = tuple(
                s for s in patterns
                if all(known.get(p, char) == char for p, char in zip(sites, s))
            )
            assert allowed, (frame, col)
            groups.append(allowed)
        output.append(tuple(groups))
    return tuple(output)


def q4_choices(known):
    """Q4 slash depth per background class, nine positions times three depths."""
    return tuple(
        tuple(
            depth for depth in range(3)
            if all(
                site not in known or
                ((known[site] == "/") == (k == depth))
                for k, site in enumerate([82+j, 91+j, 100+j])
            )
        )
        for j in range(9)
    )


def requested_cells(selector):
    """For each core triplet, map selected cell index to output column j."""
    return tuple(
        tuple(
            tuple((k, col+3*k) for k in range(3)
                  if selector[col+3*k] == frame % 3)
            for col in range(3)
        )
        for frame in range(9)
    )


def min_disagreements(panel, groups, requested, bound=28):
    """Optimal mismatch count over all compatible missing core cells."""
    result = 0
    for frame in range(9):
        quarter = frame // 3
        for col in range(3):
            wanted = requested[frame][col]
            if wanted:
                result += min(
                    sum(s[k] != panel[quarter][j] for k, j in wanted)
                    for s in groups[frame][col]
                )
                if result > bound:
                    return result
    return result


def symbol_bounds(groups, selections):
    output = {}
    for mark in SIGNS:
        lowest, highest = 28, -1
        for selector in selections:
            wanted = requested_cells(selector)
            lo = hi = 0
            for frame in range(9):
                for col in range(3):
                    positions = [k for k, _ in wanted[frame][col]]
                    counts = [
                        sum(s[k] == mark for k in positions)
                        for s in groups[frame][col]
                    ]
                    lo += min(counts)
                    hi += max(counts)
            lowest, highest = min(lowest, lo), max(highest, hi)
        output[mark] = (lowest, highest)
    return output


def class_options(groups, choices):
    result = {}
    for j, depths in enumerate(choices):
        three_symbol_words = set()
        for d in depths:
            positions = [
                {s[j // 3] for s in groups[3*q+d][j % 3]}
                for q in range(3)
            ]
            three_symbol_words.update(
                "".join(chars) for chars in itertools.product(*positions)
            )
        result["ABCDEFGHI"[j]] = tuple(sorted(three_symbol_words))
    return result


def synthesise(selector, groups):
    """Guaranteed valid synthetic 3x9 output for internal positive control."""
    panel = [list("?"*9) for _ in range(3)]
    for j, depth in enumerate(selector):
        for q in range(3):
            frame = 3*q+depth
            panel[q][j] = groups[frame][j % 3][0][j // 3]
    return tuple("".join(row) for row in panel)


def subwindows(source, transpose, flip_rows, flip_columns):
    height, width = (9,3) if transpose else (3,9)
    for y0 in range(33-height):
        for x0 in range(33-width):
            panel = []
            for q in range(3):
                line = []
                for j in range(9):
                    y = 2-q if flip_rows else q
                    x = 8-j if flip_columns else j
                    line.append(
                        source[y0+x][x0+y] if transpose else
                        source[y0+y][x0+x]
                    )
                panel.append("".join(line))
            yield y0, x0, tuple(panel)


def main():
    observed, acorn = source_data()
    core = core_groups(observed)
    depth_options = q4_choices(observed)
    assert all(depth_options)
    selectors = tuple(itertools.product(*depth_options))
    assert len(selectors) == 18

    projected = class_options(core, depth_options)
    print("Q4 depth options per A-I class:", dict(zip("ABCDEFGHI", depth_options)))
    for panel_row in PRINT_LAYOUT:
        print("  ", " | ".join(
            c + ":" + "".join(map(str, depth_options[ord(c)-65]))
            for c in panel_row
        ))
    print("Compatible 3-sign strings per class:")
    for klass in "ABCDEFGHI":
        print(" ", klass, len(projected[klass]), " ".join(projected[klass]))
    assert projected["B"] == ("//-",)
    assert projected["E"] == projected["F"] == ("///",)
    assert projected["H"] == ("--/",)
    bounds = symbol_bounds(core, selectors)
    assert bounds == {".": (0, 6), "/": (14, 23), "-": (4, 12)}
    print("Exact output-sign count bounds:", bounds)

    prepared = tuple((sel, requested_cells(sel)) for sel in selectors)
    synthetic = synthesise(*((prepared[0][0], core)))
    assert min_disagreements(synthetic, core, prepared[0][1]) == 0
    changed = list(synthetic)
    damaged = list(changed[0])
    damaged[4] = "."  # E quarter 0 is definitely slash.
    changed[0] = "".join(damaged)
    assert min_disagreements(changed, core, prepared[0][1]) >= 1

    n = accepted = 0
    best = (28, None)
    for perm in itertools.permutations(SIGNS):
        trans = dict(zip(SIGNS, perm))
        image = tuple("".join(trans[s] for s in line) for line in acorn)
        for transpose, flip_rows, flip_columns in itertools.product(
            (False, True), repeat=3
        ):
            for y, x, panel in subwindows(
                image, transpose, flip_rows, flip_columns
            ):
                for sel, requested in prepared:
                    n += 1
                    distance = min_disagreements(
                        panel, core, requested, best[0]
                    )
                    accepted += distance == 0
                    if distance < best[0]:
                        best = (distance, (perm, transpose, flip_rows,
                                           flip_columns, y, x, sel))
    assert n == 6 * 8 * 720 * 18 == 622080
    print("Exact PC/PS4 acorn window tests:", n)
    print("Zero-conflict compatible projections:", accepted)
    print("Minimum necessary output-symbol disagreements:", best[0])
    print("Best retrospective registration:", best[1])
    assert accepted == 0 and best[0] == 1
    print("Reject only the tested literal 3x9/9x3 acorn-subwindow receiver.")


if __name__ == "__main__":
    main()

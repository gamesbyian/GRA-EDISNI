#!/usr/bin/env python3
"""Bounded literal 27-mark comparison to authenticated historical printer rows.

Only source-fixed window lengths (32 PC/PS4, 36 Xbox) and four documented
simple identities (forward/reverse, slash/dash polarity) are evaluated.
We DO NOT claim substring similarity establishes shared authorial decoding.

Run: python scripts/audit_middle_depth_printer_control.py
     python scripts/audit_middle_depth_printer_control.py --output /tmp/print-control.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_finite_receiver_invariance import physical_observations, fixed_depth, populations

ROOT = Path(__file__).resolve().parents[1]
CORPORA = (
    ("pc_ps4_raw", ROOT / "data/printer-reference/pc-ps4-raw.txt", 32, 32),
    ("pc_ps4_solved_acorn_order",
     ROOT / "data/printer-reference/pc-ps4-acorn-order.txt", 32, 32),
    ("xbox_one_raw", ROOT / "data/printer-reference/xbox-one-raw.txt", 36, 36),
)


def lines(path: Path, width: int, expected: int) -> list[str]:
    out = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
           if len(line.strip()) == width and set(line.strip()) <= set(".-/")]
    assert len(out) == expected, (path, len(out), expected)
    return out


def invert(word: str) -> str:
    return word.translate(str.maketrans("/-", "-/"))


def variants(word: str) -> dict[str, str]:
    return {
        "literal": word,
        "reverse": word[::-1],
        "invert_slash_dash": invert(word),
        "reverse_invert_slash_dash": invert(word[::-1]),
    }


def compare(rows: list[str], word: str) -> dict:
    size = len(rows[0])
    assert all(len(line) == size for line in rows)
    assert len(word) <= size
    results = {}
    for convention, query in variants(word).items():
        scores = [
            (sum(mark != "?" and mark != line[start+j]
                 for j, mark in enumerate(query)),
             row, start)
            for row, line in enumerate(rows)
            for start in range(size-len(query)+1)
        ]
        min_dist = min(dist for dist, _row, _start in scores)
        winners = [(row, start) for dist, row, start in scores if dist == min_dist]
        results[convention] = {
            "minimum_hamming_mismatches": min_dist,
            "windows_at_minimum": len(winners),
            "best_window_row_index0_offset0": list(winners[0]),
            "exact_matches": sum(dist == 0 for dist, _row, _start in scores),
            "tested_windows": len(scores)
        }
    return results


def audit() -> dict:
    physical = physical_observations()
    members = populations()
    fixed_words = {fixed_depth(word, 1) for word in members["U2"]}
    assert fixed_words == {"---/-/-/--//////--//////---"}
    fixed = next(iter(fixed_words))
    sites = [q*27 + 10 + j for q in range(3) for j in range(9)]
    masked = "".join(physical.get(r, "?") for r in sites)
    assert masked == "-?-/-/?/--///?//-??//??/---"
    assert masked.count("?") == 7
    assert all(a == b for a,b in zip(fixed,masked) if b != "?")

    results = {}
    for name,path,width,count in CORPORA:
        source = lines(path,width,count)
        exact = compare(source,fixed)
        partial = compare(source,masked)
        results[name] = {
            "source":str(path.relative_to(ROOT)),
            "source_row_count":len(source),"native_row_width":width,
            "complete_u2_conditional_word":exact,
            "direct_physical_20_mark_mask":partial,
        }
    assert {name: tuple(row["complete_u2_conditional_word"][key]
                              ["minimum_hamming_mismatches"]
                               for key in ("literal","reverse","invert_slash_dash",
                                           "reverse_invert_slash_dash"))
            for name,row in results.items()} == {
                "pc_ps4_raw":(6,6,10,8),
                "pc_ps4_solved_acorn_order":(6,6,10,8),
                "xbox_one_raw":(4,7,10,11),
            }
    assert {name: tuple(row["direct_physical_20_mark_mask"][key]
                              ["minimum_hamming_mismatches"]
                               for key in ("literal","reverse","invert_slash_dash",
                                           "reverse_invert_slash_dash"))
            for name,row in results.items()} == {
                "pc_ps4_raw":(4,4,6,5),
                "pc_ps4_solved_acorn_order":(4,4,6,5),
                "xbox_one_raw":(3,5,8,7),
            }
    assert all(
        variant["exact_matches"] == 0
        for row in results.values()
        for table in ("complete_u2_conditional_word","direct_physical_20_mark_mask")
        for variant in row[table].values()
    )

    return {
        "research_mode":"DEVELOP; finite historical-receiver literal control only",
        "fixed_middle_depth_u2":"---/-/-/--//////--//////---",
        "physical_20_symbol_mask":masked,
        "corpora":results,
        "interpretation":(
            "Neither the model-imputed U2 fixed 27-mark word nor its 20-mark "
            "physical subset occurs as a contiguous 27-wide window in any "
            "authenticated PC/PS4 or Xbox full-width printer row under four "
            "fixed order/polarity conventions."
        ),
        "limitations":[
            "No row-spanning scan, arbitrary permutation, rotation of assembled full image, or overlay evaluated.",
            "PC raw and acorn ordered rows are the same 32 strings, not independent evidence.",
            "Window/hamming similarity is a diagnostic, not an ARG decoding criterion.",
            "This cannot exclude nonliteral or noncontiguous cross-ARG use of the printer images.",
        ]
    }


def self_test() -> None:
    assert compare(["---/"],"---/")["literal"]["minimum_hamming_mismatches"] == 0
    assert compare(["-/-/"],"?/-/")["literal"]["minimum_hamming_mismatches"] == 0
    assert invert("///---...") == "---///..."
    print("synthetic substring controls: pass")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    self_test()
    if args.self_test:
        return
    result = audit()
    encoded = json.dumps(result,indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
        print(f"saved {args.output}")
    else:
        print(encoded)


if __name__ == "__main__":
    main()

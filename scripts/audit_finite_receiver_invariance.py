#!/usr/bin/env python3
"""Finite CE sticker readouts evaluated against exact U2/U3/U4/U5 completions.

Research mode: DEVELOP, not an identified decoder or CE recipient.

Uses existing independently implemented population generators rather than
regenerating, hand-picking, or imputing missing sticker symbols.

Run:
  python scripts/audit_finite_receiver_invariance.py
  python scripts/audit_finite_receiver_invariance.py --output /tmp/receiver-frontier.json
  python scripts/audit_finite_receiver_invariance.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Callable

from audit_completion_universe_layers import machine_layers
from build_completion_universe import build

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data/observations.csv"
LETTERS = "ABCDEFGHI"
LAYOUT = ("IAB", "CDE", "FGH")
POS = {letter: (row, col)
       for row, word in enumerate(LAYOUT)
       for col, letter in enumerate(word)}
NO_POS3 = "INVALID"
EXPECTED = {
    "family_counts": {"U2": 324, "U3": 108, "U4": 12, "U5": 10},
    "tail_depth9": [18, 18, 6, 4],
    "fixed_middle_depth27": [1, 1, 1, 1],
    "selected_depth27": [68, 30, 3, 2],
    "selected_pos3_triplet": [16, 13, 3, 2],
    "terminal_pos3": [2, 2, 2, 1],
    "class9_binary_addresses": [18, 6, 5, 4],
    "primary_dash_census_by_quarter": [2, 1, 1, 1],
    "full_mark_census": [2, 1, 1, 1],
}


def physical_observations() -> dict[int, str]:
    observed = {}
    serials = set()
    with OBS.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 84, len(rows)
    for row in rows:
        serial, residue, symbol = (
            int(row["serial"]), int(row["residue"]), row["symbol"])
        assert serial not in serials
        serials.add(serial)
        assert (serial - 1) % 108 + 1 == residue
        assert symbol in ("/", "-") if residue <= 81 else symbol in ("/", ".")
        assert residue not in observed or observed[residue] == symbol
        observed[residue] = symbol
    assert len(observed) == 66
    return observed


def populations() -> dict[str, list[str]]:
    _report, u2, _unknown = build()
    u3, u4, u5 = machine_layers()
    result = {"U2": [word for *_prefix, word in u2],
              "U3": u3, "U4": u4, "U5": u5}
    assert {name: len(words) for name, words in result.items()} == EXPECTED["family_counts"]
    assert all(len(set(words)) == len(words) for words in result.values())
    assert all(set(result[n]).issubset(set(result[p])) for n, p
               in (("U3", "U2"), ("U4", "U3"), ("U5", "U4")))
    return result


def selector(word: str) -> tuple[int, ...]:
    out = []
    for j in range(9):
        sites = [d for d in range(3) if word[81 + 9*d + j] == "/"]
        assert len(sites) == 1, (j, sites)
        out.append(sites[0])
    return tuple(out)


def chosen_surface(word: str, q: int, terminal: bool = False) -> str:
    s = selector(word)
    return "".join(word[27*(s[j] if terminal else q) + 9*s[j] + j]
                   for j in range(9))


def pos3(word9: str) -> str:
    assert len(word9) == 9
    result = []
    for col in range(3):
        dash_rows = [row for row in range(3)
                     if word9[LETTERS.index(LAYOUT[row][col])] == "-"]
        if len(dash_rows) != 1:
            return NO_POS3
        result.append(str(dash_rows[0]))
    return "".join(result)


def fixed_depth(word: str, depth: int) -> str:
    return "".join(word[q*27 + depth*9:q*27 + depth*9 + 9]
                   for q in range(3))


def selected_read(word: str) -> str:
    return "".join(chosen_surface(word, q) for q in range(3))


def tail_depth9(word: str) -> str:
    return "".join(map(str, selector(word)))


def selected_pos3_triplet(word: str) -> str:
    return "/".join(pos3(chosen_surface(word, q)) for q in range(3))


def terminal_pos3(word: str) -> str:
    return pos3(chosen_surface(word, 0, terminal=True))


def nine_class_addresses(word: str) -> str:
    nums = []
    for j in range(9):
        bits = "".join("1" if word[9*f+j] == "/" else "0" for f in range(9))
        nums.append(str(int(bits, 2)))
    return ",".join(nums)


def primary_dash_census(word: str) -> str:
    return ",".join(str(word[q*27:q*27+27].count("-")) for q in range(3))


def full_census(word: str) -> str:
    return ",".join(str(word.count(mark)) for mark in ("/", "-", "."))


# These are transparently chosen bounded *readout probes*, NOT discovered
# original Playdead decoder instructions. Order stable for reproducibility.
READOUTS: tuple[tuple[str, Callable[[str], str], str], ...] = (
    ("tail_depth9", tail_depth9, "nine one-hot Q4 depths"),
    ("tail_raw27", lambda w: w[81:], "full physical Q4 marks"),
    ("primary_raw81", lambda w: w[:81], "full physical primary marks"),
    ("fixed_depth0_27", lambda w: fixed_depth(w, 0), "three q slices at d=0"),
    ("fixed_middle_depth27", lambda w: fixed_depth(w, 1), "three q slices at d=1"),
    ("fixed_depth2_27", lambda w: fixed_depth(w, 2), "three q slices at d=2"),
    ("selected_depth27", selected_read, "Q4 selects one depth per A-I site"),
    ("selected_pos3_triplet", selected_pos3_triplet,
     "selected 3x3 physical-column positional words; INVALID retained"),
    ("terminal_pos3", terminal_pos3,
     "Q4 selected depth reused as q; INVALID retained"),
    ("class9_binary_addresses", nine_class_addresses,
     "nine 9-bit binary A-I column addresses; slash=1; serial order"),
    ("primary_dash_census_by_quarter", primary_dash_census,
     "primary dashes across three 27-site quarters"),
    ("full_mark_census", full_census, "whole H108 slash/dash/dot counts"),
)


def summarise(values: list[str]) -> dict:
    counts = Counter(values)
    assert sum(counts.values()) == len(values)
    unique = sorted(counts)
    same_width = len({len(v) for v in unique}) == 1
    mask = None
    if same_width:
        mask = "".join(c if all(v[i] == c for v in unique) else "?"
                       for i, c in enumerate(unique[0]))
    return {
        "distinct_outputs": len(unique),
        "invariant": len(unique) == 1,
        "fixed_character_mask": mask if mask and len(mask) <= 40 else None,
        "all_outputs": unique if len(unique) <= 6 else None,
        "output_counts": dict(sorted(counts.items())) if len(unique) <= 6 else None,
        "invalid_masters": counts.get(NO_POS3, 0),
    }


def audit() -> dict:
    seen = physical_observations()
    groups = populations()
    outputs = {}
    for key, fn, meaning in READOUTS:
        outputs[key] = {
            "operation": meaning,
            "families": {name: summarise([fn(word) for word in words])
                         for name, words in groups.items()}
        }

    assert all(
        [outputs[k]["families"][u]["distinct_outputs"] for u in groups]
        == expected
        for k, expected in EXPECTED.items()
        if k != "family_counts"
    )
    assert outputs["fixed_middle_depth27"]["families"]["U2"]["all_outputs"] == [
        "---/-/-/--//////--//////---"
    ]
    assert outputs["terminal_pos3"]["families"]["U2"]["output_counts"] == {
        NO_POS3: 180, "100": 144
    }
    assert outputs["terminal_pos3"]["families"]["U3"]["output_counts"] == {
        NO_POS3: 60, "100": 48
    }
    assert outputs["terminal_pos3"]["families"]["U4"]["output_counts"] == {
        NO_POS3: 2, "100": 10
    }
    assert outputs["terminal_pos3"]["families"]["U5"]["output_counts"] == {
        "100": 10
    }

    mid_residues = [q*27 + 9 + j + 1 for q in range(3) for j in range(9)]
    assert len(set(mid_residues) & seen.keys()) == 20
    # "middle-depth" fixed *conditional* values, seven unseen physical cells.
    mid_unobserved = [r for r in mid_residues if r not in seen]
    assert mid_unobserved == [11, 16, 41, 45, 64, 67, 68]

    # Within U5 the selected-depth readout has two strings; it differs at
    # precisely four readout coordinates. This does not identify a consumer.
    u5_words = outputs["selected_depth27"]["families"]["U5"]["all_outputs"]
    assert u5_words and len(u5_words) == 2
    diff = [j+1 for j in range(27) if u5_words[0][j] != u5_words[1][j]]
    assert diff == [10, 16, 19, 25], diff
    ambiguous_cells = [
        {"output_slot_1_based": slot,
         "quarter_1_based": (slot - 1)//9 + 1,
         "background_class": LETTERS[(slot - 1)%9],
         "physical_row_col_1_based":
             [POS[LETTERS[(slot - 1)%9]][0]+1,
              POS[LETTERS[(slot - 1)%9]][1]+1]}
        for slot in diff
    ]
    assert [cell["background_class"] for cell in ambiguous_cells] == [
        "A", "G", "A", "G"
    ]
    assert [cell["quarter_1_based"] for cell in ambiguous_cells] == [2, 2, 3, 3]
    assert {cell["physical_row_col_1_based"][1] for cell in ambiguous_cells} == {2}

    # A genuine hypothetical consumer example: parity of selected output.
    # Report as a functional projection, NOT evidence of parity/ECC authorship.
    hypothetical_parity = {}
    for family, words in groups.items():
        grouped = Counter(selected_read(word).count("-") % 2 for word in words)
        hypothetical_parity[family] = dict(sorted(grouped.items()))
    assert sum(hypothetical_parity["U2"].values()) == 324

    return {
        "research_mode": "DEVELOP / finite typed readout probes; no CE receiver verified",
        "physical_records": 84,
        "distinct_h108_residues": 66,
        "family_members": {name: len(words) for name, words in groups.items()},
        "readouts": outputs,
        "fixed_middle_depth": {
            "word": "---/-/-/--//////--//////---",
            "physically_observed_positions": 20,
            "conditionally_reconstructed_positions": 7,
            "reconstructed_residues": mid_unobserved,
        },
        "u5_selected_depth27": {
            "two_possible_words": u5_words,
            "differing_output_slots_1_based": diff,
            "ambiguous_cells": ambiguous_cells,
            "invariant_slots_1_based": [
                slot for slot in range(1, 28) if slot not in diff
            ],
        },
        "terminal_100_scope": {
            "U2": {"valid_100": 144, "invalid": 180},
            "U3": {"valid_100": 48, "invalid": 60},
            "U4": {"valid_100": 10, "invalid": 2},
            "U5": {"valid_100": 10, "invalid": 0},
            "interpretation": (
                "Whenever this particular Q4 double-selection surface is a valid "
                "single-dash-per-physical-column POS3 code, its readout is 100 "
                "even without first-pass closure. This is a conditional "
                "structural degeneracy, not a proven externally consumed key."
            )
        },
        "hypothetical_selected_dash_parity": hypothetical_parity,
        "limits": [
            "These finite operation choices are declared probes, not independently specified original decoders.",
            "U2/U3/U4/U5 are nested interpretations of the same 66 physical positions.",
            "Identical readouts under an assumed grammar do not prove intended solve path.",
            "A source-authored receiver and acceptance test are still missing.",
            "Physical gauge families outside U2 require separate expansion before claiming universal invariance."
        ]
    }


def self_test() -> None:
    assert pos3("---//////") == "100"
    assert pos3("/////////") == NO_POS3
    assert pos3("---//////") != pos3("-/-////-/")
    fake = "a"*108
    assert fixed_depth(fake, 1) == "a"*27
    assert summarise(["a", "a", "b"])["distinct_outputs"] == 2
    assert summarise(["abc", "axc"])["fixed_character_mask"] == "a?c"
    print("small synthetic controls: pass")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, help="write a JSON result to this path")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    self_test()
    if args.self_test:
        return
    result = audit()
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"saved {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CX-E3: two *literal* receiver controls for proposed 4/9/12 rail fields.

(1) The four nine-site middle fields comprise a 36-character object.
    Test three source-fixed layouts against all original long Xbox
    printer rows, forward and reversed, using only observed sites.
(2) The nine background URL digits are assigned to image classes in
    independently solved IAB/CDE/FGH physical order. If a digit is a
    literal shared-state lookup key, equal digit labels MUST have
    equal CE marks within each quarter. Find forced contradictions.

This closes only literal identity/readout assumptions, not any
transform, keyed XOR, multiple-pass reader or hypothetical receiver.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = "IABCDEFGH"
SERIAL = "FGHIABCDE"
URL_DIGITS = "534965398"


def observations(path):
    obs = {}
    with Path(path).open(newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            residue = int(row["residue"])
            mark = row["symbol"].strip()
            assert 1 <= residue <= 108
            assert mark in ("/", "-", ".")
            expected = "ABCDEFGHI"[(residue - 1) % 9]
            assert row["image_class"].strip() in ("", expected)
            assert residue not in obs or obs[residue] == mark
            obs[residue] = mark
    return obs


def printer_rows(path):
    lines = Path(path).read_text(encoding="utf8").splitlines()
    long = [x for x in lines if len(x) == 36 and set(x) <= set("/-.")]
    unique = list(dict.fromkeys(long))
    assert len(long) == 36 and len(unique) == 35
    return unique


def run(obs_path, xbox_path):
    obs = observations(obs_path)
    printer = printer_rows(xbox_path)
    fields = []
    for quarter in range(4):
        rows = [(quarter*27+6+j, SERIAL[j], obs.get(quarter*27+6+j, "?"))
                for j in range(9)]
        assert "".join(r[1] for r in rows) == SERIAL
        fields.append({cl: mark for _, cl, mark in rows})
    raw = {
        "quarter_serial": "".join("".join(f[c] for c in SERIAL) for f in fields),
        "quarter_physical": "".join("".join(f[c] for c in PHYSICAL) for f in fields),
        "class_major": "".join("".join(f[c] for f in fields) for c in PHYSICAL),
    }
    # The twelve-site suffix itself begins with another full nine-class
    # cycle. Give it the same *literal* Xbox-row controls, separately.
    suffix_order = "GHIABCDEF"
    suffix_fields = []
    for quarter in range(4):
        byclass = {suffix_order[j]: obs.get(quarter*27+16+j, "?")
                   for j in range(9)}
        suffix_fields.append(byclass)
    raw.update({
        "suffix_quarter_serial": "".join(
            "".join(f[c] for c in suffix_order) for f in suffix_fields),
        "suffix_quarter_physical": "".join(
            "".join(f[c] for c in PHYSICAL) for f in suffix_fields),
        "suffix_class_major": "".join(
            "".join(f[c] for f in suffix_fields) for c in PHYSICAL),
    })
    tests = {}
    for kind, target in raw.items():
        assert len(target) == 36
        matches = []
        for index, row in enumerate(printer, 1):
            for direction, candidate in (("forward", row), ("reverse", row[::-1])):
                conflicts = [{"index_1based": i+1, "observed": symbol,
                              "xbox": candidate[i]}
                             for i, symbol in enumerate(target)
                             if symbol != "?" and symbol != candidate[i]]
                matches.append({"source_unique_row": index,
                                "orientation": direction,
                                "known": sum(x != "?" for x in target),
                                "conflicts": len(conflicts),
                                "first_five_conflicts": conflicts[:5]})
        matches.sort(key=lambda x: (x["conflicts"], x["source_unique_row"],
                                   x["orientation"] != "forward"))
        tests[kind] = {
            "partial_pattern": target,
            "comparisons": len(matches),
            "best_conflicts": matches[0]["conflicts"],
            "best_matches": [x for x in matches if
                             x["conflicts"] == matches[0]["conflicts"]],
            "exact_matches": sum(x["conflicts"] == 0 for x in matches),
        }
    repeated = defaultdict(list)
    for cl, digit in zip(PHYSICAL, URL_DIGITS):
        repeated[digit].append(cl)
    assert {d:len(v) for d,v in repeated.items()} == {
        "5":2, "3":2, "4":1, "9":2, "6":1, "8":1}
    conflicts = []
    comparable = []
    for qi, field in enumerate(fields, 1):
        for digit, cls in repeated.items():
            if len(cls) != 2:
                continue
            c1, c2 = cls
            x, y = field[c1], field[c2]
            if x != "?" and y != "?":
                entry = {"quarter":qi, "digit":digit,
                         "class_a":c1, "class_b":c2,
                         "mark_a":x, "mark_b":y}
                comparable.append(entry)
                if x != y:
                    conflicts.append(entry)
    return {
        "classification": "literal receiver negative tests only",
        "known_h108_residues":len(obs),
        "middle_fields_known_of_36":sum(x != "?" for x in raw["quarter_serial"]),
        "suffix_nine_fields_known_of_36":sum(x != "?" for x in raw["suffix_quarter_serial"]),
        "native_class_order":PHYSICAL,
        "native_url_digits":URL_DIGITS,
        "xbox_long_rows":36,
        "xbox_unique_long_rows":len(printer),
        "xbox_fixed_readouts":tests,
        "equal_digit_same_symbol_test": {
            "comparable_repeated_digit_pairs":len(comparable),
            "observed_conflicts":conflicts,
            "literal_equal_digit_lookup_falsified":bool(conflicts)
        },
        "open": "source-specified layered transforms and repeated-address operators"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", type=Path, default=ROOT/"data/observations.csv")
    parser.add_argument("--xbox", type=Path, default=ROOT/"data/printer-reference/xbox-one-raw.txt")
    args = parser.parse_args()
    print(json.dumps(run(args.observations, args.xbox), indent=2))

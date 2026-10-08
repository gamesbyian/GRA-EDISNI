#!/usr/bin/env python3
"""Experiment 433: cube-to-cube symbol transfer under residue/cube holdouts.

FROZEN OPERATION MENU: identity; reverse/rotate depth; 180deg XY rotation;
XY horizontal reflection; XY cyclic-column control. Q4 is excluded from
direct transfer because it uses the different slash/dot alphabet.

Do not train a transformation on the target quarter's marks. Independent
cross-cube correlation does not imply cellwise predictive usefulness.
"""
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHI"
LAYOUT = ("IAB", "CDE", "FGH")
COORDS = {LETTERS.index(LAYOUT[x][y]): (x, y)
          for x in range(3) for y in range(3)}
FROM_COORD = {(x, y): LETTERS.index(LAYOUT[x][y])
              for x in range(3) for y in range(3)}
COLS = [[LETTERS.index(LAYOUT[row][col]) for row in range(3)]
        for col in range(3)]


def load_observations():
    observed = {}
    n = 0
    with (ROOT / "data" / "observations.csv").open(newline="", encoding="utf8") as stream:
        for row in csv.DictReader(stream):
            n += 1
            r = int(row["residue"])
            mark = row["symbol"]
            assert r in range(1, 109) and mark in ("/", "-", ".")
            assert r not in observed or observed[r] == mark
            observed[r] = mark
    assert n == 84 and len(observed) == 66, "Update for new observations."
    return observed


def transformed(d, j, mode):
    x, y = COORDS[j]
    if mode == "identity":
        return d, j
    if mode == "reverse_depth":
        return 2 - d, j
    if mode == "cyclic_depth_plus1":
        return (d + 1) % 3, j
    if mode == "rotate180_xy":
        return d, FROM_COORD[2-x, 2-y]
    if mode == "reflect_horizontal_xy":
        return d, FROM_COORD[x, 2-y]
    if mode == "shift_column_xy":
        return d, FROM_COORD[x, (y+1) % 3]
    raise ValueError(mode)


MODES = ("identity", "reverse_depth", "cyclic_depth_plus1",
         "rotate180_xy", "reflect_horizontal_xy", "shift_column_xy")


def address(r):
    q, remainder = divmod(r-1, 27)
    d, j = divmod(remainder, 9)
    return q, d, j


def peer_prediction(obs, r, mode, allowed_quarters=(0, 1, 2)):
    q, d, j = address(r)
    assert q in range(3)
    d2, j2 = transformed(d, j, mode)
    peers = [obs.get(1 + 27 * k + 9 * d2 + j2)
             for k in allowed_quarters if k != q]
    peers = [v for v in peers if v is not None]
    return peers[0] if peers and len(set(peers)) == 1 else None


def training_majority(obs, omit_r=None, omit_q=None):
    data = [v for r, v in obs.items()
            if r <= 81 and r != omit_r
            and (omit_q is None or address(r)[0] != omit_q)]
    assert data
    return "/" if data.count("/") >= data.count("-") else "-"


def leave_one_residue_out(obs):
    results = {}
    for mode in MODES:
        covered = correct = baseline = two_peer_conflicts = 0
        for r, real in obs.items():
            if r > 81:
                continue
            training = {k: v for k, v in obs.items() if k != r}
            guess = peer_prediction(training, r, mode)
            if guess is None:
                continue
            covered += 1
            correct += guess == real
            baseline += training_majority(training) == real
        results[mode] = {"covered": covered, "correct": correct,
                         "baseline_on_same_targets": baseline}
    assert results["identity"] == {
        "covered": 33, "correct": 22, "baseline_on_same_targets": 23
    }
    return results


def train_pair_agreement(obs, source_quarters, mode):
    q0, q1 = source_quarters
    known = matched = 0
    for d in range(3):
        for j in range(9):
            d2, j2 = transformed(d, j, mode)
            x = obs.get(1 + 27*q0 + 9*d + j)
            y = obs.get(1 + 27*q1 + 9*d2 + j2)
            if x is not None and y is not None:
                known += 1
                matched += x == y
    return known, matched


def leave_one_cube_out(obs):
    folds = []
    for heldout in range(3):
        sources = tuple(q for q in range(3) if q != heldout)
        training_scores = []
        for mode in MODES:
            n, matched = train_pair_agreement(obs, sources, mode)
            # Fixed Laplace smoothing before comparing different sample sizes.
            training_scores.append({"mode": mode, "pairs": n, "matches": matched,
                                    "score": (matched + 1) / (n + 2)})
        # Tie breaks follow the frozen MODES order.
        winner = max(training_scores, key=lambda entry: entry["score"])
        guess_count = right = baseline = 0
        for r, real in obs.items():
            if r > 81 or address(r)[0] != heldout:
                continue
            prediction = peer_prediction(obs, r, winner["mode"], sources)
            if prediction is None:
                continue
            guess_count += 1
            right += prediction == real
            baseline += training_majority(obs, omit_q=heldout) == real
        folds.append({"heldout_quarter": heldout+1,
                      "selected_operation": winner["mode"],
                      "training": training_scores,
                      "covered": guess_count, "correct": right,
                      "baseline_on_same_targets": baseline})
    assert [(f["selected_operation"], f["covered"], f["correct"],
             f["baseline_on_same_targets"]) for f in folds] == [
        ("rotate180_xy", 10, 5, 4),
        ("identity", 12, 8, 10),
        ("identity", 10, 6, 7)
    ]
    return folds


def column_frame_options(obs, frame):
    options = []
    for minority in ("/", "-"):
        majority = "-" if minority == "/" else "/"
        for row_choices in itertools.product(range(3), repeat=3):
            symbols = [majority] * 9
            for col, row in enumerate(row_choices):
                symbols[COLS[col][row]] = minority
            if all(obs.get(1+9*frame+j, symbols[j]) == symbols[j]
                   for j in range(9)):
                options.append(symbols)
    assert options
    return options


def prospective_disagreements(obs):
    options = [column_frame_options(obs, f) for f in range(9)]
    table = []
    for residue in range(1, 82):
        if residue in obs:
            continue
        peer = peer_prediction(obs, residue, "identity")
        frame, cell = divmod(residue-1, 9)
        allowed = sorted(set(candidate[cell] for candidate in options[frame]))
        if peer is None:
            continue
        record = {
            "residue": residue,
            "letter": LETTERS[(residue-1) % 9],
            "copy_prediction": peer,
            "column_grammar_symbols": "".join(allowed),
            "column_grammar_forced": len(allowed) == 1,
            "physical_serials_up_to_600": list(range(residue,601,108))
        }
        table.append(record)
    disagreements = [
        row for row in table
        if row["column_grammar_forced"] and
           row["column_grammar_symbols"] != row["copy_prediction"]
    ]
    assert [x["residue"] for x in disagreements] == [11,33,41,64,68,77]
    assert len(table) == 19 and len(disagreements) == 6
    return table, disagreements


def exact_cube_letter_copy_null(obs):
    # Complete exact enumeration of shuffles within the observed positions
    # sharing both a 27-residue quarter and the A-I class.
    groups = []
    data = ["?"] * 109
    for r,v in obs.items():
        data[r] = v
    for q in range(4):
        for j in range(9):
            sites = [1+27*q+9*d+j for d in range(3)
                     if 1+27*q+9*d+j in obs]
            symbols = tuple(obs[r] for r in sites)
            if len(set(symbols)) > 1:
                choices = sorted(set(itertools.permutations(symbols)))
                groups.append((sites, choices))

    targets = []
    for r in obs:
        if r <= 81:
            q, d, j = address(r)
            peers = [1+27*k+9*d+j for k in range(3)
                     if k != q and (1+27*k+9*d+j) in obs]
            targets.append((r, peers))

    def score():
        covered = correct = baseline = 0
        for r, peers in targets:
            if not peers:
                continue
            values = [data[p] for p in peers]
            if len(set(values)) != 1:
                continue
            covered += 1
            correct += data[r] == values[0]
            # The observed primary slash majority remains "/" under
            # these cube-and-letter symbol-count-preserving shuffles.
            baseline += data[r] == "/"
        return covered, correct, correct-baseline

    actual = score()
    total = ge_accuracy = ge_delta = ge_right = 0
    equal_coverage = ge_right_equal_coverage = 0
    coverage_hist = Counter()
    correct_sum = coverage_sum = delta_sum = 0

    def visit(i):
        nonlocal total,ge_accuracy,ge_delta,ge_right,equal_coverage
        nonlocal ge_right_equal_coverage,correct_sum,coverage_sum,delta_sum
        if i == len(groups):
            n, right, delta = score()
            total += 1
            coverage_hist[n] += 1
            correct_sum += right
            coverage_sum += n
            delta_sum += delta
            ge_accuracy += right * actual[0] >= actual[1] * n
            ge_delta += delta >= actual[2]
            ge_right += right >= actual[1]
            if n == actual[0]:
                equal_coverage += 1
                ge_right_equal_coverage += right >= actual[1]
            return
        sites, choices = groups[i]
        for labels in choices:
            for r,v in zip(sites, labels):
                data[r] = v
            visit(i+1)

    visit(0)
    assert actual == (33, 22, -1)
    assert len(groups) == 16 and total == 331776
    assert ge_accuracy == 34560 and ge_delta == 129024
    assert equal_coverage == 76800 and ge_right_equal_coverage == 18816
    return {
        "total_shuffles": total,
        "observed_covered_correct_copy_minus_majority": actual,
        "null_mean_covered": coverage_sum/total,
        "null_mean_correct": correct_sum/total,
        "null_mean_copy_minus_majority": delta_sum/total,
        "null_fraction_accuracy_at_least_observed": ge_accuracy/total,
        "null_fraction_advantage_at_least_observed": ge_delta/total,
        "null_fraction_right_count_at_least_observed": ge_right/total,
        "matched_coverage_null_shuffles": equal_coverage,
        "matched_coverage_fraction_right_count_at_least_observed":
            ge_right_equal_coverage/equal_coverage,
        "null_coverage_distribution": dict(sorted(coverage_hist.items()))
    }


def main():
    obs = load_observations()
    one = leave_one_residue_out(obs)
    folds = leave_one_cube_out(obs)
    forecast, conflicts = prospective_disagreements(obs)
    null = exact_cube_letter_copy_null(obs)
    print(json.dumps({
        "source_records": 84,
        "unique_residues": len(obs),
        "primary_known_residues": sum(r <= 81 for r in obs),
        "single_residue_holdout": one,
        "whole_cube_operation_selection_holdout": folds,
        "identity_forecasts_missing_primary": forecast,
        "identity_vs_column_grammar_frozen_disagreements": conflicts,
        "strict_copy_control": null,
        "interpretation": (
            "No proposed cross-cube copy/reversal/rotation operation "
            "beats a simple primary-symbol majority reliably; use the six "
            "disagreement residues only as conditional future discriminators."
        ),
        "limits": [
            "Operations were chosen after the general idea had been discussed.",
            "Whole-quarter selection excludes all target quarter marks.",
            "These are cross-theory discriminators, not probability estimates.",
            "Physical-column one-hot predictions remain a model assumption.",
            "No automatic semantic interpretation or image recognition."
        ]
    }, indent=2))


if __name__ == "__main__":
    main()

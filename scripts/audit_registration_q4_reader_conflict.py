#!/usr/bin/env python3
"""Experiment 463: compare registration scoring to frozen Cube 4 axes.

Standard-library only. Imports previously established observation-only
complete-master enumeration, precise Discord pair definitions and the
native-depth vs globally relabelled quarter-axis consumer rules.
"""
import json
from math import exp

from enumerate_sticker_completion_ensembles import observations
from audit_q4_axis_consumer_comparison import (
    candidate_masters, valid_axis, PERMS, IDENTITY,
)
from audit_cube_lab_completion_ensemble import edges


def score(master, aligned, displaced):
    same = sum(master[i] == master[j] for i, j in aligned)
    shifted = sum(master[i] == master[j] for i, j in displaced)
    return same / len(aligned) - shifted / len(displaced)


def main():
    records, observed = observations()
    assert records == 84 and len(observed) == 66
    same = edges("ABCDEFGHI", "exact")
    shifted = edges("ABCDEFGHI", "x")
    all_rows = []
    for master, selector in candidate_masters(observed):
        value = score(master, same, shifted)
        native = valid_axis(master, selector, "depth", IDENTITY)
        relabelled = any(valid_axis(master, selector, "quarter", p)
                         for p in PERMS)
        all_rows.append((master, value, native, relabelled))

    assert len(all_rows) == 324
    assert sum(x[2] for x in all_rows) == 12
    assert sum(x[3] for x in all_rows) == 10
    assert not any(x[2] and x[3] for x in all_rows)

    weight = [exp(25 * row[1]) for row in all_rows]
    denominator = sum(weight)
    families = {}
    for name, selected in (
        ("all", lambda row: True),
        ("native_depth", lambda row: row[2]),
        ("globally_relabelled_quarter", lambda row: row[3]),
    ):
        group = [(row, w) for row, w in zip(all_rows, weight)
                 if selected(row)]
        families[name] = {
            "masters": len(group),
            "mean_alphabetical_x_contrast":
                sum(row[1] for row, _ in group) / len(group),
            "fraction_of_registration_weight":
                sum(w for _, w in group) / denominator,
        }

    uncertain = {}
    for residue in (50, 54, 93):
        counts = {
            mark: sum(w for row, w in zip(all_rows, weight)
                      if row[0][residue-1] == mark) / denominator
            for mark in ("/", "-", ".")
        }
        uncertain[residue] = {
            mark: value for mark, value in counts.items() if value > 0
        }
    assert 0.74 < uncertain[50]["/"] < 0.75
    assert 0.74 < uncertain[54]["/"] < 0.75
    assert 0.37 < uncertain[93]["/"] < 0.39

    print(json.dumps({
        "physical_records": records,
        "unique_residues": len(observed),
        "alpha_x_registration_beta": 25,
        "families": families,
        "unobserved_symbol_weights": uncertain,
        "warning": (
            "Retrospectively chosen softmax weights over candidate "
            "completions are not calibrated probabilities or independent "
            "evidence of a Cube 4 instruction mechanism."
        )
    }, indent=2))


if __name__ == "__main__":
    main()

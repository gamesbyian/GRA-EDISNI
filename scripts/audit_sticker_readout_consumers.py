#!/usr/bin/env python3
"""Experiment 430: bounded external-consumer readout of exact sticker ensembles.

Compare the typed tail-depth selection against three fixed-layer controls.
The historically suggested lever mapping /->U, -->R is only a relabeling;
there is no independent known 27-step lever target or extracted plaintext.
"""
from collections import Counter
from itertools import product
import json

from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, q4_choices,
    primary_columns, simple_row_exception, make_master, selected_columns,
)

LEVER = str.maketrans({"/": "U", "-": "R", ".": "L"})


def primary_readout(master, depths):
    return "".join(master[27*q + 9*depths[j] + j]
                   for q in range(3) for j in range(9))


def summarize(masters):
    result = {}
    for operation in ("selector", "0", "1", "2"):
        signatures = [
            primary_readout(master, depths if operation == "selector"
                            else (int(operation),) * 9)
            for master, depths in masters
        ]
        assert all(len(s) == 27 and set(s) <= {"/", "-"}
                   for s in signatures)
        fixed = "".join(
            next(iter(symbols)) if len(symbols := set(s[i] for s in signatures)) == 1
            else "?"
            for i in range(27)
        )
        distinct = sorted(set(signatures))
        result[operation] = {
            "unique_readouts": len(distinct),
            "invariant_positions": 27 - fixed.count("?"),
            "fixed_mask": fixed,
            "example_readout": distinct[0],
            "example_lever_commands": distinct[0].translate(LEVER),
            "dash_census": dict(sorted(Counter(s.count("-") for s in signatures).items())),
        }
    return result


def main():
    records, observed = observations()
    assert records == 84 and len(observed) == 66
    frames = [primary_frame_choices(observed, q) for q in range(9)]
    tail_codes = tuple(product(*q4_choices(observed)))
    families = {"column": [], "column_selected": [], "column_row_selected": []}
    for fs in product(*frames):
        if not all(primary_columns(f) for f in fs):
            continue
        for depths in tail_codes:
            master = make_master(fs, depths)
            families["column"].append((master, depths))
            if selected_columns(master, depths):
                families["column_selected"].append((master, depths))
                if simple_row_exception(master, depths):
                    families["column_row_selected"].append((master, depths))
    assert [len(families[k]) for k in families] == [324, 12, 6]
    summary = {name: summarize(masters) for name, masters in families.items()}
    assert summary["column"]["selector"]["unique_readouts"] == 68
    assert summary["column_selected"]["selector"]["unique_readouts"] == 3
    assert summary["column_row_selected"]["selector"]["unique_readouts"] == 3
    assert summary["column"]["1"]["unique_readouts"] == 1
    assert summary["column_selected"]["selector"]["invariant_positions"] == 21
    assert summary["column"]["1"]["invariant_positions"] == 27
    print(json.dumps({
        "physical_records": records,
        "unique_residues": len(observed),
        "families": summary,
        "interpretation": (
            "The Q4-selected reading is less completion-invariant than the "
            "fixed middle depth. Translating slash/dash to Up/Right does not "
            "supply a 27-command lever consumer or validate any readout."
        ),
        "limitations": [
            "Completeness, invariant masks and distinct outputs are conditional on each grammar.",
            "The selected one-dash-per-column grammar itself forces three dashes per selected surface.",
            "A fixed-depth control is not a proposed solved decoder.",
            "No readout may be declared meaningful without an independently cued consumer."
        ]
    }, indent=2))


if __name__ == "__main__":
    main()

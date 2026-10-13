#!/usr/bin/env python3
"""Optional OR-Tools CP-SAT versus independent exact U2 enumeration.

Raw physical observations plus named 3/6 one-minority-per-column and one-slash
tail grammars ONLY. No machine predictions, plaintext, or semantic fitting.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import time

try:
    from ortools.sat.python import cp_model
except ImportError as exc:
    raise SystemExit("Install optional solver: python -m pip install ortools==9.15.6755") from exc

from enumerate_sticker_completion_ensembles import (
    COLS, observations, primary_frame_choices, primary_columns,
    q4_choices, make_master,
)


class AllMasters(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        super().__init__()
        self.variables = variables
        self.masters = set()

    def on_solution_callback(self):
        encoded = "".join("/" if self.value(v) else ("-" if i < 81 else ".")
                          for i, v in enumerate(self.variables))
        if encoded in self.masters:
            raise AssertionError("Duplicate full assignment")
        self.masters.add(encoded)
        if len(self.masters) > 5000:
            self.stop_search()
            raise AssertionError("Unexpectedly wide search: re-audit family")


def cpsat_ensemble(observed):
    model = cp_model.CpModel()
    symbols = [model.new_bool_var("slash_%d" % (i + 1)) for i in range(108)]
    for r, mark in observed.items():
        assert mark in (("/", "-") if r <= 81 else ("/", "."))
        model.add(symbols[r - 1] == int(mark == "/"))
    for frame in range(9):
        group = symbols[9*frame:9*(frame+1)]
        slash_is_minority = model.new_bool_var("slash_minority_%d" % frame)
        model.add(sum(group) == 3).only_enforce_if(slash_is_minority)
        model.add(sum(group) == 6).only_enforce_if(slash_is_minority.Not())
        for physical_col in COLS:
            col = sum(group[pos] for pos in physical_col)
            model.add(col == 1).only_enforce_if(slash_is_minority)
            model.add(col == 2).only_enforce_if(slash_is_minority.Not())
    for class_j in range(9):
        model.add_exactly_one([symbols[81+9*depth+class_j] for depth in range(3)])
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = 30
    collector = AllMasters(symbols)
    status = solver.solve(model, collector)
    assert status == cp_model.OPTIMAL, ("Incomplete enumeration", solver.status_name(status))
    return collector.masters


def library_free_ensemble(observed):
    frames = [[f for f in primary_frame_choices(observed, i) if primary_columns(f)]
              for i in range(9)]
    choices = q4_choices(observed)
    return {
        "".join(make_master(group, depths))
        for group in itertools.product(*frames)
        for depths in itertools.product(*choices)
    }


def run():
    records, observed = observations()
    assert (records, len(observed)) == (84, 66)
    start = time.perf_counter()
    baseline = library_free_ensemble(observed)
    baseline_seconds = time.perf_counter() - start
    start = time.perf_counter()
    competing = cpsat_ensemble(observed)
    solver_seconds = time.perf_counter() - start
    assert baseline == competing, (len(baseline - competing), len(competing - baseline))
    assert len(baseline) == 324, len(baseline)
    digest = hashlib.sha256(("\n".join(sorted(baseline)) + "\n").encode()).hexdigest()
    return {
        "mode": "DISCOVER/DEVELOP: conditional U2, not proof of intended encoding",
        "physical_records": records,
        "observed_residues": len(observed),
        "u2_surviving_complete_masters": len(baseline),
        "exact_candidate_sets_identical": True,
        "canonical_master_set_sha256": digest,
        "wall_seconds_not_portable": {
            "stdlib_exact": round(baseline_seconds, 6),
            "ortools_cpsat": round(solver_seconds, 6),
        },
        "warning": "Matching conditional candidates is a consistency check, not independent physical evidence."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

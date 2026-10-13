#!/usr/bin/env python3
"""Optional Z3 cross-check of the observation-only three-position tail codes.

DISCOVER/DEVELOP research tooling, NOT a CE foreground decoder. Requires
z3-solver; reads ONLY the canonical raw-observation file via the established
observation-only loader. Never imports the incumbent machine or predictions.

Purpose beyond existing exact enumeration: produce an SMT satisfiability
witness, a per-residue backbone, and a minimal conflicting subset of raw
observations for a rejected polarity.
"""
from __future__ import annotations

import json
from math import prod

try:
    import z3
except ImportError as exc:
    raise SystemExit(
        "Z3 pilot is optional. Install: python -m pip install z3-solver==4.16.0.0"
    ) from exc

from audit_tail_metadata import CLASSES, compatible_positions, load_symbols

POSITIONS = tuple(range(82, 109))
COMPLETION_CAP = 10_000


def tail_for_class(j: int) -> tuple[int, int, int]:
    """A-I serial-class trace, independent of any assumed 3x3 machine."""
    return tuple(82 + 9 * depth + j for depth in range(3))


def make_solver(observed: dict[int, str], slash_per_class: int):
    if slash_per_class not in (1, 2):
        raise ValueError("The current pilot supports one slash or one dot")
    solver = z3.Solver()
    solver.set("random_seed", 0)
    cells = {r: z3.Bool(f"slash_{r}") for r in POSITIONS}
    for j in range(9):
        group = tail_for_class(j)
        solver.add(z3.PbEq([(cells[r], 1) for r in group], slash_per_class))

    assumptions = {}
    for r in POSITIONS:
        if r not in observed:
            continue
        mark = observed[r]
        if mark not in ("/", "."):
            raise ValueError(f"Unexpected tail symbol at {r}: {mark!r}")
        a = z3.Bool(f"raw_residue_{r}")
        solver.add(z3.Implies(a, cells[r] if mark == "/" else z3.Not(cells[r])))
        assumptions[r] = a
    return solver, cells, assumptions


def count_completions(solver, cells, assumptions):
    """Enumerate only for a *small* finite family; fail if capped/unknown."""
    active = list(assumptions.values())
    rows = []
    while True:
        state = solver.check(*active)
        if state == z3.unsat:
            return rows
        if state != z3.sat:
            raise RuntimeError(f"Z3 returned {state}")
        if len(rows) >= COMPLETION_CAP:
            raise RuntimeError("Completion cap exceeded: keep this family symbolic")
        model = solver.model()
        values = tuple(z3.is_true(model.eval(cells[r], model_completion=True))
                       for r in POSITIONS)
        rows.append(values)
        solver.add(z3.Or(
            *[cells[r] != z3.BoolVal(value)
              for r, value in zip(POSITIONS, values)]
        ))


def minimal_conflict(solver, assumptions):
    """Deletion-minimize the assumption core; minimal, not minimum cardinality."""
    active = list(assumptions)
    assert solver.check(*(assumptions[r] for r in active)) == z3.unsat
    core_names = {str(a) for a in solver.unsat_core()}
    active = [r for r in active if str(assumptions[r]) in core_names]
    for r in list(active):
        candidate = [s for s in active if s != r]
        if solver.check(*(assumptions[s] for s in candidate)) == z3.unsat:
            active = candidate
    assert solver.check(*(assumptions[s] for s in active)) == z3.unsat
    for r in active:
        assert solver.check(*(assumptions[s] for s in active if s != r)) == z3.sat
    return active


def analyze(observed: dict[int, str]) -> dict:
    slash_solver, cells, assumptions = make_solver(observed, 1)
    slash_completions = count_completions(slash_solver, cells, assumptions)
    assert slash_completions, "one-slash model became inconsistent"

    # Independent, older standard-library enumerator as a cross-check.
    allowed = {}
    for j, cls in enumerate(CLASSES):
        tail = "".join(observed.get(r, "?") for r in tail_for_class(j))
        allowed[cls] = compatible_positions(tail, "/")
    assert len(slash_completions) == prod(len(v) for v in allowed.values()), (
        "SMT and existing observation-only enumerator disagree"
    )

    possible = {
        str(r): sorted({"/" if row[i] else "." for row in slash_completions})
        for i, r in enumerate(POSITIONS)
    }
    backbone = {r: marks[0] for r, marks in possible.items() if len(marks) == 1}
    undetermined = [int(r) for r, marks in possible.items() if len(marks) > 1]

    dot_solver, dot_cells, dot_assumptions = make_solver(observed, 2)
    assert dot_solver.check(*dot_assumptions.values()) == z3.unsat
    conflict = minimal_conflict(dot_solver, dot_assumptions)
    assert all(observed[r] in ("/", ".") for r in conflict)

    # The strict controls come from the already documented Experiment 317,
    # not from a claim that this pilot has discovered a new cipher.
    assert len(slash_completions) == 36, len(slash_completions)
    assert {cls: values[0] for cls, values in allowed.items() if len(values) == 1} == {
        "B": 2, "E": 0, "F": 1, "H": 2, "I": 2
    }

    return {
        "mode": "DISCOVER/DEVELOP (conditional structural hypothesis)",
        "input": "data/observations.csv (physical observations only)",
        "engine": "z3-solver",
        "one_slash_per_class": {
            "status": "satisfiable; NOT evidence of intended encoding",
            "completions": len(slash_completions),
            "positions_by_class": allowed,
            "forced_tail_residues": backbone,
            "undetermined_tail_residues": undetermined,
            "possible_symbols": possible,
        },
        "one_dot_per_class": {
            "status": "unsatisfiable with observed physical marks",
            "minimal_conflicting_observations": [
                {"residue": r, "symbol": observed[r]} for r in conflict
            ],
            "note": "Deletion-minimal contradiction, not guaranteed smallest proof",
        },
        "scope": "No POS3, semantic scoring, guessed stickers, or Steam input claims",
    }


def main():
    print(json.dumps(analyze(load_symbols()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

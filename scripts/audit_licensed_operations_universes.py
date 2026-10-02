#!/usr/bin/env python3
"""Experiment 367: replay only currently licensed historical operations across U2-U5.

This is deliberately not a transform sweep. The operation set is frozen by
Experiment 338's R3 evidence gate and existing completed experiments:

* historical 3x3 mosaic: deterministic representation only, no candidate filter;
* frozen tail-selected row / one-exception rule from Experiment 329;
* column/rail sibling from Experiment 329 (already contradicted);
* historically motivated lever mapping with the known normal bunker password
  from Experiments 342-343 (hard negative under the 81/27 alphabet boundary).

Pending/closed R3 families are not executed.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from generate_master import legal_states, generate_master as generate_state_master, format_state

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-367-licensed-operations-universe.json"
SERIAL = "ABCDEFGHI"
NORMAL_CODE = "UURLRRRUUURLLL"
SYMBOL_TO_LEVER = {"/": "U", "-": "R", ".": "L"}


def selector_depth(master: str, class_index: int) -> int:
    hits = [
        depth
        for depth in range(3)
        if master[(82 + 9 * depth + class_index) - 1] == "/"
    ]
    assert len(hits) == 1
    return hits[0]


def one_exception(line: str) -> bool:
    slash = line.count("/")
    return slash in (1, 2)


def selected_row(master: str, class_index: int, depth: int) -> str:
    return "".join(
        master[(1 + class_index + 9 * (3 * depth + k)) - 1]
        for k in range(3)
    )


def selected_column(master: str, class_index: int, depth: int) -> str:
    return "".join(
        master[(1 + class_index + 9 * k) - 1]
        for k in (depth, depth + 3, depth + 6)
    )


def row_selector_ok(master: str) -> bool:
    return all(
        one_exception(selected_row(master, j, selector_depth(master, j)))
        for j in range(9)
    )


def column_selector_ok(master: str) -> bool:
    return all(
        one_exception(selected_column(master, j, selector_depth(master, j)))
        for j in range(9)
    )


def cyclic_windows(tape: str, width: int):
    doubled = tape + tape[: width - 1]
    for start in range(len(tape)):
        yield start + 1, doubled[start : start + width]


def rotations(word: str):
    for k in range(len(word)):
        yield word[k:] + word[:k]


def lever_known_password_hit(master: str) -> bool:
    tape = "".join(SYMBOL_TO_LEVER[ch] for ch in master)
    targets = set(rotations(NORMAL_CODE)) | set(rotations(NORMAL_CODE[::-1]))
    return any(window in targets for _start, window in cyclic_windows(tape, len(NORMAL_CODE)))


def invariant_map(masters: list[str], unknown: tuple[int, ...]) -> dict[int, str]:
    out = {}
    for residue in unknown:
        values = {master[residue - 1] for master in masters}
        if len(values) == 1:
            out[residue] = next(iter(values))
    return out


def minimum_discriminator(masters: list[str], unknown: tuple[int, ...]):
    variable = [
        residue
        for residue in unknown
        if len({master[residue - 1] for master in masters}) > 1
    ]
    lower = math.ceil(math.log2(len(masters)))
    for k in range(lower, len(variable) + 1):
        examples = []
        count = 0
        for residues in itertools.combinations(variable, k):
            signatures = {
                tuple(master[r - 1] for r in residues)
                for master in masters
            }
            if len(signatures) == len(masters):
                count += 1
                if len(examples) < 12:
                    examples.append(list(residues))
        if count:
            return {
                "information_lower_bound": lower,
                "minimum_size": k,
                "number_of_minimum_sets": count,
                "examples": examples,
            }
    raise AssertionError("no discriminator found")


def main():
    _u2_summary, u2_rows, unknown = build()
    u2 = [master for *_prefix, master in u2_rows]
    u3, u4, u5 = machine_layers()
    layers = {"U2": u2, "U3": u3, "U4": u4, "U5": u5}

    state_by_master = {
        generate_state_master(state): format_state(state)
        for state in legal_states()
    }
    assert set(u5) == set(state_by_master)

    result = {
        "experiment": 367,
        "gate_source": "Experiment 338 / data/reset-r3-operation-gates.json",
        "operations": {
            "historical_mosaic": {
                "status": "licensed representation, not a candidate selector",
                "definition": "reshape each 9-sticker sequence row as IAB/CDE/FGH and tile twelve 3x3 frames",
                "layer_counts": {},
            },
            "frozen_tail_selected_row_one_exception": {
                "status": "licensed simple tail-as-operation family; exploratory/frozen since Experiment 329",
                "layer_counts": {},
            },
            "tail_selected_column_one_exception": {
                "status": "frozen sibling negative from Experiment 329",
                "layer_counts": {},
            },
            "known_bunker_password_lever_replay": {
                "status": "historically motivated consumer; direct known-password replay closed by Experiment 343",
                "mapping": SYMBOL_TO_LEVER,
                "target": NORMAL_CODE,
                "tested": "all cyclic starts, target rotations, reverse target rotations",
                "layer_counts": {},
            },
        },
        "not_run_by_design": {
            "pending_specific_evidence": [
                "boundary_constrained_permutation",
                "prior_stage_output_as_selector",
                "cross_artifact_consumer",
            ],
            "closed_until_cue": [
                "exact_value_or_class_filter",
                "externally_cued_generative_transform",
                "in_world_reference_overlay",
                "carrier_conversion",
            ],
        },
    }

    for name, masters in layers.items():
        row_survivors = [master for master in masters if row_selector_ok(master)]
        col_survivors = [master for master in masters if column_selector_ok(master)]
        lever_survivors = [master for master in masters if lever_known_password_hit(master)]

        base_fixed = invariant_map(masters, unknown)
        row_fixed = invariant_map(row_survivors, unknown)
        newly_fixed = {
            str(r): value
            for r, value in row_fixed.items()
            if r not in base_fixed
        }

        result["operations"]["historical_mosaic"]["layer_counts"][name] = {
            "applicable": len(masters),
            "survivors": len(masters),
            "note": "deterministic representation supplies no independent pass/fail criterion",
        }
        result["operations"]["frozen_tail_selected_row_one_exception"]["layer_counts"][name] = {
            "total": len(masters),
            "survivors": len(row_survivors),
            "survival_fraction": len(row_survivors) / len(masters),
            "newly_fixed_residues": newly_fixed,
            "minimum_discriminator_within_survivors": minimum_discriminator(row_survivors, unknown),
        }
        result["operations"]["tail_selected_column_one_exception"]["layer_counts"][name] = {
            "total": len(masters),
            "survivors": len(col_survivors),
        }
        result["operations"]["known_bunker_password_lever_replay"]["layer_counts"][name] = {
            "total": len(masters),
            "survivors": len(lever_survivors),
        }

    u5_row = [m for m in u5 if row_selector_ok(m)]
    result["operations"]["frozen_tail_selected_row_one_exception"]["u5_state_labels"] = sorted(
        state_by_master[m] for m in u5_row
    )

    expected_row = {"U2": 144, "U3": 48, "U4": 7, "U5": 6}
    for name, count in expected_row.items():
        assert result["operations"]["frozen_tail_selected_row_one_exception"]["layer_counts"][name]["survivors"] == count

    for name in layers:
        assert result["operations"]["tail_selected_column_one_exception"]["layer_counts"][name]["survivors"] == 0
        assert result["operations"]["known_bunker_password_lever_replay"]["layer_counts"][name]["survivors"] == 0

    assert result["operations"]["frozen_tail_selected_row_one_exception"]["u5_state_labels"] == [
        "0011", "0101", "1001", "1011", "1101", "1111"
    ]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

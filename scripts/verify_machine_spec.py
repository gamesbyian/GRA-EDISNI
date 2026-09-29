#!/usr/bin/env python3
"""Check data/machine-spec.json against the executable canonical generator.

This is a drift detector, not an independent implementation. It protects the
machine-readable handoff contract used by new agents and downstream tooling.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from generate_master import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    generate_master,
    legal_states,
    primary_payload_lattice,
    q4_selector_field,
)

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "data" / "machine-spec.json"


def physical_layout_from_positions() -> list[list[str]]:
    layout = [["" for _ in range(3)] for _ in range(3)]
    for letter, (row, col) in PHYSICAL_POSITION.items():
        layout[row][col] = letter
    assert all(all(cell for cell in row) for row in layout)
    return layout


def variable_residues(masters: list[str]) -> list[int]:
    return [
        residue
        for residue in range(1, 109)
        if len({master[residue - 1] for master in masters}) > 1
    ]


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    states = legal_states()
    masters = [generate_master(state) for state in states]

    assert spec["schema_version"] == 3
    assert spec["closed_corpus"] is True

    hidden = spec["hidden_state"]
    assert hidden["bits"] == ["X", "Y", "Z", "G"]
    assert hidden["physical_state_count"] == len(states) == 14

    legal_xyz = {(s.X, s.Y, s.Z) for s in states}
    all_xyz = {
        (x, y, z)
        for x in (0, 1)
        for y in (0, 1)
        for z in (0, 1)
    }
    forbidden_xyz = all_xyz - legal_xyz
    assert forbidden_xyz == {(0, 1, 1)}
    assert hidden["forbidden_functional_word"] == "011"

    carrier = spec["carrier"]
    assert carrier["foreground_period"] == 108
    assert carrier["background_period"] == 9
    assert carrier["primary_range"] == [1, 81]
    assert carrier["q4_range"] == [82, 108]
    assert carrier["serial_order"] == list(SERIAL_ORDER)
    assert carrier["physical_layout"] == physical_layout_from_positions()

    # The templated payload lattice in the JSON must instantiate exactly to the
    # canonical generator's payload for every legal state.
    template = spec["primary"]["payload_lattice"]
    for state in states:
        instantiated = [
            [
                cell.replace("x", str(state.x)).replace("y", str(state.y))
                for cell in row
            ]
            for row in template
        ]
        assert instantiated == primary_payload_lattice(state)

    # Derive the three Q4 control cores from the executable selector field and
    # compare them to the handoff spec.
    cores: dict[int, set[str]] = {0: set(), 1: set(), 2: set()}
    for state in states:
        field = q4_selector_field(state)
        A = field[0][1]
        D = field[1][1]
        G_control = field[2][1]
        cores[state.p].add(f"{A}{D}{G_control}")

    assert all(len(values) == 1 for values in cores.values())
    derived_cores = {
        f"p{p}": next(iter(values))
        for p, values in sorted(cores.items())
    }
    assert spec["q4"]["control_cores"] == derived_cores

    relation: dict[str, set[int]] = {}
    for state in states:
        key = f"{state.X}{state.Y}"
        relation.setdefault(key, set()).add(state.p)
    expected_relation = {
        key: set(values)
        for key, values in spec["grant_relation"]["table"].items()
    }
    assert relation == expected_relation

    variable = variable_residues(masters)
    anatomy = spec["master_anatomy"]["preferred_representative"]
    assert variable == spec["latent_register_residues"]
    assert anatomy["variable_residues"] == len(variable) == 13
    assert anatomy["invariant_residues"] == 108 - len(variable) == 95

    quotient = spec["master_anatomy"]["gauge_quotient"]
    exact = quotient["exact_transducer"]
    assert exact["physical_gauge_bits"] == 4
    assert exact["physical_gauge_settings"] == 16
    assert exact["hidden_states_per_setting"] == 14
    assert exact["distinct_complete_masters"] == 224
    assert exact["operation_gauge_bits"] == 1
    assert exact["total_gauge_bits"] == 5
    assert exact["total_representation_settings"] == 32

    broader = quotient["broader_recursive_family"]
    assert broader["viable_physical_settings"] == 24
    assert broader["distinct_complete_masters"] == 336
    assert broader["operation_gauge_settings"] == 2
    assert broader["total_representation_settings"] == 48
    assert broader["state_operation_representations"] == 672
    assert len(broader["union_variable_residues"]) == 21

    assert spec["primary"]["physical_completion_gauge"]["bits"] == 2
    assert spec["q4"]["polarity_gauge"]["bits"] == 3
    q4_gauge = spec["q4"]["polarity_gauge"]
    assert q4_gauge["shared_polarity_required_for_function"] is False
    assert q4_gauge["independent_polarity_route_masks"] == ["0", "A", "C", "A+C"]
    assert q4_gauge["independent_polarity_route_shell"] == ["120", "012", "102"]
    assert q4_gauge["functional_ablation_experiment"] == 292

    q4_inverse = spec["q4"]["abstract_selector_inverse"]
    assert q4_inverse["experiment"] == 294
    assert q4_inverse["raw_q4_observations_used"] is False
    assert q4_inverse["expected_terminal_used_as_filter"] is False
    assert q4_inverse["expected_core_location_used_as_filter"] is False
    assert q4_inverse["selector_maps"] == 3**9 == 19683
    assert q4_inverse["core_location_candidates"] == 84
    assert q4_inverse["first_pass_pos3_pairs"] == 288
    assert q4_inverse["second_pass_pos3_pairs"] == 208
    assert q4_inverse["terminal_distribution"] == {
        "100": 28,
        "102": 84,
        "110": 24,
        "112": 72,
    }
    assert q4_inverse["route_capable_core_locations"] == ["ADG"]
    assert q4_inverse["scaffold_coordinate_order"] == "BCEFHI"
    assert q4_inverse["route_capable_scaffolds"] == ["200122", "220122"]
    assert q4_inverse["states_per_scaffold"] == 7
    assert q4_inverse["recovered_core_words"] == ["110", "220", "212"]
    assert q4_inverse["recovered_terminal"] == "100"
    assert q4_inverse["recovered_route_shell"] == ["120", "012", "102"]
    assert q4_inverse["remaining_abstract_selector_gauge"] == "C=0 or 2"

    q4_code = spec["q4"]["physical_codebook_holdout"]
    assert q4_code["experiment"] == 295
    assert q4_code["depends_on_experiment"] == 294
    assert q4_code["recovered_fixed_selector"] == {
        "B": 2,
        "E": 0,
        "F": 1,
        "H": 2,
        "I": 2,
    }
    assert q4_code["fixed_scaffold_q4_observation_records"] == 9
    assert q4_code["fixed_scaffold_distinct_codebook_entries_observed"] == 6
    assert q4_code["fixed_scaffold_compatible_shared_codebooks"] == 8
    assert q4_code["full_q4_observation_records"] == 11
    assert q4_code["recovered_selector_fields_tested"] == 6
    assert q4_code["full_family_forced_codebook_entries"] == 7
    assert q4_code["full_family_compatible_shared_codebooks"] == 4
    assert q4_code["residual_physical_codebook_gauge_entries"] == [
        "E[0,2]",
        "E[1,2]",
    ]
    assert q4_code["pairwise_distinct_codeword_survivors"] == 4
    assert q4_code["all_nonuniform_codeword_survivors"] == 4
    assert q4_code["equal_row_weight_survivors"] == 1
    assert q4_code["cyclic_equivariant_survivors"] == 1
    assert q4_code["minimum_slash_survivors"] == 1
    assert q4_code["recovered_codewords_by_selector"] == ["/..", "./.", "../"]
    assert q4_code["recovered_rule"] == (
        "slash iff physical depth d equals selector value S"
    )

    assert spec["recursion_gauge"]["bits"] == 1

    expected_census = Counter({
        "/": anatomy["symbol_census"]["slash"],
        "-": anatomy["symbol_census"]["dash"],
        ".": anatomy["symbol_census"]["dot"],
    })
    assert expected_census == Counter({"/": 54, "-": 36, ".": 18})
    assert all(Counter(master) == expected_census for master in masters)

    assert spec["first_pass"]["hidden_rank"] == 3
    assert spec["terminal"]["hidden_rank"] == 1
    assert spec["terminal"]["frame"] == 9
    assert spec["terminal"]["payload"] == "100"
    assert spec["terminal"]["raw_serial_word"] == "---//////"

    print("OK(spec): machine-spec schema/version and closed-corpus status")
    print("OK(spec): 14-state legality and forbidden functional word")
    print("OK(spec): carrier geometry matches executable generator")
    print("OK(spec): primary payload template matches every legal state")
    print("OK(spec): Q4 control cores and request/grant table match runtime states")
    print("OK(spec): preferred latent register, 95/13 split, and 54/36/18 census match")
    print("OK(spec): corrected coupled gauge-family metadata is internally consistent")
    print("OK(spec): Experiment 292 shared-polarity ablation is recorded")
    print("OK(spec): Experiment 294 abstract-selector inverse is recorded")
    print("OK(spec): Experiment 295 physical-codebook holdout is recorded")
    print("OK(spec): terminal handoff fields remain canonical")


if __name__ == "__main__":
    main()

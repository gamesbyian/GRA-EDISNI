#!/usr/bin/env python3
"""Re-run CX-E to CX-E5 against the original 66-site observation snapshot.

This is a *historical reproducibility* check, not proof the conjectures
are correct. New physical observations may change live-model outcomes,
but must not change previously frozen benchmark results or predictions.
"""
import json
from pathlib import Path

from conjecture_lab_cx_e_rail_nulls import run as rail_nulls
from conjecture_lab_cx_e_rail_field_pilot import run as rail_fields
from conjecture_lab_cx_e3_native_receivers import run as native_receivers
from conjecture_lab_cx_e4_dual_nine_fields import run as dual_grid
from conjecture_lab_cx_e5_ghi_boolean import run as boolean_test

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"data/conjecture-lab-h108-66-residue-freeze-2026-10-09.csv"
XBOX=ROOT/"data/printer-reference/xbox-one-raw.txt"


def fixture(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf8"))


def run():
    r1=rail_nulls(FROZEN)
    assert r1["observed_unique_residues"]==66
    assert r1["fully_observed_columns_1_based"]==[5,9,15,17,20]
    assert r1["all_slash_columns_1_based"]==[5,15]
    assert abs(r1["quarter_shuffle_any_two"]-0.0293474512065495)<1e-12
    assert abs(r1["typed_grammar_any_two"]-0.0486894772376543)<1e-12

    r2=rail_fields(FROZEN)
    assert r2["total_row_rule_middle_field_completions"]==48
    assert r2["window_look_elsewhere"]["n_tested"]==19
    assert r2["window_look_elsewhere"]["n_all_four_quarters_survive"]==4
    expected2={6:"-",8:"-",11:"-",41:"-",64:"-",91:"/"}
    assert {x["residue"]:x["cx_e2_row_forecast"]
            for x in r2["frozen_conditional_forecasts"]}==expected2
    stored2=fixture("conjecture-lab-cx-e2-rail-predictions-2026-10-09.json")
    assert {x["residue"]:x["predicted_symbol"] for x in stored2["forecasts"]}==expected2

    r3=native_receivers(FROZEN,XBOX)
    assert r3["xbox_unique_long_rows"]==35
    assert r3["middle_fields_known_of_36"]==19
    assert r3["suffix_nine_fields_known_of_36"]==24
    mins={key:item["best_conflicts"]
          for key,item in r3["xbox_fixed_readouts"].items()}
    assert mins=={
        "quarter_serial":6,"quarter_physical":6,"class_major":9,
        "suffix_quarter_serial":10,"suffix_quarter_physical":11,
        "suffix_class_major":10}
    assert len(r3["equal_digit_same_symbol_test"]["observed_conflicts"])==2

    r4=dual_grid(FROZEN)
    assert [(len(x["row_minority_options"]),len(x["column_minority_options"]))
            for x in r4["quarter_suffix_fields"]]==[(1,0),(0,1),(1,1),(2,3)]
    edges=r4["adjacent_quarter_8D4_x_2role_edges"]
    assert [len(x["exact_zero_conflict_variants"]) for x in edges]==[2,0,0]
    assert edges[0]["best_overlap_among_exact"]==6
    counts=r4["fixed_mask_q1_q2_exact_null"]
    assert counts["conditional_sample_space"]==315
    assert counts["event_counts"]=={
        "any_zero":110,"any_zero_with_six_overlap":28,
        "row_col_unique":144,
        "row_col_unique_transpose_complement":8}
    expected4={16:"-",22:"/",45:"/",49:"-",50:"/"}
    assert {x["residue"]:x["conditional_predicted_symbol"]
            for x in r4["special_q1_q2_transform"]["frozen_conditional_forecasts"]}==expected4
    stored4=fixture("conjecture-lab-cx-e4-transport-predictions-2026-10-09.json")
    assert {x["residue"]:x["predicted_symbol"] for x in stored4["forecasts"]}==expected4

    r5=boolean_test(FROZEN)
    assert r5["all_16_survivor_ids"]==[6]
    assert r5["selected_truth_table_bits_00_01_10_11"]==[0,1,1,0]
    assert len(r5["all_classes_XOR_physical_contradictions"])==5
    assert r5["unique_XOR_subsets"]==["AHI","DHI","GHI"]
    assert len(r5["unique_boolean_subsets"])==19
    assert r5["all_84_three_class_subsets_survivor_count_distribution"]["0"]==44
    expected5={8:"/",27:"/",35:"-",61:"/",62:"/",99:"/",107:"."}
    assert {x["residue"]:x["conditional_xor_forecast"]
            for x in r5["selected_forecasts"]}==expected5
    stored5=fixture("conjecture-lab-cx-e5-ghi-xor-predictions-2026-10-09.json")
    assert {x["residue"]:x["predicted_symbol"] for x in stored5["forecasts"]}==expected5
    return {
        "historical_observed_residues":66,
        "slashed_rail_columns":[5,15],
        "literal_xbox_matching_readouts_falsified":6,
        "cx_e2_forecasts":len(expected2),
        "cx_e4_forecasts":len(expected4),
        "cx_e5_forecasts":len(expected5),
        "cx_e5_unique_selected_boolean_rule":"XOR",
        "all_status":"reproduced historic conditions; NO CE decode claimed"
    }


if __name__=="__main__":
    print(json.dumps(run(),indent=2))

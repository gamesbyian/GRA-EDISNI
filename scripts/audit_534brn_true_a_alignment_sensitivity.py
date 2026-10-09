#!/usr/bin/env python3
"""CL10: repeat historical 534brn five-path alignment stability with TRUE original A.

The earlier CL09 byte restoration increased heuristic fills to 245. This
experiment asks how many agree among five equally admissible selected edit
alignments (tie priority diagonal/up/left, unique anchor length 10/12/14).
This is NOT a proof of unique values across ALL cheapest alignment paths.

Run locally: python scripts/audit_534brn_true_a_alignment_sensitivity.py
May save --output-json to inspect changed positions.
"""
import argparse
import json
from pathlib import Path
import audit_534brn_alignment_sensitivity as sensitivity

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"data"/"534brn-true-a-adversarial-alignment-2026-10-08.json"

def calculate():
    # The legacy audit reads the A INPUTS descriptor from this imported
    # shared module, so change exactly the A source identity without
    # modifying its alignment algorithm, parameters or B/P.
    old=sensitivity.INPUTS["A"]
    sensitivity.INPUTS["A"]=(
        "A-original-capture.bin",
        "ce55c03ee972954f6e80f55a1a279bb85024f99b",
        12140,
    )
    try:
        out=sensitivity.audit()
    finally:
        sensitivity.INPUTS["A"]=old
    assert out["baseline_recovered"]==245
    assert len(out["stable_position_values_hex"])==out["stable_across_five"]
    assert out["stable_across_five"] <=245
    assert out["variable_baseline"]+out["stable_across_five"]==245
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-json")
    p.add_argument("--freeze",action="store_true",
                   help="during one-shot discovery bypass fixture check")
    args=p.parse_args()
    out=calculate()
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    if not args.freeze:
        f=json.loads(FROZEN.read_text(encoding="utf8"))
        assert f["source_original_a_git_sha1"]=="ce55c03ee972954f6e80f55a1a279bb85024f99b"
        for key in ("cases","baseline_recovered","stable_across_five",
                    "variable_baseline","changed_by_case",
                    "stable_position_values_hex"):
            assert out[key]==f[key],key
    short={k:out[k] for k in
           ("cases","baseline_recovered","stable_across_five",
            "variable_baseline","changed_by_case","stable_position_values_hex")}
    print("CL10_SOURCE_A_ADVERSARIAL="+json.dumps(short,separators=(",",":")))
    print("PASS: fixed alignment implementation replayed on byte-authentic original A")

if __name__=="__main__":
    main()

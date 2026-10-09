#!/usr/bin/env python3
"""CL12: offline source/provenance contract for externally published SAF workbench.

Verifies the only declared first-party source is already present byte-for-byte
in this repository, and guards against reclassifying model-reconstructed
11.78MB streams as independent 2019 source captures.
Not a reimplementation or validation of the external decompressor.
"""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data"/"conjecture-lab-saf-external-workbench-audit-2026-10-08.json"
SOURCE=ROOT/"archive"/"external"/"twinysam-inside-arg"/"terminal41.link"/"dat"/"saf_dat_col.html"
def main():
    d=json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert (d["schema_version"],d["id"])==(1,"CL-12")
    up=d["upstream"]
    raw=SOURCE.read_bytes()
    assert len(raw)==up["original_source_bytes"]==1986163
    assert hashlib.sha256(raw).hexdigest()==up["original_source_sha256"]
    h=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()
    assert h==up["original_source_sha1_git"]=="349b818fce618ef55c404bedfb602b1d03f29a48"
    assert up["original_source_is_exact_existing_GRA_copy"] is True
    c=d["implementation"]
    assert c["recorded_candidate_count"]==c["original_input_candidate_count"]+c["community_input_candidate_count"]==17
    assert (c["original_input_candidate_count"],c["community_input_candidate_count"])==(10,7)
    assert c["default_payload_bytes"]==11779416
    assert c["source_native_decoded_payload_proven"] is False
    assert d["historical_scope"]["independent_original_data_acquisition"] is False
    assert d["historical_scope"]["contains_saf_dat_col_BACKUP_html"] is False
    assert up["sha256_tests_are_self_consistency_not_original_ground_truth"] is True
    print("CL12 PASS: original SAF capture byte-identical; 17 speculative reconstructions are not original sources")
if __name__=="__main__":
    main()

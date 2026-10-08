#!/usr/bin/env python3
"""Self-contained verifier and optional binary image renderer for CL-05.

Fixture contains source-derived bitmap and complete 256-phase census.
Does NOT need to download original 20MB source; source re-acquisition and
exact pixel authentication live in conjecture_lab_gate98_phase_replay.py.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"data/conjecture-lab-gate98-native-phase-2026-10-08.json"
EXPECTED_SOURCE_SHA1="127d8772912ffc499e5afaffe321d5bab7e920df"
EXPECTED_PLANET_SHA256="38e3f2e176277851a059c9a8c9d37cc913e2602e5fc661b71298dbb9ccaf8411"


def load_and_verify():
    d=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert d["source_git_blob_sha1"]==EXPECTED_SOURCE_SHA1
    assert d["model_free"] is True
    counts=d["phase_counts_16x16_y_then_x"]
    assert len(counts)==16 and all(len(row)==16 for row in counts)
    ranked=sorted(
        [(n,x,y) for y,row in enumerate(counts) for x,n in enumerate(row)],
        reverse=True,
    )
    assert ranked[:2]==[(1591,4,12),(68,5,12)]
    assert counts[0][0]==62
    assert d["winner_phase_xy"]==[4,12]
    assert d["runner_up_phase_xy"]==[5,12]
    assert d["wrong_phase_00_hits"]==62
    assert d["planet_bitmap"]["size"]==[128,64]
    mask=base64.b64decode(d["planet_bitmap"]["base64"],validate=True)
    assert len(mask)==1024
    assert hashlib.sha256(mask).hexdigest()==EXPECTED_PLANET_SHA256
    assert d["planet_bitmap"]["sha256"]==EXPECTED_PLANET_SHA256
    assert sum(v.bit_count() for v in mask)==1591
    return d,mask


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pbm",help="Write exact original 128x64 planet mask as binary PBM")
    a=p.parse_args()
    d,mask=load_and_verify()
    if a.pbm:
        Path(a.pbm).write_bytes(b"P4\n128 64\n"+mask)
    print("OK: CL05 original-source phase winner (4,12), black 1591; second (5,12), 68")
    print("OK: 256-phase census; incorrect (0,0) black count 62")
    print("OK: 128x64 source planet mask, 1024 bytes, SHA256 "+EXPECTED_PLANET_SHA256)
    print("OK: no CE sticker values involved")


if __name__=="__main__":
    main()

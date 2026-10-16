#!/usr/bin/env python3
"""Verify the 2023 community mirror uploader's explicit missing-file caveats.

This is documentary provenance from uploader commit d0b11cf8..., NOT proof
of original 2019/2020 website bytes, original backend or sticker decoding.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
fixture=json.loads((ROOT/"data/terminal41-uploader-provenance-2026-10-16.json").read_text())
tree=json.loads((ROOT/"data/terminal41-source-tree.json").read_text())
paths={f["path"] for f in tree["files"]}
assert fixture["upstream_upload_commit"]=="d0b11cf8c6462c9592bc141ee6a4dddc0a029da6"
assert tree["source_tree_sha"]==fixture["preserved_mirror_source_tree"]
assert len(tree["files"])==74
missing=fixture["missing_file_names_as_uploader_reported"]
assert len(missing)==6 and len(set(missing))==6
assert not any("terminal41.link/"+p in paths for p in missing)
variants=fixture["upstream_described_non_original_html_versions"]
assert len(variants)==8 and len(set(p["claimed"] for p in variants))==8
assert all("terminal41.link/"+p["available"] in paths for p in variants)
assert len([p for p in variants if p["claimed"]!=p["available"]])==4
census=json.loads((ROOT/"data/terminal41-complete-client-census-2026-10-16.json").read_text())
assert census["summary"]["blob_match"]==73
linked={x["unpreserved_route"] for x in census["unmatched_internal_edges"]}
assert "/sys/activate_shutdown_protocol/commit/___________DONE_SD.html" in linked
assert any("___________DONE_SD_CONFIRMED_10.html" in p for p in missing)
print("PASS: 2023 uploader reported six absent paths and eight version-limited source copies; mirror identity is not website originality.")

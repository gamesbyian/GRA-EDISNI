#!/usr/bin/env python3
"""Verify the directly preserved Terminal41 seven-field ASCII island.

Run from the research repository:
  python scripts/audit_terminal41_saf_ascii_island.py
  python scripts/audit_terminal41_saf_ascii_island.py --source /path/to/saf_dat_col.html

The default test reproduces the field grammar and the archived-transcription
diff from separately preserved repo files. The optional source path performs
an independent whole-file ASCII-island scan. It does not reconstruct binary
image data or imply an intended semantic decode.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "endgame-saf-dat-island-2026-10-08.json"
ARCHIVE = ROOT / "archive" / "external" / "bigdusty" / "data" / "block_descriptions_full.json"
PATTERN = re.compile(r"[A-Za-z0-9+]{35,}")


def archive_block(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks = data["blocks"] if isinstance(data, dict) else data
    matches = [entry for entry in blocks if entry.get("id") == "block_116"]
    if len(matches) != 1:
        raise AssertionError("Expected one archived block_116")
    return matches[0]["text"]


def audit(source: Path | None = None) -> dict:
    record = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source_run = record["source_run"]
    derived = archive_block(ARCHIVE)
    fields = source_run.split("+")
    assert len(source_run) == 75
    assert [len(value) for value in fields] == [26, 22, 10, 2, 3, 1, 5]
    assert source_run.count("+") == 6
    assert fields[1] == "38546uy754j9j6tuk5fi34"
    assert fields[-1] == "41212"
    assert derived == record["archive_transcription"]
    assert len(derived) == len(source_run)
    substitutions = [
        {"offset": i, "source": char, "archive": derived[i]}
        for i, char in enumerate(source_run)
        if char != derived[i]
    ]
    assert substitutions == [{"offset": 24, "source": "i", "archive": "1"}]
    result = {
        "source_blob_sha": record["primary_blob_sha"],
        "fields": fields,
        "field_lengths": [len(value) for value in fields],
        "plus_delimiters": source_run.count("+"),
        "archive_differences": substitutions,
        "checks": "passed",
    }
    if source is not None:
        content = source.read_bytes().decode("utf-8", errors="replace")
        found = [(match.start(), match.group()) for match in PATTERN.finditer(content)]
        assert found == [(record["source_long_run_start_index_utf16_js"], source_run)], found[:20]
        result["whole_file_islands_35_or_longer"] = len(found)
        result["whole_file_observation"] = "exactly one, matching frozen source field"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="optional original saf_dat_col source file")
    args = parser.parse_args()
    print(json.dumps(audit(args.source), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

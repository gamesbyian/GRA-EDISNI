#!/usr/bin/env python3
"""Validate the curated sticker evidence map and its historical title index.

Offline, standard-library-only structural checks. This script is NOT an
independent reproduction of the science in the cited experiment reports.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data/sticker-evidence-register.csv"
INDEX = ROOT / "docs/experiment-title-index.md"
LEDGER = ROOT / "docs/experiment-ledger.md"
VIEW = ROOT / "docs/evidence-register-view.md"
MATRIX = ROOT / "docs/hypothesis-test-coverage-matrix.md"
CONCEPT = ROOT / "docs/experiment-concept-map.md"
FAMILIES = {
    "BASE", "CROSS", "ORDER", "GEOMETRY", "TAIL", "RECURSIVE",
    "CONVENTIONAL", "DIGIT", "LEVER", "OVERLAY", "CUBE", "PUNCH",
}
COLUMNS = [
    "record_id", "family", "question", "test_design", "independence",
    "assessment", "experiment_ids", "source", "source_state", "corpus",
    "dependency_cluster", "finding", "scope_limit", "needed_evidence",
]
LEDGER_LINE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|$", re.M)
RECORD_ID = re.compile(r"R\d{3}$")
PR_URL = re.compile(
    r"https://github\.com/gamesbyian/GRA-EDISNI/pull/\d+$"
)


def main() -> int:
    errors: list[str] = []
    ledger = LEDGER.read_text(encoding="utf-8")
    original = [(int(num), title) for num, title in LEDGER_LINE.findall(ledger)]
    canonical_ids = {num for num, _ in original}
    if len(canonical_ids) != len(original):
        errors.append("duplicate experiment numbers in main ledger")
    if not original or max(canonical_ids) < 423:
        errors.append("main ledger does not reach expected pilot vintage 423")

    # The index duplicates titles for navigation only; exact matching catches drift.
    expected_titles = [
        (num, title.replace("|", "/")) for num, title in original
    ]
    title_rows = [(int(num), title) for num, title in
                  LEDGER_LINE.findall(INDEX.read_text(encoding="utf-8"))]
    # The historical index is a dated snapshot. New ledger rows must not make
    # unrelated research PRs fail CI; changed/deleted historical titles should.
    current_titles = dict(expected_titles)
    if not title_rows or any(current_titles.get(num) != title for num, title in title_rows):
        errors.append("historical title index contains a title absent/changed in ledger")
    new_since_index = len(original) - len(title_rows)
    if new_since_index > 0:
        print(f"NOTE: historical title index needs a refresh for {new_since_index} newer entries")

    with REGISTER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != COLUMNS:
            errors.append("unexpected evidence-register column schema")
        rows = list(reader)
    if not rows:
        errors.append("empty evidence register")
    record_ids = [r.get("record_id", "") for r in rows]
    if len(set(record_ids)) != len(record_ids):
        errors.append("duplicate claim record IDs")
    for index, row in enumerate(rows, start=2):
        tag = f"CSV row {index}"
        if any(not row.get(key) for key in COLUMNS):
            errors.append(f"{tag}: missing required field")
            continue
        rid = row["record_id"]
        if not RECORD_ID.fullmatch(rid):
            errors.append(f"{tag}: invalid record id {rid}")
        if row["family"] not in FAMILIES:
            errors.append(f"{tag}: invalid mechanism family {row['family']}")
        source_state = row["source_state"]
        source = row["source"]
        if source_state == "main":
            candidate = ROOT / source
            if source.startswith("http") or not candidate.is_file():
                errors.append(f"{tag}: main source path unavailable {source}")
        elif source_state == "open-pr":
            if not PR_URL.fullmatch(source):
                errors.append(f"{tag}: unmerged source is not a PR URL")
            if row["assessment"] != "pending" or row["independence"] != "pending":
                errors.append(f"{tag}: unmerged result is not quarantined as pending")
        else:
            errors.append(f"{tag}: invalid source_state {source_state}")
        ids = [] if row["experiment_ids"] == "none" else row["experiment_ids"].split(";")
        for exp in ids:
            if not exp.isdigit():
                errors.append(f"{tag}: invalid experiment id {exp}")
                continue
            if source_state == "main" and int(exp) not in canonical_ids:
                errors.append(f"{tag}: experiment {exp} absent from main ledger")
        if source_state == "open-pr" and not ids and row["family"] != "BASE":
            errors.append(f"{tag}: non-context PR without a numbered experiment")

    view = VIEW.read_text(encoding="utf-8")
    headings = re.findall(r"^## (R\d{3}) · ", view, re.M)
    if headings != record_ids:
        errors.append("human evidence cards do not match canonical CSV IDs/order")

    matrix = MATRIX.read_text(encoding="utf-8")
    referenced = set(re.findall(r"\bR\d{3}\b", matrix))
    unknown = referenced - set(record_ids)
    if unknown:
        errors.append("unregistered matrix record IDs: " + ", ".join(sorted(unknown)))
    if str(len(title_rows)) not in INDEX.read_text(encoding="utf-8"):
        errors.append("title index count description appears stale")
    if not CONCEPT.is_file():
        errors.append("conceptual map missing")
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print(f"PASS: {len(original)} historical titles; {len(rows)} curated claims; "
          f"{len(FAMILIES)-2} mechanisms + BASE context + CROSS method; "
          f"{sum(r['source_state'] == 'open-pr' for r in rows)} pending claim cards; "
          f"{len(set(r['dependency_cluster'] for r in rows))} dependence clusters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

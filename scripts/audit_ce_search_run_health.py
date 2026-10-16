#!/usr/bin/env python3
"""Audit actual execution and censoring across public INSIDE CE discovery outputs.

Offline, schema-aware and fail-closed: DOES NOT search the internet or infer
ownership from a result URL. Intended for retained historical artifacts and CI.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

KINDS = ("brave_index", "wayback_cdx", "reddit_archive",
         "public_harvest", "html_images", "bluesky")
NOT_ATTEMPTED = {"planned_unexecuted", "not_attempted", "not-attempted",
                 "not_attempted_after_provider_block", "not-attempted-after-rate-limit",
                 "skipped_after_endpoint_access_failure"}
SUCCESS = {
    "brave_index": {"index_search_success"},
    "wayback_cdx": {"metadata_sample_received"},
    "reddit_archive": {"ok"},
    "bluesky": {"ok"},
}
ERROR = {"http_error", "request_error", "unavailable", "error",
         "CDX-http-error", "CDX-unavailable"}

def _rows(value):
    if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
        raise ValueError("Expected a list of evidence records")
    return value

def health(kind, payload):
    if kind not in KINDS:
        raise ValueError("Unknown public search artifact kind")
    if kind in ("brave_index", "wayback_cdx", "reddit_archive"):
        rows = _rows(payload)
    elif not isinstance(payload, dict):
        raise ValueError("Expected structured search report")
    else:
        rows = _rows(payload.get("results", [])) if kind == "bluesky" else []
    counts = Counter()
    possible_missing = []
    actual_success = set()
    if kind in SUCCESS:
        for i, row in enumerate(rows):
            status = row.get("status", "")
            if kind == "bluesky" and row.get("kind") == "direct_control":
                counts["source_direct_controls"] += 1
                continue
            if status in NOT_ATTEMPTED:
                counts["not_attempted"] += 1
            elif status in SUCCESS[kind]:
                counts["valid_provider_responses"] += 1
                actual_success.add(i)
            elif status in ERROR or "error" in status.lower():
                counts["provider_failures"] += 1
            else:
                counts["unknown_statuses"] += 1
                possible_missing.append({"row": i, "status": status})
            if row.get("possibly_truncated") or row.get("cursor_available"):
                counts["potentially_truncated_query_pages"] += 1
            omitted = row.get("new_candidates_omitted_at_cap", 0)
            if isinstance(omitted, int) and omitted > 0:
                counts["qualified_candidates_dropped_by_cap"] += omitted
            if kind == "brave_index" and status == "index_search_success":
                counts["index_result_appearances"] += len(row.get("matches", []))
            if kind == "bluesky" and status == "ok":
                counts["index_result_appearances"] += len(row.get("posts", []))
    if kind == "public_harvest":
        sources = _rows(payload.get("sources", []))
        for row in sources:
            counts["selected_sources"] += 1
            if row.get("classification") != "ok":
                counts["not_acquired"] += 1
            elif not any(x.get("size", 0) > 0 for x in row.get("files", [])):
                counts["success_without_payload"] += 1
            else:
                counts["source_payload_acquired"] += 1
    if kind == "html_images":
        meta = payload.get("source_coverage", {})
        if not isinstance(meta, dict):
            raise ValueError("Malformed HTML image coverage report")
        counts["image_mentions"] = len(_rows(payload.get("image_mentions", [])))
        for col in ("source_metadata_files", "html_pages_seen", "readable_html_pages",
                    "oversized_html_pages", "invalid_metadata_files",
                    "metadata_without_public_url", "html_pages_without_image_urls"):
            value = meta.get(col, 0)
            if not isinstance(value, int) or value < 0:
                raise ValueError("Invalid HTML image count: " + col)
            counts[col] = value
    if kind == "bluesky" and payload.get("state") != "executed_bounded":
        # An offline plan may retain task rows, but must never report retrieval.
        if any(x.get("status") == "ok" for x in rows):
            raise ValueError("Unexecuted plan cannot report retrieved posts")
        counts["unexecuted_run"] += 1
    data = dict(sorted(counts.items()))
    flags = []
    if data.get("unexecuted_run") or (not rows and kind not in ("public_harvest", "html_images")):
        flags.append("no_measured_search_responses")
    if data.get("not_attempted"):
        flags.append("some_tasks_never_attempted")
    if data.get("provider_failures") or data.get("not_acquired"):
        flags.append("provider_or_acquisition_failures")
    if data.get("potentially_truncated_query_pages"):
        flags.append("first_page_does_not_establish_recall")
    if data.get("qualified_candidates_dropped_by_cap"):
        flags.append("qualified_candidates_dropped")
    if data.get("success_without_payload"):
        flags.append("zero_payload_despite_success_classification")
    if data.get("oversized_html_pages") or data.get("invalid_metadata_files") or data.get("metadata_without_public_url"):
        flags.append("source_pages_not_inspected")
    if data.get("unknown_statuses"):
        flags.append("unrecognized_outcome_needs_review")
    if kind == "html_images" and not data.get("readable_html_pages"):
        flags.append("no_html_body_scanned")
    if kind == "public_harvest" and not data.get("source_payload_acquired"):
        flags.append("no_source_payload_acquired")
    return {
        "schema_version": 1,
        "kind": kind,
        "row_count": len(rows) if kind in SUCCESS else data.get("selected_sources", data.get("source_metadata_files", 0)),
        "counts": data,
        "flags": sorted(set(flags)),
        "unrecognized_rows": possible_missing,
        "evidence_bound": "sampled_source_or_search_execution_only_not_owner_or_sticker_proof",
        "new_confirmed_stickers": 0,
    }

def load_input(path: Path):
    body = path.read_text(encoding="utf-8").strip()
    if not body:
        raise ValueError("Empty source evidence")
    if body.startswith("["):
        return json.loads(body)
    if body.startswith("{"):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass
    return [json.loads(line) for line in body.splitlines() if line.strip()]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=KINDS, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict", action="store_true",
                        help="Return exit 2 when failures, incompleteness or zero acquisition detected")
    args = parser.parse_args()
    result = health(args.kind, load_input(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    if args.strict and result["flags"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()

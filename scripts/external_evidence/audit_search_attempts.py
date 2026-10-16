#!/usr/bin/env python3
"""Offline CE search-run accounting and safe resumable queue.

Does not execute searches. Consume immutable planned tasks and observed provider
events; preserve individual attempts while distinguishing no result, no attempt,
provider error, censored pagination and original source retrieval. Never
conclude sticker ownership or historical nonexistence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

OK = {"index_search_success", "original_source_retrieved", "original_image_retrieved"}
FAILED = {"http_error", "request_error", "blocked", "rate_limited", "unavailable", "provider_timeout"}
CENSORED = {"pagination_incomplete", "result_cap_reached", "not_attempted_after_provider_block"}
NOT_ATTEMPTED = {"planned_unexecuted", "not_attempted"}
STATUSES = OK | FAILED | CENSORED | NOT_ATTEMPTED
SHA = re.compile(r"[0-9a-f]{64}")


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = []
    with path.open(encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"row {n}: expected an object")
            rows.append(row)
    return rows


def evaluate(tasks: list[dict], events: list[dict]) -> tuple[dict, list[dict], list[dict]]:
    manifests = {}
    for row in tasks:
        ident = str(row.get("task_id") or "")
        if not ident or ident in manifests:
            raise ValueError("missing or duplicate planned task ID")
        manifests[ident] = row
    latest = {}
    attempts = set()
    counts = Counter()
    ledger = []
    for row in events:
        ident = str(row.get("task_id") or "")
        if ident not in manifests:
            raise ValueError(f"observed event not in frozen task manifest: {ident}")
        event = dict(row)
        state = str(event.get("status", ""))
        if state not in STATUSES:
            raise ValueError(f"unknown event status for {ident}: {state}")
        attempt_id = event.get("attempt_id", "")
        if state not in NOT_ATTEMPTED:
            if not isinstance(attempt_id, str) or not attempt_id.strip():
                raise ValueError(f"real provider event needs attempt_id: {ident}")
            identity = (ident, attempt_id)
            if identity in attempts:
                raise ValueError(f"duplicate provider attempt: {ident}/{attempt_id}")
            attempts.add(identity)
            if state in OK and not SHA.fullmatch(str(event.get("response_sha256") or "")):
                raise ValueError(f"successful acquisition requires content response SHA256: {ident}")
        if state in CENSORED and event.get("pages_exhausted") is True:
            raise ValueError(f"censored response cannot claim exhausted pages: {ident}")
        if state in FAILED and event.get("no_evidence_exists") is True:
            raise ValueError(f"blocked provider cannot establish absence: {ident}")
        counts[state] += 1
        ledger.append(event)
        latest[ident] = event

    summary_counts = Counter()
    pending = []
    for ident, task in manifests.items():
        event = latest.get(ident)
        state = event["status"] if event else "planned_unexecuted"
        summary_counts[state] += 1
        # A valid first page does not prove that search pagination is exhausted.
        incomplete = event and state in OK and event.get("pages_exhausted") is not True
        if state not in OK or incomplete:
            pending.append({**task, "resume_status": state,
                            "retry_policy": "manual-review-before-retrying" if state in FAILED
                                            else "pagination-requires-review" if incomplete
                                            else "not-yet-complete"})
    # Manifest identity remains stable across resumptions. Prior event logs can
    # be concatenated verbatim but every attempt ID stays unique.
    stable = "\n".join(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in tasks)+"\n"
    report = {
        "schema_version": 1,
        "planned_tasks": len(manifests),
        "task_manifest_sha256": hashlib.sha256(stable.encode("utf-8")).hexdigest(),
        "event_records": len(ledger),
        "real_provider_attempts": len(attempts),
        "successful_acquisition_events": sum(counts[x] for x in OK),
        "blocked_or_error_events": sum(counts[x] for x in FAILED),
        "censored_events": sum(counts[x] for x in CENSORED),
        "latest_task_states": dict(sorted(summary_counts.items())),
        "pending_or_censored_tasks": len(pending),
        "complete_tasks_with_exhausted_pagination": len(manifests) - len(pending),
        "source_discovery_claim": "attempted valid returned responses only",
        "no_historical_absence_claim": True,
        "new_confirmed_stickers": 0,
    }
    return report, pending, ledger


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks", required=True, type=Path,
                   help="Frozen task JSONL (gold or public native campaign)")
    p.add_argument("--events", type=Path, action="append",
                   help="Append-only observed provider-event JSONL; may repeat for prior runs")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    tasks = read_jsonl(args.tasks)
    events = []
    for path in args.events or []:
        events.extend(read_jsonl(path))
    report, pending, log = evaluate(tasks, events)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "run-summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    for filename, rows in (("resume-pending.jsonl", pending), ("validated-events.jsonl", log)):
        (args.out / filename).write_text(
            "".join(json.dumps(x, ensure_ascii=False, sort_keys=True)+"\n" for x in rows),
            encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

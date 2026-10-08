#!/usr/bin/env python3
"""Experiment 460: independently check the April 2020 URL discovery chronology.

Checks only pinned community timeline claims and saved pre-/post-index readings.
Source text is documented in a fixture with upstream GitHub commit permalinks.
Does NOT claim that the original images are legible at every URL character,
that Discord message content was independently fetched, or that the CE
foreground has been decoded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "experiment-460-background-url-discovery.json"
DISCORD_EPOCH_MS = 1420070400000


def levenshtein(a: str, b: str) -> int:
    prior = list(range(len(b) + 1))
    for i, left in enumerate(a, 1):
        current = [i]
        for j, right in enumerate(b, 1):
            current.append(min(
                current[-1] + 1, prior[j] + 1,
                prior[j - 1] + (left != right),
            ))
        prior = current
    return prior[-1]


def date_of_snowflake(identifier: str) -> datetime:
    stamp = (int(identifier) >> 22) + DISCORD_EPOCH_MS
    return datetime.fromtimestamp(stamp / 1000, tz=timezone.utc)


def run(before: Path | None = None, after: Path | None = None,
        transcript: Path | None = None) -> dict:
    record = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert record["schema_version"] == 1
    e = record["evidence"]
    correct = e["external_discovery"]["exact_target"]
    assert correct == "dat/534brn9653f9j8mmd"
    assert len(correct) == 21
    assert e["before_april21"]["commit"] != e["after_april21"]["commit"]
    assert not e["before_april21"]["contains_exact_address"]
    assert e["after_april21"]["contains_exact_address"]
    assert "twinysam/INSIDE-ARG" == record["upstream_repo"]

    # Optional *actual snapshot* checks, when text has been separately
    # acquired with correct SHA provenance. No network/API dependency in CI.
    if before is not None:
        assert correct not in before.read_text(encoding="utf-8")
    if after is not None:
        assert correct in after.read_text(encoding="utf-8")

    direct = e["primary_discord_export"]
    assert direct["blob_sha"] == "1889cc948f86f5a4455de0d7310b15cdb1b88b5c"
    assert len(direct["directly_recovered_events"]) == 8
    if transcript is not None:
        source = transcript.read_bytes()
        sha = hashlib.sha1(
            f"blob {len(source)}\\0".encode("ascii") + source
        ).hexdigest()
        assert sha == direct["blob_sha"], (sha, direct["blob_sha"])
        text = source.decode("utf-8")
        for event in direct["directly_recovered_events"]:
            marker = f"[{event['export_timestamp']}] {event['author']}\\n"
            start = text.find(marker)
            assert start >= 0, event
            stop = text.find("\\n\\n\\n[", start)
            block = text[start:stop if stop >= 0 else len(text)]
            assert event["content_contains"] in block, event

    output = []
    for candidate in e["recorded_preindex_candidates"]:
        guess = candidate["text"]
        timestamp = (date_of_snowflake(candidate["discord_snowflake"])
                     if candidate.get("discord_snowflake") else None)
        if timestamp is not None:
            assert timestamp < date_of_snowflake(e["external_discovery"]["discord_snowflake"])
        mismatches = [
            {"position_1_based": i + 1, "suggested": x, "later_exact": y}
            for i, (x, y) in enumerate(zip(guess, correct))
            if x != y
        ]
        assert len(guess) == len(correct)
        assert levenshtein(guess, correct) == len(mismatches)
        assert mismatches
        output.append({
            "stage": candidate["label"],
            "literal_guess": guess,
            "characters": len(guess),
            "mismatch_count": len(mismatches),
            "matches": len(correct) - len(mismatches),
            "mismatches": mismatches,
            "referenced_discord_message_utc": timestamp.isoformat() if timestamp else None,
            "provenance_warning": candidate["source_tier"],
        })
    assert [p["mismatch_count"] for p in output] == [4, 3, 2]
    external = e["external_discovery"]
    source_discovery = date_of_snowflake(external["discord_snowflake"])
    assert source_discovery.date().isoformat() == "2020-04-21"
    before_commit_date = datetime.fromisoformat(
        e["before_april21"]["commit_date_utc"].replace("Z", "+00:00")
    )
    after_commit_date = datetime.fromisoformat(
        e["after_april21"]["commit_date_utc"].replace("Z", "+00:00")
    )
    assert before_commit_date < source_discovery < after_commit_date
    assert correct + "/" in external["paths_reported"]
    assert len(external["paths_reported"]) == 4
    return {
        "result": "historical source-enumeration-assisted identification",
        "earliest_pinned_git_source_utc": before_commit_date.isoformat(),
        "source_index_discovery_discord_id_utc": source_discovery.isoformat(),
        "earliest_pinned_git_solution_utc": after_commit_date.isoformat(),
        "preindex_partial_artwork_interpretations": output,
        "recognized_exact_address": correct,
        "discovery_channel": external["channel"],
        "reported_index_paths": external["paths_reported"],
        "pre_index_full_blind_decode_documented": False,
        "ce_background_association_documented": True,
        "original_channel_export_sha": direct["blob_sha"],
        "original_channel_events_corroborated": len(direct["directly_recovered_events"]),
        "original_export_directly_verified_this_run": transcript is not None,
        "sticker_foreground_decoder_evidence": False,
        "limits": record["interpretive_boundaries"],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--before", type=Path, help="optional pinned April 21 README")
    p.add_argument("--after", type=Path, help="optional pinned April 23 README")
    p.add_argument("--export", type=Path,
                   help="optional exact original exported Discord .txt, with Git blob verification")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = run(args.before, args.after, args.export)
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print(content, end="")


if __name__ == "__main__":
    main()

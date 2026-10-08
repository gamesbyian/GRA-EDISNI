#!/usr/bin/env python3
"""Experiment 466: fixed, retrospective Terminal41 directory lookup control.

Checks how the *historically recorded* partial CE-background readings rank
against a known September-2026 74-path preserved mirror. NOT a recreation
of the original April 2020 Wayback directory index or a blind solve.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "terminal41-source-tree.json"
HISTORY_PATH = ROOT / "data" / "experiment-465-background-url-discovery.json"
EXPECTED_SOURCE_TREE = "4de72d7c2f21bd9eb4144fda51281c84cbcb90c4"


def normalized_url_path(path: str) -> str:
    assert path.startswith("terminal41.link/"), path
    path = path[len("terminal41.link/"):]
    if path.endswith("/index.html"):
        return path[:-len("/index.html")]
    for ending in (".html", ".txt", ".png"):
        if path.endswith(ending):
            return path[:-len(ending)]
    return path


def edit_distance(a: str, b: str) -> int:
    old = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        new = [i]
        for j, cb in enumerate(b, 1):
            new.append(min(new[j - 1] + 1, old[j] + 1,
                           old[j - 1] + (ca != cb)))
        old = new
    return old[len(b)]


def run() -> dict:
    manifest = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    assert manifest["source_repo"] == "twinysam/INSIDE-ARG"
    assert manifest["source_tree_sha"] == EXPECTED_SOURCE_TREE
    assert manifest["count"] == len(manifest["files"]) == 74
    target = history["evidence"]["external_discovery"]["exact_target"]
    assert target == "dat/534brn9653f9j8mmd"
    paths = [normalized_url_path(obj["path"]) for obj in manifest["files"]]
    assert len(set(paths)) == len(paths) == 74
    assert paths.count(target) == 1
    assert any(obj["path"].endswith(target + "/index.html")
               for obj in manifest["files"])

    comparisons = []
    historical = history["evidence"]["recorded_preindex_candidates"]
    for candidate in historical:
        partial = candidate["text"]
        assert len(partial) == len(target) == 21
        alternatives = sorted(
            [{"path": path, "edit_distance": edit_distance(partial, path)}
             for path in paths],
            key=lambda row: (row["edit_distance"], row["path"]),
        )
        winner, runner = alternatives[:2]
        target_dist = edit_distance(partial, target)
        assert winner == {"path": target, "edit_distance": target_dist}
        assert target_dist in (2, 3, 4)
        assert runner["edit_distance"] >= 15
        assert target_dist == sum(a != b for a, b in zip(partial, target))
        comparisons.append({
            "readout": partial,
            "claimed_historical_stage": candidate["label"],
            "provenance": candidate["source_tier"],
            "source_2026_paths": len(paths),
            "winner": winner,
            "runner_up": runner,
            "separation_in_edits": runner["edit_distance"] - target_dist,
            "index_without_target_nearest_distance": runner["edit_distance"],
            "not_blind_2020_success": True,
        })
    assert len(comparisons) == 3
    assert [item["winner"]["edit_distance"] for item in comparisons] == [4, 3, 2]
    assert [item["runner_up"]["edit_distance"] for item in comparisons] == [17, 15, 15]
    return {
        "experiment": 466,
        "source": "2026-09-29 archived Terminal41 74-path tree and pinned 2020 chronology",
        "source_tree_sha": manifest["source_tree_sha"],
        "paths": 74,
        "normalization": "strip terminal41.link/ prefix; strip terminal /index.html, or .html/.txt/.png",
        "partial_readings": comparisons,
        "finding": ("The known exact CE background endpoint is the unique closest "
                    "string in this retrospective 74-route mirror for all three "
                    "documented partial readings."),
        "essential_limits": [
            "Mirror paths represent a retrospective curated survivor set, not the exact April 2020 Wayback index.",
            "Presence of the correct path in a reference set chosen after discovery makes rank not a blind decoder test.",
            "Levenshtein distance is a transparent retrieval rule, not a proven rule Playdead intended.",
            "Historical 19/21 variant is from a later summary and lacks located contemporaneous original message.",
            "The control says nothing about foreground dot/dash/slash operations, which require a separate source-licensed bridge.",
            "No p-value, model posterior, or probability of independent accidental URL match is inferred.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path)
    p.add_argument("--summary", action="store_true")
    args = p.parse_args()
    result = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    if args.summary:
        print(json.dumps({
            "status": "PASS",
            "source_paths": result["paths"],
            "distances": [
                [x["winner"]["edit_distance"], x["runner_up"]["edit_distance"]]
                for x in result["partial_readings"]
            ],
        }, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

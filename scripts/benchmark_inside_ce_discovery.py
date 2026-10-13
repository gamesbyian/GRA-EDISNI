#!/usr/bin/env python3
"""Plan and evaluate CE source discovery against frozen known positives.

Queries contain language-appropriate products/site terms but NEVER target URLs
or owner identifiers from the gold dataset. Original source URLs are held out
in the private evaluation step until provider results are available. No web
requests; a zero-hit API result does not prove historical absence.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/reference/inside-ce-discovery-gold-controls.tsv"

def load_gold(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    needed = ("control_id", "surface", "target_url", "source_discovery_query_a",
              "source_discovery_query_b", "required_evidence_surface")
    for row in rows:
        if any(not row.get(k) for k in needed):
            raise ValueError("Incomplete gold control")
    if len({x["control_id"] for x in rows}) != len(rows):
        raise ValueError("Repeated gold control IDs")
    return rows

def plan(gold: list[dict]) -> list[dict]:
    tasks = []
    for field in ("source_discovery_query_a", "source_discovery_query_b"):
        for row in gold:
            u = urlsplit(row["target_url"])
            if not u.hostname or u.scheme not in ("http", "https"):
                raise ValueError("Gold control must be a public HTTP(S) URL")
            query = row[field]
            if row["target_url"].lower() in query.lower():
                raise ValueError("Source URL leaked into blind search query")
            # Do not append precise thread IDs, post IDs, usernames, or full
            # known URL paths. General index scoping is not source leakage.
            site = u.hostname.lower().removeprefix("www.")
            expression = "site:" + site + " " + query
            key = "\0".join((row["control_id"], field, expression))
            task_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
            tasks.append({
                "task_id": task_id, "community": "gold-" + row["surface"],
                "control_id": row["control_id"], "gold_search_variant": field[-1],
                "term": query, "index_query": expression,
                "language": "ru" if row["control_id"] == "G10" else "en",
                "state": "planned_unexecuted",
                "retrieval_goal": row["required_evidence_surface"],
                "coverage": "independent_discovery_query_withheld_original_source",
            })
    return tasks

def evaluate(gold: list[dict], results: list[dict]) -> tuple[list[dict], dict]:
    # Reuse URL source normalization; topic-level overlap is deliberately
    # weaker than a recovered exact post, comment, listing or image.
    import importlib.util
    file = ROOT / "scripts/triage_inside_ce_index_results.py"
    spec = importlib.util.spec_from_file_location("ce_triage_for_gold", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    wanted = {x["control_id"]: x for x in gold}
    tasks = {x["task_id"]: x["control_id"] for x in plan(gold)}
    observations = {g["control_id"]: {"attempted": 0, "successful": 0,
                                         "exact": 0, "topic_only": 0,
                                         "candidate_urls": set()}
                    for g in gold}
    for row in results:
        control = row.get("control_id") or tasks.get(row.get("task_id", ""))
        if control not in wanted:
            raise ValueError("Index result missing known gold control_id")
        slot = observations[control]
        slot["attempted"] += 1
        if row.get("status") != "index_search_success":
            continue
        slot["successful"] += 1
        target, target_topic, _ = module.normalize_url(wanted[control]["target_url"])
        for hit in row.get("matches", []):
            try:
                actual, topic, _ = module.normalize_url(hit.get("url", ""))
            except ValueError:
                continue
            slot["candidate_urls"].add(actual)
            if actual == target:
                slot["exact"] += 1
            elif target_topic and target_topic == topic:
                slot["topic_only"] += 1
    output = []
    for control, slot in observations.items():
        status = ("not_executed" if not slot["attempted"] else
                  "search_failed_or_unavailable" if not slot["successful"] else
                  "exact_source_found" if slot["exact"] else
                  "related_topic_only" if slot["topic_only"] else
                  "not_in_returned_index_hits")
        output.append({
            "control_id": control,
            "surface": wanted[control]["surface"],
            "known_community_status": wanted[control]["canonical_status"],
            "required_evidence_surface": wanted[control]["required_evidence_surface"],
            "provider_queries_attempted": slot["attempted"],
            "provider_queries_succeeded": slot["successful"],
            "distinct_candidate_urls": len(slot["candidate_urls"]),
            "exact_source_matches": slot["exact"],
            "topic_only_matches": slot["topic_only"],
            "outcome": status,
            "source_recall_assertion": "exact_source_only" if slot["exact"] else
                "no_claim_of_historical_absence",
        })
    summary = {
        "known_controls": len(gold),
        "queries_with_results_records": len(results),
        "controls_with_indexed_exact_source": sum(
            x["outcome"] == "exact_source_found" for x in output),
        "controls_without_executed_search": sum(
            x["outcome"] == "not_executed" for x in output),
        "scope": "only_submitted_provider_results; not full forum or image/reply coverage",
        "note": "A successful URL search is only URL discovery, not sticker verification.",
    }
    return output, summary

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gold", type=Path, default=DEFAULT)
    sub = ap.add_subparsers(dest="operation", required=True)
    generate = sub.add_parser("plan")
    generate.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("evaluate")
    check.add_argument("--input", type=Path, nargs="+", required=True)
    check.add_argument("--output", type=Path, required=True)
    check.add_argument("--summary", type=Path, required=True)
    args = ap.parse_args()
    gold = load_gold(args.gold)
    if args.operation == "plan":
        prepared = plan(gold)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in prepared),
            encoding="utf-8"
        )
        print(json.dumps({"controls": len(gold), "planned_queries": len(prepared),
                          "network": "none", "state": "planned_unexecuted"}))
    else:
        collected = []
        for path in args.input:
            with path.open(encoding="utf-8") as f:
                collected.extend(json.loads(line) for line in f if line.strip())
        report, summary = evaluate(gold, collected)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
        print(json.dumps(summary))

if __name__ == "__main__":
    main()

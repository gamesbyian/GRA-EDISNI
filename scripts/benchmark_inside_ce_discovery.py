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
import re

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

def locator_quality(row: dict) -> str:
    """Whether a gold URL names an original source, rather than an alias or profile."""
    u = urlsplit(row["target_url"])
    host = (u.hostname or "").lower()
    if host in {"ebay.io", "ebay.to"}:
        return "short_redirect_requires_original_listing"
    if row["surface"] == "instagram" and not re.search(r"/(?:p|reel|tv)/[^/]+", u.path):
        return "profile_not_original_image_post"
    return "original_source_locator"


def scope_site(row: dict, variant: str) -> str:
    """Use the real indexed platform, not a link-shortener's host."""
    surface = row["surface"]
    if surface == "ebay":
        return "ebay.com"
    if surface == "twitter":
        return "x.com" if variant == "b" else "twitter.com"
    host = urlsplit(row["target_url"]).hostname or ""
    return host.removeprefix("www.").lower()


def source_url_identity(url: str, normalize):
    """Treat old/new X domains as one exact status ID, not two owners."""
    u = urlsplit(url)
    if (u.hostname or "").lower() in {"x.com", "twitter.com", "www.twitter.com",
                                       "mobile.twitter.com", "www.x.com"}:
        match = re.search(r"/status/(\d+)(?:/|$)", u.path)
        if match:
            return ("twitter-status:" + match.group(1), "", "twitter-status:" + match.group(1))
    return normalize(url)


def mixed_latin_cyrillic_words(query: str) -> list[str]:
    """Detect accidental confusable script mixing *within* a native word.

    Brand words in Latin script beside Russian words are normal; a single
    character sequence like Cyrillic х + Latin a + Cyrillic дл isn't.
    """
    return [
        word for word in re.findall(r"\w+", query)
        if re.search(r"[A-Za-z]", word) and re.search(r"[\u0400-\u052F]", word)
    ]


def plan(gold: list[dict]) -> list[dict]:
    tasks = []
    for field in ("source_discovery_query_a", "source_discovery_query_b"):
        for row in gold:
            u = urlsplit(row["target_url"])
            if not u.hostname or u.scheme not in ("http", "https"):
                raise ValueError("Gold control must be a public HTTP(S) URL")
            query = row[field]
            if mixed_latin_cyrillic_words(query):
                raise ValueError("Mixed Latin-Cyrillic search token: "
                                 + str(mixed_latin_cyrillic_words(query)))
            if row["target_url"].lower() in query.lower():
                raise ValueError("Source URL leaked into blind search query")
            serial = row.get("canonical_sticker_record", "")
            if re.fullmatch(r"\d{3}", serial) and re.search(
                rf"(?<!\d){re.escape(serial)}(?!\d)", query):
                raise ValueError("Known sticker serial leaked into blind recall query")
            # Do not append precise thread IDs, post IDs, usernames, or full
            # known URL paths. General index scoping is not source leakage.
            site = scope_site(row, field[-1])
            expression = "site:" + site + " " + query
            key = "\0".join((row["control_id"], field, expression))
            task_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
            tasks.append({
                "task_id": task_id, "community": "gold-" + row["surface"],
                "gold_target_locator_quality": locator_quality(row),
                "site_scope": site,
                "control_id": row["control_id"], "gold_search_variant": field[-1],
                "term": query, "index_query": expression,
                "language": "ru" if row["control_id"] == "G10" else "en",
                "state": "planned_unexecuted",
                "retrieval_goal": row["required_evidence_surface"],
                "coverage": "independent_discovery_query_withheld_original_source",
            })
    return tasks

def evaluate(gold: list[dict], results: list[dict]) -> tuple[list[dict], dict]:
    """Measure attempted vs merely listed queries and score only real source locators."""
    import importlib.util
    file = ROOT / "scripts/triage_inside_ce_index_results.py"
    spec = importlib.util.spec_from_file_location("ce_triage_for_gold", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    wanted = {x["control_id"]: x for x in gold}
    tasks = {x["task_id"]: x["control_id"] for x in plan(gold)}
    slots = {k: {
        "attempted": 0, "successful": 0, "failures": 0, "not_attempted_rows": 0,
        "exact": 0, "topic_only": 0, "candidate_urls": set(), "statuses": [],
    } for k in wanted}
    seen_task_ids = set()
    not_attempted = {
        "not_attempted", "planned_unexecuted", "not-attempted",
        "not_attempted_after_provider_block", "not-attempted-after-rate-limit",
    }
    errors = {"request_error", "http_error", "unavailable", "error"}
    for row in results:
        task_id = row.get("task_id", "")
        control = row.get("control_id") or tasks.get(task_id)
        if control not in wanted:
            raise ValueError("Index result missing known gold control_id")
        if task_id and task_id not in tasks:
            raise ValueError("Unrecognized task ID in gold index result")
        if task_id and tasks[task_id] != control:
            raise ValueError("Gold task ID does not belong to stated control")
        if task_id and task_id in seen_task_ids:
            raise ValueError("Duplicate gold task result would double-count recall")
        if task_id:
            seen_task_ids.add(task_id)
        slot = slots[control]
        status = row.get("status", row.get("state", ""))
        slot["statuses"].append(status)
        if status in not_attempted:
            slot["not_attempted_rows"] += 1
            continue
        if status != "index_search_success" and status not in errors:
            raise ValueError("Unrecognized gold index execution status: " + str(status))
        slot["attempted"] += 1
        if status != "index_search_success":
            slot["failures"] += 1
            continue
        if not isinstance(row.get("matches"), list):
            raise ValueError("Successful gold result without matches list")
        slot["successful"] += 1
        target, target_topic, _ = source_url_identity(
            wanted[control]["target_url"], module.normalize_url)
        for hit in row["matches"]:
            try:
                actual, topic, _ = source_url_identity(hit.get("url", ""), module.normalize_url)
            except (ValueError, AttributeError):
                continue
            slot["candidate_urls"].add(actual)
            if actual == target:
                slot["exact"] += 1
            elif target_topic and target_topic == topic:
                slot["topic_only"] += 1

    output = []
    for control, slot in slots.items():
        kind = locator_quality(wanted[control])
        scoreable = kind == "original_source_locator"
        status = (
            "original_locator_unscorable" if not scoreable else
            "not_executed" if slot["attempted"] == 0 else
            "search_failed_or_unavailable" if not slot["successful"] else
            "exact_source_found" if slot["exact"] else
            "related_topic_only" if slot["topic_only"] else
            "partial_index_inconclusive" if slot["successful"] < 2 or slot["failures"] else
            "not_in_returned_index_hits"
        )
        output.append({
            "control_id": control,
            "surface": wanted[control]["surface"],
            "known_community_status": wanted[control]["canonical_status"],
            "required_evidence_surface": wanted[control]["required_evidence_surface"],
            "target_locator_quality": kind,
            "original_source_recall_scoreable": scoreable,
            "provider_queries_planned": 2,
            "provider_queries_attempted": slot["attempted"],
            "provider_queries_succeeded": slot["successful"],
            "provider_queries_failed": slot["failures"],
            "provider_queries_explicitly_unattempted": slot["not_attempted_rows"],
            "provider_queries_without_result_record": max(
                0, 2 - len(slot["statuses"])),
            "distinct_candidate_urls": len(slot["candidate_urls"]),
            "exact_source_matches": slot["exact"] if scoreable else 0,
            "topic_only_matches": slot["topic_only"],
            "outcome": status,
            "source_recall_assertion": (
                "exact_source_only" if status == "exact_source_found"
                else "no_claim_of_historical_absence"),
        })
    summary = {
        "known_controls": len(gold),
        "controls_with_unscoreable_original_locator": sum(
            not x["original_source_recall_scoreable"] for x in output),
        "queries_with_results_records": len(results),
        "queries_attempted": sum(x["provider_queries_attempted"] for x in output),
        "queries_succeeded": sum(x["provider_queries_succeeded"] for x in output),
        "queries_failed": sum(x["provider_queries_failed"] for x in output),
        "queries_explicitly_unattempted": sum(
            x["provider_queries_explicitly_unattempted"] for x in output),
        "queries_not_represented_in_results": sum(
            x["provider_queries_without_result_record"] for x in output),
        "controls_with_indexed_exact_source": sum(
            x["outcome"] == "exact_source_found" for x in output),
        "controls_without_executed_search": sum(
            not x["provider_queries_attempted"] for x in output),
        "scope": "returned provider index pages only; not full forum, photo or comment recall",
        "note": "A redirect alias or account profile is not an exact original sticker photo.",
        "new_confirmed_stickers": 0,
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

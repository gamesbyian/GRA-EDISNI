#!/usr/bin/env python3
"""Create a bounded, offline, per-site forum-search task queue. No HTTP requests.

Each line of the terms file is an independent query, not a comma-separated or
space-separated token list. This script does not execute searches.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "data/reference/global-gaming-forums.tsv"
ROUTES = ROOT / "data/reference/global-gaming-forum-search-routing.tsv"
REQUIRED = {
    "community", "url", "primary_method", "fallback_method",
    "platform_hint", "classification_basis", "index_query_scope",
    "access_gate", "gha_mode", "directory_evidence", "known_limitations",
}


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if not rows:
        raise ValueError(f"Empty TSV: {path}")
    return rows


def check_routes(directory: list[dict[str, str]],
                 routes: list[dict[str, str]]) -> None:
    if not REQUIRED.issubset(routes[0]):
        raise ValueError(f"Routing matrix missing: {sorted(REQUIRED - routes[0].keys())}")
    directory_keys = [(x["community"], x["url"]) for x in directory]
    route_keys = [(x["community"], x["url"]) for x in routes]
    if len(set(route_keys)) != len(route_keys):
        raise ValueError("Duplicate routing matrix community+URL entries")
    if route_keys != directory_keys:
        missing = list(set(directory_keys) - set(route_keys))[:5]
        extra = list(set(route_keys) - set(directory_keys))[:5]
        raise ValueError(f"Routing matrix does not match directory: missing={missing}; extra={extra}")
    for row in routes:
        parts = urlsplit(row["url"])
        if parts.scheme != "https" or not parts.netloc:
            raise ValueError(f"Invalid HTTPS forum URL: {row['url']}")
        if not row["index_query_scope"].startswith("site:"):
            raise ValueError(f"Missing site scope for {row['community']}")


def get_terms(file_path: Path, other_terms: list[str]) -> list[str]:
    terms = file_path.read_text(encoding="utf-8").splitlines()
    terms.extend(other_terms)
    distinct, seen = [], set()
    for raw in terms:
        term = raw.strip()
        if not term:
            continue
        if len(term) > 600:
            raise ValueError("Individual query exceeds 600 characters")
        if term not in seen:
            seen.add(term)
            distinct.append(term)
    if not distinct:
        raise ValueError("Provide at least one non-empty search term")
    return distinct


def index_phrase(term: str, mode: str) -> str:
    if mode == "expression":
        return term
    # Plain literal phrases. Search providers may ignore punctuation or quoting;
    # this is a query suggestion, not exact-match proof.
    return '"' + term.replace('"', " ").strip() + '"'


def conditional_native_link(row: dict[str, str], term: str) -> str | None:
    base = "https://" + urlsplit(row["url"]).netloc
    m = row["primary_method"]
    if m == "discourse_search_json":
        # Unvalidated per host. Treat as a suggested probe, never a proven API.
        return base + "/search.json?" + urlencode({"q": term})
    if m == "stackexchange_search_advanced":
        return "https://api.stackexchange.com/2.3/search/advanced?" + urlencode(
            {"site": "gamedev", "q": term, "sort": "relevance", "pagesize": 100}
        )
    if m == "reddit_research_access_gate":
        path = urlsplit(row["url"]).path.rstrip("/")
        return "https://www.reddit.com" + path + "/search/?" + urlencode(
            {"q": term, "restrict_sr": "1"}
        )
    return None


def generate(directory: list[dict[str, str]], routes: list[dict[str, str]],
             terms: list[str], mode: str, max_tasks: int, output: Path,
             statuses: set[str]) -> dict[str, object]:
    check_routes(directory, routes)
    selected = [x for x in routes if x["directory_evidence"] in statuses]
    metadata = {(x["community"], x["url"]): x for x in directory}
    total = len(selected) * len(terms)
    if total > max_tasks:
        raise ValueError(f"{total} planned queries exceed --max-tasks={max_tasks}; "
                         "split the campaign or explicitly raise the cap")
    output.parent.mkdir(parents=True, exist_ok=True)
    by_method: Counter[str] = Counter()
    with output.open("w", encoding="utf-8") as f:
        for row in selected:
            for term in terms:
                index_query = row["index_query_scope"] + " " + index_phrase(term, mode)
                uid = hashlib.sha256(
                    (row["community"] + "\0" + row["url"] + "\0" + term +
                     "\0" + mode).encode("utf-8")
                ).hexdigest()[:20]
                descriptor = metadata[(row["community"], row["url"])]
                task = {
                    "task_id": uid,
                    "language": descriptor["language"],
                    "region": descriptor["region"],
                    "community": row["community"],
                    "url": row["url"],
                    "term": term,
                    "term_mode": mode,
                    "primary_method": row["primary_method"],
                    "fallback_method": row["fallback_method"],
                    "classification_basis": row["classification_basis"],
                    "access_gate": row["access_gate"],
                    "gha_mode": row["gha_mode"],
                    "directory_evidence": row["directory_evidence"],
                    "known_limitations": row["known_limitations"],
                    "index_query": index_query,
                    "manual_index_search_url": "https://www.google.com/search?" +
                        urlencode({"q": index_query}),
                    "conditional_native_url": conditional_native_link(row, term),
                    "archive_lookup_url": "https://web.archive.org/web/*/" + row["url"],
                    "state": "planned_unexecuted",
                    "results": [],
                }
                f.write(json.dumps(task, ensure_ascii=False) + "\n")
                by_method[row["primary_method"]] += 1
    return {
        "status": "planned_unexecuted",
        "total_forums_in_directory": len(directory),
        "selected_forums": len(selected),
        "distinct_terms": len(terms),
        "task_count": total,
        "query_mode": mode,
        "method_task_counts": dict(sorted(by_method.items())),
        "limitations": [
            "No network search, URL verification or corpus scan has been performed.",
            "A site-restricted search is an index sample, never proof of completeness.",
            "Conditional native URLs are candidates requiring per-host authorization/probe.",
            "Do not submit restricted sources to AI services without verifying their terms.",
        ],
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms-file", type=Path, required=True)
    parser.add_argument("--term", action="append", default=[])
    parser.add_argument("--query-mode", choices=("literal", "expression"),
                        default="literal")
    parser.add_argument("--statuses", default="V,C,H",
                        help="Comma-delimited directory statuses to include")
    parser.add_argument("--max-tasks", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("forum-search-tasks.jsonl"))
    parser.add_argument("--summary", type=Path, default=Path("forum-search-summary.json"))
    args = parser.parse_args()
    statuses = {x.strip() for x in args.statuses.split(",")}
    if not statuses or not statuses.issubset({"V", "C", "H"}):
        parser.error("--statuses must be a non-empty subset of V,C,H")
    if args.max_tasks < 1:
        parser.error("--max-tasks must be positive")
    stats = generate(load_tsv(DIRECTORY), load_tsv(ROUTES),
                     get_terms(args.terms_file, args.term), args.query_mode,
                     args.max_tasks, args.output, statuses)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()

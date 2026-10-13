#!/usr/bin/env python3
"""Build a locale-specific, provenance-safe CE/ARG search campaign (no HTTP)."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from urllib.parse import urlsplit
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data/reference/inside-ce-native-search-lexicon.tsv"
SECONDARY = ROOT / "data/reference/inside-ce-ownership-secondary-platforms.tsv"
DIRECTORY = ROOT / "data/reference/global-gaming-forums.tsv"
ROUTES = ROOT / "data/reference/global-gaming-forum-search-routing.tsv"
ARCHIVES = ROOT / "data/reference/global-gaming-forum-archive-routes.tsv"
MULTI_LOCALES = (
    "en", "fr", "de", "es", "es-AR", "es-MX", "es-CL", "es-CO", "es-PE",
    "pt", "pt-BR", "it", "nl", "pl", "cs", "sk", "hu", "ro", "bg", "sr",
    "hr", "sl", "el", "tr", "sv", "no", "da", "fi", "is", "ja",
    "zh-CN", "zh-TW", "zh-HK", "ko", "vi", "th", "id", "ms", "tl", "hi",
    "bn", "ur", "ne", "si", "ru", "uk", "ar", "fa", "he", "sw"
)
FIRST_PASS_LOCALES = (
    "en", "ja", "zh-TW", "zh-CN", "ko", "fr", "de", "es", "pt-BR",
    "it", "vi", "ar", "ru", "tr", "pl", "nl", "id", "th", "uk", "fa"
)

def load_tsv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def quote(v):
    return '"' + v.replace('"', " ").strip() + '"'

def expressions(lang):
    """Native expressions: the identifying proper names are not translated."""
    v = {k: quote(x) for k, x in lang.items() if k != "locale"}
    return (
        ("owner_bought", f'{quote("INSIDE")} {quote("iam8bit")} {v["ownership_phrase"]}'),
        ("owner_received", f'{quote("INSIDE")} {quote("iam8bit")} {v["arrival_phrase"]}'),
        ("edition_discussion", f'{quote("Playdead")} {v["edition_term"]}'),
        ("owner_without_game_name", f'{quote("RealDoll")} {v["ownership_phrase"]}'),
        ("sticker_photograph", f'{quote("INSIDE")} {quote("RealDoll")} {v["sticker_term"]}'),
        ("edition_number", f'{quote("INSIDE")} {quote("iam8bit")} {v["number_term"]}'),
        ("serial_without_title", f'{quote("RealDoll")} {v["number_term"]}'),
        ("arg_discussion", f'{quote("INSIDE")} {quote("Playdead")} {v["puzzle_term"]}'),
        ("for_sale", f'{quote("INSIDE")} {quote("iam8bit")} {v["sale_phrase"]}'),
        ("unboxing", f'{quote("INSIDE")} {quote("RealDoll")} {v["unboxing_term"]}'),
        ("outer_wrapper", f'{quote("INSIDE")} {v["outer_wrapper_term"]} {v["sticker_term"]}'),
        ("wrapper_without_title", f'{quote("iam8bit")} {v["outer_wrapper_term"]}'),
        ("edition_broad", f'{quote("INSIDE")} {v["edition_term"]}'),
        ("unboxing_without_game_name", f'{quote("Playdead")} {v["unboxing_term"]}'),
        ("sticker_with_number", f'{quote("Playdead")} {v["sticker_term"]} {v["number_term"]}'),
    )

def locales_for_site(label):
    """Use each community's language(s), not English translations of the user query."""
    if label == "multi":
        return MULTI_LOCALES
    if label in ("en-ur", "bn-en", "en-si", "en-ne", "en-ms", "en-tl"):
        return tuple(dict.fromkeys(label.split("-")))
    if label in ("ar-fr", "fr-ar", "uk-ru"):
        return tuple(dict.fromkeys(label.split("-")))
    return (label,)

def interleave_search_tasks(tasks):
    """Diversify early API queries across locales and source websites.

    One term from each locale per round; within a locale rotate sources before
    returning to another category on the same site. Reproducible and O(tasks).
    """
    pools = {}
    for task in tasks:
        pools.setdefault(task["locale"], {}).setdefault(task["site"], deque()).append(task)
    priority = {label: i for i, label in enumerate(FIRST_PASS_LOCALES)}
    ordered_locales = sorted(pools, key=lambda l: (priority.get(l, 1000), l))
    site_cycles = {}
    for idx, locale in enumerate(ordered_locales):
        sites = sorted(
            pools[locale],
            key=lambda s: (0 if pools[locale][s][0].get("priority", "P1") == "P0" else 1, s)
        )
        turn = idx % len(sites)
        site_cycles[locale] = deque(sites[turn:] + sites[:turn])
    ordered, remaining = [], len(tasks)
    while remaining:
        for locale in ordered_locales:
            sites = site_cycles[locale]
            if not sites:
                continue
            site = sites.popleft()
            queue = pools[locale][site]
            ordered.append(queue.popleft())
            remaining -= 1
            if queue:
                sites.append(site)
    return ordered


def build(directory, routes, archives, lexicon, *, allowed_statuses, max_tasks,
          include_weak=True, categories=None):
    if len(directory) != len(routes) or len(archives) != len(routes):
        raise ValueError("Directory, route and archive tables differ in length")
    for row, route, archive in zip(directory, routes, archives):
        if (row["community"], row["url"]) != (route["community"], route["url"]):
            raise ValueError("Forum route joined incorrectly")
        if (row["community"], row["url"]) != (archive["community"], archive["original_url"]):
            raise ValueError("Archive fallback joined incorrectly")
    dictionary = {v["locale"]: v for v in lexicon}
    if len(dictionary) != len(lexicon):
        raise ValueError("Duplicate locale code")
    records, omissions = [], Counter()
    for site, route, archive in zip(directory, routes, archives):
        if site["evidence_status"] not in allowed_statuses:
            continue
        if not include_weak and site["type"] in ("comments", "deals", "tabletop-adjacent"):
            continue
        for locale in locales_for_site(site["language"]):
            if locale not in dictionary:
                omissions[locale] += 1
                continue
            for category, expr in expressions(dictionary[locale]):
                if categories and category not in categories:
                    continue
                index_query = route["index_query_scope"] + " " + expr
                key = (site["community"], site["url"], locale, category, expr)
                task_id = hashlib.sha256("\0".join(key).encode("utf-8")).hexdigest()[:20]
                record = {
                    "task_id": task_id, "site": site["community"],
                    "community": site["community"], "url": site["url"],
                    "term": expr, "language": locale,
                    "locale": locale, "site_language_label": site["language"],
                    "category": category, "expression": expr,
                    "index_query": index_query,
                    "primary_method": route["primary_method"],
                    "access_gate": route["access_gate"],
                    "historical_route": archive["historical_route"],
                    "archive_assurance": archive["source_assurance"],
                    "host_capture_status": archive["host_capture_status"],
                    "evidence_status": site["evidence_status"],
                    "state": "planned_unexecuted",
                    "findings": [],
                    "interpretation": "query_candidate_no_search_executed",
                }
                records.append(record)
                if len(records) > max_tasks:
                    raise ValueError("Campaign exceeds --max-tasks; use site/category/status filters")
    if omissions:
        raise ValueError("Missing language profiles: " + repr(dict(omissions)))
    if len(records) != len({v["task_id"] for v in records}):
        raise ValueError("Duplicate task identifier")
    return interleave_search_tasks(records)

def build_secondary(sources, lexicon, *, max_tasks=20000, categories=None):
    """Discovery-only tasks for social/video/collector platforms, not API access."""
    dictionary = {row["locale"]: row for row in lexicon}
    tasks = []
    for source in sources:
        domain = urlsplit(source["url"]).netloc.lower()
        if not domain:
            raise ValueError("Missing auxiliary source host")
        for locale in locales_for_site(source["language"]):
            if locale not in dictionary:
                raise ValueError(f"Secondary {source['source']} has unknown locale {locale}")
            for category, expr in expressions(dictionary[locale]):
                if categories and category not in categories:
                    continue
                key = "\0".join((source["source"], source["url"], locale, category, expr))
                task_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
                tasks.append({
                    "task_id": task_id,
                    "community": source["source"], "site": source["source"],
                    "url": source["url"], "locale": locale, "language": locale,
                    "site_language_label": source["language"],
                    "term": expr, "expression": expr, "category": category,
                    "index_query": "site:" + domain + " " + expr,
                    "primary_method": source["primary_search"],
                    "access_gate": source["access_gate"],
                    "historical_route": source["fallback"],
                    "surface_type": source["surface_type"],
                    "why_relevant": source["why_relevant"],
                    "priority": source["priority"],
                    "source_scope": "secondary_social_resale",
                    "state": "planned_unexecuted",
                    "findings": [],
                    "interpretation": "index_discovery_only_neither_ownership_nor_sticker_verified",
                })
                if len(tasks) > max_tasks:
                    raise ValueError("Secondary search tasks exceed --max-tasks")
    if len(tasks) != len({x["task_id"] for x in tasks}):
        raise ValueError("Duplicate auxiliary search tasks")
    return interleave_search_tasks(tasks)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--secondary-output", type=Path,
                        help="Also prepare licensed-index leads for video/social/resale sites")
    parser.add_argument("--statuses", default="V,C,H")
    parser.add_argument("--max-tasks", type=int, default=20000)
    parser.add_argument("--exclude-weak", action="store_true",
                        help="Skip news/comment/deal pages; default includes them")
    parser.add_argument("--category", action="append")
    args = parser.parse_args()
    statuses = set(args.statuses.split(","))
    if not statuses <= {"V", "C", "H"} or not statuses:
        parser.error("Invalid evidence statuses")
    items = build(
        load_tsv(DIRECTORY), load_tsv(ROUTES),
        load_tsv(ARCHIVES), load_tsv(LEXICON),
        allowed_statuses=statuses, max_tasks=args.max_tasks,
        include_weak=not args.exclude_weak,
        categories=set(args.category) if args.category else None
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in items),
        encoding="utf-8"
    )
    stats = {
        "state": "planned_unexecuted", "tasks": len(items),
        "unique_sites": len({x["site"] for x in items}),
        "native_locales": sorted({x["locale"] for x in items}),
        "native_locale_count": len({x["locale"] for x in items}),
        "categories": dict(Counter(x["category"] for x in items)),
        "note": "No network search or ownership verification was performed by this planner.",
    }
    if args.secondary_output:
        secondary = build_secondary(
            load_tsv(SECONDARY), load_tsv(LEXICON),
            max_tasks=args.max_tasks,
            categories=set(args.category) if args.category else None
        )
        args.secondary_output.parent.mkdir(parents=True, exist_ok=True)
        args.secondary_output.write_text(
            "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n"
                    for x in secondary), encoding="utf-8"
        )
        stats["secondary_site_count"] = len({x["site"] for x in secondary})
        stats["secondary_tasks"] = len(secondary)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()

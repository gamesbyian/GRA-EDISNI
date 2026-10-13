#!/usr/bin/env python3
"""Build a locale-specific, provenance-safe CE/ARG search campaign (no HTTP)."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data/reference/inside-ce-native-search-lexicon.tsv"
DIRECTORY = ROOT / "data/reference/global-gaming-forums.tsv"
ROUTES = ROOT / "data/reference/global-gaming-forum-search-routing.tsv"
ARCHIVES = ROOT / "data/reference/global-gaming-forum-archive-routes.tsv"
MULTI_LOCALES = ("en", "fr", "de", "es", "pt-BR", "ja", "zh-CN", "zh-TW", "ko", "ru", "ar")

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
                    "task_id": task_id, "site": site["community"], "url": site["url"],
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
    # Distribute first-pass queries across countries/languages, rather than
    # exhaust one English forum before visiting an East-Asian/Arabic forum.
    by_locale = {}
    for item in records:
        by_locale.setdefault(item["locale"], []).append(item)
    ordered = []
    while any(by_locale.values()):
        for locale in sorted(by_locale):
            if by_locale[locale]:
                ordered.append(by_locale[locale].pop(0))
    return ordered

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
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
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()

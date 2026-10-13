#!/usr/bin/env python3
"""Exact-ID public CE resale post archival retrieval, independent of keyword search.

Always preserve missing IDs, API failure, archival date and duplicate-control roles.
No account tracing or outreach. A repost is not a second physical edition.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

if __package__:
    from .search_public_reddit_ce_media import (clean_item, curated_case_map, known_status,
                                                 known_url_evidence, request_json)
else:
    from search_public_reddit_ce_media import (clean_item, curated_case_map, known_status,
                                               known_url_evidence, request_json)

API = "https://arctic-shift.photon-reddit.com/api/posts/ids?ids="


def probe(sources: list[dict], known: dict[str, set[str]], requester=request_json):
    if not 1 <= len(sources) <= 20:
        raise ValueError("must select between 1 and 20 preapproved public post IDs")
    ids = []
    for entry in sources:
        ident = entry["id"]
        if not re.fullmatch(r"[a-z0-9]{5,9}", ident, re.I):
            raise ValueError("invalid target public post ID")
        if ident in ids:
            raise ValueError("duplicate target post ID")
        ids.append(ident)
    url = API + ",".join(ids)
    try:
        payload, digest = requester(url)
        results = payload.get("data", [])
        if not isinstance(results, list):
            raise ValueError("archive exact ID response is not an array")
        found = {str(x.get("id", "")).removeprefix("t3_").lower(): x for x in results
                 if isinstance(x, dict)}
        output = []
        for source in sources:
            ident = source["id"]
            raw = found.get(ident)
            if raw is None:
                output.append({"post_id": ident, "source_page_url": source["source_page_url"],
                               "status": "not-found-in-archive", "source_role": source["source_role"]})
                continue
            candidate = clean_item(raw, "post")
            if candidate is None:
                output.append({"post_id": ident, "source_page_url": source["source_page_url"],
                               "status": "archived-but-not-ce-relevant-or-removed",
                               "source_role": source["source_role"]})
                continue
            candidate["source_role"] = source["source_role"]
            candidate["source_status"] = known_status(candidate, known)
            candidate["curated_case_ref"] = known.get("case_by_post_id", {}).get(ident)
            candidate["retrieval"] = "exact-public-archived-post-id"
            candidate["status"] = "archived-post-available"
            output.append(candidate)
        return {"status": "ok", "archive_sha256": digest, "requested_ids": ids,
                "records": output}
    except (OSError, ValueError) as exc:
        return {"status": "archive-unavailable", "reason": str(exc)[:350],
                "requested_ids": ids,
                "records": [{"post_id": i, "status": "not-attempted-service-error",
                             "source_page_url": s["source_page_url"],
                             "source_role": s["source_role"]} for i, s in zip(ids, sources)]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path("data/reference/inside-ce-public-archived-resale-posts.json"))
    parser.add_argument("--canonical-ledger", type=Path,
                        default=Path("archive/external/twinysam-inside-arg/stickers.md"))
    parser.add_argument("--curated-known-sales", type=Path,
                        default=Path("data/reference/inside-ce-curated-known-public-sale-links.json"))
    parser.add_argument("--out", type=Path,
                        default=Path("visual-evidence-work/exact-ce-resale-posts.json"))
    args = parser.parse_args()
    sources = json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    known = known_url_evidence(args.canonical_ledger)
    known["case_by_post_id"] = curated_case_map(args.curated_known_sales)
    report = probe(sources, known)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "schema_version": 1, "interpretation": "Public archival leads only, not owner or sticker proof",
        **report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "requested": len(sources),
                      "archived_posts": sum(r["status"] == "archived-post-available"
                                            for r in report["records"])}))


if __name__ == "__main__":
    main()

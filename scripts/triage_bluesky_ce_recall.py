#!/usr/bin/env python3
"""Offline, deduplicated review queue from a measured Bluesky public search.

Consumes ONLY the explicitly executed native recall artifact. It does not
contact owners, infer ownership from matching text, or alter sticker records.
"""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from rank_inside_ce_public_leads import score

AT_POST = re.compile(r"^at://(did:[^/]+)/app\.bsky\.feed\.post/([a-zA-Z0-9]+)$")
HANDLE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9.-]{1,250}$")

def candidate_url(post):
    match = AT_POST.fullmatch(str(post.get("uri") or ""))
    handle = str(post.get("handle") or "")
    if not match or not HANDLE.fullmatch(handle):
        return None
    return "https://bsky.app/profile/" + quote(handle.lower(), safe=".-") + "/post/" + match.group(2)


def classify_ce_context(text):
    """Conservative Playdead-specific source relevance, separate from owner score.

    Blank text cannot be classified by words. The original native API artifact
    still retains every post, so a future image/alt-text experiment can review
    it separately without mistaking broad-query hits for proven CE evidence.
    """
    s = unicodedata.normalize("NFKC", str(text or "")).casefold()
    s = s.translate(str.maketrans({"’": "'", "‘": "'", "ʼ": "'"}))
    s = re.sub(r"\s+", " ", s)
    # Negative control: another game literally titled "Evil Inside" produces
    # "Evil Inside Collector's Edition" and passes naive title-prefix logic.
    if (("house of 1000 doors" in s or "evil inside collector" in s)
            and "playdead" not in s and "iam8bit" not in s):
        return "unrelated_or_unresolved"
    named_ce = bool(
        re.search(r"\binside\s+collector(?:'s|s)?\s+edition\b", s)
        or re.search(r"\bcollector(?:'s|s)?\s+edition\s+of\s+(?:playdead's\s+)?inside\b", s)
        or re.search(r"\bcollector(?:'s|s)?\s+edition\s+for\s+(?:the\s+game\s+)?inside\b", s)
    )
    playdead_inside = bool(re.search(r"\bplaydead\b", s) and re.search(r"\binside\b", s))
    meaningful_context = bool(re.search(
        r"\b(?:collector|sticker|cipher|arg|packaging|code|huddle|real doll|realdoll|statue|jelly)\b",
        s))
    # "iam8bit" + "inside" is not a game identifier: "what was inside
    # my iam8bit parcel?" or missing Blue Prince merch can match it.
    # Require independently distinctive CE/INSIDE puzzle vocabulary.
    iam8bit_inside = bool("iam8bit" in s
                          and re.search(r"\binside\b", s)
                          and re.search(r"\b(?:collector|sticker|huddle|realdoll|real doll|"
                                        r"statue|jelly|cipher|puzzle)\b", s))
    if not (named_ce or (playdead_inside and meaningful_context) or iam8bit_inside
            or "#insidearg" in s):
        return "unrelated_or_unresolved"
    owner_language = bool(re.search(
        r"\b(?:do i still need|should i keep|i (?:have|own|bought|got|received|"
        r"ordered|sold|unboxed)|my (?:copy|edition|statue|huddle|sticker|"
        r"collector)|selling my|getting rid of)\b", s))
    if owner_language:
        return "possible_owner_claim"
    if re.search(r"\b(?:arg|cipher|sticker|puzzle|code)\b", s) or "#insidearg" in s:
        return "arg_discussion"
    return "other_playdead_ce_context"

def build_queue(report, *, max_candidates=100):
    if report.get("state") != "executed_bounded" or not isinstance(report.get("results"), list):
        raise ValueError("Measured executed public search required")
    if not 1 <= max_candidates <= 500:
        raise ValueError("Candidate cap must be 1..500")
    joined = {}
    checked, indexed, errors = 0, 0, 0
    for result in report["results"]:
        if result.get("kind") != "blind_discovery":
            continue
        if result.get("status") == "error":
            errors += 1
            continue
        if result.get("status") != "ok":
            continue
        checked += 1
        for rank, post in enumerate(result.get("posts", []), 1):
            indexed += 1
            url = candidate_url(post)
            if not url:
                continue
            pts, reasons = score({"text": post.get("text_excerpt", "")})
            context = classify_ce_context(post.get("text_excerpt", ""))
            uri = post["uri"]
            x = joined.setdefault(uri, {
                "uri": uri, "url": url, "published_at": post.get("created_at"),
                "excerpt": str(post.get("text_excerpt") or "")[:450],
                "lead_score": pts, "reason_codes": reasons,
                "context_class": context,
                "search_matches": [], "known_positive_control": bool(post.get("target")),
                "evidence_status": "unverified_public_post_for_review",
                "owner_verified": False, "sticker_verified": False,
                "new_confirmed_stickers": 0,
            })
            if pts > x["lead_score"]:
                x["lead_score"], x["reason_codes"] = pts, reasons
            x["search_matches"].append({
                "key": result.get("key"), "version": result.get("version"),
                "rank_on_page": rank,
            })
    priority = {"possible_owner_claim": 0, "arg_discussion": 1,
                "other_playdead_ce_context": 2}
    relevant = [x for x in joined.values() if x["context_class"] in priority]
    # Keep all original unfiltered posts in the immutable API artifact; never
    # hand a generic sports/film post to Raezores merely for matching "Inside".
    ranked = sorted(relevant, key=lambda x: (
        priority[x["context_class"]], -x["lead_score"],
        -len(x["search_matches"]), x["uri"]))
    classes = Counter(x["context_class"] for x in joined.values())
    summary = {
        "retrieved_at_utc": report.get("fetched_at_utc"),
        "api_host": report.get("api_host", "unrecorded"),
        "searched_queries_with_valid_response": checked,
        "failed_queries": errors,
        "search_post_appearances": indexed,
        "unique_public_post_uris": len(joined),
        "context_class_counts": dict(sorted(classes.items())),
        "relevant_review_candidates": len(relevant),
        "excluded_from_review_queue": len(joined) - len(relevant),
        "original_unfiltered_api_results_retained": True,
        "queue_written": min(max_candidates, len(ranked)),
        "queue_truncated": len(ranked) > max_candidates,
        "known_positive_found": any(x["known_positive_control"] for x in relevant),
        "new_confirmed_stickers": 0,
        "interpretation": "Public source suggestions for independent human review, not known owners",
    }
    return ranked[:max_candidates], summary

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--summary", type=Path, required=True)
    ap.add_argument("--max-candidates", type=int, default=100)
    args = ap.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    hits, summary = build_queue(report, max_candidates=args.max_candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(hit, ensure_ascii=False) + "\n" for hit in hits),
        encoding="utf-8")
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == "__main__":
    main()

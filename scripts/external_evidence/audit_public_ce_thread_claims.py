#!/usr/bin/env python3
"""Public single-thread CE purchase/receipt-claim contradiction audit.

Only an exact public subreddit post ID is queried; authors are compared within
that thread, not across other accounts or profile histories. A contradictory
claim is not proof of nonownership, just a reason NOT to promote the initial
purchase assertion as an independently proven collector.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

if __package__:
    from .recover_reddit_comment_images import iter_comments, request_json
else:
    from recover_reddit_comment_images import iter_comments, request_json

POST_ID = re.compile(r"[a-z0-9]{5,9}", re.I)
HANDLE = re.compile(r"[A-Za-z0-9_-]{3,32}")
CLAIMS = {
    "purchase-asserted": re.compile(r"\b(?:just bought|i bought|i purchased|i ordered|"
                                   r"placed my order|bought the damn thing)\b", re.I),
    "purchase-retracted": re.compile(r"\b(?:i didn.t buy|i did not buy|"
                                    r"cancelled my order|canceled my order|"
                                    r"i never bought|i won.t buy)\b", re.I),
    "receipt-asserted": re.compile(r"\b(?:i received|i got mine|arrived today|"
                                  r"my copy arrived)\b", re.I),
}


def classify_body(body: str) -> list[str]:
    if body.strip().lower().startswith(("[deleted]", "[removed]")):
        return []
    return [tag for tag, regex in CLAIMS.items() if regex.search(body)]


def audit(comments: list[dict], post_id: str, *, truncated: bool = False) -> dict:
    if not POST_ID.fullmatch(post_id):
        raise ValueError("Expected original public Reddit post ID")
    grouped: dict[str, list[dict]] = {}
    for item in comments:
        body = item.get("body")
        handle = item.get("author")
        cid = str(item.get("id", ""))
        link = str(item.get("link_id", "")).removeprefix("t3_")
        if (not isinstance(body, str) or not isinstance(handle, str)
                or not HANDLE.fullmatch(handle) or not POST_ID.fullmatch(cid)
                or (link and link.lower() != post_id.lower())):
            continue
        claims = classify_body(body)
        if not claims:
            continue
        # Store the source-account pseudonym only to allow same-thread
        # reconciliation; NEVER query that handle across Reddit.
        excerpt = re.sub(r"\s+", " ", body)[:260]
        if "http" in excerpt.lower():
            excerpt = re.sub(r"https?://\S+", "[link]", excerpt)
        grouped.setdefault(handle.casefold(), []).append({
            "comment_id": cid,
            "comment_url": f"https://www.reddit.com/comments/{post_id}/_/{cid}/",
            "created_utc": item.get("created_utc"),
            "claim_types": claims,
            "context_excerpt": excerpt,
            "public_author": handle,
        })
    results = []
    for author_key, statements in sorted(grouped.items()):
        statements.sort(key=lambda c: (int(c["created_utc"] or 0), c["comment_id"]))
        types = {tag for c in statements for tag in c["claim_types"]}
        purchased_at = [c["created_utc"] for c in statements
                        if "purchase-asserted" in c["claim_types"]]
        reversed_at = [c["created_utc"] for c in statements
                       if "purchase-retracted" in c["claim_types"]]
        contradiction = bool(
            purchased_at and reversed_at
            and any((r or 0) >= (p or 0) for p in purchased_at for r in reversed_at)
        )
        if contradiction:
            classification = "same-thread-later-purchase-retraction-review"
        elif "receipt-asserted" in types:
            classification = "receipt-text-only-not-physical-sticker"
        elif "purchase-asserted" in types:
            classification = "purchase-text-only-no-receipt-confirmed"
        else:
            classification = "purchase-declined-or-cancelled"
        results.append({
            "public_author": statements[0]["public_author"],
            "classification": classification,
            "observed_statement_count": len(statements),
            "statements": statements,
            "physical_copy_confirmed": False,
            "sticker_serial_confirmed": False,
        })
    return {
        "schema_version": 1,
        "post_id": post_id,
        "public_thread_url": f"https://www.reddit.com/comments/{post_id}/",
        "possible_partial_archived_tree": truncated,
        "public_author_claim_groups": results,
        "summary": {
            "statement_groups": len(results),
            "later_purchase_retractions": sum(
                r["classification"] == "same-thread-later-purchase-retraction-review"
                for r in results),
        },
        "interpretation": "Observed statements only, not physical CE ownership or sticker confirmation; non-exhaustive archive.",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--post-id", required=True)
    p.add_argument("--max-comments", type=int, default=150)
    p.add_argument("--output", type=Path,
                   default=Path("visual-evidence-work/public-ce-thread-claim-audit.json"))
    args = p.parse_args()
    if not POST_ID.fullmatch(args.post_id) or not 1 <= args.max_comments <= 300:
        p.error("post-id must be 5-9 alphanumeric, max-comments 1..300")
    url = ("https://arctic-shift.photon-reddit.com/api/comments/tree"
           f"?link_id=t3_{args.post_id}&limit={args.max_comments}"
           "&start_breadth=100&start_depth=16")
    response, sha = request_json(url)
    comments, partial = iter_comments(response, max_nodes=args.max_comments)
    result = audit(comments, args.post_id, truncated=partial)
    result["archive_response_sha256"] = sha
    result["archived_comment_count"] = len(comments)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({"archived_comments": len(comments),
                      **result["summary"],
                      "possible_partial_tree": partial}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact public-handle crosscheck for INSIDE CE source leads.

No cross-platform identity linking. A same-platform handle match is a *review
signal*, never evidence that two physical CEs are identical or an owner consented.
Canonical data is a separately supplied, SHA-pinned public stickers.md.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, unquote

REDDIT_HOSTS = {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com"}
TWITTER_HOSTS = {"twitter.com", "www.twitter.com", "x.com", "www.x.com"}
FIELDS = ("source_url", "public_platform", "public_author", "canonical_handle_relation",
          "canonical_sticker_entries", "matched_public_handle", "source_evidence_status",
          "new_confirmed_stickers")

def user_handle(url):
    """Only extract explicit Reddit and X public user profile URLs."""
    try:
        p = urlsplit(url)
        if p.scheme not in ("http", "https"):
            return None
        host = p.hostname or ""
        path = unquote(p.path)
        if host in REDDIT_HOSTS:
            m = re.search(r"^/(?:user|u)/([A-Za-z0-9_-]{3,30})(?:/|$)", path, re.I)
            return ("reddit", m.group(1).casefold()) if m else None
        if host in TWITTER_HOSTS:
            m = re.search(r"^/([A-Za-z0-9_]{1,15})(?:/status/[0-9]+)?/?$", path, re.I)
            if m and m.group(1).lower() not in ("i", "intent", "share", "search", "home"):
                return ("twitter", m.group(1).casefold())
    except ValueError:
        pass
    return None

def find_explicit_handles(line):
    result=set()
    # Only explicitly marked platform handles, NEVER arbitrary proper names.
    for u in re.findall(r"https?://[^\s<>)\]]+", line):
        h=user_handle(u.rstrip(".,;"))
        if h:
            result.add(h)
    for match in re.finditer(r"\b(?:u/|Reddit user\s+)([A-Za-z0-9_-]{3,30})\b",line,re.I):
        result.add(("reddit",match.group(1).casefold()))
    # Known explicit prose prefix, not just any occurrence of "user".
    for match in re.finditer(r"\bResetEra user\s+([A-Za-z0-9_.-]{3,30})\b",line,re.I):
        result.add(("resetera",match.group(1).casefold()))
    return result

def canonical_index(markdown: str):
    """Map public handle to the particular sticker list entries that mention it."""
    idx=defaultdict(set)
    for line in markdown.splitlines():
        line=line.strip()
        if not line.startswith("- "):
            continue
        entry=re.match(r"^-\s+(?:\[([0-9]{3})\]|(L[0-9]{2,3}|U[0-9]{2,3}))",line)
        if not entry:
            continue
        sticker=entry.group(1) or entry.group(2)
        for handle in find_explicit_handles(line):
            idx[handle].add(sticker)
    return idx

def classify(source_url, platform, author, idx):
    """Cannot prove identity from a username; return a conservative flag."""
    platform=platform.casefold().strip()
    author=author.strip().lstrip("@")
    if platform not in ("reddit","twitter","resetera"):
        return ("platform_or_author_unverified", [], "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", author):
        return ("platform_or_author_unverified", [], "")
    key=(platform,author.casefold())
    if key not in idx:
        return ("no_exact_canonical_public_handle_match", [], "")
    return ("same_platform_handle_in_canonical_needs_review",sorted(idx[key]),author)

def annotate(records,canonical):
    idx=canonical_index(canonical)
    output=[]
    for row in records:
        url=str(row.get("source_url") or row.get("url") or "")
        platform=str(row.get("public_platform") or row.get("platform") or "")
        author=str(row.get("public_author") or row.get("author") or "")
        relation,stickers,match=classify(url,platform,author,idx)
        output.append({
            "source_url":url,
            "public_platform":platform,
            "public_author":author,
            "canonical_handle_relation":relation,
            "canonical_sticker_entries":";".join(stickers),
            "matched_public_handle":match,
            "source_evidence_status":"requires_original_post_and_canonical_reconciliation",
            "new_confirmed_stickers":0,
        })
    return output

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidates",type=Path,required=True)
    p.add_argument("--canonical-stickers",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--summary",type=Path,required=True)
    args=p.parse_args()
    markdown=args.canonical_stickers.read_bytes()
    with args.candidates.open(encoding="utf-8") as f:
        if args.candidates.suffix==".tsv":
            data=list(csv.DictReader(f,delimiter="\t"))
        else:
            data=[json.loads(x) for x in f if x.strip()]
    result=annotate(data,markdown.decode("utf-8"))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,delimiter="\t")
        writer.writeheader()
        for row in result:
            # Formula-safe TSV from untrusted site author strings.
            writer.writerow({k:"'"+str(v) if str(v).lstrip().startswith(("=","+","-","@")) else v
                             for k,v in row.items()})
    summary={
        "source_records":len(result),
        "public_canonical_handle_matches":sum(
            r["canonical_handle_relation"]=="same_platform_handle_in_canonical_needs_review"
            for r in result),
        "canonical_sha256":hashlib.sha256(markdown).hexdigest(),
        "new_confirmed_stickers":0,
        "note":"Same-platform public handle occurrence is contextual only. No identity or CE object equivalence proved."
    }
    args.summary.parent.mkdir(parents=True,exist_ok=True)
    args.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()

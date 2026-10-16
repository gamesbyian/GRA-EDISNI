#!/usr/bin/env python3
"""Bounded, source-first MediaWiki revision audit.

Read-only public research. Output flags are review candidates, never proof
of ARG intent or Playdead authorship.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

MARKERS = ("terminal41", "setrinamair", "hasty", "534brn9653f9j8mmd",
           "multipleprobesdispatched", "newplanetdiscovered", "lifedetected")
HIDDEN_RE = re.compile(r"<!--.*?-->", re.DOTALL)
URL_RE = re.compile(r"https?://[^\\s\\]<>|{}'\\\"]+", re.IGNORECASE)
STRANGE = {"Cf", "Cc"}
ALLOWED_CONTROLS = "\\r\\n\\t"


def revision_text(rev):
    """Support legacy MediaWiki, formatversion=2 and modern MCR content."""
    if isinstance(rev.get("content"), str):
        return rev["content"]
    if isinstance(rev.get("*"), str):
        return rev["*"]
    main = rev.get("slots", {}).get("main", {})
    for key in ("content", "*"):
        if isinstance(main.get(key), str):
            return main[key]
    raise ValueError("Revision content missing: cannot claim complete audit")


def api_get(endpoint, params, retries=3):
    url = endpoint + ("&" if "?" in endpoint else "?") + urllib.parse.urlencode(params)
    last = None
    for attempt in range(retries):
        request = urllib.request.Request(url, headers={
            "User-Agent": "GRA-EDISNI-WikiRevisionAudit/0.1 (public-history research)",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.loads(response.read(12_000_000).decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Could not retrieve {endpoint}: {last}")


def harvest(endpoint, title, max_revisions=2000, delay=1.0):
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.netloc or not parsed.path.endswith("/api.php"):
        raise ValueError("Endpoint must be a public HTTPS MediaWiki /api.php URL")
    base = {
        "action": "query", "prop": "revisions", "titles": title,
        "rvprop": "ids|timestamp|user|comment|size|content",
        "rvslots": "main", "rvlimit": "max", "rvdir": "newer",
        "format": "json", "formatversion": "2",
    }
    cursor = {}
    revisions = []
    seen = set()
    while True:
        data = api_get(endpoint, {**base, **cursor})
        if data.get("error"):
            raise RuntimeError(f"MediaWiki API failure: {data['error']}")
        pages = data.get("query", {}).get("pages", [])
        if len(pages) != 1 or pages[0].get("missing") is True:
            raise RuntimeError(f"Title not retrievable: {title}")
        for rev in pages[0].get("revisions", []):
            rid = rev.get("revid")
            if rid in seen:
                raise RuntimeError("Repeated revision ID across pages: pagination corrupt")
            seen.add(rid)
            rev["content"] = revision_text(rev)
            revisions.append(rev)
        cont = data.get("continue")
        if len(revisions) > max_revisions or (len(revisions) == max_revisions and cont):
            raise RuntimeError("Revision cap reached before cursor exhaustion: audit incomplete")
        if not cont:
            break
        cursor = cont
        time.sleep(delay)
    return {"site": parsed.netloc, "title": title,
            "retrieval": "MediaWiki revisions with exhausted continuation",
            "revisions": revisions}


def changed_lines(before, after):
    a = [line.strip() for line in before.splitlines() if line.strip()]
    b = [line.strip() for line in after.splitlines() if line.strip()]
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    added, deleted = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "insert"):
            added.extend(b[j1:j2])
        if tag in ("replace", "delete"):
            deleted.extend(a[i1:i2])
    return added, deleted


def delta_days(first, second):
    try:
        a = datetime.fromisoformat(first.replace("Z", "+00:00"))
        b = datetime.fromisoformat(second.replace("Z", "+00:00"))
        return (b - a).total_seconds() / 86400
    except (ValueError, TypeError):
        return None


def indicators(before, after, added):
    flags = []
    joined = "\\n".join(added)
    newly_hidden = set(HIDDEN_RE.findall(after)) - set(HIDDEN_RE.findall(before))
    if newly_hidden:
        flags.append({"kind": "added_html_comment", "examples": sorted(newly_hidden)[:3]})
    unusual = sorted(set(c for c in joined if
        ((unicodedata.category(c) in STRANGE and c not in ALLOWED_CONTROLS)
         or unicodedata.bidirectional(c) in {"RLO", "LRO", "RLE", "LRE", "PDF"})))
    if unusual:
        flags.append({"kind": "invisible_or_directional_unicode",
                      "codepoints": [f"U+{ord(c):04X}" for c in unusual]})
    added_urls = sorted(set(URL_RE.findall(joined)) - set(URL_RE.findall(before)))
    if added_urls:
        flags.append({"kind": "new_url", "examples": added_urls[:10]})
    mentioned = [marker for marker in MARKERS if marker in joined.lower()]
    if mentioned:
        flags.append({"kind": "predeclared_arg_marker", "markers": mentioned})
    return flags


def audit(dataset, transient_days=7):
    revisions = dataset["revisions"]
    if not isinstance(revisions, list) or not revisions:
        raise ValueError("No revisions: zero is not a successful audit")
    for rev in revisions:
        rev["content"] = revision_text(rev)
    if len({rev["revid"] for rev in revisions}) != len(revisions):
        raise ValueError("Duplicate revision identifiers")
    timestamps = [rev["timestamp"] for rev in revisions]
    if timestamps != sorted(timestamps):
        raise ValueError("Revisions must be oldest-first")
    events = []
    for i, rev in enumerate(revisions):
        before = revisions[i - 1]["content"] if i else ""
        added, removed = changed_lines(before, rev["content"])
        flags = indicators(before, rev["content"], added)
        if i:
            for j in range(i + 1, len(revisions)):
                days = delta_days(rev["timestamp"], revisions[j]["timestamp"])
                if days is None or days > transient_days:
                    break
                later_added, later_removed = changed_lines(
                    revisions[j - 1]["content"], revisions[j]["content"])
                reverted = sorted(set(added) & set(later_removed))
                if reverted:
                    flags.append({"kind": "short_lived_added_lines",
                                  "removed_by": revisions[j]["revid"],
                                  "days": round(days, 3), "examples": reverted[:5]})
                    break
        if flags:
            events.append({"revid": rev["revid"], "timestamp": rev["timestamp"],
                           "user": rev.get("user"), "comment": rev.get("comment", ""),
                           "added_lines": len(added), "removed_lines": len(removed),
                           "indicators": flags})
    return {"site": dataset.get("site"), "title": dataset.get("title"),
            "revision_count": len(revisions), "first_revision": timestamps[0],
            "last_revision": timestamps[-1], "finding_count": len(events),
            "flag_type_counts": dict(Counter(flag["kind"]
                for event in events for flag in event["indicators"])),
            "events": events, "assessment": "Anomaly candidates only; no ownership attribution"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", type=Path, help="Offline revision dataset JSON")
    source.add_argument("--endpoint", help="Public HTTPS MediaWiki API endpoint")
    parser.add_argument("--title", help="Wiki page title (required with endpoint)")
    parser.add_argument("--max-revisions", type=int, default=2000)
    parser.add_argument("--transient-days", type=float, default=7)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--raw-output", type=Path)
    args = parser.parse_args()
    if args.endpoint and not args.title:
        parser.error("--title required with --endpoint")
    if args.max_revisions < 1 or args.transient_days < 0:
        parser.error("Bounds must be nonnegative; at least one revision required")
    try:
        dataset = (json.loads(args.fixture.read_text(encoding="utf-8"))
                   if args.fixture else harvest(args.endpoint, args.title, args.max_revisions))
        result = audit(dataset, args.transient_days)
        if args.raw_output:
            args.raw_output.write_text(
                json.dumps(dataset, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

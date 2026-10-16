#!/usr/bin/env python3
"""Extract image-bearing leads from already acquired public HTML, without fetching them."""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

KEYWORDS = ("inside", "playdead", "iam8bit", "real doll", "realdoll", "huddle",
            "collector", "collectible", "unbox", "sticker", "limited")
NON_IMAGE_URLS = ("gravatar.com", "google-analytics.com", "doubleclick.net")


def normal_url(base: str, candidate: str) -> str:
    candidate = html.unescape(candidate.strip())
    if not candidate or candidate.startswith(("data:", "blob:", "javascript:", "#")):
        return ""
    url = urldefrag(urljoin(base, candidate))[0]
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return ""
    if parsed.hostname.lower().endswith(NON_IMAGE_URLS):
        return ""
    return url


class ImageHTMLParser(HTMLParser):
    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.urls: dict[str, set[str]] = {}

    def insert(self, candidate: str, context: str) -> None:
        u = normal_url(self.base, candidate)
        if u:
            self.urls.setdefault(u, set()).add(context[:250])

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        description = " ".join(str(attr.get(k) or "") for k in ("alt", "title", "aria-label"))
        if tag == "meta" and (attr.get("property") in {"og:image", "og:image:url",
                "twitter:image"} or attr.get("name") in {"twitter:image"}):
            if attr.get("content"):
                self.insert(attr["content"], f"meta {attr.get('property') or attr.get('name')}")
        if tag == "link" and ("image_src" in (attr.get("rel") or "")
                or (attr.get("as") or "") == "image"):
            if attr.get("href"):
                self.insert(attr["href"], f"link {description}")
        if tag in {"img", "source"}:
            for key in ("src", "data-src", "data-original", "data-lazy-src", "data-image"):
                if attr.get(key):
                    self.insert(attr[key], f"{tag}:{key} {description}")
            for key in ("srcset", "data-srcset"):
                if attr.get(key):
                    for part in attr[key].split(","):
                        candidate = part.strip().split(" ")[0]
                        if candidate:
                            self.insert(candidate, f"{tag}:{key} {description}")


def extract(html_body: str, page_url: str) -> list[dict]:
    parser = ImageHTMLParser(page_url)
    parser.feed(html_body)
    result = []
    for url, contexts in sorted(parser.urls.items()):
        evidence = " ".join(sorted(contexts))
        hits = sorted({term for term in KEYWORDS if term in (url + " " + evidence).lower()})
        result.append({"image_url": url, "contexts": sorted(contexts),
                       "keyword_hints": hits, "hint_count": len(hits),
                       "review_status": "unfetched-and-unverified"})
    result.sort(key=lambda r: (-r["hint_count"], r["image_url"]))
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--acquired", type=Path, default=Path("evidence-work"))
    p.add_argument("--output", type=Path, default=Path("visual-evidence-work/html-image-leads.json"))
    p.add_argument("--max-html-bytes", type=int, default=10_000_000)
    args = p.parse_args()
    all_results = []
    coverage = {"source_metadata_files": 0, "invalid_metadata_files": 0,
                "metadata_without_public_url": 0,
                "html_pages_seen": 0, "oversized_html_pages": 0,
                "readable_html_pages": 0, "html_pages_with_image_urls": 0,
                "html_pages_without_image_urls": 0}
    for metadata in sorted(args.acquired.glob("*/acquisition.json")):
        coverage["source_metadata_files"] += 1
        try:
            rec = json.loads(metadata.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            coverage["invalid_metadata_files"] += 1
            continue
        url = rec.get("final_url") or rec.get("url") or ""
        if not url.startswith(("http://", "https://")):
            coverage["metadata_without_public_url"] += 1
            continue
        for page in sorted(metadata.parent.rglob("*.html")):
            coverage["html_pages_seen"] += 1
            if page.stat().st_size > args.max_html_bytes:
                coverage["oversized_html_pages"] += 1
                continue
            leads = extract(page.read_text(encoding="utf-8", errors="replace"), url)
            coverage["readable_html_pages"] += 1
            coverage["html_pages_with_image_urls" if leads else
                     "html_pages_without_image_urls"] += 1
            for lead in leads:
                lead["source_id"] = rec.get("source_id") or metadata.parent.name
                lead["source_page_url"] = url
                lead["source_local_path"] = str(page.relative_to(args.acquired))
            all_results.extend(leads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "schema_version": 1, "source_type": "acquired-public-html",
        "interpretation": "candidate image URLs only; not retrieved, owned, or readable stickers",
        "source_coverage": coverage,
        "unscanned_or_skipped_html": coverage["oversized_html_pages"] +
                                      coverage["invalid_metadata_files"] +
                                      coverage["metadata_without_public_url"],
        "image_mentions": all_results
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"extracted {len(all_results)} public HTML image mentions; none fetched")


if __name__ == "__main__":
    main()

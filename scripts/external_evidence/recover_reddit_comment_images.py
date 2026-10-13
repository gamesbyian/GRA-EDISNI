#!/usr/bin/env python3
"""Recover bounded public Reddit comment image links from named archival threads.

Uses official documented Arctic Shift comments/tree API for exact public post IDs
and PullPush's comment search as fallback. Archives can be incomplete or stale.
Never promotes a retrieved link or historical comment into a sticker observation.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from urllib.parse import urlparse

POST_ID = re.compile(r"/comments/([0-9a-z]+)/", re.IGNORECASE)
LINK_RE = re.compile(r"https?://[^\s\[\]()<>\"']+", re.IGNORECASE)
IMAGE_HINT = re.compile(r"sticker|serial|number|collect|unbox|photo|picture|image|receipt|box|"
                        r"包装|贴纸|写真|限定|シール|사진|스티커|номер|наклейк|foto|"
                        r"imagem|imagen|coleccion|edición|edição", re.IGNORECASE)
ARCHIVE_HOSTS = {"arctic-shift.photon-reddit.com", "api.pullpush.io"}
PREFERRED_MEDIA_HOSTS = {"i.redd.it", "preview.redd.it", "i.imgur.com", "pbs.twimg.com",
                         "i.ebayimg.com"}
RELATED_GALLERY_HOSTS = {"imgur.com", "www.imgur.com", "flickr.com", "www.flickr.com",
                         "ibb.co", "postimg.cc", "photos.app.goo.gl", "www.instagram.com"}
MAX_ARCHIVE_BYTES = 8 * 1024 * 1024


class ConstrainedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = urlparse(newurl)
        if u.scheme != "https" or u.hostname not in ARCHIVE_HOSTS:
            raise ValueError("Unapproved archive API redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request_json(url: str) -> tuple[object, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ARCHIVE_HOSTS:
        raise ValueError("Archive API host not allowlisted")
    req = urllib.request.Request(url, headers={
        "User-Agent": "GRA-EDISNI-CE-public-comment-evidence/1.0",
        "Accept": "application/json",
    })
    with urllib.request.build_opener(ConstrainedRedirect()).open(req, timeout=30) as response:
        if response.headers.get_content_type() != "application/json":
            raise ValueError("Unexpected archive content type")
        payload = response.read(MAX_ARCHIVE_BYTES + 1)
        if not 0 < len(payload) <= MAX_ARCHIVE_BYTES:
            raise ValueError("Unbounded or empty archive JSON")
        return json.loads(payload), hashlib.sha256(payload).hexdigest()


def arctic_tree_url(post_id: str, max_comments: int) -> str:
    if not re.fullmatch(r"[a-z0-9]{5,9}", post_id, re.IGNORECASE):
        raise ValueError("Invalid public post ID")
    q = urllib.parse.urlencode({
        "link_id": "t3_" + post_id, "limit": max_comments,
        "start_breadth": 100, "start_depth": 16,
    })
    return "https://arctic-shift.photon-reddit.com/api/comments/tree?" + q


def pullpush_url(post_id: str) -> str:
    if not re.fullmatch(r"[a-z0-9]{5,9}", post_id, re.IGNORECASE):
        raise ValueError("Invalid public post ID")
    return "https://api.pullpush.io/reddit/search/comment/?link_id=" + post_id + "&size=100"


def iter_comments(obj: object, *, max_nodes: int) -> tuple[list[dict], bool]:
    """Support nested Reddit-style tree and flat 'data' arrays without recursion."""
    pending = [obj]
    visited = 0
    found: dict[str, dict] = {}
    collapsed = False
    while pending:
        node = pending.pop()
        visited += 1
        if visited > max_nodes * 25:
            collapsed = True
            break
        if isinstance(node, list):
            pending.extend(reversed(node))
            continue
        if not isinstance(node, dict):
            continue
        if node.get("kind") == "more":
            collapsed = True
            continue
        data = node.get("data")
        if isinstance(data, (dict, list)):
            pending.append(data)
        if isinstance(node.get("children"), (dict, list)):
            pending.append(node["children"])
        if isinstance(node.get("replies"), (dict, list)):
            pending.append(node["replies"])
        cid = node.get("id")
        body = node.get("body")
        if isinstance(cid, str) and isinstance(body, str):
            if re.fullmatch(r"[a-z0-9]{4,12}", cid, re.IGNORECASE):
                found[cid] = node
                if len(found) >= max_nodes:
                    collapsed = True
                    break
    return list(found.values()), collapsed


def collect_comment_links(post_id: str, source: dict, comments: list[dict]) -> tuple[list[dict], list[dict]]:
    media, galleries = [], []
    for comment in comments:
        body = comment.get("body", "")
        if not isinstance(body, str) or body.strip().lower() in {"[deleted]", "[removed]"}:
            continue
        cid = comment.get("id", "")
        if not re.fullmatch(r"[a-z0-9]{4,12}", cid, re.IGNORECASE):
            continue
        l_id = str(comment.get("link_id", ""))
        if l_id and l_id.lower().removeprefix("t3_") != post_id:
            continue
        context = re.sub(r"\s+", " ", body)[:240]
        comment_page = f"https://www.reddit.com/comments/{post_id}/_/{cid}/"
        seen = set()
        for raw in LINK_RE.findall(html.unescape(body)):
            url = raw.rstrip(".,!?:;}>").replace("&amp;", "&")
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.hostname:
                continue
            host = parsed.hostname.lower()
            if url in seen:
                continue
            seen.add(url)
            record = {
                "source_id": source["id"], "source_page_url": comment_page,
                "thread_url": source["url"], "comment_id": cid,
                "created_utc": comment.get("created_utc"),
                "image_url": url, "contexts": [context],
                "keyword_hints": ["sticker-or-CE-context"] if IMAGE_HINT.search(context) else [],
                "hint_count": 1 if IMAGE_HINT.search(context) else 0,
                "review_status": "archived-comment-url-not-verified",
            }
            if host in PREFERRED_MEDIA_HOSTS:
                media.append(record)
            elif host in RELATED_GALLERY_HOSTS:
                record["classification"] = "gallery-or-login-needed-manual-review"
                galleries.append(record)
    media.sort(key=lambda o: (o["source_id"], o["comment_id"], o["image_url"]))
    galleries.sort(key=lambda o: (o["source_id"], o["comment_id"], o["image_url"]))
    return media, galleries


def scan(sources: list[dict], requester=request_json, max_comments: int = 600):
    reports, media, galleries = [], [], []
    for source in sources:
        url = source.get("url", "")
        match = POST_ID.search(url)
        if not match or "reddit.com" not in (urlparse(url).hostname or ""):
            continue
        post_id = match.group(1)
        report = {"source_id": source["id"], "post_id": post_id, "thread_url": url,
                  "status": "unavailable", "attempts": []}
        for provider, endpoint in [
            ("arctic-shift-comments-tree", arctic_tree_url(post_id, max_comments)),
            ("pullpush-comments-search-first-page", pullpush_url(post_id)),
        ]:
            try:
                payload, digest = requester(endpoint)
                comments, truncated = iter_comments(payload, max_nodes=max_comments)
                if not comments:
                    report["attempts"].append({"provider": provider, "status": "no-comments"})
                    continue
                found, manual = collect_comment_links(post_id, source, comments)
                media.extend(found)
                galleries.extend(manual)
                report.update({"status": "archived-comments-available", "provider": provider,
                               "archive_sha256": digest, "comments_returned": len(comments),
                               "possible_partial_tree": truncated or provider.startswith("pullpush"),
                               "direct_image_urls": len(found), "gallery_links": len(manual)})
                break
            except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
                report["attempts"].append({"provider": provider, "status": "failed",
                                           "error": str(exc)[:220]})
        reports.append(report)
    return reports, media, galleries


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/reference/inside-ce-visual-historical-pages.json"))
    p.add_argument("--out", type=Path, default=Path("visual-evidence-work"))
    p.add_argument("--max-comments", type=int, default=600)
    args = p.parse_args()
    if not 1 <= args.max_comments <= 2000:
        p.error("--max-comments must be 1..2000")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    reports, media, galleries = scan(manifest, max_comments=args.max_comments)
    args.out.mkdir(parents=True, exist_ok=True)
    for filename, payload in [
        ("reddit-comment-archive-report.json", {"schema_version": 1, "sources": reports}),
        ("reddit-comment-photo-links.json", {"schema_version": 1, "image_mentions": media}),
        ("reddit-comment-gallery-review.json", {"schema_version": 1, "gallery_links": galleries}),
    ]:
        (args.out / filename).write_text(json.dumps(payload, indent=2,
             ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"archived threads: {len(reports)}, direct photo links: {len(media)}, "
          f"manual gallery links: {len(galleries)}")


if __name__ == "__main__":
    main()

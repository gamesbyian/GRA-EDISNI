#!/usr/bin/env python3
"""Bounded one-record Wayback capture-body test for a witnessed GameFAQs URL.

Original URL and timestamp are frozen to previously observed CDX metadata.
No historical forum crawling, redirects, retries, external credentials or
bulk content retention. Output is a small evidence/status report only.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

ORIGINAL = "https://gamefaqs.gamespot.com/boards/194097-inside/76386967"
CAPTURE = "20190306051337"
REPLAY = f"https://web.archive.org/web/{CAPTURE}id_/{ORIGINAL}"
MAX_BYTES = 1_500_000
KEYWORDS = ("inside", "iam8bit", "playdead", "collector", "realdoll", "sticker")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

class TextOnly(HTMLParser):
    BLOCKED = {"script", "style", "noscript", "svg", "template"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCKED:
            self.hidden += 1
        if tag in {"p", "article", "div", "br", "li", "blockquote"}:
            self.parts.append(" ")
    def handle_endtag(self, tag):
        if tag in self.BLOCKED and self.hidden:
            self.hidden -= 1
        if tag in {"p", "article", "div", "br", "li", "blockquote"}:
            self.parts.append(" ")
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)
    def text(self):
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()

def summarize_html(raw: bytes) -> dict:
    body = raw.decode("utf-8", errors="replace")
    parser = TextOnly()
    parser.feed(body)
    text = parser.text()
    matches = []
    for term in KEYWORDS:
        for m in list(re.finditer(re.escape(term), text, flags=re.I))[:2]:
            snippet = text[max(0, m.start() - 65):m.end() + 95]
            if snippet not in matches:
                matches.append(snippet)
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "html_bytes": len(raw),
        "extracted_text_characters": len(text),
        "keyword_snippets": matches[:10],
        "body_classification": "replay_response_not_necessarily_original_forum_posts",
    }

def probe(*, execute: bool = False, opener=None) -> dict:
    result = {
        "original_url": ORIGINAL, "wayback_capture_timestamp": CAPTURE,
        "wayback_replay_url": REPLAY,
        "source_cdx_run_id": 38441436347,
        "source_cdx_digest": "MHNUGWQN4H3TEOTD2U3ZFVLWYUZJHLTC",
        "capture_body_state": "planned_unexecuted" if not execute else "request_started",
        "retrieval_scope": "one_verified_public_html_snapshot_only",
        "new_confirmed_stickers": 0,
    }
    if not execute:
        return result
    if opener is None:
        opener = urllib.request.build_opener(NoRedirect()).open
    try:
        req = urllib.request.Request(
            REPLAY, headers={
                "Accept": "text/html",
                "User-Agent": "GRA-EDISNI-historical-source-review/1.0",
            },
        )
        with opener(req, timeout=25) as response:
            status = response.getcode()
            mime = response.headers.get("Content-Type", "")
            result["http_status"] = status
            result["http_content_type"] = mime[:160]
            if status != 200 or "html" not in mime.lower():
                result["capture_body_state"] = "unexpected_response"
                return result
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            result["capture_body_state"] = "size_limit_exceeded_no_body_saved"
            return result
        result.update(summarize_html(raw))
        result["capture_body_state"] = "html_body_retrieved"
    except urllib.error.HTTPError as exc:
        result["capture_body_state"] = "http_error"
        result["http_status"] = exc.code
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        result["capture_body_state"] = "request_error"
        result["error_type"] = type(exc).__name__
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = probe(execute=args.execute)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "state": result["capture_body_state"],
        "original_url": ORIGINAL,
        "capture_timestamp": CAPTURE,
        "text_bytes": result.get("html_bytes"),
        "keyword_snippet_count": len(result.get("keyword_snippets", [])),
        "status": result.get("http_status"),
    }))

if __name__ == "__main__":
    main()

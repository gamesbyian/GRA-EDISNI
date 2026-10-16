#!/usr/bin/env python3
"""Inspect every preserved Terminal41 text page for genuine HTML-side receivers.

The frozen external source manifest is the sampling frame. No live requests,
new sticker retrieval, password trials, image decoding or guessed routes.
This is a client-source census, NOT a proof about missing historic backends.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/terminal41-source-tree.json"
BASE = ROOT / "archive/external/twinysam-inside-arg"
URL_ROOT = "http://terminal41.link/"
CONTROL_TAGS = {"form", "input", "textarea", "select", "button", "option"}
EXEC_ATTRS = {"onclick", "onsubmit", "onchange", "onkeydown", "onkeyup", "onkeypress", "onload"}
OBSERVED_ANCHOR = {
    "terminal41.link/comms_main_viewgate.html",
    "terminal41.link/comms_main_viewgate_002.html",
}
TARGET_RE = re.compile(r"""(?i)\b(?:https?://[^\s'"<>\\]+|(?:\.\./|/)?(?:sys|dat|loadSys|comms)/[A-Za-z0-9_./\-\[\]]{3,})""")
REFRESH_RE = re.compile(r"(?i)(?:^|;)\s*url\s*=\s*['\"]?([^;\s'\"]+)")
CALL_RE = re.compile(r"\b(?:fetch|XMLHttpRequest|sendBeacon|location\.(?:assign|replace)|window\.open)\s*\(", re.I)

class MarkupInspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.controls = Counter()
        self.method_form = []
        self.script_srcs = []
        self.inline_script_chars = 0
        self._script_depth = 0
        self.execute_attrs = Counter()
        self.submit_attrs = []
        self.anchors = []
        self.meta_redirects = []
        self.srcs = []
        self.inline_js_parts = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in CONTROL_TAGS:
            self.controls[tag] += 1
            if tag == "form":
                self.method_form.append({
                    "method": d.get("method", "GET").upper(),
                    "action": d.get("action", ""),
                })
            if tag in {"input", "button", "select", "textarea"} and "formaction" in d:
                self.submit_attrs.append(d["formaction"])
        for a, v in attrs:
            if a in EXEC_ATTRS or a.startswith("on"):
                self.execute_attrs[a] += 1
            if a in {"href", "src", "action", "formaction"} and isinstance(v, str) and v.lower().startswith("javascript:"):
                self.execute_attrs["javascript_url"] += 1
        if tag == "script":
            if d.get("src"):
                self.script_srcs.append(d["src"])
            self._script_depth += 1
        if tag == "a" and d.get("href"):
            self.anchors.append(d["href"])
        if tag in ("img","iframe","object","embed") and d.get("src"):
            self.srcs.append(d["src"])
        if tag == "meta" and d.get("http-equiv", "").lower() == "refresh":
            m = REFRESH_RE.search(d.get("content",""))
            if m:
                self.meta_redirects.append(m.group(1))

    def handle_endtag(self, tag):
        if tag == "script":
            self._script_depth = max(0, self._script_depth - 1)

    def handle_data(self, data):
        if self._script_depth:
            self.inline_script_chars += len(data)
            self.inline_js_parts.append(data)


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def classify_link(src: str, href: str, manifest_paths: set[str]) -> dict:
    link = urljoin(URL_ROOT + src.removeprefix("terminal41.link/"), href)
    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"}:
        return {"raw": href, "kind": "other_scheme"}
    if parsed.hostname not in {"terminal41.link","www.terminal41.link"}:
        return {"raw": href, "kind": "external"}
    route = unquote(parsed.path).lstrip("/")
    potential = ["terminal41.link/" + route]
    if not route or route.endswith("/"):
        potential.append("terminal41.link/" + route + "index.html")
    # Historical extensionless URL paths are not assumed to resolve.
    on_disk = next((p for p in potential if p in manifest_paths), None)
    return {
        "raw": href, "kind": "captured_internal" if on_disk else "uncaptured_internal",
        "url_path": "/" + route, "manifest_path": on_disk,
    }


def inspect() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["count"] == len(manifest["files"]) == 74
    entries = [x for x in manifest["files"] if x["media_class"] != "binary-media"]
    all_paths = {x["path"] for x in manifest["files"]}
    pages = []
    for e in sorted(entries, key=lambda x: x["path"]):
        path = BASE / e["path"]
        if not path.is_file():
            raise AssertionError(f"missing original source file: {path}")
        raw = path.read_bytes()
        correct_size = len(raw) == e["size_bytes"]
        correct_blob = blob_sha(raw) == e["blob_sha"]
        txt = raw.decode("utf-8", errors="replace")
        h = MarkupInspector()
        # .txt files are preserved source bytes but should not
        # arbitrarily be recast as executable HTML.
        html_like = path.suffix.lower() in {".html", ".htm"}
        if html_like:
            h.feed(txt)
            h.close()
        link_out = [
            classify_link(e["path"], href, all_paths)
            for href in h.anchors + h.meta_redirects
        ]
        candidate_literals = sorted(set(x.rstrip(".,;)]") for x in TARGET_RE.findall(txt)))
        inline_code = "\n".join(h.inline_js_parts)
        p = {
            "path": e["path"],
            "bytes": len(raw),
            "manifest_size_matches": correct_size,
            "manifest_git_blob_matches": correct_blob,
            "file_format": "html" if html_like else "text",
            "controls": dict(sorted(h.controls.items())),
            "form_destinations": h.method_form,
            "formaction_destinations": h.submit_attrs,
            "script_srcs": sorted(set(h.script_srcs)),
            "inline_script_chars": h.inline_script_chars,
            "inline_request_api_reference": bool(CALL_RE.search(inline_code)),
            "event_handlers": dict(sorted(h.execute_attrs.items())),
            "anchors": h.anchors,
            "meta_redirects": h.meta_redirects,
            "link_analysis": link_out,
            "textual_route_reference_count": len(candidate_literals),
            # "Text references" can be pasted URLs, lore, or ASCII art.
            # They are never promoted to working receivers.
            "textual_route_references_sample": candidate_literals[:8],
            "printed_input_literal": bool(re.search(r"Input:\s*\[", txt, re.I)),
            "text_fingerprint_sha256": hashlib.sha256(raw).hexdigest(),
        }
        pages.append(p)

    counts = Counter()
    for p in pages:
        counts["html_pages" if p["file_format"] == "html" else "text_files"] += 1
        counts["size_match"] += int(p["manifest_size_matches"])
        counts["blob_match"] += int(p["manifest_git_blob_matches"])
        counts["native_form_pages"] += int(bool(p["controls"].get("form")))
        counts["form_control_pages"] += int(bool(set(p["controls"]) & (CONTROL_TAGS - {"option"})))
        counts["executable_js_page"] += int(bool(p["inline_script_chars"] or p["script_srcs"] or p["event_handlers"]))
        counts["inline_request_api_pages"] += int(p["inline_request_api_reference"])
        counts["printed_input_literal_pages"] += int(p["printed_input_literal"])
        counts["anchor_pages"] += int(bool(p["anchors"]))
        counts["meta_redirect_pages"] += int(bool(p["meta_redirects"]))
        for link in p["link_analysis"]:
            counts["links_"+link["kind"]] += 1
    assert len(pages) == 73
    return {
        "mode": "VALIDATE_preserved_client_snapshot_ONLY",
        "source_ref": manifest["source_ref"],
        "source_tree_sha": manifest["source_tree_sha"],
        "total_source_manifest_files": manifest["count"],
        "inspected_text_sources": len(pages),
        "excluded_binary_media": sorted(all_paths-{p["path"] for p in pages}),
        "summary": dict(sorted(counts.items())),
        "pages": pages,
        "scope_caveat": (
            "No client-side control in this fixed mirror never proves the "
            "original historical server never accepted a query, URL route, "
            "POST, cookie or side-channel. Archive canonical URLs, literal "
            "ASCII input and internal links are not executable inputs."
        ),
    }


def self_test():
    h = MarkupInspector()
    h.feed("<pre>Input: [_____]</pre><form action='/x' method='post'><input name='a'>"
           "<button onclick='go()'>Go</button></form>"
           "<meta http-equiv='refresh' content='0; url=foo.html'>")
    assert h.controls == Counter({"form":1, "input":1, "button":1})
    assert h.method_form == [{"method": "POST", "action": "/x"}]
    assert h.meta_redirects == ["foo.html"]
    assert h.execute_attrs["onclick"] == 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--summary", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    self_test()
    result = inspect()
    if a.check:
        assert all(p["manifest_size_matches"] and p["manifest_git_blob_matches"] for p in result["pages"]), (
            "source mirror drifted from its original manifest; inspect before making negative claims")
        for name in OBSERVED_ANCHOR:
            item = next(p for p in result["pages"] if p["path"] == name)
            assert item["printed_input_literal"] and not item["controls"] and not item["event_handlers"]
        print("PASS: 73 text pages in pinned 74-file source manifest; direct Viewgate placeholders are not HTML controls.")
    if a.summary:
        print(json.dumps(result["summary"], sort_keys=True, indent=2))
        print("PAGES WITH CONTROLS / EXECUTABLE JS / EVENT HANDLERS:")
        for item in result["pages"]:
            if item["controls"] or item["script_srcs"] or item["event_handlers"] or item["inline_script_chars"]:
                print(item["path"], item["controls"], item["script_srcs"],
                      item["event_handlers"], item["inline_script_chars"])
        print("UNCAPTURED INTERNAL LINK EDGES:")
        for item in result["pages"]:
            for edge in item["link_analysis"]:
                if edge["kind"] == "uncaptured_internal":
                    print(item["path"], "->", edge["raw"], edge["url_path"])
    if a.json or not (a.check or a.summary):
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

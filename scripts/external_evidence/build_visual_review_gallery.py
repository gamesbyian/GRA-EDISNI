#!/usr/bin/env python3
"""Offline self-contained CE visual-review gallery, NOT sticker verification.

Consume outputs of visual_index.py; embed bounded thumbnails of already acquired
public/approved local files. No network, tracking, JavaScript or OCR. Every
candidate remains evidence-unverified, regardless of a perceptual match.
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, ImageOps, UnidentifiedImageError

MAX_PIXELS = 40_000_000
MAX_ITEMS = 200
MAX_THUMB_SIDE = 300
ROLE_ORDER = {
    "known-sticker-photo": 0,
    "historical-owner-photo-no-visible-sticker": 1,
    "standalone-product-reference": 2,
    "promotional-reference": 3,
}
KIND_ORDER = {"byte-identical": 0, "whole-image-similar": 1, "possible-cropped-repost": 2}


def original_link(url: str) -> str:
    """Only allow explicitly normal HTTPS source hyperlinks in a local report."""
    try:
        u = urlsplit(url or "")
        if u.scheme == "https" and u.hostname and not (u.username or u.password):
            return html.escape(url, quote=True)
    except (ValueError, TypeError):
        pass
    return ""


def source_label(item: dict) -> str:
    """Source identity is an acquisition grouping, NOT the collector's identity."""
    return str(item.get("source_kind") or item.get("source_url") or "unknown-source")


def match_by_candidate(data: dict) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for match in data.get("matches", []):
        if isinstance(match, dict) and match.get("candidate_id"):
            groups[str(match["candidate_id"])].append(match)
    for key in groups:
        groups[key].sort(key=lambda r: (
            ROLE_ORDER.get(r.get("reference_role"), 99),
            KIND_ORDER.get(r.get("kind"), 99),
            int(r.get("dhash_distance") or 0) + int(r.get("ahash_distance") or 0),
            str(r.get("reference_id", "")),
        ))
    return groups


def select_for_review(items: list[dict], matches: dict, limit: int) -> list[dict]:
    """Diverse first-pass review; include unmatched examples to audit recall."""
    if not 1 <= limit <= MAX_ITEMS:
        raise ValueError("review limit outside supported bounds")
    seen = set()
    groups = defaultdict(list)
    for item in items:
        ident = str(item.get("id") or "")
        if not ident or ident in seen:
            raise ValueError("missing or duplicate candidate ID")
        seen.add(ident)
        groups[source_label(item)].append(item)
    for key in groups:
        groups[key].sort(key=lambda item: (
            not bool(matches.get(item["id"])),  # similarities first, not only similarities
            item["id"],
        ))
    ordered_keys = sorted(groups, key=lambda k: (
        not any(matches.get(x["id"]) for x in groups[k]), k
    ))
    chosen = []
    for depth in range(max(map(len, groups.values()), default=0)):
        for key in ordered_keys:
            if depth < len(groups[key]):
                chosen.append(groups[key][depth])
                if len(chosen) >= limit:
                    return chosen
    return chosen


def thumbnail(path: Path) -> str:
    with Image.open(path) as raw:
        if raw.width * raw.height > MAX_PIXELS:
            raise ValueError("oversized image")
        image = ImageOps.exif_transpose(raw)
        image.thumbnail((MAX_THUMB_SIDE, MAX_THUMB_SIDE), Image.Resampling.LANCZOS)
        image = image.convert("RGB")
        out = io.BytesIO()
        image.save(out, format="JPEG", quality=68, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(out.getvalue()).decode("ascii")


def safe_candidate_path(root: Path, relative: str) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        return None
    candidate = (root / relative).resolve()
    return candidate if candidate.is_relative_to(root.resolve()) and candidate.is_file() else None


def render(index: dict, visual: dict, root: Path, max_items: int = 48) -> tuple[str, dict]:
    items = index.get("candidates", [])
    if not isinstance(items, list):
        raise ValueError("candidate index must contain an array")
    matchmap = match_by_candidate(visual)
    selected = select_for_review(items, matchmap, max_items)
    source_count = len({source_label(x) for x in selected})
    cards = []
    errors = []
    for item in selected:
        ident = str(item["id"])
        path = safe_candidate_path(root, item.get("path", ""))
        try:
            if path is None:
                raise ValueError("source media missing or outside candidate root")
            embedded = thumbnail(path)
            photo = f'<img src="{embedded}" alt="Public image candidate {html.escape(ident, quote=True)}" loading="lazy">'
        except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
            errors.append({"candidate_id": ident, "error": str(exc)[:150]})
            photo = '<div class="missing">Original candidate image unavailable or unsafe</div>'
        source = original_link(item.get("source_url", ""))
        media = original_link(item.get("image_url", ""))
        source_html = f'<a href="{source}" rel="noreferrer noopener">Original public source</a>' if source else "No verified HTTPS source link"
        media_html = f'<a href="{media}" rel="noreferrer noopener">Original media URL</a>' if media else ""
        matches = matchmap.get(ident, [])
        descriptions = []
        for match in matches[:5]:
            role = html.escape(str(match.get("reference_role", "unknown")))
            title = html.escape(str(match.get("reference_id", "")))
            kind = html.escape(str(match.get("kind", "possible match")))
            case = html.escape(str(match.get("reference_canonical_case") or ""))
            suffix = f" · Known case {case}" if case else ""
            descriptions.append(f'<li>{role}: {title} ({kind}){suffix}</li>')
        summary = "<ul>" + "".join(descriptions) + "</ul>" if descriptions else "<p>No hash match among retained references. This does not imply a new CE.</p>"
        source_tag = html.escape(source_label(item))
        ident_tag = html.escape(ident)
        sha = html.escape(str(item.get("sha256", ""))[:16])
        cards.append(f'''<article class="card">
  {photo}
  <div class="body"><h2>{ident_tag}</h2>
  <p class="meta">Source batch: {source_tag}</p>
  <p class="links">{source_html} · {media_html}</p>
  <p class="meta">Local image digest prefix: {sha}</p>
  <h3>Review-only similarity</h3>{summary}
  <p class="status">UNREVIEWED · no sticker verified</p></div>
</article>''')
    styles = """
body{font:15px/1.5 system-ui,sans-serif;margin:2rem auto;padding:0 1rem;max-width:1500px;background:#f4f4f4;color:#191919}
header{max-width:900px;margin-bottom:2rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:1rem}
.card{background:white;border:1px solid #ccc;border-radius:10px;overflow:hidden;min-width:0}
.card img{display:block;width:100%;height:250px;object-fit:contain;background:#ddd}
.card .body{padding:1rem}.card h2{font-size:1.05rem;margin:0}.card h3{font-size:.9rem}
.meta{color:#505050;overflow-wrap:anywhere}.links{overflow-wrap:anywhere}
.status{font-weight:bold;font-size:.8rem;color:#8a4400}.missing{padding:3rem 1rem;background:#e8e8e8}
ul{padding-left:1.3rem}li{margin-bottom:.3rem}a{color:#124f9b}"""
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline';">
<title>INSIDE CE public-image review</title><style>{styles}</style></head><body>
<header><h1>INSIDE CE public-image review</h1>
<p>Offline, source-first, review-only gallery. Candidate photographs and similarity scores never verify sticker numbers or distinct collectors.</p>
<p>{len(selected)} of {len(items)} indexed candidates shown, from {source_count} source groups. No external image or script request is made.</p>
</header><main class="cards">{"".join(cards)}</main></body></html>'''
    summary = {
        "schema_version": 1,
        "indexed_candidates": len(items),
        "selected_for_review": len(selected),
        "excluded_by_review_limit": len(items) - len(selected),
        "represented_source_groups": source_count,
        "unavailable_or_unsafe_thumbnails": errors,
        "selected_candidate_ids": [str(x["id"]) for x in selected],
        "new_confirmed_stickers": 0,
        "evidence_ceiling": "offline unreviewed media and hash-similarity only",
    }
    return document, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=Path("visual-evidence-work/candidate-index.json"))
    parser.add_argument("--matches", type=Path, default=Path("visual-evidence-work/visual-matches.json"))
    parser.add_argument("--candidate-root", type=Path, default=Path("evidence-work"))
    parser.add_argument("--output", type=Path, default=Path("visual-evidence-work/review-gallery.html"))
    parser.add_argument("--max-items", type=int, default=48)
    args = parser.parse_args()
    body, report = render(
        json.loads(args.index.read_text(encoding="utf-8")),
        json.loads(args.matches.read_text(encoding="utf-8")),
        args.candidate_root,
        args.max_items,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(body, encoding="utf-8")
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "unavailable_or_unsafe_thumbnails"}))


if __name__ == "__main__":
    main()

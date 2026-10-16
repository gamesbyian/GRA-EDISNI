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


def region_preview(path: Path, bounds: list[int]) -> str:
    """Render a locally acquired source crop in EXIF-oriented pixel coordinates."""
    if not isinstance(bounds, list) or len(bounds) != 4 or any(
        type(v) is not int for v in bounds
    ):
        raise ValueError("malformed region coordinates")
    with Image.open(path) as raw:
        if raw.width * raw.height > MAX_PIXELS:
            raise ValueError("oversized source image")
        oriented = ImageOps.exif_transpose(raw)
        l,t,r,b = bounds
        if not (0 <= l < r <= oriented.width and 0 <= t < b <= oriented.height
                and min(r-l,b-t) >= 16):
            raise ValueError("invalid or out-of-image proposed crop")
        patch = oriented.crop(bounds)
        patch.thumbnail((180,180),Image.Resampling.LANCZOS)
        output = io.BytesIO()
        patch.convert("RGB").save(output,format="JPEG",quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode("ascii")


def region_by_candidate(regions: dict | None) -> dict[str, list[dict]]:
    if regions is None:
        return {}
    if regions.get("new_confirmed_stickers", 0) != 0:
        raise ValueError("a region-search report must not claim verified stickers")
    mapping = {}
    for row in regions.get("candidates", []):
        ident=row.get("candidate_id")
        if not isinstance(ident,str) or not ident or ident in mapping:
            raise ValueError("duplicate or missing candidate in regional report")
        mapping[ident]=row.get("suggestions",[])
    return mapping


def render(index: dict, visual: dict, root: Path, max_items: int = 48,
           regions: dict | None = None) -> tuple[str, dict]:
    items = index.get("candidates", [])
    if not isinstance(items, list):
        raise ValueError("candidate index must contain an array")
    matchmap = match_by_candidate(visual)
    regionmap = region_by_candidate(regions)
    selected = select_for_review(items, matchmap, max_items)
    source_count = len({source_label(x) for x in selected})
    cards = []
    errors = []
    roi_errors = []
    roi_previews = 0
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
        roi_markup = ""
        proposals = regionmap.get(ident, [])
        if proposals:
            details = []
            for ordinal, proposal in enumerate(proposals[:3], start=1):
                try:
                    if path is None:
                        raise ValueError("source image unavailable")
                    src = region_preview(path, proposal.get("bbox_xyxy_original_pixels"))
                    if proposal.get("new_sticker_confirmed") is not False:
                        raise ValueError("region proposal cannot verify a sticker")
                    reference = html.escape(str(proposal.get("reference_id", "unnamed")))
                    coords = html.escape(str(proposal.get("bbox_xyxy_original_pixels", [])))
                    distance = html.escape(str(proposal.get("hash_distance_sum", "?")))
                    details.append(f'<div class="roi"><img src="{src}" alt="Unverified region {ordinal}">'
                                   f'<p>Region {ordinal}: example {reference} · hash distance {distance}'
                                   f'<span class="coords">{coords}</span></p></div>')
                    roi_previews += 1
                except (OSError,ValueError,UnidentifiedImageError,Image.DecompressionBombError) as exc:
                    roi_errors.append({"candidate_id":ident,"region":ordinal,
                                       "error":str(exc)[:140]})
            roi_markup = ('<h3>Suggested image regions (unverified)</h3>'
                          '<div class="roi-grid">'+''.join(details)+'</div>'
                          '<p class="meta">A reference sticker number is an example template,'
                          ' NOT a reading of the candidate photograph.</p>')
        source_tag = html.escape(source_label(item))
        ident_tag = html.escape(ident)
        sha = html.escape(str(item.get("sha256", ""))[:16])
        cards.append(f'''<article class="card">
  {photo}
  <div class="body"><h2>{ident_tag}</h2>
  <p class="meta">Source batch: {source_tag}</p>
  <p class="links">{source_html} · {media_html}</p>
  <p class="meta">Local image digest prefix: {sha}</p>
  <h3>Review-only similarity</h3>{summary}{roi_markup}
  <p class="status">UNREVIEWED · no sticker verified</p></div>
</article>''')
    styles = """
body{font:15px/1.5 system-ui,sans-serif;margin:2rem auto;padding:0 1rem;max-width:1500px;background:#f4f4f4;color:#191919}
header{max-width:900px;margin-bottom:2rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:1rem}
.card{background:white;border:1px solid #ccc;border-radius:10px;overflow:hidden;min-width:0}
.card img{display:block;width:100%;height:250px;object-fit:contain;background:#ddd}
.roi-grid{display:flex;gap:.4rem;flex-wrap:wrap}.roi{max-width:120px}.roi img{width:120px;height:120px;object-fit:contain;background:#ececec}.roi p{font-size:.72rem;overflow-wrap:anywhere}.coords{display:block;color:#595959}\n.card .body{padding:1rem}.card h2{font-size:1.05rem;margin:0}.card h3{font-size:.9rem}
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
        "region_crop_previews_embedded": roi_previews,
        "invalid_region_preview_records": roi_errors,
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
    parser.add_argument("--regions",type=Path,default=None,
                        help="Optional review-only region-suggestions.json from opt-in pilot")
    args = parser.parse_args()
    body, report = render(
        json.loads(args.index.read_text(encoding="utf-8")),
        json.loads(args.matches.read_text(encoding="utf-8")),
        args.candidate_root,
        args.max_items,
        regions=json.loads(args.regions.read_text(encoding="utf-8")) if args.regions else None,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(body, encoding="utf-8")
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "unavailable_or_unsafe_thumbnails"}))


if __name__ == "__main__":
    main()

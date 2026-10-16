#!/usr/bin/env python3
"""Fetch a bounded allowlisted subset of image URLs extracted from PUBLIC HTML.

No page crawling, proxying, credentials, external-search automation, or arbitrary host
fetches. Preserve URL -> source page -> original media SHA256 -> local file mapping.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image

Image.MAX_IMAGE_PIXELS = 40_000_000
MAX_IMAGE_BYTES = 15 * 1024 * 1024
HOSTS = {
    "www.iam8bit.com", "cdn.shopify.com", "cdn.vox-cdn.com",
    "i.redd.it", "preview.redd.it", "i.imgur.com",
    "pbs.twimg.com", "i.ebayimg.com", "static0.polygonimages.com",
}
FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}
MAX_TOTAL_BYTES = 180 * 1024 * 1024


def approved(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.scheme == "https" and parsed.hostname in HOSTS
            and not parsed.username and not parsed.password)


class RestrictRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not approved(newurl):
            raise ValueError("Image redirect not on approved HTTPS hosts")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def retrieve(url: str) -> tuple[bytes, str, str]:
    if not approved(url):
        raise ValueError("Image host not approved; source kept for manual review")
    req = urllib.request.Request(url, headers={
        "User-Agent": "GRA-EDISNI-public-CE-visual-research/1.0",
        "Accept": "image/jpeg,image/png,image/webp,image/gif",
    })
    op = urllib.request.build_opener(RestrictRedirects())
    with op.open(req, timeout=25) as response:
        if not approved(response.geturl()):
            raise ValueError("Image final URL not approved")
        if not response.headers.get_content_type().startswith("image/"):
            raise ValueError("Not image content-type")
        data = response.read(MAX_IMAGE_BYTES + 1)
        if not 0 < len(data) <= MAX_IMAGE_BYTES:
            raise ValueError("Image empty or over size limit")
        with Image.open(io.BytesIO(data)) as im:
            fmt = im.format
            w, h = im.size
            im.verify()
        if fmt not in FORMATS or min(w, h) < 32 or w * h > Image.MAX_IMAGE_PIXELS:
            raise ValueError("Unsupported image type or dimensions")
        return data, response.geturl(), FORMATS[fmt]


def safe_dir(name: str) -> str:
    return "htmlimg-" + re.sub(r"[^a-zA-Z0-9_-]+", "-", name)[:80]


def asset_key(url: str) -> tuple[str, str, str]:
    """Identical resource path at different CDN widths is one *candidate asset*.

    This is deliberately weaker than byte or physical-object equivalence. Only
    use to allocate fetching budget. The original individual URLs are retained.
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    version = query.get("v", [""])[0]
    return (parsed.hostname or "", parsed.path, version)


def resolution_preference(url: str) -> float:
    """Prefer usable large versions, but avoid huge 15 MiB downloads by default."""
    q = parse_qs(urlparse(url).query)
    try:
        width = float(q.get("width", q.get("w", ["0"]))[0])
        dpr = float(q.get("dpr", ["1"])[0])
        effective = max(0, width * min(max(dpr, 1), 3))
    except (ValueError, OverflowError):
        return 0
    # Reference photos should be legible, with a natural ceiling at 2048px.
    return min(effective, 2048) - max(0, effective - 2048) * .1


def select(leads: list[dict], per_page: int, total: int) -> list[dict]:
    """Choose diverse full assets, not eight near-identical srcset resolutions.

    Public promotional controls receive higher priority when their asset path
    names the product; generic site assets are kept out of official-page pilot
    budgets. Independent owner pages can still have opaque image names.
    """
    grouped: dict[str, dict[tuple[str, str, str], dict]] = {}
    for entry in leads:
        key = entry.get("source_id", "")
        url = entry.get("image_url", "")
        if not key or not approved(url):
            continue
        # Official retail and syndicated press pages may embed unrelated shop
        # carousels. Their original article media should include a product clue.
        if key.startswith("ce-visual-official-") and not any(
            word in url.lower() for word in ("inside", "playdead", "realdoll", "huddle")
        ):
            continue
        assets = grouped.setdefault(key, {})
        ident = asset_key(url)
        previous = assets.get(ident)
        score = (entry.get("hint_count", 0), resolution_preference(url))
        if previous is None or score > (
            previous.get("hint_count", 0),
            resolution_preference(previous["image_url"]),
        ):
            assets[ident] = entry
    # Round-robin selection prevents lexicographically earlier source IDs
    # from consuming the entire batch before later source pages are considered.
    # Score the first round by each source's strongest lead rather than its ID.
    queues = {
        key: sorted(
            rows.values(),
            key=lambda r: (-r.get("hint_count", 0),
                           -resolution_preference(r["image_url"]), r["image_url"]),
        )[:per_page]
        for key, rows in grouped.items()
    }
    source_order = sorted(
        queues,
        key=lambda key: (-queues[key][0].get("hint_count", 0),
                         -resolution_preference(queues[key][0]["image_url"]),
                         key),
    )
    selected = []
    for depth in range(per_page):
        for key in source_order:
            if depth < len(queues[key]):
                selected.append(queues[key][depth])
                if len(selected) == total:
                    return selected
    return selected


def selection_coverage(leads: list[dict], chosen: list[dict]) -> dict:
    """Report image leads excluded by allowlist, official URL heuristics and caps.

    These are *not irrelevant images*, merely assets not acquired in this
    particular budgeted pass. Original lead URLs remain in the input artifact.
    """
    states = {"missing_source_or_url": 0, "unapproved_image_host": 0,
              "official_product_url_heuristic": 0, "eligible_url_mentions": 0}
    asset_groups = set()
    for entry in leads:
        key = entry.get("source_id", "")
        url = entry.get("image_url", "")
        if not key or not url:
            states["missing_source_or_url"] += 1
            continue
        if not approved(url):
            states["unapproved_image_host"] += 1
            continue
        if key.startswith("ce-visual-official-") and not any(
            word in url.lower() for word in ("inside", "playdead", "realdoll", "huddle")
        ):
            states["official_product_url_heuristic"] += 1
            continue
        states["eligible_url_mentions"] += 1
        asset_groups.add((key, asset_key(url)))
    selected_groups = {(row["source_id"], asset_key(row["image_url"])) for row in chosen}
    states.update({
        "input_url_mentions": len(leads),
        "unique_eligible_asset_families": len(asset_groups),
        "eligible_variants_collapsed": states["eligible_url_mentions"] - len(asset_groups),
        "asset_families_selected_for_transfer": len(selected_groups),
        "eligible_asset_families_not_selected_by_budget": len(asset_groups - selected_groups),
        "original_lead_inventory_retained_separately": True,
        "interpretation": "unselected does not imply irrelevant or no sticker",
    })
    return states


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--leads", type=Path, default=Path("visual-evidence-work/html-image-leads.json"))
    p.add_argument("--out", type=Path, default=Path("evidence-work"))
    p.add_argument("--additional-leads", type=Path, action="append",
                   help="Optional JSON image_mentions from PUBLIC archive metadata")
    p.add_argument("--max-per-page", type=int, default=8)
    p.add_argument("--max-images", type=int, default=48)
    args = p.parse_args()
    if not (1 <= args.max_images <= 200 and 1 <= args.max_per_page <= 50):
        p.error("max-images must be 1..200 and max-per-page 1..50")
    rows = json.loads(args.leads.read_text(encoding="utf-8"))["image_mentions"]
    for lead_file in args.additional_leads or []:
        rows += json.loads(lead_file.read_text(encoding="utf-8"))["image_mentions"]
    chosen = select(rows, args.max_per_page, args.max_images)
    waterfall = selection_coverage(rows, chosen)
    args.out.mkdir(parents=True, exist_ok=True)
    reports = []
    total_bytes = 0
    by_source: dict[str, dict] = {}
    for row in chosen:
        parent = args.out / safe_dir(row["source_id"])
        parent.mkdir(parents=True, exist_ok=True)
        name = hashlib.sha256(row["image_url"].encode("utf-8")).hexdigest()[:24]
        record = {"image_url": row["image_url"], "source_id": row["source_id"],
                  "source_page_url": row["source_page_url"], "keyword_hints": row["keyword_hints"],
                  "status": "unavailable"}
        try:
            if total_bytes >= MAX_TOTAL_BYTES:
                raise ValueError("Run total-byte budget reached")
            data, final_url, suffix = retrieve(row["image_url"])
            if total_bytes + len(data) > MAX_TOTAL_BYTES:
                raise ValueError("Run would exceed total-byte budget")
            dest = parent / (name + suffix)
            dest.write_bytes(data)
            total_bytes += len(data)
            record.update({"status": "downloaded", "path": str(dest.relative_to(args.out)),
                           "final_url": final_url, "bytes": len(data),
                           "sha256": hashlib.sha256(data).hexdigest()})
            bucket = by_source.setdefault(row["source_id"], {
                "source_id": safe_dir(row["source_id"]), "url": row["source_page_url"],
                "kind": "public-html-image-candidate", "classification": "unreviewed",
                "image_urls": {}, "source_pages": {},
            })
            bucket["image_urls"][dest.name] = row["image_url"]
            bucket["source_pages"][dest.name] = row["source_page_url"]
        except (OSError, ValueError, urllib.error.URLError) as exc:
            record["error"] = str(exc)[:240]
        reports.append(record)
        print(row["source_id"], record["status"])
    for source_id, data in by_source.items():
        out = args.out / safe_dir(source_id) / "acquisition.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path = args.out / "html-image-download-report.json"
    report_path.write_text(json.dumps({
        "schema_version": 1, "max_images": args.max_images,
        "bytes_downloaded": total_bytes, "image_downloads": reports,
        "selection_coverage": waterfall,
        "note": "Remote media unreviewed; nothing here confirms an edition or sticker"
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

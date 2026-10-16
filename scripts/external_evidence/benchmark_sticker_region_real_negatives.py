#!/usr/bin/env python3
"""Score SHA-pinned already-acquired *visible sticker* negative reference images.

For manual, permission-bounded CE visual workflows only. Promotional packshots,
standalone INSIDE PS4 product photos and a known CE collector's open-box image
without a VISIBLE numbered sticker are source-specific negative controls.
No acquisition/network, OCR, owner lookup or sticker confirmation.

Absence of a visible sticker in one photograph is NOT proof of physical loss.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

if __package__:
    from .visual_region_probe import load_regions, scan, sha256
else:
    from visual_region_probe import load_regions, scan, sha256

PINNED_ROLES = {
    "negative-control-promotional-screenshot",
    "negative-control-marketing-repost",
    "negative-control-standalone",
    "positive-control-public-owner-open-ce-no-visible-sticker",
}
CURVE = (24,32,40,48,56,65)


def sources_to_scan(manifest: dict, root: Path, *, max_files: int=8) -> tuple[list[dict],list[dict]]:
    """Source IDs are never substituted from unchecked acquired filenames."""
    if not 1<=max_files<=8:
        raise ValueError("negative benchmark max_files must be 1..8")
    sources=manifest.get("sources",[])
    if not isinstance(sources,list):
        raise ValueError("visual reference manifest is not a source list")
    expected=[s for s in sources if s.get("expected_sha256") and s.get("role") in PINNED_ROLES]
    selected=expected[:max_files]
    loaded,skipped=[],[]
    root=root.resolve()
    for source in selected:
        ident=source.get("id","")
        expected_sha=source.get("expected_sha256","")
        ext=source.get("extension","")
        if not isinstance(ident,str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,120}",ident):
            raise ValueError("bad pinned negative source ID")
        if not isinstance(ext,str) or ext not in {".jpg",".jpeg",".png",".webp"}:
            raise ValueError("unsupported pinned negative extension")
        if not isinstance(expected_sha,str) or not re.fullmatch(r"[a-f0-9]{64}",expected_sha):
            raise ValueError("missing or malformed negative source SHA")
        path=(root/(ident+ext)).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            skipped.append({"source_id":ident,"reason":"image-not-acquired"})
            continue
        actual=sha256(path)
        if actual!=expected_sha:
            raise ValueError(f"source image digest mismatch, refuse evaluation: {ident}")
        loaded.append({"source_id":ident,"role":source["role"],"path":path,
                       "sha256":actual,"source_url":source.get("url",""),
                       "source_page":source.get("source_page","")})
    return loaded,skipped


def report_negatives(manifest: dict, media_root: Path, refs: list[dict],
                     *, max_files: int=8, max_windows: int=1600,
                     max_refine_windows: int=1200, top_k: int=8) -> dict:
    if top_k!=8 or max_windows!=1600 or max_refine_windows!=1200:
        raise ValueError("negative scoring budget frozen; use a versioned new benchmark")
    ready,missing=sources_to_scan(manifest,media_root,max_files=max_files)
    observations=[]
    for row in ready:
        try:
            with Image.open(row["path"]) as original:
                proposals,coverage=scan(original,refs,
                    max_windows=max_windows,
                    max_refine_windows=max_refine_windows,
                    max_suggestions=top_k)
            observations.append({
                "source_id":row["source_id"],"role":row["role"],
                "original_media_sha256":row["sha256"],"source_url":row["source_url"],
                "source_page":row["source_page"],
                "has_no_visible_numbered_sticker_in_documented_source":True,
                "not_evidence_of_physical_sticker_loss":True,
                "topk_candidate_distances":[p["hash_distance_sum"] for p in proposals],
                "topk_count":len(proposals),"coverage":coverage,
                "new_confirmed_stickers":0,
            })
        except (OSError,UnidentifiedImageError,Image.DecompressionBombError,ValueError) as exc:
            missing.append({"source_id":row["source_id"],"reason":"image-invalid-for-scan",
                            "error_class":type(exc).__name__})
    operating=[{
        "max_hash_distance":cutoff,
        "scanned_images_with_at_least_one_false_visual_prompt":sum(
            any(d<=cutoff for d in item["topk_candidate_distances"]) for item in observations),
        "scanned_negative_images":len(observations),
        "acquisition_failures_excluded":len(missing),
    } for cutoff in CURVE]
    return {
        "schema_version":1,
        "kind":"original-public-image-no-visible-sticker-visual-prompt-audit",
        "acquisition":"already-acquired-and-source-sha-verified; no network",
        "negative_controls_expected":len([
            s for s in manifest.get("sources",[]) if s.get("expected_sha256")
            and s.get("role") in PINNED_ROLES][:max_files]),
        "negative_controls_scanned":len(observations),
        "unavailable_or_invalid_source_controls":missing,
        "reference_original_photographs":len({r["reference_id"] for r in refs}),
        "operating_points":operating,"per_source":observations,
        "known_original_photos_have_no_visible_numbered_sticker":True,
        "interpretation":"visible-sticker negative prompts, not physical absence; unreviewed similar rectangles may occur",
        "new_confirmed_stickers":0,
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=Path("."))
    p.add_argument("--source-manifest",type=Path,
                   default=Path("data/reference/inside-ce-visual-sources.json"))
    p.add_argument("--media",type=Path,default=Path("visual-reference-work"))
    p.add_argument("--output",type=Path,
                   default=Path("visual-evidence-work/region-real-negative-controls.json"))
    args=p.parse_args()
    root=args.repo_root.resolve()
    manifest=args.source_manifest if args.source_manifest.is_absolute() else root/args.source_manifest
    refs=load_regions(root/"data/reference/inside-ce-sticker-region-pilot-rois.csv",root)
    result=report_negatives(json.loads(manifest.read_text(encoding="utf-8")),
                            args.media,refs)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"negative_controls_scanned":result["negative_controls_scanned"],
                      "negative_controls_expected":result["negative_controls_expected"],
                      "unavailable_or_invalid_source_controls":len(result["unavailable_or_invalid_source_controls"]),
                      "operating_points":result["operating_points"],
                      "new_confirmed_stickers":0},sort_keys=True))


if __name__=="__main__":
    main()

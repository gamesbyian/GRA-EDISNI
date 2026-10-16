#!/usr/bin/env python3
"""Source-first SAHI-inspired overlapping tiles for existing CPU paper contours.

No SAHI package/model weights are loaded. We reuse our OpenCV generic *paper*
proposal method per local tile, map results back to the same EXIF-oriented
source coordinates, and deduplicate by overlap-over-smaller. Proposals
remain unverified, and the output is never a serial or owner classifier.

Supports opt-in already-acquired, SHA-pinned source images only.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

if __package__:
    from .visual_geometry_proposals import propose
    from .visual_region_probe import sha256, diverse_candidates, box_iou
else:
    from visual_geometry_proposals import propose
    from visual_region_probe import sha256, diverse_candidates, box_iou

DEFAULT_MAX_TILES = 24
DEFAULT_MAX_RESULTS = 8
MAX_TILE_PROPOSALS = 16
MAX_IMAGE_PIXELS = 40_000_000
TILE_OVERLAP = 0.25


def overlap_over_smaller(a: list[int], b: list[int]) -> float:
    w = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    if not w or not h:
        return 0.
    aa = (a[2] - a[0])*(a[3] - a[1])
    ab = (b[2] - b[0])*(b[3] - b[1])
    return (w*h / min(aa,ab)) if min(aa,ab)>0 else 0.


def starts(length: int, tile: int, overlap: float) -> list[int]:
    if not 0 <= overlap < .75:
        raise ValueError("tile overlap fraction outside 0..0.75")
    if tile < 64:
        raise ValueError("tile side too small")
    if length <= tile:
        return [0]
    stride = max(1, int(round(tile*(1-overlap))))
    positions = list(range(0, length-tile+1, stride))
    if positions[-1] != length-tile:
        positions.append(length-tile)
    return positions


def tile_plan(width: int, height: int, *, max_tiles: int = DEFAULT_MAX_TILES,
              overlap: float = TILE_OVERLAP) -> tuple[list[tuple[int,int,int,int]],dict]:
    if not 1 <= max_tiles <= 48:
        raise ValueError("max tiles must be 1..48")
    if width < 64 or height < 64 or width*height>MAX_IMAGE_PIXELS:
        raise ValueError("input exceeds tileable pixel limits")
    # Fix both a lower bound for detection and a bound on tile compute.
    # 720x540 -> ~297 px tile, 3000x4000 -> 768 px tile.
    tile = max(240,min(768,int(round(min(width,height)*.55))))
    tile = min(tile,width,height)
    xs = starts(width,tile,overlap)
    ys = starts(height,tile,overlap)
    all_boxes = [(x,y,min(width,x+tile),min(height,y+tile))
                 for y in ys for x in xs]
    if len(all_boxes)<=max_tiles:
        chosen=all_boxes
    else:
        # Uniform coverage: choose farthest tile centers; corners first.
        # A cap must not silently skip every tile at the right/bottom side.
        chosen_indices=[]
        corners=[(0,0),(width,0),(0,height),(width,height)]
        for tx,ty in corners:
            nearest=min(range(len(all_boxes)),
                        key=lambda i:(((all_boxes[i][0]+all_boxes[i][2])/2-tx)**2+
                                      ((all_boxes[i][1]+all_boxes[i][3])/2-ty)**2,i))
            if nearest not in chosen_indices and len(chosen_indices)<max_tiles:
                chosen_indices.append(nearest)
        while len(chosen_indices)<max_tiles:
            def separation(i):
                cx=(all_boxes[i][0]+all_boxes[i][2])/2/width
                cy=(all_boxes[i][1]+all_boxes[i][3])/2/height
                return min(((cx-(all_boxes[j][0]+all_boxes[j][2])/2/width)**2+
                            (cy-(all_boxes[j][1]+all_boxes[j][3])/2/height)**2)
                           for j in chosen_indices)
            available=[i for i in range(len(all_boxes)) if i not in chosen_indices]
            chosen_indices.append(max(available,key=lambda i:(separation(i),-i)))
        chosen=[all_boxes[i] for i in sorted(chosen_indices)]
    return chosen,{
        "tiled_original_width":width,"tiled_original_height":height,
        "tile_side_px":tile,"overlap_ratio":overlap,
        "tiles_proposed":len(all_boxes),"tiles_evaluated":len(chosen),
        "tiles_censored_by_budget":len(all_boxes)-len(chosen),
        "tiling_incomplete_at_cap":len(all_boxes)>max_tiles,
        "tile_locations":list(map(list,chosen)),
    }


def suggest(image: Image.Image, *, max_tiles: int = DEFAULT_MAX_TILES,
            top_k: int = DEFAULT_MAX_RESULTS,
            include_global: bool = True) -> tuple[list[dict],dict]:
    if not 1<=top_k<=48:
        raise ValueError("review shortlist size outside 1..48")
    oriented=ImageOps.exif_transpose(image).convert("RGB")
    if oriented.width*oriented.height > MAX_IMAGE_PIXELS:
        raise ValueError("oversize image")
    tiles,coverage=tile_plan(oriented.width,oriented.height,max_tiles=max_tiles)
    pool=[]; input_counts=[]; input_total=0
    for number,window in enumerate(tiles):
        patch=oriented.crop(window)
        boxes,stats=propose(patch,max_proposals=MAX_TILE_PROPOSALS)
        input_counts.append(stats)
        input_total+=len(boxes)
        for proposal in boxes:
            l,t,r,b=proposal["bbox_xyxy_original_pixels"]
            full=[window[0]+l,window[1]+t,window[0]+r,window[1]+b]
            if full[2]>oriented.width or full[3]>oriented.height:
                raise ValueError("tiled-to-original geometry mapping exceeded source size")
            pool.append({**proposal,
                "bbox_xyxy_original_pixels":full,
                "tile_index":number,"tile_source_xyxy":list(window),
                "proposal_method":"overlapping-tiled-bright-contours",
                "new_sticker_confirmed":False,
            })
    if include_global:
        global_boxes,global_stats=propose(oriented,max_proposals=MAX_TILE_PROPOSALS)
        for proposal in global_boxes:
            pool.append({**proposal, "tile_index":None,
                         "tile_source_xyxy":[0,0,oriented.width,oriented.height],
                         "proposal_method":"full-image-bright-contours",
                         "new_sticker_confirmed":False})
    else:
        global_stats=None
    # The heuristic order is not a calibrated recognition score. Across
    # scales it may favor blank cards. Preserve provenance of both passes.
    pool.sort(key=lambda p:(-p["heuristic_order_score"],
                            p["bbox_xyxy_original_pixels"],
                            p["tile_index"] if p["tile_index"] is not None else -1))
    selected=[]; duplicates=0
    for item in pool:
        if any(overlap_over_smaller(item["bbox_xyxy_original_pixels"],
                                   kept["bbox_xyxy_original_pixels"])>.72
               for kept in selected):
            duplicates+=1
            continue
        selected.append(item)
        if len(selected)>=top_k:
            break
    coverage.update({
        "global_pass_included":include_global,
        "global_pass_stats":global_stats,
        "tiled_proposals_before_merge":input_total,
        "all_proposals_with_global_before_merge":len(pool),
        "shortlist_count":len(selected),
        "duplicate_suppressed_until_shortlist_full":duplicates,
        "unreviewed_or_unranked_at_topk":max(0,len(pool)-duplicates-len(selected)),
        "paper_candidate_false_positives_unmeasured":True,
        "never_verifies_ce_sticker":True,
        "individual_tile_stats":input_counts,
    })
    return selected,coverage


def scan_index(index: dict, root: Path, *, max_files: int=48,
               max_tiles: int=DEFAULT_MAX_TILES, top_k:int=8)->dict:
    rows=index.get("candidates",[])
    if not isinstance(rows,list):
        raise ValueError("candidate index requires list")
    chosen=diverse_candidates(rows,max_files)
    root=root.resolve()
    results=[];errors=[]
    for item in chosen:
        ident=item.get("id","")
        path=(root/str(item.get("path",""))).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append({"candidate_id":ident,"reason":"unsafe-or-unavailable-source"})
            continue
        if sha256(path)!=item.get("sha256"):
            errors.append({"candidate_id":ident,"reason":"sha256-mismatch"})
            continue
        try:
            with Image.open(path) as im:
                proposals,stats=suggest(im,max_tiles=max_tiles,top_k=top_k)
            results.append({"candidate_id":ident,"source_url":item.get("source_url",""),
                            "source_kind":item.get("source_kind",""),
                            "proposals":proposals,"coverage":stats,
                            "new_sticker_confirmed":False})
        except (ValueError,OSError,UnidentifiedImageError,Image.DecompressionBombError) as exc:
            errors.append({"candidate_id":ident,"reason":type(exc).__name__})
    return {
        "schema_version":1,"proposal_method":"cpu-sliced-contours-with-global-pass",
        "total_candidate_files":len(rows),"selected_candidate_files":len(chosen),
        "candidate_files_not_selected_by_cap":len(rows)-len(chosen),
        "scanned_source_files":len(results),"source_failures":errors,"candidates":results,
        "autonomous_sticker_detection_validated":False,
        "new_confirmed_stickers":0,
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidate-index",type=Path,required=True)
    ap.add_argument("--candidate-root",type=Path,required=True)
    ap.add_argument("--output",type=Path,default=Path("visual-evidence-work/sliced-paper-proposals.json"))
    ap.add_argument("--max-files",type=int,default=48)
    ap.add_argument("--max-tiles",type=int,default=DEFAULT_MAX_TILES)
    ap.add_argument("--top-k",type=int,default=8)
    args=ap.parse_args()
    result=scan_index(json.loads(args.candidate_index.read_text(encoding="utf-8")),
                     args.candidate_root,max_files=args.max_files,
                     max_tiles=args.max_tiles,top_k=args.top_k)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="candidates"},sort_keys=True))


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""CL-04c: explicitly after-inspection 0xCF (207) RGB palette hypothesis.

Repeated sampled colours included #CFCF00, #CFCFCF, #00CFCF,
#CF00CF, #0000CF. This conjecture tests the FULL 2^3 class
with each R/G/B component either 0 or 207. This after-inspection
palette family is exploratory, never source-confirmed.

Evaluate SOURCE REGION independently of sticker outputs, then test
all 64 fixed 512-site banks for both balanced p0,G0 CE candidates.
"""
import argparse
from collections import Counter
from io import BytesIO
import json
from itertools import product
from pathlib import Path

from PIL import Image
from conjecture_lab_gate98_real_pixels import (
    load_bytes, EXPECTED_DIMENSIONS, PIXELS_PER_ROW, PIXELS_PER_COL,
    SAMPLE_STEP, BANK_SIZE, BANKS, class_addresses, q4_depths
)
from enumerate_sticker_completion_ensembles import observations
from generate_master import generate_master, legal_states

LEVEL = 207
PALETTE = [tuple(LEVEL if b else 0 for b in bits)
           for bits in product((0,1), repeat=3)]
assert len(PALETTE)==8

def run(path):
    payload, source_id=load_bytes(path)
    with Image.open(BytesIO(payload)) as src:
        assert src.size==EXPECTED_DIMENSIONS
        img=src.convert("RGB")

    sampled=[tuple(img.getpixel((16*x,16*y)))
             for y in range(PIXELS_PER_COL)
             for x in range(PIXELS_PER_ROW)]
    assert len(sampled)==32768
    counter=Counter(sampled)
    subset=set(PALETTE)
    coords_by_color={color:[] for color in PALETTE}
    for i,color in enumerate(sampled):
        if color in subset:
            y,x=divmod(i, PIXELS_PER_ROW)
            coords_by_color[color].append((x,y))
    candidate_palette=[]
    for c in PALETTE:
        coords=coords_by_color[c]
        candidate_palette.append({
            "rgb":list(c),
            "hex":"#" + "".join(f"{v:02X}" for v in c),
            "triple_bits":"".join("1" if v==LEVEL else "0" for v in c),
            "sampled_marks":len(coords),
            "top_64_sampled_rows":sum(y<64 for x,y in coords),
            "bottom_192_sampled_rows":sum(y>=64 for x,y in coords),
            "sampled_bbox":([min(x for x,y in coords),
                             min(y for x,y in coords),
                             max(x for x,y in coords),
                             max(y for x,y in coords)]
                            if coords else None),
        })

    n,obs=observations()
    assert n==84 and len(obs)==66
    states=[]
    for state in legal_states():
        if state.p!=0 or state.G!=0:
            continue
        master=generate_master(state)
        if all(master[k-1]==v for k,v in obs.items()):
            states.append((state,master))
    assert len(states)==2

    matrices=[]
    for state,master in states:
        addresses=class_addresses(master)
        depths=q4_depths(master)
        assert len(addresses)==len(depths)==9
        banks=[]
        for bank in range(BANKS):
            sites=[sampled[bank*BANK_SIZE+addr] for addr in addresses]
            palette_hits=[color in subset for color in sites]
            output="".join(
                str(int(sites[j][depths[j]]==LEVEL))
                if palette_hits[j] else "?"
                for j in range(9)
            )
            banks.append({
                "bank":bank,
                "source_rgb_hex":[
                    "#" + "".join(f"{v:02X}" for v in c)
                    for c in sites
                ],
                "palette_hits":sum(palette_hits),
                "paletted_mask":"".join("1" if v else "0" for v in palette_hits),
                "selector_plane_bits":output,
            })
        matrices.append({
            "state":f"{state.X}{state.Y}{state.Z}{state.G}",
            "addresses":addresses,
            "q4_depths":depths,
            "max_palette_hits":max(b["palette_hits"] for b in banks),
            "all_nine_hits_banks":[b["bank"] for b in banks if b["palette_hits"]==9],
            "all_64_banks":banks,
        })

    return {
        "status":"after-inspection palette guess, conditional source-content test NOT native decoder",
        "source_git_sha1":source_id,
        "palette_level":LEVEL,
        "palette_selection":"Observed some repeated 0xCF pixel colors before hypothesizing full 2^3 palette",
        "candidate_3bit_colors":candidate_palette,
        "total_palette_hits_on_fixed_16px_grid":sum(counter[c] for c in PALETTE),
        "total_palette_hits_top_64_rows":sum(
            x["top_64_sampled_rows"] for x in candidate_palette),
        "total_palette_hits_bottom_192_rows":sum(
            x["bottom_192_sampled_rows"] for x in candidate_palette),
        "source_lattice_dimensions":[128,256],
        "candidate_512_site_banks":64,
        "selected_complete_master_branches":matrices,
        "scope":"Only fixed top-left 16px sample, row-major 512 banks, 0/207 exactly, native Q4->RGB bit labels; other source colors/regions/transformations remain open",
        "warning":"The 0xCF level was recognized after source image inspection; it is a discovery device. Seven historical marked colors have not been independently authenticated as exactly this palette."
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source")
    p.add_argument("--output")
    args=p.parse_args()
    r=run(args.source)
    if args.output:
        Path(args.output).write_text(json.dumps(r,indent=2)+"\n",encoding="utf8")
    print(json.dumps({
        "source_gitsha":r["source_git_sha1"],
        "palette_census":r["candidate_3bit_colors"],
        "palette_grid_total":r["total_palette_hits_on_fixed_16px_grid"],
        "palette_top_64":r["total_palette_hits_top_64_rows"],
        "palette_bottom_192":r["total_palette_hits_bottom_192_rows"],
        "master_bank_maxima":[{
            "state":x["state"],"max_color_hits":x["max_palette_hits"],
            "all_nine_hits_banks":x["all_nine_hits_banks"],
        } for x in r["selected_complete_master_branches"]],
    },indent=2))

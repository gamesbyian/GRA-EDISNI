#!/usr/bin/env python3
"""CL05: recover source-native phase of 2018 gate-98 PNG; control CE lookups.

Historic method: exact-black pixels on a 16-pixel spacing expose a planet.
Infer the grid PHASE from original black coordinates alone, never sticker
values or intended output. Freeze the bitmap hash before speculative reads.

Requires Pillow. With --source, no network access.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from PIL import Image
from conjecture_lab_gate98_real_pixels import (
    load_bytes, EXPECTED_DIMENSIONS, SAMPLE_STEP,
    PIXELS_PER_ROW, PIXELS_PER_COL, BANKS, BANK_SIZE,
    class_addresses, q4_depths,
)
from enumerate_sticker_completion_ensembles import observations
from generate_master import legal_states, generate_master

W,H=EXPECTED_DIMENSIONS
STRIDE=SAMPLE_STEP
SOURCE_TOP=1024
EXPECTED_PHASE=(4,12)
EXPECTED_PLANET_SHA256="38e3f2e176277851a059c9a8c9d37cc913e2602e5fc661b71298dbb9ccaf8411"
CF207={
    (r,g,b) for r in (0,207) for g in (0,207)
    for b in (0,207) if r or g or b
}

def phase_scan(im):
    """Exhaust all 256 phases using only original exact-black pixel count."""
    counts=[[0]*16 for _ in range(16)]
    crop=im.crop((0,0,W,SOURCE_TOP))
    for i,pix in enumerate(crop.getdata()):
        if pix[:3]==(0,0,0):
            y,x=divmod(i,W)
            counts[y%STRIDE][x%STRIDE]+=1
    ranked=sorted(
        [(counts[dy][dx],dx,dy) for dy in range(16) for dx in range(16)],
        reverse=True)
    assert ranked[:2]==[(1591,4,12),(68,5,12)], ranked[:2]
    assert counts[0][0]==62
    return counts,ranked

def black_bitmap(im,origin):
    sx,sy=origin
    binary=bytearray()
    n=0
    for y in range(64):
        for i in range(0,128,8):
            b=0
            for j in range(8):
                black=im.getpixel((sx+(i+j)*16,sy+y*16))[:3]==(0,0,0)
                b=(b<<1)|black
                n+=black
            binary.append(b)
    assert len(binary)==1024 and n==1591
    digest=sha256(binary).hexdigest()
    assert digest==EXPECTED_PLANET_SHA256,digest
    return bytes(binary),n,digest

def actual_lattice(im,origin):
    sx,sy=origin
    return [
        tuple(im.getpixel((sx+16*x,sy+16*y))[:3])
        for y in range(PIXELS_PER_COL)
        for x in range(PIXELS_PER_ROW)
    ]

def candidate_bytes(grid,obs):
    live=[]
    for st in legal_states():
        if st.p!=0 or st.G!=0:continue
        word=generate_master(st)
        if all(word[k-1]==v for k,v in obs.items()):
            live.append((st,word))
    assert [f"{s.X}{s.Y}{s.Z}{s.G}" for s,_ in live]==["0100","1100"]

    allstates=[]
    for st,word in live:
        addr=class_addresses(word)
        channel=q4_depths(word)
        banks=[]
        for bank in range(BANKS):
            colors=[grid[bank*BANK_SIZE+a] for a in addr]
            raw=bytes(colors[j][channel[j]] for j in range(9))
            nn=sum(c in CF207 for c in colors)
            tri=sum(all(v in (0,207,251) for v in c) for c in colors)
            banks.append({
                "bank":bank,
                "raw_ascii_byte_hex":raw.hex(),
                "printable_ascii_count":sum(32<=v<=126 for v in raw),
                "nonblack_207_palette_hits":nn,
                "zero_207_251_three_level_palette_hits":tri,
                "source_rgb_hex":[bytes(c).hex() for c in colors],
            })
        assert len(banks)==64
        assert max(b["printable_ascii_count"] for b in banks)==3
        assert max(b["nonblack_207_palette_hits"] for b in banks)==3
        assert max(b["zero_207_251_three_level_palette_hits"] for b in banks)==7
        assert not any(b["zero_207_251_three_level_palette_hits"]==9 for b in banks)
        allstates.append({
            "state":f"{st.X}{st.Y}{st.Z}{st.G}",
            "nine_class_addresses":addr,
            "nine_q4_channel_depths":channel,
            "banks":banks,
        })
    return allstates

def run(source):
    payload,gitsha=load_bytes(source)
    from io import BytesIO
    with Image.open(BytesIO(payload)) as obj:
        assert obj.size==EXPECTED_DIMENSIONS
        im=obj.convert("RGB")
    counts,ranked=phase_scan(im)
    phase=(ranked[0][1],ranked[0][2])
    assert phase==EXPECTED_PHASE
    bitmap,planet_n,planet_hash=black_bitmap(im,phase)
    n,observed=observations()
    assert n==84 and len(observed)==66
    grid=actual_lattice(im,phase)
    samples=Counter(grid)
    states=candidate_bytes(grid,observed)

    return {
        "status":"source-native historical planet-scan positive control; CE consumer unverified",
        "source_git_sha1":gitsha,
        "source_dimensions":[W,H],
        "historic_operation":"exact-black separation and 16-pixel grid",
        "entire_first_1024_pixel_rows_scanned_without_using_stickers":True,
        "all_256_black_phase_counts":counts,
        "best_phase_derived_from_black_only_xy":list(phase),
        "black_phase_runner_up":list(ranked[1]),
        "black_at_incorrect_origin_00":counts[0][0],
        "black_at_recovered_origin":planet_n,
        "native_planet_bitmap_dimensions":[128,64],
        "native_planet_bitmap_sha256":planet_hash,
        "source_phase_rgb_distinct_color_count":len(samples),
        "source_phase_cf207_nonblack_count":sum(samples[c] for c in CF207),
        "source_phase_207_251_tri_colour_count":sum(
            v for c,v in samples.items() if all(x in (0,207,251) for x in c)),
        "conditional_sticker_reader":{
            "warning":"512-site banks and Q4-to-RGB choice invented; phase is now grounded, but these other settings are NOT",
            "bank_count_per_state":64,
            "all_banks_per_state":states,
            "all_nine_ascii_words":0,
            "all_nine_exact_tri_palettes":0,
        },
        "provenance":"Known 2018 route text is not used by any scanner, ranking or assertion. Visual content independently matches contemporary described 'planet scan'; exact historic six-colour text codebook remains unverified."
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source")
    p.add_argument("--output")
    a=p.parse_args()
    result=run(a.source)
    if a.output:
        Path(a.output).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "source":result["source_git_sha1"],
        "recovered_black_phase":result["best_phase_derived_from_black_only_xy"],
        "black_at_phase":result["black_at_recovered_origin"],
        "runner_up":result["black_phase_runner_up"],
        "incorrect_origin_black":result["black_at_incorrect_origin_00"],
        "planet_sha256":result["native_planet_bitmap_sha256"],
        "source_phase_rgb_distinct":result["source_phase_rgb_distinct_color_count"],
        "new_candidate_summary":[
            {"state":x["state"],
             "max_printable":max(b["printable_ascii_count"] for b in x["banks"]),
             "max_cf207":max(b["nonblack_207_palette_hits"] for b in x["banks"]),
             "max_tri":max(b["zero_207_251_three_level_palette_hits"] for b in x["banks"])}
            for x in result["conditional_sticker_reader"]["all_banks_per_state"]
        ]
    },indent=2))

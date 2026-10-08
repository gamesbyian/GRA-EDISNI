#!/usr/bin/env python3
"""CL-06: byte-pinned 2019 gate-98 historical reference and exact layer replay.

DISCOVER/DEVELOP only. Offsets were selected against the 2019 historical
witness, not independently prescribed by Playdead. The input includes NO
CE sticker data or predicted missing marks.

Default fixture-only mode runs offline without Pillow/source PNG.
--source and --witness enable byte-exact optional source reproduction.
"""
from __future__ import annotations

import argparse
import base64
from hashlib import sha256
import json
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data" / "conjecture-lab-gate98-historical-layer-control-2026-10-08.json"

def read_fixture():
    d = json.loads(DATA.read_text(encoding="utf8"))
    assert d["source"]["png_git_blob_sha1"] == "127d8772912ffc499e5afaffe321d5bab7e920df"
    assert d["historic_witness"]["png_sha256"] == "ae685557122be8562028d8a1c4384c954a760bc4e42e6877c29391d810892d12"
    assert d["historic_witness"]["width"] == 916
    assert d["historic_witness"]["height"] == 913
    assert d["historic_witness"]["white_pixel_threshold"] == 200
    assert d["historic_witness"]["white_pixel_count"] == 2577
    assert d["stage"]["union_exact_white_count"] == 2070
    assert d["stage"]["union_false_positives"] == 0
    assert d["stage"]["unexplained_historic_white_count"] == 507
    assert sum(x["source_color_crop_count"] for x in d["five_registered_layers"]) == 2117
    assert len(d["five_registered_layers"]) == 5
    assert len({x["rgb"] for x in d["five_registered_layers"]}) == 5
    assert all(x["source_color_crop_count"] == x["historic_white_overlap"]
               for x in d["five_registered_layers"])
    assert d["limits"]["remaining_sixth_nonblack_source_color_confirmed"] is False
    return d


def replay(d, source_png, historic_png):
    from PIL import Image
    import numpy as np

    def image_and_bytes(path):
        raw = Path(path).read_bytes()
        return Image.open(path), raw

    im, raw = image_and_bytes(source_png)
    assert im.size == (2048,4096), im.size
    sha = sha256(raw).hexdigest()
    assert sha == d["source"]["png_sha256"], sha
    img = np.asarray(im.convert("RGB"))
    assert img.shape == (4096,2048,3)

    old, oldbytes = image_and_bytes(historic_png)
    assert old.size == (916,913), old.size
    witness_sha=sha256(oldbytes).hexdigest()
    assert witness_sha == d["historic_witness"]["png_sha256"], witness_sha
    witness=np.asarray(old.convert("RGB"))[:,:,0] > 200
    assert witness.sum() == 2577

    recovered=np.zeros_like(witness)
    summary=[]
    for layer in d["five_registered_layers"]:
        x,y=layer["crop_start_xy"]
        rgb=tuple(bytes.fromhex(layer["rgb"]))
        marks=np.all(img[y:y+913,x:x+916,:] == rgb,axis=2)
        n=int(marks.sum())
        overlap=int((marks & witness).sum())
        new=int((marks & ~recovered).sum())
        bad=int((marks & ~witness).sum())
        assert (n,overlap,bad,new) == (
            layer["source_color_crop_count"],
            layer["historic_white_overlap"],
            0,
            layer["new_white_pixel_count"]
        ), (layer,n,overlap,bad,new)
        recovered |= marks
        summary.append({"rgb":layer["rgb"],"offset":[x,y],
                        "captured":n,"new":new,"false":bad})

    assert int(recovered.sum()) == 2070
    assert int((recovered & ~witness).sum()) == 0
    assert int((witness & ~recovered).sum()) == 507

    # Exact negative: do not retroactively treat the sixth 020206
    # source-colour candidate as verified, because this one cropping
    # produces **309 false pixels**.
    s=d["candidate_sixth_color_negative_control"]
    x,y=s["tested_offset_xy"]
    rgb=tuple(bytes.fromhex(s["rgb"]))
    raw_candidate=np.all(img[y:y+913,x:x+916,:]==rgb,axis=2)
    assert (int(raw_candidate.sum()),int((raw_candidate&witness).sum()),
            int((raw_candidate&~witness).sum())) == (560,251,309)

    return {"historic_reference_sha256":witness_sha,
            "source_sha256":sha,"five_layers":summary,
            "positive_white":int(recovered.sum()),"false_white":0,
            "remaining_white":507,"status":"PASS"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",help="Original gate-98 2048x4096 PNG, byte-pinned")
    p.add_argument("--witness",help="2019 Game Detectives 916x913 PNG")
    args=p.parse_args()
    d=read_fixture()
    if bool(args.source) != bool(args.witness):
        p.error("--source and --witness are required together")
    if args.source:
        result=replay(d,args.source,args.witness)
    else:
        result={
            "status":"fixture metadata verified; full pixel verification requires source+2019 witness",
            "layer_count":5,
            "historic_white":2577,
            "recovered_white":2070,
            "false_positive_white":0,
            "remaining_white":507
        }
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()

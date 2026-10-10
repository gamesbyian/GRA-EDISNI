#!/usr/bin/env python3
"""Source-verified cover scan retrieval + coordinate-index contact sheets.

Downloads only six pinned public GitHub export assets. Raw byte provenance
must match *original* Git blob SHA1, NOT an image rendition or GitHub tool's
UTF-8 conversion. The outputs are diagnostic presentation aids for manual
source-art comparison. They NEVER align foreground stickers or optimize a
source-to-source transform.

Designed for one bounded GitHub Actions run. Offline --self-test checks
geometry and manuscript generation without any internet access.
"""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

REPO = "gamesbyian/playdead-unofficial-exports"
BASE = f"https://raw.githubusercontent.com/{REPO}/master/assets/"
SIZE_CAP = 32 * 1024 * 1024
SOURCES = (
    {"name": "INSIDE_A-5d197786f158c567.JPG",
     "git_blob": "875403acac93d83a8acae97e14240c35b88d33ab",
     "role": "original 2020 archived high-resolution INSIDE interior scan",
     "expected_size": [6552, 5040]},
    {"name": "INSIDE_B-80fbff1237c37913.JPG",
     "git_blob": "d533d4161f0572b65d134d54f4fa6477029f2d64",
     "role": "original 2020 archived high-resolution INSIDE exterior scan",
     "expected_size": [6552, 5040]},
    {"name": "image-7be117e2c68d1b1e.png",
     "git_blob": "40039a204800383f69c1b0e4475edcc0989944ef",
     "role": "archived historical partial acorn cover crop"},
    {"name": "image-46edcfb62af0b550.png",
     "git_blob": "24b6429bfab9557760313401f3cb2184664fada6",
     "role": "archived historical acorn reference comparison"},
    {"name": "image-21b86ef8e34e269b.png",
     "git_blob": "c07e87d72a92d4181b1014f3a8269e086a4ef471",
     "role": "archived historical cover planet-family crop"},
    {"name": "image-d6d0d0f76ab751ca.png",
     "git_blob": "b6216e584a62e44ae0594cb881c9ad27ef5266fe",
     "role": "archived historical cover graph-family crop"},
)

class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        p = urlparse(newurl)
        if p.scheme != "https" or p.hostname not in {
            "raw.githubusercontent.com", "github.com", "objects.githubusercontent.com",
            "release-assets.githubusercontent.com"
        }:
            raise ValueError(f"Refusing redirect to {p.scheme}://{p.hostname}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() +
                        b"\x00" + data).hexdigest()


def acquire(source, output: Path):
    url = BASE + source["name"]
    opener = build_opener(SafeRedirect())
    request = Request(url, headers={"User-Agent": "INSIDE-ARG-source-witness/1.0",
                                    "Accept": "application/octet-stream"})
    with opener.open(request, timeout=40) as stream:
        if int(stream.headers.get("Content-Length", "0")) > SIZE_CAP:
            raise ValueError("Historical source exceeds fixed size cap")
        data = stream.read(SIZE_CAP+1)
        if len(data) > SIZE_CAP:
            raise ValueError("Historical source exceeds fixed size cap")
    digest = git_blob_sha(data)
    if digest != source["git_blob"]:
        raise ValueError(f"{source['name']}: original Git blob SHA mismatch: {digest}")
    if source["name"].lower().endswith(".jpg") and not data.startswith(b"\xff\xd8\xff"):
        raise ValueError("Not an original JPEG")
    if source["name"].lower().endswith(".png") and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Not an original PNG")
    from PIL import Image
    with Image.open(io.BytesIO(data)) as im:
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        dimensions = list(im.size)
    if source.get("expected_size") and dimensions != source["expected_size"]:
        raise ValueError(f"{source['name']}: unexpected dimensions: {dimensions}")
    path = output / "verified_source" / source["name"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {**source,"sha256":hashlib.sha256(data).hexdigest(),
            "bytes":len(data),"size_px":dimensions,"download":url,
            "verified_git_blob":True,"output":str(path.relative_to(output))}


def canvas_sheet(img, title, filename, out, cols=4, rows=3):
    from PIL import Image, ImageDraw, ImageFont
    width, height = img.size
    cell_w, cell_h = 500, 410
    head = 60
    sheet = Image.new("RGB", (cols*cell_w, rows*(cell_h+head)), "white")
    draw = ImageDraw.Draw(sheet)
    for gy in range(rows):
        for gx in range(cols):
            box=(width*gx//cols,height*gy//rows,
                 width*(gx+1)//cols,height*(gy+1)//rows)
            original=img.crop(box).convert("RGB")
            original.thumbnail((cell_w-12,cell_h-12), Image.Resampling.LANCZOS)
            x,y=gx*cell_w+(cell_w-original.width)//2,gy*(cell_h+head)+head
            sheet.paste(original,(x,y))
            draw.text((gx*cell_w+8,gy*(cell_h+head)+8),
                      f"{title}  tile ({gx+1},{gy+1})",fill="black")
            draw.text((gx*cell_w+8,gy*(cell_h+head)+28),
                      f"pixel bounds {box}",fill="black")
    sheet.save(out/filename, optimize=True)


def summary_pair(images, out):
    from PIL import Image, ImageDraw
    thumb_w, thumb_h = 1400, 1100
    sheet=Image.new("RGB",(thumb_w*len(images),thumb_h+65),"white")
    draw=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate(images):
        small=im.copy()
        small.thumbnail((thumb_w-12,thumb_h-12), Image.Resampling.LANCZOS)
        sheet.paste(small,(i*thumb_w+(thumb_w-small.width)//2,65+
                           (thumb_h-small.height)//2))
        draw.text((i*thumb_w+15,14),f"ARCHIVED ORIGINAL: {label}",fill="black")
        draw.text((i*thumb_w+15,36),
                  "Presentation overview only; see hash-verified full native source",fill="black")
    sheet.save(out/"cover_original_pair_overview.png",optimize=True)


def create_presentation(output, metadata):
    from PIL import Image, ImageDraw
    covers=[]
    for item in metadata:
        path=output/item["output"]
        if "expected_size" not in item:
            continue
        with Image.open(path) as im:
            rgb=im.convert("RGB")
        label="A (internal)" if "INSIDE_A" in item["name"] else "B (external)"
        covers.append((label,rgb))
        canvas_sheet(rgb,label,
                     "cover_"+("A" if "INSIDE_A" in item["name"] else "B")+
                     "_coordinate_index.png",output)
    if len(covers)==2:
        summary_pair(covers,output)
    previews=[]
    for item in metadata:
        if "expected_size" in item:
            continue
        with Image.open(output/item["output"]) as im:
            rgb=im.convert("RGB")
        enlarged=rgb.resize((rgb.width*5,rgb.height*5),
                            Image.Resampling.NEAREST)
        fname="reference_"+item["name"]
        enlarged.save(output/fname)
        previews.append({"source":item["name"],"artifact":fname,
                         "note":"5x NEAREST-NEIGHBOR viewing only, not an alleged original enlarged asset"})
    return previews


def offline_self_test(output):
    from PIL import Image
    output.mkdir(parents=True,exist_ok=True)
    img=Image.new("RGB",(240,180))
    for y in range(180):
        for x in range(240):
            img.putpixel((x,y),((x*255)//240,(y*255)//180,(x+y)%256))
    canvas_sheet(img,"SYNTHETIC TEST ONLY",
                 "synthetic_coordinate_grid.png",output,3,3)
    assert git_blob_sha(b"abc") == "f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f"
    return {"test":"only source digest+tiler code",
            "result":"pass","source_pixels_authenticated":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("cover_source_artifacts"))
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    if args.self_test:
        print(json.dumps(offline_self_test(args.output),indent=2))
        return
    completed=[]
    errors=[]
    for item in SOURCES:
        try:
            completed.append(acquire(item,args.output))
        except Exception as exc:
            errors.append({"source":item["name"],"error":str(exc)})
    previews=[]
    if len(completed)==len(SOURCES):
        previews=create_presentation(args.output,completed)
    report={
        "purpose":"source-verified original cover contact sheets; no sticker decoding",
        "provenance":"gamesbyian/playdead-unofficial-exports original Git blob identities",
        "verified_sources":completed,
        "errors":errors,
        "previews":previews,
        "cover_running_man_pixel_identity":"not evaluated; original 2021 registered running-man target source not authenticated",
        "no_transform_fit":True,
    }
    (args.output/"report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in report.items()
                      if k!="verified_sources"},indent=2))
    if errors:
        raise SystemExit(f"Could not verify {len(errors)} pinned source(s): consult report.json")


if __name__=="__main__":
    main()

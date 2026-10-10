#!/usr/bin/env python3
"""Acquire only source-tree-authenticated 2021 acorn/running-man archive assets.

The original June 2021 Discord CDN link is dead (HTTP 404), but a
public archived Discord export's *real* Git asset tree lists an acorn
video, a related solution GIF and running-man assets. Pin by exact path
and original Git blob SHA1. Do not infer that the saved video is the
specific June 2021 message until visual/context comparison is made.

Produces intact originals, SHA256 manifest, only presentation-sized
derived preview images and bounded ffmpeg key frames.
"""
import hashlib
import json
import pathlib
import subprocess
import urllib.parse
import urllib.request

REPO="gamesbyian/playdead-unofficial-exports"
BASE=f"https://raw.githubusercontent.com/{REPO}/master/assets/"
ROOT=pathlib.Path("acorn_2021_original_export")
CAP=16*1024*1024
ASSETS=[
    ("acorn-c53ef409753e9fa2.mp4","0480da448164c0a1bbd115f1065ffd9d68f70bf2",408693,"historical candidate for original acorn demonstration"),
    ("SPOILER_acorn_solution_hidden_message-d83e87eda3958d3f.gif","fedfc28f1c0c02db99bdf951f662f618fb1af1f2",129101,"archived claimed hidden-message animation"),
    ("RunningMan-2d6ba6bee8527a23.png","57ce0d872eec1016bf8d572800d793514cb78617",63728,"archived running-man art A"),
    ("RunningMan-ece91af0a7bbadc1.png","ae84d0dca1de6cce8d3bb0339d04b596fbd12d63",80441,"archived running-man art B"),
    ("running_man-1be468408953c7de.png","78548e87469b54d64d9b2fda2e7e71fc7241b744",108538,"archived running-man art C"),
    ("running_man2.0-c9d06a3dc7fd0ad5.JPG","ee49bef10092c2e1a13b10aed8f3dc25e3dc4c5a",7661,"archived running-man image reworking"),
    ("Inside_pc_acorn_fixed-081372579ea1409c.png","c04ac01fc6f3f3af05d00f7e2b104396ade440e1",8234,"archived canonical-ish PC acorn art"),
    ("Inside_pc_acorn_fixed-9cbfe9261ce9d333.png","c92a39e7dd42d1cf35a7b312c2f23a705df49b43",11116,"alternate PC acorn raster"),
    ("Acorn_mirrored-ef05ed3fe6490745.jpg","c99dff3e49e2f6bb441a042956e2aed7be0b150a",27783,"archived mirrored acorn reference"),
]

def git_sha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()

def download(name,sha,size):
    url=BASE+urllib.parse.quote(name)
    req=urllib.request.Request(url,headers={"User-Agent":"INSIDE-original-2021-acorn-export/1.0"})
    with urllib.request.urlopen(req,timeout=45) as resp:
        data=resp.read(CAP+1)
    if len(data)!=size or len(data)>CAP:
        raise ValueError(f"{name}: expected {size}, got {len(data)} bytes")
    if git_sha(data)!=sha:
        raise ValueError(f"{name}: source Git blob digest mismatch")
    if name.endswith(".mp4") and data[4:8]!=b"ftyp":
        raise ValueError("MP4 source magic invalid")
    if name.endswith(".png") and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("PNG source magic invalid")
    if name.endswith(".gif") and not data.startswith((b"GIF89a",b"GIF87a")):
        raise ValueError("GIF source magic invalid")
    if name.endswith((".jpg",".JPG")) and not data.startswith(b"\xff\xd8\xff"):
        raise ValueError("JPEG source magic invalid")
    out=ROOT/"verified_source"/name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)
    return {"path":name,"git_blob_sha1":sha,"sha256":hashlib.sha256(data).hexdigest(),
            "bytes":size,"original_export_url":url}

def previews(rows):
    from PIL import Image,ImageDraw
    ROOT.mkdir(exist_ok=True)
    gallery=[]
    for row in rows:
        path=ROOT/"verified_source"/row["path"]
        if row["path"].endswith(".mp4"):
            continue
        try:
            with Image.open(path) as im:
                n=getattr(im,"n_frames",1)
                row["size_px"]=list(im.size)
                row["n_frames"]=n
                im.seek(0)
                still=im.convert("RGB")
                still.thumbnail((900,640))
                still.save(ROOT/("preview_"+row["path"].replace(".gif",".png").replace(".JPG",".png")))
                gallery.append((row["path"],still))
                if n>1:
                    for k in sorted(set([0,n//4,n//2,(3*n)//4,n-1])):
                        im.seek(k)
                        fr=im.convert("RGBA")
                        fr.thumbnail((1200,800))
                        fr.save(ROOT/f"gif_{k:03d}.png")
        except Exception as ex:
            row["preview_error"]=str(ex)
    if gallery:
        W,H=1200,480
        sheet=Image.new("RGB",(2*W,((len(gallery)+1)//2)*H),"white")
        draw=ImageDraw.Draw(sheet)
        for i,(name,im) in enumerate(gallery):
            x=(i%2)*W;y=(i//2)*H
            draw.text((x+15,y+12),name,fill="black")
            sheet.paste(im,(x+(W-im.width)//2,y+42+(H-48-im.height)//2))
        sheet.save(ROOT/"running_man_acorn_archive_atlas.png")

def video_frames():
    f=ROOT/"verified_source"/"acorn-c53ef409753e9fa2.mp4"
    target=ROOT/"video_stills"
    target.mkdir(exist_ok=True)
    summary={"ffmpeg_stills":"unavailable"}
    try:
        proc=subprocess.run(["ffprobe","-v","error","-show_entries",
                "format=duration,size:stream=codec_name,width,height",
                "-of","json",str(f)],capture_output=True,text=True,timeout=15)
        if proc.returncode==0:
            summary["video_probe"]=json.loads(proc.stdout)
        proc=subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error",
                "-i",str(f),"-vf","fps=1,scale=640:-1","-frames:v","36",
                str(target/"frame_%03d.png")],
                capture_output=True,text=True,timeout=90)
        summary["ffmpeg_stills"]="ok" if proc.returncode==0 else proc.stderr[:500]
        summary["n_stills"]=len(list(target.glob("frame_*.png")))
    except Exception as e:
        summary["ffmpeg_stills"]="error "+str(e)[:500]
    return summary

def main():
    ROOT.mkdir(exist_ok=True)
    rows=[];errors=[]
    for name,sha,size,role in ASSETS:
        try:
            item=download(name,sha,size)
            item["role"]=role
            rows.append(item)
        except Exception as e:
            errors.append({"path":name,"error":str(e)})
    if rows:
        previews(rows)
    v=video_frames() if any(x["path"].endswith(".mp4") for x in rows) else {}
    report={
        "origin":"public immutable Git tree gamesbyian/playdead-unofficial-exports/assets; tree SHA 4eb26bc0cba73425dc5ed7d03f1d4ba78fee929e",
        "purpose":"recover 2021 acorn demo candidate and RunningMan source masks by pinned Git content identity",
        "archival_CDN_2021_direct_result":"HTTP 404, separate probe run 38025078818",
        "all_sources":rows,"errors":errors,
        "video":v,
        "identity_warning":"same-archive filenames are not by themselves proof exact identity with June 2021 Discord attachment; visual validation needed",
        "no_CE_sticker_observations_changed":True}
    (ROOT/"report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in report.items() if k!="all_sources"},indent=2))
    if errors:raise SystemExit(f"{len(errors)} source errors; no substitutions")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Reproduce the non-generative L14 / Inside Gaming forensic review bundle.

All outputs are derived only from source video pixels (plus the known #324
sticker photo used as a layout/degradation reference). No generative model,
inpainting, super-resolution synthesis, or OCR reconstruction is used.
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from skimage.restoration import richardson_lucy

START_ABS = 73.5
FPS = 30000 / 1001


def ffmpeg_native(video: Path, out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", "3.5", "-i", str(video), "-t", "4.5", "-vsync", "0",
        str(out / "frame-%04d.png"),
    ], check=True)
    return sorted(out.glob("frame-*.png"))


def label(im: Image.Image, text: str, pad: int = 28) -> Image.Image:
    c = Image.new("RGB", (im.width, im.height + pad), "white")
    c.paste(im, (0, 0))
    ImageDraw.Draw(c).text((5, im.height + 5), text, fill="black")
    return c


def sheet(items: list[Image.Image], cols: int, out: Path, quality: int = 94) -> None:
    if not items:
        return
    w=max(i.width for i in items); h=max(i.height for i in items)
    rows=math.ceil(len(items)/cols)
    canvas=Image.new("RGB",(cols*w,rows*h),"white")
    for k,im in enumerate(items):
        canvas.paste(im,((k%cols)*w,(k//cols)*h))
    canvas.save(out, quality=quality)


def crop_frame(p: Path, box=(1580, 410, 1920, 900)) -> Image.Image:
    return Image.open(p).convert("RGB").crop(box)


def sec_for(n: int) -> float:
    return START_ABS + (n-1)/FPS


def enlarge(im: Image.Image, width: int, nearest=False) -> Image.Image:
    h=round(im.height*width/im.width)
    return im.resize((width,h), Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)


def make_contact(frames: list[Path], indices: list[int], out: Path, cols=4, box=(1500,360,1920,940), width=300):
    ims=[]
    for n in indices:
        p=frames[n-1]
        cr=Image.open(p).convert("RGB").crop(box)
        cr=enlarge(cr,width)
        ims.append(label(cr,f"{sec_for(n):.3f}s  f{n}"))
    sheet(ims,cols,out)


def make_enhanced(frames: list[Path], indices: list[int], out: Path):
    ims=[]
    for n in indices:
        cr=crop_frame(frames[n-1])
        g=ImageOps.grayscale(cr)
        g=ImageOps.autocontrast(g)
        g=ImageEnhance.Contrast(g).enhance(1.6)
        g=g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=160, threshold=2))
        g=enlarge(g.convert("RGB"),330)
        ims.append(label(g,f"classical contrast/sharpen  {sec_for(n):.3f}s"))
    sheet(ims,3,out)


def make_channels(frame: Path, out: Path):
    im=np.array(crop_frame(frame))
    chans=[]
    names=["R","G","B"]
    for i,name in enumerate(names):
        ch=Image.fromarray(im[:,:,i]).convert("L")
        ch=ImageOps.autocontrast(ch)
        chans.append(label(enlarge(ch.convert("RGB"),450),name))
    gray=ImageOps.autocontrast(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)))
    chans.append(label(enlarge(gray.convert("RGB"),450),"grayscale"))
    sheet(chans,2,out)


def make_deconv(frame: Path, out: Path):
    cr=np.array(crop_frame(frame).convert("L"),dtype=np.float32)/255
    psf=np.ones((5,5),dtype=np.float32); psf/=psf.sum()
    de=richardson_lucy(cr,psf,num_iter=14,clip=False)
    de=np.clip(de*255,0,255).astype(np.uint8)
    a=enlarge(Image.fromarray((cr*255).astype(np.uint8)).convert("RGB"),500)
    b=enlarge(Image.fromarray(de).convert("RGB"),500)
    sheet([label(a,"native grayscale"),label(b,"Richardson-Lucy, 5x5 PSF / 14 iterations")],2,out)


def make_aligned_stack(frames: list[Path], indices: list[int], out: Path):
    crops=[]
    for n in indices:
        arr=np.array(crop_frame(frames[n-1]).convert("L"),dtype=np.uint8)
        crops.append(arr)
    ref=crops[len(crops)//2]
    aligned=[]
    for img in crops:
        warp=np.eye(2,3,dtype=np.float32)
        try:
            cv2.findTransformECC(ref.astype(np.float32)/255,img.astype(np.float32)/255,warp,cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,100,1e-5))
            a=cv2.warpAffine(img,warp,(ref.shape[1],ref.shape[0]),flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_REPLICATE)
        except cv2.error:
            a=img
        aligned.append(a)
    arr=np.stack(aligned).astype(np.float32)
    products=[
        ("mean",arr.mean(0)),
        ("median",np.median(arr,axis=0)),
        ("25th percentile",np.percentile(arr,25,axis=0)),
        ("75th percentile",np.percentile(arr,75,axis=0)),
    ]
    ims=[]
    for name,a in products:
        x=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
        x=ImageOps.autocontrast(x)
        ims.append(label(enlarge(x.convert("RGB"),450),name))
    sheet(ims,2,out)


def make_geometry(frame: Path, ref_path: Path, out: Path):
    src=Image.open(frame).convert("RGB")
    crop=src.crop((1500,350,1920,940))
    d=ImageDraw.Draw(crop)
    # Conservative expected numeral region, based on comparison with known physical labels.
    d.rectangle((180,250,320,390),outline="red",width=5)
    d.text((8,8),"L14 frame: expected serial zone lies under fingers",fill="red")
    ref=Image.open(ref_path).convert("RGB")
    ref.thumbnail((780,720))
    top=label(enlarge(crop,780),"L14: geometry/occlusion review")
    bottom=label(ref.resize((780,round(ref.height*780/ref.width))),"Known #324 physical sticker layout reference")
    sheet([top,bottom],1,out)


def make_serial_strips(frames: list[Path], indices: list[int], out: Path):
    ims=[]
    for n in indices:
        cr=Image.open(frames[n-1]).convert("RGB").crop((1680,500,1920,760))
        ims.append(label(enlarge(cr,400,nearest=True),f"nearest-neighbour  {sec_for(n):.3f}s"))
    sheet(ims,3,out)


def make_rectified(frames: list[Path], indices: list[int], out: Path):
    ims=[]
    for n in indices:
        cr=crop_frame(frames[n-1])
        # Simple affine normalization only; no invented pixels.
        a=np.array(cr)
        h,w=a.shape[:2]
        src=np.float32([[15,40],[w-15,20],[20,h-20]])
        dst=np.float32([[0,0],[w,0],[0,h]])
        M=cv2.getAffineTransform(src,dst)
        r=cv2.warpAffine(a,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        ims.append(label(enlarge(Image.fromarray(r),280),f"affine-normalized f{n}"))
    sheet(ims,3,out)


def make_reference_simulations(ref_path: Path, outdir: Path):
    im=Image.open(ref_path).convert("RGB")
    # Preserve a transparent sanity check: these are degradation simulations,
    # never evidence for L14.
    im.thumbnail((900,900))
    stages=[]
    for i,(scale,blur,q) in enumerate([(0.30,0.6,80),(0.18,1.0,60),(0.11,1.3,45)],1):
        x=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.LANCZOS)
        x=x.filter(ImageFilter.GaussianBlur(blur))
        x=x.resize((im.width,im.height),Image.Resampling.LANCZOS)
        p=outdir/f"clean324_simulated{i if i>1 else ''}.jpg"
        x.save(p,quality=q)
        stages.append(p)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--video",type=Path,required=True)
    ap.add_argument("--reference-sticker",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    native=args.output/"_native"
    frames=ffmpeg_native(args.video,native)

    make_contact(frames,list(range(1,len(frames)+1,5)),args.output/"sticker_all_native_contact.jpg",cols=4)
    make_contact(frames,list(range(1,61,3)),args.output/"early_sticker_frames.jpg",cols=4)
    make_contact(frames,list(range(91,min(len(frames),136)+1,3)),args.output/"late_sticker_frames.jpg",cols=4)
    make_contact(frames,list(range(70,126,4)),args.output/"all_right_edge.jpg",cols=4,box=(1600,380,1920,900))
    make_enhanced(frames,list(range(108,121,2)),args.output/"sticker_enhanced_108_120.jpg")
    make_serial_strips(frames,list(range(100,122,2)),args.output/"serial_strip_nearest.jpg")
    make_channels(frames[108],args.output/"frame109_channels.jpg")
    make_deconv(frames[108],args.output/"deconv_frame109.jpg")
    make_aligned_stack(frames,list(range(104,119)),args.output/"aligned_serial_stack.jpg")
    make_rectified(frames,[106,109,112,115,118,121],args.output/"rectified_stickers.jpg")
    make_geometry(frames[108],args.reference_sticker,args.output/"serial_occlusion_geometry.jpg")

    # Two geometry-focused variants retained because they were useful during review.
    g=Image.open(args.output/"serial_occlusion_geometry.jpg").convert("RGB")
    g.save(args.output/"serial_expected_region.jpg",quality=94)
    s=Image.open(args.output/"serial_strip_nearest.jpg").convert("RGB")
    s.save(args.output/"serial_expected_region_detail.jpg",quality=94)

    make_reference_simulations(args.reference_sticker,args.output)

    # Remove extracted source frames: they are reproducible and too bulky for Git.
    for p in native.glob("*.png"): p.unlink()
    native.rmdir()


if __name__=="__main__":
    main()

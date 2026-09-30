#!/usr/bin/env python3
"""Build consensus A-I background-tile masters from noisy sticker photographs.

The pipeline deliberately treats every photograph as noisy evidence:
- discover local/upstream sticker images whose filenames contain a 3-digit serial;
- derive tile A-I from the documented serial modulo-9 cycle;
- rectify the sticker to a common square canvas using its bright quadrilateral;
- crop the printed background field above the serial;
- detect and mask the large black foreground symbol independently in each sample;
- photometrically normalize and align samples within each tile class;
- take a masked per-pixel median; only the small pixels hidden by every symbol require inpainting.

Outputs include the nine masters, enhanced views, support maps, contact sheet and provenance CSV.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
from PIL import Image, ImageFile, UnidentifiedImageError

# Strict input policy: do not let Pillow silently accept truncated source photos.
ImageFile.LOAD_TRUNCATED_IMAGES = False

TILES = "ABCDEFGHI"
SERIAL_RE = re.compile(r"(?<!\d)(\d{3})(?!\d)")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


@dataclass
class Sample:
    path: Path
    serial: int
    tile: str
    source_root: Path
    sha256: str
    original_w: int = 0
    original_h: int = 0
    rectification: str = ""
    alignment_score: float = float("nan")
    included: bool = False
    note: str = ""


def tile_for_serial(serial: int) -> str:
    return TILES[(serial - 1) % 9]


def discover_images(roots: Iterable[Path]) -> list[Sample]:
    seen_hashes: set[str] = set()
    samples: list[Sample] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
                continue
            m = SERIAL_RE.search(path.stem)
            if not m:
                m = SERIAL_RE.search(str(path.relative_to(root)))
            if not m:
                continue
            serial = int(m.group(1))
            if serial < 1 or serial > 600:
                continue
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
            if digest in seen_hashes:
                continue
            seen_hashes.add(digest)
            samples.append(Sample(path, serial, tile_for_serial(serial), root, digest))
    return sorted(samples, key=lambda s: (s.tile, s.serial, str(s.path)))


def order_quad(pts: np.ndarray) -> np.ndarray:
    pts = np.asarray(pts, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    return np.array([
        pts[np.argmin(s)],
        pts[np.argmin(d)],
        pts[np.argmax(s)],
        pts[np.argmax(d)],
    ], dtype=np.float32)


def detect_sticker_quad(image: np.ndarray) -> tuple[np.ndarray, str] | tuple[None, str]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    candidates: list[tuple[float, np.ndarray, str]] = []
    for pct in (55, 65, 75):
        th = np.percentile(blur, pct)
        mask = (blur >= th).astype(np.uint8) * 255
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8), iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area < 0.12 * w * h:
                continue
            peri = cv2.arcLength(c, True)
            poly = cv2.approxPolyDP(c, 0.025 * peri, True)
            if len(poly) == 4 and cv2.isContourConvex(poly):
                quad = order_quad(poly[:, 0, :])
                box_area = abs(cv2.contourArea(quad.astype(np.float32)))
                if box_area <= 0:
                    continue
                rectangularity = min(1.0, area / box_area)
                score = area * (0.65 + 0.35 * rectangularity)
                candidates.append((score, quad, f"quad-p{pct}"))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1], candidates[0][2]
    th = np.percentile(blur, 60)
    mask = (blur >= th).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8), iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, "no-contour"
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 0.1 * w * h:
        return None, "tiny-contour"
    return order_quad(cv2.boxPoints(cv2.minAreaRect(c))), "min-area-rect"


def warp_sticker(image: np.ndarray, quad: np.ndarray, size: int = 1200) -> np.ndarray:
    dst = np.array([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(quad.astype(np.float32), dst)
    return cv2.warpPerspective(image, H, (size, size), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def crop_background_field(sticker: np.ndarray, out_w: int = 900, out_h: int = 650) -> np.ndarray:
    h, w = sticker.shape[:2]
    x0, x1 = int(0.10 * w), int(0.90 * w)
    y0, y1 = int(0.12 * h), int(0.76 * h)
    return cv2.resize(sticker[y0:y1, x0:x1], (out_w, out_h), interpolation=cv2.INTER_AREA)


def normalize_gray(field: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(field, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.GaussianBlur(gray, (0, 0), 35)
    flat = gray - bg + 180.0
    lo, hi = np.percentile(flat, [1.5, 99.0])
    if hi - lo < 5:
        lo, hi = float(flat.min()), float(flat.max() + 1)
    return np.clip((flat - lo) * (235.0 / (hi - lo)) + 10.0, 0, 255).astype(np.uint8)


def symbol_mask(gray: np.ndarray) -> np.ndarray:
    h, w = gray.shape
    center = np.zeros_like(gray, np.uint8)
    center[int(.08*h):int(.93*h), int(.12*w):int(.88*w)] = 255
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    t = min(85, int(np.percentile(blur[center > 0], 16)))
    dark = ((blur < t) & (center > 0)).astype(np.uint8) * 255
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8), iterations=2)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(dark, 8)
    mask = np.zeros_like(gray, np.uint8)
    for i in range(1, n):
        x, y, ww, hh, area = stats[i]
        cx, cy = x + ww / 2, y + hh / 2
        if area < 0.004 * w * h:
            continue
        if not (0.15*w <= cx <= 0.85*w and 0.10*h <= cy <= 0.90*h):
            continue
        if ww > 0.92*w or hh > 0.92*h:
            continue
        mask[labels == i] = 255
    if np.any(mask):
        mask = cv2.dilate(mask, np.ones((17, 17), np.uint8), iterations=1)
    return mask


def align_to_reference(ref: np.ndarray, img: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    ref_e = cv2.Canny(ref, 25, 80)
    img_e = cv2.Canny(img, 25, 80)
    img_e = img_e.copy()
    img_e[mask > 0] = 0
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        score, warp = cv2.findTransformECC(
            ref_e.astype(np.float32) / 255.0,
            img_e.astype(np.float32) / 255.0,
            warp,
            cv2.MOTION_AFFINE,
            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-6),
            None,
            3,
        )
    except cv2.error:
        score = float("nan")
        warp = np.eye(2, 3, dtype=np.float32)
    h, w = ref.shape
    aligned = cv2.warpAffine(img, warp, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
    aligned_mask = cv2.warpAffine(mask, warp, (w, h), flags=cv2.INTER_NEAREST | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    return aligned, aligned_mask, float(score)


def masked_median(images: list[np.ndarray], masks: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    stack = np.stack(images).astype(np.float32)
    mstack = np.stack(masks) > 0
    stack[mstack] = np.nan
    with np.errstate(all="ignore"):
        master = np.nanmedian(stack, axis=0)
    support = np.sum(~mstack, axis=0).astype(np.uint16)
    missing = ~np.isfinite(master)
    fallback = np.median(np.stack(images).astype(np.float32), axis=0)
    master[missing] = fallback[missing]
    out = np.clip(master, 0, 255).astype(np.uint8)
    if np.any(missing):
        hole = cv2.dilate(missing.astype(np.uint8) * 255, np.ones((5, 5), np.uint8), iterations=1)
        out = cv2.inpaint(out, hole, 5, cv2.INPAINT_TELEA)
    return out, support, missing.astype(np.uint8) * 255


def enhance(gray: np.ndarray) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(10, 10))
    e = clahe.apply(gray)
    blur = cv2.GaussianBlur(e, (0, 0), 1.2)
    return cv2.addWeighted(e, 1.45, blur, -0.45, 0)


def make_contact_sheet(images: dict[str, np.ndarray], out: Path) -> None:
    if not images:
        return
    cell_h, cell_w = next(iter(images.values())).shape[:2]
    sheet = np.full((cell_h*3 + 120, cell_w*3, 3), 245, np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for idx, tile in enumerate(TILES):
        if tile not in images:
            continue
        r, c = divmod(idx, 3)
        img = cv2.cvtColor(images[tile], cv2.COLOR_GRAY2BGR)
        y0 = r * cell_h + 40
        x0 = c * cell_w
        sheet[y0:y0+cell_h, x0:x0+cell_w] = img
        cv2.putText(sheet, tile, (x0+20, y0-10), font, 1.1, (20,20,20), 2, cv2.LINE_AA)
    cv2.imwrite(str(out), sheet)


def write_provenance(samples: list[Sample], out: Path) -> None:
    fields = ["tile","serial","path","source_root","sha256","original_w","original_h","rectification","alignment_score","included","note"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in samples:
            w.writerow({
                "tile": s.tile, "serial": f"{s.serial:03d}", "path": str(s.path),
                "source_root": str(s.source_root), "sha256": s.sha256,
                "original_w": s.original_w, "original_h": s.original_h,
                "rectification": s.rectification,
                "alignment_score": "" if math.isnan(s.alignment_score) else f"{s.alignment_score:.6f}",
                "included": int(s.included), "note": s.note,
            })


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+", type=Path, help="directories to scan recursively")
    ap.add_argument("--out", type=Path, default=Path("artifacts/background-tile-masters"))
    ap.add_argument("--min-samples", type=int, default=2)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    samples = discover_images(args.roots)
    by_tile: dict[str, list[tuple[Sample, np.ndarray, np.ndarray]]] = {t: [] for t in TILES}
    for s in samples:
        # Decode through Pillow first. This keeps harmless PNG metadata warnings
        # away from libpng/OpenCV while rejecting truncated/corrupt image streams
        # before they can contribute pixels to a consensus master.
        try:
            with Image.open(s.path) as probe:
                probe.verify()
            with Image.open(s.path) as src:
                rgb = np.asarray(src.convert("RGB"))
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
            kind = "oversize-image quarantine" if isinstance(exc, Image.DecompressionBombError) else "corrupt-image quarantine"
            s.note = f"{kind}: {type(exc).__name__}: {exc}"
            continue
        if rgb.size == 0:
            s.note = "corrupt-image quarantine: empty decoded image"
            continue
        img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        s.original_h, s.original_w = img.shape[:2]
        quad, method = detect_sticker_quad(img)
        s.rectification = method
        if quad is None:
            s.note = "no sticker quadrilateral"
            continue
        field = crop_background_field(warp_sticker(img, quad))
        gray = normalize_gray(field)
        mask = symbol_mask(gray)
        masked_fraction = float(np.mean(mask > 0))
        if masked_fraction > 0.45 or float(np.std(gray)) < 4.0:
            s.note = f"quality reject masked_fraction={masked_fraction:.3f} std={np.std(gray):.2f}"
            continue
        by_tile[s.tile].append((s, gray, mask))
    enhanced_masters: dict[str, np.ndarray] = {}
    summary_rows = []
    for tile in TILES:
        rows = by_tile[tile]
        if len(rows) < args.min_samples:
            summary_rows.append((tile, len(rows), "insufficient samples"))
            continue
        sharpness = [float(cv2.Laplacian(r[1], cv2.CV_64F).var()) for r in rows]
        ref_idx = int(np.argmax(sharpness))
        ref = rows[ref_idx][1]
        aligned_images, aligned_masks = [], []
        for i, (s, gray, mask) in enumerate(rows):
            if i == ref_idx:
                a, m, score = gray, mask, 1.0
            else:
                a, m, score = align_to_reference(ref, gray, mask)
            s.alignment_score = score
            s.included = True
            aligned_images.append(a)
            aligned_masks.append(m)
        master, support, missing = masked_median(aligned_images, aligned_masks)
        enhanced = enhance(master)
        enhanced_masters[tile] = enhanced
        cv2.imwrite(str(args.out / f"{tile}.png"), master)
        cv2.imwrite(str(args.out / f"{tile}-enhanced.png"), enhanced)
        support8 = np.clip(support.astype(np.float32) / max(1, len(aligned_images)) * 255.0, 0, 255).astype(np.uint8)
        cv2.imwrite(str(args.out / f"{tile}-support.png"), support8)
        cv2.imwrite(str(args.out / f"{tile}-inpainted-mask.png"), missing)
        summary_rows.append((tile, len(rows), f"reference={rows[ref_idx][0].serial:03d}"))
    make_contact_sheet(enhanced_masters, args.out / "A-I-contact-sheet.png")
    write_provenance(samples, args.out / "provenance.csv")
    with (args.out / "README.md").open("w", encoding="utf-8") as f:
        f.write("# A-I background tile masters\n\n")
        f.write("Consensus reconstructions from registered sticker photographs. `A.png`..`I.png` are conservative grayscale masters; `*-enhanced.png` are viewing copies; `*-support.png` records how many samples supplied each pixel; `*-inpainted-mask.png` marks pixels hidden by every available foreground symbol and therefore filled from neighbors.\n\n")
        f.write("| tile | accepted samples | note |\n|---|---:|---|\n")
        for tile, n, note in summary_rows:
            f.write(f"| {tile} | {n} | {note} |\n")
    print(f"discovered {len(samples)} unique serial-tagged images")
    for tile, n, note in summary_rows:
        print(f"{tile}: {n} {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

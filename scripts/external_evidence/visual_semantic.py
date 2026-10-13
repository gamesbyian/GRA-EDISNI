#!/usr/bin/env python3
"""Optional CLIP object/scene ranking on unreviewed CE images (not an evidence classifier).

Dependencies (separate opt-in environment): Pillow, torch, transformers.
Default is cache-only. Network model download requires --allow-model-download.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageOps

MODEL = "openai/clip-vit-base-patch32"
LABELS = {
    "ce-numbered-wrapper": "A close-up photograph of a small numbered paper label or sticker on black protective packaging plastic",
    "ce-premium-box": "A real collector holding a large red INSIDE collector's edition presentation box with black protective foam",
    "ce-huddle-figurine": "A photograph of the pale pink silicone Huddle sculpture from Playdead INSIDE collector's edition on its display stand",
    "ce-art-cards": "A photograph of concept-art print cards and little boy figurine from Playdead INSIDE collector's edition",
    "ce-unboxing": "An amateur tabletop photograph of someone unboxing and unpacking the large INSIDE iam8bit collector's edition box",
    "standalone-disc": "A photograph of a single blue PlayStation 4 video game case for INSIDE without any collector's edition packaging",
    "publisher-promo": "A professionally lit advertising photograph of video game collectible merchandise arranged on a backdrop",
    "game-screenshot": "A screen capture from the 2016 side scrolling video game INSIDE made by Playdead",
    "unrelated-game": "A photograph of an unrelated video game, console accessory or collectible toy",
}
# Rankings are relative only to these labels. They are NOT probabilities of CE ownership.


def ranking(labels: list[str], logits: list[float]) -> list[dict]:
    if len(labels) != len(logits):
        raise ValueError("label/logit count mismatch")
    return [{"label": label, "relative_logit": round(float(score), 5)}
            for label, score in sorted(zip(labels, logits), key=lambda x: (-x[1], x[0]))]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--index", type=Path, default=Path("visual-evidence-work/candidate-index.json"))
    p.add_argument("--candidate-root", type=Path, default=Path("evidence-work"))
    p.add_argument("--out", type=Path, default=Path("visual-evidence-work/semantic-rankings.json"))
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--allow-model-download", action="store_true")
    args = p.parse_args()
    if not 0 < args.limit <= 2000:
        p.error("limit must be 1..2000")
    items = json.loads(args.index.read_text(encoding="utf-8"))["candidates"]
    if not items:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"model": MODEL, "candidates": [], "status": "empty"}) + "\n")
        return
    try:
        import torch
        from transformers import AutoProcessor, CLIPModel
    except ImportError as exc:
        raise SystemExit("Install optional 'torch' and 'transformers' to run semantic ranking") from exc
    try:
        processor = AutoProcessor.from_pretrained(MODEL, local_files_only=not args.allow_model_download)
        model = CLIPModel.from_pretrained(MODEL, local_files_only=not args.allow_model_download)
    except (OSError, ValueError) as exc:
        raise SystemExit("Model unavailable locally. Pre-cache an audited model, or opt in "
                         "with --allow-model-download. Details: " + str(exc)[:200]) from exc
    model.eval()
    labels = list(LABELS)
    prompts = list(LABELS.values())
    root = args.candidate_root.resolve()
    output = []
    errors = []
    for entry in items[:args.limit]:
        candidate = (root / entry["path"]).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            errors.append({"candidate_id": entry["id"], "reason": "missing-or-unsafe-path"})
            continue
        try:
            with Image.open(candidate) as img:
                img = ImageOps.exif_transpose(img).convert("RGB")
                if img.width * img.height > 40_000_000:
                    raise ValueError("image too large")
                features = processor(text=prompts, images=img, return_tensors="pt", padding=True)
            with torch.inference_mode():
                logits = model(**features).logits_per_image[0].cpu().tolist()
            output.append({
                "candidate_id": entry["id"], "path": entry["path"],
                "source_url": entry["source_url"], "rankings": ranking(labels, logits)[:5],
                "review_required": True, "new_sticker_confirmed": False,
            })
        except (OSError, ValueError) as exc:
            errors.append({"candidate_id": entry["id"], "reason": str(exc)[:180]})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "schema_version": 1, "model": MODEL, "inference": "zero-shot-relative-ranking",
        "calibrated_probability": False, "evidence_grade": "candidate-ranking-only",
        "candidates": output, "errors": errors,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ranked {len(output)} candidates, {len(errors)} errors; no evidence promoted")


if __name__ == "__main__":
    main()

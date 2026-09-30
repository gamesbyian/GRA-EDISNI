#!/usr/bin/env python3
"""Extract reconnaissance, scene-change, or dense frame sets with ffmpeg."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def require(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"{name} is required")


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["sample", "scene", "dense"], default="sample")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="Sample interval in seconds for sample mode.")
    parser.add_argument("--start", help="ffmpeg start timestamp, e.g. 00:07:10")
    parser.add_argument("--duration", type=float, help="bounded duration in seconds")
    parser.add_argument("--scene-threshold", type=float, default=0.30)
    args = parser.parse_args()

    require("ffmpeg")
    args.output.mkdir(parents=True, exist_ok=True)

    base = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-i", str(args.video)]
    if args.start:
        base = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-ss", args.start, "-i", str(args.video)]
    if args.duration is not None:
        base += ["-t", str(args.duration)]

    if args.mode == "sample":
        vf = f"fps=1/{args.interval}"
        pattern = args.output / "sample-%06d.png"
        run(base + ["-vf", vf, "-vsync", "vfr", str(pattern)])
    elif args.mode == "scene":
        vf = f"select='gt(scene,{args.scene_threshold})'"
        pattern = args.output / "scene-%06d.png"
        run(base + ["-vf", vf, "-vsync", "vfr", str(pattern)])
    else:
        # Dense mode intentionally preserves every decoded source frame in the selected window.
        pattern = args.output / "frame-%08d.png"
        run(base + ["-vsync", "0", str(pattern)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

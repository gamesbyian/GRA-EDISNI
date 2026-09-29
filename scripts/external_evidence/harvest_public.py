#!/usr/bin/env python3
"""Manifest-driven public evidence harvester.

Large media is written to a work directory for Actions artifact upload or manual
promotion. Authentication is intentionally unsupported here.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load_manifest(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["sources"]


def run(
    cmd: list[str],
    cwd: Path,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd), flush=True)
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        message = f"{output}\nTimed out after {timeout}s".strip()
        print(message, flush=True)
        return subprocess.CompletedProcess(cmd, 124, stdout=message)
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n", flush=True)
    return proc


def classify_extractor_failure(proc: subprocess.CompletedProcess[str]) -> str:
    output = (proc.stdout or "").lower()
    if proc.returncode == 124 or "timed out after" in output:
        return "timeout"
    if "sign in to confirm you" in output and "not a bot" in output:
        return "login-required-or-antibot"
    if "429" in output or "too many requests" in output:
        return "rate-limited"
    if "private video" in output or "login required" in output:
        return "login-required"
    if "video unavailable" in output or "has been removed" in output:
        return "removed-or-missing"
    return "extractor-broken"


def harvest_direct(source: dict, root: Path) -> dict:
    out_dir = root / source["id"] / "original"
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = source.get("suggested_filename") or Path(source["url"]).name or "download.bin"
    dest = out_dir / filename
    urllib.request.urlretrieve(source["url"], dest)  # noqa: S310

    result = {
        "files": [{
            "path": str(dest.relative_to(root)),
            "size": dest.stat().st_size,
            "sha256": sha256(dest),
            "git_blob_sha1": git_blob_sha1(dest),
        }]
    }
    if source.get("expected_size") is not None and dest.stat().st_size != source["expected_size"]:
        raise RuntimeError(
            f"size mismatch for {source['id']}: expected {source['expected_size']}, got {dest.stat().st_size}"
        )
    expected_blob = source.get("expected_git_blob_sha1")
    if expected_blob and git_blob_sha1(dest).lower() != expected_blob.lower():
        raise RuntimeError(
            f"Git blob mismatch for {source['id']}: expected {expected_blob}, got {git_blob_sha1(dest)}"
        )
    result["verified"] = bool(source.get("expected_size") or expected_blob)
    return result


def harvest_youtube(source: dict, root: Path, include_media: bool) -> dict:
    if shutil.which("yt-dlp") is None:
        raise RuntimeError("yt-dlp is not installed")

    out_dir = root / source["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--no-overwrites",
        "--write-info-json",
        "--write-description",
        "--write-thumbnail",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "all,-live_chat",
        "--paths", str(out_dir),
        "--output", "%(id)s/%(title).200B [%(id)s].%(ext)s",
    ]
    if source.get("comments"):
        cmd += ["--write-comments"]
    if not include_media or not source.get("media", True):
        cmd += ["--skip-download"]
    else:
        cmd += ["-f", "bv*+ba/b", "--merge-output-format", "mkv"]
    cmd += [source["url"]]
    proc = run(cmd, cwd=Path.cwd())
    if proc.returncode != 0:
        return {
            "exit_code": proc.returncode,
            "classification_override": classify_extractor_failure(proc),
            "extractor_output_tail": (proc.stdout or "")[-4000:],
        }

    return {"exit_code": proc.returncode}


def harvest_gallery(source: dict, root: Path) -> dict:
    if shutil.which("gallery-dl") is None:
        raise RuntimeError("gallery-dl is not installed")
    out_dir = root / source["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = run(
        [
            "gallery-dl",
            "--dest", str(out_dir),
            "--write-metadata",
            "--write-info-json",
            source["url"],
        ],
        cwd=Path.cwd(),
        timeout=180,
    )
    if proc.returncode != 0:
        return {
            "exit_code": proc.returncode,
            "classification_override": classify_extractor_failure(proc),
            "extractor_output_tail": (proc.stdout or "")[-4000:],
        }

    files = [p for p in out_dir.rglob("*") if p.is_file()]
    media_files = [p for p in files if p.suffix.lower() not in {".json", ".txt"}]
    if source.get("media") and not media_files:
        return {
            "exit_code": proc.returncode,
            "classification_override": "no-media-found",
            "note": "Extractor exited successfully but produced no media payload.",
        }
    return {"exit_code": proc.returncode}


def inventory_files(source_root: Path, work_root: Path) -> list[dict]:
    items = []
    if not source_root.exists():
        return items
    for path in sorted(p for p in source_root.rglob("*") if p.is_file()):
        items.append({
            "path": str(path.relative_to(work_root)),
            "size": path.stat().st_size,
            "sha256": sha256(path),
        })
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("data/external-acquisition-targets.json"))
    parser.add_argument("--output", type=Path, default=Path("evidence-work"))
    parser.add_argument("--source-id", default="all")
    parser.add_argument("--include-media", action="store_true")
    parser.add_argument("--include-social", action="store_true",
                        help="Attempt public gallery-dl acquisition for Instagram/Twitter/VK.")
    args = parser.parse_args()

    sources = load_manifest(args.manifest)
    if args.source_id != "all":
        sources = [s for s in sources if s["id"] == args.source_id]
        if not sources:
            raise SystemExit(f"unknown source id: {args.source_id}")

    args.output.mkdir(parents=True, exist_ok=True)
    summary = []

    for source in sources:
        record = {
            "source_id": source["id"],
            "kind": source["kind"],
            "url": source["url"],
            "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        try:
            if source.get("auth_required"):
                record["classification"] = "login-required"
                record["note"] = "Skipped by public harvester."
            elif source["kind"] == "direct":
                record.update(harvest_direct(source, args.output))
                record["classification"] = "ok"
            elif source["kind"] == "youtube":
                record.update(harvest_youtube(source, args.output, args.include_media))
                record["classification"] = record.pop("classification_override", "ok")
            elif source["kind"] in {"instagram", "twitter", "vk", "facebook"}:
                if not args.include_social:
                    record["classification"] = "manual-review"
                    record["note"] = "Public social extraction disabled unless --include-social is supplied."
                else:
                    record.update(harvest_gallery(source, args.output))
                    record["classification"] = record.pop("classification_override", "ok")
            else:
                record["classification"] = "unsupported"
        except Exception as exc:  # noqa: BLE001
            record["classification"] = "extractor-broken"
            record["error"] = repr(exc)

        record["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        record["files"] = inventory_files(args.output / source["id"], args.output)
        meta_dir = args.output / source["id"]
        meta_dir.mkdir(parents=True, exist_ok=True)
        (meta_dir / "acquisition.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        summary.append(record)
        print(f"{source['id']}: {record['classification']}", flush=True)

    (args.output / "acquisition-summary.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "sources": summary,
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

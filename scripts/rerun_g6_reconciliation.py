#!/usr/bin/env python3
"""Experiment 356: rerun and preserve evidence from the three frozen G6 audits."""

from __future__ import annotations

import contextlib
import io
import json
import runpy
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "experiment-356"
AUDITS = [
    ("291", ROOT / "scripts" / "audit_human_second_selection.py", "Experiment 291"),
    ("322", ROOT / "scripts" / "audit_g6_selector_map_family.py", "Experiment 322"),
    ("269", ROOT / "scripts" / "audit_idempotent_recursion.py", "Experiment 269"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"experiment": 356, "audits": {}}
    failed = False

    for key, script, marker in AUDITS:
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        error = None
        tb = None
        try:
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                runpy.run_path(str(script), run_name="__main__")
        except BaseException as exc:
            error = f"{type(exc).__name__}: {exc}"
            tb = traceback.format_exc()
            failed = True

        stdout = stdout_buf.getvalue()
        stderr = stderr_buf.getvalue()
        marker_present = marker in stdout
        if error is None and not marker_present:
            error = f"expected marker {marker!r} absent from stdout"
            failed = True

        (OUT / f"experiment-{key}.txt").write_text(stdout, encoding="utf-8")
        if stderr:
            (OUT / f"experiment-{key}.stderr.txt").write_text(stderr, encoding="utf-8")
        if tb:
            (OUT / f"experiment-{key}.traceback.txt").write_text(tb, encoding="utf-8")

        summary["audits"][key] = {
            "script": str(script.relative_to(ROOT)),
            "stdout_bytes": len(stdout.encode("utf-8")),
            "stderr_bytes": len(stderr.encode("utf-8")),
            "expected_marker": marker,
            "marker_present": marker_present,
            "error": error,
        }

    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

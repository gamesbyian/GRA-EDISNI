#!/usr/bin/env python3
"""Experiment 356: rerun and preserve stdout from the three frozen G6 audits."""

from __future__ import annotations

import json
import subprocess
import sys
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
    for key, script, marker in AUDITS:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        if marker not in stdout:
            raise AssertionError(
                f"{script.name} exited successfully but did not emit expected marker {marker!r}; "
                f"stdout={stdout!r}, stderr={stderr!r}"
            )
        (OUT / f"experiment-{key}.txt").write_text(stdout, encoding="utf-8")
        if stderr:
            (OUT / f"experiment-{key}.stderr.txt").write_text(stderr, encoding="utf-8")
        summary["audits"][key] = {
            "script": str(script.relative_to(ROOT)),
            "stdout_bytes": len(stdout.encode("utf-8")),
            "stderr_bytes": len(stderr.encode("utf-8")),
            "expected_marker": marker,
            "marker_present": True,
        }

    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

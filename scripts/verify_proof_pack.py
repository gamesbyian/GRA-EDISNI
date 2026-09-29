#!/usr/bin/env python3
"""Run the executable mechanical proof pack.

This is deliberately a thin orchestration/checking layer. It does not reimplement
the machine. Instead it:

1. parses the checked-in theorem graph;
2. verifies that theorem dependencies are acyclic and internally resolvable;
3. verifies that terminal T6 depends only on transition-side O/G/T nodes, never
   observer, algebra, or semantic branches;
4. verifies that every declared transition-side input is actually upstream of T6;
5. runs the independent implementations/reconstructions named in the manifest.

A green proof pack therefore checks both epistemic wiring and implementation
agreement without making one implementation the oracle for all others.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "theorem-obligations.json"
NODE_RE = re.compile(r"^[OGTRAS]\d+[a-z]?$")
DEP_RE = re.compile(r"\b[OGTRAS]\d+[a-z]?\b")


def load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        manifest = json.load(fh)
    assert manifest["schema_version"] == 1
    return manifest


def parse_graph(path: Path) -> dict[str, dict]:
    nodes: dict[str, dict] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue

        node_id, node_class, claim, dependency_text = cells[:4]
        if not NODE_RE.fullmatch(node_id):
            continue

        assert node_id not in nodes, f"duplicate theorem node: {node_id}"
        assert node_class == node_id[0], (
            f"class mismatch for {node_id}: table says {node_class}"
        )

        nodes[node_id] = {
            "class": node_class,
            "claim": claim,
            "deps": set(DEP_RE.findall(dependency_text)),
        }

    assert nodes, f"no theorem nodes parsed from {path}"
    return nodes


def check_references(nodes: dict[str, dict]) -> None:
    for node_id, node in nodes.items():
        unknown = node["deps"] - nodes.keys()
        assert not unknown, f"{node_id} has unknown theorem dependencies: {sorted(unknown)}"


def check_acyclic(nodes: dict[str, dict]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str, trail: tuple[str, ...]) -> None:
        if node_id in visited:
            return
        assert node_id not in visiting, (
            "theorem dependency cycle: " + " -> ".join(trail + (node_id,))
        )
        visiting.add(node_id)
        for dep in sorted(nodes[node_id]["deps"]):
            visit(dep, trail + (node_id,))
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in sorted(nodes):
        visit(node_id, ())


def ancestors(nodes: dict[str, dict], target: str) -> set[str]:
    seen: set[str] = set()

    def walk(node_id: str) -> None:
        for dep in nodes[node_id]["deps"]:
            if dep not in seen:
                seen.add(dep)
                walk(dep)

    walk(target)
    return seen


def check_terminal_quarantine(nodes: dict[str, dict], manifest: dict) -> None:
    target = manifest["terminal_target"]
    assert target in nodes, f"terminal target {target} missing from theorem graph"

    upstream = ancestors(nodes, target)
    upstream_with_target = upstream | {target}

    forbidden = set(manifest["forbidden_terminal_ancestor_classes"])
    bad = sorted(
        node_id
        for node_id in upstream_with_target
        if nodes[node_id]["class"] in forbidden
    )
    assert not bad, (
        f"{target} improperly depends on observer/algebra/semantic nodes: {bad}"
    )

    required_inputs = set(manifest["required_transition_inputs"])
    missing = required_inputs - upstream
    assert not missing, (
        f"{target} no longer depends on declared transition inputs: {sorted(missing)}"
    )


def check_manifest_coverage(nodes: dict[str, dict], manifest: dict) -> None:
    required_nodes = set(manifest["required_nodes"])
    missing_nodes = required_nodes - nodes.keys()
    assert not missing_nodes, (
        f"manifest requires theorem nodes absent from graph: {sorted(missing_nodes)}"
    )

    declared_coverage: set[str] = set()
    for check in manifest["checks"]:
        script = ROOT / check["script"]
        assert script.is_file(), f"proof-pack script missing: {check['script']}"
        for node_id in check["covers"]:
            assert node_id in nodes, (
                f"{check['id']} claims coverage of unknown node {node_id}"
            )
            declared_coverage.add(node_id)

    # The executable pack is intentionally mechanical. O/G premises are checked
    # structurally in the graph; derived T nodes should have executable coverage.
    transition_theorems = {
        node_id
        for node_id, node in nodes.items()
        if node["class"] == "T" and node_id in ancestors(nodes, manifest["terminal_target"]) | {manifest["terminal_target"]}
    }
    uncovered = transition_theorems - declared_coverage
    assert not uncovered, (
        "terminal-chain theorem nodes lack declared executable coverage: "
        + ", ".join(sorted(uncovered))
    )


def run_checks(manifest: dict) -> None:
    for check in manifest["checks"]:
        script = ROOT / check["script"]
        print(f"\n== {check['id']} ==")
        subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
        )


def main() -> None:
    manifest = load_manifest()
    graph_path = ROOT / manifest["theorem_graph"]
    nodes = parse_graph(graph_path)

    check_references(nodes)
    check_acyclic(nodes)
    check_terminal_quarantine(nodes, manifest)
    check_manifest_coverage(nodes, manifest)

    print(f"OK(proof-pack): parsed {len(nodes)} theorem nodes")
    print("OK(proof-pack): dependency graph is acyclic and internally resolved")
    print(
        "OK(proof-pack): terminal T6 has no observer/algebra/semantic ancestors"
    )
    print(
        "OK(proof-pack): every terminal-chain theorem has declared executable coverage"
    )

    run_checks(manifest)
    print("\nOK(proof-pack): all independent mechanical checks passed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Integrity guard for the 27-card perspective-driven INSIDE research queue."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/perspective-experiments-2026-10-16.json"
PORTFOLIO = ROOT / "docs/perspective-driven-sticker-experiments-2026-10-16.md"
QUEUE = ROOT / "docs/research-queue.md"
def check():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cards = data["cards"]
    expected = {f"PX-{n:02d}" for n in range(1, 21)}
    expected |= {f"PX-C{n}" for n in range(1, 7)}
    expected.add("PX-M1")
    seen = [r["id"] for r in cards]
    assert len(cards) == data["count_expected"] == 27, "wrong experiment cardinality"
    assert len(seen) == len(set(seen)) and set(seen) == expected, "missing/duplicate experiment ID"
    portfolio = PORTFOLIO.read_text(encoding="utf-8")
    queue = QUEUE.read_text(encoding="utf-8")
    for card in cards:
        for field in ("discipline","question","test","control","discriminator","gate","stop","status","readiness","priority","mode","reuse","depends_on"):
            assert field in card and card[field] is not None, f"{card['id']}: missing {field}"
        assert card["priority"] in {"P0", "P1", "P2"}, card["id"]
        assert card["mode"] in {"DISCOVER", "DEVELOP", "VALIDATE"}, card["id"]
        assert card["readiness"] in {"ready", "evidence_gate"}, card["id"]
        assert card["status"] in {"queued", "active", "blocked", "completed", "superseded"}, card["id"]
        assert f"### {card['id']}:" in portfolio, f"{card['id']}: missing portfolio card"
        assert card["id"] in queue, f"{card['id']}: missing queue index"
        for parent in card["depends_on"]:
            assert parent in expected and parent != card["id"], f"{card['id']}: invalid dependency"
        for old in card["reuse"]:
            assert (ROOT / old).is_file(), f"{card['id']}: broken research crosswalk {old}"
        if card["status"] in {"completed","superseded"}:
            assert card.get("outcome_url") and card.get("disposition"), f"{card['id']}: closed without outcome"
    assert "perspective-driven-sticker-experiments-2026-10-16.md" in queue, "queue missing canonical portfolio"
    print(f"OK: {len(cards)} linked perspective experiments; 20 individual, 6 synthesis, 1 capstone.")
if __name__ == "__main__":
    check()

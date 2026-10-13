"""Synthetic controls for image-provenance triage; no downloaded CE media required."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.external_evidence.visual_index import (
    analyze, candidates, compare, image_record, promotional_refs, sticker_refs,
)


def artwork(path: Path, *, reverse: bool = False) -> None:
    im = Image.new("RGB", (320, 240), "#f3f0ee" if not reverse else "#191919")
    d = ImageDraw.Draw(im)
    d.rectangle((18, 26, 137, 104), fill="#17100a" if not reverse else "#fffcea")
    d.ellipse((163, 44, 280, 186), fill="#a71d28" if not reverse else "#10ed9a")
    d.line((40, 219, 295, 150), fill="#2455b2" if not reverse else "#faff01", width=13)
    im.save(path)


class VisualProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.refs = self.root / "refs"
        self.refs.mkdir()
        self.inbox = self.root / "inbox"
        self.inbox.mkdir()
        self.original = self.refs / "promo.jpg"
        artwork(self.original)

    def record(self, path: Path, ident="x", role="promotional-reference"):
        return image_record(path, root=self.root, ref_id=ident, role=role)

    def test_same_bytes_and_resized_recompress_are_review_only(self):
        a = self.record(self.original, "promo")
        copy = self.inbox / "copy.jpg"
        copy.write_bytes(self.original.read_bytes())
        dup = self.record(copy, "dup", "unreviewed-candidate")
        result = compare(dup, a)
        self.assertEqual(result["kind"], "byte-identical")
        with Image.open(self.original) as im:
            im.resize((640, 480), Image.Resampling.LANCZOS).save(self.inbox / "resized.jpg", quality=97)
        resized = self.record(self.inbox / "resized.jpg", "resized", "unreviewed-candidate")
        self.assertIn(compare(resized, a)["kind"], {"whole-image-similar", "possible-cropped-repost"})
        summary = analyze([a], [dup], 5)
        self.assertEqual(summary["triage"][0]["classification"], "promotional-reuse-review")
        self.assertIs(summary["triage"][0]["new_sticker_confirmed"], False)

    def test_standalone_product_photo_cannot_be_counted_as_ce(self):
        original = self.record(self.original, "ps4-only", "standalone-product-reference")
        candidate = self.inbox / "repost.jpg"
        candidate.write_bytes(self.original.read_bytes())
        result = analyze([original], [self.record(candidate, "c", "unreviewed-candidate")], 3)
        self.assertEqual(result["triage"][0]["classification"], "standalone-ps4-image-review")
        self.assertFalse(result["triage"][0]["new_sticker_confirmed"])

    def test_metadata_provenance_and_corrupt_input(self):
        folder = self.inbox / "auction-example"
        folder.mkdir()
        (folder / "acquisition.json").write_text(json.dumps({
            "url": "https://example.org/public-auction/1", "classification": "ok",
            "image_urls": {"scan.jpg": "https://i.redd.it/known-public-source.jpg"},
            "source_pages": {"scan.jpg": "https://www.reddit.com/comments/e9bteo/_/gabc12/"}
        }))
        (folder / "scan.jpg").write_bytes(self.original.read_bytes())
        (folder / "broken.png").write_text("not an image")
        records, errors = candidates(self.inbox, max_files=10)
        self.assertEqual(len(records), 1)
        self.assertEqual(len(errors), 1)
        self.assertEqual(records[0]["source_url"], "https://www.reddit.com/comments/e9bteo/_/gabc12/")
        self.assertEqual(records[0]["source_kind"], "auction-example")
        self.assertEqual(records[0]["image_url"], "https://i.redd.it/known-public-source.jpg")

    def test_original_manifest_integrity_and_distinct_roles(self):
        manifest = self.root / "stickers.csv"
        original = self.root / "sticker-002.jpg"
        original.write_bytes(self.original.read_bytes())
        from scripts.external_evidence.visual_index import digest
        row = {"serial": "002", "tile": "B", "symbol": "/", "category": "community-original",
               "canonical_input": "yes", "path": "sticker-002.jpg",
               "source_repo": "twinysam/INSIDE-ARG", "source_ref": "master",
               "source_path": "images/stickers/002.jpg", "sha256": digest(original)}
        with manifest.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row)
            writer.writeheader()
            writer.writerow(row)
        refs = sticker_refs(self.root, manifest)
        self.assertEqual(refs[0]["role"], "known-sticker-photo")
        self.assertEqual(refs[0]["sticker"]["serial"], "002")
        tampered = row.copy()
        tampered["sha256"] = "0" * 64
        with manifest.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=tampered)
            writer.writeheader()
            writer.writerow(tampered)
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            sticker_refs(self.root, manifest)

    def test_missing_public_marketing_control_is_reported_not_retrieved(self):
        manifest = self.root / "promotion.json"
        manifest.write_text(json.dumps({"sources": [{
            "id": "not-fetched", "extension": ".jpg",
            "origin": "publisher-product-photo",
            "url": "https://www.iam8bit.com/image.jpg"}]}))
        r, skipped = promotional_refs(self.root, self.root / "missing", manifest)
        self.assertEqual(r, [])
        self.assertEqual(skipped[0]["reason"], "not-downloaded")

    def test_limit_and_exact_clusters(self):
        artwork(self.inbox / "x.png")
        (self.inbox / "y.png").write_bytes((self.inbox / "x.png").read_bytes())
        with self.assertRaisesRegex(ValueError, "exceeds"):
            candidates(self.inbox, max_files=1)
        found, errors = candidates(self.inbox, max_files=3)
        self.assertFalse(errors)
        result = analyze([], found, 5)
        self.assertEqual(len(result["exact_candidate_groups"]), 1)
        self.assertEqual(len(result["exact_candidate_groups"][0]["candidate_ids"]), 2)
        self.assertEqual(result["triage"][0]["classification"], "unmatched-visual-review")


if __name__ == "__main__":
    unittest.main()

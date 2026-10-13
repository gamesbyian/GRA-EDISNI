"""Synthetic local-only CE image provenance tests; does not fetch real photos."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ce_image_index", ROOT / "scripts/index_inside_ce_public_images.py")
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)

def source(aid, filename, kind):
    return {
        "asset_id": aid, "file_path": filename,
        "source_url": "https://example.org/public/" + aid,
        "source_kind": kind, "published_at": "2019-12-15",
        "captured_at": "2026-10-13", "permission_basis": "synthetic_test"
    }

class MediaProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # Highly asymmetric test pattern makes perceptual checks informative.
        x = Image.new("RGB", (160, 130), "#dadada")
        d = ImageDraw.Draw(x)
        d.rectangle((11, 10, 85, 64), fill="#172134")
        d.ellipse((100, 20, 153, 90), fill="#d02020")
        d.polygon([(35, 110), (140, 111), (68, 70)], fill="#24a172")
        x.save(self.root / "marketing.png")
        x.save(self.root / "repost.png", compress_level=9)
        x.resize((320, 260)).save(self.root / "repost-resized.png")
        y = Image.new("RGB", (160, 130), "black")
        d = ImageDraw.Draw(y)
        d.rectangle((5, 0, 150, 80), fill="white")
        d.ellipse((40, 85, 100, 120), fill="#3300ff")
        y.save(self.root / "unrelated.png")
        self.rows = [
            source("a", "marketing.png", "official_marketing"),
            source("b", "repost.png", "public_resale"),
            source("c", "repost-resized.png", "community_repost"),
            source("d", "unrelated.png", "owner_public_post"),
        ]
    def tearDown(self):
        self.tmp.cleanup()

    def test_exact_and_perceptual_clusters(self):
        images, summary = media.analyze(self.rows, root=self.root)
        by_id = {x["asset_id"]: x for x in images}
        self.assertEqual(by_id["a"]["pixel_sha256"], by_id["b"]["pixel_sha256"])
        self.assertEqual(by_id["a"]["candidate_cluster"], by_id["b"]["candidate_cluster"])
        self.assertEqual(by_id["a"]["candidate_cluster"], by_id["c"]["candidate_cluster"])
        self.assertNotEqual(by_id["a"]["candidate_cluster"], by_id["d"]["candidate_cluster"])
        self.assertEqual(summary["candidate_clusters"], 2)
        self.assertEqual(summary["new_confirmed_stickers"], 0)
        self.assertEqual(by_id["d"]["marketing_reference_proximity"],
                         "none_in_supplied_corpus")
        self.assertEqual(by_id["b"]["marketing_reference_proximity"],
                         "potential_reused_official_asset_needs_review")
        self.assertTrue(all(x["assessment"] == "unreviewed_image_provenance_only"
                            for x in images))
        self.assertTrue(any(x["kind"] == "same_decoded_pixels"
                            for x in summary["pair_records"]))
        self.assertTrue(any(x["kind"] == "perceptual_similarity_needs_review"
                            for x in summary["pair_records"]))

    def test_png_webp_lossless_same_pixels(self):
        img = Image.open(self.root / "marketing.png")
        img.save(self.root / "reencoded.webp", lossless=True)
        a = media.normalized_image(self.root / "marketing.png")
        b = media.normalized_image(self.root / "reencoded.webp")
        self.assertNotEqual(a["file_sha256"], b["file_sha256"])
        self.assertEqual(a["pixel_sha256"], b["pixel_sha256"])

    def test_validation_no_missing_permission_or_private_source(self):
        row = dict(self.rows[0], source_url="file:///home/user/images")
        with self.assertRaises(ValueError):
            media.validate_row(row)
        row = dict(self.rows[0], permission_basis="")
        with self.assertRaises(ValueError):
            media.validate_row(row)
        row = dict(self.rows[0], source_kind="private_dm")
        with self.assertRaises(ValueError):
            media.validate_row(row)

    def test_path_safety_and_duplicate_ids(self):
        rows = [dict(self.rows[0], file_path="../not_allowed.png")]
        with self.assertRaises(ValueError):
            media.analyze(rows, root=self.root)
        with self.assertRaises(ValueError):
            media.analyze([self.rows[0], self.rows[0]], root=self.root)
        with self.assertRaises(ValueError):
            media.analyze([dict(self.rows[0], file_path="missing.png")],
                          root=self.root)

    def test_aspect_and_pair_guards(self):
        base = media.normalized_image(self.root / "marketing.png")
        other = dict(base, aspect_ratio=5)
        other["pixel_sha256"] = "0"*64
        self.assertFalse(media.similar(base, other))
        self.assertRaises(ValueError, media.img_hash,
                          Image.open(self.root / "marketing.png").convert("L"), "bad")

    def test_manifest_output_scope_and_schema(self):
        manifest = self.root / "images.tsv"
        with manifest.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=sorted(media.REQUIRED), delimiter="\t")
            w.writeheader()
            w.writerows(self.rows)
        with manifest.open(newline="", encoding="utf-8") as f:
            prepared = list(csv.DictReader(f, delimiter="\t"))
        images, summary = media.analyze(prepared, root=self.root)
        self.assertEqual(len(images), 4)
        self.assertIn("only_locally_supplied", summary["coverage"])
        self.assertEqual(len(media.OUTPUT), len(set(media.OUTPUT)))

if __name__ == "__main__":
    unittest.main()

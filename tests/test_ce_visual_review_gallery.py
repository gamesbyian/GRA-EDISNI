"""No-network review gallery tests: source diversity, privacy, path safety."""
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.external_evidence.build_visual_review_gallery import (
    render, select_for_review, original_link, safe_candidate_path,
)


class GalleryTests(unittest.TestCase):
    def test_source_fairness_and_unmatched_sampling(self):
        items = [
            {"id": "a1", "source_kind": "aaa"},
            {"id": "a2", "source_kind": "aaa"},
            {"id": "b1", "source_kind": "bbb"},
            {"id": "z1", "source_kind": "zzz"},
        ]
        matches = {"a1": [{"reference_role": "known-sticker-photo"}],
                   "z1": [{"reference_role": "promotional-reference"}]}
        selected = select_for_review(items, matches, 3)
        self.assertEqual({x["source_kind"] for x in selected},
                         {"aaa", "bbb", "zzz"})
        self.assertEqual({x["id"] for x in selected}, {"a1", "b1", "z1"})
        self.assertEqual([x["id"] for x in select_for_review(items,matches,3)],
                         [x["id"] for x in selected])
        with self.assertRaises(ValueError):
            select_for_review(items + [items[0]], matches, 3)
        with self.assertRaises(ValueError):
            select_for_review(items, matches, 0)

    def test_gallery_bounded_embedded_offline_and_source_escaped(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ("same.jpg", "other.jpg"):
                Image.new("RGB", (160, 120), "#555555").save(root / name)
            items = {"candidates": [
                {"id": "image1", "path": "same.jpg", "source_kind": "batchA",
                 "source_url": 'https://example.org/post?q="><script>bad</script>',
                 "image_url": "javascript:alert(1)", "sha256": "abc"},
                {"id": "image2", "path": "other.jpg", "source_kind": "batchB",
                 "source_url": "https://example.org/other", "sha256": "def"}
            ]}
            evidence = {"matches": [{"candidate_id": "image1",
                "reference_role": "known-sticker-photo", "reference_id": "sticker-043",
                "reference_canonical_case": "043", "kind": "byte-identical"}]}
            output, report = render(items, evidence, root)
            self.assertEqual(report["selected_for_review"], 2)
            self.assertEqual(report["represented_source_groups"], 2)
            self.assertEqual(report["new_confirmed_stickers"], 0)
            self.assertEqual(report["unavailable_or_unsafe_thumbnails"], [])
            self.assertEqual(output.count('src="data:image/jpeg;base64,'), 2)
            self.assertNotIn("<script>bad</script>", output)
            self.assertNotIn('href="javascript:', output)
            self.assertIn("Known case 043", output)
            self.assertIn("No hash match among retained references", output)
            self.assertIn("no sticker verified", output)
            self.assertIn("Content-Security-Policy", output)
            self.assertNotIn("https://", output.split('<style>')[0])

    def test_missing_unsafe_symlink_and_excluded_count(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root = Path(d)
            (Path(outside) / "private.jpg").write_bytes(b"not an image")
            (root / "escape.jpg").symlink_to(Path(outside) / "private.jpg")
            self.assertIsNone(safe_candidate_path(root, "../other/image.jpg"))
            self.assertIsNone(safe_candidate_path(root, "escape.jpg"))
            items = {"candidates": [
                {"id": "bad", "path": "escape.jpg", "source_kind": "s0"},
                {"id": "missing", "path": "absent.jpg", "source_kind": "s1"}
            ]}
            output, report = render(items, {"matches":[]}, root, max_items=1)
            self.assertEqual(report["selected_for_review"], 1)
            self.assertEqual(report["excluded_by_review_limit"], 1)
            self.assertEqual(len(report["unavailable_or_unsafe_thumbnails"]), 1)
            self.assertIn("unavailable or unsafe", output)

    def test_source_link_scheme_and_login_rejected(self):
        self.assertEqual(original_link("http://example.org/"), "")
        self.assertEqual(original_link("https://user:pw@example.org/p"), "")
        self.assertEqual(original_link("javascript:alert(1)"), "")
        self.assertEqual(original_link("https://example.org/?a=1&b=2"),
                         "https://example.org/?a=1&amp;b=2")


if __name__ == "__main__":
    unittest.main()

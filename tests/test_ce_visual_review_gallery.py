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

    def test_review_gallery_embeds_bounded_unverified_region_crops(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            Image.new("RGB",(250,180),"gray").save(root/"collector.jpg")
            index={"candidates":[{"id":"photo","path":"collector.jpg",
                                  "source_kind":"public-owner",
                                  "source_url":"https://example.org/owner"}]}
            regions={"new_confirmed_stickers":0,"candidates":[
              {"candidate_id":"photo","suggestions":[
                {"bbox_xyxy_original_pixels":[25,25,120,135],
                 "reference_id":"sticker-037","hash_distance_sum":10,
                 "new_sticker_confirmed":False},
                {"bbox_xyxy_original_pixels":[0,0,99999,99999],
                 "reference_id":"sticker-999","hash_distance_sum":0,
                 "new_sticker_confirmed":False}]}]}
            output,report=render(index,{"matches":[]},root,regions=regions)
            self.assertEqual(report["region_crop_previews_embedded"],1)
            self.assertEqual(len(report["invalid_region_preview_records"]),1)
            self.assertIn("Suggested image regions (unverified)",output)
            self.assertIn("NOT a reading of the candidate photograph",output)
            self.assertIn("sticker-037",output)
            self.assertEqual(output.count('src="data:image/jpeg;base64,'),2)
            self.assertNotIn("sticker-999",output)
            with self.assertRaisesRegex(ValueError,"must not claim"):
                render(index,{"matches":[]},root,regions={
                    **regions,"new_confirmed_stickers":1})

    def test_geometry_paper_crops_are_never_identified_as_stickers(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            Image.new("RGB",(160,160),"white").save(root/"photo.jpg")
            index={"candidates":[{"id":"candidate","path":"photo.jpg",
                                  "source_kind":"demo","source_url":"https://example.org/photo"}]}
            geometries={"new_confirmed_stickers":0,"candidates":[{
                "candidate_id":"candidate","proposals":[
                    {"bbox_xyxy_original_pixels":[20,30,100,110],
                     "candidate_type":"bright-rectangle-unverified",
                     "new_sticker_confirmed":False,
                     "ink_layout":{"dark_pixel_fractions_by_zone":{
                          "center_mark":.08,"bottom_print":.013}}},
                    {"bbox_xyxy_original_pixels":[0,0,5000,5000],
                     "new_sticker_confirmed":False}]}]}
            html_text,report=render(index,{"matches":[]},root,geometry=geometries)
            self.assertEqual(report["geometry_crop_previews_embedded"],1)
            self.assertEqual(len(report["invalid_geometry_preview_records"]),1)
            self.assertIn("the geometric method does NOT identify stickers",html_text)
            self.assertIn("Center dark: 0.080; lower dark: 0.013 (NOT sticker proof)",html_text)
            self.assertEqual(html_text.count('src="data:image/jpeg;base64,'),2)
            self.assertEqual(report["new_confirmed_stickers"],0)
            with self.assertRaisesRegex(ValueError,"must not establish"):
                render(index,{"matches":[]},root,geometry={**geometries,
                                                          "new_confirmed_stickers":2})
            bad=dict(geometries)
            bad["candidates"]=[{"candidate_id":"candidate","proposals":[
                {"bbox_xyxy_original_pixels":[20,30,100,110],
                 "new_sticker_confirmed":True}]}]
            # Per-proposal violations are visibly withheld, not promoted.
            out,summary=render(index,{"matches":[]},root,geometry=bad)
            self.assertEqual(summary["geometry_crop_previews_embedded"],0)
            self.assertEqual(len(summary["invalid_geometry_preview_records"]),1)
            self.assertIn("cannot identify",summary["invalid_geometry_preview_records"][0]["error"])

    def test_source_link_scheme_and_login_rejected(self):
        self.assertEqual(original_link("http://example.org/"), "")
        self.assertEqual(original_link("https://user:pw@example.org/p"), "")
        self.assertEqual(original_link("javascript:alert(1)"), "")
        self.assertEqual(original_link("https://example.org/?a=1&b=2"),
                         "https://example.org/?a=1&amp;b=2")


if __name__ == "__main__":
    unittest.main()

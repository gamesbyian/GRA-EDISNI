"""Public HTML image candidate extraction controls; deliberately no network."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.external_evidence.discover_html_images import extract, normal_url
from scripts.external_evidence.visual_semantic import LABELS, ranking
from scripts.external_evidence.fetch_html_images import approved, select, safe_dir, asset_key, selection_coverage


class HtmlLeadTests(unittest.TestCase):
    def test_lazy_srcset_social_image_and_dedup(self):
        source = """
        <html><head><meta property="og:image" content="/images/promo.jpg">
        <meta name="twitter:image" content="/images/promo.jpg"></head>
        <body><img src="/images/promo.jpg" alt="INSIDE CE Huddle">
        <picture><source srcset="/product-small.jpg 1x, /product-large.jpg 2x"></picture>
        <img data-src="/auction/sticker.jpeg" alt="INSIDE collector sticker">
        <img src="data:image/png;base64,abc"></body></html>
        """
        rows = extract(source, "https://example.org/post/123")
        self.assertEqual(len(rows), 4)
        promo = next(r for r in rows if r["image_url"].endswith("/images/promo.jpg"))
        self.assertEqual(len(promo["contexts"]), 3)
        self.assertIn("huddle", promo["keyword_hints"])
        sticker = next(r for r in rows if r["image_url"].endswith("sticker.jpeg"))
        self.assertIn("sticker", sticker["keyword_hints"])
        self.assertEqual(sticker["review_status"], "unfetched-and-unverified")

    def test_disallow_non_links_and_fragment(self):
        self.assertEqual(normal_url("https://example.org/page", "javascript:alert(1)"), "")
        self.assertEqual(normal_url("https://example.org/page", "//x.com/abc.jpg#foo"),
                         "https://x.com/abc.jpg")
        self.assertEqual(normal_url("https://example.org/page", "https://www.google-analytics.com/a.gif"), "")

    def test_download_host_restriction_and_priority(self):
        self.assertTrue(approved("https://i.redd.it/abc.jpg"))
        self.assertFalse(approved("http://i.redd.it/abc.jpg"))
        self.assertFalse(approved("https://localhost/internal.jpg"))
        self.assertFalse(approved("https://i.redd.it.attacker.example/img.jpg"))
        self.assertEqual(safe_dir("page:1/2"), "htmlimg-page-1-2")
        rows = [
            {"source_id": "s1", "image_url": "https://i.redd.it/low.jpg",
             "source_page_url": "https://reddit.com/x", "keyword_hints": [], "hint_count": 0},
            {"source_id": "s1", "image_url": "https://i.redd.it/high.jpg",
             "source_page_url": "https://reddit.com/x", "keyword_hints": ["inside"], "hint_count": 1},
            {"source_id": "s1", "image_url": "https://elsewhere.org/blocked.jpg",
             "source_page_url": "https://reddit.com/x", "keyword_hints": ["inside"], "hint_count": 1},
        ]
        result = select(rows, per_page=1, total=5)
        self.assertEqual([x["image_url"] for x in result], ["https://i.redd.it/high.jpg"])

    def test_visual_waterfall_keeps_excluded_original_candidates_visible(self):
        rows = [
            {"source_id": "ce-visual-official-ce", "image_url": "https://cdn.shopify.com/photo/opaque.jpg",
             "hint_count": 2},
            {"source_id": "ce-visual-official-ce", "image_url": "https://cdn.shopify.com/photo/inside.jpg?width=400",
             "hint_count": 1},
            {"source_id": "ce-visual-official-ce", "image_url": "https://cdn.shopify.com/photo/inside.jpg?width=800",
             "hint_count": 1},
            {"source_id": "owner", "image_url": "https://i.redd.it/owner1.jpg", "hint_count": 2},
            {"source_id": "owner", "image_url": "https://i.redd.it/owner2.jpg", "hint_count": 1},
            {"source_id": "owner", "image_url": "https://example.org/not-allowlisted.jpg", "hint_count": 3},
        ]
        chosen = select(rows, per_page=1, total=1)
        report = selection_coverage(rows, chosen)
        self.assertEqual(report["input_url_mentions"], 6)
        self.assertEqual(report["official_product_url_heuristic"], 1)
        self.assertEqual(report["unapproved_image_host"], 1)
        self.assertEqual(report["eligible_variants_collapsed"], 1)
        self.assertEqual(report["unique_eligible_asset_families"], 3)
        self.assertEqual(report["asset_families_selected_for_transfer"], 1)
        self.assertEqual(report["eligible_asset_families_not_selected_by_budget"], 2)
        self.assertTrue(report["original_lead_inventory_retained_separately"])

    def test_srcset_resolution_family_collapses_to_one_download(self):
        base = "https://www.iam8bit.com/cdn/shop/products/InsideCE_Lifestyle_00001B.jpg?v=123"
        rows = [{"source_id": "ce-visual-official-full-product",
                 "image_url": base + "&width=" + str(w),
                 "source_page_url": "https://www.iam8bit.com/products/inside-collector-s-edition",
                 "keyword_hints": ["inside"], "hint_count": 1}
                for w in (200, 400, 1000, 1600, 2000, 3648)]
        rows += [{"source_id": "ce-visual-official-full-product",
                  "image_url": "https://www.iam8bit.com/cdn/shop/files/Billboardstickers.png?width=500",
                  "source_page_url": "https://www.iam8bit.com/products/inside-collector-s-edition",
                  "keyword_hints": ["sticker"], "hint_count": 1}]
        chosen = select(rows, per_page=8, total=20)
        self.assertEqual(len(chosen), 1)
        self.assertTrue(chosen[0]["image_url"].endswith("&width=2000"))
        self.assertEqual(asset_key(rows[0]["image_url"]), asset_key(rows[1]["image_url"]))

    def test_polygon_image_variants_are_distinct_by_original_asset(self):
        base = "https://static0.polygonimages.com/wordpress/wp-content/uploads/chorus/uploads/chorus_asset/file/"
        rows = []
        for path in ("19487418/InsideCE_Lifestyle_00001.jpg", "19487419/InsideCE_Lifestyle_00008.jpg"):
            for w in (500, 825):
                rows.append({"source_id": "press-article", "image_url": base + path + "?q=50&fit=crop&w=" + str(w),
                             "source_page_url": "https://polygon.com/article", "keyword_hints": ["inside"],
                             "hint_count": 1})
        chosen = select(rows, per_page=8, total=20)
        self.assertEqual(len(chosen), 2)
        self.assertTrue(all("w=825" in item["image_url"] for item in chosen))

    def test_no_direct_photo_links_produces_empty_valid_download_report(self):
        from scripts.external_evidence.fetch_html_images import main
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            leads = root / "links.json"
            leads.write_text(json.dumps({"image_mentions": []}))
            output = root / "created-by-run"
            argv = ["fetch_html_images.py", "--leads", str(leads), "--out", str(output)]
            with patch.object(sys, "argv", argv):
                main()
            result = json.loads((output / "html-image-download-report.json").read_text())
            self.assertEqual(result["image_downloads"], [])
            self.assertEqual(result["bytes_downloaded"], 0)

    def test_round_robin_allows_later_source_within_small_budget(self):
        def row(source, name, hints):
            return {"source_id": source, "image_url": f"https://i.redd.it/{name}.jpg",
                    "source_page_url": f"https://reddit.com/{source}",
                    "keyword_hints": ["inside"] * hints, "hint_count": hints}
        leads = [row("aaa", f"early{i}", 2) for i in range(5)]
        leads += [row("zzz", "later", 1), row("mmm", "middle", 3)]
        selected = select(leads, per_page=4, total=3)
        self.assertEqual([r["source_id"] for r in selected], ["mmm", "aaa", "zzz"])
        self.assertEqual(len(set(r["source_id"] for r in selected)), 3)
        self.assertEqual(selection_coverage(leads, selected)["eligible_asset_families_not_selected_by_budget"], 4)

    def test_round_robin_preserves_priority_and_per_page_limit(self):
        sources = []
        for source in ("a", "b"):
            for idx in range(4):
                sources.append({"source_id": source,
                                "image_url": f"https://i.redd.it/{source}{idx}.jpg",
                                "hint_count": 4 - idx})
        selected = select(sources, per_page=2, total=10)
        self.assertEqual([(x["source_id"],x["hint_count"]) for x in selected],
                         [("a",4),("b",4),("a",3),("b",3)])
        self.assertEqual(len(selected), 4)

    def test_static_embedded_images_not_only_img_tags(self):
        source = """
        <html><head>
          <base href="https://www.iam8bit.com/media/">
          <script type="application/ld+json">{"@type":"Product",
            "image":["/images/inside-cover.jpg",
                     {"@type":"ImageObject","contentUrl":"huddle.jpg"}],
            "offers":{"price":"400","url":"https://example.org/not-image"}}
          </script>
        </head><body>
          <video poster="../frame/sticker-cover.png"></video>
          <div style="background-image: url('/images/black-wrapper.webp')"></div>
          <a href="sealed-game.jpeg?size=large">See package photograph</a>
          <a href="https://example.org/forum/post">Not an image</a>
        </body></html>
        """
        results = extract(source, "https://www.iam8bit.com/archive/post")
        urls = {r["image_url"]: r for r in results}
        self.assertEqual(len(urls), 5)
        self.assertIn("https://www.iam8bit.com/images/inside-cover.jpg", urls)
        self.assertIn("https://www.iam8bit.com/media/huddle.jpg", urls)
        self.assertIn("https://www.iam8bit.com/frame/sticker-cover.png", urls)
        self.assertIn("https://www.iam8bit.com/images/black-wrapper.webp", urls)
        self.assertIn("https://www.iam8bit.com/media/sealed-game.jpeg?size=large", urls)
        self.assertTrue(all(x["review_status"] == "unfetched-and-unverified"
                            for x in results))
        self.assertTrue(any("jsonld:" in context
                            for result in results for context in result["contexts"]))

    def test_malformed_jsonld_and_disallowed_urls_remain_nonfatal(self):
        source = """
        <script type="application/ld+json">{not json</script>
        <div style="background-image:url(javascript:alert(1))"></div>
        <video poster="data:image/jpeg;base64,aaa"></video>
        <a href="https://example.org/p/photo.jpg">review candidate</a>
        """
        rows = extract(source, "https://example.org/post")
        self.assertEqual([x["image_url"] for x in rows],
                         ["https://example.org/p/photo.jpg"])

    def test_semantic_ranks_are_relative_and_untrusted(self):
        keys = list(LABELS)[:3]
        rows = ranking(keys, [0.1, 0.7, 0.3])
        self.assertEqual(rows[0]["label"], keys[1])
        self.assertEqual(len(rows), 3)
        with self.assertRaises(ValueError):
            ranking(keys, [1])


if __name__ == "__main__":
    unittest.main()

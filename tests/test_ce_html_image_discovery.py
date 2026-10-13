"""Public HTML image candidate extraction controls; deliberately no network."""
import unittest

from scripts.external_evidence.discover_html_images import extract, normal_url
from scripts.external_evidence.visual_semantic import LABELS, ranking
from scripts.external_evidence.fetch_html_images import approved, select, safe_dir


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

    def test_semantic_ranks_are_relative_and_untrusted(self):
        keys = list(LABELS)[:3]
        rows = ranking(keys, [0.1, 0.7, 0.3])
        self.assertEqual(rows[0]["label"], keys[1])
        self.assertEqual(len(rows), 3)
        with self.assertRaises(ValueError):
            ranking(keys, [1])


if __name__ == "__main__":
    unittest.main()

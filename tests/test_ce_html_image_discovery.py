"""Public HTML image candidate extraction controls; deliberately no network."""
import unittest

from scripts.external_evidence.discover_html_images import extract, normal_url
from scripts.external_evidence.visual_semantic import LABELS, ranking


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

    def test_semantic_ranks_are_relative_and_untrusted(self):
        keys = list(LABELS)[:3]
        rows = ranking(keys, [0.1, 0.7, 0.3])
        self.assertEqual(rows[0]["label"], keys[1])
        self.assertEqual(len(rows), 3)
        with self.assertRaises(ValueError):
            ranking(keys, [1])


if __name__ == "__main__":
    unittest.main()

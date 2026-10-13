"""Offline, adversarial validation of bounded historical eBay capture-index retrieval."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.external_evidence.probe_ce_ebay_cdx import (
    CDXHTTPError, inspect, item_id_matches_url, parse_capture_rows, query_url
)


class HistoricCDXTests(unittest.TestCase):
    def setUp(self):
        self.item = "389713956842"
        self.record = {
            "item_id": self.item, "ebay_url": f"https://www.ebay.com/itm/{self.item}",
            "initial_reconciliation": "unreconciled-by-canonical-exact-item-id",
        }
        self.header = ["timestamp", "original", "statuscode", "mimetype", "digest"]

    def test_accepts_exact_canonical_and_slug_variants_only(self):
        self.assertTrue(item_id_matches_url(
            "http://www.ebay.com/itm/389713956842?hash=itemwhatever", self.item))
        self.assertTrue(item_id_matches_url(
            "https://www.ebay.com/itm/INSIDE-COLLECTORS-EDITION/389713956842", self.item))
        for wrong in (
            "https://www.ebay.com/itm/3897139568421",
            "https://www.ebay.com/itm/389713956842-foo",
            "https://www.ebay.com/p/389713956842",
            "https://example.com/itm/389713956842",
            "https://www.ebay.com/itm/389713956842/elsewhere",
            "https://www.ebay.com@evil.example/itm/389713956842",
        ):
            self.assertFalse(item_id_matches_url(wrong, self.item), wrong)

    def test_query_is_bounded_to_single_public_item(self):
        url = query_url(self.item)
        self.assertIn("web.archive.org/cdx/search/cdx?", url)
        self.assertIn("matchType=prefix", url)
        self.assertIn("statuscode%3A200", url)
        with self.assertRaises(ValueError):
            query_url(self.item, limit=500)
        with self.assertRaises(ValueError):
            query_url("389713956842;rm -rf /")

    def test_capture_parser_refuses_nearby_items_and_non_html(self):
        rows = [self.header,
                ["20260311091201", "https://www.ebay.com/itm/389713956842", "200", "text/html", "A"],
                ["20260312091201", "http://www.ebay.com/itm/fancy/389713956842", "200", "text/html", "B"],
                ["20260313091201", "https://www.ebay.com/itm/3897139568429", "200", "text/html", "C"],
                ["20260314091201", "https://www.ebay.com/itm/389713956842", "404", "text/html", "D"],
                ["20260315091201", "https://www.ebay.com/itm/389713956842", "200", "image/jpeg", "E"],
                ["badtime", "https://www.ebay.com/itm/389713956842", "200", "text/html", "F"],
                ["20260311091201", "https://www.ebay.com/itm/389713956842", "200", "text/html", "A"]]
        captures, rejected = parse_capture_rows(rows, self.item)
        self.assertEqual(len(captures), 2)
        self.assertEqual(rejected, 4)
        self.assertTrue(all(x["serial_number_observed"] is False for x in captures))
        self.assertTrue(all(x["capture_status"] == "CDX-index-only-not-fetched" for x in captures))

    def test_unexpected_schema_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            parse_capture_rows([["foo", "original"], ["bar", "sample"]], self.item)
        self.assertEqual(parse_capture_rows([], self.item), ([], 0))
        with self.assertRaisesRegex(ValueError, "Expected"):
            parse_capture_rows({}, self.item)

    def test_rate_limit_causes_remaining_ids_to_be_skipped(self):
        next_id = "294530200626"
        second = {**self.record, "item_id": next_id,
                  "ebay_url": f"https://www.ebay.com/itm/{next_id}"}
        calls = []
        def fake(item_id):
            calls.append(item_id)
            raise CDXHTTPError(429, "1800")
        result = inspect([self.record, second], fetcher=fake)
        self.assertEqual(calls, [self.item])
        self.assertEqual(result[0]["http_status"], 429)
        self.assertEqual(result[0]["retry_after"], "1800")
        self.assertEqual(result[1]["status"], "not-attempted")

    def test_success_and_no_capture_are_distinguishable(self):
        result = inspect([self.record], fetcher=lambda _: (
            [self.header, ["20260313000000",
                           f"https://www.ebay.com/itm/{self.item}",
                           "200", "text/html", "DIGEST"]], "f" * 64))
        self.assertEqual(result[0]["capture_count"], 1)
        self.assertEqual(result[0]["status"], "CDX-capture-pointers-unverified")
        result = inspect([self.record], fetcher=lambda _: ([self.header], "e" * 64))
        self.assertEqual(result[0]["status"], "CDX-no-capture-pointers")

    def test_genuine_empty_cdx_json_is_no_capture_not_error(self):
        result = inspect([self.record], fetcher=lambda _: ([], "a" * 64))
        self.assertEqual(result[0]["status"], "CDX-no-capture-pointers")
        self.assertEqual(result[0]["archive_query_sha256"], "a" * 64)
        self.assertEqual(result[0]["capture_count"], 0)

    def test_known_case_source_cannot_enter_unknown_probe(self):
        with self.assertRaisesRegex(ValueError, "Known or non-CE"):
            inspect([{**self.record, "initial_reconciliation": "canonical-known"}],
                    fetcher=lambda _: ([], ""))

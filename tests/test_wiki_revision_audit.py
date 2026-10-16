"""Offline regression tests for bounded public MediaWiki revision auditing."""
import unittest

from scripts.wiki_revision_audit import audit, changed_lines, revision_text


class WikiRevisionAuditTests(unittest.TestCase):
    def test_payload_variants(self):
        self.assertEqual(revision_text({"*": "old"}), "old")
        self.assertEqual(revision_text({"slots": {"main": {"content": "new"}}}), "new")
        with self.assertRaises(ValueError):
            revision_text({})

    def test_diff(self):
        self.assertEqual(changed_lines("a\nb", "a\nc"), (["c"], ["b"]))

    def test_known_positive_short_lived_injection(self):
        base = "== INSIDE ==\nThe printer is in the facility."
        dataset = {"site": "example.invalid", "title": "Inside_ARG", "revisions": [
            {"revid": 1, "timestamp": "2018-11-15T00:00:00Z", "content": base},
            {"revid": 2, "timestamp": "2018-11-16T19:54:00Z",
             "content": "ARG invitation https://example.org/vault\n" + base},
            {"revid": 3, "timestamp": "2018-11-20T21:55:00Z", "content": base},
            {"revid": 4, "timestamp": "2018-11-21T00:00:00Z",
             "content": base + "\n<!-- hidden -->\nInvisible \u200b"},
        ]}
        result = audit(dataset)
        events = {event["revid"]: event for event in result["events"]}
        types2 = {flag["kind"] for flag in events[2]["indicators"]}
        types4 = {flag["kind"] for flag in events[4]["indicators"]}
        self.assertEqual(result["revision_count"], 4)
        self.assertTrue({"short_lived_added_lines", "new_url"} <= types2)
        self.assertTrue({"added_html_comment", "invisible_or_directional_unicode"} <= types4)

    def test_no_fabricated_negative(self):
        dataset = {"site": "example.invalid", "title": "Neutral", "revisions": [
            {"revid": 1, "timestamp": "2019-01-01T00:00:00Z", "content": "Hello"},
            {"revid": 2, "timestamp": "2019-01-02T00:00:00Z", "content": "Hello world"},
        ]}
        self.assertEqual(audit(dataset)["finding_count"], 0)
        with self.assertRaises(ValueError):
            audit({"revisions": []})
        with self.assertRaises(ValueError):
            audit({"revisions": [dataset["revisions"][1], dataset["revisions"][0]]})


if __name__ == "__main__":
    unittest.main()

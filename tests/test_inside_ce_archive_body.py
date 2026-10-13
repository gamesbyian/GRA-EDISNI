"""Synthetic one-record Wayback archived HTML body retrieval tests; offline only."""
import importlib.util
from io import BytesIO
from pathlib import Path
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ce_archive_body", ROOT / "scripts/retrieve_inside_ce_known_wayback_body.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Response(BytesIO):
    def __init__(self, data, mime="text/html", status=200):
        super().__init__(data)
        self.headers = {"Content-Type": mime}
        self._status = status
    def getcode(self):
        return self._status
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()

class ArchiveBodyTests(unittest.TestCase):
    def test_offline_default(self):
        r = mod.probe()
        self.assertEqual(r["capture_body_state"], "planned_unexecuted")
        self.assertEqual(r["wayback_capture_timestamp"], "20190306051337")
        self.assertEqual(r["new_confirmed_stickers"], 0)

    def test_one_known_archived_page_exact_url_and_bounded_snippets(self):
        html = b"<html><title>INSIDE</title><script>private_label=123</script>" + \
               b"<body><div>Playdead Collector Edition announcement</div>" + \
               b"<p>A fan is discussing RealDoll.</p></body></html>"
        requests = []
        def opener(req, timeout):
            requests.append((req.full_url, timeout))
            return Response(html)
        r = mod.probe(execute=True, opener=opener)
        self.assertEqual(r["capture_body_state"], "html_body_retrieved")
        self.assertEqual(r["html_bytes"], len(html))
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0], mod.REPLAY)
        self.assertEqual(requests[0][1], 25)
        self.assertTrue(any("Playdead" in s for s in r["keyword_snippets"]))
        self.assertFalse(any("private_label" in s for s in r["keyword_snippets"]))
        self.assertEqual(r["new_confirmed_stickers"], 0)

    def test_invalid_response_is_not_claimed_as_archived_body(self):
        r = mod.probe(execute=True, opener=lambda *args, **kwargs:
                      Response(b"not-html", mime="application/json"))
        self.assertEqual(r["capture_body_state"], "unexpected_response")
        self.assertNotIn("sha256", r)

    def test_size_cap(self):
        r = mod.probe(execute=True, opener=lambda *args, **kwargs:
                      Response(b"A" * (mod.MAX_BYTES + 1)))
        self.assertEqual(r["capture_body_state"], "size_limit_exceeded_no_body_saved")
        self.assertNotIn("keyword_snippets", r)

    def test_denied_or_unreachable(self):
        def reject(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)
        denied = mod.probe(execute=True, opener=reject)
        self.assertEqual(denied["http_status"], 403)
        self.assertEqual(denied["capture_body_state"], "http_error")
        def timeout(req, **kwargs):
            raise TimeoutError("simulated")
        blocked = mod.probe(execute=True, opener=timeout)
        self.assertEqual(blocked["capture_body_state"], "request_error")
        self.assertEqual(blocked["error_type"], "TimeoutError")

if __name__ == "__main__":
    unittest.main()

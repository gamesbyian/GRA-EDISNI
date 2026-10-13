#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from audit_decompiled_consumer_hits import scan


class Tests(unittest.TestCase):
    def test_candidate_hit_is_not_decoder(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"Paper.cs").write_text("class PrintingPaperEasterEgg {\n void Update() { }\n}\n")
            (root/"No.cs").write_text("class TreeRender {}\n")
            (root/"Ghost.cs").write_text("class ThePrintingPaperEasterEggVariant {}\n")
            report = scan(root)
            self.assertEqual(report["files_examined"], 3)
            self.assertEqual(report["matched_files"], 1)
            self.assertEqual(report["totals"]["printer_research"], 1)
            self.assertEqual(report["matches"][0]["hits"][0]["line"], 1)
            self.assertFalse(report["validated_entrypoint"])
            self.assertNotIn("class PrintingPaperEasterEgg", str(report))

    def test_invalid_input_rejected(self):
        with self.assertRaises(FileNotFoundError):
            scan(Path("/unavailable/this/directory"))


if __name__ == "__main__":
    unittest.main()

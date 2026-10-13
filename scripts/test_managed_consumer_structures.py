#!/usr/bin/env python3
"""Synthetic C# fixtures only; no actual INSIDE source in the repository."""
import tempfile
import unittest
from pathlib import Path
from audit_managed_consumer_structures import mask, scan

class ConsumerStructuresTests(unittest.TestCase):
    def test_comment_and_string_mask(self):
        src = ('// void Ghost() { }\n'
               'string x = "void Fake() { }";\n'
               '/* void Absent() { } */\n'
               'public void Real() { this.F(); }\n')
        clean = mask(src)
        self.assertEqual(len(clean), len(src))
        self.assertEqual(src.count("\n"), clean.count("\n"))
        self.assertIn("void Real()", clean)
        self.assertNotIn("void Ghost()", clean)
        self.assertNotIn("void Fake()", clean)

    def test_unknown_name_prefix_validator(self):
        text = '''class Puzzle {
           string entered = "";
           void A7(string next) {
             entered += next;
             string want = expected.Substring(0, entered.Length);
             if (entered != want) entered = "";
           }
           void Unrelated() { Do(); }
        }'''
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/"Fixture.cs").write_text(text)
            report = scan(Path(folder))
            self.assertEqual(report["files_examined"], 1)
            hits = report["matched_files"][0]["methods"]
            self.assertEqual([x["method"] for x in hits], ["A7"])
            self.assertIn("structural-prefix-validator-candidate", hits[0]["reasons"])
            self.assertFalse(report["game_consumer_verified"])
            self.assertNotIn("expected.Substring", str(report))

    def test_signal_subscription_vs_comment(self):
        text = '''class Printer {
          void Setup() { SignalIn.GetOrCreate("printSecretMessage"); }
          void Empty() { /* "printSecretMessage" */ }
        }'''
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/"Printer.cs").write_text(text)
            report = scan(Path(folder))
            self.assertEqual(report["reported_signal_reference_paths"], ["Printer.cs"])
            hits = report["matched_files"][0]["methods"]
            self.assertEqual([x["method"] for x in hits], ["Setup"])
            self.assertTrue(hits[0]["reported_signal_literal"])
            self.assertFalse(hits[0]["validated_consumer"])

    def test_no_cross_method_inference(self):
        text = '''class FalsePositive {
          void A() { input += next; }
          void B() { expected.Substring(0, input.Length); }
          void C() { if (input != expected) input = ""; }
        }'''
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/"Separate.cs").write_text(text)
            self.assertEqual(scan(Path(folder))["matched_files"], [])

    def test_not_existing_path(self):
        with self.assertRaises(FileNotFoundError):
            scan(Path("/not-a-real-inside-csharp-directory"))

    def test_symlink_directory_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/"Inside.cs").write_text("class X { void CheckPassword() {} }")
            try:
                (root/"loop").symlink_to(root, target_is_directory=True)
            except OSError:
                pass
            report = scan(root)
            self.assertEqual(report["files_examined"], 1)

if __name__ == "__main__":
    unittest.main()

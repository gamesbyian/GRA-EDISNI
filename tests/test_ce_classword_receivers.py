"""Tests for the CE purchaser-facing classword receiver domain census.

Run: python -m unittest discover -s tests -p 'test_ce_classword_receivers.py' -v
All data-dependent assertions are intentionally locked to the 2026-10-12 snapshot.
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'ce_classword_receiver', ROOT / 'scripts' / 'audit_ce_classword_receivers.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ClasswordReceiverAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = MODULE.analyze(ROOT / 'data' / 'observations.csv')
        cls.saved = json.loads((ROOT / 'data' /
            'ce-classword-receiver-domain-2026-10-12.json').read_text(encoding='utf-8'))

    def test_source_snapshot_and_independent_saved_result(self):
        a, b = self.actual, self.saved
        self.assertEqual(a['observation_count'], 84)
        self.assertEqual(a['distinct_residues'], 66)
        self.assertEqual((a['body_observed'], a['tail_observed']), (54, 12))
        for key in a:
            if key == 'uniform_subset_null_p_at_least_one_complete_body_class':
                self.assertAlmostEqual(a[key], b[key], places=12)
            else:
                self.assertEqual(a[key], b[key], key)

    def test_raw_vs_conditional_anchors(self):
        a = self.actual
        self.assertEqual(a['body_completions'], 18)
        self.assertEqual(a['tail_completions'], 18)
        self.assertEqual(a['complete_raw_classes'], ['C'])
        self.assertEqual(a['complete_conditional_classes'], list('BCFH'))
        self.assertEqual({k: a['conditional_classes'][k]['values'] for k in 'BCFH'},
                         {'B': [382], 'C': [58], 'F': [407], 'H': [129]})
        self.assertEqual(a['raw_classes']['C']['observed_word'], '---///-/-')
        self.assertEqual(a['frame_option_counts'], [1, 1, 2, 1, 1, 3, 3, 1, 1])

    def test_bitmap_address_typing_rejects_direct_128_256(self):
        for key, row in self.actual['index_projection_tests'].items():
            if key.startswith(('7bits', '8bits')):
                self.assertEqual(row['valid_full_vectors'], 0, key)
                self.assertGreaterEqual(row['minimum_out_of_range'],
                                        6 if key.startswith('7bits') else 3)
            else:
                self.assertEqual(row['valid_full_vectors'], 18, key)

    def test_manual_raw_word_and_inversion(self):
        self.assertEqual(MODULE.decode_word('---///-/-'), 58)
        self.assertEqual(MODULE.decode_word('---///-/-', reverse=True), 184)
        self.assertEqual(MODULE.decode_word('---///-/-', one='-'), 453)

    def test_frame_enumerator_checks_both_polarities(self):
        # The known first physical frame is a unique frame-local pattern.
        rows, known = MODULE.read_stickers(ROOT / 'data' / 'observations.csv')
        self.assertEqual(MODULE.frame_options(known, 0), ['//--///-/'])
        self.assertEqual(len(rows), 84)

    def test_bad_serial_or_conflicting_repeat_fails(self):
        header = 'serial,residue,symbol,image_class\n'
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'bad.csv'
            p.write_text(header + '1,2,/,B\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                MODULE.read_stickers(p)
            p.write_text(header + '2,2,/,B\n110,2,-,B\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                MODULE.read_stickers(p)
            p.write_text(header + '2,2,/,C\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                MODULE.read_stickers(p)

    def test_toy_null_not_assumed_significant(self):
        self.assertAlmostEqual(self.actual[
            'uniform_subset_null_p_at_least_one_complete_body_class'],
            0.17588648657977396, places=12)


if __name__ == '__main__':
    unittest.main()

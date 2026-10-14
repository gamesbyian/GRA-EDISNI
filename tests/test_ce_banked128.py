"""Regression for the conjectural four-bank-by-128 classword decomposition.

Run: python -m unittest discover -s tests -p 'test_ce_banked128.py' -v
"""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location(
    'audit_ce_banked_128', ROOT / 'scripts' / 'audit_ce_banked_128.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FourBankAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = MODULE.audit(ROOT / 'data' / 'observations.csv')
        cls.frozen = json.loads((ROOT / 'data' / 'ce-banked-128-2026-10-12.json')
                                .read_text(encoding='utf-8'))

    def test_source_snapshot_and_saved_output(self):
        self.assertEqual(self.current, self.frozen)
        self.assertEqual((self.current['corpus_records'],
                          self.current['distinct_residues'],
                          self.current['conditional_bodies']), (84, 66, 18))

    def test_all_four_orientation_polarity_controls(self):
        branches = self.current['interpretations']
        self.assertEqual(len(branches), 4)
        for key, result in branches.items():
            self.assertEqual(result['bank_pattern_count'], 1, key)
            self.assertTrue(result['distinct_nine_addresses_per_body'], key)
            self.assertEqual(sum(result['bank_counts'][0].values()), 9, key)
            for offsets in result['seven_bit_offsets'].values():
                self.assertTrue(all(0 <= v < 128 for v in offsets), key)

    def test_source_neutral_native_bank_invariants(self):
        branch = self.current['interpretations']['reverse0_one/']
        self.assertEqual(branch['bank_patterns'][0], [2,2,0,1,2,3,2,1,2])
        self.assertEqual({k: branch['seven_bit_offsets'][k] for k in 'BCFH'},
                         {'B': [126], 'C': [58], 'F': [23], 'H': [1]})

    def test_reversing_and_inverting_produces_different_bank_schemes(self):
        branches = self.current['interpretations']
        self.assertEqual(branches['reverse1_one-']['bank_patterns'][0],
                         [2,2,2,0,0,0,1,1,1])
        self.assertEqual(branches['reverse1_one/']['bank_patterns'][0],
                         [1,1,1,3,3,3,2,2,2])


if __name__ == '__main__':
    unittest.main()

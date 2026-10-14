"""Independent regression for single-CE-owner versus pooled 108-symbol readout."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'ce_owner_local', ROOT / 'scripts' / 'audit_ce_owner_local_channels.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OwnerLocalCodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = MODULE.analyze(ROOT / 'data' / 'observations.csv')
        cls.saved = json.loads((ROOT / 'data' /
            'ce-owner-local-period-audit-2026-10-12.json').read_text(encoding='utf-8'))

    def test_snapshot_matches_exact_saved_artifact(self):
        for key in self.actual:
            if key != 'fixed_period108_body_label_shuffle_null':
                self.assertEqual(self.actual[key], self.saved[key], key)
        left = self.actual['fixed_period108_body_label_shuffle_null']
        right = self.saved['fixed_period108_body_label_shuffle_null']
        for key in left:
            if key == 'exact_conditional_probability':
                self.assertAlmostEqual(left[key], right[key], places=15)
            else:
                self.assertEqual(left[key], right[key], key)
        self.assertEqual(self.actual['physical_stickers'], 84)
        self.assertEqual(self.actual['distinct_h108_residues'], 66)

    def test_unreported_image_classes_remain_inferred_only(self):
        self.assertEqual(self.actual['unreported_physical_image_class'], [43, 427])
        self.assertEqual(self.actual['inferred_classes_for_unreported'],
                         {'43': 'G', '427': 'D'})
        self.assertEqual(self.actual['unseen_local_tokens'], ['A.', 'C.', 'F.'])
        self.assertEqual(self.actual['distinct_observed_local_tokens_class_plus_glyph'], 24)

    def test_periods_and_exact_agreements(self):
        a = self.actual
        self.assertEqual(a['extra_physical_repeat_records'], 18)
        self.assertEqual(a['repeated_h108_residue_groups'], 16)
        self.assertEqual([p['period'] for p in a['zero_symbol_conflict_periods']],
                         [108, 197, 216])
        self.assertEqual([p['period'] for p in a['zero_joint_class_symbol_conflict_periods']],
                         [108, 216])
        self.assertEqual([p['joint_token_conflicts'] for p in a['zero_symbol_conflict_periods']],
                         [0, 6, 0])

    def test_exact_conditional_null_uses_integers(self):
        z = self.actual['fixed_period108_body_label_shuffle_null']
        self.assertEqual(z['all_assignments'], 75553695443676829680)
        self.assertEqual(z['favorable_assignments'], 440079448381568)
        self.assertEqual(z['repeat_group_sizes'], {'1': 38, '2': 14, '3': 2})
        self.assertAlmostEqual(z['exact_conditional_probability'],
                               5.824724334094749e-06, places=15)

    def test_synthetic_repeated_records_and_conflict(self):
        def row(serial, glyph):
            return dict(serial=serial, residue=(serial - 1) % 108 + 1,
                        symbol=glyph, image_class='A')
        matching = [row(1, '/'), row(109, '/')]
        checked = MODULE.scan_periods(matching, 108)
        self.assertEqual(checked[0][-1]['symbol_conflicts'], 0)
        inconsistent = [row(1, '/'), row(109, '-')]
        checked = MODULE.scan_periods(inconsistent, 108)
        self.assertFalse(any(p['period'] == 108 for p in checked[0]))
        self.assertFalse(any(p['period'] == 108 for p in checked[1]))


if __name__ == '__main__':
    unittest.main()

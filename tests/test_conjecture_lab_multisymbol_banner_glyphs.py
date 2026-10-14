#!/usr/bin/env python3
"""Deterministic regression checks for experimental three-symbol glyph search."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import conjecture_lab_multisymbol_banner_glyphs as lab


class MultisymbolGlyphTests(unittest.TestCase):
    def test_physical_and_provisional_status(self):
        s = lab.physical_master()
        self.assertEqual(len(s), 108)
        self.assertEqual(s.count(' '), 42)
        self.assertEqual(s.count('.'), 8)
        self.assertEqual(s[103], '.')
        self.assertEqual(s[45], ' ')
        provisional = lab.physical_master(include_045=True)
        self.assertEqual(provisional[45], '.')
        self.assertEqual(provisional.count(' '), 41)
        self.assertEqual(sum(a != b for a, b in zip(s, provisional)), 1)

    def test_all_four_roles_and_masks(self):
        for ch in lab.CHARS:
            for w in (3, 4, 5):
                for h in (4, 5):
                    for op in lab.OPS:
                        r = lab.roles(ch, w, h, op)
                        self.assertEqual(len(r), h)
                        self.assertTrue(all(len(row) == w for row in r))
                        self.assertTrue(all(0 <= cell <= 2 for row in r for cell in row))

    def test_observation_only_score_is_reconstructible(self):
        for width, provisional, expected in (
            (4, False, (45, 'NLLYSC')),
            (4, True, (45, 'NLLYSC')),
            (6, False, (45, 'JSS')),
            (6, True, (47, 'EQG')),
        ):
            with self.subTest(width=width, provisional=provisional):
                s = lab.physical_master(provisional)
                rows = lab.rows_for(s, width)
                result = lab.search(rows, 20261014 + width)
                self.assertEqual((result['matches'], result['word']), expected)
                canvas = lab.rotate_landscape(rows, [i-1 for i in result['row_permutation_1based']])
                sup = lab.support(canvas, result)
                self.assertEqual(sum(sup['correct_by_expected_role'].values()), expected[0])
                self.assertEqual(sum(sup['observed_positions_by_expected_role'].values()), 67 if provisional else 66)

    def test_shuffle_preserves_known_masks_and_row_censuses(self):
        import random
        original = lab.rows_for(lab.physical_master(), 4)
        shuffled = lab.matched_shuffle(original, random.Random(1337))
        for a, b in zip(original, shuffled):
            self.assertEqual([i for i, ch in enumerate(a) if ch == ' '],
                             [i for i, ch in enumerate(b) if ch == ' '])
            self.assertEqual(sorted(ch for ch in a if ch != ' '),
                             sorted(ch for ch in b if ch != ' '))


if __name__ == '__main__':
    unittest.main()

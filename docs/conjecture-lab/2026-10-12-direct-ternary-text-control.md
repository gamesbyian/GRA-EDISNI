# Direct fixed-width ternary readout control, 12 October 2026

**Mode: DISCOVER.** Input: `data/observations.csv` (84 physical records; 66 of 108 unique residues observed). Reproduce with `python scripts/conjecture_lab_steam_password_direct.py`.

Test three **previously known** text strings as backward-fitted targets. For each target test 3/4/5/6-trit fixed-width character encodings where representable, all six foreground-symbol-to-trit permutations, both read directions and every fitting contiguous offset. Unknown physical residues are not filled or counted as matches. The script includes a masked-source positive control.

| Historical target | Lowest observed-cell conflict count | Exact compatible trials |
|---|---:|---:|
| `NEWPLANETDISCOVERED` | 14 | 0 |
| `LIFEDETECTED` | 7 | 0 |
| `534BRN9653F9J8MMD` | 18 | 0 |

These are *negative results for the three specified historic texts and bounded mapping class only*. They say nothing conclusive about an unknown derived text, a geometric decoder, variable-width encoding or any receiving artifact. Historical known outputs were selected retrospectively, not blindly.

Proceed with the competing Q4 models documented in [the three-role study](2026-10-12-q4-readout-competition.md), rather than widening fixed-width target search solely to create an attractive near-match.

# Experiment 298 — historical Discord column-shift transform audit

_Date: 2026-09-29_

## Question

Does the historical Discord **Column Shift Tool** expose visually or structurally exceptional organization once its bottom-three-row control bits are applied to rotate the nine upper columns?

The tool is preserved verbatim at:

`archive/discord/2026-09-29/Puzzle Column Shift Tool.html`

Its own rules restrict the nine column shifts to:

`2, 8, 4, 4, 4, 2, 4, 4, 2`

possible values, respectively, for exactly **65,536 admissible vectors**.

This experiment treats the transform as a historical hypothesis, not as part of the current machine.

## Preregistered scores

The scores below were selected before inspecting any winning transformed grids. Unknown cells are ignored.

1. **Orthogonal coherence** — number of equal known slash/dash neighbors one cell apart horizontally or vertically.
2. **3×3 block purity** — for each of the nine 3×3 blocks, count the local majority symbol; sum those nine counts.
3. **180° agreement** — number of equal known slash/dash pairs under half-turn symmetry.
4. **Period-3 agreement** — number of equal known slash/dash pairs separated by exactly three rows or three columns.

These are deliberately generic structural/image scores. No score references the present POS3 machine, terminal `100`, a desired plaintext, or a visually selected target.

## Null family

The matched null is the full **unrestricted `8^9 = 134,217,728` column-shift family** using the same top 9×9 sparse grid.

The script computes the unrestricted score distributions exactly by dynamic programming or factorization. There is no Monte Carlo sampling.

Executable audit:

`scripts/audit_discord_column_shifts.py`

## Results

| Score | Admissible mean | Unrestricted mean | Admissible best | Global unrestricted best | Unrestricted fraction ≥ admissible best |
|---|---:|---:|---:|---:|---:|
| Orthogonal coherence | 30.3125 | 30.015625 | 40 | 42 | 0.0001643077 |
| 3×3 block purity | 35.765625 | 35.54296875 | 41 | 42 | 0.0008800998 |
| 180° agreement | 10.59375 | 10.171875 | 16 | 17 | 0.0014144182 |
| Period-3 agreement | 28.09375 | 28.4375 | 39 | 41 | 0.0001318604 |

The tail-constrained family shifts the means only weakly relative to the unrestricted family:

- orthogonal coherence: about **+0.10 unrestricted SD**;
- 3×3 purity: about **+0.14 SD**;
- 180° agreement: about **+0.23 SD**;
- period-3 agreement: about **−0.13 SD**.

None of the four admissible winners reaches the corresponding unrestricted global optimum.

More importantly, because the historical tool searches 65,536 configurations, the best admissible scores are not family-level surprises. Under independent unrestricted draws, the probability that a batch of 65,536 trials contains at least one score at least this large is:

- orthogonal coherence: **0.999979**;
- 3×3 purity: effectively **1.0**;
- 180° agreement: effectively **1.0**;
- period-3 agreement: **0.999823**.

The visual-search multiplicity therefore completely explains the existence of superficially strong winners under these generic scores.

## Interpretation

This is a useful negative result.

The bottom-tail constraints do not produce a strong, score-independent structural concentration in the shifted 9×9 block. Three metrics move slightly upward and one moves slightly downward, but the effect sizes are small, the constrained family misses every unrestricted optimum, and winner-level scores are expected after 65,536 attempts.

Therefore the historical Column Shift Tool should remain archived as a **preregistered negative transform** rather than promoted into the mechanical solve.

This result does **not** prove that every conceivable column-shift interpretation is false. It closes the generic visual-structure version of the hypothesis. Reopening it now requires an independent clue that specifies a narrower target statistic or operation before the transformed output is inspected.

## Consequences

- Do not eyeball the 65,536 transformed grids for a compelling bitmap.
- Do not add a new hand-designed score after seeing a winner unless an external artifact independently motivates that score.
- Preserve the transform and this audit as anti-hindsight evidence.
- No current machine theorem, POS3 claim, Q4 selector claim, or terminal claim changes.

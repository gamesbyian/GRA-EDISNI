# Experiment 431: cross-cube same-coordinate agreement, mask-aware controls

## Trigger

New Discord plots supply explicit null descriptions for 65 known residues:
original unrestricted 81/27 shuffle, then per-cube, per-9-sticker-layer,
and per-cube-plus-letter census-preserving shuffles. Their within-cube
line-neighbour signal remains at chance (observed 0.513, restrictive null
0.513). Their cross-cube same-position value was 33/63 = 0.5238;
the restrictive cube-and-letter null was 0.438, p~0.06.

## Updated physical evidence

The repository's 84 physical records yield **66 unique H108 residues**,
including serial 427 = dot at residue 103. Counting each pair among cube
quarters at the same local offset 0..26 gives **33 matches in 64 known
pairs**, versus the Discord sample's 33/63. The added pair is a mismatch.

| Cube quarters | match/pairs |
| --- | ---: |
| Q1–Q2 | 10/15 |
| Q1–Q3 | 7/12 |
| Q2–Q3 | 7/13 |
| Q1–Q4 | 3/7 |
| Q2–Q4 | 3/8 |
| Q3–Q4 | 3/9 |
| **Q1–Q3 subtotal** | **24/40** |
| **All six pairs** | **33/64** |

Pair counts are correlated because individual physical observations can
enter more than one pair. Do not model 64 pairs as independent Bernoulli
trials.

## New structural null

Randomly generate each primary 9-cell frame under **one exceptional
symbol per solved physical 3×3 column** (27 patterns per chosen minority
polarity), allowing both slash/dash polarities, and retain only generated
patterns matching that *frame's observed number* of slash symbols at
the fixed actual physical observation mask. This preserves the existing
3×3 grammar and frame-wise colour composition but *not* the specific
observed symbol placement. Conditioning on the latter would give the
observed correlation by construction.

For Q4, generate the 3^9 possible exceptional-slash depth patterns
and retain the **6,120** choices with exactly four slashes at the twelve
physically observed Q4 sites. The original eight observed Q4 dots are
not kept at their precise positions during the null shuffle.

Primary per-frame eligible pattern counts: 12,12,6,9,12,16,9,12,12.
Across 100,000 deterministic JS samples of this exact setup, the
diagnostic results were:

| Statistic | Actual | Null mean | fraction >= actual |
| --- | ---: | ---: | ---: |
| All cross-cube pairs | 33/64 | 25.828/64 | 0.0356 |
| Primary-only (Q1–Q3) | 24/40 | 20.696/40 | 0.1691 |
| Q4-involving pairs | 9/24 | ~5.132/24 | not separately tested |

These are **retrospective, model-conditioned tails**, not
discovery-adjusted significance values. They are also sensitive to how
different cube alphabets are treated as binary colours. The per-cube
and per-letter shuffle result reported by the community (p~0.06) is
an important counterweight: no one null should be privileged after
seeing the match rate.

## Same-mask geometric transform controls

A second comparison uses only actual Q1–Q3 observations. For every
rotation/reflection/one-step cyclic 3×3 translation, compare the
identity same-coordinate match with the transformed match on exactly
the **same** source coordinates having observed targets under *both*
placements. This avoids falsely comparing percentages with different
visibility masks.

| Competing target registration | common pairs | identity matches | shifted matches |
| --- | ---: | ---: | ---: |
| rotation 90° | 23 | 12 | 12 |
| rotation 180° | 26 | 17 | 16 |
| rotation 270° | 30 | 18 | 16 |
| horizontal reflection | 33 | 21 | 17 |
| vertical reflection | 32 | 18 | 16 |
| main diagonal | 28 | 17 | 19 |
| antidiagonal | 26 | 15 | 16 |
| cyclic shift row +1 | 27 | 16 | 13 |
| cyclic shift column +1 | 28 | 15 | 12 |

Identity does **not** dominate every alternative: on matched support,
the diagonal and antidiagonal reflections can equal or outperform it.
These are exploratory diagnostics, not preselected statistical tests.

## Interpretation

The broad 33/64 cross-cube effect is not fully explained by the specific
frame-constrained null constructed here. However, its statistical
strength mostly disappears when restricting to the shared slash/dash
alphabet in primary cubes 1–3, and exact XY registration is not uniquely
favoured over all rotations/reflections. Thus there is **no sufficiently
robust evidence yet for a geometrically registered four-cube readout**.

This does not refute the one-of-three Q4 depth-address mechanism, which
has independent observation and historical arguments (see Experiments
317, 373, 427–430). It does prevent the 52% cross-cube colour
correlation from serving as separate confirmatory evidence for it.

Next possible discriminator: predict *which* Q4/primary registered
symbol matches should appear under a **frozen** operation family,
rather than rewarding a general similarity statistic chosen after
inspection. The current 42 unobserved cells are not additional
independent observations.

## Reproduction

```bash
python scripts/audit_cross_cube_masked_null.py --samples 100000 --seed 20261008
```

The script asserts updated physical counts and reports the primary,
Q4-involving and overall comparisons plus matched-support transforms.
Its Python random generator will produce a different Monte Carlo
realization than the independently run JS baseline, but should approach
the same null expectations. New Python code awaits checkout execution.

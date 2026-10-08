# Experiment 475: registration without Cube 4

## Question

Experiment 471 showed that the all-four-cube **observed magnitude**
of exact-position minus alphabetical-horizontal-X similarity remains
unusual under frame-census nulls, even though full completed-string
registration signs arise naturally under weak frame grammar
(Experiment 470).

Does the same measured effect exist without *any* use of Cube 4?
This matters because the proposed Q4 command layer might be a
separate instruction channel, and the Q4 slash/dot alphabet
differs from the primary slash/dash alphabet.

## Q1–Q3-only observed values

Using the supplied Cube Registration Lab's exact no-wrap, ±1,
different-cube pair rules, but accepting only Q1–Q3 pairs:

| Relation | Matching observed pairs | Same-symbol rate |
| --- | ---: | ---: |
| Exact corresponding coordinates | **24/40** | **60.0%** |
| Alphabetical X shifted ±1 | **16/47** | **34.0%** |
| Physical X shifted ±1 | 18/41 | 43.9% |
| Alphabetical Y shifted ±1 | 23/44 | 52.3% |
| Z shifted ±1 | 24/50 | 48.0% |

The observed alphabetical-X difference is **25.96 percentage points**,
only a little smaller than the all-four-cube 27.75-point effect.

At the primary cube-pair level:

| Cube comparison | Exact matches | Alphabetical-X matches |
| --- | ---: | ---: |
| Q1–Q2 | 10/15 | 6/15 |
| Q1–Q3 | 7/12 | 4/17 |
| Q2–Q3 | 7/13 | 6/15 |

Caution: each relationship has its own set of observed pair positions
and denominator. These are exact Lab relation rates, **not**
same-mask causal pair differences.

## Census- and missing-mask-preserving structural null

I again preserve which physical positions are known and each
primary 9-sticker frame's **number of observed slash marks**,
without conditioning on the exact placements of those slashes.

Each randomized primary frame has exactly three minority marks
(either polarity), with or without the additional one-minority-
per-physical-column constraint. **No Q4 observations, symbols or
completion assumptions are used in generating or scoring this null.**

Two independent 250,000-draw NumPy implementations yielded:

| Q1–Q3-only null | Unadjusted tail for alphabetical X contrast | Exploratory six-test X/Y/Z × both-layout max-Z tail |
| --- | ---: | ---: |
| Three-of-nine primary frames | **0.0172** | **0.0565** |
| Plus physical-column placement | **0.0143** | **0.0433** |

This is weaker than the all-four-cube result in Experiment 471,
particularly with the limited six-comparison maximum.
Nonetheless, the core primary-cube contrast is not entirely
explained by the tested frame-census nulls.

The main observation is **not** that Cube 4 is unnecessary for
the puzzle. The narrower conclusion is that **the statistical
alphabetical-X registration signal already exists among the
first three cubes**, and therefore cannot by itself prove a
special Q4 selector or an intended four-cube geometric mechanism.

## Reproduction

```bash
python scripts/audit_cube_primary_registration_null.py --samples 250000
python scripts/audit_cube_primary_registration_null.py --samples 5000
```

The standard-library script uses the canonical physical observation
CSV and the existing lab pair definitions, independently verifies
24/40 and 16/47, and reports both declared nulls plus simultaneous
six-comparison maxima. Because its pseudorandom generator differs
from the independent NumPy reference, the Monte Carlo tail
fractions are expected to vary within finite-sample error.
Results are **retrospective diagnostics**, not adjusted for the
community's historical exploration of alternative cube layouts.

# Experiment 470: how generic is cube registration in completed strings?

The previous exact lab reproduction (Experiment 459) showed that **all
324 observation-compatible full masters** built from physical
one-minority-per-column frames and a one-slash-per-A-I Q4 depth stack
exhibit greater full-grid same-coordinate agreement than shifted
agreement. This experiment weakens the frame grammar before calculating
the same relationship.

## Parent ensembles

Use the canonical **84 physical sticker records / 66 H108 residues**.
Fix every observed foreground mark. In the first nine nine-symbol frames,
allow either slash/dash polarity with exactly three of the minority
symbol, but **do not** impose physical column placement. In Q4,
require one slash per each of the nine A–I depth stacks, compatible with
the observed dot/slash marks.

There are **12,960** compatible primary bodies × **18** compatible Q4
selectors, producing **233,280** complete candidate strings. The nested
physical-column grammar instead has 18 primary bodies × 18 selectors,
or 324 masters.

Count unordered pairs in **different quarters** using precisely the
community Cube Registration Lab's no-wrap ±1 X/Y/Z pair definitions.
For each completely specified string, calculate each relation's
matching fraction using its entire eligible pair set, not only the
positions physically observed.

## Exact counts

| Comparator (same spot beats this shifted relation) | 233,280 broad completions | 324 physical-column completions |
| --- | ---: | ---: |
| Physical horizontal X | **229,349** (98.31%) | 324 (100%) |
| Physical vertical Y | **214,525** (91.96%) | 324 (100%) |
| Depth Z | **232,395** (99.62%) | 324 (100%) |
| Alphabetical horizontal X | **233,136** (99.94%) | 324 (100%) |
| Alphabetical vertical Y | **220,876** (94.68%) | 324 (100%) |

The broad physical X mean same-minus-shift difference is about
**5.85 percentage points**; alphabetical X is **7.95 points**.
Strengthening to physical-column grammar raises these averages
to about **7.08** and **10.58 points**, respectively.

Thus a **positive sign** for the registration contrast is already
close to automatic under a very weak three-of-nine completion grammar.
It is not unique to Cube 4 as a 3D instruction layer, and saying that
"all 324 completions are registered" is *not* independent confirmation.

Crucial limitation: the **magnitude** of the contrast among the
currently observed subset is a different statistic. Experiment 471
tests that under fixed physical observation masks and frame-census
preserving nulls rather than comparing only signs across fitted
complete masters.

## Reproduction

```bash
node scripts/audit_cube_registration_extended.js
```

The script asserts 233,280/324 completion family sizes and the exact
233,136 alphabetical-X count. Numbers were separately verified by
NumPy exhaustive enumeration. No additional physical observations
or semantic target are claimed.

# Experiment 461: does the *observed magnitude* of alphabetical X survive a frame-structural null?

## Why a second null matters

Experiment 460 finds that most grammar-compatible completed strings
have a positive same-position-versus-shift comparison. That is a
**conditional sign test of fitted complete masters**, not an
independent null for the actual 66 observed foreground marks. To test
whether the recovered stickers' **large** exact-vs-alphabetical-X
difference is ordinary under broad production constraints, this
experiment samples structurally complete masters without conditioning
on the individual observed mark positions.

The physical **observation mask is fixed**. For every primary
nine-symbol frame, retain the actual *number of observed slash
marks* among its observed sites, but freely rearrange the slash/dash
values at those sites, subject to the null's frame grammar. For Q4,
choose a uniform one-slash-per-depth A–I completion subject only to
the total of **four slashes among the twelve observed Q4 sites**.
Thus the Q4 null has **6,120** legal depth-code sequences. These null
strings deliberately need not match the actual mark at every
individual observed position; otherwise the statistic would be
unchanged by construction.

Two sampling families are checked:

- **Three-of-nine grammar:** exactly three minority marks per primary
  frame, either polarity.
- **Plus physical-column grammar:** each of the three physical
  columns in each primary frame contains exactly one minority mark.

For both, count only physically observed cross-quarter pairs under
the independent Discord lab's same / ±1 X,Y,Z relation sets,
including the differing denominators for each relation.

## Constrained Monte Carlo, current 66-residue ledger

250,000 independently generated complete strings per grammar,
seeded `20261008` and `20262935` respectively. The original
actual rates and contrast are fixed:

- Exact: **33/64 = 51.5625%**.
- Alphabetical X: **20/84 = 23.8095%**.
- Actual exact-minus-alphabetical-X: **27.75298 percentage points**.

| Grammar-constrained null | Mean alphabetical-X contrast | Tail ≥ observed contrast | Maximum over six declared X/Y/Z × physical/alphabetical contrasts |
| --- | ---: | ---: | ---: |
| Three-of-nine only | **3.52 points** | **0.002732** | **0.010016** |
| Physical-column also | **3.11 points** | **0.002764** | **0.008528** |

The maximum-statistic correction standardizes each contrast against
its own structural-null distribution and compares the observed
maximum with the maximum of the **same six** standardized comparisons
in each simulated realization. These tail fractions are
**Monte Carlo estimates**, with finite sampling error, not exact
permutation fractions or universal discovery-adjusted p-values.
The null's equal weighting of grammatical choices is a modelling
convention, not a demonstrated production probability.

For comparison, the earlier exact 331,776-way cube×A–I
colour-count-preserving null gives an alphabetical-X uncorrected tail
near **0.0132**, and a six-comparison maximum-statistic tail near
**0.0393**. This new structural null preserves different
properties, and therefore need not yield matching p-values.

## What is and is not explained

The grammar strongly explains the **direction** of the complete-data
comparison (Experiment 460), but the *actual magnitude* of the
alphabetical-X registration effect remains uncommon under these
new frame-census-constrained nulls. That is legitimate exploratory
evidence of positional dependence not fully specified by the tested
grammars.

It is **not** evidence that Cube 4 specifically carries a physical
depth-selection instruction. The original Discord researcher tested
multiple axes, coordinate orders, wraps, nulls and candidate
geometries; the alphabetical X contrast was noticed among those
options. An exact six-contrast family correction cannot compensate
for the broader, historically accumulated hypothesis search.
Observation acquisition is unlikely to be a guaranteed uniform
sampling mechanism, and any manufacturing geography or photo
selection bias remains a confounder.

## Reproduction

```bash
node scripts/audit_cube_registration_extended.js
node scripts/audit_cube_registration_extended.js --fast
```

The second command runs a smaller **5,000-sample smoke check**;
the first uses 250,000 samples per null. The source freezes both
layouts and all three shifts *before* drawing Monte Carlo samples.
The same null was implemented independently in NumPy and gave
compatible, not identical, Monte Carlo estimates.

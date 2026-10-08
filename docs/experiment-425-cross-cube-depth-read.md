# Experiment 425: Q4-selected depth read across the first three cubes

## Narrow question

Does the Q4 physical slash/dot index select a depth in each of Q1, Q2,
Q3 whose foreground symbols agree more often across the three cubes
than an independently chosen depth per A–I address?

This tests the simplest literal interpretation of the community's four
3×3×3-cube proposal. It uses *only* raw, confirmed foreground marks;
the incumbent transducer, filled symbols, visual output, and semantic
filters are excluded.

## Exact mapping and score

For image-class index `j=0..8`, the slash location among Q4's three
serials `82+j, 91+j, 100+j` is the depth choice `d`. Read the three
primary quarter marks at residues `1+27q+9d+j`, for `q=0,1,2`.
Ignore unobserved marks. Count agreements among all observed unordered
pairs of the selected three positions, divided by observed pairs.
This is a simple preregistered *same-symbol agreement* diagnostic, not
an assumption that the eventual code requires identical symbols.

The Q4 observed tails in A–I order are:

```
A ???   B ?./   C ???
D .?.   E /.?   F ?/?
G ?.?   H ..?   I .?/
```

Allowed depth choices are A={0,1,2}, B={2}, C={0,1,2},
D={1}, E={0}, F={1}, G={0,2}, H={2}, I={2}.
There are **18** possible Q4 slash-index completions on the latest
physical CSV (the older Experiment 317 used 36; dot residue 103
subsequently forces D's slash to depth 1).

## Exact result

All 18 admissible Q4 codes produce one of three agreement counts:

| agreement | observed pairs | compatible Q4 codes |
| ---: | ---: | ---: |
| 10 | 16 | 6 |
| 11 | 17 | 6 |
| 10 | 17 | 6 |

Thus the admissible selected-depth concordance lies between 58.82%
and 64.71%, depending on unresolved Q4 positions.

As a broad comparator, enumerate all `3^9 = 19,683` independently
chosen depth addresses with uniform equal probability, and re-score
the same observed physical cells (so varying physical coverage is
reflected in the denominator).

- 10,608/19,683 (53.89%) of null depth assignments score at least
  as high as the lowest admissible Q4 score (10/17).
- 6,753/19,683 (34.31%) score at least as high as the highest
  admissible score (11/17).

The Q4-indexed direct-depth read therefore does *not* show strong
cross-quarter same-symbol coherence under this diagnostic. This
doesn't eliminate a routing/masking/other depth-address consumer.
It does eliminate this concordance statistic as a justification for
preferring direct voxel stacking over simpler rival models.

## Evidence controls

The 18 codes use the same Q4 observations as the prior tail
one-hot family and are **not** new physical observations or a clean
independent holdout. The experiment tests cross-quarter coherence,
which is separate from Q4 tail feasibility. The null is a descriptive
equal-depth-address comparator, not a generative model of sticker
manufacturing or a valid discovery-adjusted p-value.

The next admissible 3D experiment needs a *specified* output operation
or an independent clue; blind rotations, projections, or arbitrary
transform searches would be post-hoc and are not authorized here.

Reproduce: `python scripts/audit_cube_depth_read.py`.

# Experiment 427: observation-only 3×3×3 cube-depth null

## Origin and preregistered scope

A community suggestion maps 108 residue positions to four consecutive 27-cell
cubes. Each cube has three 9-position A–I XY slices at depths 0, 1, 2.
This was already considered in Experiments 18, 34, and 46. The new bounded
test asks whether the physical Q4 observations alone make an exact-one-slash
depth-stack code surprising against a census-preserving, observation-site-fixed
label-exchange null. No generated machine completion or visual recognition
is included in the test.

The mapping is `residue - 1 = 27*q + 9*d + j`, where `q=0..3`,
`d=0..2`, and `j=0..8`. The XY orientation may follow the solved
background tile layout `IAB/CDE/FGH`, but rotations/reflections only
relabel complete XY stacks and cannot change the statistic tested here.

## Data

`data/observations.csv` contains 84 physical records and 66 distinct
H108 residues at this checkpoint. Q4 has 12 known positions (four slash,
eight dot). The nine depth stacks, in serial A–I order, are:

```
A ???   B ?./   C ???
D .?.   E /.?   F ?/?
G ?.?   H ..?   I .?/
```

All stacks remain compatible with *exactly one* slash. That compatibility
alone is not evidence for intended cube encoding.

## Exact null

Condition on the twelve observed Q4 sites and the observed total of four
slashes. Assign slashes to any four of the twelve sites, holding everything
else dot. There are C(12,4)=495 equally weighted assignments. Of those,
280 avoid placing multiple slashes on any XY depth stack. Every such
assignment can be completed to exactly one slash on all nine stacks,
because no stack has all three depths physically observed.

Conditional compatible fraction: **280/495 = 56.5657%**.

This is a deliberately narrow diagnostic, not a confirmatory p-value.
The real physical serials/marks are not necessarily sampled uniformly;
hypothesis discovery used the same corpus. Even on this favourable
conditional null, the observed compatibility is unexceptional.

## Discrimination and next step

- D4 rotation/reflection of XY does not change exact-one depth-stack
  compatibility. It is wrong to count eight orientations as independent
  successful tests.
- The depth stack code remains a legitimate *addressing representation*.
  Existing reset-era Experiment 317 originally established a 36-completion
  one-slash-tail family from an earlier observation snapshot; the current
  corpus has only 18 completions (Experiment 428). This compatibility
  must not be counted twice as fresh evidence for a cube.
- Compare a *frozen* depth-index prediction family to genuinely withheld
  or future physical observations, and separately challenge depth-index
  consumption against simple row/chunk and column/rail rivals (Experiment
  318 could not distinguish those).
- No new 3D images, semantics, machine-transition assumptions, or
  missing-sticker predictions are licensed merely by this null test.

Reproduce with `python scripts/audit_cube_observation_null.py`.

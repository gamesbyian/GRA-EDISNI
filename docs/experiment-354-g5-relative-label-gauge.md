# Experiment 354 — G5 relative-label gauge audit

_Status: preregistered before result inspection, 1 Oct 2026._

## Question

Experiment 290 found that among the four literal selector/body coordinate-copy operations
`(q,q)`, `(q,S)`, `(S,q)`, and `(S,S)`, only `(q,S)` is simultaneously
selector-sensitive, external-q preserving, and nondegenerate.

Experiment 352 later exposed a hidden assumption in that result: the tail's three positional labels and the
body depth axis were silently given the same `0,1,2` orientation.

Experiment 354 isolates that assumption.

> If G5 keeps the literal replace-depth operation, which relative labeling of the tail positions onto body depth is supported before any second-pass, route, or terminal criterion is used?

## Frozen family

Let `pi` be one shared permutation of the three tail labels:

```
pi : {0,1,2} -> {0,1,2}
```

There are exactly `3! = 6` such maps.

For each candidate machine and each physical cell `j`, define the first-pass body address as:

```
(q, d, j) -> (q, pi(S(j)), j)
```

The same `pi` is used globally for all cells and all external q surfaces.

No per-column relabeling, state-dependent map, affine offset, route target, or second recursive pass is permitted.

## Inputs

Use the same raw-compatible family as Experiment 290:

- 6 primary payloads from physical observations;
- 36 tail selectors from physical observations;
- 216 Cartesian-product candidate machines.

For every `pi`, build the three external-q output surfaces and decode each only by the already-supported one-minority-per-column positional rule.

## Frozen measurements

For each of the six permutations report:

1. number of raw candidate machines whose three first-pass surfaces are all valid positional columns;
2. number of distinct three-surface decoded output families;
3. whether output varies with external q;
4. whether output varies across surviving selector completions.

Primary comparison is survivor count. Ties remain ties unless the frozen nondegeneracy measurements distinguish them.

## Guardrail

This experiment does **not** ask which map reaches terminal `100`, which produces the incumbent route shell, which preserves 14 final states, or which has nicer semantics.

A unique identity result would support shared physical orientation between tail position and body depth inside the literal G5 family.

A multi-permutation tie would show that the shared orientation is a gauge at first-pass level.

A different permutation winning would falsify the incumbent orientation inside this family.

## Reproducibility

Run:

```bash
python scripts/audit_g5_relative_label_gauge.py
```

# Experiment 354 — G5 relative-label gauge audit

_Status: completed; preregistration frozen before result inspection, 1 Oct 2026._

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


## Result

The six-way audit is decisive.

| tail→depth labeling `pi(0)pi(1)pi(2)` | first-pass survivors | distinct output families |
|---|---:|---:|
| `012` | **20** | **6** |
| `021` | 0 | 0 |
| `102` | 0 | 0 |
| `120` | 0 | 0 |
| `201` | 0 | 0 |
| `210` | 0 | 0 |

All six identity-surviving output families vary with external q, so the identity result is not being carried by a constant/trivial surface. Ten of the 36 raw selector completions participate in the 20 surviving raw machines.

Every non-identity shared relabeling is physically incompatible with first-pass positional closure.

## Interpretation

Experiment 352 showed that the primary row labels are gauge **before** a consuming operation identifies them with another three-position carrier.

Experiment 354 now fixes the relative gauge between the tail selector and body depth axis inside the literal G5 family:

> the observed tail position and the body-depth position must share the same orientation.

This is stronger than an aesthetic preference and weaker than an external clue. It is an observation-constrained identification that emerges at the first point where the two independently motivated positional carriers interact.

Combined with Experiment 290:

1. among the four literal coordinate-copy consumers, `(q,S)` is uniquely selector-sensitive, q-preserving and nondegenerate;
2. among all six shared tail→depth relabelings of that operation, only identity survives at all.

Thus the exact literal G5 representative is unique inside this small human-legible family **before** G6, route selection, terminal `100`, hidden-state count, or semantic interpretation.

What remains model-level is the higher-order choice to search the literal coordinate-copy family in the first place. Experiment 353 found no independent historical source explicitly instructing that substitution.

Workflow evidence: run `36819851134`, artifact `11142559363`, digest `sha256:1534a573e98833677cb360b1259028fe625de2be758b2ca28f240c5156ae96b1`.

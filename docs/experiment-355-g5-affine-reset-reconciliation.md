# Experiment 355 — G5 affine-family reset reconciliation

_Status: rerun/reconciliation of pre-existing Experiments 266–267, 1 Oct 2026._

## Purpose

Experiments 353–354 narrowed the current G5 question:

- no independent historical/external source explicitly supplies the exact substitution;
- inside the smallest literal coordinate-copy family, `(q,S)` is uniquely nondegenerate;
- all five non-identity tail→depth label relabelings fail first-pass positional closure.

Before inventing a broader new consumer family, this experiment checks whether the repository already contains the relevant broader attack.

It does: Experiments 266–267 exhaust affine maps on the two ternary coordinates `(q,S)`.

Experiment 355 does not define a new model family. It reruns those frozen scripts on current main and reconciles their implications with the epistemic reset.

## Frozen prior experiments

### Experiment 266

Enumerates every invertible affine map over `F3^2`:

```
(q', d') = M (q,S) + t
```

There are `|AGL(2,3)| = 432` such maps.

Acceptance criterion is only that all three first-pass surfaces decode as valid positional columns for the raw-compatible 216 machines.

No terminal, route, hidden-state count, expected first-pass words, or semantic target is supplied.

Frozen asserted result:

- survivor-count distribution: `0:402, 1:6, 7:6, 10:12, 20:6`;
- maximum first-pass retention: 20;
- exactly six maps attain 20;
- every maximizing map has `d' = S` exactly;
- their only freedom is an affine permutation of external `q`: `q'=a*q+u` with `a∈{1,2}`, `u∈{0,1,2}`.

Thus no invertible affine mixing of `q` into the selected body depth survives at maximum retention.

### Experiment 267

Extends to all `3^6 = 729` affine maps, including singular/information-destroying maps.

Frozen asserted result:

- singular maps can retain far more raw states, up to all 216;
- every perfect-retention map ignores selector `S` in both output coordinates;
- every perfect-retention map is singular;
- among affine bijections, 20 remains the maximum.

This is the negative control explaining why raw-state count alone cannot justify singular consumers: information erasure trivially inflates compatibility.

## Reset interpretation

Experiments 290, 354 and 266 now form a nested G5 evidence chain:

1. **literal-copy family:** `(q,S)` is the unique selector-sensitive, q-preserving nondegenerate copy;
2. **relative-label family:** identity tail→depth registration is the only one with any first-pass survivors;
3. **all invertible affine consumers:** every maximum-retention map forces `d'=S` exactly, with only external-q relabeling left.

Therefore the body-depth substitution is not a fragile consequence of one hand-picked parameterization. It is the unique maximum-retention depth behavior throughout the natural affine-bijection parent family.

What remains model-level is the parent-family principle itself: preserve the two-coordinate address carrier under an invertible affine transformation and require first-pass positional closure. Experiment 267 shows why dropping information preservation makes the comparison meaningless.

## Reproducibility

Experiment 355 reruns, unchanged:

```bash
python scripts/audit_affine_first_pass.py
python scripts/audit_affine_degeneracy.py
```

and preserves stdout as workflow artifacts.


## Rerun evidence

Current-main rerun succeeded without modification.

- workflow run: `36820146966`
- artifact: `11142778794`
- digest: `sha256:8b3a63f56a2fd73c8a065b9d061dfc9358d312867111f91528c3a02c3b8121c7`

The reproduced Experiment-266 distribution is `{0:402, 1:6, 7:6, 10:12, 20:6}`; all six 20-state maxima force `d'=S`. Experiment 267 again finds 24 perfect-retention singular maps, all of which erase selector S.

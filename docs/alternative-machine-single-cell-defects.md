# Experiment 296 — Single-cell recursion-defect audit

## Question

How brittle is the current two-pass selector operation to the smallest possible local rewrite?

This experiment deliberately leaves the source representation alone. It does **not** weaken primary POS3, alter Q4 polarity/codebook assumptions, change the carrier, or search a new semantic output. Instead it perturbs one address read at one physical A–I cell by one nonzero ternary step.

That makes it orthogonal to the current primary/input-POS3 work in PR #31 and the Q4 representation work in PR #32.

## Parent space

Use the established Experiment-250 raw parent:

- 6 raw-compatible primary payloads;
- 36 raw-compatible Q4 selectors;
- 216 raw candidate machines.

Canonical recursion:

```
first pass:  (q, S(j), j)
second pass: (S(j), S(j), j)
```

The defect family changes exactly one physical cell and one coordinate role:

- first-pass depth `S -> S+1` or `S+2`;
- second-pass quarter `S -> S+1` or `S+2`;
- second-pass depth `S -> S+1` or `S+2`.

There are exactly `9 × 2 × 3 = 54` one-defect operations.

The only acceptance tests are the existing structural ones:

1. all three first-pass surfaces decode as dash-POS3;
2. the second-pass surface decodes as dash-POS3.

No expected state count, terminal value, master set, or route word is used as a filter.

## Result

The canonical operation retains 14 states and terminal `100`.

No one-cell first-pass defect preserves that exact machine family.

Seven **second-pass** defects do preserve it exactly:

| role | cell | offset | support |
|---|---|---:|---|
| second-pass q | E | +1 | selector E=0; canonical and alternate sources are `/` in all 14 states |
| second-pass q | E | +2 | same |
| second-pass q | F | +1 | selector F=1; both sources are `/` in all 14 |
| second-pass q | F | +2 | same |
| second-pass q | I | +1 | selector I=2; both sources are `/` in all 14 |
| second-pass d | C | +1 | selector C∈{0,2}; both sources are `-` in all 14 |
| second-pass d | I | +1 | selector I=2; both sources are `/` in all 14 |

For each of those seven, the complete second-pass **surface itself** is unchanged for every one of the canonical 14 machines, not merely its decoded `100` value. They are therefore true local equality-locus gauges.

This is an important boundary on claims of operation uniqueness. If pass-specific, cell-specific exceptions are admitted, the physical object cannot distinguish these seven address rewrites. Their existence does not undermine the compact canonical rule; it shows why the rule's uniformity is part of the model class.

## The one higher-retention sibling

Exactly one one-cell defect retains more raw-compatible states while still producing an invariant terminal:

```
first-pass depth at A: S -> S+1
states: 16
terminal: 100 for all 16
```

Its first-pass functional families are:

```
102 / 012 / 100
102 / 022 / 100
112 / 012 / 100
112 / 012 / 120
122 / 022 / 100
```

So the intermediate rank grows from 3 to 5.

More importantly, the last family contains no ternary permutation at any q position. The sibling therefore cannot assign a reversible route word to every functional class. It preserves the endpoint only by degrading the route layer that makes the canonical machine structurally coherent.

This is exactly the sort of adversarial sibling Priority 5 asks for: similar carrier, same ternary coding, same two-pass budget, tiny local description change, more retained raw states, same terminal, but a worse internal computation.

## Survivor anatomy

The 18 defects in each role have these final-state distributions:

```
first_d:
  0:10, 4:1, 6:1, 7:2, 8:1, 10:2, 16:1

second_q:
  0:5, 7:2, 8:2, 10:1, 14:6, 16:1, 18:1

second_d:
  0:9, 4:2, 6:2, 7:1, 8:1, 10:1, 14:2
```

The broader lesson is asymmetric:

- first-pass local damage usually destroys closure or changes the functional quotient;
- second-pass local damage exposes several exact equality gauges because the terminal reads through symbol-equal addresses.

## Interpretation

This experiment does **not** argue for adding seven exceptions to the machine. The opposite conclusion is more useful.

Once the operation grammar permits arbitrary per-cell, per-pass exceptions, extra freedom appears faster than explanatory value. The canonical uniform substitution remains the compact representative. The seven invisible rewrites should be treated as a known quotient of an over-broad local-defect family, not as unresolved intended behavior.

That gives Priority 5 a concrete stop signal for this direction:

> cell-specific exception grammars are too permissive to improve identification unless an independent physical cue licenses a particular exception.

The 16-state A sibling is also useful as a regression adversary. Any future criterion claimed to characterize the intended machine should explain why it prefers the clean three-class reversible route structure over this nearly identical terminal-preserving alternative.

## Reproduction

Run:

```bash
python scripts/audit_single_cell_recursion_defects.py
```

The script asserts the full 54-operation outcome distribution, the seven exact equality gauges, and the route-degeneracy of the unique >14-state invariant-terminal sibling.

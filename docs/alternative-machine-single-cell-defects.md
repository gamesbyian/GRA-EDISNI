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


# Experiment 297 — Up-to-two-cell first-pass defect audit

Experiment 296 found that one local first-pass exception could retain 16 raw-compatible states and terminal `100`, but only by expanding the functional quotient and breaking reversible routing. Experiment 297 asks whether **two** local exceptions can repair that weakness.

## Parent family

Keep the second pass canonical.

For the first pass, allow depth `S(j)` to be shifted by `+1` or `+2` at zero, one, or two distinct A–I cells.

The complete family has:

```
1
+ 9*2
+ C(9,2)*2^2
= 163 configurations
```

Every configuration is enumerated exactly.

## Results

The final-state / terminal-cardinality distribution is:

```
(0,0):   128
(2,1):     2
(3,1):     2
(4,1):     5
(5,1):     4
(6,1):     3
(7,1):     2
(8,1):     3
(10,1):    2
(12,1):    3
(14,1):    4
(16,1):    2
(18,1):    1
(20,1):    2
```

So local exceptions can indeed manufacture larger invariant-terminal families. The two maximum-retention configurations are:

```
A1 + D1
A1 + D2
```

Both retain 20 raw-compatible states and terminal `100` for every survivor.

Neither has a valid three-class reversible route shell.

## Exact 14-master siblings

Three two-cell configurations preserve the **exact same 14 physical masters** and terminal `100` while altering the first-pass computation:

```
B1 + H1
B2 + H2
F2 + I1
```

Their first-pass families are:

```
B1+H1:
  102 / 002 / 122
  102 / 012 / 102
  102 / 022 / 102

B2+H2:
  100 / 002 / 122
  100 / 012 / 102
  100 / 022 / 102

F2+I1:
  102 / 202 / 120
  102 / 212 / 100
  102 / 222 / 100
```

All three fail the route criterion.

- `B1+H1` forces duplicate reversible choice `102` across classes.
- `B2+H2` contains a functional family with no reversible word at all.
- `F2+I1` again forces duplicate `102` routes.

So identical physical masters and identical terminal do not imply an equivalent intermediate machine.

## Route-capable configurations

Across all 163 zero/one/two-cell configurations, only three admit the Experiment-278 route criterion:

```
canonical : 14 states
C1        :  7 states
C2        :  7 states
```

All three expose the same unique route shell:

```
120 / 012 / 102
```

The canonical operation therefore **uniquely maximizes raw-state retention among route-capable configurations** in this local-defect family.

This is a considerably stronger adversarial statement than merely observing that local defects tend to fail. Some local variants retain 18 or 20 states and some preserve the exact 14 masters, but once the independently motivated reversible route layer is required, canonical wins cleanly.

## What this says about Priority 5

The local-exception family is useful precisely because it is hostile to the preferred model:

- tiny description changes can preserve terminal `100`;
- tiny changes can preserve the exact physical 14-master family;
- tiny changes can even retain **more** raw-compatible states.

The endpoint and raw-state retention are therefore insufficient discriminators by themselves.

The route layer continues to do real work. In the full 163-member family, it leaves canonical at 14 states and only two damaged seven-state C siblings.

That suggests a productive general rule for future alternative-machine searches:

> retain route structure as an independent model-selection criterion, and treat terminal agreement alone as weak evidence.

It also reinforces the stopping signal from Experiment 296. Expanding to arbitrary cell-local exceptions rapidly creates representational siblings, while the structurally meaningful discriminator remains the same reversible route shell already derived independently.


# Experiment 298 — Full 3^9 first-pass local-offset closure

Experiments 296–297 suggested that local exception freedom grows rapidly, but the family is still small enough to close exactly.

At every A–I cell independently choose:

```
d' = S(j) + offset[j] mod 3
offset[j] ∈ {0,1,2}
```

External q remains untouched and the second pass remains canonical.

This is the complete `3^9 = 19,683` cell-local first-pass offset family. No defect-count bound remains.

## Global result

Before first-pass closure, the canonical second pass admits 96 of the 216 raw machines as valid POS3 terminals, and all 96 already terminate at `100`.

The full first-pass search produces this survivor-count distribution:

```
0  -> 19059
1  ->    16
2  ->    88
3  ->    48
4  ->    72
5  ->    32
6  ->    88
7  ->    16
8  ->    64
9  ->    16
10 ->    64
12 ->    48
14 ->     8
16 ->    24
18 ->     8
20 ->    24
24 ->     8
```

The largest local-offset machines retain 24 states. None has a reversible route shell.

## The eight 14-state operations

Exactly eight operations retain 14 states, and all eight select the **same exact 14 raw physical machines**:

```
canonical
F2+I1
B1+H1
B1+F2+H1+I1
B1+E1+H2
B1+E1+F2+H2+I1
B2+H2
B2+F2+H2+I1
```

Only **canonical** admits the reversible three-route shell.

This is a useful distinction between physical-family reconstruction and transition reconstruction: seven alternative local rules recover the same 14 physical masters and terminal `100`, yet all seven distort the intermediate computation enough to lose the independently derived route structure.

## All route-capable operations

Out of 19,683 operations, only six admit any three-class shell of three distinct ternary permutations:

```
canonical                  14 states   120 / 012 / 102
C1                          7 states   120 / 012 / 102
C2                          7 states   120 / 012 / 102
A1+B2+G2+H2                12 states   102 / 012 / 120
A1+B2+C1+G2+H2              6 states   102 / 012 / 120
A1+B2+C2+G2+H2              6 states   102 / 012 / 120
```

Therefore:

> canonical is the unique maximum-retention route-capable operation in the entire 3^9 local-offset family.

This is stronger than the one- and two-cell results. It is not merely that canonical wins near its immediate neighborhood. Every independent cyclic depth rewrite at every physical cell has now been exhausted.

## The best alternate route machine

The strongest noncanonical route-capable sibling is:

```
A1+B2+G2+H2
12 states
route shell 102 / 012 / 120
terminal 100
```

It is genuinely a different physical family:

- only 2 of its 12 states are canonical states;
- 10 are new raw-compatible states;
- 12 canonical states are excluded.

So this is a real alternative machine, not a gauge copy. It has the same carrier, same Q4 selector field, same two-pass budget, a reversible three-route layer, and the same terminal, but it retains fewer raw-compatible states.

The already declared maximum-retention criterion therefore has concrete discriminatory force here: 14 beats 12 without requiring the expected endpoint or expected route orientation.

## Consequence for the broader-alternative queue

This closes one natural hostile family completely.

Within **all cell-local cyclic rewrites of first-pass selector depth**:

- terminal `100` is extremely non-discriminating because the canonical second pass already makes it available to 96 raw candidates;
- raw-state retention alone is also insufficient because route-degenerate machines reach 24 states;
- exact physical-master recovery alone is insufficient because seven noncanonical rules recover the same 14 masters;
- reversible-route structure alone is insufficient because a genuine 12-state sibling survives;
- **route structure plus maximum raw-state retention uniquely selects canonical**.

That combination is not a post-hoc endpoint target. Both ingredients were independently motivated earlier: route reversibility/distinction in Experiment 278 and maximum raw-state retention in Experiment 253.

The family is now exhausted rather than sampled. Further cell-local first-pass offset work would add no information unless a new physical constraint changes the model class.

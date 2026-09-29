# Experiment 306 — Single-cell recursion-defect audit

> **Canonical numbering note:** this research lane was originally merged from isolated PR #34 using provisional experiment numbers 296–302. Those IDs later collided with canonical Q4/Discord work. The reconciliation pass of 2026-09-29 preserves the experiments unchanged and renumbers the lane 306–312.


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


# Experiment 307 — Up-to-two-cell first-pass defect audit

Experiment 306 found that one local first-pass exception could retain 16 raw-compatible states and terminal `100`, but only by expanding the functional quotient and breaking reversible routing. Experiment 307 asks whether **two** local exceptions can repair that weakness.

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

It also reinforces the stopping signal from Experiment 306. Expanding to arbitrary cell-local exceptions rapidly creates representational siblings, while the structurally meaningful discriminator remains the same reversible route shell already derived independently.


# Experiment 308 — Full 3^9 first-pass local-offset closure

Experiments 306–307 suggested that local exception freedom grows rapidly, but the family is still small enough to close exactly.

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


# Experiment 309 — Full second-pass local address closure

Experiment 308 closed all cell-local cyclic depth rewrites on the first pass. Experiment 309 turns the telescope around and asks how identifiable the **terminal pass** is if it is allowed its own local address rule.

At each A–I cell independently choose both coordinates:

```
q' = S(j) + q_offset[j] mod 3
d' = S(j) + d_offset[j] mod 3
```

Each cell therefore has 9 local choices. The complete family contains:

```
9^9 = 387,420,489
```

second-pass operations.

The first pass remains canonical, leaving the established 20 raw-compatible first-pass survivors.

## Exact factorization

A literal 387-million-operation loop is unnecessary because terminal POS3 validity factorizes by physical column.

Each three-cell column has only `9^3 = 729` local address-choice triples. When those are collapsed by their exact 20-candidate output signature, the three columns contain only:

```
10
270
4
```

distinct signatures.

Thus every physical operation is counted exactly by only:

```
10 × 270 × 4 = 10,800
```

signature combinations, with multiplicities carried through.

This is an exact quotient, not sampling.

## Result

The unconstrained second pass is dramatically less identifiable than the first.

- 35,640 operations retain **all 20** first-pass states.
- Every 20-state operation has three terminal payloads and is not a maximum route-compatible model.
- 17,359,920 operations retain some three-class reversible route structure.
- The maximum route-capable state count is 14.
- Exactly 249,480 operations attain that 14-state route maximum.
- Every one of those 249,480 operations selects the **same canonical 14 physical states**.
- Conversely, every operation selecting exactly the canonical 14 is route-capable because the first-pass computation is unchanged.

So maximum route-compatible retention still identifies the physical state family, but it does **not** identify the terminal address rule.

## How underdetermined is the terminal?

Within those exact-canonical 249,480 operations:

- 27 distinct terminal profiles occur;
- 178,200 operations produce one invariant terminal across all 14 states;
- only 4,320 produce invariant terminal `100`.

So even the combination:

```
exact canonical 14 physical states
+ canonical first-pass route shell
+ invariant terminal 100
```

still admits **4,320 distinct cell-local second-pass address rules** if pass two is allowed its own arbitrary local coordinate rewrites.

That is a useful negative result. The terminal is not independently reconstructible under such a permissive grammar.

## Interpretation

This does not weaken the recursive model. It clarifies which part of the model carries explanatory force.

A pass-specific rule with 18 independently choosable ternary offsets is an enormous exception budget. Once that budget is admitted, the same observed terminal can be manufactured thousands of ways.

The important mechanical claim is therefore not merely:

> there exists a second address read producing 100.

It is:

> the **same simple selector-address operation is reused** recursively.

Experiment 309 deliberately removes that uniform-reuse constraint and shows exactly what happens: identification evaporates.

That makes pass-to-pass rule reuse a substantive structural premise rather than cosmetic elegance.


# Experiment 310 — Same local operator reused on both passes

Experiment 309's huge ambiguity suggests the obvious hostile control: keep cell-local freedom, but require it to describe an actual recursive operation rather than a special terminal decoder.

At each cell choose one depth offset:

```
F_j(q,S) = (q, S + offset[j]) mod 3
```

and use the **same** `F_j` on both passes:

```
first:  F_j(q,S)
second: F_j(S,S)
```

The complete family is again `3^9 = 19,683` operations.

## Result

Only 18 of the 19,683 operations preserve any three-class reversible route shell.

Their retained-state counts are:

```
4  states : 2 operations
5  states : 4
6  states : 4
7  states : 2
8  states : 1
10 states : 2
12 states : 2
14 states : 1
```

The unique 14-state route-capable operation is:

```
canonical
```

The two best route-capable siblings retain only 12 states:

```
B2+G2+H2
A2+B2+G2+H2
```

Both split their terminals evenly between `122` and `102`.

## Bigger machines exist, but lose the route layer

The global maximum within the same-operation family is 22 states, reached by:

```
D2
B1+D2+H1
B2+D2+H2
```

All three are route-degenerate.

Thus every operation retaining more raw-compatible states than canonical pays for it by losing the reversible three-class computation.

## Exact-master siblings

Two noncanonical same-operation rules recover exactly the same 14 physical candidates:

```
B1+H1
B2+H2
```

Both terminate invariantly at `102`, and both destroy the route shell.

So even within a genuinely reused operation grammar, exact physical-state reconstruction alone is still weaker than reconstructing the transition structure.

## Combined lesson from 298–300

These three experiments separate three questions that had previously been easy to blur:

1. **Can a local rule reproduce the physical state family?**
2. **Can it preserve the reversible intermediate computation?**
3. **Is it genuinely one operation reused recursively rather than a pass-specific decoder?**

The answers are now sharply different.

- Arbitrary first-pass local rewrites: several physical siblings and larger state families exist, but canonical uniquely maximizes retention among route-capable rules.
- Arbitrary second-pass local rewrites: thousands of terminal rules reproduce the canonical family and endpoint because pass-specific exception freedom is enormous.
- Same local operation reused on both passes: canonical becomes the **unique maximum-retention route-capable rule** across the full 19,683-member family.

This gives Priority 5 a stronger stopping condition for local-coordinate alternatives.

The meaningful model class is not “anything cell-local that happens to terminate.” It is a compact operation that survives raw-state pressure, preserves the independently derived reversible route layer, and is reused across recursion.

Within the complete cyclic local-depth family, that combination now selects canonical uniquely.


# Experiment 311 — Arbitrary local selector permutations

Experiment 310 still restricted every local selector rewrite to a cyclic shift. Experiment 311 broadens each A–I cell to an arbitrary permutation of `{0,1,2}`, while preserving the crucial same-operation-reuse rule:

```
g_j ∈ S3
F_j(q,S) = (q,g_j(S))
```

The same `F_j` is used on both passes.

The physical family has:

```
6^9 = 10,077,696
```

local operations.

Column-signature factorization reduces the exact enumeration to:

```
24 × 216 × 17 = 88,128
```

signature combinations, with exact multiplicities.

## Result

Only 5,760 of the 10,077,696 operations retain any three-class reversible route structure.

Their state-count distribution is:

```
4  : 640
5  : 1408
6  : 1280
7  : 512
8  : 320
10 : 704
12 : 640
14 : 256
```

The global maximum is 22 states, reached by 384 operations, but those are route-degenerate.

At the route maximum there are 256 physical operations, divided into exactly four observational classes of 64 operations each.

The simplest representatives are:

```
canonical
A:102
D:210
A:102 + D:210
```

where a three-digit mapping means `g(0)g(1)g(2)`.

The four classes are:

| representative | overlap with canonical | terminal | first-pass / route |
|---|---:|---|---|
| canonical | 14/14 | 100×14 | canonical |
| A:102 | 10/14 | 100×14 | canonical |
| D:210 | 10/14 | 100×10, 110×4 | altered |
| A:102+D:210 | 6/14 | 100×10, 110×4 | altered |

The A-only transposition is therefore a much stronger near-rival than anything in the cyclic-offset family. It keeps:

- 14 states;
- invariant terminal `100`;
- the same three first-pass functional families;
- the same unique route shell `120 / 012 / 102`.

It changes four raw-compatible physical states.

So strict uniqueness does **not** survive the move from local cyclic shifts to arbitrary local S3 relabelings.

That does not mean the rival is equally explanatory. Canonical remains the unique globally uniform / zero-exception operation. But the A sibling is close enough that it needs to be explained rather than dismissed by description length alone.


# Experiment 312 — Gauge decomposition of the A-swap fork

The A:102 rival looks serious at the functional level. Its physical difference turns out to be extremely localized.

## The four replaced states

The two 14-state families share 10 states.

For each of the four replacements:

- the primary payload is identical;
- every Q4 selector value except A is identical;
- canonical has physical `A=1`;
- the sibling has physical `A=0`;
- first-pass outputs are identical;
- terminal remains `100`.

The complete H108 masters differ only at:

```
residue 82
residue 91
```

Those are the depth-0 and depth-1 cells of the Q4 A stack.

Neither residue is present in the classified public corpus.

The depth-2 A residue 100 remains dot in both representations, so it does not differ.

## Why the operation compensates

Canonical uses physical `A=1` and identity mapping, giving effective selected depth 1.

The sibling uses physical `A=0` but local mapping:

```
A:102
```

which maps `0 -> 1`.

So the first-pass primary read at A is restored exactly.

On the second pass, the only residual source-address difference is:

```
canonical: (q,d) = (1,1)
sibling:   (q,d) = (0,1)
```

At physical A, those two source symbols are identical for **all six raw-compatible primary payloads**.

That is the same local equality underlying the already-established `f1` recursion gauge.

Thus the sibling combines:

1. an unobserved physical Q4-A selector relabel;
2. an inverse local operation relabel restoring the effective depth;
3. an already-known terminal q-address equality.

It is a coupled latent-label / operation gauge.

## Why every route-max class has multiplicity 64

The invariant-100 canonical class is itself not one literal operation table. It is a `2^6` orbit generated by six independent local involutions:

```
B:102
C:210
E:021
F:210
H:102
I:102
```

Five of these, B/E/F/H/I, merely exchange selector inputs that are never exercised at those fixed-value positions in the canonical 14-state family.

C is the nontrivial sixth bit. `C:210` swaps depths 0 and 2, but at physical C those two primary symbols are exactly equal for every q and all six raw primary payloads.

All 64 combinations therefore produce the exact same canonical survivor/output mapping.

Adding `A:102` to every member creates a second disjoint 64-operation orbit, all producing the exact same A-sibling survivor/output mapping.

Together these two 64-element cosets exhaust the invariant-`100`, 14-state route-max fork found in Experiment 311.

## Consequence

The broader S3 search does uncover a real **representation ambiguity**, but not a second functional machine.

The corpus cannot distinguish whether those four states print A as selector 1 with the identity operation or selector 0 with an A-local transposition, because the only changed printed Q4 cells are unobserved and the residual terminal address difference sits on an exact primary-symbol equality.

So the correct statement is narrower than “canonical is uniquely forced”:

> canonical is the simplest uniform representative of the route-max functional machine; the broader local-permutation grammar contains a coupled A-label gauge that the closed corpus cannot resolve.

That is exactly the kind of adversarial caveat Priority 5 is supposed to surface.

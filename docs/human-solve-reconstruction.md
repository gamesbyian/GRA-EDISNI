# Human solve reconstruction

_Status: Experiment 248. This is a hindsight-controlled reconstruction of the shortest plausible human path to the mechanical endpoint._

The goal is not to prove what Playdead's intended solve path was. The goal is to identify a path a technically capable person could plausibly discover from the physical sticker evidence without importing later algebra before it becomes visible.

## Ground rule

A step may use only facts available at that point. Later results can validate an earlier guess, but they cannot retroactively serve as the reason the guess was made.

Discovery grades:

- **D — directly visible:** readable from serials/marks with little or no model choice.
- **S — strongly suggested:** one low-complexity organization explains a conspicuous pattern.
- **H — hypothesis test:** requires proposing an operation and checking it.
- **C — confirmation only:** useful after the mechanism is found, but not a plausible discovery prerequisite.

## Short path

### 1. Notice the serial/image cadence — D

The sticker serial advances through image classes A–I with period 9.

That immediately suggests separating:

- a slowly changing foreground mark;
- a nine-state image-class carrier.

Do not begin with plaintext. The serial number is behaving like an address.

### 2. Fold foreground marks modulo 108 — S

The foreground has a 108-state repeat structure while the image class repeats every 9.

Factor:

```
108 = 4 × 3 × 9
```

and write:

```
r - 1 = 27q + 9d + j
```

with:

- `q in 0..3`;
- `d in 0..2`;
- `j in 0..8`.

At this stage `q` and `d` are labels for nested serial blocks, not yet semantic “quarter” and “depth” concepts.

### 3. Use the physical A–I 3×3 layout — D/S

The image classes occupy:

```
I A B
C D E
F G H
```

so each nine-residue serial block can be viewed as a physical 3×3 frame.

The 108-fold now becomes twelve 3×3 frames: four groups of three.

### 4. Split the 9+3 foreground alphabets — D

Residues 1–81 use slash/dash. Residues 82–108 use slash/dot.

That split lands exactly on:

```
9 primary frames + 3 selector frames
```

This is a much stronger clue than any letter-like resemblance in arbitrary reshapes.

### 5. Read primary columns as ternary positional code — S

In the slash/dash region, each physical column behaves as a 3-position code: one row is exceptional, so its row index is a ternary digit.

Call that primitive `POS3`.

Do not assume the final 3×3 ternary lattice yet. Decode local columns first.

### 6. Recover the frame-polarity staircase from the stickers — D/S

Experiment 246 shows what a human actually has available here.

If each frame is allowed to choose independently whether dash or slash is the minority symbol, the classified corpus itself fixes 8 of the 9 frame polarities.

They are:

```
dash  slash slash
dash  dash  ?
dash  dash  dash
```

in `q` rows and `d` columns.

The single missing entry is `q=1,d=2`.

A human has two legitimate routes from here. The quick visual hypothesis is the lower-triangular rule:

```
minority is dash iff d <= q
```

Experiment 247 shows that `q-d>=0` is the unique minimum-coefficient linear-threshold completion, and Experiment 261 shows slash-minority is locally more determined.

More importantly, Experiment 277 means the solver does not need to *assume* either heuristic. Carry both locally valid polarities forward into the selector test. The slash-minority branch produces 20 valid first-pass machines and the canonical 14-state closure. The dash-minority branch has 12 raw primary payloads × 36 selectors = 432 candidate machines, and every one fails first-pass POS3. The recursive operation therefore supplies the missing polarity. The staircase can be noticed early as a good guess, then becomes a theorem once the selector is tried.

### 7. Let the raw corpus reveal almost the entire ternary primary — D

Once POS3 and the polarity staircase are in place, the observations force 25 of the 27 primary ternary digits.

Only two remain unresolved:

```
(q0,d2,c1) = x in {1,2}
(q2,d0,c1) = y in {0,1,2}
```

The resulting lattice is:

```
112   212   0x0
212   002   100
1y2   022   100
```

This is an important correction to the intuitive story of the solve: the compact lattice is not mainly a clever fitted abstraction. Nearly all of it is directly reconstructible from the public classified stickers once the local ternary grammar is recognized.

The old “outer no-self” rule need not be discovered separately. All 18 outer digits are already observation-forced and automatically satisfy it.

### 8. Read Q4 as the same positional primitive in the other alphabet — S

The 27 slash/dot residues naturally form three depth layers over the same 3×3 A–I positions.

At each physical A–I cell, one of the three depths contains the slash.

So Q4 uses the same abstract primitive as the primary:

> ternary value = position of the exceptional member in a three-cell rail.

The difference is only the symbol alphabet and the axis along which the three positions are stacked.

This is the first major “recognition” moment: primary and Q4 are two instances of one positional code.

### 9. Treat Q4 as a selector, not a message — H

Use each Q4 ternary value `S(j)` as an address into the three primary depths at the same physical position `j`:

```
(q,d,j) -> (q,S(j),j)
```

This operation is physically natural because Q4 is literally a depth-indexed three-way choice.

Experiment 245 shows the choice is not fragile hindsight. In the broader shell-preserving family `B(f(q),g(S),j)`, valid POS3 output plus p-factorization forces `g` to identity. The only remaining permutation freedom is relabeling the three external q outputs; fixing their physical labels leaves the canonical substitution uniquely.

### 10. Observe the collapse to three functional states — D after H

The selected surfaces become:

```
p=0: 102 / 002 / 120
p=1: 102 / 012 / 100
p=2: 102 / 022 / 100
```

The original physical uncertainty has collapsed to three operational classes.

At this point `p` is not an arbitrary hidden label. It is the selector's own functional class.

### 11. Recognize the route shell — S/H

The selector baseline `210` reindexes:

```
q = 2 - p
```

and the completed Q3 route family is:

```
q=0 -> 102
q=1 -> 012
q=2 -> 120
```

A human-friendly way to test the completion no longer needs the arbiter interpretation. There are only 27 ways to pick one q-indexed output from each of the three first-pass classes. Ask for a proper route shell: each chosen ternary word should be a reversible permutation, and the three functional classes should not all route the same way. Exactly one choice survives, selecting `120 / 012 / 102` at q choices `2 / 1 / 0`.

Only afterwards need the solver notice that this is the compact relation `q=2-p`, with one 3-cycle, identity, and transposition. The request/grant or arbiter interpretation is explanatory confirmation rather than a prerequisite.

### 12. Reuse the selector once more — H

The first pass produced three q-indexed selected surfaces. Use the same selector to choose q as well as depth:

```
(q,S(j),j) -> (S(j),S(j),j)
```

or:

```
U(j) = B(S(j),S(j),j)
```

Every legal physical completion collapses to:

```
frame 9
100
---//////
```

There is also a simple sanity check on whether this deserves to be called a terminal: apply the selector operation again. Experiment 279 shows `100` is unchanged. The equally large nonlinear `102` sibling found in Experiment 268 is not stable at all; every state moves from `102` to `100` on the next application. So a solver can recognize `100` as the fixed point of the recursive process rather than stopping merely because two passes happened to produce a uniform word.

Experiment 244 broadens this step over all 729 pairs of ternary coordinate maps `B(f(S),g(S),j)`. Twenty-five arbitrary map pairs can manufacture some invariant POS3 terminal, but exactly one shell-preserving permutation pair survives: identity/identity, and its terminal is `100`.

That makes selector reuse a plausible discovered operation rather than a post-hoc way to force the known endpoint.

## What a human does not need

None of these are required for the short mechanical solve:

- `S3` / `T3` transformation-monoid analysis;
- minimum generating sets;
- observer-bus minimization;
- Boolean `XYZG` compression;
- Horn-clause normal form;
- latent-register coding theory;
- generic MDL searches;
- arbiter terminology;
- semantic guesses such as XML/MIX/MISS;
- complemented-binary `?`.

Those are useful explanations, cross-checks, or closures after the machine is found.

## Likely worksheet order

A practical paper-and-pencil reconstruction would use five sheets/tables:

1. **serial ledger:** serial, residue mod 108, image class A–I, mark;
2. **12-frame sheet:** the twelve physical 3×3 frames;
3. **primary ternary sheet:** minority position per column, with the 3×3 frame-polarity staircase beside it;
4. **Q4 selector sheet:** one selected depth per physical A–I cell;
5. **recursive output sheet:** first-pass three surfaces, then selector reuse to the terminal.

This path is short enough to be human-plausible and keeps every large conceptual jump attached to something visually available in the object.

## Remaining human-path uncertainty

The weakest human-discovery step is still the first recognition of POS3 itself. Once POS3 is noticed, Experiment 246 shows that the primary reconstruction becomes unusually constrained.

Experiment 259 now gives an exact answer to the narrower verification version of that question: once H108/POS3 is being tested, a unique set of 34 distinct primary residues preserves all eight raw-forced frame polarities and all 25 raw-forced trits. See `docs/minimum-primary-witness.md`.

Experiment 261 also improves the last ambiguous primary frame. At `q=1,d=2`, the current slash-minority polarity yields one exact POS3 payload completion, while the alternate dash-minority polarity leaves two. A human can therefore prefer the current completion by local determinacy even before noticing the global `d<=q` threshold rule.

Experiment 262 answers the first version of that question positively inside the candidate grammar. In `docs/raw-first-primary-witness.md`, the 34 residues are shown only as nine consecutive sparse 3×3 physical frames. Eight frames eliminate one polarity outright under exact POS3; the ninth resolves by local completion count 1 versus 8. A solver can therefore recover the entire polarity sequence before seeing the `q,d` lattice or the global staircase.

Experiments 263–265 now push one step earlier, into discovery of the rail orientation itself.

Among the four natural parallel-line partitions of a 3×3 frame, only physical columns fit exact POS3 across all nine full-corpus primary frames. Broadening to every one of the 280 possible 3+3+3 cell partitions leaves four combinatorial survivors, but physical columns are the only one made of three straight parallel rails.

More importantly, the 34-residue witness can be used as a genuine discovery set rather than merely a retrospective illustration. It nominates five partitions that both fit all nine sparse frames and maximize polarity determinacy. The other 20 observed primary residues then act as holdout evidence: four candidates fail, while physical columns alone generalize to all nine full frames.

That gives a plausible human sequence:

1. fold to consecutive 9-residue physical frames;
2. test simple three-cell rail organizations;
3. notice that columns are exceptionally constraining;
4. use more stickers as validation rather than as part of the original guess;
5. recover frame polarity locally;
6. only then write the ternary digits and notice the global staircase.

The remaining earlier discovery question is now the H108/A–I framing itself, not POS3 orientation.

Experiment 274 adds a second, genuinely raw-facing cue before full POS3 commitment. Normalize the observed slash/dash marks only to minority/majority using the frame polarities, then compare the nine sparse physical frames pairwise. Exactly two frame pairs have the strongest conflict-free support available in the corpus: four positions observed in both frames, no normalized conflicts, and eight of nine physical positions covered across the pair. They are `q0,d1=q1,d0` and `q1,d2=q2,d2`. Those are precisely two repeated motifs in the canonical primary tensor. In the weaker frame-weight-three + centroid parent, extending both partial repeats to exact frame equality removes the only 14-state centre-column sibling and leaves the canonical 14 states. A human route can therefore treat repeated sparse motifs as a recognition cue rather than needing to invent one-pulse-per-column from nothing. The inferential jump is still real: partial compatibility does not logically prove full equality.

Experiment 275 gives a useful confirmation check that does not require spotting those repeats. In the weak centroid parent, both the distributed and centre-pileup interpretations initially permit all six combinations of the two visibly free primary coordinates `x` and `y`. Running the recursive selection preserves that complete `2×3` primary domain only for the distributed-column interpretation. The pileup interpretation unexpectedly bans one otherwise raw-legal primary combination and compensates with extra selector multiplicity elsewhere. For a human solver, that is a strong warning that the pileup reading is coupling independent-looking parts of the object for no visible reason.

Experiment 276 makes the warning visible at the next worksheet step. If the centre-pileup reading is carried through the selector operation, every surviving physical state produces the same first-pass output. The three-way functional collapse that makes the recursive mechanism legible simply disappears. The distributed-column reading, by contrast, produces three clean first-pass classes. So a solver need not prefer POS3 because it is visually prettier: it is the interpretation that preserves an actual three-way computation.


## Reconciliation with the earlier physical-entry work

Experiments 184–190 already answer the remaining pre-POS3 framing questions strongly enough that this lane should not be reopened as if it were missing.

The physical route is:

1. serial numbers and A–I artwork are coupled exactly by the period-9 cadence;
2. H108 folds the foreground into twelve consecutive A–I rows;
3. the alphabet changes exactly at the 81/27 boundary, giving nine slash/dash rows plus three slash/dot rows;
4. the serial hierarchy therefore supplies the native 4×3×3×3 address directly;
5. later local registration/recursion distinguishes the two inner ternary axes as quarter then depth rather than an arbitrary transpose;
6. in Q4, the three repeated A–I rows already form nine raw serial stacks separated by 9, so the depth-selector idea can be noticed before the A–I values are placed into final physical image-space.

Combined with Experiments 259–265, the human path is now unusually well staged from raw object to POS3 orientation without requiring tensor notation or hindsight from the terminal. The remaining genuinely weak human step is no longer address discovery or rail orientation; it is whether the author expected solvers to promote the locally visible one-of-three patterns into recursive address substitution.

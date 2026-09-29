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

The simplest completion is visibly the lower-triangular rule:

```
minority is dash iff d <= q
```

Experiment 247 makes that statement precise: among small integer linear-threshold rules fitting the eight observed cells, `q-d>=0` is the unique minimum-coefficient completion.

This is a plausible human inference, not a need for group theory or global optimization.

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

A human-friendly way to see the completion is:

- the middle/no-request case is identity `012`;
- the high case is the unique 3-cycle with no fixed point, `120`;
- the remaining case is `102`.

The request/grant or arbiter interpretation is explanatory confirmation. It is not required to perform the mechanical solve.

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

The remaining discovery question is narrower and cleaner:

> Can a solver notice the exceptional-position / frame-balance structure from a raw-first rendering of the 34-residue witness, before seeing solved ternary digits or the compact lattice?

The next worksheet should therefore show the nine sparse physical 3×3 frames first, then progressively reveal frame polarity, minority positions, and only finally the ternary lattice.

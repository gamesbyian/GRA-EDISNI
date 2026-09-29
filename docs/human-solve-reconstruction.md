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

### 2. Fold foreground marks modulo 108 — D/S

The foreground has a 108-state repeat structure while the image class repeats every 9. Experiment 297 and the full Discord export add useful historical control here. The period-9 A–I image carrier was explicit by February 2020; the earliest explicit community statement found that the foreground repeat has minimum length 108 is 25 March 2021; on 11 December 2021 the community published a formal candidate-period argument and a 108-symbol rendering with row length 12. The supplied community master exactly round-trips the same 82-record corpus, so this is not new data, but it shows the fold was genuinely discoverable without hindsight from the later routing interpretation.

The archive also improves the *historical motivation* for treating geometry and boundaries as meaningful. On 26 January 2022, while discussing the 108 foreground rendering, a solver explicitly compared its conspicuous empty/boundary structure to the side pixels of the older Xbox printer puzzle and suggested that such marks could indicate the intended message format/resolution. On 24 December 2022 another solver summarized the older picture-puzzle pattern as: dots carried important information while dashes/slashes helped arrange the image correctly. These are community hypotheses rather than proofs of the present machine, but they show that a solver at the time already had a Playdead-specific reason to inspect registration structure instead of treating the 108 symbols as a flat cipher string.

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

### 3. Use the physical A–I 3×3 layout — D

The image classes occupy:

```
I A B
C D E
F G H
```

so each nine-residue serial block can be viewed as a physical 3×3 frame.

Experiment 297 verifies the registration directly across all 82 records: serial modulo 9 maps `1..8,0 -> A..H,I` with zero mismatches. Serial 0 therefore lands on `I`, the top-left physical cell. The linked historical FAQ explicitly cites this background puzzle as the reason the 108 foreground master should also start at sticker 0. Phase zero is therefore an externally motivated physical registration, not a rotation chosen after seeing the machine.

The 108-fold now becomes twelve 3×3 frames: four groups of three.

### 4. Split the 9+3 foreground alphabets — D

Residues 1–81 use slash/dash. Residues 82–108 use slash/dot.

That split lands exactly on:

```
9 primary frames + 3 selector frames
```

This is a much stronger clue than any letter-like resemblance in arbitrary reshapes.

The Discord chronology makes this especially strong as a human-discovery step. On **26 January 2022**, while the foreground was still unsolved, a solver explicitly proposed that the first **81** slash/dash cells might be one object and the following **27** slash/dot cells a separate checksum-like region, motivated by the powers-of-three geometry and the nine sticker backgrounds. The checksum interpretation did not survive, but the 81+27 boundary itself was seen directly. On **29 October 2023**, solvers again singled out “why are yellows only at the bottom?” as the likely big clue and compared that asymmetry to the visual aids used by the PC/Xbox printer puzzles. This is anti-hindsight evidence for noticing the alphabet boundary, not independent evidence for the later selector semantics.

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

In the preferred all-slash representative, each physical A–I cell has one slash among two dots. More generally, the local ternary fact is only that a nonuniform three-cell stack has one exceptional member; its depth supplies the value whether the exceptional symbol is slash or dot.

So Q4 uses the same abstract primitive as the primary:

> ternary value = position of the exceptional member in a three-cell rail.

The difference is only the symbol alphabet and the axis along which the three positions are stacked.

This is the first major “recognition” moment: primary and Q4 are two instances of one positional code.

There is also a whole-object checksum-like cue for the physical polarity. With exact primary POS3, the primary contributes 45 slashes and 36 dashes. If every Q4 stack uses slash as its exceptional member, Q4 contributes 9 slashes and 18 dots, giving the complete master the unusually clean ratio `54:36:18 = 3:2:1`. Experiment 281 shows any dot-exception stack breaks that ratio. This is not a logical proof from the sparse corpus, but it is a conspicuous physical regularity pointing to the same all-slash interpretation.

Experiment 292 removes the need to make that shared-polarity choice in order to obtain the functional machine. Let every Q4 stack choose slash- or dot-exception independently. Raw observations permit 256 polarity words; recursive closure leaves 16; maximum 14-state retention leaves 8; and the independently derived three-distinct-reversible-route test leaves only `0`, `A`, `C`, and `A+C`. Those four share the same `120/012/102` route shell, and Experiment 289 already shows A/C are completely unobserved physical gauges with unchanged selector depths. A human can therefore try the visually simple all-slash reading early without silently making the eventual route computation depend on it.

Experiment 294 is stronger as a hindsight-resistant validation than as a literal next human pencil step. Once the solver has the modest hypothesis “Q4 is one ternary selector value at each A–I position,” throw away the observed Q4 values and enumerate every one of the `3^9` abstract selector fields. Also refuse to assume that the visible A/D/G centre lane is the control core: test all 84 possible three-position cores. Recursive POS3 closure leaves many alternatives and four different terminal words, but the later reversible-route criterion leaves only the real A/D/G core, the real fixed scaffold modulo C, cores `110/220/212`, seven compatible primary/core states, route shell `120/012/102`, and terminal `100`. The practical human lesson is not “enumerate 19,683 maps by hand.” It is that the selector interpretation earns unusually strong downstream confirmation without relying on its own sparse Q4 cell values or on knowing the answer in advance.

Experiment 295 turns that hindsight validation back into a paper-and-pencil cue. Once the abstract selector scaffold has been inferred, lay out the known Q4 marks by **selector value S** versus **physical depth d**, rather than by letter. The fixed scaffold already shows slash at `(S,d)=(0,0),(1,1),(2,2)`, plus several off-diagonal dots, leaving three codebook cells unknown. The recovered A/D/G core family then lets the observed D-depth-0 dot be used without guessing a hidden state: because D can carry S=1 or2, that mark forces `E[1,0]=dot` as well. Seven of nine shared-codebook entries are now fixed; only `E[0,2]` and `E[1,2]` remain. If the three ternary values are expected to use equally weighted physical codewords, those two blanks must both be dots. The same completion follows from the equally natural requirement that shifting both selector value and depth together should not change the symbol. Either way the codebook becomes `/..`, `./.`, `../`. That gives a human a concrete reason to recognize “one slash marks the selected depth” after the functional selector hypothesis has started to pay rent, rather than requiring the one-slash rule as the initial leap.

### 9. Treat Q4 as a selector, not a message — H

There is now a particularly small way to discover the operation rather than guess it. With primary coordinates `(q,d)` and a visible ternary selector `S`, try the four literal coordinate copies `(q,q)`, `(q,S)`, `(S,q)`, `(S,S)`. Experiment 290 shows three fail immediately as useful selector operations: `(q,q)` ignores Q4, `(S,q)` produces no valid raw machine, and `(S,S)` erases external-quarter structure. `(q,S)` alone remains selector-sensitive and nondegenerate.

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

Experiment 291 makes this second use testable rather than ceremonial. From the 20 first-pass candidates, simply reading q=0, q=1, or q=2 keeps all 20 and leaves three different words. Using q=S is the only equally simple choice that actually filters the family: it leaves 14 and every survivor yields the same word `100`.

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

Experiment 284 adds a useful warning: applying the selector yet again sends those `102` alternatives back to `102`, and they continue alternating forever. So the natural stopping test is genuinely “the surface no longer changes,” not “keep iterating until everything happens to equal 100.”

Experiment 285 also explains why two stable address rules still survive that test. Their only difference is whether q0 and q1 are swapped when the selector says 1. But selector value 1 can occur only at A, D, and F, and those cells contain the same symbol in q0,d1 and q1,d1. The swap is therefore literally invisible on the object. A human should choose the identity rule because it is the simpler address operation, not because the stickers contain evidence distinguishing the two.

Experiment 286 originally tried to treat all of those freedoms as independent gauges. Experiment 287 shows that was too neat. The primary H↔F completion bit and the Q4 F+I polarity branch interfere: using both destroys recursive closure. The genuinely exact-transducer gauge is smaller and cleaner: two primary bits, Q4 A/C polarity bits, and the invisible `f_1` address bit. The F+I branch is a coupled alternative that keeps the 14→3→1 shape and terminal `100` but changes the intermediate first-pass words. Experiment 288 gives a simple reason not to treat it as equivalent notation: when the solver reaches the route-shell step, two of its three functional classes can only supply the same reversible word `102`, so the three distinct reversible routes cannot be built. No renaming of ternary digits repairs that. A human reconstruction should therefore use local POS3 / all-slash representative / identity as the clean working convention, while treating F+I as a nearby route-degenerate alternative rather than part of the exact gauge. Experiment 292 confirms that the shared all-slash choice can be postponed until this route test: the functional route survives exactly modulo the invisible A/C polarity gauges.

Experiment 289 clarifies the remaining A/C freedom. Those two Q4 stacks simply have no known sticker cells at all. Switching their slash/dot polarity does not change which depth the selector chooses in any surviving state, so nothing downstream notices. They are genuine missing-surface bits, unlike F+I. A solver can choose all-slash because it is globally homogeneous and preserves the 3:2:1 census, while recognizing that A/C cannot be proved from the present corpus.

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

The earlier H108/A–I framing question is now materially reduced by Experiment 297 plus the full archive: the A–I background phase is historically attested in February 2020, H108 explicitly by March 2021, the 12×9 rendering by December 2021, and sticker-0/top-left foreground phase explicitly by January 2022. The remaining discovery question is the transition from that historically available carrier view to the finer three-cell POS3 rail interpretation.

Experiment 274 adds a second, genuinely raw-facing cue before full POS3 commitment. Normalize the observed slash/dash marks only to minority/majority using the frame polarities, then compare the nine sparse physical frames pairwise. Exactly two frame pairs have the strongest conflict-free support available in the corpus: four positions observed in both frames, no normalized conflicts, and eight of nine physical positions covered across the pair. They are `q0,d1=q1,d0` and `q1,d2=q2,d2`. Those are precisely two repeated motifs in the canonical primary tensor. In the weaker frame-weight-three + centroid parent, extending both partial repeats to exact frame equality removes the only 14-state centre-column sibling and leaves the canonical 14 states. A human route can therefore treat repeated sparse motifs as a recognition cue rather than needing to invent one-pulse-per-column from nothing. The inferential jump is still real: partial compatibility does not logically prove full equality.

Experiment 275 gives a useful confirmation check that does not require spotting those repeats. In the weak centroid parent, both the distributed and centre-pileup interpretations initially permit all six combinations of the two visibly free primary coordinates `x` and `y`. Running the recursive selection preserves that complete `2×3` primary domain only for the distributed-column interpretation. The pileup interpretation unexpectedly bans one otherwise raw-legal primary combination and compensates with extra selector multiplicity elsewhere. For a human solver, that is a strong warning that the pileup reading is coupling independent-looking parts of the object for no visible reason.

Experiment 276 makes the warning visible at the next worksheet step. If the centre-pileup reading is carried through the selector operation, every surviving physical state produces the same first-pass output. The three-way functional collapse that makes the recursive mechanism legible simply disappears. The distributed-column reading, by contrast, produces three clean first-pass classes. So a solver need not prefer POS3 because it is visually prettier: it is the interpretation that preserves an actual three-way computation.

Experiment 280 adds an important humility check. Not every non-POS3 deviation can be rejected by computation. Two tiny deviations live in cells that the selector never addresses: H↔F in q0,d0 and I↔E in q1,d1. They are also entirely unobserved in the public corpus. Toggling either or both leaves the whole 14→3→1 computation unchanged. A human choosing exact one-per-column POS3 is therefore also choosing the simplest uniform physical code and fixing a real two-bit gauge. That is a plausible authoring inference, but it should not be retold as something recursion proved.

Experiment 282 gives the human solver another reason to make that choice. Forget columns for a moment and simply ask how far the three minority marks have to move as neighboring primary frames change. The all-POS3 completion is the unique smoothest member of the four transition-equivalent gauges under minimum Manhattan transport. Each invisible pulse swap independently makes its local neighborhood jumpier. This is still a simplicity judgment, but it is visually native to the 3×3 frame sheet and does not depend on knowing the recursive answer.

Experiment 283 checks that this is not a peculiarity of Manhattan distance. As long as diagonal movement costs even slightly more than one orthogonal step, the same all-POS3 completion remains uniquely smoothest. Only under the extreme rule that a diagonal is exactly as cheap as an orthogonal move does the I↔E gauge bit become invisible to the smoothness score. So the cue is reasonably robust rather than metric-picked.

Experiment 293 supplies a useful boundary rather than a shorter human route. Exact source POS3 can be recovered without imposing one-pulse-per-column directly if a solver instead assumes common frame weight, promotes both strongest sparse-frame repeats to exact equality, and imposes one aggregate column-balance relation in each quarter. Those five regularities are jointly subset-minimal in that tested parent: remove any one and extra non-POS3 states return. That makes the construction a legitimate weaker composite authoring grammar, but not a simpler discovery story. For the human reconstruction, direct recognition of the three physical column rails remains the cleaner hypothesis to test.


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

# Current Research State

_Last compacted from the canonical Google Results through Experiment 240._

## Status

The closed-corpus mechanical crack is substantially complete.

The preferred model is one serial-addressed ternary positional machine with:

- one four-bit constrained hidden state `H=(X,Y,Z,G)`;
- one shared three-position code primitive `POS3`;
- one primary memory generator;
- one Q4 selector generator;
- one recursive address-substitution operation used twice;
- one canonical Q3 route shell;
- one rank-1 terminal `100`;
- one frozen observer bus that recovers the hidden state.

No downstream completion-invariant plaintext, URL, instruction, image, or lore phrase has been established.

The internal semantic branch is closed at the current evidence level. Reopen it only if an external physical/archive/ARG clue independently supplies a consumer for the terminal object.

## Closed-corpus posture

Assume no additional sticker will ever surface.

The current object is symbolically complete:

- 65 observed H108 residues;
- 30 additional residues forced by the machine;
- 13 variable state-register residues;
- 14 legal complete H108 masters;
- 95 invariant H108 residues total.

The remaining uncertainty is which of 14 legal physical states was authored. Generic compression does not select one, and the transition does not need one selected.

## Hidden state: preferred normal form

Use Boolean state:

```
H = (X,Y,Z,G)
```

with one validity clause:

```
Y AND Z -> X
```

Equivalently, the only forbidden functional word is:

```
XYZ = 011
```

Gauge `G` is free, so the two forbidden physical words are `0110` and `0111`.

There are exactly 14 legal physical states.

Decode native variables:

```
x = 1 + X

y = 2                  if Y=1
y = Z                  if Y=0

g = 2G
```

Grant rails:

```
P0 = Y AND NOT Z
P1 = NOT X AND NOT Y
P2 = X AND (NOT Y OR Z)
```

Exactly one `P_i` is 1 for every legal state.

The forbidden word `011` gives `P0=P1=P2=0`: the unrepaired Q4 baseline `210`.

## Carrier/address layer

For H108 residue `r in 1..108`:

```
Q = floor((r-1)/27)
d = floor(((r-1) mod 27)/9)
j = (r-1) mod 9
```

so:

```
r-1 = 27Q + 9d + j
```

The serial background cycle is exactly A–I with period 9.

Physical A-I layout:

```
I A B
C D E
F G H
```

The foreground period is 108.

Residues:

- 1–81: slash/dash primary memory;
- 82–108: slash/dot Q4 selector memory.

## Shared ternary primitive

Define:

```
POS3(v; exceptional, background)
```

as three physical positions with the exceptional symbol at ternary position `v` and background symbol at the other two positions.

Primary columns and Q4 depth stacks use the same representation family:

> ternary value = position of the exceptional member of a three-cell rail.

This replaces separate “primary one-hot” and “Q4 one-slash” code concepts with one common positional code.

## Primary memory

Normalized ternary payload lattice:

```
112   212   0x0
212   002   100
1y2   022   100
```

Substitute:

```
x = 1+X
y = 2Y + (1-Y)Z
```

Frame polarity:

```
minority symbol is dash iff d <= q
otherwise minority symbol is slash
```

The supplied local registration axiom is:

> the two outer minority rows of a frame at depth `d` do not equal `d`.

Recursion derives the T `100/110/111` polarity staircase. Do not treat the staircase as an independent supplied premise.

### Route/cross normal form

The fixed primary tensor compresses to:

- Q1 left route: `120`;
- Q2 left route: `201 = 120^-1`;
- right route: `220` in every quarter;
- Q3 left route: `101`, the non-self complement of right `220`;
- centre plane: terminal `100` on middle row and main diagonal, `102` on middle column, with state ports `x,y` on anti-diagonal endpoints.

## Q4 selector

Recovered functional selector field in physical layout:

```
2   A   2
g   D   0
1   G   2
```

with:

```
A = 2 - P0
D = 1 + P1
G_control = 2*P2
g = 2G
```

Legal control cores:

```
p=0 -> 110
p=1 -> 220
p=2 -> 212
```

Their unrepaired common baseline is:

```
210
```

Broad inverse searches recover the cores, baseline, seven-state legality relation, scaffold, and terminal from operation. The only physical selector freedom left is the transition-invisible C gauge.

Q4 decomposes into:

- 19 operation-forced scaffold/check cells;
- 8 latent p/g cells.

All 11 currently observed Q4 cells are reproduced by the operationally reconstructed selector family.

## Recursive transition

First pass substitutes selector depth into the inner macro address:

```
(q,d,j) -> (q,S(j),j)
```

producing three registered surfaces `O_q`.

Their normalized payloads depend only on `p`:

```
p=0: 102 / 002 / 120
p=1: 102 / 012 / 100
p=2: 102 / 022 / 100
```

The first recursion erases `x`, fine `y`, and `g`. Hidden-state dependence drops from rank 14 to rank 3.

## Request/grant object

With:

```
X=[x=2]
Y=[y=2]
```

the compatibility relation is:

```
00 -> p=1
01 -> p=0
10 -> p=2
11 -> p in {0,2}
```

In routed-quarter order `q=0,1,2`, eligibility is:

```
E = [X, NOR(X,Y), Y]
```

Standard-object match:

> two-request priority-free MUTEX arbiter plus explicit middle idle/fallback state.

This relation is derived by selector/primary operational compatibility, not stored as a lookup table.

## Routing

Recovered baseline:

```
210
```

routes:

```
q = 2-p
```

Completed Q3 route table:

```
q=0 -> 102
q=1 -> 012
q=2 -> 120
```

Human inverse derivation:

- q=1 is no-request fallback, so route is identity `012`;
- q=2 is the unique loopless/derangement route, forcing `120`;
- uniqueness of the derangement forces q=0 to `102`.

Q3 contains a transposition, identity, and 3-cycle. Q1/Q2 are the two opposite 3-cycles.

## One-hot / thermometer conversion

Q4 stores `p` as one-hot rails `P0,P1,P2`.

Route/terminal layers expose:

```
b = [p!=0] = P1 OR P2
s = [p=2]  = P2
```

so:

```
p=0 -> 00
p=1 -> 10
p=2 -> 11
```

and inverse:

```
P0 = NOT b
P1 = b AND NOT s
P2 = s
```

Prepending the fixed 1 gives:

```
100
110
111
```

which is exactly the T staircase. These are recodings of one ternary state, not independent confirmations.

## Terminal

Second selector reuse substitutes the selector into both macro digits:

```
(q,S(j),j) -> (S(j),S(j),j)
```

or:

```
U(j) = B(S(j),S(j),j)
```

Every legal state yields:

```
frame 9
payload 100
raw A-I word ---//////
```

Transition rank:

```
14 -> 3 -> 1
```

`100` is also the p-order indicator of the unique derangement route class.

The terminal is mechanically generated by selector reuse. The derangement identity is a certificate/description, not a separately demonstrated physical circuit.

## Observer

Frozen same-quarter observer:

```
0 0 X
1 0 0
Y 0 0
```

Frozen Q4-target observer:

```
0 0 (X AND Y AND P0)
1 G P0
NOT([y=1]) 1 NOT(P0)
```

Information-optimal postprocessing:

```
X = S3
Y = S7
G = Q5
Z = NOT Q7 OR (S3 AND S7 AND Q9)
```

Thus the 18 raw query bits reduce exactly to the optimal four-bit state word `X,Y,Z,G`.

Raw-query minima:

- 3 queries recover the 5-state control quotient;
- 4 recover the 7 functional states;
- 5 recover all 14 physical states.

With Boolean postprocessing, 4 bits are information-theoretically optimal for 14 states.

The pointer bus has no unexplained semantic capacity left: it is a redundant state observer.

## Physical latent register

Variable residues:

```
22,25,
55,58,61,
84,88,91,94,100,102,103,106
```

Interpretation:

```
22  = X
25  = NOT X

55  = [y=0]
58  = [y=1]
61  = [y=2]

84  = G
102 = NOT G

100 = P0
91  = NOT P0
94  = P1
103 = NOT P1
88  = P2
106 = NOT P2
```

All 14 legal codewords have Hamming weight 6 and minimum distance 2.

Global symbol census for every complete master:

```
slash : dash : dot = 54 : 36 : 18 = 3 : 2 : 1
```

## Algebraic characterization

Under native map notation `abc = (0->a,1->b,2->c)`:

- `120` and `102` generate `S3`;
- adding terminal `100` generates the full 27-map transformation monoid `T3`;
- `{120,102,100}` is a minimum-size generating set.

This is mathematical closure only.

Experiment 211 closes ordinary map composition as the physical selector mechanism. Physical irreversibility is recursive spatial selection, not generic transformation composition.

## Evidence/axiom status

Preferred irreducible transition-side supplied set:

1. serial/H108/A-I carrier geometry;
2. primary physical column positional code;
3. primary frame-polarity staircase (minority dash iff `d<=q`), with 8/9 entries directly forced by the corpus under POS3;
4. Q4 as depth-indexed POS3 selector encoding;
5. recursive application of selector to primary memory;
6. reuse of the same selector on regenerated surfaces;
7. canonical-shell/permutation preservation when reconstructing Q4 without raw Q4 cell placements.

Increasingly theorem-level rather than separately supplied:

- outer no-self registration;
- T polarity staircase;
- 210 baseline;
- p self-label;
- arbiter table;
- NOR fallback;
- Q3 table;
- route cycle spectrum;
- thermometer code;
- terminal `100`;
- derangement certificate;
- T3 closure.

The frozen pointer observer is a separate preregistered readout module, not part of the transition generator.

## Post-240 uniqueness hardening

Experiments 241–246 sharpen the status of the recursion, implementation, and primary-grammar assumptions without changing the preferred machine.

Experiment 241 makes the dependency structure explicit in `docs/theorem-graph.md`, separating physical observations, supplied local grammars, derived theorems, observer-only facts, algebraic descriptions, and the semantic stopping statement.

Experiments 242–243 provide a second implementation in native `(x,y,p,g)` coordinates. It derives the 14-state family directly from the request/grant relation rather than the Boolean `XYZG` Horn normal form. The two implementations independently reproduce the corpus-facing invariants and emit exactly the same set of 14 complete 108-symbol masters.

Experiment 245 broadens the first recursion to:

```
B(f(q), g(S(j)), j)
```

for all 27 ternary maps `f` and `g` (729 ordered pairs). Requiring valid POS3 outputs and dependence only on selector class `p` leaves 49 broad survivors. Restricting both coordinate maps to permutations leaves exactly six: `g` is forced to identity and `f` is any permutation of the three external q labels. Once the physical q labels are held fixed, identity/identity is the sole survivor.

Experiment 244 broadens the terminal reuse to:

```
B(f(S(j)), g(S(j)), j)
```

over the same 729 ordered map pairs. Twenty-five arbitrary-map pairs yield a completion-invariant valid POS3 terminal, so completion invariance alone is not unique. Under canonical-shell/permutation preservation, however, exactly one pair survives:

```
f = identity
g = identity
terminal = 100
```

Thus the current first and second address substitutions are now unique inside a substantially broader shell-preserving coordinate-map family. This does **not** prove uniqueness over every conceivable recursion grammar; the remaining queue explicitly targets broader non-coordinate-map parents.

Experiment 246 reconstructs the primary payload directly from the classified corpus under POS3 while initially leaving each frame polarity free. Eight of the nine frame polarities are forced by observations. The sole ambiguity is frame `q=1,d=2`, exactly the missing upper-triangle entry in the global `d<=q` staircase. Applying that staircase forces 25 of the 27 primary trits directly from raw observations; the only unresolved positions are the already-known state ports `x=(q0,d2,c1)` and `y=(q2,d0,c1)`.

All 18 outer primary trits are among the 25 observation-forced values and all satisfy minority-row `!= d`. The former “outer no-self registration” therefore adds no independent constraint once POS3 and the frame-polarity staircase are in place. It should be treated as a derived corpus fact rather than a separate supplied axiom.

Experiment 247 tests the sole unobserved polarity entry against bounded integer linear-threshold completions `[a*q+b*d+c>=0]`. Both binary completions are possible in that broader family, but the current staircase is the unique global minimum-L1 primitive rule: `q-d>=0` (cost 2). The alternate completion first appears as `2q-d>=0` (cost 3). This is a bounded simplicity result, not an absolute proof over all polarity grammars.

Experiment 249 removes each of the 54 distinct observed primary residues in turn and reruns the raw reconstruction. Thirty residues affect at least one headline metric, but no single deletion changes more than one forced frame polarity and/or one forced trit: the worst case moves from 8 forced polarities / 25 forced trits to 7 / 24. The primary reconstruction is therefore not dependent on any single public residue.

## Mechanical completion

Experiment 237 provides a single typed transducer specification.

Experiment 238 audits it for hidden lookup tables and finds no large unexplained table or state-selection step within the investigated native low-complexity families.

Experiment 239 independently reimplements the four-bit generator and checks it against the live public ledger:

- 82 classified stickers;
- 65 distinct H108 residues;
- 82/82 serial→A-I matches;
- zero repeated-residue conflicts;
- 82/82 foreground symbols compatible;
- 14 generated physical states;
- exact 95 invariant / 13 variable split.

## Semantic stopping point

Experiment 240 audits established INSIDE ARG consumer families against terminal `100` / `---//////`.

Every established family is:

- already applied and negative;
- dimension/carrier mismatched;
- state-dependent internal readout;
- or requires a new discretionary choice.

The attractive complemented-binary terminal `000111111 = 63 = '?'` is explicitly post-hoc and not promoted.

Current endpoint:

```
frame 9 / normalized 100 / raw ---//////
```

Treat this as the mechanically generated acceptance/canonical state.

A semantic epilogue remains possible only if new independent information specifies how to consume it.

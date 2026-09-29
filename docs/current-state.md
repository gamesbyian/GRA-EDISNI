# Current Research State

_Last compacted from the canonical Google Docs after Experiment 208._

## One-paragraph status

The current closed-corpus model is a registered ternary selector/routing/canonicalization machine over an H108 sticker master. The physical serial supplies a natural 4×3×3×3 address. The first 81 residues form nine slash/dash primary 3×3 frames; the final 27 form a slash/dot Q4 selector. Primary registration normalizes the nine frames to a compact ternary lattice with only two primary variables. Q4 selects depth, first-stage regeneration produces a three-state control `p`, a priority-free two-request relation constrains that state, `210` routes `p` to quarter `q=2-p`, completed Q3 supplies the route family `102/012/120`, and reusing Q4 canonicalizes every legal state to frame 9 / payload `100` / raw `---//////`. No completion-invariant semantic plaintext has been established.

## Physical addressing

For H108 residue `r in 1..108`:

```
Q = floor((r-1)/27)             # quarter 0..3
d = floor(((r-1) mod 27)/9)    # depth/frame row 0..2
j = (r-1) mod 9                 # A-I serial image class
```

The solved A-I image maps `j` into physical 3×3 coordinates.

Observed vocabulary zoning:

- residues 1–81: slash/dash only;
- residues 82–108: slash/dot only.

All 82 classified stickers obey the serial→A-I cadence exactly.

## Primary normalized lattice

Normalized ternary payloads by quarter × depth:

```
112   212   0x0
212   002   100
1y2   022   100
```

with:

```
x in {1,2}
y in {0,1,2}
X = [x=2]
Y = [y=2]
```

Registration: in frame depth `d`, the two outer cells of physical row `d` are majority. Minority-row positions become ternary payload digits.

## Q4

Q4 is exactly one slash per depth stack.

Functional centre-column baseline:

```
210
```

The three legal control cores are:

```
p=0: 110
p=1: 220
p=2: 212
```

with C-stack gauge `g in {0,2}` functionally irrelevant to transition behavior.

Experiment 208 inverse result: inside the 48-member natural single-defect family, requiring both legal first-stage O1 regeneration and legal rank-1 second-stage canonicalization uniquely forces baseline `210` and cores `110/220/212`.

## Request/grant relation

Gauge-quotiented legal states:

```
(x,y,p)
(1,0,1)
(1,1,1)
(1,2,0)
(2,0,2)
(2,1,2)
(2,2,0)
(2,2,2)
```

Boolean quotient:

```
X=0,Y=0 -> p=1
X=0,Y=1 -> p=0
X=1,Y=0 -> p=2
X=1,Y=1 -> p in {0,2}
```

Standard-object match: two-request priority-free MUTEX arbiter plus explicit middle idle/fallback state.

## Routing

`210` gives:

```
q = 2 - p
```

Completed Q3 route table:

```
q=0 -> 102
q=1 -> 012
q=2 -> 120
```

Each row is a permutation of `012` and self-labels in its centre.

Human inverse reconstruction:

- q=1 is fallback, so neutral route is identity `012`;
- q=2 is the unique loopless/derangement route, forcing `120`;
- uniqueness of that derangement forces q=0 to `102`.

Q1 left route is `120`; Q2 left route is `201=120^-1`.

## Terminal

Second selector reuse gives:

```
U(r,c) = B(S(r,c), S(r,c), r, c)
```

so the terminal step samples only diagonal primary frames 1, 5, 9.

Every legal state terminates at:

```
normalized payload: 100
primary frame:      9
raw A-I word:       ---//////
```

`100` is also the p-order indicator of the unique derangement route class.

Causal caveat: the second selector physically generates the terminal. The derangement indicator is an exact certificate/description, not a separately demonstrated physical circuit.

## State hierarchy

Physical state:

```
P = (x,y,p,g)
|P| = 14
```

Gauge quotient:

```
F = (x,y,p)
|F| = 7
```

Control quotient:

```
C = (X,Y,p)
|C| = 5
```

Routed state:

```
R = q
|R| = 3
```

Terminal:

```
|T| = 1
```

Treat `14 -> 7 -> 5 -> 3 -> 1` as an information-compression ladder. In particular, 5→3 forgets request context after grant selection; it is not a pre-grant bisimulation quotient.

## Thirteen-cell latent register

Only 13 of the 43 physically unobserved residues remain variable. The other 30 are forced.

Binary convention:

- primary slash=0, dash=1;
- Q4 slash=0, dot=1.

Exact register:

```
22  = X
25  = NOT X

55  = [y=0]
58  = [y=1]
61  = [y=2] = Y

84  = [g=2]
102 = [g=0]

100 = P0 = [p=0]
91  = NOT P0

94  = P1 = [p=1]
103 = NOT P1

88  = P2 = [p=2]
106 = NOT P2
```

`55/58/61` and `P0/P1/P2` are one-hot.

Every legal 13-bit codeword has Hamming weight 6. There are exactly 14 codewords; minimum Hamming distance is 2. This is state redundancy/observability, not a general error-correcting code.

The whole 108-cell symbol census is completion-invariant:

```
slash : dash : dot = 54 : 36 : 18 = 3 : 2 : 1
```

## Frozen observer

Same-quarter query vector:

```
0 0 X
1 0 0
Y 0 0
```

Q4-target query vector:

```
0 0 (X AND Y AND P0)
1 G P0
NOT([y=1]) 1 NOT(P0)
```

where `G=[g=2]`.

Minimum query sets:

- 3 queries recover five-state control `(X,Y,p)`;
- 4 recover seven functional states `(x,y,p)`;
- 5 recover all 14 physical states `(x,y,p,g)`.

Observer and transition are complementary:

- observer preserves all 14 distinctions;
- transition progressively erases them and ends rank 1.

## Algebraic closure

Native map convention: ternary word `abc` means `0→a,1→b,2→c`.

`120` and `102` generate `S3`.

Adding terminal `100` generates the full 27-element transformation monoid `T3`.

The set `{120,102,100}` is minimum-size for `T3`: two permutation generators plus one singular map.

This is mathematical closure only. Arbitrary physical composition is not demonstrated.

## What is NOT solved

- which of the 14 physical completions is the authored one;
- whether one authored completion even matters beyond the transition quotient;
- any downstream plaintext, URL, place, instruction, or lore phrase;
- whether frame-9 canonicalization is the intended final endpoint or precedes one independently cued semantic operation;
- any physical cycle-index microchannel.

Generic simplicity does not choose a completion.

## Strongest current interpretation

A serial-addressed visual master contains a compact registered three-state control machine. It reconstructs a legal grant, routes it through a complete three-state permutation shell, and canonicalizes all legal states to a unique loopless certificate/state `100`.

That is already a coherent crack. Further work should make the structural description smaller or derive new completion-invariant consequences, not force English out of it.

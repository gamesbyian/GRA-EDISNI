# Experiment 367 — licensed historical operations × completion universes

_Status: completed, 2 Oct 2026._

## Purpose

Experiments 365–366 made U2→U5 explicit candidate populations. The next question is whether historically motivated operations can actually **select among those candidates**.

This experiment deliberately refuses to run every old ARG trick. It obeys Experiment 338's evidence-gate matrix.

Only operations already licensed, frozen, or already tested in a uniquely justified form are replayed. Pending and closed operation families remain untouched.

## Candidate layers

- U2: 648 broad structural masters
- U3: 216 exact-POS3/polarity masters
- U4: 20 first-recursion survivors
- U5: 14 canonical full-machine masters

## Operation 1 — historical 3×3 mosaic

The Dec-2022 operation reconstructed in Experiment 364 is deterministic:

1. read each consecutive nine-sticker sequence row;
2. place it in solved `IAB/CDE/FGH` geometry;
3. tile twelve 3×3 frames.

That transform applies to **every** complete master.

It therefore has:

| layer | applicable | survivors |
| --- | ---: | ---: |
| U2 | 648 | 648 |
| U3 | 216 | 216 |
| U4 | 20 | 20 |
| U5 | 14 | 14 |

This is not a failure. It clarifies the role of the historical mosaic: it supplies a coordinate system, not an independently licensed scoring or filtering criterion.

Experiment 364 already showed that local image-like continuity on this mosaic does not predict withheld stickers. Without another external cue, the mosaic should not be used to rank candidates visually.

## Operation 2 — frozen tail-selected row / one-exception rule

Experiment 329 froze the following exploratory family:

> each A–I tail contains one slash; its position chooses one consecutive 3-cell body row; that selected row contains exactly one exceptional mark.

Apply that exact rule without modification to every completion:

| layer | total | survivors | fraction |
| --- | ---: | ---: | ---: |
| U2 | 648 | **144** | 22.22% |
| U3 | 216 | **48** | 22.22% |
| U4 | 20 | **7** | 35.00% |
| U5 | 14 | **6** | 42.86% |

This is the only currently licensed/frozen operation in this audit that acts as a nontrivial candidate filter.

At U2 and U3 it newly forces the entire C tail:

```
84 = .
93 = .
102 = /
```

At U4/U5, residue 93 is already fixed, so the new information is:

```
84 = .
102 = /
```

Within U5 the six surviving hidden states are exactly:

```
0011
0101
1001
1011
1101
1111
```

This reproduces Experiment 331 from the new universe direction rather than assuming the incumbent first.

### It still does not solve the universe

The row rule reduces U2 from 648 to 144, not to one candidate.

Minimum complete discriminator sizes *within the row-rule survivors* are:

- U2 row survivors: 9 stickers for 144 candidates;
- U3 row survivors: 7 for 48;
- U4 row survivors: 4 for 7;
- U5 row survivors: 4 for 6.

So the operation is genuinely selective, but nowhere near sufficient by itself.

Its evidentiary status remains unchanged: the one-exception criterion was noticed after row/column outputs had been inspected, and Experiment 339 showed the discovery asymmetry is not rare under matched nulls. Its value now is as a **frozen prospective rival**.

## Operation 3 — tail-selected column / one-exception sibling

Experiment 329's direct column/rail interpretation is tested unchanged.

| layer | survivors |
| --- | ---: |
| U2 | **0 / 648** |
| U3 | **0 / 216** |
| U4 | **0 / 20** |
| U5 | **0 / 14** |

This is a hard negative already implied by observed E/F column traces. No completion of the 43 missing cells can rescue it inside these universes.

## Operation 4 — historical lever mapping + known bunker password

The independently motivated cover/lever mapping is:

```
/ -> U
- -> R
. -> L
```

The known normal bunker code is:

```
UURLRRRUUURLLL
```

Experiments 342–343 already establish that the H108 alphabet zones make direct contiguous replay impossible. Experiment 367 confirms this against every explicit master.

The test allows:

- every cyclic H108 start;
- every cyclic rotation of the known 14-command target;
- reversal plus every cyclic rotation.

Result:

| layer | survivors |
| --- | ---: |
| U2 | **0 / 648** |
| U3 | **0 / 216** |
| U4 | **0 / 20** |
| U5 | **0 / 14** |

So completion uncertainty cannot rescue the ordinary bunker-password replay.

The broader lever-consumer hypothesis remains live only if a new clue supplies a different sequence, subset, traversal, or selection operation.

## Operations deliberately not run

### Pending specific evidence

These remain unopened:

- boundary-constrained permutation;
- prior-stage output as selector/key;
- cross-artifact consumer.

Each lacks the parameter or registration rule that would make a test non-arbitrary.

### Closed until cue

These remain untouched:

- exact-value/class filtering;
- Game of Life or other generated transforms;
- text/artwork overlays;
- carrier conversion such as audio/spectrogram.

The existence of 648 explicit masters is **not** permission to sweep these operations.

## Main result

The completion-universe framework cleanly separates three kinds of historical operation:

1. **coordinate/representation operations** that organize every candidate but do not select among them;
2. **bounded structural consumers** that can genuinely reduce the candidate population;
3. **hard negatives** that no unknown-cell completion can rescue.

At present, the frozen row-selector family is the only nontrivial member of category 2.

That gives it a precise role: not “the answer,” but an independently trackable 648→144 rival whose strongest prospective physical predictions remain residues 84 and 102.

The next major narrowing requires one of two things:

- new physical sticker evidence; or
- an independently supplied parameter that opens one of Experiment 338's pending gates.

## Reproducibility

Run:

```bash
python scripts/audit_licensed_operations_universes.py
```

Output:

`data/experiment-367-licensed-operations-universe.json`

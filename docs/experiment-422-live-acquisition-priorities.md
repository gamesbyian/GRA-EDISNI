# Experiment 422 — live acquisition priorities after 427

_Status: active executable ranking, 4 Oct 2026._

Experiment 418 removed the old 534brn-selected E2 pair. The acquisition queue therefore needed to be rebuilt from the **actual live U4 and U5 ensembles** rather than inherited from that dead branch.

This experiment ranks every still-unobserved H108 residue in two separate ways:

1. **U4-vs-U5 discrimination** using total-variation distance between the two symbol distributions;
2. **U5 state resolution** using the entropy of the symbol split inside the 10-state U5 family.

These answer different questions and should not be conflated.

## Decisive fork: residue 82

Residue 82 is uniquely strong:

```
U4: dot 10 / slash 2
U5: dot 10 / slash 0
```

So a single physical observation has an exact interpretation:

- `82 = /` → all U5 states are falsified and exactly the two G5-only states remain;
- `82 = .` → the two G5-only states are removed and U4 collapses exactly to U5.

Physical serial family:

```
082, 190, 298, 406, 514, 622
```

## Best U5 state resolvers

Residues **84** and **102** are exactly balanced 5/5 inside U5, providing one full bit each:

```
84:  084, 192, 300, 408, 516, 624
102: 102, 210, 318, 426, 534, 642
```

They do not separate U4 from U5, so their value is conditional on the recursive family remaining live.

The next-highest U5 entropies are residues 61, 88, 91, 100 and 106, each with a 4/6 or 6/4 split.

## Secondary U4-vs-U5 discriminators

After residue 82, the largest current distribution shifts are:

```
22, 25, 55
61, 100
88, 91, 106
58
```

None is individually decisive because both possible symbols still occur in U5.

## Prospective tail validation

Residue 94 is not a state discriminator anymore, but the tail-stack rule now predicts it sharply:

```
85  = dot   observed
94  = slash predicted
103 = dot   observed
```

Physical family:

```
094, 202, 310, 418, 526, 634
```

A physical 94-family sticker therefore tests the one-slash-per-depth-stack rule directly.

## Operational use

Run this ranking again whenever a new physical sticker adds a previously unseen residue. Repeat observations such as sticker 043 should update provenance/replication counts but will not change this ranking unless they contradict the established residue value.

The scores are **model-conditional acquisition utilities**, not posterior probabilities for U4 or U5.

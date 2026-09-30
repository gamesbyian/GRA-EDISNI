# Experiment 343 - lever-cue lineage and alphabet-boundary proof

_Status: completed, 30 Sep 2026._

## Historical provenance is earlier and stronger than Experiment 342 initially recorded

Experiment 342 anchored the sticker-symbol -> lever hypothesis to the 21 Mar 2021 discussion. A deeper pass through the same immutable public Discord export finds the idea almost a year earlier.

On **23 Apr 2020**, shortly after the nine-piece background layer had been assembled, the community inspected the Collector's Edition reversible cover. The archived discussion records:

- the cover was advertised by iam8bit as containing a hidden clue;
- an otherwise awkward/impossible-to-achieve game perspective makes the three familiar sticker marks conspicuous;
- `aperson1` explicitly identifies those marks as the Collector's Edition sticker symbols;
- a few minutes later, the same discussion compares their physical arrangement with the secret-ending three-position lever;
- the proposed workflow is to identify the order of the CE symbols and enter that code into the lever;
- `santiface` proposes the printed copy number as the likely ordering.

This is followed in March 2021 by the more explicit formulation already captured by Experiment 342:

```
dot   = left
dash  = right
slash = top
```

matching the lever:

```
left / right / up
```

and therefore:

```
. -> L
- -> R
/ -> U
```

The lever-consumer idea is thus not a single late speculative comment. It has a documented 2020 -> 2021 lineage grounded in the CE cover, the sticker marks, and the in-game lever.

### Source

Public archive:

- repository: `gamesbyian/playdead-unofficial-exports`;
- channel: `ARG / solving`, ID `461275582970462209`;
- immutable text blob: `1889cc948f86f5a4455de0d7310b15cdb1b88b5c`;
- first recovered lever linkage: 23 Apr 2020;
- explicit positional mapping: 21 Mar 2021.

The April 2020 discussion also preserves a useful epistemic distinction: "copy number" was a community proposal for ordering, not a developer instruction. The printed serial remains independently real evidence, but serial-order-as-lever-sequence is a hypothesis.

## A stronger negative than Experiment 342's sparse-data replay

Experiment 342 tested the known normal bunker password against the incomplete physical corpus and found no exact canonical forward/reverse match.

The 81/27 alphabet boundary gives a stronger result that does not depend on missing cells.

Under the historical sleeve mapping:

```
residues 1..81: slash/dash -> U/R only
residues 82..108: slash/dot -> U/L only
```

So the complete H108 tape, whatever the unknown symbols turn out to be, has this command alphabet:

```
81 commands drawn only from {U,R}
followed by
27 commands drawn only from {U,L}
```

The known bunker password is:

```
UURLRRRUUURLLL
```

It alternates between R and L in a way that cannot be embedded across a carrier having only one U/R -> U/L boundary per 108-cycle.

Exact enumeration confirms:

- canonical forward placements: **0 / 108**;
- canonical reverse placements: **0 / 108**;
- placements after any of the 14 cyclic rotations: **0**;
- placements after reversal plus any cyclic rotation: **0**.

This is independent of every unobserved foreground cell.

## Correction to Experiment 342's cyclic sensitivity result

Experiment 342 reported one wildcard-compatible match after rotating the known password:

```
H108 start 98
5 / 14 cells physically observed
```

Experiment 343 shows that this cannot survive completion of the *known alphabet zones*. It only appeared because Experiment 342 treated unobserved cells as unrestricted wildcards rather than respecting the directly observed slash/dash versus slash/dot zone alphabets.

Therefore that weak cyclic hit is now **closed**, not merely low-confidence.

## Interpretation

The familiar 14-command bunker password is decisively ruled out as a contiguous substring of the serial-ordered H108 sticker tape under the sleeve/lever mapping.

That does not kill the lever consumer. It sharpens what the live hypothesis must be:

1. the sticker foreground encodes a **different** lever sequence; or
2. an independently supplied selection/reordering operation must be applied before lever entry; or
3. the CE cover uses lever geometry to communicate the three symbol meanings, while the eventual consumer is not the ordinary bunker password.

The direct serial-order idea is historically plausible and physically natural, but it currently supplies a 108-period command tape with a conspicuous two-zone alphabet. Any intended lever interpretation must explain that architecture.

## Consequence for priorities

The next useful question is no longer "can the stickers contain the known password?" That branch is closed structurally.

Instead search for an independent cue that answers at least one of:

- which subset of H108 is the actual command sequence;
- where the sequence starts and ends;
- whether the 81/27 split is an instruction to transform/select rather than a literal command boundary;
- whether another CE/game artifact gives the required traversal or selection.

Do not brute-force arbitrary subsequences or permutations into lever codes.

## Reproducibility

```bash
python scripts/audit_lever_alphabet_boundary.py
```

# Experiment 430: historically cued lever readout versus fixed-depth controls

## Question and frozen operations

Prior INSIDE ARG puzzle mechanics demonstrate that code can specify a physical
operation (Switch controller actions), and 2021 community sticker discussion
explicitly mapped the CE sleeve's three symbols to the secret-ending lever:
dot=left, dash=right, slash=up. There is **no independently supplied
27-action consumer**, so translating a sticker-derived word into lever actions
does not establish a valid lever password.

This audit instead tests a narrower claim: does the native Q4 selected-depth
operation produce unusually *completion-stable* output on the raw
observation-compatible family compared to **three fixed-depth control reads**?

- **Selector**: for each primary quarter q=0,1,2 and each A–I index j,
  take the symbol at `(q, S[j], j)`, with S the exceptional Q4 slash depth.
- **Fixed 0,1,2 controls**: replace S[j] with constant depth d for all j.
- Read the 9 symbols for each quarter in serial A–I order, concatenating
  Q1,Q2,Q3 to a 27-character word. Optionally translate slash to U and dash
  to R, which is merely a reversible re-labeling.

The first-nine 3-of-9 body grammar and one-slash tail are the same
observation-only family from Experiment 429. The result is evaluated on
324 A∩B candidates, the narrower 12 A∩B∩S candidates, and the narrowest
six A∩B∩R∩S overlaps. Requiring S to have one dash per column **already
forces nine total dashes** in the selected 27-mark readout.

## Exact result

| Candidate ensemble | Masters | Selector distinct words | Selector fixed positions | Fixed depth 0/1/2 distinct words |
|---|---:|---:|---:|---|
| A∩B | 324 | **68** | 19/27 | 3 / **1** / 6 |
| A∩B∩S | 12 | **3** | 21/27 | 3 / **1** / 2 |
| A∩B∩R∩S | 6 | **3** | 21/27 | 3 / **1** / 2 |

The fixed middle depth is identical for every one of the 324 primary-column
candidates:

```
---/-/-/--//////--//////---
```

That rigidity is a property of the observed marks plus the primary
placement constraints; it is not evidence that Playdead instructed the
solver to read the middle layer.

The 12 S-constrained masters yield exactly the following three
selector-read 27-mark words (Q1/Q2/Q3 separated by spaces):

```
 //-///--/ //////--- ---//////
 -/-////-/ -//////-- /--///-//
 -/-////-/ //////--- ---//////
```

Their multiplicities in the 12-member set are 2, 4 and 6,
respectively. Their common mask fixes 21 of 27 output positions.
The same three words appear among the six-way overlap; frequencies
within that smaller subset differ.

The apparent repetition of the incumbent `---//////` terminal in
some third-quarter readouts must not be promoted as independent
confirmation: the S filter was built from the same selected-column
machinery that generates this pattern, and the variant readout
`/--///-//` also survives.

## Interpretation

1. A compact selector readout is possible under the selected-surface
   condition, but **the simplest unconditional stability diagnostic does
   not privilege the selector**. Fixed middle depth has one possible
   output across the much larger 324-member family.
2. A slash/dash-to-Up/Right relabeling is motivated by a historical
   external artifact, but it gives 27 commands, whereas the previously
   cited bunker word has 14 commands. No clue selects a justified 14-mark
   subsequence or ordering.
3. All these words have only two symbol types because they are drawn
   from the first 81 positions. No Left command appears. That is
   incompatible with the familiar 14-action bunker word if applied
   without another independently cued transformation.
4. D4 rotations and reflections of the 3×3 XY field are bijections on
   positions. They do not create extra information or change distinct
   word counts. Testing them for aesthetic output would be semantic fishing.

The result is **negative/limiting**. It preserves the concrete three-word
candidate set and closes the naive claim that a Q4-selected 27-action
lever command is uniquely determined by existing observations.

## Reproduction

```bash
python scripts/audit_sticker_readout_consumers.py
```

The script imports the previous exact completion-ensemble helper and
asserts all family sizes, distinct-readout counts and invariants.
The counts were independently enumerated against the physical CSV
when authored; the repository Python script awaits checkout execution.

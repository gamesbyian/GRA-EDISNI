# Experiment 429: exact cross-theory completion ensembles

## Question

Can many plausible guesses for the remaining 42 unobserved H108 foreground positions
be tested against the historical row/column, cube-depth, and Q4-selector
hypotheses without treating attractive reconstructions as discoveries?

This audit enumerates the *whole* space in nested, explicitly conditional
grammar classes, rather than independently sampling 42 unknowns or silently
filling them with the incumbent machine.

## Evidence and frozen coordinates

Input: `data/observations.csv` as of the 84-record/66-unique-residue checkpoint.
The first nine consecutive 9-symbol frames (residues 1–81) are ordered A–I,
each physically laid out `IAB/CDE/FGH`; three final frames (82–108) share
the same A–I coordinates. Unknown physical symbols remain unknown at intake.

No machine-derived missing stickers, hidden-state guesses, terminal `100`,
semantic ranking, or external artifact is used.

## Four independent filtering conditions

- **A: 3-of-9 body census**: each of the nine primary 3×3 frames has exactly
  three of one symbol and six of the other, with either polarity allowed.
  The Q4 A–I depth stack has exactly one slash and two dots.
- **B: physical-column placement**: additionally, each primary physical
  column has exactly one minority symbol.
- **R: simple row exceptional selection**: for each A–I class, the Q4
  slash position selects one of the three primary quarter groups and
  its three-depth word contains exactly one minority mark. This is a
  simple same-type interpretation, *not* the complete frozen Experiment
  329 family and not a genuine independently validated row decoder.
- **S: selected-surface one-dash-per-column**: for each of the three
  primary quarters, choose at each A–I position the depth marked by
  that class's Q4 slash. The resulting 3×3 physical surface has exactly
  one dash in each column. This is a test of a *pre-existing,
  machine-associated* structural rule, not independent confirmation
  of recursion.

## Exact census of physical-compatible complete 108-cell masters

| Conditional family | Masters |
|---|---:|
| A | **233,280** |
| A∩B | **324** |
| A∩R | **62,640** |
| A∩S | **4,528** |
| A∩R∩S | **1,656** |
| A∩B∩R | **108** |
| A∩B∩S | **12** |
| A∩B∩R∩S | **6** |

These are exact enumerations of full-length candidate symbols, including the
one-slash Q4 family. No probability weights are implied. **Important prior-art
reconciliation:** Experiment 418 already reports incumbent-stage counts
U2=324, U3=108, U4=12, U5=10 after sticker 427. Numerically equal counts
are not novel discoveries; this audit's contribution is transparent
operation-by-operation cross-family intersections and a much broader
233,280-candidate parent. Set identity with U2/U3/U4 must not be assumed
from count equality alone.

The 233,280 count factors as 12,960 complete primary bodies × 18 admissible
Q4 depth codes. Physical-column B restricts the first factor to 18, hence
18 × 18 = 324. Across A, 116,640 masters also match a total slash/dash/dot
census of 54/36/18; this extra census is *not* a licensed independent rule.

Among the A∩B family, **91/108 residues** are invariant, with the remaining
17 at 22,25,49,50,52,54,55,58,61,82,84,88,91,93,100,102,106.
Those invariants depend on the chosen B grammar and are not newly
observed physical sticker marks.

## Spatial cube signal check

Using only primary cubes 1–3 (to avoid the known slash/dot alphabet
boundary), count same-symbol adjacency on the solved physical 3×3 XY
surface and between adjacent depths at identical XY.

- A∩B: XY match count range **45–53 / 108 edges**;
  Z match count range **22–27 / 54 edges**.
- A∩B∩S (12 survivors): XY **47–50 / 108**,
  Z **22–26 / 54**.

All selected-candidate adjacency scores lie inside the full A∩B range.
No unusual *additional* cube-local visual clustering emerges under
this elementary score. These are conditional ranges, not randomization
p-values.

## Frozen discrimination within the six-way overlap

Among the six A∩B∩R∩S masters, exactly ten still-unobserved
residues vary: **22, 25, 55, 58, 61, 82, 88, 91, 100, 106**.

Two positions make an exactly balanced **3/3** split:

| H108 residue | six-master foreground division | physical serials ≤600 |
|---|---|---|
| **61** | `/` ×3, `-` ×3 | 61, 169, 277, 385, 493 |
| **100** | `/` ×3, `.` ×3 | 100, 208, 316, 424, 532 |

Residues 22/25/55/88/91/106 split 2/4; residues 58/82 split 1/5.
These counts apply *only* to the six-way overlap. They are not general
forecasts or probabilities and should not overwrite the independently
frozen incumbent prediction matrix.

## Interpretation

1. The complaint that there are too many missing stickers to test ideas
   is incorrect **within a specified structural grammar**: there are
   only 324 full candidates in A∩B, and 12 in A∩B∩S.
2. The initial 324 reduction comes largely from assumptions established
   through analysis of the same physical data. It is not 324 independent
   confirmations of the model.
3. The 12-master survivor count follows explicitly from selector-style
   conditions already explored in prior experiments. Its compactness
   cannot be used as independent proof those conditions were intended.
4. The simple row-selector family and selected-depth family overlap at
   6 strict masters. Current data need not select exactly one of them.
5. Nothing in these tests licenses a new 3D reading, 4D geometry,
   image reconstruction, direct plaintext, or endpoint.

## Reproducibility

```bash
python scripts/enumerate_sticker_completion_ensembles.py
```

The script exhaustively enumerates and asserts all eight family counts,
checks every candidate against observed residues, and reports histograms,
physical invariants, and the nested-family census.

## Follow-ups that would be genuinely discriminating

- Compare the six overlap masters' actual foreground differences and
  select the highest-information missing residue, *before* inspecting any
  new physical observation.
- Introduce a new 3D operation only when an independent physical or
  historical clue fixes its inputs and rules before ranking outputs.
- Use matched completion-family nulls whenever displaying 3D projections.
  Do not compare a structurally constrained master with freely shuffled
  symbols; that merely detects the constraints already imposed.

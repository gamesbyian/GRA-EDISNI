# Experiment 424 — literal IBM 029 punch-card transform

## Question

Could the sticker foreground alphabet `/`, `-`, `.` be intended as literal IBM/Hollerith punch-card characters, with each sticker symbol expanded into a 12-row card column?

This was prompted by a community suggestion that the symbols resemble old IBM punch-card codes.

## Historical mapping

For the IBM 029 card code, the relevant special characters are:

| sticker symbol | IBM 029 punches |
|---|---|
| `-` | `11` |
| `/` | `0-1` |
| `.` | `12-8-3` |

Physical card row order is `12, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9`.

Primary historical source: IBM 29 Card Punch Reference Manual, Figure 29 ("Special Characters"), A24-3332 series. A convenient scan is preserved by the IBM Hursley Museum.

## Method

`scripts/audit_hollerith_punch_card.py` loads the current physical foreground corpus from `data/observations.csv`, deduplicates observations by H108 residue, and expands each known sticker symbol into its literal 12-position IBM 029 punch mask.

Unknown residues are left unknown only on rows that can ever be punched by one of the three sticker symbols. Rows impossible for all three symbols remain known zeroes.

No row permutation, symbol reassignment, polarity choice, completion selection, visual scoring or plaintext criterion is introduced.

## Result

Current physical corpus:

- 66 unique H108 residues;
- 36 slash;
- 22 dash;
- 8 dot;
- 42 unknown residues.

The literal transform contains 118 observed holes.

More important are the completion-independent invariants:

- rows `2,4,5,6,7,9` are **always blank**, regardless of how every missing sticker is completed;
- rows `0` and `1` are exact duplicates because both mean "slash";
- rows `12`, `8` and `3` are exact duplicates because all three mean "dot";
- row `11` alone means "dash".

Thus the nominal 12-row matrix has only **three independent nonzero occupancy patterns**. Those three patterns are exactly the original three sticker-symbol indicator vectors.

The mapping is injective symbol by symbol, so it loses no information, but it gains none either. It is a redundant recoding of the existing ternary foreground.

## Consequences

This sharply limits what the punch-card idea can explain by itself.

It does **not** provide:

- twelve independent bitmap rows;
- a reason to reorder the existing twelve 9-residue sticker rows;
- a discriminator between 12×9 and 9×12 sticker presentation;
- a completion constraint on any of the 42 unknown H108 residues;
- a delimiter role for dot under the literal card-code reading;
- an independent image or plaintext criterion.

A 36×36 reshape of the resulting 1296 bits is not part of IBM card geometry and would destroy the only historically licensed 12-row structure, so it is not promoted as an experiment.

## Disposition

**Historically grounded representation candidate; structurally non-generative on its own.**

The coincidence is still worth preserving because Playdead could have chosen the three glyphs as a punch-card allusion, and the exact 1/2/3 punch multiplicities are unusual. But any next step now needs an independently supplied punch-card-specific consumer, card-column ordering cue, or second artifact that tells us what to do with this representation.

Absent such a cue, visual rearrangement of the expanded matrix would be transform fishing.

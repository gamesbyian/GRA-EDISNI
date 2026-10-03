# Experiment 371 — Xbox Braille structural message selector

_Status: completed exact structural audit, 2 Oct 2026._

The residual-number branch produced a stronger result than the missing `5`.

The solved Xbox Braille field contains 88 cells. In standard six-dot numbering, inspect only the **top row of each cell**, dots 1 and 4, and keep a cell iff either top-row dot is raised.

That selects exactly 19 cells in reading order:

`NEWPLANETDI!COVERED`

Applying the already documented one-dot `!`→`S` correction yields exactly:

`NEWPLANETDISCOVERED`

So the community instruction “put all letters back-to-back” has an exact non-semantic structural equivalent.

Every selected cell is a letter or the anomalous `!`. Every one of the remaining **69 cells** has both top-row dots absent and decodes only to a digit, apostrophe, or dash.

The field therefore has a clean partition:

```
top Braille row active   -> message payload
top Braille row empty    -> residual/filler channel
```

This explains why the residual is so number-heavy. Once dots 1 and 4 are forced off, only dots 2,3,5,6 remain, giving a natural 16-state four-bit subspace. Eleven of those states occur. The five absent states correspond in Braille ASCII to:

`space, comma, double quote, semicolon, 5`

So ASCII `5` is indeed the only missing **digit**, but it is not the only missing state in the natural parent code space. It is one of five absent top-row-empty patterns.

That substantially demotes the literal “nine Xbox digits = nine CE A-I backgrounds” idea.

What becomes more interesting is the solved Xbox mechanism itself: after spatial registration and Braille conversion, one fixed geometric subspace inside each cell identifies payload while the complementary subspace produces plausible-looking junk symbols. That is a much stronger historical precedent for a **structural payload selector** than for a decimal lookup table.

This does not license importing “top row active” into the CE. It does license looking for a sticker-native feature that cleanly separates payload-bearing units from carrier/filler units without semantic scoring.

Relation to this branch:

- Experiment 368 recorded the nine-of-ten digit support and missing `5`.
- Experiment 369 showed that support is orientation-sensitive and strongest in the independently correct orientation.
- Experiment 370 established that original solvers explicitly noticed the numbers and left them unresolved.
- Experiment 371 supplies the simpler structural explanation for why the residual looks numeric at all.

The missing `5` remains a real curiosity, but it is no longer the main result.

Reproduce with:

```bash
python scripts/audit_xbox_braille_structural_selector.py
```

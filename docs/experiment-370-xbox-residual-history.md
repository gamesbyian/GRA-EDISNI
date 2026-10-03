# Experiment 370 — historical status of the Xbox residual numbers

_Status: completed provenance audit, 2 Oct 2026._

## Question

Were the non-letter Braille-ASCII cells in the solved Xbox printer planet ever discussed by the original ARG community, or were they silently discarded?

They were explicitly discussed.

## Primary maintained solving document

The community Google Doc **INSIDE PRINTER SECRET**, last updated 15 Apr 2019, documents the Xbox solution in detail. After explaining the circle reconstruction, 90° rotation, Braille extraction, the `!`→`S` correction, and `NEWPLANETDISCOVERED`, it explicitly says that the meaning of the numbers, apostrophe and dash was unresolved.

Its wording is:

> “it is unclear whether the numbers ... mean anything, or simply serve as ‘filler’”

The same passage also says the Xbox short codes had not been used in solving the puzzle.

Source:
`https://docs.google.com/document/d/1vlpah0LdCRpJe-OfhnkaiBIcmepGXust5BMbaFJGGt8/`

## Contemporaneous Discord/TLDR evidence

The preserved 7 Jul 2018 TLDR says that, once the strings are arranged into the circle and the dash layer is read as Braille, the “legible braille characters” roughly spell `NEWPLANETDISCOVERED`.

That language is important. The community did not establish that every Braille cell belonged to one textual message. They isolated a readable letter channel and left the rest unresolved.

Preserved source:
`gamesbyian/playdead-unofficial-exports`,
`Playdead Unofficial - ARG - tldr [462637922944811028].txt`.

## What is old and what appears new

**Old:**
- solvers noticed the numbers;
- solvers explicitly wondered whether they meant anything;
- filler/obscuration was proposed as one possibility;
- no solution for the residual non-letter cells was established.

**Apparently new in the recovered corpus:**
- the exact census that the 67 numeric cells use nine decimal ASCII glyph identities;
- the observation that ASCII `5` / Braille dots 2+6 is the only decimal glyph absent;
- the exact 9↔9 cardinality comparison with the later CE A-I background alphabet;
- Experiment 369's result that the nine-state decimal support occurs only in the independently correct orientation among the four 2×3-cell symmetries.

So the current line is not resurrecting a solved or rejected old theory. It is revisiting a **known unresolved residue** with a newly noticed structural property.

## Consequence

The historical record changes the framing in a useful way.

Do not call the numbers random filler. The original solvers did not know that.

Equally, do not assume they are a hidden second message. No recovered source establishes that.

The correct status is:

> **historically noticed, explicitly unresolved, newly structurally constrained.**

That is strong enough to keep the lane open while retaining Experiment 368's mapping guardrail.

## Next step

The best evidence-bearing continuation is to reconstruct the exact Xbox Braille cell field with coordinates and ask whether the missing dots-2+6 cell is excluded by the planet geometry or by the letter-placement construction. That can distinguish “incidental consequence of the carrier” from “suspiciously curated residual alphabet” without importing CE data.

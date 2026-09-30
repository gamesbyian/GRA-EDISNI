# INSIDE sticker-mystery community conventions

_Date: 2026-09-29_

Companion to `docs/community-glossary.md`.

This document records recurring notation, visualization, indexing, provenance, and presentation conventions used by the INSIDE ARG community around the Collector's Edition stickers and related puzzles. These are descriptive conventions, not universal rules. When an original source supplies its own legend, orientation, or notation, that source wins.

## Core presentation principle

Prefer community-established wording and visual conventions when presenting community material. Preserve the source's terminology when attributing historical work. Use present-project technical language only where it adds needed precision.

Do not imitate community members, adopt their identities, or write as though the project is part of the historical Discord. The goal is interoperability: a community member should recognize the vocabulary and notation without the agent pretending to be one of them.

## Sticker symbol notation

The physical sticker marks are normally written literally:

- slash: `/`
- dash: `-`
- dot: `•` or `.`

Some later tools use `*` for the dot or one-letter color abbreviations.

When possible, prefer the literal slash/dash/dot symbols in human-facing sticker tables because this is closest to the public sticker ledger.

## Sticker 108-grid color convention

A documented community rendering of the 108-cell sticker master uses:

- red = dash
- grey = slash
- yellow = dot

This explains the later shorthand:

- R = dash
- G = slash
- Y = dot

These colors and letters are visualization conveniences, not intrinsic values printed on the stickers.

## Colors are artifact-local, not ARG-global

Do not assume a color has one meaning throughout the INSIDE ARG.

Game Detectives documents earlier printer-code visualizations in which slash was colored red, dash blue, and dot orange for the PC/PS4 acorn and Xbox planet solutions. That differs from the later sticker-grid red/grey/yellow convention.

Therefore:

1. use the legend belonging to the artifact being discussed;
2. preserve the original palette when reproducing a historical visualization;
3. never translate a color into a sticker symbol without first identifying the source convention.

## 12 by 9 foreground layout

A standard community view writes the 108 foreground positions as 12 rows by 9 columns, in sequence order across each row before moving to the next row.

Later analytical prose calls this row-major order.

References to top rows, bottom rows, row numbers, or columns in community sticker discussion usually assume this layout unless the source says otherwise.

## Cycle indexing and position zero

Physical stickers carry positive three-digit numbers, while the repeating foreground grid includes cycle position 0.

The community reconstruction uses sticker number modulo 108, so stickers 108, 216, 324, and so on occupy cycle position 0.

This creates an off-by-one hazard. Before interpreting an old chart, establish whether it labels cells from 0, from 1, or by physical sticker number.

## A-I background cycle

The nine texture-image classes follow the repeating community convention:

- numbers congruent to 1 through 8 modulo 9 map to A through H;
- numbers divisible by 9 map to I.

The public ledger uses A-I as image-class labels even when the texture itself is difficult to read, because the repeating number-to-image pattern can identify the class.

## Nine-piece assembly orientation

The historically recovered A-I arrangement is:

```text
I A B
C D E
F G H
```

When writing about historical work, distinguish between the community solving the nine-piece image and later researchers using that solved arrangement as a coordinate or registration system.

## TOP and BOTTOM

Later community analysis often divides the 12 by 9 grid into:

- TOP: first 9 rows, 81 cells;
- BOTTOM: final 3 rows, 27 cells.

When discussing the sources that use these terms, prefer TOP/BOTTOM over retroactively replacing them with current-project labels such as primary or Q4.

## Filled, unknown, and overlap cells

A filled or known cell is supported by a physical sticker observation.

An empty or unknown cell has not been physically observed. A blank in a community grid should not automatically be read as zero, space, off, or a fourth symbol.

An overlap is a repeating position represented by more than one physical sticker number. Agreeing overlaps are commonly used as a consistency check.

## Observed versus predicted

Later community tools sometimes display guesses in the same grid as known cells.

Maintain the distinction:

- observed / found / known = backed by physical sticker evidence;
- predicted / guessed = supplied by a heuristic or model.

A filled-looking predicted cell must never be copied into the physical observation ledger as though it were observed.

## Public ledger fields

The canonical public sticker list uses compact notation such as:

`symb: /   img: B`

where:

- `symb` means foreground symbol;
- `img` means A-I texture-image class.

Prefer these labels when reproducing or closely summarizing the community ledger. More formal project terms can follow in parentheses if useful.

## L and U identifiers

Lxx labels are lost-sticker case IDs.

Uxx labels are unresolved or unknown-status case IDs.

Neither is a physical sticker serial. A U case can later resolve into a known sticker or be reclassified into the lost register.

When both appear in one sentence, write the physical sticker number explicitly as a sticker number or serial to avoid ambiguity.

## Three-digit sticker numbers

Community catalogues commonly preserve leading zeroes, for example 002, 020, and 095.

Code may store these as integers, but human-facing community-compatible presentation should normally keep the three-digit form.

## Date convention

The public twinysam sticker ledger explicitly uses day/month/year for the date when sticker information was received.

Preserve that convention when quoting or reproducing ledger dates, and convert to an unambiguous written date when mixing with other date conventions.

## Attribution chains using "via"

Community ledger entries frequently record discovery paths with "via", for example an owner via a finder via Raezores.

This is provenance, not an ownership chain. Do not imply that every named intermediary possessed the Collector's Edition.

## Discovery route is meaningful metadata

The community routinely records whether a sticker came from Discord, Reddit, eBay, Facebook, Instagram, YouTube, Twitter/X, a forum, an image search, or direct owner contact.

Preserve this information when it helps distinguish duplicate sightings, ownership transfers, or independent evidence.

## Original versus edited images

The community ledger sometimes links edited or cropped images made to expose the faint background texture.

For ordinary presentation these can be useful references. For forensic image analysis, the original photograph is primary evidence and edited derivatives must be identified as such.

## Black wrapper / packet language

Historical community outreach often describes the sticker as sealing the black wrapper, black paper wrapping, packet, or packaging around the PS4 game.

These phrases refer to the same practical location of the sticker. When communicating with collectors or summarizing owner reports, this concrete packaging language is often clearer than abstract phrases such as physical carrier.

## Sticker "code"

Community outreach sometimes calls the sticker's number/symbol information a code or ARG code.

Use this wording only where the context is clearly the sticker as a clue. It should not replace more precise terms such as sticker number, symbol, or A-I image class in technical analysis.

## Acorn-based ordering precedent

The acorn is both a historical ARG object and shorthand for an earlier successful ordering method.

Historical sticker discussion includes suggestions to arrange the sticker material "like the acorn". That refers to reusing a prior Playdead puzzle grammar in which row order was constrained by boundary or side marks, not merely making the data resemble an acorn.

Older sources describe these features with phrases such as side pixels, alternating pixels, margin slashes, or dots on either side.

When attributing the historical observation, prefer those source terms. Current-project phrases such as margin bits or check bits may be added afterward for precision.

## "Same layout" and inherited operations

In historical discussion, phrases such as "same layout", "same order", or "arrange it like" another solved artifact can mean reuse of an established row order, orientation, registration, or boundary-mark convention.

Do not reduce those phrases to visual resemblance without checking the referenced earlier puzzle.

## Solved / active puzzle status

The public INSIDE-ARG repository uses explicit active/solved status presentation and often labels completed sections with "Puzzle SOLVED" followed by the recovered solution.

When summarizing community history, preserve the distinction between:

- a community-solved puzzle or sub-puzzle;
- an active unresolved puzzle;
- a hypothesis or proposed interpretation.

Do not upgrade a historically attempted method into a solved convention.

## "Discord source" convention

The public documentation frequently attaches "Discord source" links to chronology bullets and findings.

When a historical claim can be tied to a message, preserve the message/channel/timestamp provenance rather than citing only a later summary.

## Old screenshot reading checklist

Before extracting structured data from a historical community screenshot or chart, establish:

1. whether indexing begins at 0 or 1;
2. whether sequence order runs across rows or down columns;
3. which color legend applies to that specific artifact;
4. whether blanks mean unknown or an actual value;
5. whether predictions are mixed with observations;
6. whether A-I labels denote texture classes, assembled-image positions, or both;
7. whether the display has been rotated, shifted, mirrored, or otherwise transformed;
8. whether an edited image or chart has replaced the original source pixels.

## Default for new project-facing communication

When there is no strong reason to do otherwise:

- say sticker number rather than chain number;
- say slash, dash, and dot rather than G/R/Y in prose;
- retain three-digit sticker formatting;
- say A-I image or texture class rather than carrier class;
- use 12 by 9, TOP/BOTTOM, known/unknown/overlap when describing community charts;
- use acorn, side pixels, and other historically established names when referring to those artifacts;
- introduce formal machine terms only when the analysis actually depends on them.

This preference applies to presentation and communication. It does not require renaming internal code, machine-state variables, experiment identifiers, or exact theorem language where the formal vocabulary is necessary.

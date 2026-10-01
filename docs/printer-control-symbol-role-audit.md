# Printer-control symbol-role audit

_Date: 2026-10-01_

## Question

Do the newly preserved solved-printer control corpora support treating the three printed marks as exchangeable symbols, or do they show that Playdead used mark identity in structurally different roles before interpretation?

This is a control audit only. It does not transfer any printer-specific position, polarity, ordering, or answer into the Collector's Edition sticker foreground.

## Inputs

- `data/printer-reference/pc-ps4-raw.txt`
- `data/printer-reference/xbox-one-raw.txt`
- `data/printer-reference/metadata.json`

Only the fixed-length rows are used: 32 PC/PS4 rows of length 32 and 36 Xbox One rows of length 36 (including the documented repeated Xbox boundary row). Publication order is irrelevant because this audit compares fixed character positions within rows.

## Frozen readout

For each corpus and each fixed character position, count `.`, `-`, and `/`. Also inspect the two row endpoints. No row permutation, semantic scoring, image reconstruction, or sticker model is used.

## Result

Both historical controls reject a naive assumption that the three marks occupy interchangeable positional roles.

### PC/PS4

- left endpoint: 21 dash, 11 slash, **0 dot**
- right endpoint: 16 dash, 16 slash, **0 dot**
- the most slash-heavy fixed positions are 22 and 24 (zero-based), each with 18/32 slashes
- dots occur internally, reaching 8/32 at positions 6 and 20

### Xbox One

- left endpoint: 28 dash, 8 slash, **0 dot**
- right endpoint: 28 dash, 8 slash, **0 dot**
- position 32 contains 22/36 slashes
- dots are strongly concentrated at several internal positions, peaking at 31/36 at position 11

The endpoint result is exact in both controls: across 68 fixed-length rows and 136 endpoint observations, no endpoint is a dot.

## Interpretation

The solved neighboring printer puzzles provide direct historical precedent for **symbol-role asymmetry** inside the same dot/dash/slash alphabet. In both corpora, dot behaves differently from dash/slash at the row boundary before any semantic decoding is considered.

That raises the prior for sticker hypotheses in which mark identity has a structural role, including the already observation-supported slash-vs-dot tail polarity. It does **not** identify which sticker symbol is metadata, which position is a boundary, or which operation consumes the sticker tail.

In particular, this control cannot be used to choose POS3, row/chunk over column/rail, G5, recursion, terminal `100`, or any hidden completion. The reusable historical lesson is only that treating the three marks as an undifferentiated ternary alphabet is not forced by Playdead's prior printer design.

## Consequence for the reset

Add this as a narrow operation-level prior beside geometry-first decoding and boundary/check-bit registration:

> In solved INSIDE printer puzzles, glyph identity can carry structural positional information before the secondary readout.

Future sticker tests may therefore compare explicitly preregistered symbol-role models against exchangeable-symbol nulls when a sticker-native position or boundary has already been independently identified. Do not search positions or symbol roles using the incumbent machine's success criterion.

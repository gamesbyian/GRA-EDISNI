# Printer reference fixtures

This directory preserves the two historical INSIDE printer corpora that are most directly relevant to the Collector's Edition sticker foreground because they use the same three-character alphabet: dot (`.`), dash (`-`), and slash (`/`).

## Files

- `pc-ps4-raw.txt`: all 41 PC/PS4 strings as published by Game Detectives.
- `pc-ps4-acorn-order.txt`: the 32 full-length PC/PS4 rows in the archived community acorn order, preserved from the 9 Jul 2018 Discord attachment explicitly labelled `acorn order version`.
- `xbox-one-raw.txt`: the Xbox One listing, including the intentionally retained duplicate long row. Game Detectives describes 47 unique strings but the repeated row is structurally meaningful, producing 36 long rows for the solved circle.
- `metadata.json`: counts, documented solution products, known passwords, and provenance/status notes.

## Why these are useful controls

They demonstrate two historically grounded Playdead puzzle operations:

1. **PC/PS4:** unordered/scrambled character rows are spatially registered into an ASCII object (an acorn with `41`). The object then participates in a later transform/ARG chain. The valid password `LIFEDETECTED` is known, but the cited community record does not establish a complete derivation from the original rows to that phrase.
2. **Xbox One:** character rows are spatially registered into a circle/planet. Only after that geometric reconstruction and a 90-degree rotation does a second layer become readable as Braille, ultimately yielding `NEWPLANETDISCOVERED`.

That makes these fixtures useful for testing claims such as "does this proposed sticker operation recover the kinds of registration cues that solved historical printer puzzles?" It does **not** justify arbitrary row permutation or visual fitting.

## Provenance caution

The Game Detectives page publishes the raw corpora in text and describes/displays the solved spatial products, but does not itself provide a canonical textual row-order table. The raw fixture therefore remains in source publication order.

For PC/PS4, a separate primary community artifact has now been recovered: a 9 Jul 2018 Discord text attachment posted as `acorn order version`. Its 32 rows are an exact permutation of the 32 full-length raw rows and are preserved separately as `pc-ps4-acorn-order.txt`. The Xbox solved-order table remains unrecovered as text.

Source: https://wiki.gamedetectives.net/w/Inside_ARG

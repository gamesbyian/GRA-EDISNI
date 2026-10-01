# Printer reference fixtures

This directory preserves the two historical INSIDE printer corpora that are most directly relevant to the Collector's Edition sticker foreground because they use the same three-character alphabet: dot (`.`), dash (`-`), and slash (`/`).

## Files

- `pc-ps4-raw.txt`: all 41 PC/PS4 strings as published by Game Detectives.
- `xbox-one-raw.txt`: the Xbox One listing, including the intentionally retained duplicate long row. Game Detectives describes 47 unique strings but the repeated row is structurally meaningful, producing 36 long rows for the solved circle.
- `metadata.json`: counts, documented solution products, known passwords, and provenance/status notes.

## Why these are useful controls

They demonstrate two historically grounded Playdead puzzle operations:

1. **PC/PS4:** unordered/scrambled character rows are spatially registered into an ASCII object (an acorn with `41`). The object then participates in a later transform/ARG chain. The valid password `LIFEDETECTED` is known, but the cited community record does not establish a complete derivation from the original rows to that phrase.
2. **Xbox One:** character rows are spatially registered into a circle/planet. Only after that geometric reconstruction and a 90-degree rotation does a second layer become readable as Braille, ultimately yielding `NEWPLANETDISCOVERED`.

That makes these fixtures useful for testing claims such as "does this proposed sticker operation recover the kinds of registration cues that solved historical printer puzzles?" It does **not** justify arbitrary row permutation or visual fitting.

## Provenance caution

The Game Detectives page publishes the raw corpora in text and describes/displays the solved spatial products, but it does not provide a canonical textual table of the complete solved row order. Accordingly, the raw files here preserve **source publication order**, not a guessed solved order.

If a primary/community artifact containing an explicit solved ordering is acquired later, add it separately with its own provenance rather than replacing these raw fixtures.

Source: https://wiki.gamedetectives.net/w/Inside_ARG

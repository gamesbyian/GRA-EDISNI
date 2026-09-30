# Canonical sticker image archive

This directory is the repository boundary for physical INSIDE Collector's Edition sticker imagery.

## Authority

The seed corpus is the community-maintained `gamesbyian/INSIDE-ARG` fork. Its `stickers.md` ledger determines which three-digit identifiers are established physical stickers. Files are never admitted merely because a filename happens to contain three digits.

- `originals/<serial>/`: community-accepted source photographs. These are valid independent image-analysis inputs.
- `derived/community-edited/`: historical community edits/crops/enhancements. These are useful references but are **not** independent observations.
- `manifest.csv`: canonical machine-readable inventory and provenance.
- `inventory.json`: coverage summary.

Future independently recovered photographs should be added as new manifest rows only after their physical serial association is verified. Byte-identical mirrors should add provenance, not duplicate observational weight.

Current seed coverage: **81 / 81 ledger serials** with at least one community original; **144 original files** and **16 community-derived files**.

Future analysis must read `manifest.csv`. Recursive filename guessing is prohibited.

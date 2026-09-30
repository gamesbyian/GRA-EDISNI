# Canonical sticker image archive

This directory is the repository boundary for physical INSIDE Collector's Edition sticker imagery.

## Authority

The seed corpus is the community-maintained `gamesbyian/INSIDE-ARG` fork. Its `stickers.md` ledger determines which three-digit identifiers are established physical stickers. Files are never admitted merely because a filename happens to contain three digits.

- `originals/<serial>/`: community-accepted source photographs. These are valid independent image-analysis inputs.
- `derived/community-edited/`: historical community edits/crops/enhancements. These are useful references but are **not** independent observations.
- `derived/community-resized/`: community-prepared resized/cropped copies of originals. These are registration aids only and are **not** independent observations.
- `manifest.csv`: canonical machine-readable inventory and provenance.
- `inventory.json`: coverage summary.

Future independently recovered photographs should be added as new manifest rows only after their physical serial association is verified. Byte-identical mirrors should add provenance, not duplicate observational weight.

Current seed coverage: **82 / 82 ledger serials** with at least one community original; **82 original files**, **16 edited derivatives**, and **70 resized derivatives**.

Future analysis must read `manifest.csv`. Recursive filename guessing is prohibited.

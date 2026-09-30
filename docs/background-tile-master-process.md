# Background tile master reconstruction

## Goal

Produce one reproducible, same-size master image for each sticker background tile A-I by treating every available sticker photograph as a noisy observation of the same underlying printed tile.

The source corpus is not restricted to a hand-picked "best" sticker. The automated build scans:

- the current research repository for serial-tagged sticker images;
- the public `twinysam/INSIDE-ARG` sticker corpus, including raw and community-edited copies;
- the mirrored `gamesbyian/playdead-unofficial-exports` corpus when serial-tagged images are present.

Additional web/repo sources should be added to the acquisition corpus rather than manually pasted into a master. The build now parses every numbered row of the live community `stickers.md` ledger and attempts to recover linked public media as well, so Twitter/X, Reddit, eBay/archive pages, Instagram, ResetEra, collectedit, Willhaben and other ledger-linked pages become candidate photo sources rather than mere citations. Unsupported, private, removed or login-gated sources remain explicit gaps rather than being treated as absent evidence.

## Reconstruction method

`scripts/build_background_tile_masters.py`:

1. discovers image files containing a three-digit physical serial;
2. assigns A-I from the established period-9 physical cycle;
3. detects the sticker quadrilateral and perspective-rectifies it;
4. extracts the common background-print field while excluding the serial line;
5. normalizes broad illumination gradients without binarizing the halftone;
6. independently detects the large black foreground symbol in every sample;
7. masks the symbol, aligns same-tile samples, and takes a masked pixelwise median;
8. inpaints only pixels hidden by every available foreground symbol;
9. emits support and inpainting masks so reconstructed pixels never masquerade as observed pixels.

This is intentionally conservative. The dot/slash/dash foregrounds cover different pixels, so most symbol-obscured background can be recovered from other copies. Only their unavoidable overlap should require local filling, normally a small clump rather than a large invented region.

## Outputs

The generated directory `artifacts/background-tile-masters/` contains:

- `A.png` .. `I.png`: conservative grayscale masters;
- `A-enhanced.png` .. `I-enhanced.png`: contrast-enhanced viewing copies;
- `*-support.png`: per-pixel observation support;
- `*-inpainted-mask.png`: pixels not directly observed in any accepted sample;
- `A-I-contact-sheet.png`: quick visual audit sheet;
- `provenance.csv`: every discovered source, hash, rectification method, alignment score, inclusion flag and rejection note;
- `README.md`: generated sample counts and references.

The support/inpainting products are part of the canonical artifact. Do not use an enhanced image as though every pixel were directly photographed.

## Source acquisition breadth

`scripts/collect_background_tile_sources.py` copies every raw and community-edited serial-tagged image from `twinysam/INSIDE-ARG`, then walks every external URL attached to every numbered sticker entry. It first uses `gallery-dl` where supported and falls back to direct/HTML image discovery. Saved media is renamed under its physical serial before it reaches the reconstruction stage, and `source-manifest.csv` records successes and failures.

This lane deliberately complements rather than replaces PR #57's broader external-evidence harvester. PR #57 remains responsible for heavyweight video archaeology, authenticated/private social acquisition, recurring comments, and general archival evidence. When those outputs are promoted into the repository or a local evidence tree, the master builder already scans the repository and can ingest their serial-tagged images. The two lanes therefore converge on one reconstruction corpus without both owning the same acquisition machinery.

Known unavoidable gaps are authenticated Facebook groups/posts, Instagram or X pages that reject anonymous extraction, Discord media not present in the public export, removed marketplace images, and video-only observations requiring frame mining. These must stay visible in provenance rather than silently disappearing.

## Automation

`.github/workflows/build-background-tile-masters.yml` reacquires the public corpora, expands the corpus from the community ledger's outbound links, and rebuilds the masters from scratch. It commits the generated bundle back to the reconstruction branch, making the first result inspectable and preserving a reproducible path for later corpus additions.

## Follow-up audit

After generation, inspect the contact sheet and provenance table. If one tile is visibly misregistered, fix the registration/crop rule or quarantine the offending sample. Do not hand-paint the master. Any manual exception should be a provenance-visible source exclusion or geometric override, not pixel editing.

Once the A-I masters survive this audit, use them as canonical visual templates for sticker classification, unknown-image matching, frame enhancement/registration, and automated quality checks.

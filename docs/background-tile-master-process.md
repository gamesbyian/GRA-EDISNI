# Background tile master reconstruction

## Goal

Produce one reproducible, same-size master image for each sticker background tile A-I by treating every available sticker photograph as a noisy observation of the same underlying printed tile.

The source corpus is not restricted to a hand-picked "best" sticker. The automated build scans:

- the current research repository for serial-tagged sticker images;
- the public `twinysam/INSIDE-ARG` sticker corpus, including raw and community-edited copies;
- the mirrored `gamesbyian/playdead-unofficial-exports` corpus when serial-tagged images are present.

Additional web/repo sources should be added to the acquisition corpus rather than manually pasted into a master.

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

## Automation

`.github/workflows/build-background-tile-masters.yml` reacquires the public corpora and rebuilds the masters from scratch. It commits the generated bundle back to the reconstruction branch, making the first result inspectable and preserving a reproducible path for later corpus additions.

## Follow-up audit

After generation, inspect the contact sheet and provenance table. If one tile is visibly misregistered, fix the registration/crop rule or quarantine the offending sample. Do not hand-paint the master. Any manual exception should be a provenance-visible source exclusion or geometric override, not pixel editing.

Once the A-I masters survive this audit, use them as canonical visual templates for sticker classification, unknown-image matching, frame enhancement/registration, and automated quality checks.

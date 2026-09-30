# L14 background-tile recovery

_Status: provisional visual lead, not a canonical A-I classification._

## Question

Lost sticker **L14** from the Inside Gaming Collector's Edition unboxing
(`AO2YQCl5qFM`) has a stable visible foreground slash, but its serial is
occluded. This lane asks whether the background tile can nevertheless be
classified A-I from the surviving video pixels.

## Sources

- dense native frames from the bounded Inside Gaming window;
- the project's existing A-I processing artifacts, including
  `tiles_with_masks.png` and the archived mask/inpaint pipeline;
- the project's fork `gamesbyian/INSIDE-ARG`:
  - original sticker photographs;
  - `images/stickers/edited/` human-edited/cropped references;
  - `images/stickers/resized/` normalized real-photo references;
  - explicit A-I labels from `stickers.md`.

The fork currently matches upstream byte-for-byte; it is used as the project
reference source so future fork additions can flow into the same lane.

## Important correction to the first pass

The earliest edited-reference experiments compared L14's **partial exposed
sticker** against whole reference stickers. That geometry is wrong and produced
unstable C/A/H/F/I rankings. Those rankings are superseded.

The corrected comparison treats the useful L14 pixels as the exposed left-hand
portion of the sticker and compares them only with corresponding left-side
subregions of A-I references.

## Corrected frame result

Twenty-six frames from the useful sequence produced enough exposed sticker
pixels for the corrected comparison.

Across all 26 usable frames:

- **B** wins 15/26 frames;
- E wins 5/26;
- C wins 2/26;
- A, F, G, and H each win 1/26;
- D and I win 0/26.

More importantly, quality and temporal stability concentrate on B:

- the **five sharpest usable frames all select B**;
- 7/8 sharpest select B;
- frames **139 through 148 all select B**;
- in the sharpest sequence the common runners-up are C, A, and H rather than a
  single stable alternative.

This makes **B the strongest current visual lead**.

## Why B is not yet canonical

The provisional matcher was tested against 33 held-out **known slash stickers**
from the fork's resized corpus, excluding the prototype image used for each
class.

Held-out performance was poor:

- top-1 correct: **6/33 = 18.2%**;
- top-3 contains truth: **10/33 = 30.3%**.

Random top-1 expectation over nine classes is 11.1%, so the matcher contains
some information, but nowhere near enough to turn the L14 B vote into a
high-confidence physical observation.

Even high apparent match scores do not calibrate cleanly: the same procedure
can confidently misclassify good known photographs. Therefore the repeated B
vote is evidence of a lead, not a solved tile.

## Independent slash/background prior

As a weak structural cross-check, the currently preferred 108-cell completion
has the following slash counts per twelve residues of each background class:

- A 6/12
- **B 8/12**
- C 5/12
- D 6/12
- E 7/12
- F 7/12
- G 7/12
- H 3/12
- I 6/12

This is not a probability model for L14 and must not be used as one. It does,
however, mean that the known slash does not conflict with the visual B lead.

## Current disposition

Record the visual result as:

> **L14 background: B is the leading provisional image-based candidate.**

Do **not** promote L14 to background B in the canonical physical observation
ledger yet.

The useful next discriminator is an improved reference/normalization procedure
that can demonstrate materially better held-out recovery on known degraded
stickers. A clean A-I master set would help, but is no longer a prerequisite:
the fork's edited and resized corpora are sufficient to continue method
development.

## Interpretation discipline

- No generative pixels are evidence.
- Image enhancement is a review aid only.
- The previously reported C/A shortlist is superseded by the corrected
  partial-geometry pass.
- The corrected B lead remains provisional because external validation is weak.
- If a later method achieves robust held-out accuracy and still selects B on the
  sharp L14 frames, that would justify substantially higher confidence.

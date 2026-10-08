# CL-07: complete exact reconstruction of the historical gate-98 shutdown text

**8 October 2026 | Historic positive control: full bright foreground recovered | CE-sticker receiver: not identified**

## Result

The 2018 Playdead Terminal41 gate-98 source image and a separately dated [3 June 2019 Game Detectives reference image](https://wiki.gamedetectives.net/w/File:Inside_activate_shutdown.png) now agree **exactly on every one of the 2,577 bright foreground pixels**:

| Check | Measured |
| --- | ---: |
| Historical reference foreground sites (916×913, red component >200) | **2,577** |
| Six original-image exact-colour layers, duplicates counted | 2,677 |
| Overlap between six projected layers | 100 |
| Distinct bright foreground reconstructed | **2,577** |
| Extra foreground pixels absent from 2019 reference | **0** |
| Historical reference foreground pixels unaccounted for | **0** |
| Binary foreground match | **100% exact** |

Binary packed MSB-first row-major foreground digest SHA-256:

```
e730cd817bfdb952dad01d8a55a9684ca4114746e2398fce5418395527a0f5ff
```

The result reproduces the historically documented shutdown path image; it is a **retrospective exact image reconstruction**, *not* independent rediscovery of the original rule. The original phrase was already published. The historical image was consulted to choose exact colour and registration coordinates, so this is **positive-control validation of the existence and operation of six historical layers**, not an unbiased decode test.

## The missing 32-pixel shift

[CL-06](2026-10-08-gate98-historic-multi-offset-reconstruction.md) recovered five exact-colour layers accounting for 2,070 bright pixels with no false positives. It tested `#020206` at source origin `(1123,1755)`: it correctly overlapped 251 reference pixels but produced **309 errors**. It was therefore correctly excluded as an *incorrectly registered candidate*, but not eliminated as a source colour.

The overlooked sixth-layer offset was **`(1155,1755)`**, exactly **32 pixels farther right in the original source**. At this translation, *all 560 information-bearing `#020206` pixels* coincide with historical white pixels. Exactly 53 overlap already recovered white sites, explaining **all 507 remaining sites without adding a single extra site**.

Why earlier exhaustiveness was misleading: for a 2048-pixel-wide source and a 916-pixel output, the previously assumed legal crop origin was constrained to `x <= 2048 - 916 = 1132`. Yet `x=1155` is legitimate **when the source is a sparse set of original pixel positions translated into a receiving canvas** rather than a complete rectangular array crop. The output window ends at source `x=2070`, **23 pixels beyond the physical source**, but the actual `#020206` marks lie at original x positions **1204 through 2020**, entirely within the source bounds. Pixels beyond 2047 are simply empty. The former crop-bound condition silently excluded the correct translation.

The other five registrations all fit within the ordinary source rectangle.

## Complete six-colour source registration

Let `source[y,x] == exact_RGB` mean exact 8-bit channel equality. For each layer independently, mark output location `(x-source_offset_x, y-source_offset_y)` if that point lands within `[0,916) × [0,913)`. Combine the **six** resulting Boolean masks by OR. No colour thresholding, interpolation, OCR, arbitrary erasure or reordering of sticker values is involved.

| Source RGB | Source-to-canvas offset (x,y) | Colour marks | New marks | Overlap |
| --- | --- | ---: | ---: | ---: |
| `#030101` | (16,36) | 309 | 309 | 0 |
| `#010401` | (1045,57) | 463 | 458 | 5 |
| `#030303` | (14,851) | 431 | 420 | 11 |
| `#050105` | (18,1638) | 324 | 324 | 0 |
| `#030300` | (1121,787) | 590 | 559 | 31 |
| **`#020206`** | **(1155,1755)** | **560** | **507** | **53** |
| Total | | **2,677** | **2,577** | **100** |

These source colours were confirmed through the authentic source image, not approximated from a screenshot. The **2019 reference** has original dimensions **916×913**, filename `Inside_activate_shutdown.png`, upload timestamp **23:02 3 June 2019**, and byte SHA-256 `ae685557122be8562028d8a1c4384c954a760bc4e42e6877c29391d810892d12`. The [primary original gate-98 PNG](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms/gate/98/transmission_id41786174541g1f561f4186454544fdrfd532430980980000000000000000k.png) is 2048×4096, byte SHA-256 `db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded`. Both source hashes are enforced.

**Scope nuance:** The historical PNG contains **18 distinct grayscale/near-white pixel triples**, including **1,636 dark `(1,1,1)` positions**, which the bright-pixel threshold does not count. We have **not** reproduced every RGB byte of the historical PNG or proved the historical black-layer recipe. We have reproduced **the entire binary bright-text foreground at exact native pixel positions**, which establishes the archived decoded textual image without the dark background material.

The historical Game Detectives prose states that the black layer and six *other* colour filters were used. Our six recovered **nonblack** exact RGB layers account for every bright pixel. The black-source planet extraction at independent offset `(4,12)` remains a separate valid [CL-05](2026-10-08-gate98-native-phase-positive-control.md) control, not an invented seventh bright layer.

## New layout observation

All six source information layers occupy roughly a **two-column, three-band arrangement** across the 2048×4096 source. Left group: origin x values **14/16/18**, y values **36/851/1638**. Right group: x values **1045/1121/1155**, y values **57/787/1755**. These offsets do **not** form a constant-pitch perfect grid.

A secondary phase analysis demonstrates two **independent 16-pixel families after registration**:

- Four colours `#030101`, `#010401`, `#030303` and `#030300` have their strongest source-native marks projected onto **output phase (x mod16=4, y mod16=8)**, with respectively **121 / 325 / 174 / 493** sample sites.
- `#050105` and `#020206` have their strongest marks projected onto **output phase (1,6)**, with respectively **155 / 396** sites.

This makes the registration geometry more specific than a generic shuffled overlay. But these are *properties of witness-fitted offsets*, not independent proof that two output phases were intended as a keybook. The 2019 image also contains characters made of off-grid points, so the sixteen-spaced marks alone are insufficient for full text recovery.

## Reproduce and verify

The authoritative small [frozen fixture](../../data/conjecture-lab-gate98-six-layer-complete-2026-10-08.json) contains source/witness hashes, all RGB/offset/count tuples, exact binary output digest, old mistaken offset, and interpretive limits. The [replay/verifier](../../scripts/verify_gate98_six_layer_reconstruction.py) runs in two modes:

- Offline, standard library, no source downloads: validates the frozen six-layer contract and the binary mask digest; invoked by CI.
- Full forensic replay with Pillow and NumPy: reads both original PNGs, verifies their byte SHA-256, projects *all* exact-colour pixels onto the output canvas even across physical source edges, independently matches all 2,577 bright pixel positions with zero errors, hashes the reconstructed bitstream and verifies the failed old `#020206` crop.

```bash
python scripts/verify_gate98_six_layer_reconstruction.py
python scripts/verify_gate98_six_layer_reconstruction.py \
  --source /path/to/original-gate98.png \
  --witness /path/to/Inside_activate_shutdown.png \
  --png-output /tmp/reconstructed-gate98.png
```

**Source control deliberately matters.** No live Terminal41 action, backend POST, or CE owner contact is involved. The date of the historical witness **predates** the physical CE sticker mystery; the original solved message is independently public.

## Consequences for the sticker project, with strict boundary

We now have a **complete executable instance of Playdead's own six-layer information-reception technique**. The decoder's defining mechanics are:

1. isolate **specific exact RGB triples**, not average luminance or three generic colour channels;
2. register **sparse coordinate sets by independently shifted source offsets**, not necessarily complete in-bounds crops;
3. overlay all six masks into one common 916×913 receiving canvas;
4. retain source-mark overlaps without necessarily erasing, averaging or XORing them;
5. recognize that the original black source pixel lattice contains another independent planet-scan observation.

The source *does not* tell us to map the CE's nine background image classes to these six colours or to map dot/dash/slash to RGB. The foreground's genuine code consumer remains unidentified. **Do not claim this new historical success solves or validates any CE decoder.**

The newly justified CE experiment class is a **source-authorized registration search**, asking whether the **sticker background images themselves** provide native crop/registration coordinates relative to `534brn9653f9j8mmd`, the destination physically reached from those backgrounds. A source-specified operation must be fixed independently of missing foreground symbols and produce an auditable check. Merely rearranging 9 tile classes until something looks like the historical puzzle is the same after-the-fact fitting this project is attempting to avoid.

## Next open question

Before borrowing this historical mechanism for the CE, establish a **blind source-native way to derive the six historical colours and offsets** from the original PNG *without comparing to the 2019 image*. The observed 2×3 sparse-panel placement suggests segmentation/registration methods, but the exact x/y shifts were not self-evident. A legitimate cross-puzzle transfer should cite a source-authored rule and freeze its predictions on data not used to devise it.

**CL-07 conclusion:** full historically solved shutdown message's bright-pixel mask, source-authenticated and completely reproduced; original input-selection grammar and any CE foreground application still open.

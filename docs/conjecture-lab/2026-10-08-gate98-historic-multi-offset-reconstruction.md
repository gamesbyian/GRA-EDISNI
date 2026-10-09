**Superseded 8 October 2026 by [CL-07](2026-10-08-gate98-complete-six-layer-reconstruction.md):** This is the preserved *intermediate* five-layer account. The previously rejected `#020206` filter is the authentic sixth foreground colour after a **32-pixel registration correction to (1155,1755)**. All **507** formerly unexplained white pixels are recovered with **zero false positives**. The correct crop projects sparse pixels 23px beyond a rectangular source canvas edge, hence the earlier legal-crop restriction excluded it. Do not continue treating the 507-site residual as an open search target. The original six-offset authorial key selection and CE link remain open.\n\n# CL-06: reconstructing the original gate-98 shutdown text from historical evidence

_Date: 8 October 2026. Research mode: DEVELOP; target-assisted exact-image reconstruction. This is **not** a Collector's Edition sticker decode._

## Original reference recovered, dated before the CE

The [Game Detectives image page](https://wiki.gamedetectives.net/w/File:Inside_activate_shutdown.png) preserves an actual **3 June 2019** composite image uploaded by Thingy, instead of only a transcription of the solved gate-98 image. Its 916×913 original is [Inside_activate_shutdown.png](https://wiki.gamedetectives.net/images/0/07/Inside_activate_shutdown.png), exactly **25,539 bytes**, SHA-256:

```
ae685557122be8562028d8a1c4384c954a760bc4e42e6877c29391d810892d12
```

There are **2,577 white pixels** if the image is converted to RGB and the red component must exceed 200. Other pixels are not part of this particular thresholded reconstruction. The known historical message is `REPO/SYS/ACTIVATE_SHUTDOWN_PROTOCOL/PROT6y723g90ty9r80234`, documented by the [2018–19 Game Detectives INSIDE ARG account](https://wiki.gamedetectives.net/w/Inside_ARG). No part of that text string was used in any pixel alignment score.

The source is the byte-authenticated `twinysam/INSIDE-ARG` gate-98 PNG, Git blob SHA-1 `127d8772912ffc499e5afaffe321d5bab7e920df`, SHA-256 `db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded`, native 2048×4096. The [CL-05 report](2026-10-08-gate98-native-phase-positive-control.md) had already recovered the original black-pixel planet-scan 16px sampling phase **(4,12)** using source pixels only.

The 2019 wiki image and the 2018 historical puzzle both predate the December 2019 CE sticker distribution, making them valid independent historical **mechanism** controls, but **not** independent witnesses that the CE foreground is meant to use this method.

## The new discovery: separately translated colour-bearing panels

The 2019 composite is not recovered by simply dropping a few selected colours from the source image onto one unchanged coordinate system. The **same-sized 916×913 window** must be selected at different source locations depending on the exact original RGB triple, then each extracted binary mask must be laid onto the target 916×913 registration.

For `(x_0,y_0)`, the raw operation is:

```python
source_region = original_rgb[y_0:y_0+913, x_0:x_0+916]
colour_mask = (
    (source_region[:, :, 0] == r)
    & (source_region[:, :, 1] == g)
    & (source_region[:, :, 2] == b)
)
combined |= colour_mask
```

This operation is exact-pixel equality. There is **no OCR, scaling, rotation, threshold adjustment or font fitting** on the source image. The historical reference is thresholded only once to define the expected bright-pixel mask.

Five individually 100%-precise original-image masks have been recovered:

| Exact source RGB | Source crop origin (x,y) | Pixels in crop | Newly explained pixels | Pixels outside 2019 reference |
| --- | --- | ---: | ---: | ---: |
| `#030101` | (16,36) | 309 | 309 | 0 |
| `#010401` | (1045,57) | 463 | 458 | 0 |
| `#030303` | (14,851) | 431 | 420 | 0 |
| `#050105` | (18,1638) | 324 | 324 | 0 |
| `#030300` | (1121,787) | 590 | 559 | 0 |
| **Five-layer union** | | **2,117** (47 duplicates) | **2,070** | **0** |

The union reconstructs **2,070 / 2,577 = 80.3% of all historical white pixels**, with **no false positives**, leaving exactly **507** unexplained. This is a concrete positive-control recovery against an independently archived historical image, not merely an attractive pareidolic shape. The original reference is still required to verify exact correspondence; the 5-layer result is not a stand-alone newly deciphered plaintext.

The finite registration audit also matters: exhaustive legal 916×913 crop translations for the tested exact source colours show that, for each of these five, the above **was its only perfect-precision window with at least 50 foreground pixels**. This greatly limits arbitrary coordinate cherry-picking *within the tested colours*. However these five **RGB colours and offsets were selected while examining the already-known reference**. This is therefore a successful **target-assisted reconstruction**, not an out-of-sample discovery of a decoder key.

## Separate source-native phase evidence

Before consulting the historical target's exact pixel pattern, the original source itself has unusually concentrated, distinct 16×16 phases for multiple colours:

| RGB | Source section (y rows) | Peak native 16px phase (x,y) | Peak count |
| --- | --- | --- | ---: |
| `#000000` | 0–1023 | (4,12) | 1,591 |
| `#030101` | 0–1023 | (4,12) | 121 |
| `#010401` | 0–1023 | (9,1) | 325 |
| `#030300` | 1024–2047 | (5,11) | 402 |
| `#030303` | 1024–2047 | (2,11) | 128 |
| `#020206` | 1024–2047 | (4,1) | 165 |
| `#050105` | 1024–2047 | (3,12) | 133 |

Unlike the earlier misleading post-selected `0xCF` colour-cube concentration, these are strongly **phase-specific** properties of the true source pixels. Different colours really do carry separately registered information, and their locations are dispersed across the large PNG. This does **not** make their crop offsets independently authorized; the phase grid specifies local periodic registration, not which 916×913 part of the full 2048×4096 image should be extracted.

## The unresolved sixth historical colour, with a useful negative

The Game Detectives description says **black plus six other exact RGB colours** were merged. Our five verified colours are among the nonblack colours. That leaves at least one nonblack extraction and perhaps a black extraction to recover.

`#020206` is tempting: all **165** of its appearances in the second source quarter lie at one 16px phase `(4,1)`. Yet the best simple crop under investigation, at offset **(1123,1755)**, produces:

- 560 exact-`#020206` source pixels;
- 251 pixels coincident with the historical white reference;
- **309 false-positive pixels** absent from the historical composite.

Across the inspected legal crop offsets with at least 50 marked sites, `#020206` did not yield a complete all-valid mask. This is a **negative for unmodified direct extraction**, not grounds for forcing background subtraction, a new scaling factor or arbitrary erasures until the 2019 picture is recreated.

The remaining **507 white pixels** are still an explicit unresolved objective. The full six-nonblack-colour historical route is **not yet regenerated** by the current code.

## Exact reproduction and validation

The durable machine-readable record [data/conjecture-lab-gate98-historical-layer-control-2026-10-08.json](../../data/conjecture-lab-gate98-historical-layer-control-2026-10-08.json) freezes the source and witness SHA-256 hashes, dates, five exact colours and offsets, source-only phase controls, independent source-target pixel overlaps, the failed sixth-colour branch, and current interpretation limits.

`python scripts/audit_gate98_historical_layer_reconstruction.py` verifies the frozen historical record from local JSON using only the Python standard library and is added to CI.

To reproduce actual pixel registration (NumPy + Pillow required):

```bash
python scripts/audit_gate98_historical_layer_reconstruction.py \
  --source /path/to/original-gate98.png \
  --witness /path/to/original-2019-Inside_activate_shutdown.png
```

The original 19 MB PNG remains byte-preserved upstream and is not duplicated in this repository. The [2019 Game Detectives image](https://wiki.gamedetectives.net/images/0/07/Inside_activate_shutdown.png) was fetched as an authenticated reference during [the CL-06 source-acquisition run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37860133993). Both inputs are SHA256-checked before comparison. The small JSON fixture and reproducer remain in the repo, even when the temporary acquisition workflow is removed.

## What this permits for CE sticker conjectures

The original ARG demonstrably uses **source-image filtering and multiple separately registered image panels that must be overlaid**. That is a stronger and more specific *historical operation-class precedent* than a speculative 512-record address book or three arbitrary RGB channels.

A conditional CE idea is to treat its nine background image classes as registrations to **nine different regions** or nine *position choices* over an external target, using foreground `/ - .` as the filter commands or layer selectors. But historical six-colour extraction is not an instruction to arrange **nine CE classes** this way, and those classes may have very different semantics. Any proposed correspondence must yield source-authored offsets/order and distinct physical predictions; one cannot cite the historic successful composite to validate a CE candidate chosen after seeing it.

The **physically linked sticker background** still directs solvers to `dat/534brn9653f9j8mmd`, which remains the stronger destination for foreground research. Gate-98 is a validated operation analogy, not a known receiving artifact for the CE.

## Forward work

1. Reconstruct the remaining 507 historical pixels with a source-derived additional colour/section rule **or obtain the original 2018 colour legend**. Maintain exact source-window cardinality/false-positive controls and stop on unlicensed parameter proliferation.
2. Once the full historical 7-colour image has been reassembled, test for a concise source-native registration grammar explaining the six source panels *without consulting the recovered text pixels*.
3. Only then transfer the **operation class**, not the already decoded answer or fitted offsets, to a clearly typed CE hypothesis, with a frozen expected artifact and matched controls.

**Bottom line:** five original RGB layers can already be reproduced at 100% precision, giving 80.3% of an independently dated historical message. The remaining stage and the CE foreground connection are both honestly unresolved.

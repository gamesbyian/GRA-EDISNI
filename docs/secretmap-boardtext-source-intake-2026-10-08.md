# Original INSIDE asset recovery: SecretMap witness and BoardText DDS

_2026-10-08, source-first asset/consumer lane. Research, not a sticker decode._

## Executive finding

**Two previously descriptive archive leads have been upgraded to inspectable source materials.**

1. A surviving **480×240 JPEG image** explicitly identified in its 2018 Chinese-language republication as `SecretMap #44506.dds` is still accessible at [image.9game.cn/2018/3/2/19669991.jpg](https://image.9game.cn/2018/3/2/19669991.jpg). The screenshot shows a **dark, perspective-like spatial scene with sloping wireframe/lines and separated red marks**, rather than a clean numbered 2D table. The image is watermarked and is not original DDS bytes. Earlier July 2016 investigators already disagreed about whether `SecretMap` was an orb map or a flattened/projected 3D object. The screenshot strengthens the need to establish native coordinates and transforms **before** making a 14-orb registration claim.
2. A real **archived original `BoardText` DDS** is present at [playdead-unofficial-exports/assets/BoardText_13309-b0922098d7c08dbe.dds](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/assets/BoardText_13309-b0922098d7c08dbe.dds), Git blob SHA `d8e19793cb3b09764728fb2fc3cf4aaa4e1d32e8`. Its exact bytes were inspected through the GitHub byte-preserving base64 fetch. It is a **256×32, DXT5/BC3 compressed texture with an eight-mip metadata field**. The base alpha plane decodes to 8,192 pixels, of which **2,061 have nonzero alpha**, and contains multiple words of small-format board lettering. This establishes actual historical texture data rather than a speculative filename. It does **not** demonstrate an alternate code-input handler or CE-sticker channel.

The two artifacts have very different provenance and interpretive force. Do not treat the externally republished screenshot as original Unity bytes, or a decoded visible texture as proof of unobserved gameplay.

## Timeline / provenance

| Source | Dated witness | What is established | What remains unavailable |
| --- | --- | --- | --- |
| [2016 Steam discussion](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2) | 15 July 2016, MASTAN | Names `BoardText_#292`, `SecretMap_#916`, their proposed meanings; links original `postimg.org/gallery/239os5ggo/` extraction gallery. | Original uploader's intact image gallery and raw full game bundles. |
| [2016 3DM Chinese report](https://www.3dmgame.com/gl/3577786.html) | 16 July 2016, derivative compilation | Calls source `SecretMap #44506.dds` and questions map interpretation, suggesting 3D projection. | Exact attachment image not independently acquired as raw bytes. |
| [2018 9game republication](https://www.9game.cn/news/2199070.html) | 2 March 2018, derivative repost of 2016 text | Its inline **SecretMap** image [direct JPEG](https://image.9game.cn/2018/3/2/19669991.jpg) is presently viewable. Companion `Sign_SecretMorse` image [direct JPEG](https://image.9game.cn/2018/3/2/19669987.jpg) is likewise available. | JPEG rescaled/watermarked; cannot establish original texture size/UV geometry or secret-site coordinates. |
| [Archived BoardText DDS](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/assets/BoardText_13309-b0922098d7c08dbe.dds) | Original asset preserved in independent community export | Actual bytes, packed texture geometry, and alpha pixels inspected. | Gameplay assembly and mesh/UI usage still not inspected; original data-derived artifact format and version may require independent retest. |

The numerals `#292`, `#916`, `#44506`, and `13309` have **incompatible exporter provenance**. They must not be treated as author-authored serial addresses or deliberately connected to sticker number 427, 23, 108, etc.

## BoardText exact format and no-appended-blob control

Source 11,152 bytes total, DDS header 128 bytes; FourCC `DXT5`; 256×32 first mip; declared mip-count field 8. A naturally formed mip pyramid **base plus eight further levels** exactly accounts for the whole blob:

| Level | Dimensions | BC3 bytes |
| --- | --- | ---: |
| 0 | 256×32 | 8,192 |
| 1 | 128×16 | 2,048 |
| 2 | 64×8 | 512 |
| 3 | 32×4 | 128 |
| 4 | 16×2 | 64 |
| 5 | 8×1 | 32 |
| 6 | 4×1 | 16 |
| 7 | 2×1 | 16 |
| 8 | 1×1 | 16 |
| **+ DDS header** | | **128** |
| **Total** | | **11,152** |

The fixed file length is **exactly** the header plus this compressed-mip footprint, leaving **zero unexplained trailing bytes** under that interpretation. Note the apparent eight-versus-nine level terminology ambiguity; this describes measured lengths, not a proof the tool's `dwMipMapCount` was semantically standard.

The primary alpha channel was decoded directly using BC3 palette interpolation, rather than interpreting the exported picture through an unreliable text-only connector. The pixel evidence supports a small textual sign. The original 2016 reader's `ENTER CODE SEQUENCE` transcription and probable association with the secret-ending status board remains the strongest **known gameplay function**. Do not infer another CE-specific input without a real input handler.

Portable exact-format reproduction:

```sh
python scripts/decode_inside_boardtext_dds.py --self-test
python scripts/decode_inside_boardtext_dds.py /path/to/BoardText_13309-b0922098d7c08dbe.dds /tmp/boardtext-alpha.pgm
```

The script checks the Git blob SHA, exact DDS dimensions/format, block layout, nine-level full-file accounting, and the 2,061 nonzero-alpha pixel census. It produces a **PGM**, not a speculative decoding of textual content.

## SecretMap: bounded next test

The 2018 image does **not** show an obvious flat 3×3 keypad or nine separate numbered cells. It shows an unusually flattened perspective arrangement of red/black markers and line segments against gray. On this evidence:

- **More plausible initial models:** technical map/projection of scene/camera or level space; a collection of in-world secret points; a flattened game-space visualization requiring native transforms.
- **Less motivated:** a direct 108-symbol monochrome canvas, a nine-tile keypad or author-specified A–I sticker code.
- **Undetermined:** number of native markers, which correspond to secret orbs, what the faint lines mean, whether the 2018 screenshot has distortion/cropping masking a meaningful diagram.

The next test must acquire the **original DDS**, use its pixel dimensions plus renderer/mesh coordinate system, and check the pre-existing **14-orb hypothesis** first. Compare any extra independent marks to the known secret positions using a registered geometry and a held-out/null set. Do not tune a homography to force red dots onto hypothetical CE symbols.

The available republished JPEG has no proven native coordinate axes. Counts of red patches from it would be segmentation- and watermark-dependent; do not promote an arbitrary blob count as evidence.

## Binary preservation and limitations

- The original **BoardText DDS already lives in the public community archive**, pinned above by Git blob hash; its bytes are not duplicated here. Its exact decoding instructions and structural constraints **are committed**.
- The original **SecretMap DDS has not been downloaded or recovered as bytes**. The [2018 derivative image](https://image.9game.cn/2018/3/2/19669991.jpg) was opened and visually examined through public web retrieval; a direct binary download to the local container failed. It is therefore source-linked, **not** declared preserved as a Git blob.
- The earlier cover-analysis ZIP and derived visuals are a separate binary retention matter, transparently documented at `archive/external/cover-source-audit/README.md` with exact integrity checks.

## Epistemic change to the endgame portfolio

`SecretMap` remains a **real unresolved asset to investigate**, but its historical appearance and speculative three-dimensionality reduce the appeal of simplistic grid index models. `BoardText` is partially upgraded from purely secondhand prose to genuine decoded source content; however it already has a strong 2016 secret-orb/bunker function and no new CE input. Both observations support the destination-first program's rule: find an **independently usable consumer or transformation**, rather than attach sticker symbolism to a coincidental picture.

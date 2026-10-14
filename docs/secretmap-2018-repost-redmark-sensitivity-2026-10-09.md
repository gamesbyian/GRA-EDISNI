# SecretMap 2018 derivative: red-mark count sensitivity audit

*9 October 2026; DISCOVER / source-quality screening only. This report introduces **no original DDS**, H108 completion, stencil key, or CE-consumer claim.*

## New fixed-byte evidence

The [bounded historical URL recovery](original-game-2016-image-recovery-protocol-2026-10-09.md) ran successfully on CI [run 38024173530](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024173530). Its artifact 11659946636 recovered these two *historically published derivative images*, while the three higher-resolution 2016 Radikal board links failed a strict host-redirect check:

- `secretmap_2018_9game_derived.png`: **480×240**, original 2018 published URL is `https://image.9game.cn/2018/3/2/19669991.jpg` but *actual retrieved bytes are PNG*, SHA-256 `5cf2c46ac98397bb47a16974317a5ee730c5ce48826f75c481322bd9ac8da3b9`.
- `secretmorse_2018_9game_derived.jpg`: historical `Sign_SecretMorse` illustrated graphic, SHA-256 `d3e1872365c1f39c51148b9bd0fbdafafc7904d1dad54f427f5d87283dfae88b`.

The image format inconsistency is important for future source tools: MIME/file extension guesses must not be substituted for magic-byte identification. Both images retain their published provenance as **2018 derivatives of 2016 asset reports**, not original Playdead Unity textures. The script does not require images to be committed to Git; obtain the recovered artifact from the completed workflow and verify the hash.

## Retrospective image-only probe

Instead of counting apparent red objects by eye and declaring the expected fourteen orb marks, run [this source-locked script](../scripts/audit_secretmap_2018_derivative_redmarks.py) against the recovered **PNG**. It uses RGB red excess over both other channels at prelisted absolute thresholds, 8-connected components, and minimum area `2,4,8` pixels. A crop `y<165` deliberately excludes the orange publisher watermark at bottom right.

**The crop and thresholds were chosen after inspecting the image.** Treat all results as sensitivity/descriptive statistics, with no p-value or independent selection score. The faint lines and black/ruby overprint, scaling, anti-aliasing and compression create merged and disappearing blobs. Source pixel coordinates cannot be reliably turned into scene coordinates.

| R-minus-G and R-minus-B threshold | Components ≥2 px | ≥4 px | ≥8 px |
|---:|---:|---:|---:|
| 12 | 20 | 19 | 16 |
| 16 | 18 | 15 | 15 |
| 20 | 15 | 15 | **14** |
| 24 | **14** | **14** | **14** |
| 28 | **13** | **13** | **13** |
| 32 | 13 | 13 | 13 |
| 36 | 12 | 12 | 10 |
| 40 | 11 | 10 | 8 |

### Interpretive limit

The screenshot contains enough distinguishable red regions that a count of **approximately thirteen to fifteen** is plausible under moderate image segmentation settings. *Fourteen* is recovered for some thresholds, consistent with the existing original-game explanation of **13 earlier secret orbs + final orb**. Adjacent settings yield 13 or 15. There is therefore **no reproducibly unique 14-point geometric registration**, much less a second layer uniquely corresponding to 9 A–I sticker classes.

At threshold 24, components split into approximately 5 on the left, 3 in the middle, 6 on the right by the derivative screenshot's x-coordinate; these are **post-hoc visual groups on nonnative projection**, not a preregistered 5/3/6 puzzle shape or a source-specified three-plane machine. The leftmost faint mark disappears at higher threshold, and neighboring marks can split at lower thresholds. Do **not** elevate that pattern to sticker evidence.

### Reproduction

```sh
python -m pip install Pillow
python scripts/audit_secretmap_2018_derivative_redmarks.py \
  /path/to/secretmap_2018_9game_derived.png \
  --out /tmp/secretmap-derivative-sensitive-counts.json
```

The script asserts the actual source SHA-256 before analyzing. All pixel/centroid outputs are derived visual measurements from *that derivative only*. It does not silently normalize to a hypothetical original DDS nor choose a source→orb homography based on correspondence score.

## Decision and remaining source dependency

**Decision:** The derivative currently **supports no positive CE bridge**. It is compatible with a mundane fourteen-orb map but insufficient even to prove the exact marker count. Maintain OG-02 as **source-acquisition dependent**, not as a solved or falsified sticker consumer.

The next useful action is still retrieval of the actual `SecretMap_#916` / `SecretMap #44506.dds` Unity texture with original pixel size and scene mesh/UV transform from a legally accessed, version-pinned retail game build. Use the *existing* [source-frozen 14-orb matching protocol](secretmap-original-asset-null-protocol-2026-10-08.md) and `scripts/audit_secretmap_registered_orbs.py`, accounting for the final orb before claiming an extra symbol. If all red native marks map to normal collectibles and wiring, **close the SecretMap CE-consumer branch**.

**No new sticker values or downstream decode are claimed.** Adjacent independent research should concentrate on the buried elevator's true 12-button/four-screen topology and the source-reference cover monitor differences rather than refitting a watermark-compressed image to a pleasing code.

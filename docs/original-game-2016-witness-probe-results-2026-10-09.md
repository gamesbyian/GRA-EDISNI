# Original-game 2016 witness recovery: observed results and next evidence gate

**Source-acquisition follow-up, 9 October 2026.** This is the result of the bounded source probe described in [the frozen protocol](original-game-2016-image-recovery-protocol-2026-10-09.md), not a new decoding experiment. The two successful image assets are **2018 article derivatives**, not Playdead-issued DDS/Unity original files.

## Executed CI results

[First run 38024173530](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024173530), artifact **11659946636**, tested 11 initially frozen URLs. [Second run 38024356081](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024356081), artifact **11659547316**, tested 13 with two source/ID-derived Imgur targets. The second run's source-preserving JSON and files supersede the first for the manifest of 13 URLs. Remote offline classifiers and manifest safety checks passed.

### Genuine image bytes now captured

| Image | Source URL | Observed native media | Exact bytes | SHA-256 | Grade |
| --- | --- | --- | ---: | --- | --- |
| Alleged \`SecretMap #44506.dds\` illustration | https://image.9game.cn/2018/3/2/19669991.jpg | **PNG**, 480×240 RGB, despite URL ending \`.jpg\` | **31,591** | \`5cf2c46ac98397bb47a16974317a5ee730c5ce48826f75c481322bd9ac8da3b9\` | 2018 derivative screenshot; **not original DDS** |
| Alleged \`Sign_SecretMorse #3372.dds\` illustration | https://image.9game.cn/2018/3/2/19669987.jpg | **JPEG**, 460×100 RGB | **5,061** | \`d3e1872365c1f39c51148b9bd0fbdafafc7904d1dad54f427f5d87283dfae88b\` | 2018 derivative screenshot; **not original DDS** |

The two originals-at-these-URL hashes **remained identical across two independently executed CI pulls**, separated by minutes. They are now temporarily preserved in original image bytes in the run artifacts rather than just linked. Source date/asset identity still depend on the corresponding [March 2018 9game page](https://www.9game.cn/news/2199070.html) which itself paraphrases [July 2016 extraction investigators](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2). Do not mistake repeated download for independent testimony about what the pictures depict.

**Non-native-format caution:** The \`.jpg\`-URL/PNG-body mismatch is a hosting/derivative property, **not** evidence of coded content, steganography or an authorial file extension trick.

### No authentic 2016 original-board screenshots recovered yet

- Three original 2016 Radikal scene-image URLs returned **blocked off-allowlist redirects**, not JPEG magic. The original observer already reported 401 from these hosts in July 2016.
- Two exact July 2016 VK links returned off-allowlist redirects. Their scene identities have not been established as the buried elevator.
- Original \`postimg.org/gallery/239os5ggo/\` extraction-gallery URL failed DNS resolution.
- Three Imgur entry-point pages returned HTML, **not original images**. Only the [original glass-code album USImD](https://imgur.com/a/USImD) exposed a title and original image ID in its HTML: **“Playdead's INSIDE - Lab 4 Glass Window Code (SOLVED)”** with source embedded \`https://i.imgur.com/Xgc8hLr.png?fb\`. The other two 5,478-byte HTML outputs have the **same SHA-256** and no \`og:image\` metadata, consistent with generic fallback shells rather than surviving real albums.
- Both follow-up imgur CDN image IDs returned **HTML error/fallback bodies**, rejected by image magic; their exact URL claims remain provenance-limited (one CDN form derived from the 2016 forum image ID; the other \`og:image\` recorded verbatim). **No Imgur original photo bytes acquired.**

### What the recovered SecretMap derivative actually looks like

A 480×240 gray-background illustration depicting dark sloping lines and multiple red/dark clusters, with a bottom-right branded watermark. The repeated clusters are distributed horizontally at different heights and appear **perspective-like**, compatible with the original 2016 conjecture that the picture was a scene/map projection rather than a clean 3×3 grid. This visual judgement is *exploratory*; source texture/UVs are missing.

A low-cost **hostile count control**, using the actually recovered 2018 PNG, excluded the visually identified bottom watermark strip **y≥174**, took 8-connected components with pixel count **at least three**, and required \`R-G > delta\`, \`R-B > delta\`, \`R >= floor\` with these **fixed sensitivity examples**:

| red-channel difference \`delta\` | R floor | detected colored components |
| ---: | ---: | ---: |
| 15 | 65 | 18 |
| 25 | 70 | 15 |
| 35 | 75 | 12 |

This is **not** an authorial count test, because the watermark cut and red threshold were selected after examining the 2018 image. It establishes that the derivative does **not** supply a robust native count of fourteen distinguishable source markers under these simple threshold choices. Do not extract exactly fourteen via additional segmentation tuning or transfer the 108 sticker marks onto this warped image. The existing [source-frozen fourteen-orb test](secretmap-original-asset-null-protocol-2026-10-08.md) is still blocked on **original DDS plus scene transforms**. The 2016 account already suggested that an apparent “fourteenth” point might simply be the last giant orb.

### New independent screen semantic negative control

A [25 July 2016 contemporary Steam comment](https://steamcommunity.com/app/304430/discussions/0/359543951720753445), by arthur_x, describes the previously discussed **“secret screens”** as images presenting stages of characters **kneeling to standing**, including the boy, scientists, engineers and controlled figures. The [23 August 2016 Atøm report](https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=11) mentions four small screens next to the buried \`Cargo_Elevator_Narrow\` console plus a nearby \`Play screens\` object.

These are two dated reports with **no confirmed object identity or shared scene path**. If they refer to the *same* screens, they support an existing animation/storyboard/control-demonstration explanation instead of four independently indexed puzzle channels. A valid next test is to recover the screen textures or code references, check contents **first**, then determine whether the same assets occur beside the hidden elevator. One narrator's inference that the images prove mind control is not an independent pixel or code-level confirmation.

## Implications for the CE sticker hypothesis

**Validated outcome:** source URLs tested; two exact 2018 derivatives saved in CI artifacts; original game texture/scene bytes remain missing; early scene-image hosts cannot be safely treated as surviving originals. There is **no** new CE decoder, in-game consumer, sticker prediction or geometry.

**Retain these source-first targets**, in order:

1. Original Unity \`SecretMap\` and \`BoardText\` scene UVs + fixed tracker changes across thirteen earlier orbs and final orb (reuse \`scripts/audit_secretmap_registered_orbs.py\`).
2. Original scene/event hierarchy of \`_SignalConnectors\`, \`TriggerElevatorStart\`, \`Cargo_Elevator_Narrow\`, \`Play screens\`. Specifically compare the 25 July “secret screens” frames with the four small elevator-adjacent displays.
3. Original \`FX_ScreenKaypro\` texture and parent screen scene.
4. Recovered original 2016 high-resolution scene images only if they pass byte-signature/provenance checks, not resized derivatives or generic Imgur shells.

Do not create new fabricated scene coordinates or infer four stages from four small screens before the source asset uses are verified. The next source probe can disclose **blocked redirect destination hostnames** while retaining strict refusal to download unknown redirect hosts. If an old source legitimately migrated to a verifiable modern image CDN, document that chain before allowing the specific host.

**Archive caveat:** GitHub Actions artifacts expire after 30 days. Preserve exact SHA-256, format and retrieval URLs in this durable report; move binary derivatives into approved project artifact storage if needed for longer-term offline reproduction. Do **not** claim the artifacts are permanently versioned in Git.

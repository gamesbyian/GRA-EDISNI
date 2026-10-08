# CL-05: recover the authentic gate-98 pixel-grid phase and planet

_Date: 8 October 2026. **Source-native positive control established for the planet scan; historical colour-layer text reconstruction remains open.**_

## Why this matters

[CL-04](2026-10-08-gate98-original-pixel-results.md) authenticated the original 19,360,240-byte Terminal41 gate-98 PNG (2048×4096; Git blob SHA-1 `127d8772912ffc499e5afaffe321d5bab7e920df`; SHA-256 `db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded`). Its initial 16px grid assumed the **unverified phase (0,0)** and obtained no full candidate sticker readout.

The historical [Game Detectives INSIDE ARG record](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button) says isolating exact black `#000000` reveals regularly spaced pixels in the upper left; taking samples at 16px intervals reveals a *planet scan*. Combining the black pixels with six other exact source RGB colours reportedly gives:

`REPO/SYS/ACTIVATE_SHUTDOWN_PROTOCOL/PROT6y723g90ty9r80234`

No reliable source we have recovered independently enumerates all **six nonblack hex RGB colours**, the exact crop or their layer ordering. The 2018-reported **planet image** and **target URL** are therefore separate validation targets. We must not supply the known URL as a dictionary to select favourable colours.

## Independent pixel-origin discovery, source only

We conducted an exhaustive, simple positive-control experiment on the **original image bytes**, with absolutely **no sticker values** or known expected plaintext in the selection algorithm:

1. Crop original source to the first **1,024 pixel rows** (2048×1024) to include the upper-left phase-bearing source area.
2. For each exact-black pixel, increment one of **256** bins indexed by `(x mod 16, y mod 16)`.
3. Rank the 256 bins solely by exact-black count. Set one 16px-grid origin to the winning `(x mod 16, y mod 16)`; *then* render the corresponding 128×64 binary mask.
4. Compare the resulting image with the independent historical **planet-scan** description. Freeze the full bitmap hash and repeatable source code.

The winning offset is

```
x = 4 + 16·column
y = 12 + 16·row
```

with **1,591** black grid positions. The second-highest offset is `(5,12)` with only **68**, and the previously assumed `(0,0)` has only **62**. The winning phase is approximately **23.4×** the second-highest phase in exact-black count. This is a huge within-file spatial-registration signature, not an ambiguous aesthetic pick.

The 128×64 reconstructed black mask is a **recognizable scan of a large circular/planet-like object at the upper left**, including its partial edge and dark surrounding marks. This directly matches the *type* of historical positive control described by Game Detectives. Hash the 1,024 mask bytes in standard row-major MSB-first packed-bit order:

```
SHA256 38e3f2e176277851a059c9a8c9d37cc913e2602e5fc661b71298dbb9ccaf8411
```

**Status:** the 16px sampling **phase** is now independently recovered from the source itself. Neither the CE stickers nor the post-selected `189/252/315` output contributed. The planet scan is reproducible, not a claim that the foreground has been decoded or the original URL recovered. See [deterministic source verifier](../../scripts/conjecture_lab_gate98_phase_replay.py).

## Falsification of CL-04's former 0xCF enthusiasm

CL-04 measured seven nonblack RGB colours `{0,207}³ \setminus {black}`: **612 of 616** occurrences on its *assumed* `(0,0)` 16px lattice appear in the top 64 sampled rows, a **459× difference in vertical regional density**. That statistic is numerically true but **is not evidence of source-native 16px registration**.

We now tested the crucial **matched-region phase control**. On the original pixel image's upper 2048×1024 region, all **255 possible common nonzero amplitudes** `k` for RGB codewords in `{0,k}³` were counted both at `(x mod 16, y mod 16)=(0,0)` and at all **off-lattice** upper-source pixels.

- At amplitude **207**, 612 samples on the old grid versus 148,651 off-grid: grid/off-grid density ratio **1.049842**.
- At amplitude **251**, 394 samples versus 98,232 off-grid: ratio **1.022783**.
- The exhaustive amplitudes 1..255 produce **no strong 16px enrichment** for this codeword family at the old (0,0) phase; other amplitudes have tiny sample counts.

Thus the 207/251 colour-cube observation is consistent with a **regional artwork palette**, not independently recovered hidden marker hues. More importantly, the native black pixel registration is *not* at the earlier origin. This is a material correction of CL-04's implicit claim that (0,0) was a good transcription of the historical sampling phase.

The original positive-control script tested the *same seven-colour 0xCF family* and every six-of-seven subset over upper-left 128×64 cells at phase (0,0); all-seven revealed scattered pixels rather than historical text. That negative is narrow; changing to the newly source-recovered phase and testing genuine historical colour values is the right next operation, not editing the earlier results.

[Source-only all-amplitude forensic script](../../scripts/conjecture_lab_gate98_all_amplitudes.py), [archival positive-control candidate overlay script](../../scripts/conjecture_lab_gate98_positive_control.py). Neither refers to CE completions.

## Re-evaluate the CE address hypothesis at the actual phase

After recovering phase (4,12), and **without choosing a bank**, we can reuse the previously defined *invented* CL-04 reader: partition all 128×256 sampled points into 64 consecutive row-major 512-site banks, index nine class columns with 9-bit slash=1 addresses, and pick one R/G/B component with each Q4 slash-depth.

The two conditional balanced-tail masters are still exactly the incumbent machine states `0100` and `1100`. On the **correct phase**, exhaustive 64-bank replay yields:

| Frozen readout condition | State 0100 | State 1100 |
|---|---:|---:|
| Most printable ASCII bytes in a 9-byte candidate | **3** | **3** |
| Banks with all nine printable ASCII bytes | 0 | 0 |
| Most exact nonblack `{0,207}³` palette hits | **3** | **3** |
| Most `{0,207,251}³` ternary-palette hits, black included | **7** | **7** |
| Banks with all nine ternary-palette hits | 0 | 0 |

The **native pixel phase** is independently grounded. The 512-site grouping, bank selection, class addressing, R/G/B mapping, use of ASCII, and acceptance of all ternary palette values **are still purely speculative**. The new negative is restricted to this **fixed** candidate implementation, not a universal failure of external-image consumers.

The full 64-bank raw RGB/byte results for both candidates are generated by `scripts/conjecture_lab_gate98_phase_replay.py`, with source-asserted planet scan and exact phase census. This now has an honest source-born origin, with the remaining invented operations kept visibly separate.

## Historical target still open: the shutdown-protocol text

The recovered planet scan supports the documented sampling *mechanism* and supplies a uniquely derived **orientation, offset and pixel scale**. It does **not** recreate the entire original *2018 layered-colour text*, because we still lack the six exact colours and, possibly, separate image-plane registration.

Highest-value follow-up: locate a contemporaneous source screenshot of the six colour isolations or a solved output image, recover **their exact hexadecimal RGB selection values** and bounds, and replay the phrase **without tuning to its known letters**. Prefer sources dated in 2018 or directly preserved in historical ARG repositories. We should also inspect which sampled image regions carry a complete colour text once colour labels are fixed, without leaking expected letters into selecting offsets.

The source is pre-CE. Even a fully successful *historical* replay would establish an authentic Playdead puzzle mechanism that might inspire an extra CE step; it still would not establish stickers as the key to gate-98. Conversely, the sticker-background `534brn` page remains the stronger same-object destination.

## Frozen status

- **Positive historical control:** black 16-grid phase and planet-like image recovered independently.
- **Negative**: amplitude-207 palette is not specially concentrated on (0,0) 16px coordinates; its prior upper-area concentration was not a grid test.
- **Negative**: fixed CE 512-bank RGB/ASCII and ternary palettes at independently discovered (4,12) origin still fail complete-read criteria.
- **Unknown**: original six RGB text layers and full shutdown URL replay.
- **Unchanged**: no new sticker observations, no rewritten prospective atlas, no claim of complete foreground decode.

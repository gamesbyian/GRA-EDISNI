# CL-16: complete 2021 LIFE DETECTED acorn-41 overlay replay from authentic source pixels

_9–10 October 2026. Successful source-preservation breakthrough and **independent exact pixel-level replay** of the 2021 historical PC/PS4 printer decoder. This is an original-printer **positive control**, not a newly decoded Collector's Edition sticker foreground._

## The original demonstration was actually preserved

[CL-13](2026-10-09-cl13-2021-acorn-overlay-provenance.md) had recovered the 25 June 2021 #tldr report that user `4987372` discovered a way to derive `LIFE DETECTED` from the previously guessed PC/PS4 password: standard seven-cell Conway Acorn generation 41, placed against the previously known 'running man' image. The historical Discord attachment URL `.../857907060334919700/acorn.mp4` now responds with **HTTP 404**, verified with a bounded one-shot [archival CDN run 38025078818](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38025078818). That negative is about the live CDN path only, not disappearance of all archived source.

Instead, the full **2,690-entry `assets/` tree** in the original public primary archive `gamesbyian/playdead-unofficial-exports`, tree SHA `4eb26bc0cba73425dc5ed7d03f1d4ba78fee929e`, contains:

* `assets/acorn-c53ef409753e9fa2.mp4`: 408,693 bytes, original Git blob `0480da448164c0a1bbd115f1065ffd9d68f70bf2`;
* `assets/Inside_pc_acorn_fixed-081372579ea1409c.png`: 8,234 bytes, Git blob `c04ac01fc6f3f3af05d00f7e2b104396ade440e1`, a 351×351 presentation of the 32×32 historical printer raster;
* multiple `RunningMan` screenshot/working files; these are **documentation/editing representations**, not automatically equivalent to the running human printed outside the cover window;
* `assets/SPOILER_acorn_solution_hidden_message-d83e87eda3958d3f.gif`: despite its misleading name, it is an unrelated animated joke, **not** the source of the proof.

A [single bounded source-tree-acquisition run 38025192150](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38025192150) retrieved nine exact source-named files. All nine matched the **original Git blob SHA1 and byte-size evidence** with zero substitution. Run artifacts preserve the raw MP4 and PNG files (30 days), plus lightweight previews. The video has **628 frames, 512×512 at 33.33 fps, ~18.84 seconds**. It demonstrably records Acorn generations 0→41, placement of the generated binary mask into the PC/PS4 red/blue/orange image, recolouring of the selected pixels, and `LIFE DETECTED` in orange on blue. This is the actual reported 2021 decoding demonstration.

The source file can be independently located at [upstream archived video](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/assets/acorn-c53ef409753e9fa2.mp4), retaining its Git content identity. Do **not** call it a new-original 2026 clip.

## Exact native recipe extracted from the recovered video

The independent pre-2021 printer fixture is the project's existing [canonical 2018 acorn row order](../../data/printer-reference/pc-ps4-acorn-order.txt), 32 full rows × 32 symbol sites, with original source characters:

| Original symbol | Historical colour | Number in the 32×32 grid |
| --- | --- | ---: |
| `/` | Red | **308** |
| `-` | Blue | **613** |
| `.` | Orange | **103** |

The archived 351×351 bitmap presents the same 32×32 lattice in these fixed colours, allowing a completely independent test against the video.

1. Use the **standard seven-live-cell Acorn**, B3/S23, seed `bo$3bo$2o2b3o!`. Evolve exactly **41 generations**. The resulting 102 live cells occupy a **30×15** bounding box, a standard mathematical result reproducible without reading the 2021 answer.
2. Register that box on the **32×32 original printer image** with zero-based upper-left at **(x=1, y=16)**, hence source columns **1 through 30** and rows **16 through 30**, leaving one margin cell at left, right and bottom. These are the original video's coordinates, **not** registration parameters fitted to CE sticker outputs. The video frame around index 200 displays exactly **102 masked sites**, and its mask **equals all 102** generated Acorn-41 positions, zero discrepancies.
3. With `M(x,y)` denoting membership in the 102-site mask and `S(x,y)` the *original* printer mark, display an orange output pixel exactly when:

   ```text
   (not M and S == '.')   OR   (M and S == '-')
   ```

   In words: the mask covers/removes **52** original orange-dot pixels; **39** originally blue-dash pixels under the mask are recoloured orange; the **11** original red-slash sites under the mask do **not** become orange. **51** original orange-dot pixels remain outside it, and **39** new orange pixels appear inside it.

4. Hence the final output has exactly **51 + 39 = 90 orange pixels**. Isolate that channel on a blue 32×32 field. It spells:

   ```text
   LIFE
   DETECTED
   ```

5. Verify against the source video final 512×512 frame (around index **565**): at the centre of each 16×16 cell, its orange mask has **90** sites. Our independently computed 90-site output and the video have **90 identical sites, zero missing, zero extra**. The frozen 32×32 ASCII mask with `#` for final orange and `.` otherwise, joined with newline including a final newline, has SHA256:

   ```text
   38ea14a45bffbd735cec104cad5ba0499bbb36163bc3c2bf0b9cf250b773bd6d
   ```

This is a **strict full-output match**, not a visually approximate resemblance, an English dictionary fit, a post hoc orange threshold search, or a guessed completion of missing CE marks. The frame palette sample uses a fixed orange-channel predicate `red>180, 45<green<180, blue<70` on the 32×32 video centres. Both the 102-site Life mask and the 90-site plaintext mask are independently checked against frames from the source-authentic preserved video. See the exact [machine-readable evidence fixture](../../data/historical-2021-acorn-41-overlay-positive-control.json).

The formula can be interpreted as a **ternary-gated two-layer selection**, rather than a generic global XOR: source **dot** survives only outside the Life mask, source **dash** becomes orange only inside it, and source **slash** is never shown as orange. There is no claim that dash/slash/dot should be assigned the same roles for the CE foreground.

## Reproducibility

Source-checked full decode, using only the already archived 2018 text row-order fixture:

```sh
python scripts/verify_historical_acorn_41_full_overlay.py
```

Optional independent video confirmation from a 512×512 PNG frame near source video index 565:

```sh
python scripts/verify_historical_acorn_41_full_overlay.py \
  --video-final-frame /path/to/recovered-video-frame-565.png
```

The older `scripts/verify_historical_acorn_41_life.py` remains the **mathematical-seed-only** control. The new source-to-text verifier is added to CI, with the output bitmap SHA pinned to the independently read original video frame rather than generated letters. If CI finds a distinction between the 2018 canonical row-order text and the separately archived fixed-image raster, that must be investigated as a legitimate source-identity problem, not concealed by replacing the source fixture.

## What this changes and what it does not

This closes the prior CL-13 note that generation 41 alone could be reproduced but the original `LIFE DETECTED` overlay could not. The actual historical operation now has **all six necessary typed ingredients**:

* original clue (acorn + printed 41);
* uniquely named generative process (Conway B3/S23);
* exact parameter 41;
* fixed 32×32 receiver (original PC/PS4 printer art, often called running-man graphic);
* exact native mask registration (1,16);
* exact palette/readout rule, yielding a checkable 90-site phrase.

The key clarification is that the **receiving artwork is the historical PC/PS4 printer's own 32×32 acorn/running-man image**, as directly shown by the video. It should not be casually described as a proven *third unrelated game artifact* or as the tiny three-dimensional running figure on the 2019 reversible cover. The original source can carry an image, an instruction and the eventual answer simultaneously.

For CE sticker revival, this gives an unusually high-quality positive control for a plausible *type of puzzle*. It **does not** validate the previous 4/9/(9+3) rail interpretation, GHI XOR selection (whose own matched null was 12.645%), an 81/27 overlay rule, or any transformation on the damaged `534brn` page. A credible CE analogue must identify an **independent native carrier/mask/parameter** and a checkable output before applying graphics until a word appears.

Related cover thesis [CL-14](2026-10-09-cl14-cover-acorn-historical-clue.md) is stronger in the sense that the source-acorn and visible running-person juxtaposition are now physically verified; it is **still not demonstrated** that the tiny scene person encodes this 32×32 running-man graphic or that the cover's complete purpose is resolved.

**Disposition: original 2021 historical puzzle decoder reproduced exactly; CE puzzle unsolved; no CE evidence changed.**

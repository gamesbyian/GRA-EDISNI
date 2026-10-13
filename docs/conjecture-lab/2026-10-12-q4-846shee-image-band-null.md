# Native Q4 against masked A–I background artwork: three-band falsification (12 October 2026)

**Mode: DISCOVER with adversarial class-permutation control.** Script: [`conjecture_lab_q4_tile_band.py`](../../scripts/conjecture_lab_q4_tile_band.py). Verified on the actual image files in [GitHub Actions run 38332272594](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38332272594), which preserves the full measurements and exact-null histograms in the `native-q4-tile-band-null` artifact.

## Independent visual input and its limits

The repository preserves an original community composite, `846shEE.jpg`, and nine 512×512 A–I tiles extracted from that particular historical image under `artifacts/background-tile-evidence-masters/`. Per-tile `*-known-mask.png` files and RGBA alpha identify directly visible pixels, excluding the removed large foreground symbol and A–I text. The surviving observable-pixel fractions are about 70–80%, and no occluded texture is synthesized. Source description: [`artifacts/background-tile-evidence-masters/README.md`](../../artifacts/background-tile-evidence-masters/README.md).

This is **one historical community composite**, not an independently authenticated original artwork print master or nine separately scanned copies. It is suitable for bounded exploratory pixel comparisons but cannot establish authorial intent.

The hypothesis assumes that the Q4 depth selector `D[j]` might point at the top, middle or bottom visual third of each same-class tile. No known source tells us to divide these 512-pixel tiles into three equal bands; this is a speculative receiving operation. The recorded observed Q4 choices are `A=012, B=2, C=012, D=1, E=0, F=1, G=02, H=2, I=2`.

## Frozen operations before reading results

For each original A–I tile, compute mean continuous pixel darkness `255 - (299R+587G+114B)/1000` separately over three equally divided horizontal or vertical bands. Count only pixels simultaneously accepted by RGBA alpha and the original known-pixel mask (both at least 128). Divide by the number of eligible pixels in that band; do not substitute invented texture for missing evidence.

Test four fixed rules:

1. Choose the horizontal third with maximum observed mean darkness.
2. Choose the horizontal third with minimum mean darkness.
3. Choose the vertical third with maximum mean darkness.
4. Choose the vertical third with minimum mean darkness.

A fifth **coverage-only negative control** selects the horizontal band with greatest directly observed-pixel fraction, without examining darkness. Exact ties choose the smallest depth. Score a rule as the number of A–I predicted band indices falling within that class's *allowed Q4 depth set*.

For every rule, enumerate all **9! = 362,880** permutations of assigning the nine original tile predictions to the nine fixed A–I selector roles. Report the one-sided null fraction of shuffled assignments with at least as many class matches. Also compute the **best of four readers on the same permutation**, preserving their dependence and calibrating the fact that four ways to read the image were inspected. This is an exact class-label randomization diagnostic, not an independent probability model of Playdead puzzle design.

## Observed results

| Reader | Predicted depth indices A–I | Matched Q4 classes out of 9 | Matched-label shuffle tail |
|---|---|---:|---:|
| Horizontal darkest | `000021010` | 4 | **74.206%** |
| Horizontal lightest | `222110202` | 6 | **35.714%** |
| Vertical darkest | `220200020` | 6 | **28.571%** |
| Vertical lightest | `002011112` | 4 | **76.508%** |
| Coverage-only control | `220000002` | 6 | **19.048%** |

**Four-reader maximum = 6 matching classes; exact familywise shuffle tail = 70.529%.** Two apparently reasonable six-class matches are completely unexceptional after accounting for class-label ordering and the four attempted operations. Even the coverage-only control gives six, showing how easy moderate apparent agreement is on this fixed mask.

All five rules and the familywise result ran successfully, not merely proposed. The JSON artifact includes the per-image per-band darkness averages, observed-pixel coverage fractions, predicted band choices, null distributions and score frequencies.

## Interpretation and next direction

This **lowers priority for darkness/lightness-band readings of the Q4 selector** on the historical A–I artwork. The model is not rescued by cherry-picking the best of the four readings.

It does not falsify the 18 Q4 selector assignments, the binary-primary 364-mask family, finer-grid artwork coordinates, multi-layer masks, the nine-sketch physical poster, the damaged Terminal41 receiving image, or the technically possible Steam branch-password destination. These are different fixed operations, not mere parameter settings of the rejected band-reader.

Given this negative, further continuous tuning of band widths, intensity thresholds, image flips or colour channels against the **same** nine masks would carry substantial look-elsewhere cost and little new information. The productive next step is a new, authored external geometry/overlay cue or pixel evidence from an actual different physical source. For an alternative image operator, declare transform, degrees of freedom and null design *before* inspecting matches.

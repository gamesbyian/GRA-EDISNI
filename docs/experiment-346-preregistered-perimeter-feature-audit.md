# Experiment 346 — preregistered replicated perimeter-feature audit

_Status: completed; preregistration frozen before analysis, 30 Sep 2026._

## Question

Experiment 344 established that 35 original sticker photographs preserve a usable physical perimeter, with at least two independent photographs in every A–I class. Experiment 346 asks the next narrow question: **is there a stable edge-localized signal that replicates across independent photographs of the same background class?**

This experiment is deliberately blind to foreground-machine predictions. It does not choose an ordering, polarity, threshold, edge location, or feature because it agrees with POS3, Q4, the frozen row-selector rival, Experiment 345's optimized row order, or any predicted unseen sticker.

## Frozen corpus

Use exactly the 35 rows marked `usable` in `data/perimeter-support-exp344-photos.csv`. No failed Experiment-344 photograph may be promoted after looking at results.

## Frozen rectification

Re-detect the sticker quadrilateral with the same detector used by Experiment 344 and rectify it to a 512×512 square by the existing `warp_sticker` projective transform. If a previously usable photograph changes Experiment-344 usability status, stop and report corpus drift rather than substituting another photograph.

## Frozen measurement bands

Measure four inward bands, expressed as fractions of rectified sticker width:

- 0–2%
- 2–4%
- 4–8%
- 8–16% control band

Treat top, right, bottom, and left separately. Corners are excluded by removing the outermost 10% of each side's longitudinal span at both ends.

For each side/band, convert to grayscale and average across band thickness to produce one longitudinal profile. Subtract that profile's median, divide by its MAD (fixed epsilon `1e-6` only to avoid division by zero), and linearly resample the longitudinal profile to 256 bins. Profiles are compared in the rectified image's fixed top-to-bottom / left-to-right orientation; no side reversal is optimized.

## Primary statistic

For every pair of independent usable photographs within the same A–I class, compute Pearson correlation of each normalized side/band profile.

For each class:

1. compute the median pairwise correlation for every side/band;
2. define the **perimeter replication score** as the median of the 12 side/band medians from 0–2%, 2–4%, and 4–8%;
3. define the **control replication score** as the median of the four 8–16% side medians.

The primary experiment statistic is the median of the nine class perimeter replication scores.

A candidate perimeter signal requires all of the following without retuning:

1. positive perimeter replication score in at least 7 of 9 classes;
2. perimeter replication score greater than control replication score in at least 7 of 9 classes;
3. the pooled within-class perimeter correlation distribution has a higher median than the same-side/same-band between-class null distribution;
4. the primary experiment statistic remains positive after removing any one physical side in turn;
5. the primary experiment statistic remains positive after removing any one photograph in turn.

These conditions are deliberately conservative and are evaluated exactly as written.

For numerical edge cases, a constant/near-constant profile has correlation 0 rather than NaN. In a single-photo jackknife, if removing that photograph leaves its A–I class with fewer than two photos, that class is unscored for that jackknife replicate; the experiment statistic is the median of the remaining scorable classes. No replacement photograph is introduced.

## Nulls

Two nulls are frozen:

1. **between-class label null:** preserve photograph, side, band, and profile, but compare only cross-class photo pairs;
2. **registration null:** circularly shift the second longitudinal profile by exactly 32 of 256 bins before correlation.

Report effect sizes and the full distributions. The registration null is descriptive: the candidate channel is strengthened if the aligned within-class median exceeds the shifted within-class median, but this is not an additional pass/fail gate.

## Stop rules

A negative result closes this specific replicated grayscale edge-profile channel. Do not respond by changing band widths, corner exclusions, profile resolution, normalization, side orientation, polarity, or class grouping.

A positive result licenses a separate follow-up to localize and characterize the replicated physical feature. It does **not** by itself license decoding, foreground ordering, or machine-model interpretation.

## Relationship to prior work

Experiment 325 showed that consensus masters cannot test the physical sticker perimeter. Experiment 344 removed that observability block using original photographs. Experiment 345 showed that the foreground rows do not self-select a useful permutation under a simple continuity metric. Experiment 346 therefore tests the historically better-motivated possibility that a separate physical edge channel could supply ordering/check-bit information.


## Result

The preregistered candidate channel fails **all five gates**.

| measure | result |
|---|---:|
| primary median of nine class perimeter scores | -0.071084 |
| classes with positive perimeter replication | 2 / 9 |
| classes with perimeter > interior control | 3 / 9 |
| pooled within-class perimeter median | -0.052606 |
| pooled between-class perimeter median | +0.019691 |
| 32-bin shifted within-class median | +0.008437 |

Only C (+0.1998) and G (+0.1742) have positive class perimeter scores. The other seven are negative.

All four side-deletion jackknives remain negative, from -0.0943 to -0.1227. Every one-photo deletion jackknife also remains negative, with the primary statistic ranging only from -0.0803 to -0.0508. The failure is therefore not carried by one badly registered side or one photograph.

The between-class null is especially informative: unrelated A-I classes correlate slightly **more** strongly than repeated photographs of the same class under this frozen edge-profile representation. The shifted-registration null also exceeds the aligned within-class median. There is no evidence here for a stable registered grayscale edge feature.

## Interpretation

This closes the specific PC-printer-style candidate in which the recoverable physical sticker perimeter itself carries a replicated grayscale profile or check-bit pattern visible under the preregistered bands.

Do **not** retune band widths, reverse individual sides, change normalization, select only C/G, or choose photographs after seeing this result.

Experiment 345's scrambled-row hypothesis therefore still requires an independent ordering cue, but Experiment 346 removes the most direct physical-perimeter implementation currently licensed by the archive. Reopen perimeter decoding only if an independent clue identifies a different measurable feature class, such as a particular printed mark, color channel, packaging feature, or known registration convention.

The exact compact result is preserved in `data/experiment-346-perimeter-feature-audit.json`. Full pairwise output is preserved by workflow run `36809370081`, artifact `11138831699`, digest `sha256:82a621af6881f06b99bad3cdd908264c28f0feeb35fbea94636b03f0e51a92a5`.

# Experiment 345 — preregistered replicated perimeter-feature audit

_Status: preregistered; analysis not yet run._

## Question

Experiment 344 established that 35 original sticker photographs preserve a usable physical perimeter, with at least two independent photographs in every A–I class. Experiment 345 asks the next narrow question: **is there a stable edge-localized signal that replicates across independent photographs of the same background class?**

This experiment is deliberately blind to foreground-machine predictions. It does not choose an ordering, polarity, threshold, edge location, or feature because it agrees with POS3, Q4, the frozen row-selector rival, or any predicted unseen sticker.

## Frozen corpus

Use exactly the 35 rows marked `usable` in `data/perimeter-support-exp344-photos.csv`. No failed Experiment-344 photograph may be promoted after looking at results.

## Frozen rectification

Re-detect the sticker quadrilateral with the same detector used by Experiment 344 and rectify it to a 512×512 square by a projective transform. If a previously usable photograph no longer yields the same fail-closed geometry classification, stop and report corpus drift rather than substituting another photograph.

## Frozen measurement bands

Measure four inward bands, expressed as fractions of rectified sticker width:

- 0–2%
- 2–4%
- 4–8%
- 8–16% control band

Treat the four physical sides separately. Corners are excluded by removing the outermost 10% of each side's longitudinal span at both ends.

For each side/band, convert to grayscale, subtract that photograph's band median, divide by its MAD (with a fixed epsilon only to avoid division by zero), and resample the longitudinal profile to 256 bins. This normalization is fixed before any class-conditioned inspection.

## Primary statistic

For every pair of independent usable photographs within the same A–I class, compute Pearson correlation of each normalized side/band profile. The primary class statistic is the median pairwise correlation. The primary experiment statistic is the median of the nine class medians.

A candidate perimeter signal requires all of the following without retuning:

1. positive replication in at least 7 of 9 classes;
2. the 0–8% perimeter bands replicate more strongly than the 8–16% interior control in the same side/class comparison;
3. within-class replication exceeds a between-class null formed by pairing photographs from different A–I classes on the same side/band;
4. the result is not carried by a single side or a single photograph.

## Nulls

Two nulls are frozen:

1. **between-class label null:** preserve photograph, side, band, and profile, but compare only cross-class photo pairs;
2. **registration null:** circularly shift one longitudinal profile by 32 of 256 bins before correlation. This tests whether any apparent replication depends on physical registration rather than broad brightness/texture.

Report effect sizes and the full distributions. Do not convert exploratory thresholds into significance claims.

## Stop rules

A negative result closes this specific replicated edge-profile channel. Do not respond by changing band widths, corner exclusions, profile resolution, normalization, side ordering, polarity, or class grouping.

A positive result licenses a separate follow-up to localize and characterize the replicated physical feature. It does **not** by itself license decoding, foreground ordering, or machine-model interpretation.

## Relationship to prior work

Experiment 325 showed that consensus masters cannot test the physical sticker perimeter. Experiment 344 removed that observability block using original photographs. Experiment 345 is the preregistered feature test that those results explicitly called for.

# CX-E: 4×27 slash rails calibrated against two observed-mask nulls

_9 October 2026. Exploratory revisit of the 4×27 foreground representation (older Experiment 433). Code: [exact non-Monte-Carlo rail calibration](../../scripts/conjecture_lab_cx_e_rail_nulls.py). Physical source: [observations.csv](../../data/observations.csv), 84 records representing 66 distinct H108 residues. **No new sticker observation, code master, solved message or source-native decoder is claimed.**_

## Why test this?

The original independent revival review highlighted two columns that remain slash under all four consecutive 27-site quarters. Hypothesis CX-E is that such slash rails could delimit an instruction/noise boundary, act as alignment marks, or indicate repeated readout positions. Before using them to choose a mapping, establish exactly how much of the phenomenon is *physically observed* and how unusual it is under matched alternatives.

## Observation-only audit

Reshape residue numbers 1–108 in **serial order** as four rows of length 27; unknown physical cells are `?`. For reading convenience, the following lines split every nine positions; the splits themselves do not use guessed completions.

```text
Q1  ?/--/?/?/ | -?-/-/?/- | -/-?--?-?
Q2  ?//-/???/ | -///?//-? | ///??-?-?
Q3  ?/-?//??/ | ?//??/--- | ?--/?////
Q4  ???./??.. | ?.??./..? | ?/?.????/
```

Observed counts per quarter: Q1 **19 observed / 8 slashes**, Q2 **17 / 12**, Q3 **18 / 12**, Q4 **12 / 4**. Across these 66 distinct physically observed sites, only **five** 1-based columns have all four sites known: **5, 9, 15, 17, 20**.

| Column | Q1 Q2 Q3 Q4 marks | Direct all-slash? |
| ---: | --- | --- |
| **5** | `////` | Yes |
| 9 | `///.` | No |
| **15** | `////` | Yes |
| 17 | `/--.` | No |
| 20 | `//-/` | No |

The remaining **22 columns cannot be called non-rails** because they contain at least one unknown physical mark. Similarly, `////` has different semantic status here from a model-completed four-slash column. This is an observed pattern, not a causal explanation.

## Exact null A: quarter-wise observed-count shuffle

Retain the actual 66-position observation mask. Independently shuffle labels within the *observed cells only* of each quarter, preserving each quarter's observed slash count. Treat the five fully observed columns as candidate four-slash rails. The event of interest is **at least two** such columns, irrespective of which columns they are.

Let `M_q` be observed sites and `K_q` observed slashes for each quarter. For any fixed `k` of the five columns to be all slash, the probability is `p_k = ∏_q (K_q)_k / (M_q)_k`, where `(n)_k` is the falling factorial. Inclusion-exclusion for at least two successes is `Σ_{k=2}^5 (-1)^k (k-1) C(5,k) p_k`.

**Exact results:**

* Any two or more complete columns all slash: **0.0293474512065495** (2.9347%).
* Specifically columns 5 and 15 designated *before seeing any marks*: **0.00311621036443473** (0.3116%). That is a *counterfactual preselection*, **not** a valid post-hoc p-value here.

This simple model does not preserve historical 3×3 frame grammar, so it should be a baseline, not the last word.

## Exact null B: conditional 3×3 frame and one-slash-per-class tail grammar

A second more structured reference model deliberately grants two conjectural regularities without taking the actual slash *positions* as fixed:

1. **First 81 cells:** each of nine 3×3 frames contains one minority mark in each of the three vertical columns; polarity may be slash-minority or dash-minority. Enumerate 27 configurations per polarity. Condition on each frame's count of slashes at the real observed-site mask, **not the observed symbol positions**. Compatible option counts in Q1/Q2/Q3 order are **12,12,6 / 9,12,16 / 9,12,12**.
2. **Final 27 cells:** each of the nine A–I picture classes has **exactly one slash across its three tail occurrences**, not one slash in each three-site column *within* a nine-mark tail frame. Enumerate all `3^9 = 19,683` placements; retain the **720** that reproduce the observed slash counts `1,1,2` across the three tail rows at observed positions. This is a **conditional U2-style tail grammar**, not proof from physical cells.

Choose uniformly among local configurations within each body frame, uniformly among the 720 tail configurations, and independently combine them. A 32-state DP over the five fully observed columns gives exact rational probabilities, without filling unknown physical H108 cells in the experiment's input.

**Exact results:**

* Any two or more fully observed columns all slash: **0.0486894772376543** (4.8689%).
* The hypothetical prospectively specified pair 5 and 15: **0.00486111111111111** (0.4861%).

**Important typing warning:** Extending the *body's* one-minority-per-vertical-stack grammar to each of the three Q4 rows would be a mistake. Q4 uses a different cross-row **same-class** domain. For instance Q4 frame 2's local positions 2/5/8 are all observed dots, so they cannot accommodate an additional mandatory slash minority in that within-frame stack. The conditional tail generator deliberately uses the correct across-row class domain. This is the same domain-discipline issue stressed by Experiment 319 and SR-04.

## Interpretation and scope

Both tests leave the two actual rails intact. The higher structural-null probability suggests they are **not exceptionally rare even under a deliberately structured interpretation**. Neither calibration accounts for the project's considerable exploratory search across 12×9, 9×12, 4×27, cube rotations, transformations and other rail definitions, nor for the fact that columns 5/15 were picked after seeing the data.

Thus **neither nominal 2.9% nor 4.9% is evidence of an intentional metapuzzle delimiter at a conventional significance level**. The missing 22 columns are explicitly unresolved; future physical observation can change the number of fully observable columns or show additional rails. Even a later exact match requires a **consumer** explaining why a slash-only column means a command boundary rather than a source-census regularity.

## Three finite continuation proposals

* **R1: boundary/sentinel readout, DEVELOP.** Assume columns 5/15 partition each quarter into fields; derive exact field lengths and one human-readable decoder *without using an output to pick the orientation*. A corresponding authentic printer/cover source must later specify why these boundaries matter. Pair with SR-04's one-shot tail rather than automatically requiring recursion.
* **R2: physical-fold or image-overlay registration, DEVELOP.** Treat the rails as two fiducials and ask whether their 10-column separation and nontrivial 27-column width match a *measured*, not invented, receiving artifact. A fixed original screenshot with exactly these landmarks would be a prospective discriminator.
* **R0: control.** In most null configurations no fully observed columns are four-slash. Future discoveries should be scored on the original five-column result and subsequently observed columns separately, with selection timing preserved. Do not treat 22 unknown columns as observed failures.

**Disposition:** Observed rails are real and worth a brief conditional walkthrough, but the first controlled calibration places CX-E below authenticated-source retrieval for damaged `534brn` and the cover. Do not use this nominal frequency to pick a decoded word or claim confirmation.

## Reproduce

```sh
python scripts/conjecture_lab_cx_e_rail_nulls.py
```

The script reads the current observation ledger, rechecks duplicate-residue consistency, prints the full observed matrix and derived column census, and computes both nulls exactly using Python `Fraction`. It does not write to the observations corpus, update a completion model, or modify a physical prediction.

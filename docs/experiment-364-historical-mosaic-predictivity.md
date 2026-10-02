# Experiment 364 — historical 3×3-mosaic predictivity audit

_Status: completed, 2 Oct 2026._

## Why this experiment exists

After Experiment 360 showed that freely optimizing row order in 9×12 or 12×9 does not improve held-out sticker guessing, the remaining high-value ordering question was the historically distinct Dec-2022 proposal summarized in the reset notes as:

> “rearranging the top 9×9 grid to account for the repeating pattern”

The archived source and its attachments now make that operation concrete.

## Primary historical reconstruction

Source:

- `gamesbyian/playdead-unofficial-exports`
- `Playdead Unofficial - ARG - solving [461275582970462209].txt`

Relevant chronology:

- **23 Dec 2022 20:57:** a solver notices that the repeat “doesn’t actually start on sticker 0, but sticker 1”;
- **21:01:** attachment `assets/image-00e6b7e6bbd4638f.png` shows the first nine sequence rows with the repeating background order labelled `I A B C D E F G H`;
- **21:24:** “rearranging the top 9x9 grid to account for the repeating pattern got me this”, attachment `assets/image-a6a790f9807f3e47.png`;
- **21:28:** “the entire grid”, attachment `assets/image-e272a602e0c11f7a.png`;
- **21:46:** the same solver explicitly considers “each 3x3 grid image per row”.

The screenshots identify the transform unambiguously:

1. each consecutive 9-sticker sequence row is read in background order `I,A,B,C,D,E,F,G,H`;
2. those nine cells are reshaped into the solved background geometry:

```
I A B
C D E
F G H
```

3. the twelve resulting 3×3 tiles are laid out three tiles across and four tiles down;
4. the first nine slash/dash tiles therefore form the 9×9 top block, and the final three slash/dot tiles form the 9×3 strip beneath it.

This is the collective version of the twelve-square representation later treated in Experiment 348. It is **not** a free row permutation.

## Question

Does this independently specified historical mosaic make unknown foreground cells easier to infer from local 2D continuity?

That is the practical value claim behind the current community suggestion: if the intended arrangement is closer to the real image geometry, missing cells should become easier to guess from nearby cells.

## Frozen input and prediction rule

Use only `data/observations.csv`.

For every one of the 65 known H108 residues:

1. hide that observation;
2. map all remaining observations into the exact historical 12×9 mosaic;
3. inspect orthogonally adjacent known cells;
4. discard neighbors from the other alphabet region (slash/dash versus slash/dot);
5. predict the strict local majority if one exists; otherwise abstain.

Two neighborhood scopes are reported:

- **all mosaic neighbors:** all orthogonal neighbors in the 12×9 collective mosaic;
- **within-tile only:** ignore neighbors that cross a 3×3 tile boundary.

The comparison baseline is the same deliberately weak alphabet-majority control used in Experiment 360:

- residues 1–81 → `/`;
- residues 82–108 → `.`.

No machine completion, POS3, frame polarity, semantic target, or optimized ordering enters the test.

## Results

| neighborhood | predictions | correct | accuracy | baseline on same cells |
|---|---:|---:|---:|---:|
| all historical-mosaic neighbors | 46 / 65 | 19 | 41.30% | 28 / 46 = 60.87% |
| within the same 3×3 tile only | 47 / 65 | 21 | 44.68% | 29 / 47 = 61.70% |
| cross-tile neighbors only | 26 / 65 | 11 | 42.31% | 14 / 26 = 53.85% |

The larger mosaic therefore provides no useful same-symbol interpolation signal. Restricting to the individual 3×3 tile improves slightly, but remains well below the trivial baseline.

## Interpretation

This closes a specific ambiguity in the reset history.

The Dec-2022 “rearranged 9×9” proposal is now reconstructed exactly and should no longer be described as an unspecified row-order hypothesis. It is the deterministic twelve-frame spatial representation:

```
one 9-sticker row
    ↓
I A B
C D E
F G H
```

repeated twelve times and tiled as a 3×4 array.

That operation is genuinely useful historically because it independently establishes the 3×3 frame domain later exploited by Experiments 348–352.

What it does **not** supply is a smooth bitmap-like neighborhood channel for guessing missing foreground symbols. Cross-frame adjacency is especially unhelpful.

So the productive information in the historical mosaic is **frame-internal combinatorial structure**, not large-scale visual continuity. This is consistent with the later positive results:

- Experiment 348: common frame census narrows to 3/6 or 4/5;
- Experiment 349: chronological evidence favors 3/6;
- Experiment 350: one-per-column occupancy gains predictive support inside the 3/6 family.

Future “image/order” work should therefore avoid treating the collective mosaic as a conventional smooth image unless an independent clue specifies another visual statistic.

## Reproducibility

Run:

```bash
python scripts/audit_historical_mosaic_predictivity.py
```

The script writes `data/experiment-364-historical-mosaic-predictivity.json`.

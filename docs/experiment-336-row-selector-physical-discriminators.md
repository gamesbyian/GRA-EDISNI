# Experiment 336 — prospective physical discriminator expansion

_Status: completed operationalization, 30 Sep 2026._

## Purpose

Experiments 329–335 leave one genuinely useful prospective output from the frozen row-selector family:

```
C tail = ../
```

Residue 93 is already dot in the incumbent. The discriminating cells are therefore:

```
84  = .
102 = /
```

This experiment turns those H108 residues into physical sticker serials for acquisition work.

## Serial expansion through 600

Because foreground symbols repeat on H108:

| H108 residue | frozen row prediction | physical serials <=600 |
|---:|---|---|
| 84 | dot | 84, 192, 300, 408, 516 |
| 102 | slash | 102, 210, 318, 426, 534 |

None of those ten exact physical serials is currently in `data/observations.csv`.

So there are **10 concrete physical sticker numbers** that can directly test the frozen rival without any new interpretive rule.

## Falsification rule

Freeze this before inspecting any future foreground:

- any provenance-backed **slash** at residue 84 falsifies the frozen row-selector family;
- any provenance-backed **dot** at residue 102 falsifies the frozen row-selector family.

An agreeing observation is prospective support for the frozen rival, but it does not by itself identify one incumbent hidden state because the broader incumbent physical family also carries gauge freedom.

## Acquisition use

When any of these serials appears in a video, auction, owner report, photograph, or archive:

```
084 102 192 210 300 318 408 426 516 534
```

record the serial and freeze the expected symbol **before** inspecting the foreground.

These should be tagged as **cross-family discriminator** leads in addition to their existing incumbent-matrix role.

## Machine-readable freeze

Canonical rival definition and predictions are stored in:

`data/frozen-row-selector-predictions.json`

This file is deliberately separate from `data/unobserved-sticker-predictions.csv`. The latter remains the incumbent prediction matrix; the new file records an alternative family and must not silently modify incumbent confidence tiers.

## Reproducibility

```bash
python scripts/expand_row_selector_discriminators.py --max-serial 600
```

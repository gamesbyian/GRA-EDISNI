# Experiment 335 — bounded Pigpen semantic search-space audit

_Status: completed anti-fishing audit, 30 Sep 2026._

## Question

Experiment 334 leaves 16 globally coherent conventional Pigpen A–R codebooks. The observation-compatible 3x3x2 tokens are still incomplete for five of nine classes.

Before anyone starts looking for "interesting words", quantify how many strings the current evidence already permits.

## Result

The per-class token counts from Experiment 332 multiply to:

```
9 × 1 × 1 × 5 × 1 × 2 × 5 × 2 × 1 = 900
```

Because each Experiment-334 codebook is a bijection on the 18-token carrier, each codebook yields exactly **900 distinct nine-letter A–R strings**.

Across all 16 orientation/polarity codebooks:

```
16 × 900 = 14,400
```

The exact enumeration finds:

- **14,400 unique nine-letter strings**;
- **zero collisions between codebooks**;
- only **4 of 9 letter positions fixed** within any one codebook.

## Interpretation

This is a large multiple-comparisons trap.

At the present evidence level, searching these outputs for English-looking fragments, ARG vocabulary, names, URLs, or thematic words would effectively select from **14,400 different strings** after the fact.

A visually or linguistically pleasing output is therefore not evidence for Pigpen unless some independent artifact first chooses:

1. the global orientation;
2. the binary grid/polarity assignment;
3. and, ideally, enough unknown token cells to shrink the 900 completions.

This quantifies why semantic fishing is especially dangerous here.

## Consequence

Freeze the conventional Pigpen branch at its structural result:

- 18-state carrier exists under the exploratory row family;
- 16 conventional A–R registrations remain;
- 900 token completions remain per registration;
- 14,400 distinct candidate strings are licensed before any language criterion;
- no X-grid/S–Z family is independently supplied.

Do not run dictionaries or language-model ranking over these strings.

Resume this branch only when a genuinely independent cue reduces the registration or token uncertainty, or when new physical evidence prospectively tests the frozen C-tail prediction.

## Reproducibility

```bash
python scripts/audit_pigpen_semantic_search_space.py
```

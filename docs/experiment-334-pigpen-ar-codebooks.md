# Experiment 334 — bounded conventional Pigpen A–R codebook enumeration

_Status: completed non-semantic enumeration, 30 Sep 2026._

## Purpose

Experiment 332 found a genuine `3×3×2 = 18` carrier inside the frozen row-selector family. That has the same abstract size as the two 3x3 grid families that encode A–R in a conventional Pigpen alphabet.

The next safe step is to enumerate that exact correspondence **without choosing whichever orientation spells something attractive**.

## Frozen mapping family

Use only:

- conventional row-major A–I in one 3x3 grid;
- conventional row-major J–R in the paired grid;
- the eight global D4 rotations/reflections;
- one global binary-layer choice: exceptional slash is A–I or exceptional dash is A–I.

Total:

```
8 × 2 = 16 global codebooks
```

No per-class transforms are permitted.

No language model, dictionary, plaintext score, or expected phrase is used.

## Result

All 16 codebooks remain structurally admissible.

The four observation-fixed tokens B, C, E, and I produce a different `BCEI` letter signature under each of the 16 global codebooks. Therefore the physical observations do not collapse the orientation or binary-layer choice.

This is exactly the ambiguity expected from a geometric alphabet with no external registration cue.

The script also emits, for every codebook, the complete possible letter set for every A-I class given the present unknown cells.

## Interpretation

The 18-state carrier can be mapped cleanly onto conventional Pigpen A–R, but the mapping is under-registered:

- 8 geometric orientations;
- 2 polarity assignments;
- 16 surviving codebooks.

Choosing among them because one produces a nicer-looking string would be semantic fishing.

More importantly, this still covers only A–R. There remains no independently supplied X-grid/S–Z family.

So the bounded conclusion is:

> a conventional Pigpen **subalphabet** is mechanically representable by the frozen row carrier, but the current sticker evidence supplies neither its global registration nor the missing eight-letter family.

## What could legitimately select a codebook?

Only an independent cue, for example:

- artwork orientation that survives Experiment 333's direct-coordinate failure but supplies a directional transform;
- a historically attested solver instruction;
- another ARG artifact explicitly indicating Pigpen orientation/polarity;
- a prospective physical observation that reduces token uncertainty in a way that distinguishes codebooks when combined with such a cue.

A plaintext-looking result is not an independent cue.

## Reproducibility

```bash
python scripts/enumerate_pigpen_ar_codebooks.py
```

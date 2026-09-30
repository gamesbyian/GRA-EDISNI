# Experiment 336 — R3 operation evidence-gate matrix

_Status: completed R3 gating pass, 30 Sep 2026._

## Purpose

The reset imported a useful library of operations that Playdead demonstrably used elsewhere in the INSIDE ARG. That library becomes dangerous if “Playdead used this before” is treated as permission to try every transform.

Experiment 336 converts R3 into an explicit evidence gate.

For each historical operation family, the repository now records whether it is:

- **licensed now** by sticker-native evidence;
- **pending specific evidence** that would supply the missing parameter;
- **closed until cue** because testing it now would be parameter fishing;
- **already tested** in the only currently justified form.

Canonical machine-readable form:

`data/reset-r3-operation-gates.json`

## Currently licensed

### Geometry first, then secondary read

This is the strongest live historical analogue.

Sticker-native support already exists:

- solved `IAB/CDE/FGH` background geometry;
- historically attested 12×9 / twelve-3×3 foreground organization;
- historically independent 9+3 body/index proposal;
- observation-only exact-one-slash tail family.

Allowed work is therefore bounded spatial interpretation with frozen rules and holdout/prospective validation.

What is not licensed is arbitrary background-to-body remapping. Experiment 319 already showed that the A-I geometry does not supply such a bijection.

### Code as operation

The distinct slash/dot tail and historical body/index proposal justify asking whether the tail tells the solver **what to do** to the body.

That licenses simple preregistered operations whose parameters come directly from the one-of-three tail index.

It does not license inventing a richer instruction language after seeing outputs.

## Pending a specific missing bridge

### Boundary-constrained permutation

The PC/acorn precedent is strong, but the sticker equivalent still needs an actual physical boundary channel.

Existing cropped masters cannot supply it. The live dependency is the full-photo perimeter-support audit. If original photos reveal a repeated margin feature, this gate can open.

### Prior-stage output as selector/key

Cross-puzzle selector reuse is historically real.

For the stickers, however, `dat/534brn9653f9j8mmd` is currently a solved background-layer **path/output**, not a demonstrated foreground key.

The damaged artifact behind that path is still being forensically recovered. If its content explicitly supplies an ordering, orientation, numeric selector, or transform instruction, that exact parameter may be tested. Until then, path characters and old ARG answers are not free key material.

### External consumer

Historical ARG endpoints consumed solved-stage values, so a downstream consumer is plausible in principle.

The gate opens only if an external artifact independently exposes an input grammar or structural fingerprint. Terminal `100` alone does not license endpoint spraying.

## Closed until a cue appears

Four operation families are formally closed for now:

- exact-value/class filtering;
- Game-of-Life or other generated transforms;
- poem/text/artwork overlays;
- carrier conversion such as audio/spectrogram.

Each has a genuine Playdead precedent. None currently has sticker-native parameters.

This is an important negative result: these are **not backlog experiments**. They are dormant branches that reopen only when new evidence supplies the missing cue.

## Operational consequence

R3 is no longer an open-ended “replay old ARG tricks” work package.

Its active frontier is narrow:

1. continue frozen geometry/tail-operation families under holdout discipline;
2. complete the physical perimeter audit;
3. recover the damaged 534brn artifact only by exact forensic constraints;
4. inspect genuinely clue-bearing external artifacts for an input grammar.

Everything else stays closed.

## Validation

`scripts/verify_reset_r3_operation_gates.py` checks that every demonstrated operation family has exactly one gate status and that the summary matches the detailed records.

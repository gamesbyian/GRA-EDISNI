# Experiment 328 — one-symbol-as-ink D4 identifiability audit

_Status: completed exhaustive bounded test, 30 Sep 2026._

## Motivation

Experiment 327 rejects the most literal Pigpen reading where both slash and dash are ink strokes of one glyph. The cheapest surviving categorical alternative is:

> one body symbol means "ink/occupied" and the other means "empty".

Before comparing anything to letters, ask whether the current observation corpus even identifies stable 3x3 shapes under the allowed D4 rotations/reflections.

## Method

For each A-I nine-cell body:

1. keep every physically observed slash/dash fixed;
2. exhaust every binary completion of `?` cells;
3. map slash=1, dash=0;
4. quotient completed 3x3 masks by D4 symmetry;
5. count the remaining geometric orbits.

The opposite global polarity, dash=1 / slash=0, is an exact complement bijection and has the same identifiability counts.

No tail cells, predicted cells, machine constraints, plaintext, or Pigpen letter templates are used.

## Result

| class | trace | unknown cells | raw completions | D4 orbits |
|---|---|---:|---:|---:|
| A | `?--?-/???` | 5 | 32 | 28 |
| B | `/?//////-` | 1 | 2 | 2 |
| C | `---///-/-` | 0 | 1 | 1 |
| D | `-/?-/???/` | 4 | 16 | 16 |
| E | `/--/??/??` | 4 | 16 | 16 |
| F | `?/-?/-///` | 2 | 4 | 4 |
| G | `/???/??-/` | 5 | 32 | 20 |
| H | `?/-?--?-/` | 3 | 8 | 8 |
| I | `/-?/??/-/` | 3 | 8 | 8 |

C is completely observed and therefore fixes one D4 shape orbit. B and F are also fairly constrained. A/D/E/G/H/I remain substantially underdetermined.

A weak "nine classes should become nine distinct shapes" requirement barely helps. Across the product of the per-class orbit sets there are:

- **73,400,320** possible orbit assignments;
- **50,550,408** assignments in which all nine classes are D4-distinct;
- fraction distinct: **0.6887**.

So distinctness alone removes only about 31% of the already-bounded geometric assignments.

## Interpretation

The current corpus does not identify a unique nine-glyph geometric alphabet under the one-symbol-as-ink reading. A solver can make many visually different complete glyph sets without contradicting a physical observation.

There are still useful anchors:

- C's complete body is a fixed prospective geometric object;
- B has only two D4 possibilities;
- F has four.

Those classes are the right places to test any **independently specified** geometric template family first. If a proposed Pigpen/Rosicrucian transform cannot accommodate C (and then B/F) without choosing a class-specific transform, reject it before touching the sparse classes.

## Consequence

Do not enumerate arbitrary 3x3 pictures looking for letters. The next admissible move is to define a small, global geometric template/codebook from an external or structural cue, then test C/B/F as fixed or near-fixed holdouts.

The observation-only SVG in `artifacts/foreground-views/observation-only-9x12.svg` is now the canonical visual aid for this lane. It renders actual slash/dash/dot marks and explicit unknowns rather than contrast-filled guesses.

## Reproducibility

```bash
python scripts/audit_pigpen_binary_orbits.py
```

# Blind human-solve worksheet

This is the operational companion to `docs/human-solve-reconstruction.md`.

The problem with a human-path reconstruction is hindsight leakage: once the
ternary lattice, POS3 columns, selector, and terminal are known, almost any
presentation can accidentally make them look obvious. The worksheet generator
therefore has a deliberately narrow contract.

Run:

```bash
python scripts/render_human_worksheet.py
```

or save a disposable copy:

```bash
python scripts/render_human_worksheet.py --output /tmp/inside-blind.md
```

The renderer reads only `data/observations.csv`, collapses duplicate sightings
of the same H108 residue, checks that duplicates agree, and presents the corpus
as twelve consecutive nine-residue blocks in two forms:

1. serial A-I order;
2. the physical A-I artwork layout.

It intentionally does **not** print:

- q/d coordinate names;
- primary/Q4 semantic labels;
- POS3 digits or rail orientation;
- frame polarity;
- the compact ternary lattice;
- selector values;
- hidden-state coordinates;
- recursion outputs;
- terminal `100`.

That makes the generated page useful for a fresh solver, a future agent, or a
human-recognition exercise without silently handing over later conclusions.

## Why this belongs in Priority 4

Experiments 184-190 establish the H108/A-I framing, while 259-265 show that
physical columns and local POS3 behavior can be rediscovered from sparse raw
evidence. The remaining question is less mathematical than procedural: can the
sequence actually be encountered in a representation that does not bake in the
answer?

This worksheet gives that question a stable input artifact. Future human-path
tests should start here and record the first transformations requested by the
solver before showing any answer-key material.

## Guardrail

This is a presentation tool, not a new experiment and not evidence that the
intended Playdead solve path used this exact worksheet. Its purpose is to make
future discovery claims more falsifiable by separating what was shown from what
was inferred.

# Experiment 372 — Xbox local-positional selector precedent for CE POS3

_Status: completed bounded cross-puzzle provenance audit, 2 Oct 2026._

Experiment 371 changes one narrow part of the sticker provenance story.

Experiments 350–352 already established that, in the first 81 CE residues, the best-supported physical skeleton is one minority cell per physical column inside each 3×3 frame, and that recording the minority row is simply the lossless coordinate system of that skeleton. The remaining provenance question was whether Playdead had ever demonstrably used **position inside a small registered geometry** as the thing that determines semantic relevance.

The Xbox printer now supplies exactly that operation class.

In the solved Xbox planet, the reconstructed Braille field is partitioned by local cell geometry: a cell is message-bearing iff one of the two top-row Braille dots is active. That fixed positional test extracts `NEWPLANETDI!COVERED` before the documented one-dot correction. The remaining cells occupy the complementary top-row-empty subspace.

The relevant abstraction is therefore:

```
registered local carrier
    ↓
inspect occupancy relative to fixed positions
    ↓
retain a positional state / semantic role
```

That is substantially closer to CE POS3 than a generic statement such as “Playdead sometimes uses grids.”

But the two mechanisms are not equivalent.

Xbox uses a binary condition on a 2×3 Braille cell: top row active versus empty. CE primary structure exposes three possible minority-row positions in each of three columns. Xbox does not provide the CE row labels, top-to-bottom orientation, shared gauge across columns, arithmetic interpretation, tail selector, recursive substitution, route semantics, or terminal interpretation.

So Experiment 372 changes provenance, not the model definition.

## Epistemic effect

For the source-side G1/POS3 question, there is now a genuine **Playdead-authored pre-CE operation-class precedent** for local positional occupancy being semantically meaningful.

This complements:

- Experiment 350: one-per-column occupancy has independent chronological support;
- Experiment 351: three-position/ternary sticker readout was historically explored by solvers;
- Experiment 352: minority-row coordinates are the lossless representation of the supported occupancy skeleton.

Together, those make the basic positional readout considerably less ad hoc than it looked during the reset.

They still do not prove that the incumbent downstream consumer is intended.

## Guardrail

Do not transfer the literal Xbox rule into the CE. In particular, do not privilege the top row of `IAB/CDE/FGH`, Braille dot numbering, or a binary active/inactive split merely because those worked on Xbox.

The transferable evidence is only the **operation class**:

> local registered geometry can carry meaning through the position of activity, while other positions remain carrier/filler.

Any CE-specific selector still needs to arise from CE evidence.

## Consequence for the queue

This reduces the value of further generic “why position?” searches. The higher-value unresolved questions remain downstream:

1. whether the three row labels share one orientation across columns/frames;
2. why the tail/index should act on the body;
3. why selector reuse should occur;
4. whether any external consumer fixes the route/terminal semantics.

Experiment 372 therefore narrows G1 provenance without reopening G5–G7.

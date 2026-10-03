# Experiment 388 — pre-machine provenance for two-coordinate and layered-sheet reading

_Status: completed historical provenance audit, 2 Oct 2026._

Experiment 386 reframed the active `534brn` candidate as a coordinate-role problem rather than an image-rotation problem.

That makes one historical question especially important:

> Before the present machine existed, had the community independently proposed reading sticker information as orthogonal coordinates and layers?

Yes.

## 19 May 2026 — explicit horizontal/vertical table duality

A preserved forwarded message describes three generated sticker tables, including:

- A–I **left to right**;
- A–I **top to bottom**.

The two attached tables visibly exchange which axis carries the A–I classes.

This is not a solved mechanism, but it is direct pre-machine evidence that the community was already treating axis exchange / matrix orientation as a natural representation family for the sticker corpus.

## 20 May 2026 — two-dimensional sheet plus layers

The next day's discussion becomes more explicit.

The proposed idea was that:

- the letters would provide one position, horizontally or vertically;
- the numbers would provide the other position;
- together they would place each sticker on a two-dimensional sheet;
- there could then be another layer beneath, “like an onion.”

That is unusually close to the abstraction now used in Experiment 386:

```
coordinate role 1
coordinate role 2
payload/layer value
```

Again, the exact modern mapping was not present. The important point is that the **operation class** was independently contemplated.

## 22 May 2026 — DTMF / Polybius coordinate model

Two days later, the same line produced the DTMF keypad proposal.

The discussion explicitly connected DTMF to a Polybius-like positional scheme and then proposed a larger first-nine domain plus a smaller last-three selector.

So, before the modern POS3/G5 machine, the sticker discussion already contained all of these broad ingredients:

- horizontal/vertical coordinate assignment;
- axis exchange;
- layered 2D placement;
- keypad/Polybius positional coordinates;
- large-domain plus small-selector composition.

## Relation to Experiment 386

Experiment 386's unique bounded candidate is:

```
external (r,c,k)
      ->
target   (Q,c,r)
```

The historical material does **not** specify that exact permutation.

It does, however, substantially reduce the novelty burden of asking whether sticker information should be treated as coordinate roles that can move between:

- horizontal position;
- vertical position;
- layer/index/value.

That is the correct level of transfer.

## Guardrail

Do not retroactively call the May-2026 discussion a discovery of the current machine.

It was exploratory and did not contain:

- `Q`;
- G5;
- `q'=2q+2`;
- `112/012/120`;
- the nine `534brn` digits as DTMF rows.

Its evidentiary value is provenance for the **coordinate/layer operation family**, not for the final parameters.

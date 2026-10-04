# Experiment 403 — direct Fractionated Morse is structurally impossible

_Status: completed bounded historical replay, 4 Oct 2026._

On 14 May 2026, the community proposed **Fractionated Morse** because it naturally works with three symbols.

The proposer immediately noticed a problem: the sticker dots are concentrated late in the cycle and suggested that a rearrangement might be required.

The weighted completion universe lets us test the cheapest version exactly.

## Frozen family

Use:

- serial H108 order;
- consecutive groups of three residues;
- standard unkeyed Fractionated Morse trigram table;
- all six bijections between sticker symbols `- / .` and Morse-fraction symbols:
  - dot;
  - dash;
  - separator `x`.

Fractionated Morse has 26 legal trigrams over `.-x`; the only excluded trigram is:

```
xxx
```

No row permutations, keywords, or language scoring are allowed.

## Result

Across:

```
6 symbol mappings
×
648 U2 completions
```

valid direct decodes:

```
0
```

Every configuration fails structurally before any letters are considered.

## Why the failure is absolute

The U2 completion universe contains several consecutive three-residue groups that are invariantly uniform.

All-dash triples begin at:

```
10, 70, 73
```

All-slash triples begin at:

```
28, 40, 46, 64, 67, 76, 79
```

An all-dot triple begins at:

```
97
```

Therefore every possible symbol assignment loses.

- If dash maps to separator `x`, a fixed `---` block becomes `xxx`.
- If slash maps to `x`, a fixed `///` block becomes `xxx`.
- If dot maps to `x`, the fixed `...` block becomes `xxx`.

That forbidden trigram exists for **every** coherent U2 completion.

## Interpretation

The historical proposer was right that the serial arrangement does not fit Fractionated Morse.

We can now say something stronger:

> direct serial-order Fractionated Morse is mathematically impossible under the broad physical completion universe.

This is a clean hard negative, not a failed English search.

## Reopening trigger

Fractionated Morse should reopen only if another artifact independently specifies a rearrangement that breaks the invariant uniform triples.

Do not search arbitrary permutations for one that avoids `xxx`.

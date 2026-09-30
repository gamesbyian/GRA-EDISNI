# Experiment 321 — Weaken G7 to information preservation

_Status: completed R4 G7 attack, 30 Sep 2026._

## Question

Experiment 320 identified G7 as the largest circularity risk in the surviving incumbent premise set.

Its current form is semantically loaded:

> choose one q-indexed word from each of the three first-pass functional families such that the three chosen words are mutually distinct permutations of 0,1,2.

That sounds like a **route** rule because it was formulated after route-like behavior had already become visible.

Can the same result be obtained from weaker, generic non-collapse principles that do not mention routes, distinct maps, cycle types, the expected shell, or terminal `100`?

## Input

The three first-pass functional families already derived before G7 are:

```
102  002  120
102  012  100
102  022  100
```

As in Experiment 278, choose one q-indexed word from each row. There are `3^3 = 27` assignments.

## Two weaker conditions

### A. Preserve the ternary alphabet inside each chosen word

Require each selected three-symbol word to contain `0`, `1`, and `2` exactly once.

This is an information-preservation condition: no ternary label is duplicated or erased inside the selected output.

It leaves **4** of the 27 assignments.

No requirement is made that the three selected words differ from one another.

### B. Preserve all three q positions across the three families

Require the three selected q indices themselves to use `0`, `1`, and `2` exactly once.

This prevents the selection rule from collapsing multiple functional families onto the same q coordinate.

It leaves **6** of the 27 assignments.

This condition does not inspect the contents of the selected words.

## Intersection

Exactly one assignment satisfies both independent non-collapse conditions:

```
q choices: 2, 1, 0
words:     120, 012, 102
```

So the canonical shell and `q=2-p` follow without requiring:

- mutual distinctness of the selected words;
- route semantics;
- fixed-point/cycle-type targets;
- the request/grant interpretation;
- terminal `100`;
- any expected route word.

## Interpretation

This materially weakens G7.

The old G7 can be replaced by two generic symmetry/information-preservation priors:

1. **word non-collapse:** a selected ternary word preserves all three ternary labels;
2. **coordinate non-collapse:** the three functional families collectively use all three q coordinates.

The result is still not a direct observation. These are authoring/simplicity priors. But they are substantially less machine-specific than “there must be three distinct reversible routes.”

In particular, **mutual route distinctness is redundant** once these two weaker conditions are imposed.

## Epistemic consequence

G7 should no longer be classified as “selected because it preserves the machine.”

Its surviving content is better classified as a **generic simplicity / information-preservation prior**.

That does not make G7 independently true. It removes the strongest circularity concern identified in Experiment 320.

After this experiment, G6 becomes the highest-priority remaining machine-preservation premise.

## Reproducibility

Run:

```bash
python scripts/audit_g7_information_preservation.py
```

The script asserts:

- 27 total q-choice assignments;
- 4 preserve the ternary alphabet in every selected word;
- 6 use all three q positions exactly once;
- their intersection contains exactly `(2,1,0) -> 120/012/102`.

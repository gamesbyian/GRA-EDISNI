# Experiment 401 — nontrivial coupling atlas across the completion ladder

_Status: completed structural ensemble audit, 4 Oct 2026._

The weighted-completion program can expose structure that is hard to see in per-residue prediction tables.

A useful example is **pairwise coupling**.

Naively counting equal or complementary residue pairs produces thousands of meaningless relations because many cells are already fixed. So this experiment uses a stricter rule.

A pair counts only when:

1. both residues vary in the parent ensemble;
2. both still vary in the child ensemble;
3. yet the child ensemble forces them always equal or always complementary.

That isolates newly created relational structure rather than fixed-cell coincidences.

## Uncertainty collapse

The number of individually variable residues is:

```
U2  19
U4  14
U5  13
E2   2
```

The active `534brn` pair really is almost completely determined physically.

## U2 -> U4

The typed one-shot closure creates exactly four nontrivial relations:

```
22  <->  25   complement
84  <-> 102   complement
88  <-> 106   complement
94  <-> 103   complement
```

No nontrivial equality relations appear.

Three of the four are tail-selector pairs. The remaining primary relation `22/25` is a compact body-side consequence of the one-shot closure.

## U4 -> U5

G6 retains those four and adds exactly one new nontrivial coupling:

```
91 <-> 100   complement
```

So a compact relational fingerprint of the recursive step is:

> G6 creates the additional 91/100 complement.

This is weaker as an acquisition target than residue 82, which already directly distinguishes E2 from U5, but it is useful as a model fingerprint.

## U4 -> E2

The externally selected pair leaves exactly one nontrivial relation:

```
84 <-> 102   complement
```

Those are also the **only two variable residues left at all**.

So E2 is not hiding a complicated cloud of uncertainty. It is literally one unresolved physical bit:

- slash at residue 84, or
- slash at residue 102.

Everything else in the complete 108-cell master is fixed.

## Why this matters

This gives a more exact description of the active external model than “two candidate masters.”

It is one master with one binary unresolved coordinate.

That binary coordinate now appears in several independent representations:

- which E2 master survives;
- class-C tail depth;
- class-C literal 3-bit number in Experiment 399;
- physical residue 84 versus 102.

This convergence makes the residue-84/102 families especially valuable acquisition targets.

## Guardrail

Do not turn the coupling atlas into generic XOR/correlation mining.

The useful family here is exact equality/complement among residues that remain individually variable. Higher-order Boolean searches require an independent reason.

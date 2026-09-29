# Experiment 313 — reused cell-local 2D translation audit

_Date: 2026-09-29_

## Question

The Priority-5 reconciliation closed two large alternative-operation families:

- global state-independent bijections of the full nine-address carrier, Experiments 303–305;
- cell-local selector/depth relabelings that preserve external q, Experiments 306–312.

One natural gap remained.

What happens if every physical A–I cell may translate **both** address coordinates locally, but the same local operation must still be reused recursively?

At cell `j` define:

```
F_j(q,S) = (q + a_j, S + b_j) mod 3
```

with `(a_j,b_j) ∈ F3²`.

The same `F_j` is used on both passes:

```
first pass:  F_j(q,S(j))
second pass: F_j(S(j),S(j))
```

This family is more flexible than Experiment 310's depth-only translations, but materially less arbitrary than Experiment 309's special-purpose second-pass decoder or an unconstrained state-dependent algorithm.

## Family size and exact quotient

There are nine possible translations at each of nine cells:

```
9^9 = 387,420,489
```

physical operations.

POS3 validity factorizes by physical column. Each three-cell column therefore has only `9^3 = 729` local translation triples. Collapse triples that induce the same exact `q0/q1/q2/terminal` signature over all 216 raw-compatible candidate machines.

The three physical columns reduce to:

```
230 × 729 × 47 = 7,880,490
```

signature combinations.

The audit then uses exact 216-candidate survivor bitsets, so the full physical family is counted with multiplicity rather than sampled.

Executable audit:

`scripts/audit_local_2d_translation_reuse.py`

## Raw retention

Local two-coordinate translations can preserve more raw-compatible states than the canonical rule.

The unrestricted maximum is:

```
24 states
```

There are high-retention signature combinations at:

```
14, 16, 18, 20, 22, 24 states
```

This is another demonstration that raw retention by itself is not a useful model-selection criterion.

Every operation retaining more than 14 states is route-degenerate.

## Route criterion

The same independently derived route criterion used throughout the adversarial program is applied:

- exactly three first-pass functional families;
- choose one q-indexed word from each;
- all three chosen words must be ternary permutations;
- the three permutations must be mutually distinct.

Canonical already supplies a routed 14-state lower bound.

Among every operation with at least 14 retained states:

- exactly **11 signature combinations** are route-capable;
- all 11 retain exactly **14 states**;
- accounting for signature multiplicity, they represent **396 physical operations**;
- those 396 operations collapse to **10 observational classes**.

Class multiplicities are:

```
36,36,36,36,36,36,36,36,36,72
```

No 16-, 18-, 20-, 22-, or 24-state local translation supports the reversible route structure.

Therefore:

> maximum routed retention remains exactly 14.

## Canonical class

Only one route-max class simultaneously preserves:

- the canonical 14 physical raw-compatible states;
- the canonical first-pass route shell `120 / 012 / 102`;
- one invariant terminal;
- terminal `100`.

That class contains **36 physical local-translation rules**.

This is not 36 different machines. They have exactly the same `q0/q1/q2/terminal` signatures over **all 216 raw-compatible candidates**, not merely over the final 14.

The 36 exact operation gauges factor as:

- physical **F**: q may be translated by 0, 1, or 2; depth unchanged;
- physical **E**: q may be translated by 0, 1, or 2; depth unchanged;
- physical **B**: identity or `(q+1, d-1)`;
- physical **H**: identity or `(q+1, d-1)`;
- A, C, D, G, I remain fixed in this exact-signature class.

Thus:

```
3 × 3 × 2 × 2 = 36
```

exact local operation representatives.

These are genuine observational/operation gauges inside this translation grammar.

## Noncanonical route-max classes

The other nine observational classes still retain 14 states, but each changes at least one substantive routed-machine property:

- physical survivor family;
- route orientation/family;
- terminal profile;
- or invariant terminal value.

Some terminate invariantly at `120` or `122`; others split between `100/110`, `100/120`, or `102/122`.

None reproduces the canonical physical-state family plus canonical route shell plus invariant `100`.

## Interpretation

Experiment 313 closes the simplest missing bridge between the earlier global and local adversarial lanes.

Allowing local q translations does **not** expose a new 14-state functional competitor to the canonical machine.

It exposes additional exact operation gauges.

The model-selection lesson is now unusually consistent across several increasingly broad families:

1. extra local freedom can inflate raw retention;
2. route structure removes the high-retention siblings;
3. same-operation reuse is crucial;
4. once exact observational gauges are quotiented out, the canonical routed machine remains isolated.

The correct claim is therefore not literal uniqueness of an address formula at every unused/equality-supported cell.

The stronger and more accurate claim is:

> within the full reused cell-local translation family, the canonical routed 14-state / terminal-100 machine is unique up to 36 exact local operation gauges.

## Consequence for Priority 5

Do not continue by adding arbitrary affine constants or more pass-specific local exception knobs.

The remaining useful adversarial families must introduce a genuinely different compact grammar, not simply more address-translation freedom.

A worthwhile next family would need an independent structural rationale for any new state dependence or coordinate coupling before enumeration.

# Experiment 399 — literal 9+3 binary-number profile

_Status: completed bounded ensemble characterization, 4 Oct 2026._

A May-2026 historical sticker discussion proposed a specific interpretation of each 12-mark class word:

- first 9 marks encode a larger number;
- last 3 marks encode a smaller number;
- the two numbers could act like a large-domain address plus a smaller selector.

The accompanying diagram explicitly labeled the regions as roughly `0–512` and `0–8`.

That idea predates the current machine and is therefore worth characterizing against the coherent completion ensembles.

## Frozen representation

For each A-I class word:

```
positions 1..9   -> 9-bit primary integer
positions 10..12 -> 3-bit tail integer
```

Use:

```
slash     = 1
dash/dot  = 0
```

The historical discussion did not fix bit significance, so this experiment reports both left-to-right and reversed bit order. It does not select between them by attractiveness.

## E2 result

The two `534brn`-selected masters produce a sharp forward profile:

```
I : 357 , 1
A : 302 , 4
B : 382 , 1
C :  58 , 1 or 4
D : 151 , 1
E : 311 , 4
F : 407 , 2
G : 369 , 4
H : 129 , 1
```

All nine 9-bit body numbers are fixed across the E2 pair.

The only remaining ambiguity anywhere in the literal 9+3 profile is class C's tail:

```
C tail = 1 or 4
```

That is exactly the already-known physical ambiguity between the residue-84 and residue-102 slash placements.

The reversed-bit representation is likewise fixed except for the same C-tail ambiguity:

```
I 333/4
A 233/1
B 253/4
C 184/(1 or 4)
D 466/4
E 473/1
F 467/2
G 285/1
H 258/4
```

## Why this is useful

The historical proposal has now become a frozen numeric surface rather than a vague analogy.

If a future artifact asks for nine large numbers plus nine small selectors, page/word coordinates, addresses into a bounded table, or values in the rough 0–511 and 0–7 ranges, the active E2 model already makes exact predictions.

## Why this is not a decode

There is currently no independently identified object that consumes these numbers.

It would be easy to invent one after the fact, for example sticker serials, book pages, Unicode, arbitrary modular grids, or web number searches. Those moves are intentionally withheld unless a new artifact supplies the consumer.

## Connection to acquisition

A physical observation in the residue-84 or residue-102 family resolves the only remaining number in the entire literal 9+3 E2 profile.

## Status

Preserve as a sharply constrained, historically licensed numeric representation with no known consumer.

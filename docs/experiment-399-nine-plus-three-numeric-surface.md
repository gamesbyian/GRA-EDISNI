# Experiment 399 — historical 9+3 binary-number surface

_Status: completed bounded representation audit, 4 Oct 2026._

The May-2026 sticker discussion supplied a particularly concrete pre-machine idea.

For each 12-cell class word:

- first 9 symbols = a larger binary number, illustrated as roughly `0–512`;
- final 3 symbols = a smaller binary number / selector;
- possible use: page number plus word/index inside a larger source.

The archived image literally labels the two zones as separate numeric domains.

The weighted-completion ensemble lets us characterize that proposal without inventing a book or scoring plaintext.

## Frozen representation

For each A-I class word:

- slash = 1;
- dash/dot = 0;
- read the first nine positions left-to-right as a 9-bit integer;
- read the last three positions left-to-right as a 3-bit integer.

This is representation-only. No external book or numeric corpus is assumed.

## Externally selected pair

For the two `534brn`-selected masters, the first-nine values are already completely fixed:

```
A 302
B 382
C  58
D 151
E 311
F 407
G 369
H 129
I 357
```

The two selected masters therefore agree on the entire nine-number body vector:

```
302, 382, 58, 151, 311, 407, 369, 129, 357
```

Their only numeric disagreement is the class-C tail.

Tail support is:

```
A 4
B 1
C 1 or 4
D 1
E 4
F 2
G 4
H 1
I 1
```

That is exactly the same remaining physical ambiguity already localized to residues 84 and 102.

## Important structural correction to the historical sketch

A generic 3-bit number has eight possible values `0..7`.

The actual sticker tail does not.

Because every class has exactly one slash in its three tail positions, the binary tail is constrained to the one-hot values:

```
001 = 1
010 = 2
100 = 4
```

So the historical “smaller number” idea is better understood as a **three-state selector** than as an unrestricted 3-bit integer.

That dovetails with the independently typed tail-depth interpretation.

## What this gives us

The numeric representation is now a clean reusable surface for any future external artifact that actually supplies a numeric consumer.

In particular, a future source could independently tell us to interpret the first-nine value as:

- a page;
- a serial / record ID;
- a row in a table;
- an offset;
- another ARG object with a known numeric domain.

If such a consumer appears, we already have its complete E2 input vector without needing the last missing physical sticker.

## What it does not give us

There is currently no independently specified book, table, page corpus, or numeric lookup surface tied to these values.

Therefore the numbers themselves are not evidence of plaintext.

Do not search arbitrary books, web pages, or modulo transforms for attractive coincidences.

The useful result is structural:

> under the strongest current external pair, the historical 9+3 numeric scheme has collapsed to nine fixed large values plus one unresolved three-state selector bit of physical evidence.

# Experiment 351 — historical 9+3 nested-index identifiability audit

_Status: completed bounded identifiability audit, 30 Sep 2026._

## Historical cue

The 22 May 2026 Discord context makes the pre-machine 9+3 proposal more specific than the earlier reset summary recorded.

The discussion used a two-layer keypad/book-cipher analogy:

1. one layer identifies a larger container, such as phone key `7` or book page `362`;
2. a second layer gives an index inside that container, such as the third letter on that key or the seventh word on that page.

The sticker proposal immediately following was:

> in the 9×12 orientation, the first 9 bits may encode one number representing the larger domain, while the last 3 bits encode a second number selecting a smaller subset.

This is historically prior to the current machine and supplies a genuine **nonrecursive nested-index operation class**. It does not specify a consumer.

## Cheapest literal realization

For each A–I class trace:

- read its first nine slash/dash cells in chronological order as a 9-bit binary integer;
- use one global body polarity, either slash=1/dash=0 or its complement;
- use Experiment 317's independently supported exact-one-slash tail family, so the final three cells define a three-way positional index;
- do not dictionary-rank, page-search, key-search, or choose a target domain.

This is intentionally the literal historical proposal rather than an optimized modern reinterpretation.

## Result

The body is far from identified.

Per global body polarity, the nine A–I body words have:

| class | body unknowns | possible 9-bit words |
|---|---:|---:|
| A | 5 | 32 |
| B | 1 | 2 |
| C | 0 | 1 |
| D | 4 | 16 |
| E | 4 | 16 |
| F | 2 | 4 |
| G | 5 | 32 |
| H | 3 | 8 |
| I | 3 | 8 |

That is exactly **134,217,728** joint nine-word assignments for either fixed global polarity. The opposite polarity simply complements every 9-bit value `n -> 511-n`.

The tail index domains are:

```
A {0,1,2}
B {2}
C {0,1,2}
D {1,2}
E {0}
F {1}
G {0,2}
H {2}
I {2}
```

giving exactly **36** joint tail-index assignments, consistent with Experiment 317.

Combining body uncertainty, tail uncertainty, and the two global body polarities leaves:

```
134,217,728 × 36 × 2 = 9,663,676,416
```

literal nested-index codebooks before any external domain or consumer is supplied.

Only C has a fully observed 9-bit body word before global polarity is chosen. Five classes, B/E/F/H/I, have fixed tail indexes.

## Interpretation

The historical two-layer idea is real and should remain in the hypothesis inventory, but the literal binary-number form is **massively underidentified** by the current physical corpus.

This is not evidence against all body+subindex designs. It closes the idea that merely reading the first nine cells as a binary integer and the last three as an index gives an actionable decoder from the closed corpus.

The important positive residue is architectural:

> community solvers independently proposed that the 9-cell body and 3-cell tail encode different scales of information, with the tail acting as an index into something selected by the body.

That is a legitimate rival operation class to G5's recursive address substitution.

## Consequence for G5

Do not claim the May-2026 discussion independently motivates `(q,d,j)->(q,S(j),j)`. It does not.

It motivates a broader nonrecursive **container + sub-index** family. The next admissible move requires an external or sticker-native specification of the larger domain or container. Without one, trying page numbers, keypad keys, dictionaries, grids, or arbitrary lookup tables would be semantic fishing across billions of compatible codebooks.

Reopen the literal nested-index branch only when another artifact supplies the domain/consumer or when new physical evidence sharply reduces body-word uncertainty.

## Reproducibility

```bash
python scripts/audit_historical_nested_index.py
```

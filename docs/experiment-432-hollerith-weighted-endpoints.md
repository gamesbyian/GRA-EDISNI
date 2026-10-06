# Experiment 432 — Hollerith-weighted census and endpoint totals

## Question

Once the literal IBM 029 character mappings are admitted as a representation candidate, do their **row-label sums** interact nontrivially with the already-established sticker symbol census and the frozen endpoint candidates?

Use only:

- `/ = 0+1 = 1`;
- `- = 11`;
- `. = 12+8+3 = 23`;
- the 10 live canonical masters;
- endpoint candidates frozen before Experiment 424: 598/600/603/612/621/630/639/648.

No alternate weights, digit operations, or endpoint search are introduced.

## Full H108 master

Every canonical complete master has the established census:

```
54 slash
36 dash
18 dot
```

Therefore its total IBM row-label sum is completion-independent:

```
54×1 + 36×11 + 18×23
= 54 + 396 + 414
= 864
= 8×108
```

Equivalently, because 54:36:18 = 3:2:1, the mean row-label sum per sticker is exactly:

```
(3×1 + 2×11 + 1×23) / 6 = 8
```

The value **8** is itself one of the period punches `12-8-3`.

This is an exact cross-representation arithmetic identity, but it is downstream of the known 3:2:1 census and the Hollerith weights rather than independent evidence.

## Frozen endpoint comparison

Repeat each live H108 master from serial 1 through each frozen endpoint and sum the literal IBM row labels.

| total | Hollerith-weighted total(s) across live masters | invariant? | square? | divisible by 23? |
|---:|---|:---:|:---:|:---:|
| 598 | 4658 / 4668 | no | no | no |
| 600 | 4660 / 4670 | no | no | no |
| 603 | 4683 | yes | no | no |
| 612 | 4722 | yes | no | no |
| 621 | **4761** | yes | **69²** | **yes** |
| 630 | 4902 / 4924 / 4946 | no | no | no |
| 639 | 5043 / 5065 / 5087 / 5109 | no | no | no |
| 648 | **5184** | yes | **72²** | no |

For 621:

```
4761 = 69²
     = (3×23)²
     = 9×23²
```

and because `621 = 27×23 = 9×69`:

```
4761 / 621 = 23/3
```

So under the hypothetical 001..621 run, the average literal Hollerith row-label sum per sticker is exactly **23/3**.

For 648:

```
5184 = 72²
```

so square-ness alone does not select 621. 648's square follows its clean six-full-H108 structure combined with the exact mean weight 8.

## Interpretation

This is more constrained than an arbitrary number hunt because every ingredient was fixed before inspection of the result.

Still, the arithmetic operation itself, **summing IBM row labels**, remains nonstandard as a punch-card decode. Experiment 424 already marked that caveat.

The right status is therefore:

- exact and reproducible numerical convergence;
- 621 gains another 23-specific property inside the frozen endpoint set;
- not independent evidence for 621 or Hollerith;
- potentially much more important if an external clue licenses arithmetic, totals, averaging, or 23.

## Disposition

Preserve the identity. Do not extend to arbitrary number-theory searches.

The strongest current conditional conjunction for 621 is now:

```
621 = 23×27
621 = 5×108 + 81
Hollerith-weighted total = 69² = (3×23)²
mean Hollerith row-label sum = 23/3
```

This is a convergence to watch, not a production-count conclusion.

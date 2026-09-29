# Experiment 301 — historical Discord interval-scanner reproduction

_Date: 2026-09-29_

## Question

What did the archived historical interval scanner actually establish, and what did its printed "total number of stickers" values mean?

The original C++ source is preserved at:

`archive/discord/2026-09-29/inside sticker code interval.txt`

Experiment 301 reproduces its logic exactly in:

`scripts/audit_discord_interval_scanner.py`

## Historical algorithm

The program stores 82 numbered sticker observations using:

- slash = 1;
- dash = 2;
- dot = 3.

It then tests every integer offset from 1 through 299.

An offset survives only if:

1. at least one pair of observed sticker numbers is separated by exactly that offset; and
2. every observed pair separated by that offset has the same foreground symbol.

This is an **exact-offset compatibility test**. It is not the same as folding every sticker modulo a candidate period and comparing all residue collisions across arbitrary multiples.

For each surviving offset the program prints:

`597 + offset - (597 mod offset)`

That is simply the next strictly greater multiple of the candidate offset after the then-maximum observed serial 597.

## Exact reproduced output

Only five offsets survive:

| Offset | Matching observed pairs | Printed "total number of stickers" |
|---:|---:|---:|
| 108 | 8 | 648 |
| 125 | 7 | 625 |
| 197 | 6 | 788 |
| 216 | 5 | 648 |
| 254 | 4 | 762 |

The Python reproduction asserts this exact list.

## Interpretation

### Why 108 mattered

108 is the **smallest contradiction-free tested offset with any exact-offset support**.

That makes the historical result genuinely relevant as discovery provenance: the old code had already isolated 108 from this particular sparse-offset test.

### Why 216 is not independent confirmation

A 216 offset is two 108 periods. Compatibility at 216 is therefore expected if the underlying object repeats every 108.

The shared printed value 648 for 108 and 216 is only a consequence of the arithmetic formula.

### Why 125, 197 and 254 survive

These offsets have only 7, 6 and 4 observed exact-offset pair comparisons, respectively. They survive because none of those sparse comparisons contradicts the offset.

The scanner does not establish that they are genuine periods.

Later fuller H108 analyses use all residue collisions and stronger family-wide tests, which is why this historical program should be treated as discovery archaeology rather than the canonical proof of periodicity.

## The 648 issue

For offset 108:

`597 + 108 - (597 mod 108) = 648`

The program therefore prints 648 by rounding the maximum observed serial upward to the next multiple of 108.

It does not read a production count from a file, infer one from a manufacturing record, or observe sticker 648.

The same code prints:

- 625 for offset 125;
- 788 for 197;
- 648 for 216;
- 762 for 254.

This demonstrates directly that these totals are candidate-offset extrapolations, not production evidence.

## Consequence

The historical interval scanner is now fully reproduced and classified.

- Preserve it as provenance for how the community found the 108 signal.
- Do not cite its 625/648/762/788 values as Collector's Edition production counts.
- Do not use 648 as evidence for the mechanical model.
- Prefer the modern full modulo-108 collision audit for canonical period claims.

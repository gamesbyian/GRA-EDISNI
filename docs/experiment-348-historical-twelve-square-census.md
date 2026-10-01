# Experiment 348 — historical twelve-square census identifiability audit

_Status: retrospective bounded audit, 30 Sep 2026._

## Historical operation

Archived community discussion independently supplies a deterministic foreground representation:

1. write H108 as twelve consecutive rows of nine stickers;
2. note that each row contains A-I once in serial order;
3. place those nine cells into the already-solved background geometry `IAB / CDE / FGH`;
4. obtain twelve 3×3 foreground squares.

This operation was discussed in Dec 2022 and stated explicitly in Oct 2023, before the present machine model. The first nine squares use slash/dash; the final three use slash/dot.

The physical A-I reshaping changes geometry but not each square's symbol census. That makes a frame-level count rule a legitimate cheap structural question.

## Question

Without importing the incumbent frame polarity or POS3 grammar, suppose only that the first nine slash/dash 3×3 squares share one common **unordered binary census**:

```
w of one symbol, 9-w of the other
```

where `w` is the minority count and `w ∈ {0,1,2,3,4}`.

Which values of `w` are compatible with every physically observed square?

This enumerates the entire five-member family. It does not select `3/6` because the incumbent uses it.

## Method

Use only `data/observations.csv`, residues 1–81.

For each of the nine consecutive 9-cell squares:

- count observed slashes, dashes, and unknowns;
- for each `w = 0..4`, exactly enumerate binary fillings of the unknown cells compatible with total slash count `w` or `9-w`;
- record the number of compatible completions.

A common census survives only if every square has at least one completion.

No frame polarity, minority-symbol assignment, depth/quarter labels, tail cells, machine closure, or semantic output is used.

## Result

Exactly two common census families survive all nine physical squares:

- **3/6**, with 12,960 joint observation-compatible completions;
- **4/5**, with 18,000 joint observation-compatible completions.

The other unordered splits 0/9, 1/8, and 2/7 are excluded by the physical observations.

Per-square compatible-completion counts are:

| square | observed / | observed - | unknown | 3/6 completions | 4/5 completions |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 2 | 3 | 3 | 4 |
| 2 | 3 | 4 | 2 | 1 | 3 |
| 3 | 1 | 5 | 3 | 3 | 1 |
| 4 | 4 | 1 | 4 | 6 | 5 |
| 5 | 5 | 2 | 2 | 2 | 1 |
| 6 | 3 | 2 | 4 | 5 | 10 |
| 7 | 4 | 1 | 4 | 6 | 5 |
| 8 | 3 | 3 | 3 | 2 | 6 |
| 9 | 5 | 2 | 2 | 2 | 1 |

## Interpretation

This changes the epistemic status of a familiar incumbent property.

A 3/6 split in every primary 3×3 square is **strongly compatible with the raw sticker corpus and independently motivated as a thing to inspect by the historical twelve-square representation**. But the physical observations do not identify 3/6 uniquely. A uniform 4/5 split also survives, with more raw completions.

Therefore:

- "every first-nine 3×3 square has a 3/6 census" must not be presented as a direct observation;
- the historical representation supplies independent motivation for a common frame-census family;
- selecting 3/6 over 4/5 still requires additional structure;
- later machine experiments may legitimately show that recursion/closure selects 3/6 inside a broader family, but that is model-level evidence rather than Layer-0 confirmation.

This is exactly the sort of distinction the epistemic reset is intended to expose.

## Relationship to Experiment 272

Experiment 272 assumed an established frame polarity and required exactly three **minority-symbol** cells per frame before applying recursive POS3 closure. Its 1,296 primary payloads are therefore a narrower, polarity-labelled family.

Experiment 348 sits upstream of that assumption. It treats slash/dash labels symmetrically and finds 12,960 raw 3/6 completions versus 18,000 raw 4/5 completions. The historical twelve-square representation motivates the frame domain independently, while the raw corpus alone does not choose between those two census families.

## Reproducibility

Run:

```bash
python scripts/audit_historical_twelve_square_census.py
```

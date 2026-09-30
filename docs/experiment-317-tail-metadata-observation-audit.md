# R2 Tail-as-Metadata Observation Audit

_Status: first discriminating reset test, 30 Sep 2026._

## Question

The historical community independently proposed reading each A-I class as a 12-symbol unit split into:

- first 9 symbols: a larger body/domain;
- final 3 symbols: a smaller selector/index.

Before importing POS3 or the current recursive machine, ask the cheapest possible question:

> Do the physical slash/dot observations in those final three positions even support a simple positional exceptional-mark code?

## Inputs

Only `data/observations.csv`.

Explicitly excluded:

- predicted unknown foregrounds;
- `machine-spec.json`;
- POS3;
- Q4 terminology;
- recursive closure;
- route criteria;
- terminal `100`.

## Tested local code families

For each A-I class's three tail positions:

1. **one slash:** exactly one position is slash and the other two are dots;
2. **one dot:** exactly one position is dot and the other two are slashes.

Unknown physical residues remain wildcards.

## Result

### One-slash family

Compatible with every observed tail mark.

Number of complete nine-class assignments:

```
36
```

The currently observed data already force the exceptional slash position for five classes:

| class | tail observations | forced slash position |
|---|---|---:|
| B | `?./` | 2 |
| E | `/.?` | 0 |
| F | `?/?` | 1 |
| H | `..?` | 2 |
| I | `.?/` | 2 |

Remaining freedom:

- A: 0/1/2;
- C: 0/1/2;
- D: 1/2;
- G: 0/2.

Thus `3 × 3 × 2 × 2 = 36`.

### One-dot family

Already impossible from raw observations.

Class H has tail:

```
..?
```

so at least two dots are physically observed. A code requiring exactly one dot in each triple has zero global completions.

## What this establishes

Without any machine assumptions, the physical corpus supports a strikingly compact statement:

> The slash/dot tail is globally compatible with one slash marking one of three positions for every A-I class, and the opposite one-dot polarity is contradicted.

This materially strengthens the historical "last three symbols act as an index/selector" idea.

It is also independently discoverable: no downstream output was used to choose the polarity.

## What this does not establish

It does **not** tell us what the marked position means.

In particular it does not establish that the slash position:

- selects one of three rows of the preceding nine;
- selects one of three columns;
- represents a ternary digit;
- selects physical depth in a 3x3 stack;
- should be applied recursively;
- participates in routing.

Those are separate hypotheses.

## Cheapest next test

Under the simplest historical interpretation, let the slash position choose one of three consecutive 3-symbol chunks from the preceding nine.

Observation-only selected chunks are then:

- B: `//-`
- E: `/--`
- F: `?/-`
- H: `?-/`
- I: `/-/`

A/C remain unconstrained; D/G have two possible choices.

No obvious plaintext interpretation is licensed at this point. The next useful comparison is structural:

1. row/chunk selection;
2. column selection from the 3x3 body;
3. three fixed masks tied to the solved A-I background geometry.

Those can be compared by how much observed structure they explain or predict, without using recursive-machine survival.

## Reproducibility

Run:

```bash
python scripts/audit_tail_metadata.py
```

The script asserts:

- 36 one-slash completions;
- zero one-dot completions;
- forced slash positions B=2, E=0, F=1, H=2, I=2.

Any future physical sticker observation that changes those facts will fail loudly.

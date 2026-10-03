# Experiment 374 — the one-shot G5 output is already a structured object

_Status: completed structural characterization, 2 Oct 2026._

Experiment 373 gives a source-side reason to apply the tail selector once:

- the tail slash position is physically a native `d` coordinate;
- applying it type-preservingly to the preceding `(Q,d)` body gives `d=S(j)`;
- that operation is exactly G5.

The obvious next question is therefore:

> What exists if we stop there, before making the additional G6 decision to reuse the d-selector as a Q-selector?

The answer is surprisingly compact.

## Exact one-shot family

Start from the 216 raw-compatible payload×tail completions.

Require only that the typed G5 selection produces valid positional columns for all three Q layers. As already known, 20 machines survive.

Those 20 machines produce only **six distinct 3×3 ternary objects**:

| first-pass Q words | raw machines |
|---|---:|
| `102 / 002 / 120` | 4 |
| `102 / 012 / 100` | 4 |
| `102 / 022 / 100` | 6 |
| `112 / 012 / 100` | 2 |
| `112 / 012 / 120` | 2 |
| `122 / 022 / 100` | 2 |

Across all six objects, six of the nine cells are invariant.

The entire family has normal form:

```
1 x 2
0 y 2
1 z 0
```

Only the middle column varies.

Its six realized middle-column states are:

```
002
010
020
110
112
220
```

So the state after one selector application is not an amorphous intermediate waiting to be cleaned up. It is already a highly registered six-state object.

## Why this matters

Until now the second selector application could feel almost inevitable because it collapses the 20 machines to 14 and produces invariant `100`.

Experiment 373 changes the burden of proof. G5 now has a native coordinate-type justification, while G6 requires a new cross-axis identification from `d` to `Q`.

Experiment 374 shows what is being discarded by that extra step: a compact 3×3 object with a fixed six-cell scaffold and all uncertainty localized to one column.

That creates a legitimate rival stopping point:

> **typed one-shot endpoint:** retain the three Q surfaces after `d=S(j)`, and seek an independently specified consumer of the resulting six-state middle column / 3×3 object.

This is not a claim that the one-shot object is the intended final answer. It is now the cleaner evidence-first endpoint because it requires no additional coordinate coercion.

## Relation to G6

G6 remains mechanically impressive:

- Experiment 322 exhausts all 27 `Q=f(S)` maps;
- only the `002`/`012` gauge pair maximizes completion-invariant retention at 14;
- both produce `100`.

But that evidence is conditional on deciding to consume Q with S at all.

The correct comparison is now:

1. **one-shot typed model:** stop at the six-state `1x2 / 0y2 / 1z0` object;
2. **recursive/cross-axis model:** add a d→Q identification, apply a second selector-conditioned read, and obtain invariant `100`.

External evidence should decide between them. Terminal elegance alone should not.

## Next research move

Search the existing ARG/CE corpus for a consumer that naturally accepts:

- a three-row 3×3 ternary object;
- the fixed scaffold `1?2 / 0?2 / 1?0`;
- or one of the six middle-column words `002,010,020,110,112,220`.

The consumer must be specified independently before matching these outputs.

Do not search arbitrary ciphers for whichever of the six looks best.

# DISCOVER: sticker-background URL digits as a native Q4 depth key (12 October 2026)

**Mode: DISCOVER/DEVELOP.** Reproduce offline with `python scripts/conjecture_lab_url_digits_q4_depth.py`. No external service or access-password interface was queried.

## Provenance and reason to try

The nine-piece CE sticker background puzzle independently supplied the Terminal41 route `534brn9653f9j8mmd`, with nine digits `534965398`. The serial/background relation supplies the native physical row-major classes `I A B / C D E / F G H`, and the original source material has historical keypad and rotation precedents (Experiments 378, 380–382). The independent foreground observation table permits the conditional Q4 slash-position depths:

```
I = {2}        A = {0,1,2}     B = {2}
C = {0,1,2}    D = {1}         E = {0}
F = {1}        G = {0,2}       H = {2}
```

This experiment asks whether the nine **already-decoded background digits** could themselves identify the nine Q4 depth choices. The key hypothesis is deliberately **not required to have been independently cued by Playdead** before being explored.

## Frozen input and candidate operations

The literal known input is `534 / 965 / 398` placed in native `IAB/CDE/FGH` order. Inspect ordinary community alphabetic `ABCDEFGHI` as a separate competing registration. For each, test all 8 rigid rotations/reflections (D4) of the 3×3 digit grid.

Operations:

1. **Arbitrary but consistent digit lookup:** all instances of the same input digit must choose the same Q4 depth, with all Q4 physical evidence obeyed. Exact feasibility is checked by set intersection rather than guessing the lookup table. This is a generous invented bridge, not evidence of a digit decoder.
2. **Standard DTMF keypad row or column:** (r=(d-1)//3), (c=(d-1)mod3), as previously licensed by 2026 community history. Each mapping's minimum hard physical contradictions is counted.
3. **Monotone three-bin decimal maps:** exhaustive partitions of 1..9 at thresholds `1 <= c1 < c2 <= 8`, with 0/1/2 assigned either increasing or decreasing, 56 total codebooks. These include the standard keypad row map and reversed alternatives. Match against the Q4 possibilities under all D4 orientations.

All operations are defined without imputing the missing 42 physical sticker residues. Do not use the observed fit to reclassify the known sticker symbols.

## Results

**Direct native alignment:** no consistent digit→depth function is possible. The same digit **5** appears at native classes **I** and **E**, but the observed Q4 depths force I=2 and E=0. This contradiction rejects every fixed one-digit lookup in the *unrotated* alignment, not only a keypad function.

**After allowing D4 rotations/reflections:**

- Native `IABCDEFGH`: **4 of 8** orientations admit at least one arbitrary consistent digit→depth lookup.
- Alphabetic `ABCDEFGHI`: **0 of 8** orientations admit such a lookup.
- **No D4 orientation** of the native digits permits an exact standard DTMF row or column readout for all nine classes.
- Exactly **one** of the tested 56 monotone mappings × 8 orientations × 2 class orders is compatible: in the native class order, **mirror the digit grid horizontally**, then map 1–5→depth 2, 6–8→depth 1, 9→depth 0. Only digits **3,4,5,6,8,9** actually occur, so the input provides no evidence about 1,2,7 beyond the assumed threshold convention. The resulting nine depths in native order are `222210102`.

The one monotone hit uses cut thresholds (5,8), an **after-inspection parameter choice**. It must not be reported as a recovered intended key.

## Exact matched permutation controls

Instead of random sampling, enumerate all **45,360** distinct reorderings of the digit multiset in `534965398` (three pairs of repeated values: 3,5,9). Preserve the exact Q4 options and apply the same complete operation search to each arrangement.

Number of D4 orientations permitting any arbitrary repeated-digit lookup, in native class order:

| Compatible D4 orientations | Reordered digit strings |
|---:|---:|
| 0 | 4,680 |
| 1 | 15,552 |
| 2 | 18,720 |
| 3 | 4,608 |
| 4 | 1,800 |

The actual ordering yields **4**, the observed maximum. Under this limited matched-null design, **1,800/45,360 = 3.968%** of arrangements do at least as well. But **40,680/45,360 = 89.683%** have at least one compatible orientation, so the existence of *a* rotated lookup is routine.

For the stricter 56-monotone-codebook × 8-orientation search, the distribution of total valid search configurations is:

| Compatible monotone configurations | Reordered digit strings |
|---:|---:|
| 0 | 41,952 |
| 1 | 1,824 |
| 2 | 792 |
| 3 | 456 |
| 4 | 192 |
| 5 | 96 |
| 6 | 24 |
| 7 | 24 |

The actual route gives **one** compatible monotone configuration. At least one occurs in **3,408/45,360 = 7.513%** of matched arrangements.

These are **descriptive** fractions under a particular null, *not* the chance the whole project could discover an attractive correlation. The hypothesis, orientation menu, and test family were motivated by years of experimentation with the same puzzle and were not preregistered. The broader look-elsewhere penalty is unquantified.

## Implications

- The nine-digit URL has a tangible and completely enumerated relationship to the Q4 selector **as a speculative candidate key**.
- Unrotated and natural DTMF-row/column implementations have exact source-backed contradictions under the declared simple family.
- A mirrored, reverse-ordered threshold mapping remains feasible, but its successful cut points are unexplained.
- Testing the *actual artwork* as a registered source of a mirror/turn direction would be a meaningful next discriminator. No mirror direction should be inferred from this match itself.
- Do not convert the conditional nine-depth string to a Steam beta password without specifying another decoder and a separate response. The Steam branch consumer hypothesis remains open.

## Reproducibility and ownership

- Script: [`conjecture_lab_url_digits_q4_depth.py`](../../scripts/conjecture_lab_url_digits_q4_depth.py)
- Source evidence: `data/observations.csv`, Experiments [378](../experiment-378-534brn-one-shot-consumer.md), [380](../experiment-380-534brn-keypad-coordinate.md), [382](../experiment-382-534brn-native-cell-registration.md).
- No physical ledger edits, model changes, password guesses, or changes to previously frozen predictions.

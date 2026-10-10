# CX-E6: exact rail-conditioned null demotes the selectively identified G/H/I XOR

_9 October 2026. Retrospective statistical calibration of the speculative [CX-E5 Boolean control](2026-10-09-cx-e5-ghi-xor-selector.md). Source: [original 66-residue physical freeze](../../data/conjecture-lab-h108-66-residue-freeze-2026-10-09.csv). Reproduce by [pure-standard-library exact rational enumerator](../../scripts/conjecture_lab_cx_e6_exact_xor_null.py). **No original sticker ledger changes and no CE decoding claim.**_

## Why this is necessary

CX-E5 correctly found that exactly one of sixteen Boolean functions is compatible with the twelve **selected G/H/I** three-layer tuples under the speculative `4 / 9 / (9+3)` foreground split: `C=A XOR B`. It then observed 3 of 84 arbitrary three-class selections uniquely identify XOR, correctly flagging a look-elsewhere problem.

But **3/84 counts selections on the *real data***. It is not the likelihood of identifying XOR by chance when the physical observation density, the body/tail slash counts and the already-selected slash rails are fixed. A more appropriate, deliberately favorable null is needed before treating 1/16 or 3/84 as impressive.

## Frozen conditional null, no grammar-driven fitting

Under null N6:

1. Keep the **actual 66 observed H108 residue positions**; unknowns remain unknown. The original 84 source rows, including duplicate residue observations, are not additional independent cells.
2. Retain the physical slash rails in every quarter at **columns 5 and 15**, exactly as originally discovered.
3. Within each of the four 27-site quarters, assign the observed slash/non-slash values **uniformly** among *the remaining observed positions*, preserving the original number of observed slashes **per quarter**. For quarter 4, a non-slash is dot, rather than dash.
4. For the selected G/H/I triple set, treat slash as bit 1 and non-slash as bit 0, enumerate **all 16** truth tables, and permit arbitrary values for unobserved positions. A table survives only if all twelve triples can be completed consistently.

The quarter-conditioned input sizes are:

| Quarter | Observed non-rail sites | Slashes among them | Directly observed G/H/I positions |
| ---: | ---: | ---: | ---: |
| 1 | 17 | 6 | 5 |
| 2 | 15 | 10 | 4 |
| 3 | 16 | 10 | 7 |
| 4 | 10 | 2 | 5 |

Those four independent urns have `C(17,6) × C(15,10) × C(16,10) × C(10,2)` equally weighted assignments. Exhaustively iterating every *overall* combined assignment is unnecessary: enumerate the at most `2^7` relevant patterns within each quarter, weight each by the exact count `C(m−n,k−r)` of unconstrained observed-site assignments, reduce its twelve-triple requirement to a **16-bit survivor mask**, and convolve the four weighted mask distributions by bitwise intersection. The convolution has **123 terminal Boolean-survivor masks**, yielding exact rational probabilities rather than a Monte Carlo approximation.

## Exact surprise level

The event that the particular, retrospectively selected set **G/H/I uniquely yields XOR** occurs with probability

```text
16,267,037 / 128,648,520 = 0.12644558211785104
```

or **12.645%**, even **after holding the observed double slash rails fixed**.

Any unique Boolean function (not necessarily XOR) is also fairly common; exact result is emitted by the same verifier. **This is a direct and substantial downgrade** of the apparent one-in-sixteen uniqueness intuition. It does not prove the XOR story false, but random datasets satisfying the observed physical count/mask constraints produce the same local uniqueness surprisingly often.

### Full 84-subset selection check

The code optionally performs a *seeded, sampling-based* comparison of all `C(9,3)=84` three-class selections on **each randomized dataset**, rather than only counting the 84 selections on the observed one:

```sh
python scripts/conjecture_lab_cx_e6_exact_xor_null.py --draws 20000 --seed 20261009
```

A separate **100,000-draw vectorized cross-check**, made before implementing the repository's standard-library verifier, found:

| Conditional event | 100,000-draw estimated frequency |
| --- | ---: |
| The specifically selected G/H/I uniquely yields XOR | **12.638%** (consistent with the exact 12.645%) |
| At least one of 84 class-triplets uniquely yields XOR | **66.906%** |
| At least three triplets uniquely yield XOR | **49.632%** |
| Mean number of uniquely-XOR triplets | **4.637** |

The actual physical set contains **three** such triplets (`AHI`, `DHI`, `GHI`). That is **not unusual** under this explicit model, which averages more than four. Values from the separate cross-check use PCG64/NumPy and may differ slightly from the repository's seeded standard-library sampling; the exact G/H/I probability is independent of Monte Carlo tooling.

## What this *does* and *doesn't* test

The null respects:

* the physical observation mask, not a filled H108 candidate;
* the observed per-quarter slash counts;
* the actual observed rails, preventing their rarity from being double-counted;
* the original Q4 slash/dot vocabulary;
* all sixteen possible Boolean truth tables and all 84 possible selected class triples.

It does **not** preserve the full hypothesized one-minority-per-nine-frame POS3 grammar or any conditional cube/selector master family. Nor does it correct the very extensive prior search over 12×9, 9×12, 4×27, field lengths, start phases, rotations, matrices and operations. For those reasons, **12.645% is a reference-model probability, not an exact global p-value**. Importantly, a more elaborate structural null could change the numerical value in either direction, so avoid claiming the result has definitively disproved intentional XOR.

The selection of slash rails and G/H/I itself was retrospective. That makes it particularly important that the *conditional* coincidence is already quite ordinary without invoking full multiple-testing costs.

## Decision and next discriminators

1. **Keep the frozen CX-E5 forecasts unchanged** (8=/, 27=/, 35=-, 61=/, 62=/, 99=/, 107=.) and separate from the physical ledger. A future authenticated 8, 62, 99 or 107 sticker remains a legitimate prospective comparison, though the hypothesis's prior plausibility should be discounted.
2. Reclassify **CX-E5 from a high-interest unique transform to a *low-evidence speculative selector***. Do not use its exact 1-of-16 function count or 3-of-84 subset count as positive support by themselves.
3. Prefer independently attested **receiver/instruction and registration**. The [2021 acorn/running-man overlay](2026-10-09-cl13-2021-acorn-overlay-provenance.md) provides an authentic positive-control example where a previous source supplied a recognizable seed and an exact generation number **before** a target image was inspected.
4. The [2019 reversible-cover alternative](2026-10-09-cl14-cover-acorn-historical-clue.md) may account for the old cover clue without CE foreground coupling. Any current cover-to-4/9/(9+3) overlay claim must first defeat that simpler historical explanation.

Reproduce exact result in a few seconds:

```sh
python scripts/conjecture_lab_cx_e6_exact_xor_null.py
```

**Disposition:** selected XOR truth-table compatibility is mathematically real; evidence of intentional CE authoring remains absent, and its apparent statistical rarity is substantially diminished.

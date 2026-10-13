# CL-VLEN-18: Six exact disagreement residues between the minimum-edit tape and U2

*13 October 2026. DISCOVER/DEVELOP, then a frozen **conditional** disagreement table. Neither decoder has been validated; no new sticker has been found.*

## Research question

The new CL-VLEN-14 tape interpretation regards each A–I class as a nine-bit register in the natural cyclic order `IAB/CDE/FGH` (cyclically equivalent to A→…→I→A), and minimizes the number of bit writes required to connect the nine physical class bodies. Its raw-source minimum is **20** writes, with **48** compatible primary-body completions.

But the established U2 conditional model **already** has an independently defined body grammar: within each original nine-symbol serial frame, each of the three interleaved 3-cell depth rails has exactly one minority glyph, either one slash/two dashes in *all three* rails or two slashes/one dash in all three. There are **18** compatible completed bodies under the observed masks, multiplied by **18** class-tail one-hot selector completions = **324 U2** complete 108-symbol candidates. This is not a licence to privilege U2; it is a genuinely competing, already documented structural hypothesis.

How would a literal minimum-write tape and U2 disagree, under **the identical physical corpus**?

## Exact experiment

The new workbench independently reconstructs all U2 primary bodies **from the 54 observed marks** without using U2 model-derived predictions or treating unknown marks as known. Each of nine original nine-site frames is completed under the same three-rail one-minority grammar; the frame choice counts are **1, 1, 2, 1, 1, 3, 3, 1, 1**, yielding **18 primary bodies**. On actual repository checkout the script additionally cross-checks the entire 324-row `data/completion-universe-u2-324.csv` by decoding its native 42-variable little-endian hex encoding and comparing the 18 distinct first-81 body objects. The frozen 42-index order is read from `data/experiment-365-completion-universe.json`. Those two files must not be mistaken for a new physical holdout.

For each of those bodies calculate the exact total class-to-class bit changes on the same cyclic A–I tape, then compare to the raw minimum-of-all-completions of 20.

| Conditional model | Completed body possibilities | Cyclic bit-write minimum |
|---|---:|---:|
| Raw observations + invented minimum-edit prior | 48 globally minimum-write bodies | **20** |
| U2 one-minority primary and one-hot tail | 18 primary ×18 tail = 324 | **34** |

The **18 U2 primary states** require write counts distributed as **34 (8), 36 (4), 38 (4), 40 (2)**. All 18 are disjoint from the 48 minimum-20-edit body states. Choosing an accepted U2 completion would cost at least **14 extra cyclic tape edits** relative to an unrestricted completion. It is not an impossibility for an edit-based reader; the *optimality assumption* and U2 geometry are mutually incompatible.

An exhaustive rank of the natural class cycle against 20,160 unoriented alternative 9-class circular orders **within each completed U2 body** places the natural cycle between roughly the top **7% and 55%** rather than its raw-unknown top-2% standing. This demonstrates that U2's additional one-minority constraints materially change the edit landscape. Neither result proves Playdead favoured smoothness or one-minority geometry.

## Six exact conditional oppositions

Across all **48** minimum-edit bodies, the following 6 missing positions are fixed one way; across all **18 U2** primary bodies, they are fixed the **opposite** way:

| H108 residue | Minimum-edit conjecture | U2 conjecture |
|---:|:---:|:---:|
| 008 | `/` | `-` |
| 016 | `/` | `-` |
| 027 | `-` | `/` |
| 033 | `/` | `-` |
| 035 | `/` | `-` |
| 062 | `/` | `-` |

**These are predictions *conditional on two competing assumptions*, not new observed stickers or confirmed symbol values.** In an admissible prospective comparison, one genuinely new physical reading of any such residue would eliminate the currently frozen *complete minimum-edit* family or the currently frozen *U2* family, subject to that reading's image/serial provenance. A richer decoder could of course survive by relaxing the exact premise that was falsified. A recovered original Playdead source that specifies one instruction language could be an equally strong discriminator without waiting for any more stickers.

The full data file also preserves the 27 primary-unknown residues' predicted slash fractions under both conjecture families. The six above are the **entire exact-opposition set** under the present snapshot; a partial probability disagreement is not an impossible prediction.

## Consequences for instructions involving different-length symbol runs

This is the most concrete reason found so far to develop **an instruction that chooses where bits are written** rather than simply copying a fixed set of symbol chunks. A naive 'minimum 20 changes' reconstruction can fit raw physical marks elegantly while violating the previously well-developed one-minority geometry. A tiny write program that *preserves the U2 geometry* must generate at least 34 changes under A–I cyclic registration.

The next useful architecture is a controlled tradeoff between **(1) completed code's source-native one-minority constraints**, **(2) number of physical-symbol writes**, and **(3) instruction description length**. Source clues should choose which expense matters before any semantic endpoint is read. Without a native cursor/codebook, generating an attractive letter or URL from either family would simply select a model after seeing the desired result.

No owner outreach or additional physical-sticker acquisition is necessary to exploit the disagreement *in principle*: archived photos, provenance-confirmed existing video, and source-authenticated operation descriptions can all discriminate. This is a test strategy, not a request to alter the research goal to collection.

## Reproduce

```sh
python scripts/conjecture_lab_u2_edit_tradeoff.py --test
python scripts/conjecture_lab_u2_edit_tradeoff.py
```

Results: [full 18-body/rank and prediction contrast atlas](../../data/conjecture-lab-u2-edit-tradeoff-2026-10-13.json), [script](../../scripts/conjecture_lab_u2_edit_tradeoff.py). Parent: [contextual instruction and minimum-write campaign](2026-10-13-contextual-instruction-and-minimal-write.md).

**Do not** write any table entry as a known mark in `data/observations.csv`, canonical U2/U5 prediction matrices, current-state narrative or community communications without explicit conditional labeling.
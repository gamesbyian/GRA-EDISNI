# Experiment 323 — Cross-family Q4 holdout comparison

_Status: completed first R5 comparison, 30 Sep 2026._

> **Audit note (Experiment 365, 1 Oct 2026):** the incumbent holdout table keeps full-corpus premises fixed, so by Experiment 340's argument its forced predictions cannot be wrong and "0 exclusions" is guaranteed for both families. The 10/11 vs 3/11 difference measures sharpness of a full-corpus-fitted grammar, **not independent predictive superiority**. See `docs/experiment-365-model-dependence-sweep.md`. **Experiment 366** calibrates this exactly: all 7 of the 330 shuffled tail datasets the incumbent can fit give 10/11, so the count is uninformative; the real comparative evidence is that the incumbent fits only 7/330 arrangements (tail-only: 192/330), an upper-bound likelihood ratio of about 27:1 because the grammar was partly fitted to the same cells.

## Question

R5 asks for holdout comparison across genuinely different grammar families, not only variants of the incumbent machine.

The simplest live nonrecursive rival after Experiments 317–319 is the **tail-index-only family**:

> for each A-I class, exactly one of the three slash/dot tail positions is slash.

This family does not assume primary POS3, G5 address substitution, G6 selector-conditioned q readout, G7 information-preservation, hidden state, route semantics, or terminal `100`.

Can it predict withheld physical tail symbols, and how does its predictive sharpness compare with the incumbent on the same cells?

## Fair comparison domain

The tail-only family does not generate the first 81 slash/dash cells, so scoring it against all 65 observed H108 residues would be meaningless.

The shared predictive domain is the **11 physically observed Q4 residues**:

```
85 86 89 90 92 95 96 97 98 101 108
```

For each residue, remove **all physical records at that H108 residue**, reconstruct the family from the remaining observations, and ask what symbols are possible at the withheld cell.

This prevents repeated serials from leaking the answer.

## Tail-index-only result

Across the 11 Q4 holdouts:

- **3/11** are forced to the correct symbol;
- **8/11** remain ambiguous but include the correct symbol;
- **0/11** exclude the correct symbol.

So the observation-only one-slash family survives every Q4 holdout.

This is genuine predictive behavior, but its current corpus constraints are weak.

## Incumbent comparison

Using the already-frozen leave-one-residue-out incumbent results in `data/sticker-holdout-residue-results.csv` on those exact same 11 residues:

- **10/11** are forced correct;
- **1/11** remains ambiguous but includes the correct symbol;
- **0/11** exclude the correct symbol.

The incumbent therefore supplies much sharper predictions on the shared Q4 domain.

## Important interpretation

This does **not** falsify the nonrecursive tail family.

The simpler family makes fewer commitments and therefore predicts less. Its survival on every holdout means the currently observed Q4 marks do not force G5.

It also means Experiment 318's row/chunk and column/rail readings remain alive: those interpretations change what the selected index *means* for the nine-cell body, but they do not change the tail-cell predictions tested here.

The result should therefore be read as:

> the incumbent earns additional predictive constraint from its extra grammar, while the nonrecursive tail-index family remains compatible with all withheld Q4 observations.

R5 must keep both facts visible. Predictive sharpness is evidence, but extra assumptions are not free.

## G5 consequence

The reset cannot honestly promote G5 to an independently derived premise from this test.

The best current status is:

- G3's one-of-three tail index is independently supported;
- simple nonrecursive meanings remain viable;
- G5 adds substantial predictive structure once assumed;
- no current holdout observation uniquely requires address substitution over the simpler family.

This moves the G5 question toward **discriminating evidence**, not more internal uniqueness proofs.

## Reproducibility

Run:

```bash
python scripts/audit_cross_family_q4_holdout.py
```

The script compares the tail-only reconstruction directly with the frozen incumbent holdout table and asserts the 3/11 versus 10/11 forced-coverage result with zero exclusions in both families.

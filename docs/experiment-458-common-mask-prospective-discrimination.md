# Experiment 458 — common-mask prospective discriminator atlas

_Date: 8 October 2026. Status: scripts executed successfully in [dedicated GitHub Actions run 37748807754](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37748807754). **Prospective prediction freeze**, not new physical confirmation or a solved decoder._

## Question

What would a newly found physical sticker actually **distinguish** between the principal currently frozen explanations, if all explanations use the **same** contemporary 84-record/66-unique-residue observation mask?

Existing experiments generated predictions within different hypothesis families, sometimes under different corpus vintages and without recording their overlapping dependencies. Experiment 458 normalizes the view to the same **42 currently unknown H108 residues**, without re-fitting any hypothesis based on a future sticker.

## Reproducing the test

```sh
python scripts/audit_cross_family_discriminator_atlas.py --summary
python scripts/audit_cross_family_discriminator_atlas.py --out /tmp/experiment-458.json --summary
```

The deterministic script verifies the exact Git blob SHA of `data/observations.csv` (`2bf9f1352c1632986e5c672b4832848fde1e6d0c`), checks the physical 84/66 census and known symbols against all coherent candidate masters, imports the already-reviewed exact model generators, and asserts the original frozen predictions in the Experiment-336, 454 and 456 JSON files. Dedicated CI uploads a machine-readable JSON record containing **every candidate symbol and every pairwise comparison**, rather than only a ranked shortlist. The saved CI artifact from the successful run is named `experiment-458-prospective-discriminator-atlas`.

This is **not** a new independent holdout on the same data. The models were developed with some or all of these observations. Their prospective usefulness comes from falsifiability **after the freeze**, not from claiming retrospectively calibrated posterior probabilities.

## Candidate models, kept distinct

| Label | Current universe or prediction rule | What it licenses | Crucial dependency |
|---|---|---|---|
| `primary_u2` | **324** coherent masters | 3/6 one minority per physical primary column; Q4 one slash per class | Common source for many stronger grammar subsets |
| `depth_identity` | **12** masters | Q4 slash position selects primary **depth**; selected surfaces one dash per physical column | Subset of U2; selected-output condition was developed retrospectively |
| `recursive_u5` | **10** masters | Current canonical two-pass POS3/terminal machine | Shares primary/tail assumptions with U2 and depth |
| `quarter_relabel` | **10** masters | Q4 slash position instead selects a **primary quarter** under one globally shared 120/210 relabel | Explicit extra coordinate-type relabel; alternative output operation |
| `tail_only` | one slash per class, no body model | Q4 symbols only | No claims about first 81 residues |
| `selected_row` | **6** remaining selector assignments | Chosen body row must have exactly one exceptional mark | Discovered post hoc; frozen after Exp 339–340 calibration |
| `identity_copy` | direct matching cross-cube coordinates only | Primary symbols where the observed peer(s) unanimously agree | Poorer than majority baseline in Exp 454; treat as fragile |

The seven **projections are not seven independent theories**. Several share the U2 representation and physical-column premise; the row/tail rivals share the same one-slash code. Counting agreements as multiple votes would overstate the evidence. A model that abstains or allows both symbols has not predicted either specific symbol.

## Result: twelve residues have at least one hard disagreement

The audit ran successfully and found:

```
11, 33, 41, 49, 50, 52, 54, 64, 68, 77, 93, 102
```

However, **eight** of these involve the weak cross-cube copying heuristic and have no hard opposing forecast between the depth/quarter/row families. Among the more structurally interesting comparisons, the decisive **four** are:

| Unobserved residue | Native depth / recursive | Relabelled quarter | Frozen row-one-exception | Interpretation |
|---:|---|---|---|---|
| **50** | `-` | `/` | no opposing singleton | Direct cube-axis discriminator |
| **54** | `-` | `/` | no opposing singleton | Direct cube-axis discriminator |
| **93** | `.` | `/` | `.` | Quarter disagrees with both depth and row |
| **102** | not uniformly forced | `.` | `/` | Quarter versus row; depth cannot be treated as a vote |

Serials no greater than 600: r50 = 50/158/266/374/482/590; r54 = 54/162/270/378/486/594; r93 = 93/201/309/417/525; r102 = 102/210/318/426/534. These are *candidate copies*, not new acquisitions.

The other eight are 11, 33, 41, 49, 52, 64, 68 and 77. Along with 54 they feature copy-versus-depth/U5 conflicts, but the direct-copy heuristic performed **22/33 versus 23/33 majority** in residue holdouts and **19/32 versus 21/32 majority** under held-quarter operation selection (Exp 454). Therefore the six original copy-versus-column disagreements at 11/33/41/64/68/77 remain **lower-confidence stress tests**, not leading methods of selecting a true missing sticker.

## Exact pairwise contradiction inventory

Only nonempty pairwise opposite-forced lists are displayed. Empty pairs and every model's full 42-residue allowed-symbol surface are preserved in the CI JSON artifact.

| Models | Opposite forced symbols at |
|---|---|
| Depth vs relabelled quarter | **50, 54, 93** |
| Recursive U5 vs relabelled quarter | **50, 54, 93** (same ancestral evidence, **do not count twice**) |
| Relabelled quarter vs selected row | **93, 102** |
| Primary U2 vs copy | 11, 33, 41, 64, 68, 77 |
| Depth vs copy | 11, 33, 41, 49, 52, 54, 64, 68, 77 |
| Recursive U5 vs copy | 11, 33, 41, 49, 52, 54, 64, 68, 77 (dependent on depth) |
| Relabelled quarter vs copy | 11, 33, 41, 50, 64, 68, 77 |

No numerical independence weights, Bayesian probabilities or ranked “most likely model” scores are inferred from this table. The exact contradiction set is a **future physical-falsification map**.

## Evidentiary interpretations

1. **The data distinguish prediction readiness from model confirmation.** The depth model may be a compact representation of a real operation, but it was selected using the corpus. Agreement between depth and U5 is structural ancestry, not two observations. The quarter family also shares U2.
2. **The row-vs-quarter collision at residue 102 is newly exposed by cross-indexing existing frozen predictions.** There is no claim it was independently predicted only by this experiment.
3. **No current test makes a conditional model true when its rival is disproved.** A fresh residue 93 slash would falsify these frozen depth and row variants, whereas dot would falsify the frozen quarter variant. A result can be inconsistent with multiple families.
4. **Tail-only does not predict primary residues.** Its blanks in first-81 cells are honest out-of-domain abstentions, not model failures.
5. **Aesthetic or semantic output search is explicitly excluded.** This experiment says where observations would matter; it does not decide what the stickers ultimately instruct.

## What comes next

- Keep existing frozen JSON and this snapshot unchanged when a new owner-confirmed symbol arrives; create a *new* post-observation assessment and record which exact model contracts survive.
- If no new sticker will ever surface, prioritize a **source-fixed external consumer** for the output. Find an authentic interface, plaintext slot, alignment template or exact action format that supplies the transform parameters independently of the candidate model.
- For any future retrospective test, explicitly quantify model-selection cost, use a training-only candidate-rule menu and match the physical holdout mask and baseline. Raw same-corpus success is not a prospective score.
- Avoid speculative new alphabets, arbitrary label relabeling after seeing outputs, and unregistered visual maximization.

**Bottom line:** the coherent structural families disagree most cleanly at **50/54/93/102**; six separate primary-body conflict residues test a significantly weaker direct-copy heuristic. These are falsification targets, not an endgame solution.

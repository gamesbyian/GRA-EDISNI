# Experiment 393 — weighted-prediction sandbox: use guesses as models, not as truth

_Status: completed methodological audit, 4 Oct 2026._

Yes, the existing guess lists can be extremely useful for trying new approaches. But they need to be used as **model ensembles**, not as a fake completed sticker sheet.

This experiment establishes the safe operating rules before doing exploratory decoding.

## Finding 1: the modal guess sheet is not a legal completion

Take the preferred symbol independently at every one of the 43 missing residues and combine it with the 65 observed residues.

That tempting “best guess” 108-cell master belongs to:

- U2: **no**
- U3: **no**
- U4: **no**
- U5: **no**

So the modal prediction table is a perfectly useful residue-by-residue summary, but it is not a coherent possible physical sticker cycle.

This matters enormously for exploratory decoding. Feeding that synthetic master into Braille, image completion, compression, or a cipher can manufacture structures that no legal model actually contains.

## Finding 2: broad U2 frequencies do not secretly rank the U4 candidates

A different tempting move is to treat the 648 U2 completion counts as empirical probabilities and score each U4 master by the product of its per-residue U2 frequencies.

That also fails as a ranking device.

All **20 U4 masters receive the same score**.

That is useful information: the U2 multiplicities are combinatorial symmetry counts, not a hidden posterior telling us which one-shot completion is likelier.

## Finding 3: the familiar 14-state weights are downstream-contaminated for pre-G6 discovery

The support numbers in `data/unobserved-sticker-predictions.csv` are frequencies across the 14 canonical U5 states.

They are not neutral priors.

The clearest example is residue 82:

```
canonical U5 support:
82 = dot   14/14
82 = slash  0/14
```

But Experiments 390–391 show that the two `534brn`-selected one-shot masters both require:

```
82 = slash
```

and are removed precisely by G6.

Therefore a naive weighted search using the old 14-state support numbers would assign zero weight to the strongest current external candidate **because the weighting scheme already assumes the disputed recursive step**.

That would be circular.

## The right way to use the guesses

The prediction lists are still very valuable. Their best role is to create **parallel counterfactual worlds**.

For every proposed new operation, run it across:

- **U2 / 648:** broad physical one-per-column + one-slash universe;
- **U3 / 216:** exact POS3 + established polarity;
- **U4 / 20:** typed one-shot G5 universe;
- **U5 / 14:** recursive incumbent universe;
- **E / 2:** the externally selected `534brn` pair;
- the frozen row-selector rival where relevant.

Then ask:

- does the operation give the same result across a whole ensemble?
- does it sharply reduce an ensemble?
- does it distinguish U4 from U5?
- is the attractive output present only in the synthetic modal sheet?
- which uncertain residues actually control the result?

That converts “AI filling in the blanks” into a disciplined robustness laboratory.

## What weighted support may still do

Support counts can be used descriptively:

- mark high- versus low-uncertainty cells;
- choose sensitivity perturbations;
- prioritize which outputs deserve robustness checks;
- identify operations dominated by a tiny number of guessed residues.

They should not be multiplied into posterior probabilities unless we independently justify a probability model.

## New sandbox rule

A new exploratory result may graduate from the sandbox only if:

1. its operation family was specified before inspecting attractive output;
2. it is tested across coherent completion ensembles;
3. survivor/output counts are reported at each relevant universe layer;
4. any weighting is identified as combinatorial or heuristic rather than probabilistic;
5. the result is rerun without downstream assumptions it is supposed to test.

Experiment 394 applies this immediately to one historically licensed new approach: Braille over the completed 9×12 sticker carrier.

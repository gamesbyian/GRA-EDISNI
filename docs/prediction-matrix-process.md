# Prediction matrix operating process

_Status: active. This process makes the H108 prediction matrix part of normal acquisition, validation, and experiment design._

## Purpose

The prediction matrix is not only a completion table. It is a frozen research surface that tells the project:

- what the current machine predicts for every H108 residue and physical serial;
- how strongly that prediction is supported;
- what kind of uncertainty a new observation would resolve;
- how valuable a newly found sticker would be before anyone inspects its foreground;
- whether later evidence confirms, discriminates between, or contradicts the current machine family.

Canonical residue-level predictions live in:

`data/unobserved-sticker-predictions.csv`

A separate frozen alternative-family probe lives in:

`data/frozen-row-selector-predictions.json`

Do not merge the two files or silently raise incumbent confidence from agreement between them. The row-selector family is an exploratory-but-frozen cross-family rival whose preregistered discriminators are residues 84 and 102.

Physical serial expansion and research-role classification live in:

`scripts/expand_physical_sticker_predictions.py`

Validation methodology lives in:

`docs/sticker-prediction-validation.md`

## Research roles

Every physical serial should be treated as one of the following roles.

### hard_model_test

An unseen residue whose foreground is invariant across the broader currently viable physical family.

A provenance-backed contradiction here is the strongest direct challenge to the present reconstruction. These should receive the highest acquisition attention.

### hidden_state_discriminator

A residue whose foreground varies across the 14 legal hidden states.

A verified observation removes some hidden-state candidates. These should be treated as correlated state evidence, not as independent unknown bits.

### hidden_state_plus_q4_gauge

A Q4 residue that simultaneously carries hidden-state information and sits on the A/C physical polarity gauge.

These are especially information-rich, but interpretation must jointly update hidden state and physical gauge rather than attributing the observation to only one.

### primary_gauge_discriminator

One of the transition-invisible primary physical gauge cells at residues 6, 8, 41, or 45.

These do not test the functional transducer directly. They test which physical representative Playdead printed.

### q4_gauge_discriminator

A canonical-state-invariant A/C Q4 cell whose printed slash/dot polarity can distinguish the exact physical representative while leaving selector depths unchanged.

### broader_branch_discriminator

A residue affected by the broader coupled F+I Q4 branch. These distinguish the canonical route-preserving family from the broader 14-state/terminal-100 sibling.

### repeat_control

A physical serial whose H108 residue has already been observed elsewhere.

These are lower acquisition priority for discovery, but useful controls for confirming the H108 repeat, detecting transcription mistakes, and checking physical-production consistency.

### already_observed

The exact physical serial is already in the canonical observation ledger.

Additional independent imagery can still improve provenance or visual confidence but should not be counted as a new structural observation.

## Acquisition priority

The serial expander emits an integer priority:

1. hard model tests and direct gauge discriminators;
2. hidden-state and broader-branch discriminators;
3. repeat controls;
4. already-observed physical serials.

Priority is about **research information value**, not confidence that a sighting is genuine. Provenance quality remains a separate axis.

When reviewing a new video, photo, post, owner report, auction, or archive:

1. identify the serial number first where possible;
2. compute its H108 residue and research role before inspecting/recording the foreground symbol;
3. freeze the matrix prediction;
4. preserve the source image/frame and provenance;
5. classify the foreground;
6. score the result against the frozen prediction;
7. only then update observations, machine candidates, gauges, or hidden-state survivors.

This order protects the project from hindsight.

## New-observation intake checklist

For every candidate physical sticker observation record:

- physical serial;
- H108 residue;
- expected A-I background;
- predicted foreground set before inspection;
- prediction confidence tier;
- research role;
- source/provenance;
- whether the exact serial was already known;
- observed foreground;
- observed background;
- agreement/disagreement outcome;
- model/gauge/state candidates eliminated;
- whether the observation changed any canonical file.

A newly seen serial that repeats an already-known residue is still useful, but must not be described as a new H108 cell.

## Contradiction protocol

Do not immediately "repair" the model after a disagreement.

For a provenance-backed contradiction:

1. preserve the pre-observation prediction file and commit;
2. verify serial reading and H108 registration;
3. verify symbol/background classification from the raw source;
4. check whether the residue is gauge-sensitive or state-dependent;
5. check for duplicate/residue conflicts in the physical ledger;
6. rerun the relevant exact reconstruction/holdout scripts;
7. only then decide whether the result falsifies a representation prior, a hidden-state candidate, a gauge choice, or the broader mechanical model.

A Tier-A hard-model contradiction is qualitatively different from a disagreement with a modal Tier-C guess.

## Experiment-design use

Before proposing a new sticker-based experiment, use the matrix to state which residue classes can actually discriminate the hypothesis.

For cross-family acquisition, also consult the frozen rival file. In particular, Experiment 336 identifies physical serials 84/102/192/210/300/318/408/426/516/534 as direct tests of the frozen row-selector family. Freeze its expected symbol before looking at any newly recovered foreground.

Good experiments should identify:

- candidate models or gauges being compared;
- the exact residues on which they differ;
- the physical serials in the plausible production range carrying those residues;
- expected symbol under each candidate;
- whether any of those positions are already observed;
- the minimum new evidence needed to decide the fork.

This prevents acquisition requests for stickers that cannot answer the experimental question.

## Historical and prospective scoring

When an old source is recovered, preserve its date and determine whether it can function as a genuine historical holdout. Do not count a same-corpus rendering or a prediction made after the underlying observation as independent validation.

For genuinely new physical evidence, the current committed matrix is the prospective prediction. Score it before revising anything.

## Agent handoff rule

Any agent doing sticker acquisition, video-frame archaeology, social-source mining, owner outreach planning, historical-ledger reconciliation, or alternative-machine work should consult the matrix before assigning value to a sticker lead.

The practical question is not merely:

> Is this sticker new?

It is:

> Which H108 residue is it, what did we predict before seeing it, and what live uncertainty would it resolve?

## Generated physical views

Use:

```
python scripts/expand_physical_sticker_predictions.py --max-serial 600 --unknown-only
```

for the consensus research view.

Use:

```
python scripts/expand_physical_sticker_predictions.py --max-serial 600 --state XYZG
```

for a coherent canonical completion under one legal hidden state.

Do not combine modal state-dependent cells into a synthetic complete master and call it a legal completion.


## Completion-universe companion surface

The frozen preferred prediction matrix remains the prospective test surface for the incumbent model. Experiment 365 adds a different tool: explicit **candidate universes** for asking whether a result depends on the incumbent assumptions.

Before running a new sticker-code experiment, identify the broadest relevant universe:

- U2 (648 masters) for observation-supported 3/6 one-per-column + one-slash-tail questions that should not assume recursion;
- U3 (216) when the established primary polarity staircase and exact POS3 are licensed;
- U4 (20) when first recursive closure is part of the hypothesis;
- U5 (14) for canonical full-machine questions.

Do not report a property found only in U5 as though it were implied by U2. Conversely, a property invariant across all 648 U2 masters is substantially less assumption-dependent than a preferred-master feature.

The residue catalog in `data/completion-universe-residue-catalog.csv` gives U2 partition counts, entropy, background class, and physical serials through 600. Candidate multiplicity is combinatorial, not probabilistic.


## Layer-aware prediction status

Experiment 366 partitions preferred fixed predictions by the weakest completion universe that forces them.

When explaining or prioritizing an unseen prediction, distinguish:

- **U2-fixed:** forced across all 648 broad one-per-column/one-slash structural masters;
- **U3-added:** first becomes fixed under exact POS3 plus established primary polarity (49, 50, 52, 54);
- **U4-added:** first becomes fixed under first recursive closure (93);
- **U5-added:** first becomes fixed under second recursive closure (82);
- **U5-variable:** remains one of the 13 hidden-state residues.

This is separate from the physical-gauge classification. A residue can be fixed inside a representation layer while still lying on a broader physical gauge support.


## Consumer/operation survivor counts

When an independent operation or consumer is proposed, prefer whole-universe survivor reporting over applying it only to the preferred completion.

Record, where applicable:

- U2 survivor count;
- U3 survivor count;
- U4 survivor count;
- U5 survivor count;
- newly forced residues induced by the operation;
- whether the operation is representation-only, a nontrivial filter, or a hard negative.

Experiment 367 is the reference implementation. The frozen row-selector family keeps 144/648 U2 masters and 6/14 U5 masters; the known-password lever replay keeps none.

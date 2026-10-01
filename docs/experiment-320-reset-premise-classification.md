# Experiment 320 — Full reset classification of supplied theorem premises

_Status: completed R4 premise audit, 30 Sep 2026._

## Question

R4 requires every supplied premise in the current theorem graph to be classified as:

- directly observed;
- historically motivated;
- a generic simplicity prior;
- selected because it preserves the machine;
- genuinely derived from independent evidence.

The point is not to relitigate downstream theorems. It is to identify the exact places where the incumbent still asks the solver to choose a grammar.

## Scope

The current transition-side supplied set in `docs/theorem-graph.md` is:

`O1, O2, G1, G3, G5, G6, G7`.

Later hardening has already removed several former premises. Primary polarity, outer no-self registration, Q4 scaffold/control words, route orientation, terminal `100`, hidden-state structure, and most gauge choices are theorem-level or downstream consequences inside the incumbent family.

The structured classification is canonicalized in:

`data/reset-premise-classification.json`

and checked by:

`python scripts/verify_reset_premise_classification.py`

## Result

| node | reset classification | circularity risk | reason |
|---|---|---|---|
| O1 | directly observed | low | H108 and A-I period-9 are corpus-supported structural facts |
| O2 | mixed | low | the 81/27 alphabet boundary is observed; `27q+9d+j` is a convenient coordinate factorization, not independently authored semantics |
| G1 | generic simplicity prior | medium | 3x3/straight-rail geometry and holdouts support it, but exceptional-position ternary meaning is still a local code choice |
| G3 | historically motivated | medium | historical 9+3 body/index thinking plus Experiment 317 independently support a one-of-three tail-index family, but not its downstream meaning |
| G5 | generic simplicity prior | medium-high | literal coordinate-copy and broad uniqueness audits make it compact, but no external cue says “copy selector depth into the body address” |
| G6 | selected because it preserves the machine | high | repeated selector reuse is chosen because it is selectively completion-invariant; no independent self-application cue is known |
| G7 | selected because it preserves the machine | very high | distinct reversible ternary routes are an explicit model-class filter and currently lack an independent route/permutation cue |

No surviving **transition grammar** is classified as “genuinely derived from independent evidence.” That is not a defect in the theorem graph. Premises that became independently derivable have mostly already migrated to T-nodes. It means the remaining reset burden sits exactly at the grammar-entry points.

## Important split inside G3

G3 should no longer be treated as one indivisible assumption.

Experiment 317 independently supports a compact physical fact-family:

> each A-I tail is compatible with one slash marking one of three positions.

Historical discussion also supplies a pre-machine 9+3 body/index interpretation.

Those facts raise the prior for a one-of-three tail index. They do **not** establish:

- that the position is a ternary number;
- that it selects a body depth;
- that it addresses the primary lattice;
- that it is reused recursively.

So R4 promotes the **tail-index architecture** while keeping the **selector semantics** live.

## Highest-priority circularity targets

### G7 first

G7 is the strongest circularity risk because it is both downstream and highly selective. It turns “three functional families exist” into a specific reversible route shell and rejects nearby branches on that basis.

Until a sticker-native or ARG-native route/permutation cue is found, route survival should be reported as conditional on G7 rather than as independent confirmation of the upstream machine.

### G6 second

The second selector application is compact and produces a completion-invariant fixed point, but that is still a machine-internal reason to prefer self-reuse.

The useful next rivals are not arbitrary maps. They are equally simple operations that consume the first-pass surface once without reapplying the same selector.

### G5 third

G5 is better motivated than G6/G7 because literal coordinate-copy families and broad bijection audits independently converge on it **inside recursive-address models**. The missing evidence is earlier: why should the tail be an address/depth substitution at all?

## Auxiliary supplied premises

Two non-core premises remain explicitly quarantined:

- **G8**, the shared/symmetric Q4 physical codebook prior, is a generic authoring-simplicity prior used for physical reconstruction, not a raw observation.
- **R1**, the preregistered observer pointer geometry, remains readout-only. Its evidence is safe only while it is not fed back into transition selection.

## R4 disposition

R4's classification requirement is now complete for the current theorem graph.

The next R4 action is no longer “classify more nodes.” It is to execute targeted rival tests in this order:

1. weaken or independently motivate G7;
2. test simple non-self-reuse alternatives to G6;
3. test nonrecursive, historically motivated uses of the G3 tail before assuming G5.

That ordering follows circularity risk, not incumbent downstream elegance.


## Reset-era update through Experiment 349

Experiments 348–349 strengthen the evidence **upstream of G1** without collapsing the distinction between frame census and positional code.

The historically attested twelve-square representation independently supplies the nine first-81 3×3 frame domains. Experiment 348 shows that raw observations narrow a common unordered binary census to 3/6 or 4/5. Experiment 349 then replays ledger-received chronology and finds the 3/6 family has 4.7907 bits lower predictive surprise than 4/5, a 27.68:1 likelihood ratio under the frozen uniform-completion model.

Accordingly, exact **3/6 frame census** now has an independent reset-era support line. G1 itself remains a generic simplicity prior because G1 additionally says those three minority cells occupy one per column and encode an exceptional-position ternary value. Experiments 348–349 do not establish that stronger positional grammar.


## Reset-era update through Experiment 350

Experiment 350 now justifies splitting G1 itself.

Within the independently supported 3/6 census, a frozen chronological comparison lets unrestricted placement, one-per-row, one-per-column, and permutation-matrix occupancy compete on the historically attested `IAB/CDE/FGH` frame geometry. The row model is physically eliminated by 13 Apr 2020 and the permutation-matrix model by 16 Jan 2020. One-per-column survives and accumulates 5.2450 bits less predictive surprise than unrestricted 3-of-9 placement, a 37.92:1 likelihood ratio under the frozen assignment model.

G1 is therefore now **mixed**:

- 3×3 frame domain: historically motivated;
- 3/6 frame census: independently supported by Experiments 348–349;
- one-per-column physical occupancy: independently supported by Experiment 350;
- interpreting the minority cell's row position as a ternary value: still a generic simplicity/code prior.

The full POS3 transition grammar is not reclassified as independently derived. The reset target has moved inward to the semantic/readout step that turns a supported physical one-per-column pattern into a ternary symbol.

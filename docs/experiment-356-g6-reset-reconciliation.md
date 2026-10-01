# Experiment 356 — G6 second-selector reset reconciliation

_Status: rerun/reconciliation of pre-existing Experiments 291, 322 and 269, 1 Oct 2026._

## Purpose

Experiment 355 moves the highest-priority circularity target from G5 to G6.

G6 asks why, after G5 has used the tail selector to select body depth, the machine should consume the selector again to collapse the remaining q axis.

Before defining any new second-pass family, Experiment 356 inventories and reruns the bounded attacks already present in the repository.

It introduces no new model-selection criterion.

## Frozen prior experiments

### Experiment 291 — four simplest second reads

Starting from the 20 G5 first-pass machines, compare:

- fixed q=0;
- fixed q=1;
- fixed q=2;
- q=S.

No target terminal or expected state count is supplied.

Frozen asserted result:

- all three fixed-q reads keep all 20 machines and produce three different output words;
- q=S is uniquely selective, reducing 20→14;
- q=S is also uniquely completion-invariant in this four-choice family, with all 14 yielding one output.

### Experiment 322 — all deterministic q=f(S) maps

Exhaust all `3^3=27` functions `f:{0,1,2}->{0,1,2}`.

Frozen asserted result:

- 8 maps have nonempty completion-invariant output;
- maximum invariant retention is 14;
- exactly two maps attain 14: `002` and `012`;
- both accept exactly the same 14 physical machines and produce the same invariant output;
- the sole map difference is at S=1, already known to be observationally invisible on the accepted family.

Thus exact identity reuse is not uniquely observable, but the functional second-read is unique modulo a known f1 gauge.

### Experiment 269 — idempotent-retraction grammar

Inside the broader 1,296-map selector-fiber-preserving recursion family, impose the structural requirement that applying the same selector reset twice is idempotent.

Frozen asserted result:

- only 6 maps in the full family are idempotent;
- exactly one has nonempty two-pass positional closure;
- it is the canonical identity operation;
- it leaves the same 14 physical masters.

This is a stronger operation-grammar argument, not an independent sticker observation.

## Reset question

After rerunning these frozen experiments, what remains unsupported?

The expected distinction is:

1. **parameter choice inside a second-selector family**, already strongly bounded;
2. **the higher-order decision to perform a second selector-conditioned collapse at all**, still potentially model-level.

Experiment 356 will preserve that distinction explicitly.

## Reproducibility

Run unchanged:

```bash
python scripts/audit_human_second_selection.py
python scripts/audit_g6_selector_map_family.py
python scripts/audit_idempotent_recursion.py
```

Workflow stdout is preserved as an artifact.


## Historical check: one selector use versus repeated reuse

A targeted pass over the pinned `playdead-unofficial-exports` archive searched sticker-relevant discussion for repeated-selector language (`use it again`, `select again`, `second selector`, `recursive`, `twice`, `second stage`, `layers`, and related phrases).

The strongest relevant historical proposal remains 22 May 2026:

- first nine symbols encode a larger domain;
- final three symbols encode a second number, a smaller subset/index used to pick within the first result;
- examples included keypad-layer selection and page-number + word-index selection.

This is genuine historical support for **one body+index consumption**, and therefore strengthens the architecture upstream of G5.

No recovered pre-machine message in this targeted pass proposes applying that same three-position index a second time after the first selection. Generic phrases about "several stages or layers" do not identify repeated use of the same selector.

Therefore G6's repeated/second selector consumption should remain epistemically separate from the historically motivated body+index architecture.


## Reproducibility repair discovered during rerun

The first hardened rerun exposed two stale assertion bugs in the historical audit scripts. Neither changes the underlying recorded counters or model conclusion.

### Experiment 291 assertion contradiction

The script already asserted the exact fixed-q distributions:

- q=0: three distinct outputs;
- q=1: three distinct outputs;
- q=2: two distinct outputs, `100` and `120`.

It then incorrectly asserted that **all three** fixed-q reads had exactly three distinct outputs. That final assertion contradicted the exact q=2 Counter immediately above it.

Repair: assert the already-established distinct-output counts `{0:3, 1:3, 2:2}`.

### Experiment 322 order-sensitive assertion

The script reverse-sorts records and then compared the two optimal maps against a hard-coded list order `002, 012`. The substantive set is correct, but the list-order check is brittle under the reverse sort.

Repair: compare the two optimal map/output pairs as an unordered set.

These are regression-harness repairs, not changes to the candidate family, scoring rule, or expected substantive results.


## Successful repaired rerun

After repairing the two regression-harness bugs above, the hardened rerun succeeds and preserves nonempty evidence for all three audits.

- workflow run: `36820725086`
- artifact: `11143231706`
- digest: `sha256:eb841b3985857b8304e2169f77bb84abd25db220663200f3dd17f89c39b0b24b`

### Experiment 291 reproduced

From the 20 G5 first-pass machines:

- fixed q=0: 20 valid, outputs `122/102/112`;
- fixed q=1: 20 valid, outputs `022/012/002`;
- fixed q=2: 20 valid, outputs `100/120`;
- q=S: 14 valid, all output `100`.

Thus q=S is the only member of the four-choice family that is both selective and completion-invariant.

### Experiment 322 reproduced

All 27 deterministic `q=f(S)` maps were rerun.

- 22 are selective;
- 8 have nonempty completion-invariant output;
- maximum invariant retention is 14;
- exactly `012` and `002` attain 14;
- both give `100` for all 14 machines;
- both accept the exact same 14-machine set;
- their only difference is the known S=1 observational gauge.

### Experiment 269 reproduced

Inside the 1,296-map selector-fiber-preserving family:

- 6 operations satisfy idempotence;
- exactly 1 has nonempty two-pass positional closure;
- it is the canonical identity reset;
- it leaves the same 14 physical masters and terminal `100`.

## Reset interpretation

G6 has the same epistemic shape that G5 acquired after Experiment 355.

Its **parameterization inside natural bounded families is strongly constrained**:

- the four simplest second reads isolate q=S;
- the full 27-map deterministic family isolates one functional solution modulo a known gauge;
- the broader idempotent-retraction grammar uniquely selects canonical identity.

But the historical archive check finds no pre-machine instruction to apply the same three-position index a second time. The May-2026 body+index discussion supports one selector use, not recursive reuse.

Therefore the remaining G6 burden is a parent-family/authoring prior:

> after the first selector-conditioned depth reduction, require another selector-conditioned information reduction that is completion-invariant and information-preserving.

Do not broaden to arbitrary second-pass functions merely because they can be enumerated. Existing bounded families already show that parameter freedom is not the main uncertainty.

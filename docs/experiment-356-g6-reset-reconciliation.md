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

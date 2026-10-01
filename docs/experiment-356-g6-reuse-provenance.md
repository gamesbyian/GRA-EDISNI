# Experiment 356 — G6 second-selector reuse provenance audit

_Status: completed bounded archival/reset audit, 1 Oct 2026._

## Question

After Experiments 353–355, G5 is no longer primarily a parameter-choice problem. Inside the natural information-preserving selector-on-body families already tested, the first selector application is strongly constrained.

The highest remaining circularity target is G6:

> after G5 has used the tail selector to choose body depth, use the tail selector again to consume the remaining q coordinate.

This experiment asks the pre-machine provenance question:

> Is there any independently recovered historical/community clue that explicitly motivates reusing the same tail/index a second time?

No downstream machine output is used to answer this question.

## Frozen evidence

Primary archival source:

- `gamesbyian/playdead-unofficial-exports`
- commit `5e5897e2ce70dad5a2bd85e459770637cb36610f`
- especially `Playdead Unofficial - ARG - solving-breakout [463106924708233216].txt`

Search vocabulary covered explicit and near-equivalent self-reuse language:

- reuse;
- use again;
- apply again;
- repeat selector;
- recursive / recursion;
- same selector again;
- second selection;
- last three bits again;
- index again;
- smaller subset;
- selector / index;
- hierarchical body+index wording.

The audit also checks the already-canonical historical findings from Experiments 351 and 353.

## Positive historical evidence recovered

The archive does independently support:

1. three-position / ternary-like local coding as a historically explored operation class;
2. a 9+3 or body+index architecture;
3. the idea that the last three positions can select a smaller subset within a larger domain;
4. multi-stage/layered decoding as a generic possibility.

The clearest body+index statement is the 22 May 2026 proposal that the first nine symbols encode a larger domain and the last three encode a second number selecting within it.

That supports **one selector application**.

## Negative result

No recovered pre-machine message in the frozen archive says, or clearly implies:

- use the same three-position selector a second time;
- recursively reapply the tail/index;
- consume the remaining q axis with the same selector;
- perform a second address substitution;
- iterate the body+index operation until a fixed point;
- use the first-pass output as a new selector target.

The archive therefore does not independently supply G6 self-reuse.

This is an absence-of-evidence result over the preserved searchable corpus, not proof that no such thought ever existed in an unarchived message or missing attachment.

## Structural evidence already present

Although historical provenance is negative, G6 is not unconstrained internally.

### Experiment 291

After G5 leaves 20 first-pass machines, compare four paper-and-pencil q choices:

- q=0;
- q=1;
- q=2;
- q=S.

The three fixed-q reads retain all 20 machines and produce multiple outputs. Reusing `S` is uniquely both selective and completion-invariant, reducing 20→14 and yielding one common output.

### Experiment 322

Exhaust every deterministic one-shot map:

```
q = f(S),  f:{0,1,2}->{0,1,2}
```

There are 27 such maps.

Eight give nonempty completion-invariant output. Maximum invariant retention is 14, achieved only by:

- `002`;
- `012`.

They accept the exact same 14 machines and differ only at the established S=1 observational gauge.

Thus exact identity reuse is not uniquely observable, but the functional selector-conditioned second read is unique modulo gauge under the frozen criterion.

### Experiment 269

Inside a much broader 1296-map selector-fiber-preserving recursion family, imposing idempotent retraction semantics leaves six maps structurally; only the canonical identity operation has nonempty two-pass positional closure, recovering the same 14 masters and terminal.

This is stronger operation grammar, not external evidence.

## Epistemic result

G6 should be split into two claims.

### Historically unsupported

> The same tail/index is intended to be applied a second time.

No independent historical cue currently supplies this.

### Strongly constrained once second use is admitted

> If the remaining q coordinate is consumed by a deterministic selector-conditioned map and completion-invariant maximum retention is required, the functional result is unique modulo the known S=1 gauge.

This is supported by Experiment 322 and strengthened by 291/269.

## Consequence

G6 remains a generic operation prior, but its uncertainty is concentrated in the **decision to perform a second selector-conditioned read at all**, not in the exact map once that family is entered.

Future work should not keep expanding arbitrary `f(S)` families; that space is exhausted.

The next useful evidence would be one of:

1. an external/historical clue explicitly suggesting repeated selection, recursion, retraction, or iteration;
2. an independently motivated stopping rule that prefers a second read over simply retaining the three first-pass q surfaces;
3. a competing equally simple one-shot consumer of the first-pass three-surface object, preregistered before inspecting route/terminal semantics.

Absent such evidence, report G6 as conditional rather than independently derived.

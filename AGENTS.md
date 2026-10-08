# AGENTS.md

## Mission

Determine the INSIDE Collector's Edition sticker mechanism from the closed corpus without privileging the current ternary-machine interpretation. Preserve the existing machine as a mature hypothesis family, but make it compete against simpler and historically demonstrated Playdead puzzle grammars. Do not assume future sticker recovery.

The active epistemic-reset protocol is `docs/sticker-epistemic-reset.md`. The cross-puzzle operation prior is `docs/arg-puzzle-mechanics-corpus.md`. The complementary conjecture protocol is `docs/conjecture-lab-protocol.md`; these serve different research purposes.

## Session recovery

Read only these first:

1. `docs/sticker-epistemic-reset.md`
2. `docs/current-state.md`
3. `docs/research-queue.md`
4. `docs/arg-puzzle-mechanics-corpus.md`
5. `data/machine-spec.json`
6. `docs/community-glossary.md`
7. `docs/community-conventions.md`

Use `docs/experiment-ledger.md` to check whether an idea has already been tested. Query the long-form Google Docs only for details that are not represented here.

Do not begin a session by rereading large tails of the Google Docs.

Baseline verification:

```bash
python scripts/verify_machine.py
```

For proof-chain or model-structure changes, also run:

```bash
python scripts/verify_proof_pack.py
```

## Evidence discipline

Keep these categories separate:

- raw physical observation;
- local reconstruction;
- model-class selection;
- machine-derived consequence;
- observer/readout;
- semantic hypothesis;
- manufacturing/provenance context.

A derived property does not become independent evidence for its own premises.

The preserved Discord 108-cell master is an exact same-corpus rendering of `data/observations.csv`; use it for historical chronology/registration provenance, never as an independent holdout for the machine.

Do not multiply matched-null frequencies or code-space densities as if independent.

## Explicit conjecture research mode

The project authorizes three distinct modes. Declare which one is being used in a report, script or agent handoff:

1. **DISCOVER (exploratory):** propose a hunch even if no prior ARG source licenses it; backsolve from a known answer, inspect visually pleasing outputs, explore dictionaries, invent provisional mappings and follow several unsupported but visible assumptions. Call every chosen-after-inspection parameter *fitted* and every observed match *exploratory*, never a blind prediction.
2. **DEVELOP (conditional):** temporarily adopt a versioned hypothesis as true long enough to deduce its full consequences, candidate receiving artifact, human solution path, costs and a risky independent prediction. Keep contradictory variants separate. Source absence alone is not a logical falsification.
3. **VALIDATE (confirmatory):** require the source-native operation, frozen parameters, controls, accurate dependence labels, physical confirmation or independent downstream response before elevating a candidate to a finding. All existing strict evidence rules apply fully.

These modes can run concurrently. They are **not evidence grades**. A successful exploration can end in a demonstrably wrong model and still be useful. Record an assumption stack and exact candidate selection history; exploratory data reuse never creates independent confirmation.

The quarantine below prohibits evidence-free **claims and repeated confirmatory tests**. It does not prohibit a labeled, budgeted DISCOVER/DEVELOP attempt. Previously falsified *fixed* implementations remain falsified; don't silently revive them by changing their parameters.

Keep conjecture work in `docs/conjecture-lab/` or separately named exploratory scripts, away from `data/observations.csv`, the physical ledger, source provenance, frozen predictions and the canonical machine spec. See `docs/conjecture-lab-protocol.md` and the [methodology audit](docs/conjecture-led-research-audit-2026-10-08.md).

## Closed-corpus rules

- Treat all 14 physical completions as live unless a machine-native operation eliminates them.
- Generic compression, visual tidiness, English-looking output, lore resemblance, endpoint arithmetic, and arbitrary transforms do not select a completion.
- Operate on the whole symbolic family whenever possible.
- New stickers are bonus validation only, never the next required step.

## Current semantic quarantine (for validated claims)

Do not reopen as **confirmatory findings** without an independently supplied operation or clue. Named alternatives may be explored with explicit hypothesis selection and a limited budget in the conjecture lane:

- XML
- MIX
- MISS / MISSION / MISSING
- generic Braille continuation
- 621 / 648 endpoint arithmetic
- generic alphabet searches
- bitmap/pixel-art fitting
- arbitrary Boolean combinations of pointer bits
- terminal printer-mask optimization

## Community language and presentation

For human-facing prose, tables, diagrams, historical summaries, acquisition work, and explanations, prefer the established community terminology and conventions documented in `docs/community-glossary.md` and `docs/community-conventions.md` when they are sufficiently precise.

Preserve historical source wording where possible. Use present-project formal terminology when it adds necessary precision, but introduce it after the community term rather than silently replacing the community's language.

Write in a way that is compatible with the community's vocabulary and visual conventions without implying that the agent is a community member or participant. Color conventions are artifact-specific; use the legend belonging to the source artifact.

This preference applies to presentation. It does not require renaming code identifiers, experiment IDs, machine-state variables, or exact theorem language.

## Incumbent-machine quarantine

`data/machine-spec.json`, the theorem graph, prediction matrix, terminal `100`, hidden-state variables, gauges, POS3, selector and routing language describe the incumbent machine hypothesis. They remain valid when discussing or testing that family, but must not be used as Layer-0 observations or as the default vocabulary for generating new hypotheses during the reset.

Before extending that family **in VALIDATE mode**, ask whether the operation is independently motivated by raw sticker evidence, historical community work, or a demonstrated ARG mechanism. In DISCOVER/DEVELOP it may be extended provisionally, but must not inherit an evidential advantage from the work already invested in the incumbent. See `docs/sticker-epistemic-reset.md`.

## Exact machine language

When discussing the incumbent machine, use the terms carefully:

- **registered one-hot primary code**
- **Q4 one-slash-per-depth-stack selector**
- **request bits** `X=[x=2]`, `Y=[y=2]`
- **priority-free two-request MUTEX relation with explicit middle idle/fallback**
- **route reindex** `q=2-p` via `210`
- **completed Q3 route table** `102 / 012 / 120`
- **selector reuse / canonicalization**
- **terminal** `100` / frame 9 / raw `---//////`
- **observer layer** separate from **generative transition layer**

Do not call the whole object a synchronizing automaton, universal computer, ECC, or monoid without the relevant caveat.

## Work hygiene

For each new experiment:

1. In VALIDATE, state the bounded parent family or operation before inspecting attractive outputs; in DISCOVER/DEVELOP, state your assumption stack and disclose which parameters or outputs were chosen after inspection.
2. Prefer exact enumeration over sampling when the space is small.
3. Record negative results.
4. Add a compact ledger entry.
5. Update `docs/current-state.md` only if the current model changes.
6. Update `docs/research-queue.md` when priorities change.
7. Append full prose to the Google Results/Diary only after the result is stable.

Commit small, coherent changes often.

## Code

Scripts should be deterministic and dependency-light. Prefer the Python standard library unless a dependency materially improves the work.

Every script that encodes a claimed invariant should fail loudly if the invariant breaks.

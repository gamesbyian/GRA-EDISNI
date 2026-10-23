# AGENTS.md

## Mission

Determine the INSIDE Collector's Edition sticker mechanism from the closed corpus without privileging the current ternary-machine interpretation. Preserve the existing machine as a mature hypothesis family, but make it compete against simpler and historically demonstrated Playdead puzzle grammars. Do not assume future sticker recovery.

The active epistemic-reset protocol is `docs/sticker-epistemic-reset.md`. The cross-puzzle operation prior is `docs/arg-puzzle-mechanics-corpus.md`. The complementary conjecture protocol is `docs/conjecture-lab-protocol.md`; these serve different research purposes.

## Agent dispatch and session recovery

Start from the current default branch and inspect open research PRs before taking an experiment. `docs/research-queue.md` owns live priority; `docs/current-state.md` owns current conclusions; `docs/experiment-ledger.md` owns reproducible attempts/negatives. Their chronological length is **not** a priority ordering: read the current top and query relevant IDs/phrases before historical tails. Google Docs are historical long-form context, not a parallel dispatch board.

| Work | Minimal route |
|---|---|
| New hypothesis / challenge to incumbent | `docs/sticker-epistemic-reset.md`, `docs/arg-puzzle-mechanics-corpus.md`, `docs/conjecture-lab-protocol.md` |
| Existing experiment / next discriminating run | Relevant research-queue entry, exact ledger ID and existing script/fixture; check prior negatives |
| Machine, closure, theorem or predictions | `data/machine-spec.json`, `docs/current-state.md`, relevant proof/observation fixture |
| Sticker acquisition, archival leads, community claims | Provenance/physical ledger, community glossary/conventions, corresponding source audit; distinguish original source from mirrors and recollections |
| Twenty-perspective portfolio | `docs/perspective-driven-sticker-experiments-2026-10-16.md`, `data/perspective-experiments-2026-10-16.json`; preserve all 27 PX IDs |
| Software/tooling change | Owning script and tests, then `python scripts/verify_machine.py`; proof changes also `python scripts/verify_proof_pack.py` |

Avoid rereading large Google Doc tails at the start of a session. Use `docs/community-glossary.md` and `docs/community-conventions.md` when reporting to readers or comparing community methods.

### Work contract

1. State whether work is DISCOVER, DEVELOP or VALIDATE before claiming its result; record assumption stack, what was fitted after viewing results, dependent sources and candidate selection. **Exploration is welcome; promotion needs independent discrimination.**
2. Define one bounded question, the cheapest test, controls/null family, expected informative outcomes and stop rule. Reuse existing scripts and evidence before collecting more. Negative and inconclusive results are durable outcomes, not invitations to silently rerun.
3. Keep hypotheses competing. Incumbent-machine structure cannot justify itself, and an archival copy of the same observation is not an independent witness. Distinguish actual absence from search/provider failure and original Playdead source from fan reconstruction.
4. Work in focused commits/PRs, reconcile parallel branches before edits, and update the *single owning* queue/ledger/state document where a result changes facts. Do not inflate all three with duplicated narrative.
5. Finish with executable script/fixture and exact command/results or a justified no-change disposition. Handoff records the candidate, evidence grade, independent observations, failed premises, next discriminating action and source/commit identity. Never describe a speculative decode as solved.
6. Research about people or communities uses public provenance responsibly. Do not contact sticker owners, impersonate community members or initiate outreach in the owner's name without a current explicit request.

The standing baseline is `python scripts/verify_machine.py`; run `python scripts/verify_proof_pack.py` for proof-chain/model-structure changes. For portfolio updates, also run `python scripts/check_perspective_queue.py`.

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

- Keep every completion consistent with the **declared conditional grammar** alive until new observations or valid model-native constraints eliminate it. The historical 14-master U5 count predates physical sticker 427; on the current 84-record/66-residue corpus, recursive U5 has **10** conditional masters, while broader U2 has **324**. Neither represents all raw 42-cell completions.
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

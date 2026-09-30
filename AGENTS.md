# AGENTS.md

## Mission

Crack the INSIDE Collector's Edition sticker-code mechanism using the current closed corpus. Do not assume future sticker recovery.

## Session recovery

Read only these first:

1. `docs/current-state.md`
2. `docs/research-queue.md`
3. `data/machine-spec.json`
4. `docs/community-glossary.md`
5. `docs/community-conventions.md`

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

## Closed-corpus rules

- Treat all 14 physical completions as live unless a machine-native operation eliminates them.
- Generic compression, visual tidiness, English-looking output, lore resemblance, endpoint arithmetic, and arbitrary transforms do not select a completion.
- Operate on the whole symbolic family whenever possible.
- New stickers are bonus validation only, never the next required step.

## Current semantic quarantine

Do not reopen without an independently supplied operation or clue:

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

## Exact machine language

Use the terms carefully:

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

1. State the bounded parent family or operation before inspecting attractive outputs.
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

# Closed-corpus cryptanalysis tooling pilot (12 October 2026)

**Research mode: DISCOVER / DEVELOP.** No new physical observations, decoded
foreground, inferred password, or independently confirmed consumer. The
single nontrivial integration in this PR is Z3. This is an operational tooling
decision, not an endorsement of the incumbent ternary-machine hypothesis.

## Decision

The repository already has unusually strong purpose-built standard-library
enumerators, exact controls, source-adjacent consumers, and a documented
experiment matrix. Third-party tools must earn their footprint by providing
something that those scripts do not already do.

| Tool | Role | Integration decision | Limitation |
| --- | --- | --- | --- |
| [Z3](https://github.com/Z3Prover/z3) (MIT) | SMT Boolean, bit-vector, string and mixed logical constraints; witnesses, unsatisfiable cores, incremental assumptions | **Pilot now:** optional standalone script with observation-only positive and negative controls | Will not recognize a cipher or assign probability by itself; a SAT solution is only conditional on supplied constraints |
| [OR-Tools CP-SAT](https://github.com/google/or-tools) (Apache-2.0) | Bounded permutations, exact cover, assignment and optimization, exhaustive candidate sets | **Next only after benchmark:** compare with a nontrivial existing search, preserving identical fixture and solution set | Optimization objective can import arbitrary aesthetic preferences; SAT model counts may be expensive |
| [CyberChef](https://github.com/gchq/CyberChef) (Apache-2.0) | Reproducible composed decoding, encoding, compression, XOR and byte transforms | **Candidate for next pilot:** saved Node recipes for a *typed*, source-supplied candidate output | General transform guessing has huge look-elsewhere effects; Node v24 currently required |
| [Ghidra](https://github.com/NationalSecurityAgency/ghidra) (Apache-2.0) | Disassembly and decompilation of **lawfully obtained local** INSIDE game code; strings, resources, alternative-branch/check validation research | **Highest consumer priority:** establish platform/version/asset hashes and one concrete receiving entrypoint, then automate a narrow headless report | No original distributable binary in this PR; static-analysis inference must be tested on the actual build |
| [angr](https://github.com/angr/angr) (BSD-like) | Python symbolic execution of a concrete consumer validation path | **Conditional follow-up:** only after Ghidra/archaeology identifies an accessible local target | High setup and path-explosion costs; not useful as an unconstrained mystery solver |
| [Ciphey](https://github.com/Ciphey/Ciphey) | Heuristic recognition of common classical encodings | **Manual exploratory triage only** once a candidate byte/string representation is supplied | False positives; cannot reason from the raw slash/dash/dot corpus or substitute for input-grammar evidence |

Do **not** add all packages to the main verification environment or vendor their
sources. Prefer one version-pinned, artifact-producing standalone probe per
independently motivated experiment. No unbounded web endpoint testing, bulk
password submission, or exploitation of third-party infrastructure.

## What is actually integrated

`scripts/audit_z3_tail_constraints.py` reads the existing observation-only
loader (`scripts/audit_tail_metadata.py`) and compares two **competing,
historically discoverable 9 × three-position tail grammars**:

- one slash among each A-I class's three slash/dot tail marks;
- one dot among each A-I class's three marks.

For both families, the physical records are hard constraints; unseen tail
symbols remain free. The SMT script:

1. checks satisfiability with only raw observations (no machine state);
2. enumerates the *small* surviving one-slash family, capped at 10,000;
3. checks its count and per-class choices against the existing independent
   standard-library enumeration;
4. outputs the backbone (symbols shared by every survivor) and unforced
   tail residues, with **no invented predictions**;
5. obtains a deletion-minimal raw-observation contradiction for one-dot.
   A minimal conflict is not a minimum-cardinality global proof.

Historical [Experiment 317](experiment-317-tail-metadata-observation-audit.md)
recorded **36** compatible one-slash assignments on the earlier corpus.
The owner-confirmed sticker **427 (dot at residue 103, class D's third
tail slot)** eliminates half the alternatives; **18** survive on the present
84-record/66-residue corpus, and class D's slash is forced at position 1.
The one-dot rival still has **0** compatible assignments. Both the existing
standard-library audit and the new SMT pilot now assert these *current*
numbers, retaining the old 36 as an explicitly dated historical result.
This migration was surfaced by the initial red CI run of PR #182.

Neither historical nor current counts constitute decoding evidence. If future
physical discoveries change these assertions, fail loudly and re-audit the
corpus change instead of silently updating the expected results.

Run locally, on an explicitly opted-in Python 3.12 environment:

```sh
python -m pip install z3-solver==4.16.0.0
python scripts/audit_tail_metadata.py
python scripts/audit_z3_tail_constraints.py
```

Use **Run workflow** for
[`z3-constraint-smoke.yml`](../.github/workflows/z3-constraint-smoke.yml)
or review the targeted PR-path smoke job. The main `verify.yml` matrix is
intentionally unchanged; it must not pay the solver installation cost on every
unrelated research change.

## Research priorities under a fixed corpus

### A. Receiving-artifact bypass (highest expected leverage)

For each source-authenticated candidate, record the physical/source provenance,
platform and version, available bits, candidate entrypoint, input type and
independent acceptance witness. Prioritize local offline analysis of:

1. Known platform-specific input surfaces and branch/version metadata, including
   the Steam beta-password hypothesis now explored on a separate PR.
2. Historical printer and website consumers, carefully distinguishing archived
   *actual input handlers* from screenshots or speculative endpoint shapes.
3. Recovered Terminal41 content and game assets that may contain the target
   information even if no foreground message is deciphered.

A separately independently discovered receiving mechanism can recover actionable
information without complete sticker reconstruction. **No receiver is currently
verified for the CE foreground.** Do not assert that an INSIDE Steam branch has
accepted a sticker-derived code.

### B. Constraint-engine tournament

Pick one bounded, frozen, currently expensive question with independent controls
and benchmark Z3 vs OR-Tools vs our existing enumerator. Measure:

- exact surviving solution set (not merely cardinality);
- time and peak memory on identical hardware;
- ability to produce minimal contradictions/forced symbols;
- stability under 66-observed-residue and alternate corpus vintages;
- preservation of assumption labels and dependence clusters.

If the custom enumerator wins, retain it. Solvers are components, not prestige
upgrades. Use observer-neutral models before encoding any POS3/recursive grammar.

### C. Reproducible transform/consumer searches

For every proposed Byte/Text consumer, freeze before the run:
source hash, initial alphabet, alignment, transforms and parameters, target
acceptance behavior, and selection history. Run matched nulls on candidate
representations; report attempted transformations and rejected ones. A readable
word selected after thousands of recipes is DISCOVER output, never VALIDATE.

## Independent adversarial review

Give one research lane permission to eliminate 108-as-one-message, serial
ordering, ternary status, nine-cell frame semantics, and text as the output.
Any simpler source-native pathway that bypasses a foreground reconstruction
should be escalated with the same provenance and exact validation standards.

## Next concrete deliverable

Obtain and classify a **single version-identified local input-consumer witness**:
a function or archived active form with input grammar, observable accept/reject,
and independent source provenance. If available, implement the smallest
reproducible offline probe; only then consider angr, a CyberChef recipe, or
enumeration of a predeclared finite password hypothesis. No new stickers or
Playdead contact are dependencies.

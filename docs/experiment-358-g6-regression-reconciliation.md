# Experiment 358 — G6 regression reconciliation

_Status: reproducibility repair and current-main rerun, 1 Oct 2026._

## Purpose

Canonical Experiment 356 (`docs/experiment-356-g6-reuse-provenance.md`) cites Experiments 291, 322 and 269 as structural support for G6 while correctly finding no independent historical cue for a second use of the selector.

During an independent attempt to rerun those audits, two stale regression assertions were discovered. Experiment 358 repairs those assertions without changing any candidate family, scoring rule, expected counter, or substantive conclusion, then reruns all three audits under a harness that preserves evidence and fails if an expected experiment marker is absent.

This is a reproducibility repair, not a new G6 model-selection result.

## Repair 1 — Experiment 291

`audit_human_second_selection.py` already asserted exact fixed-q output counters:

- q=0 has three distinct outputs;
- q=1 has three distinct outputs;
- q=2 has two distinct outputs, `100` and `120`;
- q=S has one output, `100`, across 14 survivors.

A later blanket assertion incorrectly required all three fixed-q choices to have exactly three distinct outputs. That contradicts the exact q=2 Counter immediately above it.

Repair:

```
{q: len(records[q]) for q in (0,1,2)} == {0:3, 1:3, 2:2}
```

## Repair 2 — Experiment 322

`audit_g6_selector_map_family.py` correctly identifies `002` and `012` as the only maximum-retention invariant maps.

The regression check compared those two map/output pairs as a hard-coded ordered list after the records had been reverse-sorted. The ordering is not substantive and could disagree with the literal expected order.

Repair: compare the optimal map/output pairs as an unordered set.

## Hardened rerun

`scripts/rerun_g6_reconciliation.py` executes, in-process:

- Experiment 291;
- Experiment 322;
- Experiment 269.

For each audit it executes all assertions, captures stdout/stderr, requires an experiment-specific marker, preserves stdout and any traceback, writes a structured summary, and fails only after all three audits have been attempted.

The workflow uploads the evidence artifact even on failure.

## Expected substantive reproduction

No substantive result is changed by these repairs.

Expected Experiment 291 result:

- fixed q=0/1/2 all retain the 20 first-pass machines;
- fixed q outputs are non-invariant;
- q=S uniquely reduces 20→14 and is completion-invariant.

Expected Experiment 322 result:

- all 27 deterministic q=f(S) maps are exhausted;
- 8 have nonempty invariant output;
- maximum invariant retention is 14;
- only `002` and `012` attain 14;
- they accept the exact same 14 machines.

Expected Experiment 269 result:

- among 1,296 selector-fiber-preserving operations, 6 are idempotent;
- exactly one idempotent operation has nonempty two-pass positional closure;
- it is canonical identity, with 14 physical masters.

## Relationship to Experiment 356

Experiment 356 remains the canonical provenance conclusion:

> no preserved pre-machine evidence independently instructs a second selector reuse.

Experiment 358 only strengthens the reliability of the structural support Experiment 356 cites. It does not change G6's epistemic classification.

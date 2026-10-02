# Experiment 363 — can continuity actually recover the PC acorn order?

_Status: completed reconstruction-control audit, 2 Oct 2026._

## Why this follows Experiment 362

Experiment 362 established a useful but narrower fact: the known PC acorn order has much greater aligned-symbol continuity than random row permutations.

That does **not** imply that maximizing continuity would reconstruct the acorn. A score can distinguish a known solution from random arrangements while still preferring many wrong arrangements even more strongly.

Experiment 363 tests that inverse problem.

## Input and score

Use the same 32-row fixtures and the same full-width score as Experiment 362:

- `data/printer-reference/pc-ps4-raw.txt`;
- `data/printer-reference/pc-ps4-acorn-order.txt`;
- +1 for each aligned equal symbol between adjacent rows;
- -1 for each aligned unequal symbol.

The canonical acorn score is 176.

## Search

Exact optimization over 32! paths is unnecessary for the question. It is enough to find reproducible counterexamples whose score exceeds the canonical order.

Use a deterministic heuristic with seed 363:

1. 100 greedy nearest-neighbor starts, each beginning from a seeded random row;
2. greedily append the unused row with maximum pairwise continuity;
3. repeatedly accept the first improving row swap;
4. then repeatedly accept the first improving contiguous subsequence reversal;
5. stop each restart at a local optimum.

The search is deliberately simple. Finding even one non-acorn order above 176 proves that continuity maximization does not identify the canonical reconstruction.

## Result

Across 100 deterministic restarts:

- canonical acorn score: **176**;
- worst local optimum found: **296**;
- mean local optimum: **314.9**;
- best local optimum: **328**.

The best 328-point arrangement shares only **9 of the canonical 31 undirected row adjacencies**.

Therefore the score that makes the known acorn look highly nonrandom under Experiment 362 is **not sufficient to recover the acorn order by optimization**.

## Interpretation

Experiments 362 and 363 together establish two different properties:

1. **Detection:** the real acorn arrangement has a strong continuity signal relative to random permutations.
2. **Reconstruction:** maximizing that signal alone overfits and produces much smoother wrong arrangements.

This is exactly the failure mode we wanted to guard against on the sticker puzzle. It explains why “find the smoothest row arrangement” is dangerous even when the underlying puzzle genuinely is a scrambled image.

For H108, the situation is weaker still:

- known/preregistered orders do not show the PC-like positive continuity signal;
- optimized H108 orders fail held-out sticker prediction;
- and the positive-control PC puzzle proves that blind optimization would be unsafe even if a real image were present.

The productive historical lesson is therefore not “maximize neighboring similarity.” The printer solves used **additional row-edge/interlace/boundary constraints** to restrict the candidate order before visual coherence became meaningful.

## Consequence for future row-order work

A future sticker ordering proposal should pass three gates:

1. **independent constraint:** derive candidate adjacency/order from a sticker-native or historically attested side channel;
2. **positive-control calibration:** if the proposed operation claims printer ancestry, show that it can recover or materially constrain the corresponding solved printer puzzle;
3. **blind sticker utility:** improve held-out H108 prediction or make a preregistered structural prediction.

Pure continuity optimization fails gate 1 and, by this experiment, cannot be used as a substitute for the missing historical registration rule.

## Reproducibility

Run:

```bash
python scripts/audit_pc_acorn_continuity_recoverability.py
```

The script writes `data/experiment-363-pc-acorn-continuity-recoverability.json`.

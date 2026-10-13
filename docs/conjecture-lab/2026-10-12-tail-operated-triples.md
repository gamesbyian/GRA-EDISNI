# CL-VLEN-04: can 27 tail marks command reconstruction of the preceding 81?

_12 October 2026. DISCOVER/DEVELOP, not source-authenticated decoding. Companion to CL-VLEN-01/02/03. No physical sticker, original numbered experiment, or machine-spec changes._

## A deliberately optimistic end-to-end assumption

Each of the nine A–I sticker background classes appears nine times in the 81-mark first zone and three times in the final 27-mark zone. Assume, for the sake of testing, that a class's final-three slash position **chooses which of its three three-bit body chunks is the source**, while its other chunks are copies or transformations of that source. This makes the 27-symbol channel a genuine *instruction channel for the 81-symbol channel*. It also immediately creates an erasure-recovery promise that can be falsified using partially observed physical marks, without inventing a plaintext.

This idea is conceptually related to the old 3+3+3 model families (including Experiment 26) but differs in its explicitly one-slash-indexed source, precise generator semantics, both native partitions, and matched physical controls. It must not borrow independent evidence from the incumbent Q4 recursion.

## Precisely what was tested

A class's first nine marks can be partitioned as three contiguous triples (body positions `0..2`, `3..5`, `6..8`) or three interleaved triples (`0,3,6`, `1,4,7`, `2,5,8`). The tail's exceptional slash position (0/1/2) selects a **seed** three-bit word. Relative direction is forward or backward cyclically through the other two triples.

The four source-preserving transformations are `identity`, `reverse bit order`, `invert all bits`, and `reverse then invert`. They have clear physical/electronic semantics and cannot invent a letter table. We enumerated:

- **Fanout:** each of the other two triplets is a specified transformation of the seed.
- **Chain:** the next triplet is derived from the seed and the third from the next.
- **Single-command:** only one of the two other triplets is constrained to equal a specified transform; the remaining triplet is unrestricted literal payload.

The first two have `2 partition layouts × 2 cyclic directions × 4 × 4 transform pairs × 2 chaining modes = 128` models. The single-command variants have `2 layouts × 2 directions × 4 transforms × 2 relative targets = 32`. **160 exact models**, all with one global operation convention shared by all nine A–I classes. This global shared rule matters; allowing an independent transform per class would fit nearly anything.

For each model, every possible one-hot selector and seed (8 three-bit words) generates either one complete nine-bit class body or eight possible bodies if the spare triplet is literal. Enumerating the tiny `3×8` or `3×8×8` local family produces exact compatible-completion counts against the physical corpus. No original unknown is filled into the evidence file. The correct normalization is the probability of the 84 physical sticker observations under each model's unconditional generated source-word set, compared with the independently uniform-body/one-hot-tail baseline.

## Exact result: all 160 fail this physical corpus

**Zero out of 160** models can simultaneously reproduce every observed nine-bit class body with the nine one-hot tail selectors.

The most informative local obstruction is class **B**. Its physically known body and one-hot selector are compatible with **only two of the 160 globally specified candidate models**, which are equivalent descriptions of the same relationship after reversing direction: strided three-bit partition, single target, **reverse**, selecting the opposite relative target. Neither surviving B model can accommodate the simultaneously known **D, E or I** class data. Thus B leaves zero admissible *global* uniform-transform decoders in this family. This is an exact logical contradiction for the 160 listed grammar rules, not a statistical test or a ban on other run-based decoders.

When evaluated individually rather than requiring global completion, the best individual candidate explains only **six of nine** A–I class traces. No model can account for all nine. The full JSON retains class-by-class compatibility counts for all 160 rules.

## Null control: failure is common even for matched shuffled marks

Preserve every physical observation location and its native early/late binary alphabet. Hold the 27 tail symbols *fixed*, including their one-slash class constraints. Shuffle only directly observed first-zone slash/dash labels, either within each original nine-site serial frame or within each nine-occurrence background class, preserving the observed counts for that grouping. Re-evaluate the entire 160-model family from scratch on each shuffled stream.

Across **80 deterministic controls per type**, only **one** frame-count shuffle and **one** within-class-count shuffle admits even one of the 160 globally uniform models. The actual code admits zero. The null result warns that exact incompatibility may be very common for a language this restrictive; there is no claim that the original code is statistically distinctive by *failing* the candidate generator.

## What remains possible

The result is a genuine family-level hard negative for globally shared direct transform operations, not for the parent idea of instruction-dependent runs. The author might have used a different grouping, sequential run-length data, a varying source selector, a compound opcode dependent on picture artwork, different transformations, repeated state/history, sparse edits instead of exact copying, or a 27→81 machine whose outputs are **actions** rather than replicated bits.

In particular, an operator could say "reverse the *following* group" or "repeat the last five bits" without asserting that every body class is a literal copy of another. The CL-VLEN-03 transducer explores that family at the whole-stream level, and CL-VLEN-02 explores stateful class-to-class references. These variants remain separate and should not inherit each other's negatives.

The nearest productive next research step requires a concrete, source-authenticated consumer or a parser that makes prospective physical predictions stronger than the onehot-only baseline. A nearly unbounded operation search may be useful for inventing stories, but finding one survivor in a long search would not establish authorial intent.

## Reproduce

`python scripts/conjecture_lab_tail_operated_triples.py --test`

`python scripts/conjecture_lab_tail_operated_triples.py --null-replicates 80`

The exact enumerator and reports are `scripts/conjecture_lab_tail_operated_triples.py`, `data/conjecture-lab-tail-operated-triples-2026-10-12.json`, and compact `data/conjecture-lab-tail-operated-triples-summary-2026-10-12.json`. The program does not depend on existing `machine-spec.json` or conditional H108 U2/U5 completions.
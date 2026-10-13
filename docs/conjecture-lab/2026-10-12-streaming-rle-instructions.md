# CL-VLEN-03: true streaming run-length instructions on the 81, 27 and 108-symbol channels

_12 October 2026. DISCOVER + DEVELOP with exact syntax and selected controls; not a decoded CE code, established source language or Playdead-confirmed instruction set. Companion to [CL-VLEN-01](2026-10-12-variable-length-program-grammars.md) and [CL-VLEN-02](2026-10-12-class-run-command-campaign.md)._

## This time, runs really **are** the instructions

The original question concerned different-length symbol runs acting on earlier or later runs. This experiment takes that as a literal hypothesis rather than measuring run histograms or choosing body slices. Each maximal run of one binary mark is an opcode, and the following maximal run of the opposite mark is a positive unary operand. The two marks can swap roles. Codewords are implicitly variable-width, and **the parser actually executes** command semantics on earlier output.

A deliberately invented, simple three-command set:

| Opcode run length | Instruction | Operand run of length `m` | Effect |
| ---: | --- | --- | --- |
| 1 | `EMIT` | `m` | Append integer `m` to output |
| 2 | `REPEAT` | `m` | Append the previously emitted integer `m` times; illegal before output exists |
| 3 | `REVERSE` | `m` | Reverse the last `m` emitted integers; illegal if fewer than `m` exist |
| 4 (optional) | `STOP` | no operand | Terminate exactly at the end of the stream, after output exists |

An operand length cap of 3, 5 or 9 is part of the grammar. An explicit STOP is either required or forbidden. Exact maximality is enforced because successive alternating runs of opposite symbols cannot be divided or fused. No zero-length operand, extra padding, or arbitrary parse is allowed. Examples: `100` can mean `EMIT 2` (slash opcode, dash operand), `101100` can produce `[1,1,1]`, and `1001111` can mean `EMIT 2; STOP` when STOP is active. These examples demonstrate an interpreter; they are not sticker readings.

Unlike CL-VLEN-02's local independent A–I instruction dictionary, the `REPEAT`/`REVERSE` actions use **state created by earlier commands**. Reversing the original traversal means later physical symbols can command operations on earlier ones. This also covers the possibility that an instruction semantically points forward in serial order without inventing a new buffer.

## Exactly what was searched

Three source streams, each retaining all 42 unobserved marks without imputation:

- The 81-symbol slash/dash primary zone (54 directly observed sites).
- The 27-symbol slash/dot final zone (12 directly observed sites).
- The full 108-symbol cycle (66 directly observed sites), using an explicitly **invented** slash-versus-non-slash collapse in which dot and dash both map to binary zero.

For each stream, test three physical orderings (`serial`, reverse serial, class-major A–I), two opcode-mark polarities (slash run means opcode versus non-slash run), three operand caps (3/5/9), and two stop policies (implicit end or mandatory length-four STOP). Exactly **36 models per stream, 108 total**. Class-major rearrangement operates on the initial literal H108 cycle using the nine observed background classes, with no learned permutation. The orientation and grammar dictionary were deliberately selected by a researcher; there is no source-authored instruction legend.

## Reproducible, exact counting

The code is a memoized finite-state transducer on `(input_position, number_of_prior_emitted_values)`. Its possible next transitions follow the opcode run length and the immediately following operand run. A complete binary string has at most one sequence of **maximal** runs, so there is no multiple-parse double counting. Unknown physical positions admit both binary values and are summed out exactly.

The normalizer for each grammar is the number of legal fully observed binary programs of equal length with **no constrained source bits**. Compare the fraction of those that remain compatible with the 66 actual physical observations against uniform random bits with the same observed mask: this gives an artificial source-code Bayes factor, useful as a *search score*, not a probability that this syntax was intended. The whole family is then run against 120 controlled label shuffles within each physical nine-site frame, keeping observation positions and observed counts unchanged. Each null reselects the best of all 36 grammar settings for each stream independently.

The implementation includes a genuinely independent run-by-run interpreter. Its results are exhaustively compared to the dynamic-program counts for **all binary strings up to length nine**, both opcode polarities, three length caps, both STOP policies and multiple output-length targets. Witness programs are executed and validated against their corresponding partial physical bit masks.

## Exact observations

| Stream | Best grammar | Compatible raw completions | Nominal log score | Controls at least as good |
| --- | --- | ---: | ---: | ---: |
| 81 body | Serial, non-slash opcode, cap 9, implicit stop | **4,997,120** | 1.795 | **68/120** |
| 27 tail | Reverse, slash opcode, cap 9, implicit stop | **5,756** | 1.309 | **80/120** |
| 108 collapsed | Serial, non-slash opcode, cap 9, implicit stop | **24,555,847,680** | 0.914 | **60/120** |

All three have many syntactically valid completed programs. None has exceptional **post-selection** compatibility in its corresponding 36-model search. The shuffles do not preserve the mature one-minority primary machine conjecture; they are intentionally a simple raw-count null. Stronger structural conditioned nulls can be built if a specific authentic command convention is recovered.

### The concrete fourteen-output idea

INSIDE's secret-ending lever sequence has fourteen input states in the historical research, so a program outputting *exactly fourteen integers* is worth testing as an explicitly **speculative receiving shape**. This is not a test of matching lever directions or values. The script counts all legal completed programs producing exactly 14 values, renormalizes by the total **unconstrained source-program count with the same 14-value output target**, and applies the same 36-model best-of-family null.

| Stream | Best raw-sticker-compatible output-14 family | Matched shuffles at least as good |
| --- | --- | ---: |
| 81 body | Exists, but comparatively rare among its valid programs | **69/120** |
| 27 tail | Exists | **99/120** |
| 108 collapsed | **None of the 36 models can produce 14 values with these observations** | Not applicable; no real model to rank |

The first two are not evidence for a lever consumer. The third is an exact negative only for the 36 enumerated stream grammars, output semantics and simple 108-bit collapse. An independent 14-move consumer, a different command table, or a split 81/27 producer remains possible.

## Key interpretation

The raw physical marks tolerate many **genuine executable** run-based languages. Even when the required output length is selected for a real candidate consumer, the best program offers no advantage against controls. Moreover, three independent syntactic choices (opcode polarity, operand cap, stop rule) plus the reading direction were fitted after the observations. A witness program generated by filling '?' must stay labelled as a *counterfactual completion*, never a discovered serial master.

A useful additional deduction: our earlier `69..76 = /------/` physical witness that forbids conventional Morse parsing does **not** exclude a length-six unary operand. A cap-9 RLE interpreter permits six symbols inside an operand without any violation. Accordingly, the strict Morse impossibility remains exact, while its generalization to every run-based encoding would be wrong.

## What could actually discriminate a run-program interpretation

- An independently authenticated original artifact explicitly showing unary run widths or the operations repeat/reverse/emit/stop, ideally with a known input length or register orientation.
- A consumer with a source-specified **output contract**: known move directions, an image transformation, an original printer layer/mask, a 9-class stencil selector, or a machine-readable receiver whose reaction can be reproduced.
- If inventing new programs, pre-register **sequential constraints** not optimized against output, evaluate them on the full missing-bit family, and keep both physical holdouts and a matching best-of-search null. Direct fit of a 14-number output to fourteen lever controls provides no independent validation.
- A genuinely cross-channel 27-mark instruction table controlling how the first 81 marks are consumed, rather than concatenating them into a single undifferentiated 108-bit stream.
- Erasure and bit-flip synchronization audits for an authentically constrained codebook, without falsely counting assumed error correction as discovered redundancy.

The project can continue those branches in DISCOVER and DEVELOP even without more stickers. No unconditional decoder is presently established by this campaign.

## Reproduce

Files: `scripts/conjecture_lab_streaming_rle.py` and `data/conjecture-lab-streaming-rle-2026-10-12.json`, with compact `data/conjecture-lab-streaming-rle-summary-2026-10-12.json`.

```bash
python scripts/conjecture_lab_streaming_rle.py --test
python scripts/conjecture_lab_streaming_rle.py \
  --observations data/observations.csv \
  --null-replicates 120 \
  --output data/conjecture-lab-streaming-rle-2026-10-12.json
```

No changes to original physical observation ledger, model completions, historical experiment numbers, or source provenance. Run time and null calibration may be extended without changing the codebook, but today's results are not independent holdouts for future fitted variants.
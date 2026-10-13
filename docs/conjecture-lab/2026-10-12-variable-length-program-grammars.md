# CL-VLEN-01: mixed-width codewords and an instruction-stream interpretation

_12 October 2026. DISCOVER + DEVELOP, followed by bounded adversarial controls. **Not a decoded message, identified parser, recovered source cue, model completion or new sticker observation.**_

## Question

Could runs or chunks of three, five, or other lengths represent different operands, with some chunks *instructing* us how to handle earlier or later chunks? The answer is **structurally possible**, but it is not enough to find a way to parse the corpus. A program-looking interpretation must explain the physical observations better than a similarly permissive program looking at scrambled marks; ideally it must produce a independently specified downstream reaction.

A deliberately larger search was authorized here: guessing operators and assigning meanings are **permitted in DISCOVER**. Those fitted decisions never become independent validation.

## Closest historical precedents and tested negatives

- Exp 317–318: a three-mark tail chooses a portion of preceding nine; row versus column unresolved, with five forced class selectors. This is already one kind of instruction grammar.
- Exp 400: contiguous one-of-three chunks fail the **specific** one-minority readout, not every possible three-symbol opcode.
- Exp 402–403: direct 3×36 Trifid and direct fractionated Morse fail specific historical code tables; 403 has an invariant illegal trigram under **that** table. Neither prohibits novel three-mark command words.
- Exp 404–405: slash-as-standard-Morse separator fails on a forced six-mark Morse token. A six-bit *operand*, run-length value, or non-Morse codeword could still be legal.
- CX-E2: post-hoc slash rails frame four 27-cell quarters as **4 / slash / 9 / slash / 12**. Four/nine/twelve serve as distinguishable speculative fields, not proven parser metadata.
- INSIDE's earlier printer `CTRL CON DISCON` puzzle is a source-backed precedent for *actions* as decoded output, though its operation and serial registration cannot simply be imported.

## Physical evidence and non-negotiable separation

Input is exclusively the canonical `data/observations.csv` at time of study: **84 records, 66 distinct residues**, 42 unknown H108 positions. Serial modulo 108 is checked; repeated physical observations must agree. Exactly **54/81** early slash/dash sites and **12/27** late slash/dot sites are known. Dot and dash belong to different binary zones: a single global `-/./` binary mapping is not a raw fact. The alternative codebook maps below analyze the two zones independently, with both bit polarities considered.

No `machine-spec.json`, U2/U5 completions, calculated 427 prediction or assumed `100` terminal is used. The executable program never fills an unknown mark into the physical ledger.

## Six invented grammars with executable semantics

| Grammar ID | Codewords -> actions | Action semantics |
| --- | --- | --- |
| `two_bit_backward` | `00` emit next 3, `01` emit next 5, `10` repeat, `11` reverse | Backward op requires a previously emitted chunk |
| `two_bit_forward` | `00` emit next 3, `01` emit next 5, `10` skip next 3, `11` skip next 5 | Forward skip consumes an operand with no output |
| `prefix_backward` | `0` emit next 3, `10` emit next 5, `110` repeat, `111` reverse | Mixed-length, instantaneous prefix-free opcodes |
| `prefix_forward` | `0` emit next 3, `10` emit next 5, `110` skip 3, `111` skip 5 | Mixed-length prefix-free, actions look ahead |
| `two_bit_terminated` | `00` emit 3, `01` emit 5, `10` repeat, `11` stop | Explicit STOP only at exact end, with prior emit |
| `prefix_terminated` | `0` emit 3, `10` emit 5, `110` repeat, `111` stop | Same, self-delimiting opcodes |

Every *completed* bit string has at most one parse under one of these independently defined codebooks. That follows from prefix-freeness and a deterministic operand length per opcode; the code verifies it exhaustively on all binary strings up to length eight. Each operator has a concrete executable implementation. Reversing previous means reversing **bit order of the latest emitted operand**, not bitwise complementation; skip affects subsequent operand positions; repeat re-emits the most recent operand. A full parse must consume its 81- or 27-bit zone exactly. STOP grammars require an actual terminal command at the zone end.

These grammars intentionally cover both directions of instruction dependency, fixed versus variable opcode width, and implicit versus explicit termination. They are samples from a large language-design space, **not** a claim to have enumerated every finite-state transducer or self-modifying grammar. No target output or keyword entered their design.

A dynamic program tracks input position, existence of a preceding emitted chunk, and whether a nontrivial control instruction occurred. Because an unknown operand bit can take either value, the program counts **exactly** how many missing-mark completions yield legal instruction streams. Witness completions and outputs are mechanically generated using a lexicographic path. They are invented demonstrations and cannot be promoted as physical sticker readings.

## Measured results

### Unfilled physical runs and grouping

| Quantity | First 81 | Last 27 |
| --- | ---: | ---: |
| Observed / unknown | 54 / 27 | 12 / 15 |
| Physically known adjacent pairs | 34 | 5 |
| Equal adjacent pairs | **17** | **2** |
| Fully observed consecutive trigrams | **19** | **2** |
| Full native fixed triplets (phase 0) | 6 of 27 | 0 of 9 |
| Full native fixed quintets (phase 0) | **1 of 16** | **0 of 5** |
| Full native fixed nonets (phase 0) | 0 of 9 | 0 of 3 |
| Minimum / maximum binary transitions across **every** raw-compatible completion | 22 / 59 | 7 / 22 |

For exact maximal runs, across all raw-compatible completions the number of **three-site runs** can vary from **0 to 12** in the first zone and **0 to 6** in the final zone; five-site runs from **0 to 7** and **0 to 2** respectively. These are exact per-length min/max bounds, **not simultaneous guarantees**: independently attaining the maximum count for each length can require different fillings. Only seven early exact maximal runs and one tail exact maximal run have both observed uniform interiors and observed opposite-symbol or zone-edge flanks. A longer run cannot be inferred across an unobserved neighbor.

The raw corpus is particularly sparse for five-symbol blocks: testing 5-bit letter/codeword frequencies directly would be largely an imputation exercise.

### Adjacency calibration

An observed-only label shuffle preserves the actual site mask and symbol counts. The second shuffle **also** preserves observed symbol counts independently within each nine-site frame, to avoid attributing coarse historical 9-frame structure to accidental run-level novelty. 12,000 deterministic shuffles per zone/control yielded:

| Zone | Equal adjacent observed | Global-shuffle mean | Frame9-shuffle mean | P(shuffle >= observed), global/frame9 |
| --- | ---: | ---: | ---: | --- |
| First 81 | 17 | 17.303 | 17.371 | 0.608 / 0.640 |
| Final 27 | 2 | 2.579 | 2.810 | 0.839 / 1.000 |

No enrichment in **adjacent identical known marks**. These are limited post-hoc descriptive reference distributions, not a global proof against run-length instructions. A parser could depend on transitions, unknown sites, nonserial order or external framing.

### Instruction-language acceptance, under the two physical bit orientations

Accepted completion counts below are **not decoded-message likelihoods**. They are exact fractions of all physically allowed bit-fillings that happen to permit a complete parse under a given *invented* language.

| Zone and orientation | Backward fixed | Forward fixed | Backward prefix | Forward prefix | Fixed STOP | Prefix STOP | Denominator |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| First 81, `-=0 /=1` | 50,331,648 | 30,408,704 | 35,377,152 | 0 | 0 | 337,920 | 134,217,728 |
| First 81, `/=0 -=1` | 5,807,104 | 25,165,824 | 18,382,848 | 24,756,224 | 0 | 0 | 134,217,728 |
| Final 27, `.=0 /=1` | 1,792 | 7,168 | 0 | 2,048 | 640 | 0 | 32,768 |
| Final 27, `/=0 .=1` | 4,736 | 3,072 | 2,432 | 8,320 | 0 | 0 | 32,768 |

One strikingly successful-looking first-zone invented backward-codebook accepts **37.5%** of 134,217,728 physical completions; it is thereby **terribly nonselective**. In a matched null comparing the *best* of all six grammars and both polarities over 500 shuffles, the same zone's observed maximum (50,331,648) is actually **below** the shuffled median (62,914,560 globally, 62,054,400 within frame9). Fraction of shuffles scoring at least as high as our best: **0.707** globally, **0.715** within frame9. For the tail the best observed 8,320 is likewise below shuffle medians 9,216; tail best-of-family exceedance about **0.717 / 0.709**. These are descriptive post-selection controls with Monte Carlo uncertainty and strong corpus dependence. They do not say any particular grammar is false; the tested family has no measurable privileged fit under this very limited scoring metric.

Conversely, the specific `prefix_forward` with `-=0 /=1` first-zone readout and both first-zone fixed STOP orientations have exactly zero valid completions. That is a **hard negative for those precise candidate codebooks, boundaries and polarities**, and nothing broader.

## Why a successful parse does not solve the mystery

The user-facing point matters: an opcode length, operand length, mapping, zone boundary, END rule, and operations have all been supplied by this investigation. The observations only constrain those choices, mostly weakly. A high count of conforming programs tells us the grammar is flexible, and a low count only matters relative to baseline and the cost of having tried multiple grammars. Varying 3/5 to 3/6 or allowing skips until an English message appears would manufacture confidence.

Information-theoretic code tools could assist a **future supplied codebook**. Kraft-McMillan limits possible length inventories for uniquely decodable binary codes; the Sardinas-Patterson algorithm tests unique decodability for a proposed non-prefix dictionary. Neither one infers intended semantics from sticker marks. Our fixed dictionaries are prefix-free by construction.

References: [Sardinas-Patterson algorithm](https://en.wikipedia.org/wiki/Sardinas%E2%80%93Patterson_algorithm); [Kraft-McMillan](https://en.wikipedia.org/wiki/Kraft%E2%80%93McMillan_inequality). These are methodological, not INSIDE sources.

## Strong next conjectures, deliberately unconstrained by presumed outputs

1. **Physical run-length grammar:** instead of bit-level opcodes, let runs of consecutive identical marks produce numbers, signed quantities, or delimiters. Enumerate run-length sequences over the raw partial string with a finite-state parser, preserving unknowns, 9/12/27 candidate traversals and the 81/27 boundary. Test exact parses against both label-shuffle and structural frame-null models. We now have exact per-length run bounds as inputs.
2. **One class = one instruction:** use each A–I class's nine early bits as an operand with its final three symbols as a *three-way opcode*, e.g. one variant chooses a three-bit slice, one reverses a five-bit slice, one references the preceding class. Preserve 36 physical-compatible tail assignments from Exp 317 and compare row versus column addressing without assuming the incumbent recursion. Feed the resulting nine instructions into a specific receiving object or virtual source surface.
3. **True variable-width source language:** expand from `3|5` to a preregistered bounded family of `3|5|9`, one-byte-like operation, and a self-delimiting unary length prefix. Keep the host artefact, stop rule, and any skip policy explicitly in the grammar ID. Use model enumeration *after* source-native framing is established, not as a physical substitute.
4. **Cross-channel program:** test whether 27 tail marks choose how to consume groups in the first 81, rather than parsing both streams independently. This is distinct from one-to-one Q4 selector recursion; hypotheses may use *runs*, repeats or variable-width commands. Reward concise, checkable joint outputs over opaque completions.
5. **Arbitrary output mode:** do not presume plaintext. Interpreter outputs could be a 14-move lever sequence, a sparse pixel/stencil operation, control timing, an original printer packet edit, an address, or a command acting on `534brn` page materials. Describe the entire player-visible path and one independent witness before calling any matching endpoint evidence.
6. **Self-synchronization and robustness:** test whether a purported code can recover its opcode boundaries after one erased/misplaced sticker and whether independently duplicated serials give a check bit. Distinguish manufactured redundancy from a retrospective checksum.
7. **Original source archaeology:** scan original game assets and ARG captures for unambiguous command-width legends, 3/5 operator tables, slash boundary cues, interval counts, `stop`/`repeat`/`reverse` phrases, or a device with a known 81/27 input contract. Such a source can turn a hundred invented parsers into a dozen genuine hypotheses.

These are DEVELOP investigations, not prerequisites on future owner replies. A physical code need not be human-text, and the next decoder need not belong to a conventional cryptographic family.

## Reproduce, and falsification discipline

```
python scripts/conjecture_lab_variable_length_grammar.py --test
python scripts/conjecture_lab_variable_length_grammar.py \
  --observations data/observations.csv \
  --output data/conjecture-lab-variable-length-grammar-2026-10-12.json \
  --replicates 12000 --parser-null-replicates 500
```

The first command runs exhaustive small-bitstring comparisons of the DP against an independent executing interpreter and exact run-length bounds against brute-force fillings. The second regenerates the complete ~70KB JSON containing every phase, group width, delimiter possibility, parser counts, witnesses, and null scores. The experiment is deterministic and standard-library-only. If new observations change, the regenerated report may differ; a fixed historical snapshot can be pinned to reproduce today's JSON exactly.

**Disposition:** This genuinely opens a larger language family without claiming its existence. No canonical model, prediction, physical mark or historical negative was overwritten. The most valuable current result is that *generic* 3/5 mixed command grammars explain little on their own. The next serious discriminator must exploit authentic boundary/consumer constraints or a much more selective, testable code grammar.
# CL-VLEN-02: class-local run-length opcodes, backward/forward references, and held-out sticker controls

_12 October 2026. DISCOVER and DEVELOP, with exact finite tests and matched nulls. **No decoded plaintext, intended instruction set, original consumer, raw sticker addition, or confirmed serial completion is claimed.** Continuation of [CL-VLEN-01](2026-10-12-variable-length-program-grammars.md)._

## Adopt the hunch and follow it

Assume that a background class is one **twelve-symbol message**. Its nine appearances in the first 81 serial positions are a binary operand and its final three slash/dot appearances are a command. A one-slash tail has three possible positions, so it can choose between three instructions. Don't presume the output is a word, and don't require any known result such as the old secret-ending lever pattern or the old recursive terminal.

Three genuine conditional mechanisms, all deliberately invented, were carried beyond the first intuitive reading:

1. **Numerical run instruction.** The marked final-three position says exactly how many maximal equal-symbol runs, how long the longest run, or how long the initial run must be in that class's nine-symbol body. We tested 7 triples of distinct integer values, 6 opcode assignments per triple, and all three measures: **126 local models**.
2. **Back-reference instruction.** The marked position means `literal`, `copy previous`, or `reverse previous`. `copy` and `reverse` apply to either the complete earlier nine-bit class, one of three contiguous three-bit subsequences, or one of three strided three-bit columns. Each command has executable semantics and reference variables must actually have been assigned. The other six bits remain literal payload in three-bit variants. **4 physical/artwork readings × 6 operator mappings × 7 target lanes × 2 bit-polarity policies = 336 reference models**.
3. **Forward reference.** The same commands operate on the following class by reversing traversal. Alphabetical `A..I` and its reversal, plus native assembled-art `IAB/CDE/FGH` row-major and its reversal, are all tested. These four traversals aren't independent; repeated matches are not multiple confirmations.

The bit-polarity policy for copy/reverse is either literal binary equality or equality *up to bitwise complement*. The latter is run-shape copying: complementing all bits preserves lengths of all maximal runs. In three-symbol modes it applies only to the selected lane. No body bit is silently completed into the original observation file.

The 81 early-site alphabet remains slash/dash and the 27 late-site alphabet remains slash/dot. Both use `/=1` and the other region-native mark `=0`, not an assertion that dash and dot were originally interchangeable.

## Physical input and exact accounting

Canonical file is `data/observations.csv`, verified against serial numbers modulo 108, background class, zone alphabet, and duplicated residues: **84 physical records, 66 unique H108 positions and 42 unobserved**. Exactly 54 early and 12 late sites are known. Class D's `.?.` final triple incorporates the physically confirmed sticker 427 dot and forces its one slash to be residue 94 *only if the one-slash-per-class assumption is true*. The one-hot tail hypothesis still has 18 compatible assignments across the nine classes.

For each completed class body, the script computes the exact run-length vector. It enumerates only `2^k` completions for the class's own `k` unknown body bits; it never samples missing symbols or substitutes a U2/U5 recursion model. The joint constraints are counted using a finite-state dynamic program with all 512 possible nine-bit previous words as states. For a three-bit reference, all DP masses with the same selected three-bit word are aggregated, allowing exact copy, reversal, and complemented forms without enumerating `2^42` full masters. The DP was independently checked by brute force for small two-class cases and has a deterministic smoke command.

The comparison **baseline** is independently uniform nine-bit body words with one slash in each three-bit tail. Every candidate's observed-compatible count is divided by its own *unconditional* number of syntactically valid source programs, then compared to the one-hot-only baseline as a Bayes factor under those artificial uniform priors. A raw count of accepting completions cannot be compared across grammars of different restrictiveness. The reported `log Bayes factor` is conditional on this artificial source model and **is not a posterior probability that Playdead used the grammar**.

## First exact contradiction: 126 local run-number grammars fail

The literal run-count reading has an invariant contradiction without assigning any missing marks:

| Observed-bound property | Class B | Class I |
| --- | --- | --- |
| Marked final-three selector position, under one-hot | `2` | `2` |
| Possible total number of maximal runs in nine early marks | `{2,4}` | `{5,7}` |
| Possible longest-run length | `{6,8}` | `{2,3,4,5}` |
| Possible first-run length | `{1,8}` | `{1}` |

A fixed opcode position cannot mean a **single exact run count** or a **single exact maximum run length** in both B and I: their feasible sets are disjoint. For the *initial-run-length* family, I and B force selector 2 to mean length 1. D's selector 1 also forces initial-run length 1, and E's selector 0 forces it to mean length 1. Thus a grammar requiring **three distinct run lengths** also fails independently of every missing cell.

This closes **all 126 enumerated local variants** and, more broadly, every one-to-one tail-position → one exact run-count or one exact longest-run-length mapping on these class traces. It does **not** close a command meaning *at least N*, a run-length operation requiring another parameter, a different framing/order, or a command assigning an operation rather than an exact run statistic.

## Reference grammars: partial feasibility is not evidence

All 48 strict nine-bit `literal/copy/reverse` combinations in the four traversals and two polarity modes fail the complete physical corpus. Relaxing commands to act on a *specified three-bit lane* leaves **23 of 336** reference models with at least one compatible full assignment. Thus **23 of all 462** tested grammars have a legal parse. This result is exact for these frozen codebooks, masks, and orderings, not for all possible instruction languages.

The retrospectively best one uses reversed alphabetical traversal, maps the three positions to `reverse`, `copy`, `literal`, and applies copy/reverse modulo complement to the first three body bits. It has a **log Bayes factor of ln(4)**, equivalent to an apparent fourfold fit advantage under the deliberately specified uniform source priors. The reversed artwork traversal ties. The best model is entirely **fitted to the available observations**, so neither choice is a discovery or a prospective prediction.

### Correcting for searching 462 models

Hold the 12 observed tail symbols in their exact positions, including their physical one-hot compatibility, and permute **only the 54 observed early-zone marks** at their actual observation sites. In one control preserve slash/dash totals separately within each original nine-residue serial frame; in the other preserve them within each nine-occurrence A–I background class. This preserves the observed-mask structure and both types of aggregation while challenging the specific relation between a class's early mark runs and its final-three selector. For every shuffle, optimize across the **same 462 grammars**.

| Body-only matched null | Shuffles with best score ≥ physical best | Null median log factor | Physical best log factor |
| --- | ---: | ---: | ---: |
| Preserve original serial nine-site frame counts | **119 / 120** | 2.958 | 1.386 |
| Preserve within-class body counts | **118 / 120** | 2.708 | 1.386 |

Both controls make the real data look *less* compatible with these grammars than a typical rearrangement. These are reproducible, finite seeded reference distributions, not externally calibrated authorial probabilities. The difference between 118 and 119 is unimportant relative to the many prior research choices and shared physical evidence.

### Withhold known physical evidence

Because a theory able to parse many filled-in strings can still be wrong, we also tested predictions without the held-out symbol participating in either fitting or model selection. Each fold independently chooses its highest-scoring grammar from the other evidence and computes an **exact conditional probability** for the withheld physical mark. Baseline predictions come from the same one-hot-tail assumption without invented run or reference instructions.

| 66 single-residue holdouts | Best-of-462 model | One-hot-only baseline |
| --- | ---: | ---: |
| Mean Brier error (lower better) | **0.3999** | **0.2395** |
| Mean probability assigned to actual symbol | 0.4154 | 0.5227 |
| Folds assigning actual physical symbol exactly zero probability | **12** | **0** |

The 12 impossible retrospective predictions include 10 early-zone marks and 2 late-zone marks. They are listed by residue in the JSON, including the original physically attested symbol. The models do **not** outperform an unsophisticated compatible hypothesis, despite having much greater flexibility.

For a more severe test, hold out **every physically known mark belonging to one A–I class at once** before selecting a grammar. Across nine such folds, using the other eight classes as training evidence:

| 66 marks evaluated across nine class holdouts | Best-of-462 model | One-hot-only baseline |
| --- | ---: | ---: |
| Mean Brier error | **0.2752** | **0.2449** |
| Mean probability of actual symbol | 0.4982 | 0.5101 |
| Exactly impossible physical marks | **2** | **0** |

These are retrospective cross-validation tests, not prospective 2026 predictions: the researcher had already constructed the 462-family portfolio after seeing the original physical corpus. They nevertheless decisively rebut any claim that the portfolio's best parse is an independently predictive decoding machine.

## What survives, and how to extend without outcome preconceptions

A first-class instruction format remains possible. Nothing here denies a **general** operation in which repeated or non-repeated marks change state, a length prefix changes consumption width, a three-mark command selects a frame-relative operation, or an external source fixes which operation applies. In particular the 27-symbol tail may act on the preceding 81 collectively rather than as nine independent instructions. A meaningful next test should implement such a specific **sequential** transducer, perhaps with a compact eight-state program counter and a variable-length operand, and score it against the same nulls and held-out sites. Any model producing a known original receiver output needs to log which source cue fixed the parser and any fitted parameters, and must predict something not used to discover it.

Natural next stages (no new stickers prerequisite):

- A genuine streaming run-length interpreter, with explicit `run = count`, `run = repeat previous count`, `run = reverse following count`, prefix length and STOP syntax, whose execution is tested on the 81+27 and class-major read orders. Existing CL-VLEN-01 only tested run statistics and bit-token opcode parsing; this work tests class-local run constraints, not all possible streaming run machines.
- Separate a three-bit **instruction** from a five-bit **operand**, with an explicit rule explaining the 12-per-class framing obstacle (cross-class consumption, header/trailer, padding or overlap), and test both source-fixed and conjecturally invented alternative frames.
- Translate emitted instructions into native physical consumers rather than optimizing against attractive text: the PC printer geometry and authenticated recovered `LIFE DETECTED` source, an original in-game lever/control sequence, or the authored `534brn` surface. A reverse-fitted mapping is a conjecture card, never source proof.
- Minimum-description-length enumeration of small opcode tables, but apply a **best-of-entire-enumerated-family** null and separate true held-out physical marks from existing seen data.

## Files and reproduction

- `scripts/conjecture_lab_class_run_programs.py`: source-readable exact DP, 462-model search, matched controls, physical leave-one-out and entire-class holdouts, test suite.
- `data/conjecture-lab-class-run-programs-2026-10-12.json`: all 462 model scores, exact denominators, 9 class observations and run histograms, 120+120 shuffled controls, every holdout score, and labelled limitations.
- `data/conjecture-lab-class-run-summary-2026-10-12.json`: compact readout and executable provenance.

```bash
python scripts/conjecture_lab_class_run_programs.py --test
python scripts/conjecture_lab_class_run_programs.py \
  --observations data/observations.csv \
  --null-replicates 120 \
  --output data/conjecture-lab-class-run-programs-2026-10-12.json
```

No `data/observations.csv`, physical-evidence register, older numbered experiment, frozen physical discriminator, or `data/machine-spec.json` was changed. Results are bounded to **this** 84-record physical snapshot and the explicitly enumerated codebooks. Re-running after authentic sticker changes is expected to produce a different JSON.
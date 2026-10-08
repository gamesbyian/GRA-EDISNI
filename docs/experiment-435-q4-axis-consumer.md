# Experiment 435: does Cube 4 select a depth or select a cube?

## Test definition

The 108 foreground positions have the arithmetic organization
`r-1 = 27Q + 9d + j`: primary cube/quarter `Q∈{0,1,2}`,
layer/depth `d∈{0,1,2}`, and known A–I physical position `j∈{0..8}`.
The fourth quarter (`Q=3`) contains three slash/dot frames; under
the observation-compatible one-slash-per-A–I-stack grammar, its
slash position gives a value `S(j)∈{0,1,2}`.

The community cube suggestion licenses the coordinates. Earlier
Experiments 317 and 373 already document the index/depth interpretation.
This experiment tests **two fair, explicitly defined output operations**
on exactly the same 324 complete masters from Experiment 429:

- **Native-depth selector:** for each fixed `Q`, form a 3×3 physical
  output by reading `(Q, d=π[S(j)], j)` for all A–I positions.
- **Cross-cube selector:** for each fixed `d`, form a 3×3 physical
  output by reading `(Q=π[S(j)], d, j)` for all A–I positions.

For both, require **exactly one dash in each physical column** of each
of the three output surfaces, nine constraints in total. Here `π`
is one *globally shared* permutation of the three coordinate labels,
drawn from all six possible permutations. The native identity
permutation is `012`; any other mapping is an additional convention
requiring independent justification.

The 324 parent masters retain only raw observed stickers, the
nine-frame physical one-minority-per-column grammar, and Q4 one slash
per class. The complete recursive machine, route signature, terminal
word, image fit, plaintext fit and external 534brn candidate are not
used.

## Exact operation comparison

| Label mapping π | Depth-selected full masters | Cube-selected full masters |
| --- | ---: | ---: |
| 012 (native identity) | **12** | **0** |
| 021 | 0 | 0 |
| 102 | 0 | 0 |
| 120 | 0 | **8** |
| 201 | 0 | 0 |
| 210 | 0 | **4** |

The quarter-selected 120/210 families share **two** complete masters,
so their union contains **10** distinct completions. The native-depth
12-master family and quarter-selected 10-master union share **zero**
complete strings.

The strict identity-labelled comparison favours a depth-typed reading.
But the quarter-selected interpretation is **not falsified as a whole**:
two global relabelings leave surviving full masters. Such relabelings
should not be silently granted the same prior as native physical
coordinate typing.

## Three prospective physical discriminators

Only seven unobserved residues have differing possible-symbol sets
between the two surviving operation families:

| H108 residue | Native depth (12 masters) | Relabelled quarter (10 masters) | Consequence |
| ---: | :---: | :---: | --- |
| 49 | `-` | `-` or `/` | Depth-specific forced |
| **50** | **`-`** | **`/`** | **Directly incompatible** |
| 52 | `-` | `-` or `/` | Depth-specific forced |
| **54** | **`-`** | **`/`** | **Directly incompatible** |
| 84 | `.` or `/` | `.` | Quarter-specific forced |
| **93** | **`.`** | **`/`** | **Directly incompatible** |
| 102 | `.` or `/` | `.` | Quarter-specific forced |

The three mutually exclusive single-symbol predictions occur at
**50, 54, 93**. Serial candidates no higher than 600:

- 50: 50, 158, 266, 374, 482, 590;
- 54: 54, 162, 270, 378, 486, 594;
- 93: 93, 201, 309, 417, 525.

All three remain unobserved in the current canonical 66-residue
corpus. The native-depth symbols agree with the separately frozen
preferred-machine predictions, but they are *conditional on the
shared structural grammar*. Repeated agreement between related
models must not be counted as independent evidence.

## Output stability, not a solved message

Read the three resulting 3×3 surfaces in A–I serial order, giving
27-symbol words. Over all 12 native-depth survivors there are **three
distinct outputs** with **21/27 positions invariant**. Over all ten
relabelled quarter survivors, accounting for masters compatible with
both surviving permutations, there are **five distinct outputs**
with **17/27 positions invariant**.

All outputs trivially have nine dashes (three per surface), because
that was the structural rule used to choose them. Neither family
produces one uniquely identified message or an independently cued
lever sequence. Do not credit that imposed nine-dash census as
additional evidence.

## Whole-nine-sticker-frame holdout

Remove all observed body symbols from one of the nine physical
nine-sticker frames, retain Q4 and the other eight frames, enumerate
full primary-column masters, then reapply each candidate operation
without ever consulting the hidden frame symbols. Check how many of
the withheld physical marks are forced across every surviving master.

| Allowed operation | Known primary marks held across nine folds | Forced correct | Ambiguous | Other |
| --- | ---: | ---: | ---: | --- |
| Native depth 012 | 54 | **4** | 50 | No excluded truth |
| Cube-selected 012 | 54 | **0** | 0 | No survivors in any fold |
| Cube-selected union of all six globally shared π | 54 | **0** | 54 | No excluded truth |

The two *separately fixed* quarter permutations 120 and 210 force
5/54 and 6/54 respectively, but those choices were already
identified retrospectively from the same corpus. Taking their
**honest union before predicting** produces zero forced positions.

This holdout result is a useful **coverage and falsifiability audit**,
not a blind predictive-accuracy claim: the structural rule and
permutation space were discovered using the complete observed
corpus, and any full-corpus-compatible model necessarily includes
the true symbols after removing data. No forced incorrect holdout
predictions can appear under these nested constraints.

## Interpretation

Cube 4 does support an exact simple *instruction-layer* comparison:
using its marked positions to select depths is cleaner and less
convention-heavy than using them to select quarters. That supports
the native-coordinate-typing argument from Experiment 373, and is
compatible with the preceding machine family.

It does **not** prove Playdead intended the selected-surface one-dash
rule or a literal cube puzzle. A fully relabelled quarter-selector
rival still survives present evidence and predicts three concrete,
different physical symbols.

Most useful independent next test: obtain any one of the residue
50/54/93 serial-family stickers, freeze both expected symbols
before inspection, and record whether each entire candidate family
survives. Until then, do not tune the operation to reproduce a
particular desired decoded message.

## Reproduction

```bash
python scripts/audit_q4_axis_consumer_comparison.py
```

The script enumerates 324 known-compatible full masters, all twelve
(axis × global label permutation) structural operations, the seven
symbol-set differences, and the nine frame-erasure holdouts. Counts
were independently checked in a separate local implementation;
repository checkout execution remains pending.

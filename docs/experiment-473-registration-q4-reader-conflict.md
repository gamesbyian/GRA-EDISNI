# Experiment 473: registration weighting versus the two Cube 4 axis readers

## Question

Experiment 456 froze two explicitly different potential Cube 4
*instruction* operations, both starting from the same 324
observation-compatible full masters:

- **Native-depth selector:** use the Q4 slash at each A–I location
  as the depth index for each primary quarter. Applying the chosen
  one-dash-per-physical-column output rule leaves **12** masters.
- **Relabelled-quarter selector:** interpret that Q4 slash position
  as the primary cube index after a single globally shared coordinate
  relabeling. The same output rule leaves **10** distinct masters.
  The two operation families share no complete string.

Experiment 472 separately found that a *statistical* registration
contrast, **same coordinate minus alphabetical horizontal ±1 X**,
predicts some withheld physical symbols better than uniform
complete-master weighting. Does that contrast choose one of
the specific Q4 reader models, or just rank complete strings?

## Scores across all 324 masters

| Candidate family | Masters | Mean alphabetical-X contrast, percentage points | Fraction of total exp(25×contrast) weights |
| --- | ---: | ---: | ---: |
| All raw-compatible physical-column masters | 324 | **10.58** | 100% |
| Native-depth Q4 instruction family | 12 | **8.05** | **1.78%** |
| Relabelled-quarter instruction family | 10 | **13.44** | **5.90%** |

Unweighted parent family fractions would be 12/324 = **3.70%**
and 10/324 = **3.09%**, respectively. Consequently the
registration score shifts relative weight *away* from the native
depth family and *toward* the globally relabelled quarter family.

But it does **not** select the quarter family overall: most
registration weight remains on the 302 masters in neither
instruction-family subset. Moreover, the models were defined
after overlapping prior structural explorations, and
`exp(beta × score)` is an arbitrary retrospective weighting
choice, not a manufacturing likelihood.

## Preexisting physical discriminators

Existing frozen rival-model predictions had already identified
residues **50, 54, 93** as direct opposite predictions:

| Missing H108 residue | Native depth | Relabelled quarter |
| ---: | :---: | :---: |
| 50 | `-` | `/` |
| 54 | `-` | `/` |
| 93 | `.` | `/` |

Under **unfiltered** 324-master weighting with
`beta=25` and alphabetical-X registration, the slash weights
are approximately **0.745 at residue 50**, **0.745 at residue 54**,
and **0.382 at residue 93**.

Thus the statistical score leans **toward the quarter family's
symbol at 50/54 but toward the depth family's symbol at 93**.
It does not support a single coherent Q4-axis interpretation.
Those weights must **not** be treated as physical-sticker
probabilities or claim more confidence than the conditioning
assumptions permit.

A future physical slash at residue 50 or 54 would contradict the
**exact frozen native-depth-plus-output-rule family** as defined,
but would not prove a quarter-selector or invalidate all depth
interpretations. Likewise a future dot at residue 93 contradicts
the relabelled-quarter-plus-output-rule family but does not
prove the native depth mechanism.

The new work therefore supplies a useful model clash,
**not** an endgame readout, unique complete code, proof of 3D
construction, or additional independent sticker evidence.

## Priority and stopping condition

Freeze the contrast definition, weighting strengths, pair layout,
and current observation snapshot. Reopen for genuinely new physical
residue symbols or an independently clued consumer operation.
Do not vary coordinate permutations to obtain a desired
historical ARG phrase, lever sequence, image or location.

Cross references: Experiments 456, 459–462 and
`data/frozen-q4-axis-consumer-discriminators.json`.

# Experiment 464: Cube 4 one-stack recovery versus total-erasure prediction

## Why this matters

The proposed Cube 4 instruction is a slash/dot code with one slash
in each A–I three-depth stack. The native-depth model also requires
that selecting that depth at each A–I position from each of Q1–Q3
produces a 3×3 surface with exactly **one dash per physical column**.
A rival instead selects a primary quarter using one globally
shared permutation of the Q4 depth labels.

Earlier tests held out primary stickers while keeping Q4 observed.
That does not establish whether Q4 itself is predictable from
the primary code. This experiment tests that question at **two
very different erasure strengths**, explicitly distinguishing
within-Q4 completion from independent primary-to-Q4 prediction.

The parent body family is the **18** actual-observation-compatible
physical-column primary completions. All results are conditional
on that body grammar and the additional selected-column output rule,
which were themselves developed from the same historical corpus.

## Test A: hide one entire Q4 A–I depth stack at a time

Each of the nine A–I Q4 stacks contains three possible depth
marks. For each letter with at least one physically observed Q4
mark, remove **all observed marks for that letter's stack**.
Retain the observed Q4 marks in other letters, construct every
compatible complete candidate, and predict the withheld marks.
Each visible physical Q4 position is scored exactly once.
The latest data has **12 known Q4 marks** (four slash, eight dot).

| Candidate family | Correct withheld Q4 marks /12 | Brier |
| --- | ---: | ---: |
| One slash per stack, no interaction | **8** | 0.2222 |
| Native-depth selected-column reader | **11** | **0.0441** |
| Globally relabelled quarter reader | **6** | 0.2332 |

This is real conditional within-layer reconstruction. But eight
other stacks retain their actual physical observations in each
fold. The native reader can make the withheld letter highly
predictable *given the other Q4 letters*.

## Test B: hide **all 12 known Q4 marks at once**

Retain the same 18 observed-compatible primary bodies, but
allow all **3^9 = 19,683** Q4 slash-depth codes per primary body,
without conditioning on any physical Q4 slash/dot label.
There are 18 × 19,683 = **354,294** complete masters before
applying the optional output reader.

| Candidate family | Complete masters allowed | Correct Q4 marks /12 | Brier |
| --- | ---: | ---: | ---: |
| One slash per depth stack | **354,294** | **8** | 0.2222 |
| Native-depth selected-column reader | **948** | **8** | **0.2249** |
| Globally relabelled quarter reader | **7,824** | **8** | 0.2222 |

Although the native-depth condition shrinks the code space
from 354,294 to 948 masters, **it no longer predicts the
actual Q4 marks better than the trivial dot-majority baseline**.
The competing quarter interpretation also has no independent
predictive advantage under total Q4 erasure.

This reverses the misleading conclusion that could be drawn
by reporting only the 11/12 one-stack result.

## Interpretation

The tested native-depth reader exhibits strong *internal
conditional coupling*: with most of Q4 still known, it can
recover a few withheld Q4 marks. It does **not** independently
reconstruct Cube 4's observed instructions from the primary
cubes once all Q4 labels are hidden.

This cannot by itself refute Q4 as a genuine **instruction
source**. A separate instruction code might be intentionally
independent of the body it controls and therefore impossible
to reconstruct from that body alone. But the 11/12 figure
must not be promoted as primary-to-Q4 causal evidence.

Similarly, the statistical alphabetical-X registration rule
from Experiment 462 can rank completed candidates, but the
gain largely persists when Q4 is excluded from scoring. The
operation/consumer remains unconfirmed.

No new physical observations, literal 3D password or endgame
payload are claimed.

## Reproduce

```bash
python scripts/audit_q4_erasure_scope.py
```

The script uses the canonical 84-record/66-residue CSV,
enumerates all legal masters exactly, and asserts the full
Q4-erasure survivor counts `354294/948/7824` and
the 12-symbol hit counts `8/8/8`.
Independent vectorized enumeration also reproduces the results.

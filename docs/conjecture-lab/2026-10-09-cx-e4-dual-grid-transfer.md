# CX-E4: the second 9+3 field, a transpose/complement pair, and its exact control

_9 October 2026. Independent DEVELOP revival extending [CX-E2](2026-10-09-cx-e2-four-nine-twelve-fields.md) and the [CX-E3 literal-reader negatives](2026-10-09-cx-e3-native-reader-negatives.md). Python reproduction: [dual-grid and exact 315-case enumerator](../../scripts/conjecture_lab_cx_e4_dual_nine_fields.py). All input marks come solely from the 66 known H108 residues; no missing physical sticker has been filled._

## A source-class-aware second grid, rather than an amorphous 12-mark suffix

If the two observed 4×27 slash rails are delimiters, the resulting field layout is:

```text
head: 4 | / | first across-class grid: 9 | / | second across-class grid: 9 | local suffix: 3
```

The first grid indexes F,G,H,I,A,B,C,D,E; the second indexes **G,H,I,A,B,C,D,E,F**. The final three positions are G,H,I **again**. Each grid can be mapped without a free class permutation onto the solved physical IAB/CDE/FGH tile coordinates.

Across four quarters, the entire 108-site carrier thus has a *hypothetical* typed breakdown: **16 header marks + eight delimiter slashes + 36 first-grid marks + 36 second-grid marks + 12 local-control marks = 108**.

This is an arithmetical and serial-phase consequence of the chosen delimiters, not an original Playdead instruction, not proof of two Xbox rows, and not independent corroboration from the coincidental 16 macOS printer strips. CX-E3 explicitly refutes six unchanged-original-Xbox-row interpretations.

### Raw second-grid physical observations

Each cell is a directly observed mark or unknown (`?`). Classes are in authentic **IAB/CDE/FGH** order.

| Quarter | Physical row 1 | Physical row 2 | Physical row 3 | Known of nine |
| --- | --- | --- | --- | ---: |
| Q1 | `--/` | `-?-` | `-?/` | 7 |
| Q2 | `?//` | `/??` | `-/ -` (without space `-/-`) | 6 |
| Q3 | `-?-` | `-/?` | `/--` | 7 |
| Q4 | `??/` | `?.?` | `?..` | 5 |

The slash/dash first three quarters and slash/dot last quarter remain two separate alphabets.

## A useful exact rejection and a newly constrained alternative

Grant, temporarily, the same minimal "exactly one minority mark" idea tried for CX-E2, allowing the exceptional position to run across each **physical row** or each **physical column**. Each fixed 3×3 source has at most two polarities × 3³ configurations per orientation. Hold the physical IAB/CDE/FGH registration fixed and enumerate every compatible realization.

| Second nine-field quarter | One-minority per physical row | One-minority per physical column |
| --- | ---: | ---: |
| Q1 | **1** | **0** |
| Q2 | **0** | **1** |
| Q3 | **1** | **1** |
| Q4 | **2** | **3** |

Thus applying the *same physical-row reader to both across-class nine-fields in every quarter is exactly impossible* under the known Q2 symbols. A column reader survives Q2. Conversely, a universal column reader fails Q1.

These negatives concern those exact grammars, not general source-native row/column instructions. The necessary *axis switch* is presently invented, with no authored selector.

## The Q1→Q2 relationship

There is a particularly economical, complete pairing:

```text
Q1 second field     Q2 second field
--/                 ///
-/-       ---->     /-/
--/                 -/-
```

**Apply a matrix transpose, then swap `/` and `-`.** The completed Q1 grid becomes the completed Q2 grid exactly. These are the **unique** completions of Q1 under its surviving row-minority grammar and Q2 under its surviving column-minority grammar.

More importantly, before imposing those completions, the transform has **zero disagreements at all six locations observed in both source and transformed target**. Under the frozen physical mask, among the full eight D4 geometric orientations × two binary polarity maps:

* Exactly **two of 16** produce zero contradictions for Q1→Q2. The full transpose-plus-complement uses all **six** jointly known symbols; a 90°-rotation-plus-complement alternative has only **five** jointly known symbols.
* **Zero of 16** variants give a perfect Q2→Q3 second-field transfer.
* **Zero of 16** variants give a perfect Q3→Q4 transfer using the native two-way slash/dash→slash/dot bijections.

So the data permit a specific **Q1→Q2 special relationship**, while *rejecting* the simplest universal "apply a D4 symmetry and the same binary-role transform every quarter" interpretation. The first nine-grid fields also reject literal reuse of that Q1→Q2 transpose/complement relationship at three of four compared observed sites. These are important negative controls, not blemishes to hide.

The Q1 row-minority token is `212` (the slash column chosen per row), and the Q2 column-minority token is also `212` (the dash row chosen per column). This equality is an algebraic consequence of the completed transpose/invert pairing; it must not be counted as a second independent hit.

## Exact label-count null: how often could this happen?

The null holds **which Q1/Q2 grid positions are observed** fixed, and also holds the number of observed slashes in each nine-grid fixed: Q1 has seven known sites with two slashes, Q2 six known sites with four slashes. Reassign slash/dash freely within observed positions, without changing any missing-site mask.

There are precisely `C(7,2)×C(6,4)=21×15=315` equally weighted permutations. Exhaustive counting, not Monte Carlo, gives:

| Event in this explicitly defined 315-case null | Cases | Proportion |
| --- | ---: | ---: |
| At least one D4/polarity relationship with no known contradiction, regardless of matched-site count | 110 | 34.92% |
| At least one with no known contradiction and **six or more** compared observations | 28 | **8.89%** |
| Unique Q1 row and Q2 column minority completions both exist | 144 | 45.71% |
| Those unique completions are also exact transpose/complements | **8** | **2.54%** |

Given that both minority constraints have unique completions, the exact transform occurs in **8/144 = 5.56%** of the conditioned sample.

This is a *descriptive conditional reference model, not a p-value for the historical puzzle*. The axes, quarters, rail windows, six-overlap threshold, unusual two-field split and transform family emerged after extensive looking at the sticker data. The true discovery multiplicity is not corrected by these 315 cases. Nor do these priors preserve every frame and cyclic constraint of the existing U2/U4 families.

## Five more prospective forecasts, now frozen separately

Grant the source-class layout, Q1 row-minority grammar, Q2 column-minority grammar, and their exact transpose/complement relation. Without touching the observation ledger, these uniquely fill two unknown physical sites in Q1's second grid and three in Q2's.

| Physical residue | Image class | CX-E4 conditional forecast | Earlier one-minority serial-frame grammar | Discrimination |
| ---: | --- | :---: | --- | --- |
| 16 | G | `-` | `-` | Agree |
| 22 | D | `/` | `/` or `-` | New restriction |
| **45** | I | **`/`** | **`-`** | **Direct clash** |
| 49 | D | `-` | `/` or `-` | New restriction |
| 50 | E | `/` | `/` or `-` | New restriction |

These have been stored as [CX-E4-v1 machine-readable conditional forecasts](../../data/conjecture-lab-cx-e4-transport-predictions-2026-10-09.json), **separate** from the six CX-E2 forecasts. Residue **45** is a clean, newly defined rival discriminator (in addition to 6/41/64 from CX-E2). Neither rival's conditions are established as the intended code mechanism. Physical observations collected *after* this freeze could discriminate them, without constructing the answer retrospectively.

## The final three G/H/I sites are not a simple universal copy flag

The last three sites of each 27-quarter revisit classes **G,H,I** already present in the nine-site suffix grid:

* Q1 H: residue 17 is `/`, 26 is `-`; different.
* Q2 H: residue 44 is `-`, 53 is `-`; identical.
* Q3 G/H/I: residues 70/71/72 are `---`, residues 79/80/81 are `///`; **three complementary physical pairs**.
* Q4's corresponding pairs have missing observations.

Therefore neither "always repeat the earlier GHI symbols" nor "always invert them" works for every quarter with existing physical evidence. A more complex selector may remain possible, but cannot borrow either of those direct rules. Even Q3's visually interesting `---`→`///` carries retrospective-selection risk.

## Native consumer search outcome and next gate

The archived original Xbox rows provide a 36-wide surface but fail every literal first/second-grid alignment tested in CX-E3. The real `534brn` damaged page remains a same-object destination but supplies no recovered four-quarter transposition instructions. The reversible cover genuinely invites physical reversal/layer thinking (Exp. 409–412), yet none of its monitor-to-source comparisons has authenticated a repeated transpose+binary-complement operator; cover sharing between CE and standalone editions is a dependency control.

A reasonable conditional story is that *one grid is data and the next is a transformed copy or instruction*. This study shows an actual example compatible with known observations, while also showing why **a universal algorithm covering all four quarters has not emerged**.

Next useful work: identify from original source material a **specific asymmetric** operation selecting row for Q1, column for Q2, and distinct later-quarter operations, or an external artifact that would naturally receive **two 3×3 planes plus a three-site control field**. Do not maximize agreement over new orientations or compose an English word from current ternary token lists.

```sh
python scripts/conjecture_lab_cx_e4_dual_nine_fields.py
```

**Disposition: interesting and rigorously scoped DEVELOP branch, no validated decoding operation.** The hard negatives and 11 total CX-E2/E4 conditional physical predictions make it suitable for later adversarial testing, but it should remain below authenticated source-first recovery for the missing sticker-facing consumer.

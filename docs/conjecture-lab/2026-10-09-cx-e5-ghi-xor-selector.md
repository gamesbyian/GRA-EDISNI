# CX-E5: G/H/I three-layer Boolean control forces XOR, but only conditionally

_9 October 2026. Speculative, source-class-aware DEVELOP experiment. Reproduce with [exact 16-function and 84-subset enumerator](../../scripts/conjecture_lab_cx_e5_ghi_boolean.py). Inputs: the original 84 physical sticker records representing 66 H108 residues in [observations.csv](../../data/observations.csv). Seven forecasts are [separately frozen as CX-E5-v1](../../data/conjecture-lab-cx-e5-ghi-xor-predictions-2026-10-09.json); none have been entered as physical observations._

## Why the last three marks deserve a typed operation

The [CX-E2/E4 4 / 9 / (9+3) layout](2026-10-09-cx-e4-dual-grid-transfer.md) provisionally treats slash-only 4×27 columns 5 and 15 as separators. The 12-symbol suffix of each quarter then contains a nine-site GHIABCDEF image-class cycle and three more sites for classes G/H/I. Independently the first nine-site field contains F,G,H,I,A,B,C,D,E, so **G/H/I each appear exactly once in all three fields**. These are **same physical-background-class** occurrences, avoiding the earlier mistake of equating nine occurrences of *one* class with nine *different* image classes.

For every quarter, the native serial H108 indices of these aligned three-layer observations are:

| Background class | First field A | Second field B | Final control C |
| --- | ---: | ---: | ---: |
| G | q×27 + 7 | q×27 + 16 | q×27 + 25 |
| H | q×27 + 8 | q×27 + 17 | q×27 + 26 |
| I | q×27 + 9 | q×27 + 18 | q×27 + 27 |

Here q is 0,1,2,3. No image rotation or class permutation is fitted for this three-site alignment.

**Borrowed mechanism:** assume a single Boolean two-input function `C=f(A,B)` applies to all twelve G/H/I triples. Give `/` the value 1; give the *other* mark `-` (Q1–Q3) or `.` (Q4) the value 0. This is a natural shared-slash event/polarity vocabulary, but it is **not established as the intended codebook**. The decision to use G/H/I only and to seek a Boolean function was made *after* the rail-field and symbol patterns were observed.

## Exact experiment: all 16 possible functions, unknown positions existentially quantified

Each two-input Boolean function is one of 16 truth tables, indexed by `(A,B)=(0,0),(0,1),(1,0),(1,1)`. A function survives if **each** of the twelve physical G/H/I triples admits at least one assignment of its currently missing bits consistent with that function. This uses *all partially observed constraints*, rather than only complete triples.

**Result: exactly one of 16 functions survives, `f(A,B)=A XOR B`.**

```text
A B | C
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0
```

A compact hand-check explains exactly why the function is uniquely identified, even though **only one G/H/I triple has all three symbols directly observed**:

1. Q3, class I, residues **63/72/81** are `/ - /`, proving `f(1,0)=1` under the premise.
2. Q2, class H, residues **35/44/53** are `? - -`. To yield output 0 with second input 0, and knowing `f(1,0)=1`, it must be `f(0,0)=0`; this also conditionally predicts residue **35 = -**.
3. Q4, class I, residues **90/99/108** are `. ? /`. With first input 0 and output 1, and having just fixed `f(0,0)=0`, it must be `f(0,1)=1`; this conditionally predicts **99 = /**.
4. Q1, class H, residues **8/17/26** are `? / -`. With second input 1 and output 0, and having fixed `f(0,1)=1`, it must be `f(1,1)=0`; this conditionally predicts **8 = /**.

All four Boolean function values are therefore determined: `0,1,1,0`. The [script](../../scripts/conjecture_lab_cx_e5_ghi_boolean.py) exhaustively checks this deduction including every partly observed tuple, not just these illustrative four.

**Crucial distinction:** the inference of XOR **from an adopted field grammar** is an exact mathematical result. The grammar's authorship and applicability to the CE are not proven. Calling this a "newly decoded XOR channel" would prematurely launder a conjecture.

## Seven frozen conditional forecasts

| H108 residue | Background class | CX-E5 XOR forecast | Existing conditional native-frame/one-slash-tail rival | Type |
| ---: | --- | :---: | --- | --- |
| **8** | H | **`/`** | `-` | **Discriminator** (also refutes CX-E2's `-`) |
| 27 | I | `/` | `/` | Agreement |
| 35 | H | `-` | `-` | Agreement |
| 61 | G | `/` | `-` or `/` | New restriction |
| **62** | H | **`/`** | `-` | **Discriminator** |
| **99** | I | **`/`** | `.` | **Discriminator** |
| **107** | H | **`.`** | `/` | **Discriminator** |

Every predicted mark was unknown in the 66-residue physical ledger at the time of this conjecture. The four disagreements with the older conditional model must remain visible. None of these seven symbols may be filled into the source ledger, and later observations must be compared against the [frozen data fixture](../../data/conjecture-lab-cx-e5-ghi-xor-predictions-2026-10-09.json), not against a retrofitted function.

## Two decisive controls against exaggerating the finding

### Control 1: unrestricted nine-class XOR fails outright

Instead of privileging the final three G/H/I fields, apply `A XOR B = C` to *every* class A–I in all four 27-site quarters, using the same three serial observations separated by nine. There are **eight completely observed input/output triples**; XOR matches only **three**, contradicting **five** physical triples:

| Quarter | Class | A,B,C actual |
| ---: | --- | --- |
| Q1 | E | `/--` |
| Q2 | B | `///` |
| Q2 | C | `///` |
| Q3 | C | `-/-` |
| Q3 | F | `///` |

Thus a generic "three stacked foreground planes combine by XOR" **is physically falsified**. Only a selective/metadata interpretation restricted to G/H/I avoids the counterexamples. The G/H/I selection has a motivation **conditional** on the 4/9/(9+3) segmentation, but the segmentation itself remains speculative.

### Control 2: the apparent uniqueness has a look-elsewhere cost

Test each of `C(9,3)=84` three-class subsets under the **same** existential-completion and one-global-Boolean-function rules:

* **3/84** subsets uniquely force XOR: `AHI`, `DHI`, and `GHI`.
* **19/84** subsets force *some* unique Boolean function, not always XOR.
* **44/84** three-class subsets have **zero** surviving Boolean functions.

These are counts of conditional compatibility, not corrected significance probabilities. The full prior search over dimensions, groupings, rail locations, Boolean/non-Boolean operators and previous experiments is much wider than 84 trials. The G/H/I suffix role distinguishes the intended tested subset from an unconstrained three-class search only **after granting the hypothetical delimiter format**.

## Relation to the earlier E2/E4 models and historical puzzles

The original Xbox and PC puzzle history supplies real precedents for separating payload from structural marks, and the historical Gate-98 puzzle supplies real layered-image transformation precedents. Neither authenticates literal binary XOR in this sticker position. Direct old Xbox row identity was also rejected in [CX-E3](2026-10-09-cx-e3-native-reader-negatives.md).

The mature body-frame and one-slash-tail families contradict four new forecasts at **8/62/99/107**. CX-E2 already freezes **8=-**, making **8** a particularly high-value future separator between revival ideas rather than just between a new idea and the incumbent.

The new layer model's real benefit is a **human-executable candidate procedure**: identify two slash rails, read the two 3×3 class-indexed planes, and use the three repeated G/H/I class marks as a binary XOR comparison. What it **does not** supply is a native 4-prefix instruction, an independently attested endpoint for the remaining first six classes, a reason for applying this rule to four quarters identically, or a completed visual/linguistic message.

## Status, priority and reproduction

```sh
python scripts/conjecture_lab_cx_e5_ghi_boolean.py
```

**DEVELOP outcome:** one exact Boolean-function identification, seven new frozen conditional predictions, and both matched-class selection and global-XOR negative controls. **VALIDATE outcome:** no newly observed independent sticker, authorial operation, or decoder. Prioritize a source-native G/H/I triple/check-bit cue and future independent physical observation (especially 8/62/99/107), while retaining the more directly attached damaged `534brn` source as the main endgame destination.

If no independent input grammar ever emerges, stop this branch rather than overfitting the still-unknown marks into a desired plaintext.

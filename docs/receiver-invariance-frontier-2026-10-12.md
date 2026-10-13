# Closed-corpus receiver-invariance frontier: a 23-of-27 common readout and terminal-100 degeneracy

**Date:** 12 October 2026. **Mode: DEVELOP, with bounded source-negative controls.** No CE foreground receiver, new physical mark, password, decoded image or Playdead operation has been established. This is a cross-model analysis of explicitly selected, typed readout probes rather than a search for attractive words.

Companion to [Experiment 451's depth-control result](experiment-451-readout-consumer-controls.md), [Experiment 456's axis rivalry](experiment-456-q4-axis-consumer.md), [Experiments 365–366 layered complete masters](experiment-365-completion-universe.md), the [current sticker evidence](../data/observations.csv), and the [source-first 244-candidate atlas in PR #201](https://github.com/gamesbyian/GRA-EDISNI/pull/201). Research code: [finite-model readout script](../scripts/audit_finite_receiver_invariance.py) and [actual original-printer matched-length control](../scripts/audit_middle_depth_printer_control.py).

## Question

If no new physical stickers ever appear, **which presently definable readouts are identical across every candidate completion**, and precisely where do others differ? Do these fixed outputs match the native dimensions or content of the other two original Playdead printer corpora?

This is an *answer-identifiability preflight*, not a decoder-selection criterion: a constant output is useful only if an independently justified external consumer specifies that operation.

## Inputs and exact independently implemented enumerators

Canon: **84 physical serial records, 66 H108 residues, 42 unknown**. Use the existing current-data Python generators, without filtering for a desired decoded result:

| Family | Complete physical H108 masters | Assumption added |
| --- | ---: | --- |
| U2 | **324** | 3/6 one exceptional mark per physical column of each 3×3 frame; Q4 one slash per class-depth stack |
| U3 | **108** | primary quarter/depth polarity staircase |
| U4 | **12** | first selector-selected surfaces must have valid one-dash-per-column POS3 |
| U5 | **10** | second selected surface must also have valid POS3 |

All populations use the exact same physical CSV, and U5⊂U4⊂U3⊂U2. Enumerators are `scripts/build_completion_universe.py` and `scripts/audit_completion_universe_layers.py`. Each model is conditional. Especially, U2 is **not** a statistically proven generative code.

## Twelve frozen readout probes

The probes are explicitly stipulated, not Playdead-authored or selected because of a text hit. The table reports the **number of distinct possible outputs**. Invalid positional code is counted as a distinct result rather than filtered away, except when the definition of U4/U5 already requires validity.

| Readout | U2 | U3 | U4 | U5 | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Raw 81 body marks | 18 | 6 | 5 | 4 | full physical first 81 |
| Raw 27 Q4 marks | 18 | 18 | 6 | 4 | full physical tail |
| Nine Q4 selector depths | 18 | 18 | 6 | 4 | A–I one-hot 0/1/2 |
| Nine 9-bit A–I body addresses | 18 | 6 | 5 | 4 | slash=1, forward within class |
| Fixed-depth-0 27-mark primary read | 3 | 3 | 3 | 3 | three 9-cell quarter strips |
| **Fixed-depth-1 27-mark primary read** | **1** | **1** | **1** | **1** | strongest all-U2 invariant, already noted in Exp. 451 |
| Fixed-depth-2 27-mark primary read | 6 | 2 | 2 | 2 | three 9-cell quarter strips |
| Selected-depth 27-mark primary read | 68 | 30 | 3 | **2** | Q4 selects body depths per A–I |
| Selected-depth three POS3 words | 16 | 13 | 3 | **2** | invalid 3×3 symbols remain explicit |
| Second-pass terminal POS3 | 2 | 2 | 2 | **1** | INVALID or 100 |
| Dash counts per primary quarter | 2 | 1 | 1 | 1 | printed composition, not ciphertext |
| Whole-master /,-,. census | 2 | 1 | 1 | 1 | printed composition, not message |

**Do not infer special importance from constant censuses.** 54/36/18 and the uniform terminal follow the chosen grammar.

## Result A: one exact all-U2 invariant, even though seven printed marks are missing

The fixed middle-depth read is

```
---/-/-/--//////--//////---
```

It consists of 27 body sites at primary depths `d=1` in Q1/Q2/Q3. Of the 27 sites:

- **20 are directly physically observed** in the canonical sticker list;
- **seven are imputed solely by U2's 3×3 column rule**;
- those unobserved H108 residues are **11, 16, 41, 45, 64, 67, 68**.

The strictly physical mark template, before applying any completion model, is:

```
-?-/-/?/--///?//-??//??/---
```

A literal recipient that accepts a 27-site string could in principle consume the entire first word even without more stickers **if the U2 rule is correct**. But the fixed-depth middle slice was considered in Experiment 451 as a *control* rather than an independently discovered intended operation. It must not be chosen solely because it is invariant.

## Result B: U5 selected readouts vary only at four cells on one physical column

The ten U5 masters yield **two** selected 27-mark words, with four and six master occurrences respectively:

```
-/-////-/  -//////--  /--///-//
-/-////-/  //////---  ---//////
```

(Space separates the three nine-site primary quarters; it is not printed.)

Only readout positions **10, 16, 19 and 25** differ. They map to:

| 1-based readout position | Quarter | Image class | Row, column in `IAB/CDE/FGH` |
| ---: | --- | --- | --- |
| 10 | Q2 | A | (1,2) |
| 16 | Q2 | G | (3,2) |
| 19 | Q3 | A | (1,2) |
| 25 | Q3 | G | (3,2) |

The **other 23 selected output positions are invariant across U5**. Q1 is fully invariant. In the fixed physical picture assembly, the remaining ambiguity is concentrated in the *top and bottom cells of the center column* in the last two body quarters.

This supplies a practical, finite target for a recipient audit: does the authentic CE poster/cover/page have a **nine-position reader** that ignores or collapses these four pixels, or treats the two differing output surfaces as the same instruction? There is currently no evidence that it does.

The nine Q4 selector codes fall into only **four** distinct patterns inside U5; the U5 selected-readout is even coarser at two. Different sticker sequences can thus already produce the same selected output. Claiming the 108-cell master must be uniquely recovered is stronger than the actual identification requirement for such a receptor.

## Selection-aware correction: A/G cover fewer physical sticker positions

The physical class coverage is uneven:

| Class | A | B | C | D | E | F | G | H | I |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Observed of 12 | **4** | 10 | 9 | 7 | 7 | 8 | **5** | 8 | 8 |

A and G have **only 9 of their 24 physical positions witnessed**, the two sparsest classes. Under the simplified null of uniformly choosing 66 of the 108 distinct positions:

- a **pre-specified** pair A/G would have at most nine combined observed positions with probability **0.7519%**;
- the **two least-covered classes chosen after seeing the data** would have a combined nine or fewer with probability **18.8450%**.

The second is the relevant reference for the discovered A/G sparsity, since the classes were singled out after inspecting the readout. It is not evidence for a deliberately authored center-column clue. This model conditions on 66 distinct logical residues, not the real socially mediated discovery process or unequal physical copy counts. The exact combinatorial DP and a synthetic positive control are in [the class-coverage selection-null audit](../scripts/audit_class_coverage_selection_null.py).

**Interpretation:** A/G are useful *locations* to examine on a source-authored physical receiver, but their apparent rarity is largely a selection effect.

## Result C: terminal `100` is a very weak *output discriminator*

Read the Q4 chosen depth at both original body coordinates: `(q,d,j)=(S(j),S(j),j)`. If the resulting nine-cell 3×3 surface has exactly one dash per physical column, its POS3 readout is:

| Population | Valid terminal `100` | Invalid terminal POS3 |
| --- | ---: | ---: |
| U2 | **144** | 180 |
| U3 | **48** | 60 |
| U4 | **10** | 2 |
| U5 | **10** | 0 |

**Crucially, no valid terminal under this exact operation reads anything other than `100`, even in the broad U2 population before imposing first-pass constraints.** Thus the terminal `100` is a structural *conditional consequence* of the occupied-column grammar, Q4 one-hot assumptions and actual observed marks, not a highly selective independently supplied password. It remains mechanically reproducible; its semantic authority has not been demonstrated.

## Result D: literal 27-site direct-printer receiver control is negative

Before imagining new transforms, use the two authenticated old Playdead printer datasets. Search the **existing native printer full-width rows**, without rearranging or stretching: PC/PS4 contains 32 rows × 32 marks; Xbox contains 36 rows × 36 marks. A solved-order PC/acorn copy reorders the *same 32 underlying rows*, so it is a reproducibility control rather than independent evidence.

Compare every contiguous width-27 window, for exactly four source-simple order/polarity variants: identity, reverse, swap slash/dash, reverse+swap. Score minimum Hamming distance.

| Corpus | Native full-length rows | Best mismatch of U2-imputed complete 27 marks | Best mismatch of directly observed 20-mask |
| --- | ---: | ---: | ---: |
| PC/PS4 raw | 32×32 | **6** | **4** |
| PC/PS4 community-solved acorn order | 32×32 | **6** | **4** |
| Xbox One raw (with historical duplicate) | 36×36 | **4** | **3** |

**Zero exact matches in every corpus under all four fixed conventions**, including the strict physical-only 20-site mask. These are a narrowly specified negative control, not a declaration that no older printer image could be used with a different sourced operation. A row-spanning read, independent image overlay or authentic registration could change the question entirely. Avoid describing the PC/acorn raw and solved corpora as statistically independent.

## Next source-first work

1. **Native poster/source picture registration**: discover whether the original poster/cover or the CE-linked 534brn image independently contains a 3×9/3×3 reader ignoring those four A/G cells. If not, do not invent a mask from the present result.
2. **A/G center-column role**: examine the original game status board, SecretMap, nine-sketch poster and reversible cover for *source-defined* control/data/background separation at middle-column top/bottom positions. Only after the original object establishes such geometry should a CE overlay be attempted.
3. **Strongest finite corpus recipient test**: if a real 27-site receiving layout is found, feed **all 68 U2 readouts**, not just the two U5 strings, through a fixed transform. Ask if the output is invariant across U2 or U5 and record exactly which assumptions are required.
4. **Terminal validity control**: evaluate an independent competing body layout / differently typed tail, not merely U4; a terminal 100 alone cannot validate a decoder that was selected to produce it.
5. **Literal printer route**: only reopen the direct printer comparison with *new source evidence* specifying row concatenation, registration or a noncontiguous readout. The four simple versions above have been exhausted.

## Reproducibility and evidence status

```sh
python scripts/audit_finite_receiver_invariance.py --self-test
python scripts/audit_finite_receiver_invariance.py --output /tmp/receiver-frontier.json
python scripts/audit_middle_depth_printer_control.py --self-test
python scripts/audit_middle_depth_printer_control.py --output /tmp/printer-comparison.json
python scripts/audit_class_coverage_selection_null.py --output /tmp/coverage-null.json
```

The readout counts, U5 A/G address mapping, and literal original-printer window distances were **independently enumerated against the live canonical CSV and genuine source text via a separate JavaScript implementation in this research turn**. The committed standard-library Python programs add their own hard assertions, explicit physical counts and small synthetic positive controls. **The committed Python entrypoints have not yet been executed in the repository's CI and do not replace that independent verification.**

No canonical sticker marks, frozen predictions, original captured binaries, machine model, experiment numbering, or existing CI workflows were altered.

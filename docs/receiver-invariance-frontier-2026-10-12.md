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

## Stronger observation-first result: four class words require no primary-machine grammar

The native nine-class triplet construction can be calculated using **only the actual physical records and one independent Q4 assumption**: each class's last three positions contain exactly one slash. Leave every unobserved *primary* position freely binary. Do **not** import POS3, 3/6 per frame, quarter polarity or recursion. Enumerate all compatible depth choices and freely missing primary marks for each class.

| A–I class | Distinct 3-mark words: observations + Q4 one-slash | Under U2 | Under U5 |
| --- | ---: | ---: | ---: |
| A | 8 | 4 | 2 |
| **B** | **1** | 1 | 1 |
| C | 2 | 2 | 1 |
| D | 2 | 1 | 1 |
| **E** | **1** | 1 | 1 |
| **F** | **1** | 1 | 1 |
| G | 6 | 5 | 2 |
| **H** | **1** | 1 | 1 |
| I | 4 | 2 | 1 |

Four class triplets are already completely determined **without any primary occupancy model**:

```text
B = //-  (body residues 20, 47, 74)
E = ///  (body residues 5, 32, 59)
F = ///  (body residues 15, 42, 69)
H = --/  (body residues 26, 53, 80)
```

Every body mark in these four triplets has been physically observed. The Q4 depth is directly given by an observed slash in B, E and F; H has two observed dots, so its slash at the remaining depth is forced **only if** the one-slash Q4 premise holds.

**Evidence level:** This is a smaller, cleaner conditional input to any genuinely native nine-artwork/three-channel receiver. It is much less dependent on our 3×3-machine inventions than U5's 23/27 invariant, but it still does not establish the output rule. Reproduce with [observation-first triplet audit](../scripts/audit_observation_first_class_triplets.py).

## A cheap actual-source incompatibility: duplicated digits in the background URL

The independently recovered background page has nine digits in its path, `534965398`. Suppose, **just for a deliberately literal test**, those digits align sequentially with the A–I picture classes and the same digit must signify the same *three-symbol Q4-selected foreground triplet*. This defines a fixed function from a URL digit to a single class word.

Three source digit groups repeat:

| URL digit | A–I classes | Do the weak observation-first class-word sets overlap? |
| --- | --- | --- |
| 5 | A and F | Yes, `///` is possible for both |
| 3 | B and G | Yes, `//-` is possible for both |
| **9** | **D and H** | **No. D can only be `//-` or `///`; H is fixed `--/`** |

Consequently, **this precise same-digit→same-three-symbol direct codebook fails on physical sticker evidence**, assuming only the one-slash Q4 rule, *without* needing U2/POS3 or new stickers. A different source ordering, codebook with unequal outputs for duplicate digits, use of digit position instead of value, or nonliteral transform is unaffected. Earlier experiments rejected other direct URL digit equality constructions; this extends the negative to the weakest Q4-selected per-class triple.

The candidate's 9-digit alignment and equality rule were chosen as an explicit cheap null, **not** verified original Playdead instructions. The program preserves the pairwise common possible readouts and fails loudly if the verdict drifts.

## Extension: all eight physical rotations/reflections of the source-digit codebook

The immediately preceding D/H rejection holds only when the URL's nine digits are assigned to the nine classes in *serial A–I order*. The original solved background geometry itself supplies a more natural finite trial: arrange the classes as `IAB/CDE/FGH`, then scan **each of the eight D4 rotations/reflections**, without allowing an arbitrary nine-letter permutation.

For each view, impose the same speculative equality rule: identical source digits in `534965398` require identical three-mark class triplets. Count compatible **independent observation-first class words** and the actual complete surviving **U2/U3/U4/U5 masters**, keeping all eight comparisons rather than selecting one attractive orientation.

| Orientated physical 3×3 layout | Weak one-slash-only distinct class outputs | U2 masters | U3 | U4 | U5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| IAB/CDE/FGH | 2 | 2 | 0 | 0 | 0 |
| FCI/GDA/HEB | 0 | 0 | 0 | 0 | 0 |
| HGF/EDC/BAI | 0 | 0 | 0 | 0 | 0 |
| BEH/ADG/ICF | 4 | 8 | 0 | 0 | 0 |
| BAI/EDC/HGF | 0 | 0 | 0 | 0 | 0 |
| HEB/GDA/FCI | 8 | 3 | 0 | 0 | 0 |
| **FGH/CDE/IAB** | **16** | **28** | **6** | **6** | **6** |
| ICF/ADG/BEH | 0 | 0 | 0 | 0 | 0 |

The identity row-order `IAB/CDE/FGH` is actually the native physical artwork arrangement, whereas `FGH/CDE/IAB` is its **vertical flip**. Under the stronger U5 model, the invented equal-digit rule leaves **six of ten** physically compatible masters *only* with this vertical-flip alignment, and they all produce the **same one of the two U5 selector-readout strings**. That is a precise, finite **conditional branch-selection result**.

**It is not evidence that Playdead intended a vertical flip.** The repeated-digit equality rule was invented for this test, and all eight views were inspected. A genuine externally printed mirror/flip/orientation instruction would be needed to promote the surviving branch. The four weak-model source-compatible orientations and their partial outputs are just as important to preserve as the strict-model six-state survival.

### Exact reference null for the repeated-digit placement

Because the literal same-digit codebook was invented after inspecting the existing candidate outputs, the single surviving strict-model vertical flip needs a selection-aware control. The source path has **three repeated pairs of digits plus three unique digits**. There are exactly **1,260 ways** to place three *unlabeled*, disjoint pairs among nine slots (equivalent to 45,360 distinct digit-multiset arrangements, 36 assignments per pair structure).

For **each of all 1,260 reference pairings**, allow the *best of the same eight physical D4 orientations* to satisfy the U5 candidate codebook. Count complete U5 physical masters, not independently selected class marginals.

| Event over the eight-view search | Number / 1,260 | Exact reference frequency |
| --- | ---: | ---: |
| At least one view retains any U5 master | 44 | **3.4921%** |
| A view retains at least six of the ten U5 masters | 24 | **1.9048%** |
| No view retains any U5 master | 1,216 | 96.5079% |

These are **bounded combinatorial reference frequencies, not evidential p-values**. The 8 views are adjusted for, but the hypothetical repeated-digit equality rule, choice of three-mark class outputs, U5 machine assumptions, original URL selection and large wider hypothesis search were *all chosen with hindsight*. The result is therefore only a constrained speculative lead, requiring an independent Playdead-authored instruction before it could become support for a vertical flip.

Reproduce: [exhaustive eight-orientation duplicate-digit codebook script](../scripts/audit_url_digit_triplet_d4.py). It keeps the full-model survivor sets separate from the much looser product of independent class-word possibilities and includes synthetic positive/negative controls.

## Native A–I receiving surface: class triplets, not just 27-character streams## Native A–I receiving surface: class triplets, not just 27-character streams

Instead of asking only for a 27-mark contiguous word, use the **already-solved nine-picture A–I class structure as the receiver's native coordinates**. For each class take the three selected symbols from Q1, Q2 and Q3. Exact conditional distinct **three-character outputs per picture** are:

| Physical A–I site | U2 | U3 | U4 | U5 | Complete U5 options |
| --- | ---: | ---: | ---: | ---: | --- |
| A (top middle) | 4 | 4 | 3 | **2** | `--/`, `-/-` |
| B (top right) | **1** | 1 | 1 | 1 | `//-` |
| C (mid left) | 2 | 2 | **1** | 1 | `-/-` |
| D (centre) | **1** | 1 | 1 | 1 | `///` |
| E (mid right) | **1** | 1 | 1 | 1 | `///` |
| F (bottom left) | **1** | 1 | 1 | 1 | `///` |
| G (bottom middle) | 5 | 4 | 3 | **2** | `/-/`, `//-` |
| H (bottom right) | **1** | 1 | 1 | 1 | `--/` |
| I (top left) | 2 | **1** | 1 | 1 | `/-/` |

The key is the **number of distinct outputs**, not the visual appeal of the codes. Five sites (B,D,E,F,H) are fully determined even in U2, with no dependence on recursion; seven sites are determined under U5, leaving only A and G.

Using the actual physical arrangement, the nine sites look like:

```text
I  A? B
C  D  E
F  G? H
```

Here question marks mean *U5 output uncertainty* rather than an undeciphered physical sticker. This is an exact **source-typed nine-position readout candidate** with a tightly constrained ambiguity pattern, but no real cover/poster/JPEG artifact has yet been shown to consume these particular three-mark class words.

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

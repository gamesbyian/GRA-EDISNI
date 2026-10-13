# Native A–I Q4 depth selector against authentic receivers (12 October 2026)

**Research mode: DISCOVER/DEVELOP.** This study deliberately **assumes** a typed, same-background-class selector, rather than requiring advance proof that an external consumer exists. It records falsified *particular implementations*, not a prohibition on speculative exploration. No candidate was sent to Steam. No new physical sticker was inferred. Reproduce with:

```sh
python scripts/conjecture_lab_native_q4_receiver.py
```

Inputs: `data/observations.csv` (84 records, 66 distinct residues, 42 unknown) and `data/printer-reference/pc-ps4-acorn-order.txt` (authentic historically reconstructed 32×32 PC/PS4 acorn ordering, original July 2018 community artifact). The script has source-census assertions and a synthetic positive and negative control.

## Why this receiver is better typed than the preceding frame-to-frame selector

Write a primary cell as `P[q,d,j]` with quarter `q=0..2`, depth `d=0..2`, background class `j=0..8` representing A–I, and source residue `1 + 9*(3*q+d) + j`. Write Q4's corresponding last three cells as `T[k,j]`, residue `82+9*k+j` for `k=0..2`. Under the **conditional one-slash-per-class** Q4 rule, the depth `D[j]` is the position of the slash in `T[0..2,j]`.

A type-preserving selected output is then **three rows by nine classes**:

`O[q,j] = P[q, D[j], j]`.

This selects exactly 27 of the first 81 symbols, three per A–I background class. It shares the native depth axis with the Q4 selector rather than arbitrarily using class `j` to address primary frame `j`. This distinguishes it from the earlier 54-output three-letter experiment: both remain independently useful conjectures, but the latter crosses coordinate types.

The current observable Q4 candidate depths, in A–I order, are:

```
A = 0,1,2     B = 2       C = 0,1,2
D = 1         E = 0       F = 1
G = 0,2       H = 2       I = 2
```

**Exactly 18** complete nine-trit depth assignments. In the repository's physical class layout `I A B / C D E / F G H`, that appears as:

```
      I=2         A=0/1/2      B=2
      C=0/1/2     D=1          E=0
      F=1         G=0/2        H=2
```

This is a machine-readable, bounded set of nine panel-selection instructions. Whether these positions address a poster, A–I backgrounds, the solved nine-part image, image layers, or no actual artifact at all remains open.

## Conditional output constraints: binary primary versus a permissive alternative

The **observed alphabet split** is slash/dash in primary residues 1–81 and slash/dot in Q4 residues 82–108. It is still an **assumption**, rather than independently discovered marks at the 42 missing positions, to impose this binary alphabet on every unknown primary cell. Both variants are now explicitly reproducible:

```sh
# Evidence-aligned, conditional two-sign primary alphabet:
python scripts/conjecture_lab_native_q4_receiver.py
python scripts/conjecture_lab_native_q4_base27.py

# Deliberately permissive three-sign primary stress test:
python scripts/conjecture_lab_native_q4_receiver.py --allow-primary-dots
python scripts/conjecture_lab_native_q4_base27.py --allow-primary-dots
```

For each of the nine primary frames, enforce exactly one minority in each vertical 1-4-7 / 2-5-8 / 3-6-9 triplet. In the **binary** case, only slash and dash are possible in primary missing cells; in the permissive alternative, unknown dots are also admitted. Q4's same 18 depth assignments are unchanged.

Exact output projections:

| Background class | Binary primary: distinct three-sign selected outputs | Permissive primary |
|---|---:|---:|
| A | 8 | 18 |
| B | **1: `//-`** | **1: `//-`** |
| C | 2: `-/-`, `-//` | 2 |
| D | 2: `//-`, `///` | 3 |
| E | **1: `///`** | **1: `///`** |
| F | **1: `///`** | **1: `///`** |
| G | 6 | 15 |
| H | **1: `--/`** | **1: `--/`** |
| I | 2 | 4 |

The per-class sets cannot be freely multiplied as though independent; multiple selected cells may share a primary minority triplet.

Exact 27-output-symbol count bounds across all compatible primary completions and 18 Q4 selectors:

| Symbol | Conditional binary primary | Permissive primary |
|---|---:|---:|
| Slash `/` | **15–23** | 14–23 |
| Dash `-` | **4–12** | 4–12 |
| Dot `.` | **0** | 0–6 |

Each bound is obtained by optimizing the admissible primary-triplet assignments for every Q4 selector, not by replacing missing observations with guessed physical marks. Under the binary assumption, there can be at most **12 non-slash positions** (13 under the permissive model). A literal one-non-slash-per-character fill of the 22-character historical Viewgate placeholder is therefore impossible under either specified operation; a different packing convention, slash-as-data reader or downstream transform remains available. The archived 22 underscores are **not evidence of a functioning input field**.

A tempting alternate idea is to treat the Q4-selected three quarter marks per class as an exceptional-position index for a second 3×3 coordinate on each poster sketch. **That fixed implementation fails:** classes E and F must both read `///`, providing no unique minority. A separately specified fallback would constitute a new variant, not a confirmation of this rule.

## First direct receiver test: original 32×32 acorn printer artwork

Interpret `O` as a literal 3×9 raster, and ask whether it can be a contiguous exact window of the 32×32 *original solved-order PC/PS4 acorn glyph image*. To avoid privileging an arbitrary placement, enumerate all windows of either native 3×9 or transposed 9×3 shape; all row/column reflections; and every global permutation of the three glyphs. For every window, check exact compatibility with **every observed physical sticker symbol**, the primary one-minority-per-triplet rule, and all 18 Q4 choices. Unobserved physical marks are free and chosen optimally within these hard constraints.

Tested `6 glyph bijections × 8 orientations × 720 placements × 18 selectors = 622,080` registered candidate windows.

**Result: zero exact compatible windows.** Of the **34,560** possible printer windows after orientation and global sign relabelling, only **four** even match the twelve compulsory symbols from classes B/E/F/H. Those four each still require **3, 4, 4, or 5** disagreements after exact testing of the remaining primary constraints and all legal selectors. Among *all* 622,080 configurations, the best retrospective window still needs **one disagreement** in the 27-symbol selected output. One disagreement is emphatically **not a near-solution**, because this is an aggressively multiple-tested minimum. The robust result is only the absence of an exact match in this generously parameterized, literal-window family.

The script computes exact minimum disagreements for each case using independent triplet constraint minimization; it does **not** greedily impute unknown stickers or assume that 27 output marks are independent.

Controls: A synthetic 3×9 raster constructed from an actual compatible primary completion and one legal Q4 selector must cost zero. Altering the forced E-quarter-0 slash to a dot must incur at least one necessary disagreement. The original acorn input is sourced from the contemporaneous 2018 community archive; the unsolved Xbox printer's publication row order is **not** silently promoted to a true solved 2D image.

## Nine-class readout as a speculative nine-character ternary/base-27 code

One natural consumer-oriented experiment reads each class's selected three signs as one three-trit character, tentatively in serial A–I order. This is a **deliberately assumed** symbol-to-text bridge, not evidence of a password.

**Key correction from the initial exploratory report:** allowing dots at unobserved primary positions produced **6,480** classwise combinations and **5,808** globally compatible nine-class raw outputs. That number is valid only for the *permissive ternary-primary alternative*. The much more source-aligned **binary-primary** model yields **384** classwise combinations and only **364** globally compatible outputs. Across the nine classes, 20 combinations are eliminated by shared-triplet constraints. These counts and the alphabetic projections below are checked by [`conjecture_lab_native_q4_base27.py`](../../scripts/conjecture_lab_native_q4_base27.py) in both modes.

For each legal output and every fixed global assignment of slash/dash/dot to ternary 0/1/2, three trits give a number from 0 through 26. The two class words E and F are *both compulsory `///`*, so **fifth and sixth output codes must be identical**. Their shared code is always **0, 13 or 26**, depending on the slash's digit value. Under an A=0 alphabet, this maps to A, N, or a nonalphabetic 27th code; under A=1, to a nonalphabetic zero, M, or Z.

Exact counts of nine-class outputs in which *all nine* base-27 codes fall within the specified alphabet:

| Glyphs mapped to digits 0/1/2 | Binary A=0 | Binary A=1 | Permissive A=0 | Permissive A=1 |
|---|---:|---:|---:|---:|
| `./-` | 320 | 364 | 5,464 | 5,808 |
| `.-/` | 0 | 364 | 0 | 5,808 |
| `/.-` | 320 | 0 | 5,464 | 0 |
| `/-.` | 364 | 0 | 5,808 | 0 |
| `-./` | 0 | 320 | 0 | 5,464 |
| `-/.` | 364 | 320 | 5,808 | 5,464 |

**These are not independent predictions of different passwords.** All are alternative conventions for the same observed data and conditional model. In particular, 364 compatible raw outputs are still far too many to constitute a decipherment without another selector, artifact-specific mapping or independent receiver response. The natural serial A–I order itself remains a reading choice; rotating/reordering by the physical IAB/CDE/FGH image layout moves, but does not abolish, the equality of the two class outputs.

## Significance for the receiving-artifact program

1. This gives a *specific* external-artifact negative result for one native selector operator, while leaving the operator itself alive.
2. The 27-mark projected carrier has strikingly asymmetric symbol composition, especially the compulsory slash-rich E/F columns. This is a concrete prediction for any proposed receiver to consume.
3. The nine possible poster-piece row/depth selectors form an 18-member *spatial instruction family* without any new sticker. The known nine-sketch iam8bit product photo could in principle receive these coordinates, but source documents [Experiment 481](../experiment-481-poster-cross-edition-gallery.md): neither authentic poster print master nor independent class-to-sketch registration has been established, and the same **promotional scene** appears on the separate standalone PS4 product listing.
4. The sticker backgrounds already point to an actual `dat/534brn9653f9j8mmd` route, so the Terminal41 damaged content is still a stronger physically linked destination than Steam. Neither candidate needs to be vetoed as a speculative **consumer** in DISCOVER mode.

**Next conditional experiments:** Treat the 27 output signs as overlay **instructions/masks** instead of a literal acorn patch; try small source-specific ways to register them on the real nine-piece background image (or original nine-sketch poster once reliable pixels exist); and separately test chunked address readings aimed at Terminal41 content and Steam branch passwords. Preserve parameter choices and matched controls. Never mistake a post-search word or one-symbol near-fit for independent validation.

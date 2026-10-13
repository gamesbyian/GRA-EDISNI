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

## Conditional output constraints

For each of the nine primary frames, enforce the observation-compatible three-vertical-triplet grammar: every 1-4-7, 2-5-8 and 3-6-9 triplet has exactly one minority symbol (two matching signs, one different), without filling any unknown symbol as though physically found. Unlike an ASCII translation, the new output is still original dot/dash/slash glyphs.

Exact projection of all allowed triplet assignments and 18 selectors yields:

| Background class | Distinct three-symbol selected outputs |
|---|---:|
| A | 18 |
| B | **1: `//-`** |
| C | 2: `-/-`, `-//` |
| D | 3: `//-`, `//.`, `///` |
| E | **1: `///`** |
| F | **1: `///`** |
| G | 15 |
| H | **1: `--/`** |
| I | 4 |

These per-class projections should **not** be naively multiplied into a count of globally compatible outputs: multiple classes share minority constraints inside individual primary frames.

Globally, over every admissible sticker completion and Q4 depth assignment, the 27-symbol output contains:

- between **14 and 23 slashes**;
- between **4 and 12 dashes**;
- between **0 and 6 dots**.

The extrema are found exactly by minimizing/maximizing within each independent primary triplet for each of the 18 selectors; they are not sampling estimates. This implies at most **13 non-slash positions**. If a proposed 22-character Viewgate payload needs *one non-slash mark per character position*, this direct 27-cell interpretation cannot supply all 22. Other interpretations (slash as data, grouped trits, further processing) remain possible. Historical Viewgate's 22 underscores are **not established as a live form**.

A tempting alternate claim is that each class supplies a two-dimensional 3×3 poster coordinate: Q4 picks one coordinate and the exceptional position among the three selected quarter marks picks the other. **That fixed implementation is falsified**. In two classes, **E and F**, all three selected quarter symbols must be `///`, so there is no exceptional position to select. A source-defined default/fallback could still rescue a *different* rule, but cannot be silently assumed to satisfy this one.

## First direct receiver test: original 32×32 acorn printer artwork

Interpret `O` as a literal 3×9 raster, and ask whether it can be a contiguous exact window of the 32×32 *original solved-order PC/PS4 acorn glyph image*. To avoid privileging an arbitrary placement, enumerate all windows of either native 3×9 or transposed 9×3 shape; all row/column reflections; and every global permutation of the three glyphs. For every window, check exact compatibility with **every observed physical sticker symbol**, the primary one-minority-per-triplet rule, and all 18 Q4 choices. Unobserved physical marks are free and chosen optimally within these hard constraints.

Tested `6 glyph bijections × 8 orientations × 720 placements × 18 selectors = 622,080` registered candidate windows.

**Result: zero exact compatible windows.** The best retrospective window, after selecting all parameters, still needs **one disagreement** in the 27-symbol selected output. One disagreement is emphatically **not a near-solution**, because this is an aggressively multiple-tested minimum. The robust result is only the absence of an exact match in this generously parameterized, literal-window family.

The script computes exact minimum disagreements for each case using independent triplet constraint minimization; it does **not** greedily impute unknown stickers or assume that 27 output marks are independent.

Controls: A synthetic 3×9 raster constructed from an actual compatible primary completion and one legal Q4 selector must cost zero. Altering the forced E-quarter-0 slash to a dot must incur at least one necessary disagreement. The original acorn input is sourced from the contemporaneous 2018 community archive; the unsolved Xbox printer's publication row order is **not** silently promoted to a true solved 2D image.

## Significance for the receiving-artifact program

1. This gives a *specific* external-artifact negative result for one native selector operator, while leaving the operator itself alive.
2. The 27-mark projected carrier has strikingly asymmetric symbol composition, especially the compulsory slash-rich E/F columns. This is a concrete prediction for any proposed receiver to consume.
3. The nine possible poster-piece row/depth selectors form an 18-member *spatial instruction family* without any new sticker. The known nine-sketch iam8bit product photo could in principle receive these coordinates, but source documents [Experiment 481](../experiment-481-poster-cross-edition-gallery.md): neither authentic poster print master nor independent class-to-sketch registration has been established, and the same **promotional scene** appears on the separate standalone PS4 product listing.
4. The sticker backgrounds already point to an actual `dat/534brn9653f9j8mmd` route, so the Terminal41 damaged content is still a stronger physically linked destination than Steam. Neither candidate needs to be vetoed as a speculative **consumer** in DISCOVER mode.

**Next conditional experiments:** Treat the 27 output signs as overlay **instructions/masks** instead of a literal acorn patch; try small source-specific ways to register them on the real nine-piece background image (or original nine-sketch poster once reliable pixels exist); and separately test chunked address readings aimed at Terminal41 content and Steam branch passwords. Preserve parameter choices and matched controls. Never mistake a post-search word or one-symbol near-fit for independent validation.

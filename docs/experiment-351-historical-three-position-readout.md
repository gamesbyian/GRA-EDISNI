# Experiment 351 — historical three-position readout provenance

_Status: completed archival provenance audit, 1 Oct 2026._

## Question

Experiments 348–350 now independently support most of the primary foreground skeleton without importing the incumbent machine:

1. twelve consecutive 3×3 foreground squares were historically proposed;
2. a common 3/6 symbol census is predictively favored over 4/5;
3. conditional on 3/6, one minority mark per column is predictively favored over unrestricted placement, while one-per-row and permutation-matrix rivals fail.

The remaining G1 question is narrower:

> Before the present machine reconstruction, did community solvers independently propose that a position inside a three-place carrier should be read as a three-valued coordinate, symbol, address, or selector?

This is a provenance question, not a semantic decode.

## Frozen archive

Use the pinned public export:

- repository: `gamesbyian/playdead-unofficial-exports`
- commit: `5e5897e2ce70dad5a2bd85e459770637cb36610f`
- primary channel: `Playdead Unofficial - ARG - solving-breakout [463106924708233216].txt`

Search terms were limited to three-position / ternary vocabulary and historically documented sticker layouts, including `3x36`, `trifid`, `ternary`, `trinary`, `base 3`, `groups of three`, `each column`, and explicit three-row language.

## Recovered historical proposals

### 23–30 Dec 2022: 3×36 and Trifid

On 23 Dec 2022, lime8159 posted the stickers as a `3x36` visualization.

On 30 Dec 2022, the same solver wrote:

> "currently trying the trifid cipher on the stickers in a 3x36 format, so each column should correspond to a letter"

and reported only a handful of determined letters in the 36-column output.

This is important because Trifid is intrinsically a three-coordinate cipher family. The historical proposal therefore supplies a genuine pre-machine example of treating a **three-row sticker carrier as coordinate-bearing material**, rather than merely as a bitmap.

However, its grouping is not the incumbent primary grouping. A 3×36 raw transpose groups residues separated by 36, whereas the current primary POS3 interpretation operates inside the historically attested consecutive 3×3 squares and reads one exceptional position within each physical column.

### Oct 2023: groups of three as letters

On 28–29 Oct 2023, bigdusty and lime8159 explicitly discussed splitting the 108-character sequence into 36 groups of three and assigning each group to a letter. bigdusty wrote that "each set of 3 characters represents a letter of the alphabet"; lime8159 recalled trying both `36x3` and `3x36` variants.

This independently reinforces the discoverability of a **three-symbol local code**. It still does not specify exceptional-position coding.

### 29 Oct 2023: explicit ternary/binary discussion

darkmatter_11 explicitly referred to "ternary/binary" sticker interpretations, but rejected them as underconstrained because there were too many ways to split the data and assign symbols to digits, and because the dot-only-at-the-end structure was unexplained.

This is negative but useful provenance: ternary coding was an available community idea well before the current machine, yet the archive does not show a historically supplied rule fixing the exact trit registration.

### 22 May 2026: hierarchical 9+3 numeric readout

lime8159 later proposed in a 9×12 orientation that the first nine bits might encode one number and the final three another smaller selector/index, with a book-cipher example.

This independently motivates hierarchical numeric interpretation of the 9+3 carrier, but again does not specify how the first nine symbols become three ternary values.

## Result

The archive supports the following historical operation class:

> three-position / three-symbol sticker groups can plausibly be read as coordinate or indexed symbolic units.

It does **not** currently supply the stronger incumbent statement:

> in each first-81 3×3 square, each physical column contains one minority mark and the minority mark's row position is the ternary value for that column.

No recovered pre-machine message in this audit states that exact mapping, an equivalent top/middle/bottom trit rule, or an equivalent three-column exceptional-position code.

## Epistemic consequence

Experiment 351 upgrades the *discoverability* of ternary/three-position readout from a purely present-project invention to a historically explored operation class.

It does **not** upgrade exact POS3 to Layer 0 or to an independently established historical operation. Experiments 348–350 establish the physical one-per-column skeleton; Experiment 351 establishes that three-position coordinate reading was historically thinkable. The remaining bridge is still:

> Why should the row position of the minority mark inside each column be the value, rather than some other function of the 3×3 square?

That bridge must be supplied by an independent clue, a genuinely predictive comparison against bounded rival readouts, or a demonstrated Playdead operation with the same positional semantics.

## Do not infer

Do not infer from this audit that:

- Trifid is the intended cipher;
- the 36-letter historical partial output is meaningful;
- raw 3×36 grouping is equivalent to current POS3;
- standard base-3 digit labels 0/1/2 are independently fixed;
- top-to-bottom orientation is independently fixed;
- one-per-column occupancy automatically implies positional ternary semantics.

The archival result is structural provenance only.

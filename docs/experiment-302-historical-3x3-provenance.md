# Experiment 302 — historical 3×3 assembly provenance recovery

_Date: 2026-09-29_

## Question

How much of the community's original nine-piece A–I sticker-image assembly can be recovered independently today, and what part still depends on later/current reconstruction?

This follows the September-27 verification handoff, which explicitly recorded the labeled community 3×3 assembly/order as a missing historical input.

## Recovered public chronology

The long-running public `twinysam/INSIDE-ARG` repository preserves the nine-piece puzzle chronology and original Discord references.

The current public record states:

- **1 Feb 2020:** early attempt at assembling the nine sticker-image pieces;
- the community assigns the labels **A through I** to the nine image classes;
- **21 Feb 2020:** another early image interpretation attempt;
- the assembled background is recognized as the in-game printer;
- **19 Mar 2020:** the first observed C-class sticker completes the set of all nine image classes;
- immediately afterward, all nine pieces are shown together for the first time.

The preserved Discord identifiers are useful archival anchors:

- A–I labeling message:
  `https://discord.com/channels/460626942190813184/461275582970462209/673020230200721428`
- first-C / all-pieces-complete context:
  `https://discord.com/channels/460626942190813184/461275582970462209/690392081583177739`
- first complete nine-piece assembly message:
  `https://discord.com/channels/460626942190813184/461275582970462209/690395145245425724`
- original Discord attachment referenced by that assembly message:
  channel `461275582970462209`, attachment `690395145094299678`, filename `unknown.png`
- public Imgur mirror historically referenced by the community README:
  `https://i.imgur.com/846shEE.jpg`

The public repository therefore establishes that a labeled nine-piece assembly existed in March 2020, years before the present sticker-machine reconstruction.

## Source-pixel recovery from the 2026 Discord export

The 2026 public Discord export removes the previous source-access block.

The exported `#solving` transcript contains the 20 Mar 2020 attachment URL:

`https://media.discordapp.net/attachments/461275582970462209/690395145094299678/unknown.png`

and resolves it to the locally archived asset:

`assets/unknown-c89e81cb90765451.png`

in `twinysam/playdead-unofficial-exports` / the working fork `gamesbyian/playdead-unofficial-exports`. At the inspected fork head `5e5897e2ce70dad5a2bd85e459770637cb36610f`, the asset blob SHA is:

`91268fd6700f0f8fc01527f51e63f8c2f6cb7e43`

The image is readable and visibly carries the historical A–I annotations. The old CDN/Imgur availability problem is therefore closed.

The project's current physical registration remains:

```
I A B
C D E
F G H
```

The export also resolves the convention question directly from dated chat, rather than from visual inference.

On **1 Feb 2020**, before the final C tile was recovered, the community states that its arbitrary A–I labels are arranged, “starting top left, from left to right, working down”:

```
I A B
C D E
F G H
```

The same discussion says `A = 001`, hence `I = 000`. On **23 Feb 2020** the mapping is restated explicitly as `001=A`, `002=B`, `003=C`, “etc.” This independently fixes the serial/background convention:

```
serial mod 9: 0 1 2 3 4 5 6 7 8
image class:  I A B C D E F G H
```

This is exactly the project's current registered physical carrier. The current `IAB/CDE/FGH` layout is therefore directly historically attested, not reconstructed only in hindsight.

A second archived asset makes the historical interpretation even less ambiguous:

- `assets/StickerSolution-dc12d5e516ca4922.png`
- identical duplicate: `assets/StickerSolution-f19fd331a635aebf.png`

The `#tldr` export posts this on **28 Apr 2020** under the caption “The Sticker Puzzle Solution.” The image itself labels the 3×3 pieces in the exact row-major order `IAB/CDE/FGH` and prints the recovered destination:

`dat/534brn9653f9j8mmd`

with the historical Terminal 41 URL beneath it. This closes the provenance chain from numbered sticker image classes -> nine-piece printer assembly -> recovered text/path.

Crucially, this “Sticker Puzzle Solution” refers to the **faint background-image layer** on the numbered stickers. It does not solve or semantically decode the separate foreground `/ - •` master that the present project models as H108.

This distinction now becomes:

- **historically attested and source-recovered:** labels A–I existed; the exact top-left/row-major order was `IAB/CDE/FGH`; `A=001` and `I=000`; all nine pieces were assembled; the image was recognized as the printer; and the final source attachment is readable;
- **present-project work:** the later 4×3×3×3 address semantics, POS3 rails, Q4 selector, recursion, routing, and terminal remain modern deductions rather than historical community discoveries.

## Epistemic consequence

The September-27 handoff's "blocked pending labeled A–I order" condition can now be refined.

The historical existence, date, and source pixels of the labeled complete assembly are no longer missing.

That means:

1. the human-solve chronology can safely say that the nine-piece image puzzle and A–I labeling were solved/available in 2020;
2. the current machine's `IAB/CDE/FGH` physical layout is directly supported by dated historical community text;
3. anti-hindsight claims may cite both the recovered attachment and the explicit February-2020 row-major ordering / serial-label convention;
4. no remaining source or convention gap exists for the nine-image carrier orientation itself.

## Status

**Complete historical carrier-provenance recovery.**

The historical assembly event, source identifiers, original exported pixels, row-major A–I spatial order, and serial/image-class phase convention are all recovered. The exact current `IAB/CDE/FGH` carrier is historically attested by February 2020.

This closes the orientation-provenance gap without adding any evidence for the later machine grammar.

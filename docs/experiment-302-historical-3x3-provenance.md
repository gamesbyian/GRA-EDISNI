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

However, recovering the pixels does **not** by itself license a silent coordinate rewrite. The historical image's visible A–I labels, the serial mod-9 phase convention, and the project's registered physical carrier convention must be reconciled explicitly. In particular, a visual tile-label ordering need not be identical to the serial-address ordering used later in the machine model.

This distinction now becomes:

- **historically attested and source-recovered:** labels A–I existed, all nine pieces were assembled, the image was recognized as the printer, the exact exported attachment is readable, and this all happened by March 2020;
- **remaining audit:** map the visible historical tile labels through the community's serial/background convention and compare that mapping exactly with the project's registered `IAB/CDE/FGH` carrier.

## Epistemic consequence

The September-27 handoff's "blocked pending labeled A–I order" condition can now be refined.

The historical existence, date, and source pixels of the labeled complete assembly are no longer missing.

That means:

1. the human-solve chronology can safely say that the nine-piece image puzzle and A–I labeling were solved/available in 2020;
2. the current machine may continue using its established physical layout pending the explicit convention reconciliation;
3. anti-hindsight claims may now cite the recovered attachment itself, while still avoiding any unsupported claim that its visible label order is automatically the same coordinate convention as the current `IAB/CDE/FGH` registration;
4. the remaining orientation check is now a bounded provenance comparison, not a source-recovery problem.

## Status

**Source recovered / orientation-convention reconciliation pending.**

The historical assembly event, source identifiers, and original exported pixels are recovered. The only remaining issue is an exact mapping between the historical visible labels and the current serial/carrier coordinate convention.

Do not infer the mapping from aesthetics. Resolve it from dated message context, serial/image-class phase evidence, and the recovered pixels.

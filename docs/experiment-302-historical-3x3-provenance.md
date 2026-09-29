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

## What could not be re-read independently

The original Discord CDN attachment now returns unavailable/expired through the available public archive path, and the historical Imgur mirror is likewise not retrievable through the current research tooling.

Therefore this pass does **not** independently re-read the exact tile orientation from the 2020 pixels.

The project's current physical registration remains:

```
I A B
C D E
F G H
```

That orientation is already used and independently supported elsewhere in the present investigation, but Experiment 302 does not pretend to have re-verified it from the dead historical attachment.

This distinction matters:

- **historically attested:** labels A–I existed, all nine pieces were assembled, the image was recognized as the printer, and this all happened by March 2020;
- **not independently recovered in this pass:** the exact A–I spatial order visible in the historical assembly image.

## Epistemic consequence

The September-27 handoff's "blocked pending labeled A–I order" condition can now be refined.

The historical existence and date of the labeled complete assembly are no longer missing. What remains missing is a live copy of the actual labeled image, or an independently archived transcription of its exact orientation.

That means:

1. the human-solve chronology can safely say that the nine-piece image puzzle and A–I labeling were solved/available in 2020;
2. the current machine may continue using its established physical layout;
3. anti-hindsight claims should not say the exact current `IAB/CDE/FGH` orientation was independently re-read from the March-2020 artifact in this audit;
4. once the Discord archival bot or another archive recovers message `690395145245425724` or attachment `690395145094299678`, the remaining orientation check becomes a simple visual provenance comparison rather than a research problem.

## Status

**Partial recovery / provenance milestone.**

The historical assembly event and exact source identifiers are recovered. The original pixels required to independently verify the A–I orientation are still unavailable.

Do not spend closed-corpus computation trying to infer what the missing screenshot showed. Recover the source artifact instead.

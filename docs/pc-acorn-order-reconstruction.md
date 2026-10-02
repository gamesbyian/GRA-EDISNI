# PC/PS4 acorn row-order reconstruction

_Status: primary-order fixture recovered, 2 Oct 2026._

## Result

A canonical textual ordering of the 32 full-length PC/PS4 printer rows is preserved in the archived Playdead Unofficial Discord export. The attachment was posted on 9 Jul 2018 at 17:35 with the label **“acorn order version.”**

Project fixture:

`data/printer-reference/pc-ps4-acorn-order.txt`

Every row in that file exactly matches one and only one row in the 32-line full-length subset of `data/printer-reference/pc-ps4-raw.txt`. There are no inserted, deleted, edited, or duplicated rows.

## Primary provenance

Archive repository: `gamesbyian/playdead-unofficial-exports`

Discord export: `Playdead Unofficial - ARG - solving [461275582970462209].txt`

Attachment: `assets/inside-pc-long-ascii-cdac293e0bbbcf9f.txt`

Blob SHA: `fe69159b0a31be20230aa66ce16be01deab0c108`

Timestamp / description in transcript: 9 Jul 2018 17:35, “acorn order version”.

## Reconstruction chronology

The transcript supports a bounded description of the discovery process:

1. Solvers noticed systematic slash behavior at the margins, including start/end slash classes and different behavior for dot-bearing rows.
2. A first-appearance-of-slash sort partially organized the rows but was not itself the final solution.
3. The breakthrough arrangement was described as an **alternating interlaced** construction that limited the available choices.
4. Margin slashes and a reported `1:3` / `1:2` distribution were treated as important ordering constraints.
5. The resulting image independently suggested an acorn to multiple solvers and exposed an upright `41` orientation cue.
6. Rows were still manually refined around local image continuity before the preserved textual order was posted.

## Epistemic boundary

The final permutation is primary evidence. A unique deterministic sorting algorithm is not.

The transcript never gives a complete function such as “compute key K from each row and sort ascending.” Reconstructing such a rule now from the known solved permutation would be answer-conditioned model fitting. Any transfer to the CE stickers therefore needs either:

- an independently recovered historical description of the missing interlace rule;
- a rule that can be defined from the raw PC corpus before consulting the solved order and then validated against it; or
- a sticker-native cue independently specifying how analogous margin/interlace structure should be read.

Until then, the recovered acorn order is best used as a **control corpus** for testing candidate ordering algorithms: a plausible historically faithful ordering metric should first recover or strongly concentrate the known PC permutation before being applied to H108.

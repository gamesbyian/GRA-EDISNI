# Experiment 364 — 534brn XMP provenance, GATE/81, and blocked media lanes

_Status: completed triage, 1 Oct 2026. No model change._

## 534brn JPEG metadata

The preserved XMP fragment (`assets/message-0e4be448bc32b1bf.txt`, blob `b6f5ffed`) records:

- `dc:creator` = `AnSet`, which matches the ARG's fictional "Anthony T. Setrinamairé" persona;
- `xmp:CreateDate` = `2016-12-16T14:12:24.351`;
- `rdf:about` = `uuid:faf5bdd5-ba3d-11da-ad31-d33d75182f1b`, the fixed UUID that Windows Explorer writes when file properties are edited by hand.

Consequences:

- The image behind `dat/534brn9653f9j8mmd` was authored and tagged in **December 2016**, about three years before the CE stickers shipped. It belongs to the original ARG asset set, not to the CE design.
- One other asset carries the identical timestamp, `assets/11-c670b31555824d3c.jpg` (255×255). The 21 Jul 2026 discussion shows it is eropkol's header-restored rebuild of the same damaged capture, not an independent original. eropkol estimates the hidden image is greyscale and 128–255 px square.
- No independent intact copy of the 534brn JPEG has been found in the public exports.

## GATE/81

`saf_dat_col` contains `[comms chk. [GATE/81/connect[chk]] … chk stat. [FAIL[1]]]`. This was investigated in 2019:

- `comms/gate/81/connect.html` existed (Last-Modified 2 Jul 2018) as an inactive "Gate transmission" status page that immediately redirected home. Its source is preserved in `assets/unknown-a8d5dd32c4350fd4.png`.
- It predates the CE by 17 months. The numerical match with the sticker body's 81 cells is coincidental, as `community-glossary.md` already states.

## Blocked lanes needing a person

| lane | blocker |
|---|---|
| Wayback CDX inventory of `terminal41.link/*` (to find pages missing from the GitHub mirror) | `web.archive.org` is denied by this research environment's network policy |
| iam8bit making-of video `8vG2A0BjMiY` (sticker printing, sheet or roll format) | age-restricted for the research account; needs manual viewing |
| CE art-card scans | owner declined in 2020; needs a new owner |

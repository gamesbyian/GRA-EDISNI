# Experiment 476: source-native receiving artifacts for INSIDE CE foreground

_Date: 2026-10-08. Bounded source-first audit, not a sticker decode._

## Focus question

Which original INSIDE, Collector's Edition, or Terminal41 artifact
**demonstrably accepts** an externally derived value, and which
candidate receivers only resemble one because of symbol, length,
story, or image coincidences?

This experiment follows the experiment-map's backward-chain method:
establish an artifact's *actual* input affordance, then compare
sticker projections without filling missing symbols or choosing an
attractive output. Exact evidence is pinned in
`data/experiment-476-source-native-consumer-affordances.json`.
The verifier is `scripts/audit_source_native_consumer_affordances.py`.

## Two historical functional positive controls

1. **Original in-game secret-ending lever:** has a demonstrated
   three-direction U/L/R instruction channel and an already-solved
   14-command sequence `UURLRRRUUURLLL`. The candidate physical
   sleeve mapping `/=U, -=R, .=L` was historically proposed
   in the community from 2020 onward. It is an independently
   plausible sticker-consumer **type**, not a documented second
   handler or CE-specific instruction.
2. **Original printer-to-website printing:** a **3 January 2019
   first-party Xbox Wire article by Microsoft's Glenn Gregory**
   says the decoded game-printer text was entered into the
   developer-website email-subscription field, leading to
   corrupted imagery inside a PDF. The [historical Game Detectives
   account](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button)
   specifies that the page's **printer button**, not an ordinary
   newsletter signup submission, consumed the entered field text
   and produced the conditional printout.
   [Contemporary source](https://news.xbox.com/en-us/2019/01/03/unsolved-secret-in-inside/).
   This verifies a genuine historical *text-field-to-print-to-asset*
   consumer, stronger evidence than mere resemblance to a terminal
   display. It **predates** the CE foreground and does not
   document an extra 2019–2020 sticker credential.

Neither positive control supplies an independent **CE-specific
input path**. The earliest original consumer explains previously
solved printer answers, and the bunker lever already has a known
ordinary secret-ending code.

## Preservation-level input test

The original archived Terminal41 source tree in the repo
provides direct checks unavailable from generic analogy:

| Artifact | What the preserved source actually says | New sticker input established? |
| --- | --- | --- |
| `comms_main_viewgate.html` and `_002.html` | Exactly **22 printed underscores** on each. No source `form`, `input`, `select` or `maxlength` element. | **No** in preserved source |
| `sys/printreqstatus_SD.html` | Explicitly indexed `schem[0]` through `schem[3]`: PLANET, LIFE, PROBE, CONDISCON; shows four requirements. | **No fifth ordinary scheme** in preserved status |
| `dat/534brn9653f9j8mmd/index.html` | Static damaged JFIF/Exif-like content and footer `pe^!02un`, followed by dot lines of lengths **8, 2, 1**, then termination address text. The footer has already been decoded in Experiment 413 as **128 UNSOLVED**, a potentially meaningful image-size clue. | **No fixed sticker-to-JPEG repair/key operation** |
| `dat/saf_dat_col.html` preserved ASCII island | Seven plus-delimited fields of lengths **26/22/10/2/3/1/5**, one candidate 22-character value. | **No source-labeled field consumer** |
| Nine shutdown-confirmation pages | Fixed redirects 09→01, already tested in Experiment 408. | **No choice or per-step payload** |
| CE background's nine-piece printer image | Path `dat/534brn9653f9j8mmd` was already the *output* of background reconstruction, with historical Wayback-index-assisted recognition (Experiment 465). | **No foreground index rule in surviving page** |

The footer's prior **128 UNSOLVED** reading (Experiment 413) is a source-native numerical cue and should not be discarded. Experiments 414, 417 and 423 already constrain but do not uniquely repair the JPEG. No source ties the foreground slash/dash/dot cells to lost entropy bytes or fixes a 128×128 pixel consumer. Consequently the page remains an actionable *damaged-artifact recovery* target, not a verified CE-foreground input.

The negative gate is specifically **available preserved clients/pages**.
It does not prove historical server handlers, original POST protocols
or older Wayback revisions never existed. Likewise a 22-character
`Input:[...]` rendering is not a working HTML form.

The 22-character `saf_dat_col` value
`38546uy754j9j6tuk5fi34` parses as a **111-bit unsigned
base36 integer**. The foreground's observed two-binary-sector
model has at most **108 bits** as a *direct unkeyed binary payload*.
Therefore this *particular* direct numerical conversion fails.
This does not exclude Base32 with padding, keyed transforms,
hashing, arbitrary encryption or external information; none
is source-cued here.

## Official CE physical pack-ins not yet ruled out

The [official iam8bit Collector's Edition listing](https://www.iam8bit.com/products/inside-collector-s-edition) independently confirms **three additional physical source surfaces** which must not be silently omitted from a source-first consumer census:

1. An **art card set**, in addition to the separate foreground sticker/background puzzle;
2. A **foldout poster**, for which unfolded front/back content, dimensions and any symbol registration have not been established here;
3. A **premium presentation box** incorporating spot varnish and custom foam inlays, but with no independently documented cipher role.

A [contemporaneous December 2019 unboxing discussion](https://www.reddit.com/r/PlaydeadsInside/comments/eaol69) describes **dozens of concept-art cards** (one commenter asks whether there are about 40). That is a dated eyewitness discussion, not an independently verified card count, and it warns against assuming the included set must consist of nine A–I keys merely because the stickers use nine background images. The [publisher's original unboxing video](https://www.youtube.com/watch?v=zhCdGdqCIRU) offers a more concrete next source to examine frame by frame if high-resolution stills are available.

The [separately sold iam8bit INSIDE PS4 physical edition](https://www.iam8bit.com/products/inside-ps4-physical-game) also advertises a foldout poster. Whether that poster is identical to the CE one is **unknown**, and its mere presence in both sets would not independently license a foreground overlay.

These are **verified included objects**, not verified sticker-code readers. No archival source inspected here specifies that the poster/card/box artwork accepts 9, 27 or 108 slash/dash/dot marks. The concrete source gate is original print-ready art or complete, native-scale front/back photographs, preferably with an independent publisher registration cue. Avoid treating routine glossy finish, folds or collector artwork as a code by default.

## Native-input type audit

Two elementary consequences require **no guesses** about missing
stickers:

- The 81-cell primary sector uses only slash/dash, so its direct
  lever projection is restricted to **U/R**. A Q4-selected 27-cell
  primary readout is also always U/R. No known output of those types
  contains a Left command.
- The final 27-cell slash/dot sector projects only **U/L**, with
  no Right command.

The known bunker code requires **both** Left and Right commands
in an order that cannot be a contiguous cyclic 14-command window
of either sector, nor of the full 108-code in the observed
81+27 sector order, even with arbitrary compatible unknown cells.
Exhausting all 14 password rotations, both forward and reversed,
and 108 possible H108 starts leaves **zero type-compatible placements**.
This independently rechecks the *necessary alphabet* portion of
previous Experiments 342–343; it does not disprove a distinct
lever password reached through an independently specified
noncontiguous selection.

Similarly, all 324 direct Q4-selected primary 27-mark readouts are
slash/dash only (Experiment 451); they are not a 14-command
three-direction input. The historical nine-symbol
`--/--/-/-` digit-index signature is likewise U/R-only and
its exact lever word was already present in 2023 community
De Bruijn sequences (Experiments 398/401).

**No candidate is rejected merely for lacking 9/27/108 literal
slots:** a legitimate compressed string or key could be much
shorter. What is missing is the *specific historical transform*
and actual receiving action, not a matching character count.

## Updated 2016 original-game asset null: `SecretMap`

A newly checked **July 2016 contemporary player discussion** describes
the extracted texture `SecretMap #44506.dds` and immediately notes
a possible **14th marker**. Another participant proposes that the
fourteenth denotes the game's **large final orb**, rather than
an undiscovered fifteenth secret or a later CE clue:

[Original contemporaneous thread](https://www.reddit.com/r/PlaydeadsInside/comments/4sav9x/curious_textures_found_in_the_game_files/).

This is a valuable early alternative explanation predating the
physical Collector's Edition. It **does not prove** that every
map mark registers to a known orb, that the native DDS has exactly
14 marks, or that the marker has been correctly mapped.
The native 2016 Unity texture bytes and scene UVs remain
unrecovered (see `docs/secretmap-original-asset-null-protocol-2026-10-08.md`).
As a receiving artifact, the map is downgraded until the
already-explained 14-orb null is tested on native, unchanged geometry.

It is inappropriate to free-fit the sticker dots onto a degraded
image after the native orb interpretation has been proposed.

## Receiver triage, without invented likelihoods

| Research lane | Status | Exact missing independent evidence |
| --- | --- | --- |
| Existing developer website printer box | **Functionally documented for older printer puzzles** | Actual later CE-specific form or server response; original backend code |
| Secret-ending lever | **Functionally documented, original code already used** | A distinct handler or external CE-selected command ordering |
| CE damaged JPEG + background path | **Real static source, media damaged** | Byte-correct uncensored source and a fixed sticker repair, mask or address instruction |
| CE reversible cover | **Physically real, clue-advertised** | Original print-ready art plus source-defined sticker-to-panel transform |
| CE art cards, foldout poster, spot-varnished box | **Officially verified physical pack-ins, currently unregistered** | Unmodified front/back scans or original production art, including explicit marks if present; compare standalone poster separately |
| `SecretMap` | **2016 extracted graphic reported, native bytes missing** | Native DDS/scene transform, fourteen-orb negative control, and actual extra marks |
| Terminal41 22-place Viewgate | **Static text, not a verified input control** | Original live handler or request/response accepting the purported 22-character field |
| Seven-field safety-data island | **Exact text content verified** | Source-defined schema and label for the field to be consumed |
| Nine shutdown pages | **Fixed redirects; direct consumer closed** | Previously missing alternate branch source |

### What the evidence licenses next

The most informative outstanding question is **not** whether any
sticker-derived word happens to resemble the above text or images.
It is whether a historical CE, printer, cover or game file contains
a direction to *perform an operation on the foreground marks*.
The existing archive's best direct avenues are:

1. Original pre/post 2019 website client/server captures showing a
   **new** field, handler, path parameter or key expectation.
2. Original CE package or cover artwork indicating a **registered**
   readout or instruction for slash/dash/dot marks.
3. Native `SecretMap` only after verifying all fourteen original
   secret-orb marks; its 2016 interpretation supplies a specific
   hostile null, not a ready-made sticker coordinate system.

Absent one of those evidence triggers, further fitted consumer
strings, rotation sweeps, lexical searches or speculative Base36
conversions are not authorized. This experiment does not
declare the mystery solved or exhausted.

## Reproduction

```bash
python scripts/audit_source_native_consumer_affordances.py
```

This standard-library verifier checks the actual two preserved
Viewgate pages, original four scheme labels, damaged CE page footer (and its already-established 128 UNSOLVED reading),
original field fixture, current 84/66 sticker census and
lever-alphabet impossibility. It also checks all artifact registry
source paths exist and records the historical 2016 source
separately. It fails if the source corpus changes materially.

Source independence discipline: the Xbox article is contemporary
publisher testimony about Playdead's earlier printer website; the
2016 `SecretMap` Reddit exchange is community interpretation of
game-extracted art. Neither is a developer statement about how to
solve the later Collector's Edition foreground.

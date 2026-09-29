# Discord community reconstruction and premise revisit

_Date: 2026-09-29_

## Why this matters

A user-supplied FAQ and linked Discord message add historical provenance for the most basic geometry of the sticker puzzle. The community material predates the current machine model and describes a 108-position repeating foreground master, a 9-column / 12-row display, sticker-0 phase anchoring, and an independent 9-state image/background cycle.

The important epistemic correction is that the supplied 108-character string is **not a new blind dataset**. Experiment 297 round-trips it against `data/observations.csv` and gets an exact match to every one of the repository's 82 physical records. It is therefore a historical/community reconstruction of the same public corpus, not 65 additional observations.

That still matters. It moves several facts from "geometry discovered during the present solve" to "geometry independently reached by the community before the present model existed."

## Supplied community material

The FAQ states:

- the symbol sequence repeats every 108 stickers and this has been considered essentially solved by the community for roughly five years;
- the raw sparse 108-character foreground transcription is the string now preserved in `data/discord-community-master-108.json`;
- community visualizations commonly render the 108 cells as 12 rows, with red=`-`, grey=`/`, yellow=`.`;
- indexing is anchored at sticker 0 modulo 108, with the FAQ citing the separate sticker-background puzzle as the reason to align the phase there;
- ordinary Morse and generic ternary-cipher interpretations were considered unattractive because no dot occurs in the first 85 positions;
- the linked discussion includes an attempted pixel-art/rotation interpretation that produced no useful image.

The linked historical message says its author independently reached 108 entries and width 9 by overlapping known records and using image numbering. Its screenshot reports:

- 108 cells = 12 rows × 9 columns;
- 65 filled and 43 empty;
- 15 overlap cells containing 17 extra physical records;
- zero differing-value cells among overlaps.

The author also mentions a production-quantity inference of at least 630 editions from the then-known maximum serial 597. The reasoning for 630 is not present in the supplied excerpt, so this remains attributed context rather than a project finding.

## Experiment 297 — exact round trip

`scripts/audit_discord_master.py` compares the supplied community master with all current repository observations under the community indexing rule:

```text
master character index = sticker serial mod 108
repo residue 108 = serial 0 mod 108
repo residues 1..107 = same-number character indices
```

Results:

- 82 physical records;
- 65 unique H108 residues;
- 15 repeated residues;
- 17 records beyond the first observation of a residue;
- zero disagreements among repeated foreground observations;
- zero disagreements between the Discord sparse master and the repository observations;
- foreground counts: 36 slash, 22 dash, 7 dot, 43 unknown;
- first dot at community index / serial residue 85.
- among every candidate foreground period from 1 through the current maximum observed serial 597, 108 is the smallest period consistent with all symbol collisions; it is also the smallest consistent period divisible by the independent background period 9.

The same audit checks the independent image/background labels. Every repository record obeys:

```text
serial mod 9: 1 2 3 4 5 6 7 8 0
image class:  A B C D E F G H I
```

Thus sticker 0 modulo 9 maps to class I. In the project's registered physical 3×3 image layout, I is the top-left cell:

```text
I A B
C D E
F G H
```

This directly explains the community statement that the background puzzle starts at sticker 0 in the top-left corner.

## What this strengthens

### H108 periodicity and phase

The 108-period master is now supported in three distinct senses that must not be conflated:

1. raw repeat consistency in the physical corpus;
2. an exact present-day reconstruction from the repository records;
3. a historically prior community reconstruction using overlap and image numbering.

Items 2 and 3 are not statistically independent datasets, but item 3 is independent **model chronology**. The 108 cycle and its phase were available before the current routing-machine interpretation.

### The 9-column registration is historically plausible

The 9-column view is not a layout invented after seeing the current machine. A community investigator reports reaching width 9 from the image numbering and overlap structure. This strengthens the intended-human-path case for inspecting the foreground as 12×9 and then subdividing it along the already-present 9-cell carrier.

It does not by itself prove the later 4×3×3×3 address semantics, POS3 rails, or recursive selector operation.

### Repeated records really are a checksum

The 82 current records collapse to 65 unique H108 cells. Fifteen cells are sampled more than once, accounting for 17 extra records, and none disagree. This is strong direct evidence for a deterministic serial master rather than one-off sticker artwork.

### Foreground and background are separate registered layers

The symbol master repeats every 108 while image class repeats every 9. Because 108 is a multiple of 9, the two layers stay phase-locked. The historical reconstruction explicitly used the image layer to orient the foreground layer, which makes the carrier registration a physical clue rather than a purely algebraic convenience.

## What this does not strengthen

### It is not a blind replication of terminal 100

Do **not** describe the Discord string as an independent holdout for the current machine. It is exactly the same observed symbol corpus in sparse-master form. Feeding it into the current reconstruction is a round trip, not a new test.

A genuine external replication would require independently sourced physical sticker readings that are absent from `data/observations.csv`, or a historically frozen prediction/operation that can be shown to predate the present model.

### It does not validate the recursive machine directly

The historical material supports period, phase, width, overlap consistency, and a plausible human entry geometry. Nothing in the supplied Discord excerpt independently supplies:

- column POS3;
- Q4 depth selection;
- recursive substitution;
- request/grant semantics;
- Q3 route shell;
- terminal `100`.

Those remain supported by the project's internal reconstruction and uniqueness work.

## Revisit of old branches and rejected premises

### Ordinary Morse / generic ternary plaintext

No dots occur at indices 0..84; all seven observed dots lie in the late part of the master. This remains a poor fit for an ordinary three-symbol plaintext stream. However, the community's argument should not be overextended into "three symbols cannot be ternary." The current model uses symbols positionally and role-dependently: slash/dash dominate the primary 81 cells, while slash/dot characterize Q4. The historical asymmetry is therefore more compatible with a typed positional mechanism than with a homogeneous ternary text stream.

Action: keep generic Morse/ternary plaintext search quarantined. Do not treat the FAQ's objection as evidence against positional ternary structure.

### Pixel art and rotations

A historical investigator explicitly reports trying rotations for hidden pixel art without success. This is not an exhaustive image-null proof, but it is a useful preregistered negative result. It reinforces the existing quarantine on generic bitmap/pixel-art fitting.

Action: no reopen without a new externally supplied image operation.

### 81 + 27 split

The dot desert does not prove the primary/Q4 boundary, because unknown cells remain. Still, "no dot before 85" is qualitatively consistent with the project's independently derived late 27-cell selector region beginning at 82. This is corroborative only; the 81+27 split should continue to stand on structural machine evidence.

### Physical-column POS3 and rail orientation

The historically prior 9-column visualization materially improves the human-plausibility prior for the project's physical-column grammar. It does **not** independently establish the three 3-cell columns inside each 9-cell frame. Experiments 263–265 remain the relevant tests for that finer partition.

Action: in human-solve documentation, distinguish "9-column carrier visible historically" from "3-cell rail partition derived later."

### Sticker-zero phase / registration

This is the biggest premise upgrade. Phase zero is no longer merely the convenient rotation used by the current solver. The community explicitly motivated it from the separate background-image puzzle, and the present 82-record table reproduces that mod-9 image cycle with zero mismatches.

Action: treat zero phase as externally motivated carrier registration. Still keep the foreground-machine consequences logically downstream.

### Production quantity >=630

Do not import this into the mechanical model. Recover the original argument or source before using it in manufacturing inference.

Action: archival follow-up only.

## Impact on earlier experiment families

This evidence is worth applying retroactively because it changes **which claims are discoveries of the present model** versus **facts already available to a historical solver**.

| Earlier work | Reclassification after Experiment 297 |
|---|---|
| Experiments 1–10: image classes, repeat periods, H108, nine-tile geometry | Strengthened as carrier facts and historical human-entry structure. Experiment 297 independently re-executes the earliest period question and confirms 108 is the smallest collision-consistent period in the present ledger. The community testimony additionally shows 108/9 registration was known before the current model. |
| Experiments 7 and 38: chronological quasi-holdouts | Keep the numerical robustness results, but do not describe H108 itself as a novel prospective discovery if the historical cutoff postdates the community's 108 result. Re-audit wording against actual dates. |
| Experiments 11–20: plaintext/Braille/geometry/production branches | No reopen. The historical no-dot-before-85 observation and failed rotation/pixel-art attempt add prior negative context, while the unverified >=630 production inference belongs only in archival/manufacturing work. |
| Experiment 28: exact 81/27 vocabulary boundary | Still stands on the classified corpus and machine structure. The historical dot desert is corroborative, not an independent proof of the boundary. |
| Experiments 59, 77–90 and 113–114: intended-human path and registration | Strengthened at the front end. Period 108, width 9, 12×9 display, and zero phase are now historically attested; later POS3, diagonal, and selector claims remain present-project inferences. |
| Experiment 62: Trifid/Fractionated Morse audit | Historical community skepticism toward ordinary Morse/ternary plaintext is directionally consistent with the negative result but adds no new statistical evidence. |
| Experiments 89, 100, 171, 188, 191, 192: chronology / historical solvability | Revisit wording. The new material is exactly the kind of dated prior structure those experiments are meant to classify. Distinguish "raw data existed" from "this structural inference was publicly known." |
| Experiments 165–177: evidence reconstruction, repeats, provenance | Strongly cross-checked at the bookkeeping level: the external screenshot's 65 filled / 43 empty / 15 overlap cells / 17 extra records / zero conflicts matches the repository ledger exactly. This is provenance agreement, not a second sample. |
| Experiments 184–190: physical derivation of address and Q4 serial-stack readability | Front-end assumptions become more human-plausible because the 9-column and zero-phase carrier were historically available. The 4×3×3×3 semantics and Q4 selector interpretation are not supplied by Discord. |
| Experiment 204: public-corpus blind stripe | Same-corpus caution becomes more important: community renderings of the same 65 residues cannot be counted as extra blind evidence. |
| Experiment 248 and later human-path work | Update the first two steps from reconstructed hindsight to historically corroborated discovery steps. The remaining bottleneck moves forward to recognizing the finer three-cell POS3 rail and recursive operation. |

No downstream mechanical theorem is invalidated by this reclassification. The main change is epistemic bookkeeping: some early geometry is now better supported and less hindsight-sensitive, while any claim of independent replication from the Discord master must be removed.

## Consequences for the research plan

The highest-value new lane is **historical method archaeology**, not another semantic decode:

1. recover dated Discord posts/screenshots around the original 108/9 discovery;
2. separate independently inferred structure from recycled copies of the same raw corpus;
3. recover the exact argument for sticker-0 phase and the background-image puzzle;
4. look for historically attempted operations, especially anything more specific than generic Morse/ternary/pixel-art guesses;
5. timestamp which pieces of today's human solve path were genuinely visible before the current machine model;
6. preserve negative results as preregistered historical controls;
7. avoid counting same-corpus reconstructions as independent statistical evidence.

This lane can strengthen intended-human-path and anti-hindsight claims without requiring any new sticker to surface.

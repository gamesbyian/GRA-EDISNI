# INSIDE sticker-mystery community glossary

_Date: 2026-09-29_

This glossary records vocabulary actually used by the INSIDE ARG community, historical repositories, Discord discussions, later sticker-analysis projects, and public writeups around the Collector's Edition sticker mystery and its surrounding ARG.

The purpose is **translation and provenance**, not retrospective standardization. Different eras and subgroups use different words for the same thing. Where a term is newer, local to one project, or potentially misleading, that is called out explicitly.

For recurring notation, color, indexing, layout, and presentation practices, see `docs/community-conventions.md`.

## Scope and labels

- **Early community** — terminology visible in 2019–2021-era ARG documentation and Discord-derived chronology.
- **Later community** — terminology found in later Discord work, forked repositories, and 2025–2026 sticker-analysis projects.
- **Current project** — terminology introduced or formalized by the present `gamesbyian/GRA-EDISNI` reconstruction. These terms are included only when useful for translating between old and new work; they should not be back-projected onto historical solvers.

---

## Core physical-object vocabulary

### Collector's Edition / CE
The iam8bit INSIDE Collector's Edition. Community documents commonly abbreviate it to **CE**.

### sticker / CE sticker / Collector's Edition sticker
The numbered seal sticker on the Collector's Edition wrapping. The sticker is the physical object being catalogued.

### sticker number / copy number / chain number / serial / serial number
Names used for the sticker's three-digit printed number.

- **copy number** is common in early community documentation, reflecting the initial assumption that it might directly number the edition.
- **sticker number** is the safest neutral historical term.
- **chain number** appears in later analytical work.
- **serial** / **serial number** is common in the present research repo.

These are often used interchangeably in discussion, even though the hypothesis “printed sticker number = production/order sequence” is not established.

### three-digit number
Early descriptive phrase for the printed sticker number.

### three symbols
The foreground mark on a sticker. The community consistently recognizes three possible symbols:

- **dot**: `•` or sometimes written `.`
- **dash**: `-`
- **slash**: `/`

### symbol / symb
The foreground mark. The canonical community sticker ledger abbreviates this field as **symb**.

### dot / bullet
Two names for the circular foreground symbol. Early documentation usually says **dot**; some later analysis writes **bullet** or `*`.

### dash
The horizontal foreground mark.

### slash
The diagonal foreground mark. Community analysis also sometimes uses color letters for it; see **G/R/Y** below.

### texture image / image / img
The low-contrast background artwork beneath the foreground symbol.

- Early community documents call these **texture images** or **image textures**.
- The canonical sticker ledger abbreviates the field as **img**.
- Current work often calls this the **background image**, **background class**, or **A–I class**.

### 9 texture images / nine different texture images
The nine repeating background-image pieces, labeled A through I by the community.

### A–I / A to I / image A … image I
Community labels for the nine background-image pieces.

### 9 piece puzzle / nine-piece puzzle / mini-puzzle
The separate background-image assembly problem formed by arranging one example of each A–I image.

### background image
The larger image revealed when the nine texture pieces are arranged correctly. Historical community work identified it as the in-game **printer**.

### printer image / in-game printer
The image depicted by the solved nine-piece background puzzle.

### seal / wrapping seal
Occasional descriptive language for the sticker's physical role on the package.

### black wrapper / black paper wrapping / packet / packaging
Community outreach language for the black wrapping around the PS4 game that the sticker seals. These concrete packaging terms are useful when talking to owners because they locate the sticker without requiring ARG vocabulary.

### code / sticker code / ARG code
Informal community and outreach language for the clue carried by a sticker, especially its printed number and foreground symbol. In technical work, prefer the more precise **sticker number**, **symbol**, and **A–I image class**.

### Huddle
Community name for the fleshy creature/object included in the Collector's Edition. It appears often in owner-hunting discussions because photos of the Huddle can establish that somebody had access to a CE even when the sticker is not visible.

### RealDoll
The company/collaborator associated with production of the unusual Collector's Edition object. **RealDoll** also became a useful search term in historical owner-hunting because collectors and articles often mentioned it even when they did not mention the sticker puzzle.

---

## Cataloguing and acquisition vocabulary

### found sticker / identified sticker / known sticker
A sticker for which the community has enough evidence to identify its number and relevant visible properties.

### lost sticker
A Collector's Edition sticker known or strongly believed to have been discarded, destroyed, misplaced, or otherwise become unavailable for inspection.

### L code / L register
The community's identifier scheme for lost stickers: **L01, L02, …**. These labels identify lost-sticker cases, not physical sticker serials.

### unknown sticker
A Collector's Edition known to exist where the sticker itself, its number, background, or full symbol information has not been recovered.

### U code / U register
The community's identifier scheme for unknown stickers: **U01, U02, …**.

### confirmed lost / probably lost / lost status
Status language used in the sticker ledger when evidence varies in strength.

### owner / owner hunt / owner trail
A person believed to possess or to have possessed a Collector's Edition. Later community work uses **owner hunt** or **owner trail** for attempts to trace these people through social media, resale listings, videos, comments, and old usernames.

### sticker search / new search
Community language for renewed sweeps of Reddit, YouTube, eBay, Twitter/X, Instagram, Facebook groups, Discord history, and other sources looking for owners or sticker images.

### proof sticker / proof-sticker wanted list
Later-community term for a physical sticker whose serial falls on a currently uncertain residue or hypothesis and would therefore provide especially useful confirmation.

### hard residue
Later-community term for a sticker-position class whose symbol prediction remains low-confidence or unstable.

### wanted number / chain number wanted
A sticker serial whose discovery would resolve or test an uncertain position in a repeating model.

### image quality / low-quality image / can't identify
Ledger language for cases where the sticker is visible but the texture image or symbol cannot be read reliably.

---

## Repetition, indexing, and layout vocabulary

### pattern
Generic community word for any repeated relationship between sticker number, background image, or foreground symbol.

### repeating pattern
Used especially for the A–I background cycle and later for the foreground cycle.

### background cycle / 9-state image cycle / period 9
The repeating A–I assignment by sticker number.

Historically, the community's concrete formulation is the repeating A–I pattern:
`001=A, 002=B, ... 009=I, 010=A, ...`

### 108 / 108 entries / 108-cell puzzle / 108-position pattern
Later-community language for the repeating foreground master of 108 positions.

### repeat length / period / cycle length
Names for the number of sticker positions before a pattern repeats.

### residue
Later analytical term for a sticker's position inside a repeating cycle, usually sticker number modulo 108.

### residue class
All physical serials that occupy the same modulo-108 position.

### H108 / 108 master / master 108 / sparse 108 master
Current-project and later-analysis shorthand for the reconstructed 108-position foreground sequence. Historical users more often say **108 entries**, **pattern**, or **grid** than **H108**.

### filled / known cell
A position in the 108 layout whose symbol is known from at least one physical sticker.

### empty / unknown cell
A position in the 108 layout for which the symbol remains unobserved.

### overlap / overlapping records / overlap cell
When two or more different physical sticker numbers map to the same repeating position and can therefore be checked against one another.

### extra record
A second or later physical observation of an already-observed residue.

### collision
Analytical term for two physical serials that map to the same candidate repeat position. Agreement supports the candidate period; disagreement rules it out.

### 12×9 / 12 rows × 9 columns / width 9
The community's standard display of the 108 foreground positions.

### row-major
Later analytical phrase meaning the 108 sequence is written across nine cells, then continues on the next row.

### top 9 rows / top zone / TOP
Later-community term for residues 0–80 in the 12×9 layout.

### bottom 3 rows / bottom zone / BOTTOM
Later-community term for residues 81–107.

### 81+27 / 81 + 27 split
Community/later-analysis observation that the first 81 positions and final 27 positions have different observed symbol vocabularies: the upper region uses slash/dash, while the lower region uses slash/dot.

### zone split
Later shorthand for the same 81/27 distinction.

### sticker 0 / zero phase / phase zero
Language used when aligning the repeating foreground and background cycles so that serial 0 modulo the relevant period defines the origin.

### image numbering
Historical-community phrase for using the known A–I background sequence to help orient or register the 108 foreground arrangement.

### registration
Later/current-project term for aligning one repeating layer or grid with another.

### 3×3 / twelve 3×3 squares / twelve 3×3 frames
Historical Discord geometry describing the 12×9 foreground grid as twelve 3×3 blocks.

### 9 repeating patterns
Historical phrase for the nine physical/image classes or columns participating in the 12×9 arrangement.

### sub-block / block
Generic later language for a local grouping inside the 108 layout.

---

## Community color and symbol shorthand

### G / R / Y
Later-community one-letter classes used in some sticker-analysis tools:

- **G** = slash
- **R** = dash
- **Y** = dot/bullet

These derive from common visualization colors, not from an intrinsic property of the stickers.

### red / grey / yellow
Colors used in community visualizations of the 108 master.

One documented convention is:

- red = dash
- grey = slash
- yellow = dot

Color mappings should always be checked against the particular chart or script because visual tools can differ.

---

## Background-puzzle and registration vocabulary

### arrange / put it together / all 9 pieces together
Early-community language for physically or digitally assembling the A–I texture pieces.

### early attempt
Chronology language for incomplete image assemblies before all nine pieces were known.

### first C / C image
The discovery of the previously missing C-class background tile was historically important because it completed the nine-piece set.

### C with dash
A historically useful C-class sticker whose foreground dash obscured less of the underlying background than previously collected C examples.

### concealed / obscured
Used when the foreground symbol covers part of the printed background code/image.

### acorn / acorn image
A recurring visual clue elsewhere in the INSIDE ARG, especially in cover-art and printer-related discussions. Historical sticker work also refers to arranging rows “like the acorn” when discussing ordering clues.

### side pixels / alternating pixels / dots on either side
Community language for small marks flanking an image or code that were used in earlier ARG puzzles to infer ordering.

### margin bits / check bits
Later analytical labels for those side marks when treating them as ordering or validation information. These are more formal than the historical phrasing.

---

## Historical transform / analysis vocabulary

### rotation / rotate the data
Community attempt to rotate or rearrange the 108 layout in search of hidden pixel art.

### pixel art / hidden image
A hypothesis that the symbol grid might encode a bitmap-like picture.

### Morse / Morse code
Repeatedly attempted interpretation because dots and dashes resemble Morse. The slash complicates a literal Morse reading.

### ternary / three-symbol code
Generic description of interpretations treating dot, dash, and slash as a three-symbol alphabet.

### Braille
A historically attempted geometric/text decoding family.

### LIFEDETECTED
A specific candidate plaintext/string checked in prior verification work.

### printer string
A sequence of dash/dot-like marks emitted by the in-game printer in earlier parts of the ARG.

### printer codes
Broader phrase for printer-generated coded output, including platform-specific strings.

### overlay
A community technique of placing one pattern, text, or image over another to test alignment.

### column shift / Column Shift Tool
Historical transformation that treats lower control cells as shift values used to rotate upper columns of the 12×9 layout.

### shift vector
Later analytical name for a complete set of per-column shifts.

### P1 / P2
Historical labels used in a preserved community combination search. They should be treated as source-local labels unless the exact generating script/document is being discussed.

### Sticker Studio
Name used for a historical community sticker-analysis/generation tool preserved in the archive.

### interval scanner / code interval
Historical-community tooling for testing candidate periodic offsets between known stickers.

### mod 54 / r mod 54
Later-community statistical feature based on residue modulo 54.

### partner voting / zoned / cross-zone
Later prediction-engine language for heuristics that infer unknown residues from related positions.

### leave-one-out
Later analytical validation language for hiding one known value and testing whether a predictor reconstructs it.

---

## ARG-wide terms directly connected to the sticker mystery

### ARG
Alternate reality game. Community documents use this as the umbrella for the INSIDE puzzle trail spanning the game, websites, printer strings, physical editions, social posts, and external files.

### INSIDE ARG
The community's name for the full puzzle ecosystem surrounding Playdead's INSIDE.

### Playdead Unofficial Discord / unofficial Playdead Discord
Primary community venue where much of the puzzle solving, sticker hunting, source sharing, and chronology took place.

### #solving
Historical Discord channel containing much of the general ARG-solving discussion.

### #solving-breakout
A related historical solving channel present in the exported Discord corpus.

### #stickers-solving
Later Discord channel specifically for sticker-puzzle work. Some current archival work still lacks a complete export of this channel.

### terminal41 / terminal41.link / Terminal 41
The ARG website/domain that hosted several puzzle pages and endpoints.

### dat/
Path component used by Terminal41 pages and central to the solved nine-piece sticker background code.

### 534brn9653f9j8mmd
The community's name for the sticker-background-derived Terminal41 puzzle/path and its associated corrupted/obfuscated image data.

### 534brn puzzle / 534 puzzle
Short forms for the above.

### printer
Can mean either:
1. the in-game physical printer whose image appears in the nine-piece background puzzle, or
2. the source of historical printer strings/codes.

Context matters.

### MacOS printer codes
Printer-string set discovered after the macOS release of INSIDE.

### hibernation in progress reboot pending
Solved plaintext extracted from the macOS printer-code puzzle by aligning the coded marks with a referenced E. E. Cummings text.

### breach / breach contribution register
Terminal41 vocabulary appearing in ARG pages and filenames, including `breach_contribution_reg`.

### gate / GATE
Recurring Terminal41/system vocabulary.

### GATE/81
A historical Terminal41 string associated with safety-data material. It is not the same thing as the later sticker 81/27 split, despite the numerical overlap.

### safety data / safety-data
Community/project shorthand for a family of Terminal41 material including preserved strings and page data.

### transmission
Name used for another major ARG artifact/puzzle in external research maps and archives.

### reversible cover / PS4 cover mystery
The iam8bit/PS4 physical-cover puzzle thread, often discussed near the sticker mystery because it shares the same ARG milieu and clue vocabulary.

### 12:12
The time shown on the cover-art clock, historically investigated as a clue.

### printer URL / code URL
Historical idea that the assembled nine-piece image encoded a path or URL.

---

## Source and evidence vocabulary

### sticker ledger / sticker list / canonical sticker corpus
The community-maintained table of found stickers and their properties. The twinysam `INSIDE-ARG/stickers.md` list is the main surviving public ledger.

### research document / Raezores research
Community research notes describing the long-running effort to locate owners and stickers.

### Discord source
A direct link to a historical Discord message used as provenance.

### Puzzle SOLVED / solution
Status language used in public community documentation when a puzzle or sub-puzzle had reached an accepted solution. Keep this separate from proposed interpretations, partial progress, and current-project reconstructions.


### via [username]
Ledger shorthand indicating who found, relayed, or supplied a sticker or lead.

### screenshot / attachment
Primary evidence objects in Discord chronology and sticker reconstruction.

### community master
A reconstructed 108-position symbol sequence assembled from the public sticker corpus.

### same-corpus
Current-project caution meaning that two charts or reconstructions are derived from the same underlying physical sticker observations and should not be counted as independent evidence.

### chronology
Ordered record of when discoveries, sticker finds, hypotheses, and solved puzzle steps occurred.

### provenance
Record of where a claim, sticker image, term, or reconstruction came from.

---

## Production-count vocabulary and cautions

### 500 copies / 1000 copies
Numbers that appear in different generations of community documentation and marketing/assumption history. They should be treated as claims tied to their source/date, not as interchangeable established facts.

### 597
Historically the highest widely catalogued sticker number for a long period and therefore a recurring anchor in production-count discussions.

### 630 / 648
Later inferred possible production ceilings appearing in community analysis.

- **630** appears in a historical Discord inference from the then-known data.
- **648** appears because it is the next multiple of 108 above 597 and was used in some prediction/coupon-collector work.

Neither number should be treated merely from that arithmetic as proof of the number of physical Collector's Editions produced.

### six copies of every residue
A later-community hypothesis that follows if the physical serial range really extended through 648.

### missing 598–648
Later-community phrase for hypothetical high-number serials implied by the 648 model but not physically observed.

---

## Terms that belong primarily to the current reconstruction

These appear frequently in `gamesbyian/GRA-EDISNI`, but they are **not historical community vocabulary unless a source explicitly uses them**. They are listed here so readers do not accidentally attribute them backward.

### foreground / background layers
Useful modern distinction between the three-symbol mark and A–I image carrier.

### carrier
Current-project term for the independently repeating physical/background structure used to orient another layer.

### POS3
Current-project shorthand for a ternary value encoded by the position of an exceptional symbol inside a three-cell group.

### rail
Current-project term for one of those three-cell groups.

### Q3 / Q4
Current-project machine-state labels.

### selector / selector depth
Current-project interpretation of some late 27-cell structure.

### state register / G register
Current-project machine-model terminology.

### gauge / polarity gauge
Current-project terminology for unresolved or physically unobserved orientation choices that do not necessarily alter all model outputs.

### recursive substitution / route shell / terminal 100
Current-project mechanism language derived from the reconstructed machine. These should not be described as terms used by historical community solvers.

### primary / primary region
Current-project name for the 81-cell upper region. Historical/later community sources more often say **top 9 rows**, **top zone**, or simply **first 81**.

### Q4 region / selector region
Current-project names for the final 27 cells. Historical/later community sources more often say **bottom 3 rows**, **bottom zone**, or **last 27**.

---

## Alias map

For quick translation:

| Older / community wording | Later / current wording |
|---|---|
| copy number / sticker number | serial / chain number |
| texture image / img | background image / A–I class |
| three symbols | foreground symbol alphabet |
| 9 piece puzzle | A–I background carrier assembly |
| repeating pattern | period / cycle |
| 108 entries | H108 / 108 master |
| filled cell | observed residue |
| empty cell | unobserved residue |
| overlap | repeated residue / duplicate observation |
| top 9 rows | 81-cell / primary region |
| bottom 3 rows | 27-cell / selector/Q4 region |
| arrange like the acorn | registration/order clue |
| red/grey/yellow | dash/slash/dot visualization |
| lost sticker | L-code case |
| unknown sticker | U-code case |
| sticker list | observation ledger / corpus |
| image numbering | carrier registration |
| 12×9 grid | 108-cell row-major layout |
| twelve 3×3 squares | twelve foreground frames |

---

## Usage recommendations for this repository

When writing historical or provenance-sensitive material:

1. Prefer the wording actually used by the source being described.
2. Put later formal terms in parentheses rather than silently replacing older vocabulary.
3. Do not call a historical Discord solver's “108 entries” an “H108 state machine” unless they actually made the machine claim.
4. Distinguish **dot** from later visualization labels such as **Y** or **bullet**.
5. Distinguish **copy number** as historical wording from any claim that the printed number really encodes manufacturing order.
6. Keep **Lxx/Uxx** identifiers separate from physical serial numbers.
7. Treat **630/648** as model- or source-specific production inferences unless direct physical/manufacturing evidence is cited.
8. Use **community term**, **later-community term**, and **current-project term** when vocabulary itself matters to the argument.

## Principal sources represented

This glossary was assembled from the material currently preserved or indexed by the project, especially:

- the public `twinysam/INSIDE-ARG` README and `stickers.md`;
- historical `Raezores/INSIDE-ARG` fork material;
- the September 2026 Discord-export archaeology and provenance documents;
- preserved Discord tools and handoff artifacts;
- the BigDusty INSIDE ARG map's sticker dossier;
- historical and current sticker ledgers;
- external-source and research-lineage manifests;
- public Game Detectives / Terminal41-era terminology as mirrored or referenced by those sources.

The glossary is intentionally descriptive. A term's inclusion means the community used it or a preserved source used it; it does not mean every associated hypothesis is correct.

# Discord export archaeology

_Date: 2026-09-29_

## Source

A public DiscordChatExporter-style archive is available at:

- upstream: `twinysam/playdead-unofficial-exports`
- working fork: `gamesbyian/playdead-unofficial-exports`
- inspected fork commit: `5e5897e2ce70dad5a2bd85e459770637cb36610f`
- upstream export was created 2026-09-28 and the inspected fork is byte-identical at that head.

The repository is large: about 1.72 GB across 2,699 blobs. It contains 27 HTML exports, 50 text files, 1,793 PNGs, 618 JPGs, additional GIF/video/PDF/archive assets, and several historical scripts/data files.

This is an **external archival source**, not a new physical-sticker sample. Claims extracted from chat remain attributed community statements until independently checked against physical evidence or executable source.

## Exported channels currently present

The root contains paired HTML/text exports for at least:

- `ARG / solving` — channel `461275582970462209`; plaintext export is ~5.1 MB and reports **51,835 messages** through 2026-09-28;
- `ARG / solving-breakout` — channel `463106924708233216`;
- `ARG / tldr` — channel `462637922944811028`;
- `General / inside` — channel `461275526716194818`.

The separate `#stickers-solving` channel is **not** present in the inspected tree. Late `#solving` messages explicitly redirect sticker-specific discussion there, confirming that its absence is a real corpus gap rather than a channel rename. Keep the one-shot bot workflow available specifically to fill that gap if moderators authorize it.

## High-value recovered assets

The export carries many attachments that were previously represented only by expired Discord CDN links. Important examples include:

- `assets/unknown-c89e81cb90765451.png` — blob `91268fd6700f0f8fc01527f51e63f8c2f6cb7e43`; the attachment referenced by Discord attachment ID `690395145094299678` in the 20 Mar 2020 nine-piece sticker-image discussion;
- three generations of the May-2026 community Sticker Studio / random-grid tool:
  - `sticker_random_gen-8a08af05eecf2404.py`
  - `sticker_random_gen-725456418656298f.py`
  - `sticker_random_gen-62dad1a83c441653.py`
- `assets/stickers_csv-c3400f31325053ee.csv` — a six-cycle 1–648 foreground table whose rows encode a 108-period foreground master;
- `assets/sequence_prob-bb1047802f422f07.txt` — the historical repeat-length probability table used in the 108-period discussion;
- `assets/stickers_graph-d76961da71021825.png` — a community technique graph from May 2026;
- `assets/3x36sticker-184db5ca132354d6.png` and `assets/organised_sticker_puzzle-*.jpg` — historical geometry/transposition attempts;
- `assets/StickerSolution-*.png` — screenshots relating to the older terminal/sticker webpage trail;
- printer-code data such as `Master_Morse_36-8899c086fd084e13.txt`, `inside-pc-long-ascii-cdac293e0bbbcf9f.txt`, `macos_printer_codes_corrected-*.txt`, and several raw terminal data files.

Do not copy the whole 1.7 GB archive into this research repository. Preserve commit/path/blob identifiers and import only small evidence needed for a reproducible experiment.

## Immediate provenance upgrade: historical nine-piece attachment recovered

Experiment 302 documented that the March-2020 complete A–I assembly was historically attested but the original pixels could not then be re-read.

The export resolves the first half of that block. The message text around 20 Mar 2020 contains:

`https://media.discordapp.net/attachments/461275582970462209/690395145094299678/unknown.png`

and maps it to the local export asset:

`assets/unknown-c89e81cb90765451.png`.

That image is directly readable from the fork and is therefore no longer a dead-source artifact.

That source-access problem is now fully closed by Experiment 302. The same archived transcript explicitly states the row-major order `I,A,B,C,D,E,F,G,H` in message `673020569905528835`, immediately after the A–I labeling message `673020230200721428`. The discussion also states `A=001`, hence `I=000`, fixing the serial/background phase. The current `IAB/CDE/FGH` carrier is therefore directly historically attested rather than inferred from a modern visual read.

## Historical Sticker Studio

The recovered May-2026 scripts are not new evidence. They encode:

- 108 cells split into an 81-cell slash/dash upper zone and 27-cell slash/dot lower zone;
- mod-54 prediction;
- multi-period voting over 54, 36, 27, 18, 12, 9, 6 and 4;
- weighted zoned and cross-zone guesses;
- “hard residue” targeting and confidence heatmaps.

Experiment 300 already extracted and tested these heuristics by leave-one-out. None beats the zone-majority baseline. Preserve the scripts as historical negative controls and visualization provenance, not as filled sticker observations.

The newest archived version hardcodes 65 known residues and separately labels model-filled cells as guesses. This is useful evidence that the community itself distinguished known observations from predictions.

## Historical period / production evidence

The export strengthens provenance for the 108 cycle but also exposes a common arithmetic trap.

The preserved CSV repeats the same foreground assignment across six 108-long ranges through 648. The historical interval scanner (Experiment 301) explains why 648 appeared: it is the next multiple of 108 after the then-highest serial 597, not an observed production count.

The sequence-probability asset contains a period-length table in which the 108 row reports an expected unique-symbol count around 53.824 and a coincidence probability around `1.9e-8` under that historical calculation. Treat this as historical method provenance; do not import its probability as a calibrated modern p-value without reconstructing its null model.

## Potential late observations requiring verification

The export records several very recent community reports from 27 Sep 2026:

- claimed `•427`, which maps to H108 residue 103 under `427 mod 108 = 103`;
- claimed `•369`, which maps to residue 45.

The discussion itself treats both as unverified, with `•369` specifically regarded as suspicious by one participant. Neither claim should enter `data/observations.csv` unless the original physical sticker is independently confirmed and provenance is captured.

This is especially important because residue 103 is currently a latent-register cell in the preferred machine. A genuine observation there would be highly informative, so confirmation standards should be stricter rather than looser.

## Reversible-cover and UV loose ends narrowed

The export closes some repeated “has anyone tried this?” loops.

For the reversible PS4 cover / CE printed materials:

- **15 Dec 2019:** an owner reports trying blacklight/UV and says nothing obvious appeared on first or second glance.
- **Jan 2020:** owners repeatedly scanned/photographed both sides of the reversible cover. The archive contains several of those images, including `assets/image0-82936663ee93baac.png`; participants explicitly describe the available scan as low quality.
- **2020:** the community also tested scene matching, the 12:12 clock, viewing through the case/plastic, light-angle/translucency ideas, and cover overlays without a conclusive result.
- **Feb 2022:** a participant who says they bought UV lights specifically for testing reports no finding on the sticker/envelope and posts UV photographs (`assets/unknown-56db79e565e6f04c.png`, `assets/unknown-ec3f926e6920d7a3.png`).
- Later 2026 discussion had partially forgotten these tests and again proposed UV/phosphor checks.

This does not prove that every wavelength/material test is exhausted, and the archive still describes the best cover scan as inadequate. It does mean generic “try UV” should be treated as a **historically tested negative**, not an untried priority.

The high-value cover task remains source-quality acquisition and externally registered structural inspection, not repeating generic light/filter experiments.

## User-supplied prior-ARG ordering clue cross-checked against archive

A user-supplied pair of Discord images shows:

- a raw stack of dash/slash printer strings;
- the reconstructed red/blue image whose left and right margins carry a sparse alternating series of red pixels.

The accompanying Discord explanation says those alternating side pixels help determine the order in which the rows should be placed.

The public `#solving` export contains matching historical discussion from 9 Jul 2018. Solvers describe an "alternating interlaced pattern" that limits arrangements, identify the "distribution of margin slashes" as important, note that different row orders change the visible object, and ultimately recover the acorn/41 image. On 11 Jul the `#tldr` channel records the result as a deliberate rearrangement of the PC long strings.

This closes a small but useful design-vocabulary gap: row permutation in a successful historical INSIDE ARG puzzle was not justified only by visual resemblance. Boundary/margin structure helped constrain the ordering.

Implication for current sticker work: preserve and inspect ancillary/boundary information around the physical sticker carrier before treating row/column order as an arbitrary visualization choice. Do not reopen unconstrained H108 permutations; look specifically for an external registration cue.
## Historical community applied the ordering precedent to the sticker foreground

The ordering clue is not only a retrospective analogy supplied in 2026. The archived `#solving` discussion shows the community making the connection while the sticker foreground was still unsolved:

- **26 Jan 2022:** after rendering the 108-chain from sticker 0, a participant calls out a conspicuous empty bottom row. In message `935891168124887100`, another says it may be analogous to the side pixels of the older printer-code puzzle, "kind of a hint to indicate the format/resolution of the message."
- **27 Jan 2022:** message `936157143273443359` explicitly asks whether the first nine rows could be arranged "as same as we did it acorn." A nearby quoted restatement of the boundary-pixel idea is preserved at `936154496030097418`. These were exploratory suggestions, not demonstrated sticker solves.
- **23–24 Dec 2022:** after more rearrangement attempts, a participant summarizes the earlier picture-puzzle precedent as important information living in one mark type while dashes/slashes functioned as a background element "to help us arrange it correctly."

This is valuable anti-hindsight evidence. Long before the present typed-machine interpretation, solvers already regarded **registration marks / boundary regularities / symbol-role separation** as plausible Playdead grammar for this exact sticker foreground. It does not validate any particular modern arrangement, but it lowers the epistemic cost of asking whether one symbol family is structural rather than payload.
## The 81+27 alphabet boundary was noticed years before the machine model

The export contains unusually strong anti-hindsight evidence for the modern primary/selector split:

- **26 Jan 2022:** a solver notes that the 108 rendering can be viewed as an 81-cell slash/dash region followed by 27 slash/dot cells and proposes, speculatively, that the latter might be checksums. The proposed semantics were wrong, but the exact **81+27 structural boundary** was identified from the raw symbols.
- **29 Oct 2023:** in `#solving-breakout`, solvers argue that the puzzle probably needs a visual aid because the earlier Xbox/PC puzzles did, and explicitly call “Why are yellows only at the bottom?” the big question/clue.

The current model's interpretation of those 27 cells as selector frames is much stronger than the historical checksum hypothesis, but the boundary itself did not originate with the current algebra. Treat the historical discussion as provenance for discoverability, not as an independent holdout.
## Frozen May-2026 sticker predictions versus September claims

The export preserves a useful prospective discriminator that should remain quarantined until the physical claims are verified.

On **13 May 2026**, the attached `sticker_random_gen-62dad1a83c441653.py` froze a community heuristic prediction table. In that table:

- residue **103** is predicted `Y` (dot) with confidence `0.854`;
- residue **45** is predicted `G` (slash) with confidence `0.625`.

On **27 Sep 2026**, long after that file was posted, two YouTube commenters were reported in `#solving` as claiming:

- `•427`, which maps to residue `427 mod 108 = 103` and therefore **agrees** with the frozen May prediction;
- `•369`, which maps to residue `369 mod 108 = 45` and therefore **disagrees** with the frozen May prediction.

Neither claim had a confirming sticker photograph in the exported discussion. The community itself explicitly asked for confirmation and expressed skepticism about the 369 claim. Therefore neither may enter `data/observations.csv` or be counted as validation yet.

This pair is valuable precisely because the predictions predate the claims. If either physical sticker is later photographed with provenance, score it against the frozen May artifact before updating any model. Do not tune the current machine using the claimed symbols first.
## Other-channel leads

The late `#solving` export preserves several non-sticker discoveries and loose ends that may matter only if they supply an independently motivated external consumer:

- 2026 recovery of additional information in the historical `transmission_id...` image, including `repo/sys/activate_shutdown` text and an apparent Rick Astley frame;
- a “supersecret” audio asset whose waveform data was converted into an image of Playdead's upcoming game;
- unresolved historical objects repeatedly named by the community: Ford cipher, Rorschach, PS4/Xbox short strings, leftover Xbox Braille, `fsd5t355gf`, Facility 89B/schematic, livestream/Anthony, and gateway-security percentages;
- direct 2026 game-file archaeology distinguishing cut/inactive content from live triggers.

These are valuable inventory items, but the present sticker machine should only revisit one when the external artifact itself supplies a specific structural operation or consumer, following `docs/external-consumer-audit.md`.

## Mining policy

When using this corpus:

1. preserve channel, timestamp, message/attachment IDs where available;
2. distinguish historical claim, attached executable artifact, and independently reproduced result;
3. do not treat repeated chat discussion as independent evidence;
4. do not promote community predictions into sticker observations;
5. prefer exact attachment/blob recovery over screenshots or paraphrases;
6. log negative historical attempts because they are useful anti-hindsight controls;
7. keep `#stickers-solving` explicitly marked as missing until a separate export is obtained.

## Next mining passes

Highest-value remaining work from this archive:

1. systematic attachment-to-message indexing for sticker-specific scripts/images;
2. continue chronology extraction for specific transform families beyond the already-fixed 108 / zero-phase / 9-column / 81+27 milestones;
3. locate additional frozen historical predictions that can be checked against genuinely later physical stickers;
4. continue scanning `solving-breakout`, `tldr`, and `inside` for independently motivated operations or physical/manufacturing clues relevant to the sticker machine;
5. preserve the most important small text/code assets by content hash and source path, without vendoring the full export.

Completed during this pass: the March-2020 carrier-orientation gap is closed, and the 2018 PC-code edge-ordering provenance now has exact Discord message IDs.


## First-party cover clue recovered

The archive preserves an embedded iam8bit tweet, ID `1203007268930764800`, describing the standalone physical edition as including an exclusive poster and a reversible slip cover with a **hidden clue**, and saying that this version is the one included with the Collector's Edition.

This upgrades the cover lane materially. It is no longer based only on community belief or generic CE completeness: the publisher/vendor explicitly advertised a hidden clue on that artifact.

The export also carries larger cover assets than the previously discussed low-quality scans:

- `assets/INSIDE_A-5d197786f158c567.JPG` — blob `875403acac93d83a8acae97e14240c35b88d33ab`;
- `assets/INSIDE_B-80fbff1237c37913.JPG` — blob `d533d4161f0572b65d134d54f4fa6477029f2d64`;
- `assets/Cover_blend-dfb43cdd555596a7.jpg` and `assets/Cover_blend_mirrored-c2fb3d0f85f5b014.jpg` preserve historical overlay/mirroring attempts.

Action: run a bounded structural re-audit directly on the best archived A/B source images before asking owners for new scans. Preserve the historical failed overlay/UV work as negative controls.

## Stickers-solving channel creation provenance

The missing `#stickers-solving` export is now historically explained rather than merely observed as absent.

In the archived `ARG / solving` text, on **22 Sep 2026 at 19:12**, santiface posts a pinned message:

> "to better organize the solving efforts I made two new channels: #sticker-hunting ... and #stickers-solving"

Later `#solving` messages on 25 and 28 Sep explicitly redirect sticker work into `#stickers-solving`.

Therefore:

- `#stickers-solving` is a genuinely separate channel, not a rename of `#solving`;
- it was created only six days before the export repository's 28 Sep cutoff;
- the public export appears to have captured the long-lived legacy channels but not these newly split sticker channels;
- the authorized one-shot bot remains useful specifically for this late-created gap.

This also means that essentially all sticker work before 22 Sep 2026 should still be recoverable from the exported `#solving` / `#solving-breakout` corpus.

## Strong historical precursor to the modern 81+27 / selector interpretation

A particularly important `#solving-breakout` message predates the present machine model.

On **22 May 2026 at 16:32**, lime8159, discussing a 9x12 sticker orientation, proposes that:

- the **first 9 bits** could encode one number / larger domain;
- the **last 3 bits** could encode a second number / smaller subset.

This is not the present machine and should not be retrofitted as one. But it is unusually close in *structural vocabulary* to the modern decomposition of each 12-cell stripe into a 9-cell primary region plus a 3-cell selector region. Together with the January-2022 observation of an 81-cell slash/dash zone followed by a 27-cell slash/dot zone, it is strong anti-hindsight evidence that the raw corpus itself suggested hierarchical 9+3 structure to independent solvers.

Action: treat 9+3 hierarchical decomposition as historically discoverable from the carrier, while keeping the exact POS3 / selector semantics derived from the modern executable model.

## Late 534brn/JPEG forensic recovery lane

The 2025–2026 archive contains a more advanced forensic lane than the older "JPG is irrecoverable" summary suggests.

Key points:

- **20 Dec 2025:** a solver identifies ordinary JPEG structures in the damaged payload, including EXIF/TIFF metadata, Huffman tables and quantization tables, and argues parts of the header can be reconstructed.
- **18 Mar 2026:** a solver explicitly questions whether the UTF-8 replacement corruption happened server-side or during scraping/saving.
- **14 Jul 2026:** eropkol identifies a better historical capture linked from an April-2020 Discord message, claiming it avoids some HTML-parser damage but lacks the beginning/end.
- **21 Jul–2 Aug 2026:** the group reconstructs substantial header/EXIF structure, identifies the file as grayscale JPEG-like data, and preserves a cleaner text capture as `assets/message-630970294e9fb0ce.txt`.
- **18 Aug 2026:** the original discoverer reports that only two people saw the page before the terminal shutdown and that the surviving copy may have been captured through a Chromebook, leaving the corruption provenance genuinely ambiguous.

This does **not** establish recoverability of the missing image payload; the archive still records expert and community assessments that too much entropy is missing for normal JPEG recovery. It does, however, mean the old "server-side corruption, nothing more can be done" statement is too strong.

High-value bounded follow-up: compare every preserved 534brn capture byte-for-byte, reconstruct only deterministic JPEG/EXIF fields, and quantify exactly which bytes are information-theoretically lost versus merely transformed by ANSI/UTF-8/HTML handling. Do not use guessed image content as evidence.

## 534brn capture inventory is now explicit

The preserved damaged-image material is no longer represented only by prose references. See `data/discord-534brn-captures.json` for a content-addressed inventory of every currently identified 534brn capture family and derived artifact in the export.

Notable deduplication findings:

- three differently named "original" HTML files are byte-identical at blob `ce55c03e...`;
- four `534brn..._1` HTML names are byte-identical at `f12c02c4...`;
- three later `message-*.txt` names are byte-identical at `9580913d...`;
- the historical `534brn...png` and both `StickerSolution` names are the same blob `2d9fd5b6...`;
- a BMP and two JPG filenames are all the same 3.96 MB blob `21649d1b...`, so historical filename extensions cannot be trusted as format evidence.

The later partial capture `9580913d...` is especially useful: even through the connector's lossy text view it visibly contains standard JPEG Huffman-table strings and ends with literal `pe^!02un`. Its archived provenance says it omits the beginning/end but avoided some HTML-parser damage. The next experiment must operate on raw bytes, not Unicode-decoded text.

## Frozen May-2026 table versus the current canonical corpus

A direct cross-check closes an easy-to-misstate prospective-validation question.

The current canonical `data/observations.csv` contains **82 physical sticker observations but only 65 distinct H108 residues**. After mapping canonical residue 108 to the Sticker Studio's zero-indexed residue 0, those 65 residue positions are exactly the 65 entries hard-coded in the archived May-2026 `KNOWN` table.

Therefore no provenance-backed physical observation currently in the canonical corpus supplies a genuinely new residue against which the May prediction table can be scored prospectively. The additional rows are repeat-cycle confirmations of already-known residues.

The Sep-2026 text reports for residues 103 and 45 remain interesting precisely because both positions were outside that frozen 65-residue set, but neither belongs in `observations.csv` until a photograph or equivalent provenance is recovered.

Consequence: do not quote retrospective performance of the May predictor on the current 82-row corpus as prospective validation. The only presently available out-of-freeze tests are the quarantined later claims.

## Additional terminal/gateway artifact archaeology

A second pass over the small text/code attachments recovered several exact historical implementation details that are worth preserving because they constrain what kinds of “external consumer” Playdead actually used elsewhere.

### Printer endpoint was an active server-side input consumer

`assets/print-b58746938d8d0071.txt` (blob `87e11d4878bc4fd0a3db204f820820d3dcabc45d`) is client-side JavaScript for the historical printer page. It does not decode input locally. Instead it:

1. reads the submitted string;
2. POSTs `{ in: <input>, id: <local GUID>, check: 'true' }` to `/print/index.php`;
3. on acceptance, POSTs the same input and GUID again without `check:true`;
4. inserts the server response into the printed page.

Failed and empty submissions render explicit “incorrect message received” / “no message received” printer text.

This is concrete historical precedent for a Playdead ARG endpoint acting as a **server-side validator/consumer of a compact prior-stage answer**, rather than every stage being self-decoding plaintext. It does not identify a surviving endpoint for the sticker terminal `100`, but it is a materially relevant design-vocabulary fact for `docs/external-consumer-audit.md`.

### Gateway email explicitly demanded an authentication input

`assets/Gateway_status_report.eml_redacted-2f6dcc6739e9117b.txt` (blob `d1bfa40a2fcc8f46cea7d5be0b99e6d8046412ed`) preserves a June-2018 “Gateway status report.” Decoding the visible binary yields labels including:

- `gateway: playdead.com`;
- `gateway auth.:_______`;
- `___required//////////`;
- a second gateway-auth line ending in `rejected///////`;
- `rejection reason:____`;
- `_comms handle input//`.

The email also embeds a JPEG attachment whose metadata names **Andreas Normand Grøntved** as creator. Preserve this as first-party/provenance context for the old gateway artifact, not as evidence about the Collector's Edition sticker mechanism itself.

Together with the printer JavaScript, this strengthens a narrow historical statement: Playdead's ARG infrastructure sometimes expected an externally obtained answer to be submitted to an active consumer that returned success/failure state.

### Safety-data strings recovered at exact source paths

`assets/INSIDE_saf_dat_col_interesting-50a465eb636416ab.txt` (blob `31f744647c40c6431b3ebd9de9aac0392eefd049`) preserves readable islands extracted from the historical Terminal 41 safety-data page, including:

- `repo/dat/breach_contribution_reg`;
- `fsd5t355gf`;
- `GATE/81/connect[chk]` with `chk stat. [FAIL[1]]`.

These strings were already known in community lore, but the export supplies a durable content-addressed source rather than a paraphrase. They remain unresolved external artifacts. Do not use them as generic keys against `100` without a cue supplied by the artifact itself.

### Historical geometric straightening attempt is reproducible

`assets/saf_straightened_band.setup-e3c0718ba65d9561.json` (blob `e39e4962701576f83254047b613ab1b7848bce4d`) is a `saf-byte-workbench` setup containing hundreds of explicit per-position shift points and `shiftFill: "wrap"`. It records a substantial community attempt to geometrically straighten/re-register a band in the safety-data carrier.

Treat unconstrained “try shifting/straightening the Terminal 41 data” as historically attempted territory. A future revisit should need a specific registration clue or a reproducible objective, not visual fishing.

### Embedded image metadata

`assets/jpeg-cbebfe04a2674523.txt` (blob `590624925fe3d36a362bbb1de905f459267c211b`) records JPEG metadata with Artist/XPAuthor `AnSet`, EXIF original/digitized time `2016:08:09 14:12:24`, and an XMP create date in December 2016. This is provenance metadata only; no sticker-machine consequence is inferred.

## Stateful printer-answer consumer recovered

The compact `ARG / tldr` export adds an implementation-level behavioral clue to the archived `print.js` recovered above.

On **2 Jul 2018**, after `MULTIPLEPROBESDISPATCHED` had been accepted by the Playdead printer endpoint, solvers reported that submitting a later *incorrect* code in the same browser still appended the previously unlocked successful page after the normal “incorrect message received” output. The same correct submission was reported to trigger the appearance of `printreqstatus_005.html` and shortly afterward `printreqstatus_006.html`.

Combined with the archived JavaScript's persistent browser GUID sent to `/print/index.php`, the historical consumer appears to have maintained **per-client progression/state**, rather than treating every answer as a stateless lookup.

This is relevant design precedent for any genuine external consumer of the Collector's Edition machine: an answer may act as a state transition or unlock token, not merely decode to prose. It does not identify a surviving consumer for `100`, and the old endpoint must not be probed without an independently justified grammar.

## Historical empty-window clue sharpened to residues 99–107

The archive makes the old “empty bottom row” observation more precise.

On **6 Jan 2024**, a solver explains that the conspicuous nine-cell black block in the community rendering corresponds to having found **no stickers numbered 99 through 107 modulo 108**. They explicitly say the community suspected that this absence might help solvers recognize the 108-period structure.

This is not evidence that those residues were never manufactured: discovery is heavily biased and later observations can fill historical gaps. Its value is human-solve provenance. Before the present machine model, solvers were already treating a **nine-cell contiguous absence at the end of the 108 carrier** as potentially intentional registration information rather than merely missing data.

Keep this separate from the current Q4 interpretation. It supports discoverability of the 9-cell framing clue, not the machine semantics derived later.

## Public Google Docs recover the original puzzle rationale

The Discord URL inventory led to several still-readable historical Google Docs. These are stronger than later chat recollection because they preserve the working notes produced while the original printer ARG was active.

### \`INSIDE PRINTER SECRET\`

Public document ID: \`1vlpah0LdCRpJe-OfhnkaiBIcmepGXust5BMbaFJGGt8\`.

The document states explicitly that rearranging the 32 long PC printer strings into a specific order reveals the acorn/41 image, and records the then-leading hypothesis that:

- the **dots** carry the encoded message;
- the **acorn shape serves as a method of preserving the correct order of the strings**.

That is unusually direct historical support for the registration interpretation behind the later Discord “margin/check-bit” explanations. In a solved Playdead puzzle, geometry could be the ordering scaffold while a secondary symbol layer carried the payload.

The same document records analogous multi-stage consumers on other platforms: Xbox geometry → Braille → password; iOS time-of-day ordering → 5×5 glyphs → password; Switch controller actions → RGB codes. Each accepted password/code then caused Playdead/Terminal41 state to advance.

### \`terminal41.link journal\`

Public document ID: \`1V9TsI8D-NG191aNplbQxnteboUc_TYl0IViFtkwDKWA\`.

This contemporaneous journal is useful because it separates **scheduled/server-side site changes** from changes solvers could confidently attribute to submitted answers. In late June 2018, multiple Terminal41 pages changed around platform-release dates even though the author says the community was unaware of doing anything to trigger them. The journal explicitly warns that early \`printreqstatus\`/breachlog changes may therefore have been time/release driven.

This qualifies the “active consumer” precedent:

- the archived printer JavaScript and later accepted-answer behavior demonstrate genuine submitted-input handling;
- not every Terminal41 page transition was necessarily caused by solver input;
- historical endpoint chronology must distinguish **time/platform-release gates** from **answer-triggered unlocks**.

That distinction should carry into any search for a modern consumer of terminal \`100\`: server state changes alone do not prove causation by a submitted token.

## Historical sticker-ledger drift audit: 597 discrepancy resolved

The recovered legacy Google Doc \`Inside Collector's Edition Numbers\` records sticker **597** as:

\`/597 · image C · iam8bit YouTube\`

while canonical \`data/observations.csv\` records:

\`597 · - · image C\`

This initially looked like source drift worth quarantining. Git history resolves it cleanly.

On **10 Oct 2021**, upstream \`twinysam/INSIDE-ARG\` commit \`5f1fa6f8db746519d9e83f524a2eb54baeb2aab6\`, titled **“Fixing two mistakes of symbol descriptions (306 • and 597 -)”**, explicitly changes the sticker-ledger entry for 597 from slash to dash and 306 from dash to dot. The current upstream ledger and our canonical observations agree with those corrections.

Therefore:

- **do not change canonical 597**; dash is the later explicit correction;
- treat the old Google Doc as a valuable historical snapshot, not automatically authoritative over later source corrections;
- provenance mining must compare recovered snapshots against subsequent Git history before promoting discrepancies;
- the same audit confirms canonical **306 = dot** is also a deliberate later correction.

This is a useful example of why frozen historical documents are excellent for chronology but can preserve superseded transcription errors.


### Exact ordering anchors recovered from the archive

The public \`#solving\` export contains matching historical discussion from 9 Jul 2018 with exact anchors. Message \`465922647662788609\` describes an "alternating interlaced pattern" that limits arrangements; \`465923442374344707\` calls the "distribution of margin slashes" a key feature; \`466023354214776832\` says the left/right patterns form six boundary patterns; \`466032381518807070\` says "The sides are the only thing that made this possible"; and \`466036574128439301\` explicitly calls the side marks "check-bits" used to line things up. Solvers change line order while trying to recover the image and ultimately recover the acorn/41 image. On 11 Jul the \`#tldr\` channel records the result as a deliberate rearrangement of the PC long strings.

On **27 Jan 2022**, message \`936157143273443359\` explicitly asks whether the first nine rows could be arranged "as same as we did it acorn." A nearby restatement of the boundary-pixel idea is preserved at \`936154496030097418\`. These were exploratory suggestions, not demonstrated sticker solves.

These anchors strengthen the historical claim narrowly: boundary structure and the earlier acorn ordering method were both available to sticker solvers before the present machine reconstruction.


## Live historical Google Drive sources recovered

The full URL-context extraction recovered a still-live public Google Drive folder that was posted repeatedly during the active printer investigation:

\`https://drive.google.com/drive/folders/1-381gKXFGrEi-JdQBSL9MvcxDEbayVAi\`

Exact Discord chronology:

- 30 Jun 2018 11:50 — \`dodo0303\` posts a direct file link for \`IMG_2327.TRIM.MOV\`;
- 30 Jun 2018 12:54 — \`dodo0303\` posts the containing Drive folder;
- 30 Jun 2018 15:04 — the folder is reposted in \`#solving\`;
- 1 Jul 2018 18:58 — \`dodo0303\` posts it again;
- 1 Jul 2018 19:33 — \`pitch_bright\` posts the folder in \`#solving-breakout\`.

The live folder currently exposes a sequence of original MOV/MP4 gameplay recordings created on 30 Jun–1 Jul 2018. The surviving inventory includes phone captures named \`IMG_2327.TRIM.MOV\` through \`IMG_2414.TRIM.MOV\` plus two screen recordings. This is a higher-provenance source for historical printer output than later re-encoded YouTube compilations.

One source file was acquired exactly for validation:

- Drive file ID: \`1_Zbz01f9WuAQxZ-YyfpeDqIsHNBqeKlS\`
- title: \`IMG_2327.TRIM.MOV\`
- Drive size: 15,725,021 bytes
- created: 2018-06-30T14:41:21.228Z
- modified: 2018-06-30T14:50:18.755Z
- SHA-256: \`c3e165617b0a9716e385dde4d2835bfd6963f3fd6c4dba1c6cf3054c4efe0d8a\`
- media: H.264 886×1920 at 60 fps with AAC audio, duration 43.873 s.

A visual spot-check confirms it is an INSIDE gameplay recording from the printer investigation, not an unrelated file.

Several individually linked 1 Jul 2018 iOS recordings are now dead at Drive while their historical Discord embeds survive. For example, \`1tmxJdJVtSyxys3DIR5BfhetdlMNPd3sk\` was embedded as “Inside iOS printer code.mp4” recorded at 12:30 PM but now returns 404. This makes acquisition of the still-live folder worthwhile as preservation, not merely convenience.

Do not vendor the video corpus into this repository. The external-evidence acquisition lane in PRs #56/#57 has been notified so immutable originals, hashes, and provenance can be preserved outside normal Git history.

## 2026 audio-asset dump exposes a literal \`superSecret/image\` source path

The URL ledger also recovered the public Drive folder shared on 27 Mar 2026 when \`probablynotbeard\` published INSIDE audio assets with recovered context names and paths:

\`https://drive.google.com/drive/folders/1mitP9wjW0HS1vSUWig5vO2fZlMyd1ie9\`

The Discord message explicitly says that these context names allowed \`@ghaith\` to discover one file stored in a folder called \`supersecret\`.

The live Drive hierarchy confirms this independently:

\`andreas/superSecret/image (Game2#6585 (681347534)).wav\`

The \`superSecret\` folder contains exactly that one WAV in the current public dump.

Exact file properties:

- Drive file ID: \`1GlBTcDQoYpEKQdVVjHw4iiBsc8Vk3C7K\`
- size: 1,376,204 bytes
- modified source timestamp: 2026-03-27T04:40:49Z in the Drive dump
- SHA-256: \`2392baa9dd6261e6a9711e42379c0d412f623ee9269cb8b4094045ed2d0ef335\`
- format: mono PCM signed 16-bit little-endian, 48 kHz
- duration: 14.335 s.

A first bounded signal audit found no obvious spectrogram text/image payload. The filename/path therefore remains interesting provenance, but “image” should not be promoted to a hidden-picture claim without an independent decoding cue.

The next archival question is exact source-code/event provenance for \`Game2#6585 (681347534)\` and what in-game object/action triggers this sound. The targeted Discord clue-context extractor now searches for the asset name, \`superSecret\`, \`SecretProbeFlicker\`, input 22, and morse-terminal discussion.


A first spectrogram audit shows no obvious text/image payload, which is consistent with the historical solve: the image is encoded directly in the **raw PCM sample values**, not as a spectrogram.

The expanded Discord window recovers the complete 27 Mar 2026 solution chronology. At 13:23, \`darkmatter_11\` recognizes that waveform values can be grouped as RGB triplets. At 13:42 they report the corrected dimensions as **610×376**; at 13:55 they say they took the waveform as values between -1 and 1 and made an RGB image in Mathematica. The solved image attachment is preserved as \`assets/image_wav-4eb8725b7ff41261.png\`, exactly 610×376.

The structure is independently reproducible from the archived WAV:

\`688,080 samples = 610 × 376 × 3\`

with zero remainder. Direct RGB reconstruction from the sample stream yields coherent Project 3 concept art, turning the dimensional factorization into a strong structural certificate rather than a visual guess. A deterministic verifier in the export-analysis repo is comparing candidate normalization conventions against the exact Discord solve PNG.

The same discussion records two provenance constraints:

- a 2018 GOG build reportedly still contains the asset;
- on 31 Mar 2026, \`ghaith2025\` reports the image audio is present in launch-day PS4 files compiled before release.

Those remain community reports until independently reproduced from dated builds, but they make a Collector's-Edition-only origin unlikely. The next high-value question is exact Wwise/source-code/event provenance for \`Game2#6585 (681347534)\` and whether any in-game object or event references it.

The March discussion also tested several other suspicious WAVs and concluded they were likely Wwise convolution impulse responses rather than image carriers. This is a useful negative control: filename/path plus waveform oddity is insufficient; the exact sample-count/image reconstruction is what distinguishes the genuine \`superSecret/image\` file.

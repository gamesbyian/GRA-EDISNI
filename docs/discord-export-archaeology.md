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

- **26 Jan 2022:** after rendering the 108-chain from sticker 0, a participant calls out a conspicuous empty bottom row. Another says it may be analogous to the side pixels of the older Xbox code, "kind of a hint to indicate the format/resolution of the message."
- **27 Jan 2022:** a participant explicitly asks whether the first nine rows could be arranged "as same as we did it acorn." The idea is exploratory and was not a demonstrated solve.
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

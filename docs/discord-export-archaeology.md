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

**Caution:** do not silently rewrite the project's registered `IAB/CDE/FGH` carrier from a visual glance at this screenshot. The screenshot visibly carries A–I annotations, but Experiment 302's remaining question is an exact mapping between historical tile labels, image assembly, serial phase, and the project's registered carrier convention. That comparison should be made explicitly before changing any machine coordinate statement.

Action: update Experiment 302 from “pixels unavailable” to “source pixels recovered; exact orientation reconciliation pending/available for direct audit.”

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

1. exact orientation reconciliation using the recovered March-2020 A–I attachment;
2. systematic attachment-to-message indexing for sticker-specific scripts/images;
3. chronology extraction for when 108, zero phase, 9-column rendering, 81/27 zoning, and specific transform families first appeared;
4. locate frozen historical predictions that can be checked against genuinely later physical stickers;
5. scan `solving-breakout`, `tldr`, and `inside` for independently motivated operations or physical/manufacturing clues relevant to the sticker machine;
6. preserve the most important small text/code assets by content hash and source path, without vendoring the full export.

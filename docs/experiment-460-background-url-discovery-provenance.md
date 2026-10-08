# Experiment 460 — how the nine-tile CE background URL was actually identified

_Date: 8 October 2026. Research type: historical discovery-channel provenance audit and fixed-string comparison. No new sticker symbols inferred._

## Question

**Was the background mosaic's `dat/534brn9653f9j8mmd` address completely decoded from the nine sticker pictures and then independently checked? Or did an external website listing supply the previously unreadable final characters?**

That distinction matters for the [evidence graph](concept-map-crosslink-leverage-2026-10-08.md). The CE **background** does identify a real ARG endpoint. But “independently blind-decoded endpoint” and “partially decoded clue recognized after source enumeration” are not the same relationship, and neither by itself supplies a decoder for the separate slash/dash/dot **foreground**.

## Original-source witness and times

The strongest witness is now **the original channel's public [Discord text export](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/Playdead%20Unofficial%20-%20ARG%20-%20solving%20%5B461275582970462209%5D.txt)**, Git blob `1889cc948f86f5a4455de0d7310b15cdb1b88b5c`. It retains the apparent participants, timestamps and messages in the original conversation. The [canonical community README](https://github.com/twinysam/INSIDE-ARG/blob/master/readme.md) provides a second, retrospectively expanded account. The archive export's timezone is not documented and the Discord API was not independently queried; the two source types are therefore *corroborative*, not separate independent observations.

| Source event | Source identity | What it proves and does not |
|---|---|---|
| March 20, 2020 | [Discord message 690408214470328390](https://discord.com/channels/460626942190813184/461275582970462209/690408214470328390), linked from community history | Candidate URL already being read from the nine-piece mosaic; reconstructed string has four disagreements from later-known path |
| April 6, 2020 | [Discord messages 696749987991650315 and 696860529813094420](https://discord.com/channels/460626942190813184/461275582970462209/696860529813094420) | New C sticker improved lettering, per source-linked history; **this does not timestamp either later candidate string** |
| **April 21, 2020** | [Discord message 702030280751317072](https://discord.com/channels/460626942190813184/461275582970462209/702030280751317072) and pinned Discord export | **Direct archived first-person message** posts the exact URL, then says the paths were found by browsing site indexes. A solver immediately identifies it as the CE background code. This discovery channel is no longer merely a retrospective claim |
| April 28–29, 2020 | [Pinned original Discord export](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/Playdead%20Unofficial%20-%20ARG%20-%20solving%20%5B461275582970462209%5D.txt) | A solver directly admits the path was **not fully decoded from the artwork**. Their closest remembered full-string reading is `dat/534brn9653f9i8rnd` (**18/21**). They independently count exactly three wrong characters. |
| Prior project document | [README commit 386d4f82, April 21 00:54 UTC](https://github.com/twinysam/INSIDE-ARG/blob/386d4f82c89829e8af82dfd5b9fd90c5f0e36ac9/readme.md) | The exact `534brn...` URL was **not** yet present in this pinned README. This establishes absence from that documentation, **not** nonexistence of the URL or anyone's knowledge of it |
| Subsequent project document | [README commit aefbe285, April 23 05:44 UTC](https://github.com/twinysam/INSIDE-ARG/blob/aefbe285c4df7324dad6e6998ab0a24ea24da49c/readme.md) | Explicitly names the later-known exact URL as the nine-texture puzzle solution |

**Independent timing cross-check:** Discord's message identifiers encode creation times. The March-20 link decodes to **2020-03-20 03:55:45 UTC**; the April-6 evidence message to **2020-04-06 23:14:57 UTC**; and the April-21 website-index message to **2020-04-21 05:37:42 UTC**, between the two pinned Git commits. A message ID establishes the *timestamp of the linked message*, **not independent authentication of its content**. The separately preserved 5 MB channel export now recovers the apparent original message bodies, including the website searcher's April-21 first-hand statement and the April-28 solver admission. Exported wall-clock times and Discord snowflake UTC timestamps should not be equated without the export timezone. Direct live Discord authentication remains outstanding.

## Fixed character comparison

All strings are **21 ASCII characters** long, `dat/` prefix included. We counted exact positional mismatches, with the Levenshtein distance independently agreeing because no edit insertion or deletion is beneficial.

| Historically reported stage | Candidate reading | Exact matches | Mismatches |
|---|---|---:|---:|
| March 20 candidate | `uat/5345rn9653f9i8nmd` | **17/21** | **4** |
| Retrospectively remembered pre-index candidate A (first-person April 28) | `dat/534brn9653f9i8rnd` | **18/21** | **3** |
| Retrospective pre-index candidate B (README only; original message not located) | `dat/534brn9653f9i8nmd` | **19/21** | **2** |
| Externally listed endpoint, April 21 | `dat/534brn9653f9j8mmd` | **21/21** | **0** |

The **best directly preserved first-person pre-index candidate** is **18/21**, not 19/21: its three unresolved positions are **17** (`i` versus `j`), **19** (`r` versus `m`) and **20** (`n` versus `m`). The stronger **19/21** alternative appears in the later community README, but an exact original pre-index message containing that literal string was **not found in the available export**. This is a useful distinction between first-hand recollection and later retrospective candidate indexing. Neither case is a complete blind decode; both provide substantial partial artwork evidence that the genuine listed path matched a physically assembled clue.

The auditable data are in [`data/experiment-460-background-url-discovery.json`](../data/experiment-460-background-url-discovery.json); the offline exact comparison and timestamp verifier is [`scripts/audit_2020_background_url_discovery.py`](../scripts/audit_2020_background_url_discovery.py):

```sh
python scripts/audit_2020_background_url_discovery.py
```

The verifier optionally accepts separately obtained pinned upstream README source files via `--before` and `--after`, **and the 5 MB original exported chat** via `--export`, checking its exact Git blob SHA and eight bounded message/event strings. Its default offline fixture reproduces the frozen claims, not a live Discord or original website backend reconstruction.

## Important limitation: what “site index” means

The saved [`terminal41.link/index.html`](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/index.html) is simply a meta refresh to `loadSys/`; it is **not** an archival copy of the actual directory/server index reportedly examined on April 21. Thus we now have strong **contemporaneous first-person archived discovery-channel provenance**; however, the original website index listing bytes and actual server logs remain unavailable. The export says the path appeared among recent index entries, but this alone does not date when the underlying server content was created.

We can nevertheless distinguish three statements that should **not** collapse into one row:

1. **Physical:** the nine sticker artwork classes assemble into a coherent background, with a strong *partially readable* string. This is genuine evidence.
2. **Discovery:** the community account says the exact candidate path became known by *website index enumeration* and was matched retrospectively to that background. The pinned Git before/after versions are consistent with this chronology.
3. **Intended authorial connection:** because the mosaic strongly resembles an active path, it is reasonable to treat the address as the intended destination of the *background*. **Neither the address's exact characters nor the foreground's decoding operation were established as completely blind, independently forced output**. This does **not** suggest the background is fake, incidental or unsolved in ordinary ARG terms.

## Implications for current sticker theories

**Discovery-channel exposure can turn a partially readable code into an apparently complete decode without an independent blind reading of every character.** The original CE background is an historical positive case for *answer-assisted recognition*. Future proposed sticker results should declare whether the output was fixed **before** opening/searching the candidate source. Otherwise a discovered page/code/URL may have guided symbol interpretations, orientation, OCR, or registration.

There is **independent firsthand historical separation of the foreground and background puzzles**: in the same original 29 April 2020 conversation, a solver explicitly distinguishes the now-solved nine-piece artwork from the still-uninterpreted **three foreground symbols** and what they might unlock. This is a contemporary boundary, not a retrospective distinction invented by our current research. It strongly cautions against letting the known background→URL association automatically dictate the foreground's purpose.

This is especially important for the current open bridges:

- **`534brn` as a foreground consumer:** the background identifies that page, but its discovery does **not** license using the nine URL digits, JPEG damage, 128 footer, 22-character SAF field or another observed feature as a sticker key. Those still require an independently provided mapping.
- **Original-game SecretMap and reversible cover:** a post hoc match of a cube/word/bitmap to an already inspected picture needs source-fixed scale, orientation, transform and rejection controls. The recovered historical example does not automatically license image matching.
- **Future original-source discovery:** original pre-/post-discovery versions of website archives are highly useful, but an output may need to be fixed before using an archive to prevent the same circularity.

The general [research map](concept-map-crosslink-leverage-2026-10-08.md) calls this the difference between a **source-anchored destination** and an **independently source-licensed operation**. The background securely provides the first, not the latter for its *separate* foreground.

## Reopening criteria

1. Exact authenticated March–April 2020 Discord messages or full historical image exports showing a 21/21 path reading before the April-21 website-index discovery would **revise** the claim that a full blind decode is undocumented.
2. The actual archived April-21 directory listing or server files would clarify precisely what “index” was and how complete the alternative list was.
3. A previously published document fixing the foreground-to-background operation before the exact URL was known would add a genuine missing bridge; none was recovered here.

**Result:** Provenance supports **partial physical decode → externally discovered URL → immediate retrospective match**, not a documented 21-character blind readout. This is a change in **evidence-classification precision**, not a new solution or a rejection of the Collector's Edition sticker mystery.

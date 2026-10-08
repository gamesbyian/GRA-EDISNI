# Experiment 460 — how the nine-tile CE background URL was actually identified

_Date: 8 October 2026. Research type: historical discovery-channel provenance audit and fixed-string comparison. No new sticker symbols inferred._

## Question

**Was the background mosaic's `dat/534brn9653f9j8mmd` address completely decoded from the nine sticker pictures and then independently checked? Or did an external website listing supply the previously unreadable final characters?**

That distinction matters for the [evidence graph](concept-map-crosslink-leverage-2026-10-08.md). The CE **background** does identify a real ARG endpoint. But “independently blind-decoded endpoint” and “partially decoded clue recognized after source enumeration” are not the same relationship, and neither by itself supplies a decoder for the separate slash/dash/dot **foreground**.

## Original-source witness and times

The [canonical community README](https://github.com/twinysam/INSIDE-ARG/blob/master/readme.md) describes the following chronology (reported contemporaneously in 2020 but its expanded narrative is retrospective).

| Source event | Source identity | What it proves and does not |
|---|---|---|
| March 20, 2020 | [Discord message 690408214470328390](https://discord.com/channels/460626942190813184/461275582970462209/690408214470328390), linked from community history | Candidate URL already being read from the nine-piece mosaic; reconstructed string has four disagreements from later-known path |
| April 6, 2020 | [Discord messages 696749987991650315 and 696860529813094420](https://discord.com/channels/460626942190813184/461275582970462209/696860529813094420) | New C sticker improved lettering; later README records two partial alternatives, three or two disagreements with final URL |
| **April 21, 2020** | [Discord message 702030280751317072](https://discord.com/channels/460626942190813184/461275582970462209/702030280751317072) | Community README specifically reports a newcomer inspecting the *Terminal41 site index* and **discovering four paths**, including the exact `dat/534brn9653f9j8mmd/`. The candidate was then **recognized** as matching the previously assembled tile mosaic |
| Prior project document | [README commit 386d4f82, April 21 00:54 UTC](https://github.com/twinysam/INSIDE-ARG/blob/386d4f82c89829e8af82dfd5b9fd90c5f0e36ac9/readme.md) | The exact `534brn...` URL was **not** yet present in this pinned README. This establishes absence from that documentation, **not** nonexistence of the URL or anyone's knowledge of it |
| Subsequent project document | [README commit aefbe285, April 23 05:44 UTC](https://github.com/twinysam/INSIDE-ARG/blob/aefbe285c4df7324dad6e6998ab0a24ea24da49c/readme.md) | Explicitly names the later-known exact URL as the nine-texture puzzle solution |

**Independent timing cross-check:** Discord's message identifiers encode creation times. The March-20 link decodes to **2020-03-20 03:55:45 UTC**; the April-6 evidence message to **2020-04-06 23:14:57 UTC**; and the April-21 website-index message to **2020-04-21 05:37:42 UTC**, between the two pinned Git commits. A message ID establishes the *timestamp of the linked message*, **not independent authentication of its content**. This report uses the community's source-linked summary and snapshots; direct Discord message bodies remain unverified here.

## Fixed character comparison

All strings are **21 ASCII characters** long, `dat/` prefix included. We counted exact positional mismatches, with the Levenshtein distance independently agreeing because no edit insertion or deletion is beneficial.

| Historically reported stage | Candidate reading | Exact matches | Mismatches |
|---|---|---:|---:|
| March 20 candidate | `uat/5345rn9653f9i8nmd` | **17/21** | **4** |
| April 6 candidate A | `dat/534brn9653f9i8rnd` | **18/21** | **3** |
| April 6 candidate B | `dat/534brn9653f9i8nmd` | **19/21** | **2** |
| Externally listed endpoint, April 21 | `dat/534brn9653f9j8mmd` | **21/21** | **0** |

For the strongest earlier candidate, the remaining unresolved positions are **17** (`i` versus `j`) and **19** (`n` versus `m`). These were not cleanly forced by that historical reading. A discovered genuine path could settle them, while its strong **19/21 positional agreement** makes the CE background connection meaningful. This does not require believing an arbitrary textual coincidence.

The auditable data are in [`data/experiment-460-background-url-discovery.json`](../data/experiment-460-background-url-discovery.json); the offline exact comparison and timestamp verifier is [`scripts/audit_2020_background_url_discovery.py`](../scripts/audit_2020_background_url_discovery.py):

```sh
python scripts/audit_2020_background_url_discovery.py
```

The verifier optionally accepts separately obtained pinned upstream README source files via `--before` and `--after`, which check the respective exact-URL absence/presence. Its default offline fixture does **not** download Discord messages or establish original website backend behavior.

## Important limitation: what “site index” means

The saved [`terminal41.link/index.html`](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/index.html) is simply a meta refresh to `loadSys/`; it is **not** an archival copy of the actual directory/server index reportedly examined on April 21. Thus we have strong **community-reported discovery-channel provenance**, but we do not yet have the original actual index listing bytes nor an independent server log of how the path was found.

We can nevertheless distinguish three statements that should **not** collapse into one row:

1. **Physical:** the nine sticker artwork classes assemble into a coherent background, with a strong *partially readable* string. This is genuine evidence.
2. **Discovery:** the community account says the exact candidate path became known by *website index enumeration* and was matched retrospectively to that background. The pinned Git before/after versions are consistent with this chronology.
3. **Intended authorial connection:** because the mosaic strongly resembles an active path, it is reasonable to treat the address as the intended destination of the *background*. **Neither the address's exact characters nor the foreground's decoding operation were established as completely blind, independently forced output**. This does **not** suggest the background is fake, incidental or unsolved in ordinary ARG terms.

## Implications for current sticker theories

**Discovery-channel leakage can turn an ambiguous code into an apparent complete decode.** The original CE background is an historical positive case for *answer-assisted recognition*. Future proposed sticker results should declare whether the output was fixed **before** opening/searching the candidate source. Otherwise a discovered page/code/URL may have guided symbol interpretations, orientation, OCR, or registration.

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

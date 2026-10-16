# Terminal41 entity alias source sweep and public-handle retrieval controls (2026-10-16)

**Research mode:** DISCOVER (source-grounded identification and public-account search). **Change status:** no new fictional account identified; no sticker observations altered. **Reproducible machine-readable census:** [74-entry source audit](../../data/reference/inside-arg-terminal41-entity-source-sweep-2026-10-16.json), keyed to source tree SHA `4de72d7c2f21bd9eb4144fda51281c84cbcb90c4`.

## Main source result

The [74-file mirrored Terminal41 inventory](../../data/terminal41-source-tree.json) has **73 text or text-like files plus one PNG**. Every textual file was read directly from [twinysam/INSIDE-ARG](https://github.com/twinysam/INSIDE-ARG) and searched case-insensitively for:

`anset`, `setrinamaire`, `anthony`, `tony`, `rorschach`, `noah`, `gladblad`, `tobber`, `7hg553`, `facility`, `89b`, `twitter.com`, `youtube.com`.

Findings for those **exact substring expressions**:

| Original file | Raw case-insensitive hits | Interpretation |
|---|---|---|
| `dat/534brn9653f9j8mmd/index.html` | `AnSet` 3 | All in **one** corrupted JFIF/XMP carrier; readable metadata, not 3 separate authors or channels |
| `comms_main_viewgate.html` | `facility` 2; `89b` 2; `7hg553` 2 | Verbatim `Facility 89B(7hg553)` on an original viewgate schematic |
| `comms_main_viewgate_002.html` | same as above | Variant of **same named facility**, not an independent real-world group |
| `dat/breach_contribution_reg.html` | `89b` 2 | Incidental hex-hash substrings, **not** additional Facility89B references |
| other 69 textual paths | zero | Corpus-bounded negative for the 13 **literal** expressions |
| `comms/gate/98/transmission_id…k.png` | not in textual sweep | Binary PNG; text/metadata/encoded-audio inspection is a different test |

**Recovery of the difficult 1.9MB SAF document.** Initial GitHub `fetch_file` API responses for `dat/saf_dat_col.html` returned an empty text field even when providing a line range, creating a **false content-absence risk**. A direct SHA-addressed `fetch_blob` returned the complete readable content: **1,265,970 JavaScript Unicode characters, 5,014 lines, an end-of-content marker, and 1,986,163 bytes on manual UTF-8 re-encoding**, precisely equal to the source tree's 1,986,163-byte size. Its 13 alias searches are all negative. **This byte count is a completeness control, not an independently recomputed SHA1 hash.** Do not report it as unexamined or absent.

The 2016 source metadata date `2016-12-16T14:12:24.351` and `2016:08:09 14:12:24` are internally stated artifact dates, not authenticated original creation/delivery times. The October 8 canonical A audit already preserves the exact-source byte distinction. **The existing primary repository A copy also contains the three `AnSet` occurrences**. This investigation did not newly discover the name's existence.

## Community-supported relationship and actual account search

The community already discussed **`AnSet` ≈ `An`thony `Set`rinamairé**, as reconfirmed by the project user. Classify this as a **high-priority, community-supported interpretation** rather than an invented October 2026 theory. Because the linked metadata dates predate the original June 2018 documented printer/YouTube persona, don't imply a 2018-initiated character creation or authenticated pre-reveal disclosure.

The [Game Detectives ARG chronology](https://wiki.gamedetectives.net/w/Inside_ARG#Youtube_Stream) documents **Anthony T. Setrinamairé** as the printer Gmail identity and the uploader of [the apparently never-live Terminal41 stream](https://www.youtube.com/watch?v=dWhmPSjOybI). The [original June 4 2018 Steam thread](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=52) confirms historical researchers initially searched the full surname and email. Separately searching nickname **Tony**, exact `AnSet`, diacritics, spacing, joined handles, and site restrictions is therefore a worthwhile new **query family**. The name combination itself and its possibility of being shorthand are *not* novel discoveries.

**Actual search probes:** A targeted general-index `fast` and `slow` campaign tested exact `AnSet`, surname and Tony forms, combinations with INSIDE/Playdead/Terminal41, domain limits for Reddit/Steam/YouTube/X/Bluesky/Tumblr/Instagram/GitHub, and the stream's stable video ID. No separate independently attributable fictional ARG account or historical YouTube channel ID was recovered. YouTube's original video page returned a throttled fetch error. This is **not** proof no such account exists. Documented historical YouTube video link is a positive, not a channel-ID recovery.

A `site:steamcommunity.com/id` search surfaced non-ARG/current names and broad common-word `anset` matches; none met the necessary Playdead/Terminal41 or dated-content connection. Likewise GitHub `AnSet` search is polluted by the Danish/Norwegian word and transliteration of other words. Name-matched private individuals must **not** be identified as ARG participants without original public connection.

## Other ranked source terms and disambiguation

* **`GLADBLAD`** is the strongest observed account-to-game-asset link: a **2016 Steam post already connects** the hidden Morse texture to staff artist `TobberH`, `tobbermix.gladblad.dk`; current public X/Steam/GameTracker and 2010-era `Gladblad Gamers` accounts corroborate a pre-existing developer/gaming-community signature. This finding belongs in the [identity dossier](inside-arg-fictional-identity-account-recon-2026-10-16.md), with the important caveat that the 2016 community had identified it first. The likely role is an Easter egg; no official ARG operation is demonstrated.
* **`Rorschach Desgn Noah x200564`** appears exactly in an original 2016 [Steam-reported unpacked texture](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2), with [contemporary standalone discussion](https://steamcommunity.com/app/304430/discussions/0/359543951708963220/). The word `Desgn` can plausibly be a contracted *designation*, not a corporate name. A subsequent 2020 claim that it says `Porsche Design` was challenged on the original unpacked texture; don't divert into Porsche accounts without new source verification.
* **`Facility 89B(7hg553)`** is verified exactly in the two archived HTML viewgates. Search `7hg553` with context, not every account bearing common `facility`.
* **Terminals 11/23/42/99** are recorded in the [original April 2020 directory screenshot recovery](../conjecture-lab/2026-10-08-terminal41-unarchived-route-recovery.md), not asserted to be extra live social accounts.
* **`printer.jpg` credited author Andreas Normand Grøntved** is an original 2018 [Steam observation](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=53); ordinary asset authorship must not be confused with fictional Anthony/AnSet attribution.

## Safe continuation with measured coverage

Keep [the 50-term candidate registry](../../data/reference/inside-arg-fictional-account-name-candidates-2026-10-16.tsv) and [553-query cross-platform manifest](../../data/reference/inside-arg-fictional-account-platform-search-manifest-2026-10-16.tsv) as **planned search tasks**. Only five are verified source links; the other **548 are pending unexecuted manifest rows**. The web searches carried out in the conversation are a separately recorded bounded pilot, **not proof every manifest entry ran**.

Highest-value next tests are (1) recovering the old YouTube *channel* identifier or original video metadata through lawful historical archives, (2) dated, directly discoverable `AnSet` account references that link to independent Playdead artifacts rather than metadata copies, (3) raw binary/XMP searches in distinct source images for repeated `AnSet` author fields, and (4) running indexed account searches with real dated positive controls for each surface. Preserve original date, archive date and first-seen date as separate fields.

A match qualifies as a new ARG-controlled account only with a verifiable contemporaneous link from Playdead/Terminal41 or an original ARG artifact, not based on surname shape, a matching acronym, brand name, or follower-count speculation. No account messages, owner outreach, or unrelated individual deanonymization were attempted.

**Outcome at safe stop:** original-source Terminal41 text sweep completed **73/73**; one large PNG intentionally not included in text pass; **one confirmed staff-linked online identity graph already noted in 2016**; **zero new independently confirmed fictional ARG personas**.
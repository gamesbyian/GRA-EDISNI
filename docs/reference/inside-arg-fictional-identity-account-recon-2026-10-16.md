# In-universe account and alias reconnaissance: Anthony/Tony, AnSet and Terminal 41

**Date:** 2026-10-16. **Mode:** DISCOVER / public-source account-discovery reconnaissance. **Scope:** ARG-authored fictional identities, in-world labels and public social/web account candidates; **not** Collector's Edition owner-handle tracing. Nothing here changes the physical sticker corpus or solves the foreground.

## Outcome in brief

* No independently attributable *additional* ARG-operated account was confirmed by the bounded public web/GitHub search described below. This is **not** a negative finding about all platforms or archived accounts.
* The documented persona **Anthony T. Setrinamairé** used the original Playdead printer email sender identity and also appeared as the creator/uploader of the contemporary YouTube item `Terminal41 emergency comms transmission [DATA STREAM]` at [video ID dWhmPSjOybI](https://www.youtube.com/watch?v=dWhmPSjOybI). This is **known ARG infrastructure**, not a newly found account. [Game Detectives contemporary chronology](https://wiki.gamedetectives.net/w/Inside_ARG#Youtube_Stream), [2018 Steam thread](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=52&l=schinese).
* **Newly verified within this particular search:** `AnSet` occurs as the literal `dc:creator` value in an original preserved Terminal41 artifact, not just in BigDusty's 2026 concept map. It is an **authentic metadata author token** but **not a proven second account** or a proven alternate identity of Anthony.
* **Pre-existing repository evidence, verified after initial write:** GRA-EDISNI **main** already preserved `AnSet` three times in `archive/external/terminal41-534brn/A-original-capture.bin` (source Git blob `ce55c03ee972954f6e80f55a1a279bb85024f99b`) and in its separately labeled altered-connector rendition `A-connector-rendition-not-original.bin`. The twinysam source HTML also contains three instances. This PR **did not discover or add the source string to the corpus**; it documents the cross-context author/alias interpretation for the first time in this dossier.

* **Also primary-source verified:** `[Facility][89B(7hg553)]` appears in the original archived `comms_main_viewgate.html` and `comms_main_viewgate_002.html` Terminal41 pages. This is a source-grounded facility identifier, not a demonstrated organization account.
* **Other source-backed identity vocabulary:** `Rorschach Desgn Noah x200564` from `SIGN_GirlLab_A_#935`; `GLADBLAD` from `Sign_SecretMorse_#944`; Terminal IDs **11, 23, 41, 42, 99** from dated April 2020 original screenshots. None is an established person's name beyond Anthony; don't collapse texture labels, filesystem names and playable-character labels into social personas.

## 1. Anthony, Tony and the documented identity

Canonical original name **Anthony T. Setrinamairé** (unaccented index form **Setrinamaire**). Original email sender **qpzympraddjjnymblns@gmail.com**. A documented 2018 account had a photograph of a dot-matrix printer as the Gmail avatar. The archived Game Detectives chronology says a Google surname search **at the time of discovery** led to the one YouTube item; an original June 4, 2018 Steam comment also says full-name and email searches had produced nothing obvious. [Game Detectives](https://wiki.gamedetectives.net/w/Inside_ARG#Youtube_Stream), [Steam original](https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=53&l=hungarian), [Reddit investigation](https://www.reddit.com/r/PlaydeadsInside/comments/8urx3h/major_ongoing_arg_we_need_help_figuring_this_out/).

Search alternatives intentionally include nickname **Tony**, nickname **Ant**, alternate spelling **Antony**, middle initial `T`, full/surname-only concatenations and accent-folding. *Naming possibility alone does not establish the same operator*. In particular, a `tony` account cannot be tied to the ARG by an unverified matching given name.

Search expressions actually probed during this session included exact and case/diacritic variants of `"Tony Setrinamaire"`, `"Tony Setrinamairé"`, `"Tony T. Setrinamaire"`, `"tonysetrinamaire"`, `"Anthony T. Setrinamaire"`, `"Setrinamaire"`, `"qpzympraddjjnymblns"`, plus `Playdead`, `terminal41`, `site:youtube.com`, `site:reddit.com`, `site:github.com`, `site:instagram.com`, `site:bsky.app`, `site:tumblr.com`, `site:steamcommunity.com` and `site:twitter.com` variants. **No new positively affiliated account surfaced**. Results are search-index and query-scope-limited, and are not proof that names were unavailable/never registered.

## 2. AnSet: independently traceable original metadata

Exact primary witness: [twinysam/INSIDE-ARG `terminal41.link/dat/534brn9653f9j8mmd/index.html`](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/dat/534brn9653f9j8mmd/index.html), a community-preserved page with a partly corrupted JFIF/EXIF stream and a readable embedded XMP segment. The segment contains:

```xml
<xmp:createdate>2016-12-16T14:12:24.351</xmp:createdate>
<dc:creator><rdf:seq><rdf:li>AnSet</rdf:li></rdf:seq></dc:creator>
```

The readable string is **not exclusive to the XMP block**: in the existing [GRA-EDISNI primary A artifact](../../archive/external/terminal41-534brn/A-original-capture.bin) it occurs three times, including earlier EXIF-adjacent creator text. Because the GitHub connector has historically produced different byte renditions for binary files, these are verified **readable substring observations** in the checked repository artifact, not newly asserted raw-byte offsets or an independent author identification. The earlier CL-09 original-byte checksum verification remains the provenance authority.

The same displayed artifact also includes `2016:08:09 14:12:24` strings in EXIF-like material. *Different metadata clocks must not silently be converted into one chronology or considered authenticated production timestamps.* These bytes may be preserved as a display rendition of a damaged original: the Oct 8 [CL-09 audit](../conjecture-lab/2026-10-08-terminal41-unarchived-route-recovery.md) shows the GitHub connector's 12,150-byte A rendition differs from the 12,140-byte hash-authenticated original A. Accordingly the string was verified from the **source page's readable metadata fragment**, but **no new byte-authentic XMP claim** is made without checking [the preserved exact original A bytes](../../archive/external/terminal41-534brn/A-original-capture.bin).

Independent modern secondary visualization: [BigDusty's ARG concept map](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/block_descriptions_full.json) places the literal `AnSet` label near `Anthony T. Setrinamaire` under an EXIF/author heading. The map dates to 2026; it is **not** independent historical evidence that `AnSet` was a public username.

Tested hypotheses:
1. **H-A:** `AnSet` is `An`(thony) + `Set`(rinamairé), an ARG persona/production pseudonym. This string transformation is natural but selected after seeing the target; requires independent owner-controlled link or dated account content.
2. **H-B:** `AnSet` is a separate graphic's author/software handle unrelated to the email/stream persona.
3. **H-C:** `AnSet` is an intentionally false or arbitrary metadata value.

Do not infer H-A because it is satisfying. Run handle-focused source searches for `AnSet`, `An_Set`, `an.set`, `anset41`, `an_set41` and intersections with `terminal41`, `printer`, `playdead`, `inside`; use temporal snapshots and independent linkage as the test. Current public searches under `AnSet` are dominated by the Danish/Norwegian common word **anset** and unrelated present-day brands. Broad `anset` hits are unreliable.

## 3. Documented in-world labels and account-candidate families

| Exact source-grounded label | Primary or independently dated source | Account-hunting candidates (speculative) | Relative priority |
|---|---|---|---|
| Anthony T. Setrinamairé | 2018 Game Detectives/Steam, original printer email + YouTube | `TonySetrinamaire`, `TonyTSet`, `AntSetrinamaire`, `AnthonyTSet`, `Setrinamaire`, accent-folded | Very high |
| AnSet | Terminal41 534brn embedded `dc:creator` | `AnSet`, `An_Set`, `anset41`, `AnSetrin` | Very high |
| Facility 89B(7hg553) | Original [viewgate](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms_main_viewgate.html) and [viewgate_002](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms_main_viewgate_002.html) HTML | `facility89b`, `89b7hg553`, `7hg553`, `facility_89b` | High, but label may only be a subsystem |
| Rorschach Desgn Noah x200564 | 2016 [Steam source-asset witness](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2), texture `SIGN_GirlLab_A_#935` | `rorschachdesgn`, `rorschach_design`, `noahx200564`, `x200564` | Medium-high, ambiguous designation vs identity |
| terminal41.link | Community-preserved `/loadSys/`, `/comms/`, `/sys/` and `/dat/` | `terminal41`, `term41`, `emergencyterminal41`, `terminal_41` | High |
| 11 / 23 / 41 / 42 / 99 terminals | [CL-09 2020 screenshot recovery](../conjecture-lab/2026-10-08-terminal41-unarchived-route-recovery.md); source screens show `terminate_terminal` directories | `terminal11`, `terminal23`, `terminal42`, `terminal99` | Medium, exact site routes are stronger than social usernames |
| Gateway, breach contribution registry, gate 98 | Preserved Terminal41 HTML path vocabulary | `gateway98`, `gate98`, `breachcontribution`, `breachlog`, `viewgate002` | Medium |
| GLADBLAD | 2016 Steam unpacked texture `Sign_SecretMorse_#944` | `gladblad`, `gladblad41`, `gladbladinside` | Low-medium; ordinary Nordic name/word collisions |
| WaterGirlWireFake | 2016 internal game-asset references; confirm exact native filename before asserting in-world label | `watergirlwirefake`, `watergirl` | Low-medium |
| Huddle | In-game creature and CE marketing | `huddle` variants only with rare high-precision project anchor | Low: huge non-ARG background |
| MANUN KIND / `manunkind` | E. E. Cummings poem reproduced in the solved ARG | Treat as a *literary phrase*, not a fictional organization; search only when linked to ARG date/site | Low |

**Evidence qualification:** `Rorschach Desgn` is literally on an in-game texture but not a confirmed corporate name, and `Noah` need not be a human employee. `GLADBLAD` is a deciphered asset string, not a documented ARG social actor. `Breach Contribution Registry` is merely a convenient expansion of the literal `breach_contribution_reg.html` path, not a verified named company. The `terminal41` GitHub search currently produces unrelated generic terminal software and travel blog repos; name collision is insufficient evidence.

## 4. Search execution and negative evidence

**Coverage caveat:** the GitHub connector reports `gamesbyian/GRA-EDISNI` currently `is_code_search_indexed=false`. Therefore an empty scoped GitHub code search in our repository **is not evidence of absence**. The main-branch `AnSet` occurrences were verified by direct retrieval of known binary paths, not code-search hits. GitHub's indexed search found one twinysam text file (three literal instances), but that does not establish exhaustive binary-file coverage.

This was a bounded live web-index plus connected GitHub **global file-content search**, with reference comparison to original Steam (2016/2018), Game Detectives, BigDusty's independent 2026 map and twinysam's mirrored source. Public platforms considered: Google-style general indexing, GitHub file/repo discovery, YouTube, Reddit, X/Twitter, Bluesky, Tumblr, Steam, Instagram. Search providers do **not** guarantee account/member lookup or unindexed/renamed/deleted profile recovery. No claims of complete searches of those native platform databases are made.

| Probe family | Result | Evidence classification |
|---|---|---|
| Anthony/Tony/nickname/surname, accent-fold and joined handles | Original community research and known Youtube identity; no new independently linked account | Search-index negative only |
| `AnSet` exact and with Playdead/INSIDE/Terminal41/EXIF | Original metadata witness found; unrelated common-language/name hits predominate; no independent dated account | Positive original artifact, account unresolved |
| `Facility 89B` / `7hg553` | Exact text verified in viewgate HTML; no attributable separate account | Positive original artifact, account unresolved |
| `Rorschach Desgn` / `Noah x200564` | Original texture described in 2016; later fan/wikis cite it; no attributable account | Positive game artifact, account unresolved |
| `GLADBLAD` | 2016 texture report and unrelated Nordic/public names; no support for attribution | Weak alias candidate |
| `terminal41` | Known ARG website; unrelated later GitHub repos under same stem | Known organization/site, no new account |

No source-backed second fictional online persona or ARG-controlled extra social account has been demonstrated by this search. **Do not contact accounts that happen to share one of these names.**

## 5. Next discriminating steps, in priority order

1. **Metadata connection test (best):** inspect raw byte-authenticated 534brn A and any other independently saved versions. Extract EXIF/XMP properties and maker/software fields. Check whether `AnSet` appears in other original files or online under that exact casing **before** the ARG's public reveal. Pair with `Anthony` only after an independently evidenced overlap, not on name resemblance.
2. **Resolve the original YouTube *channel ID*, not merely video ID:** use an accessible 2017–2020 channel snapshot, redirect, video metadata, Web Archive copy, or public oEmbed cache; inspect contemporaneous display names, channel `@handle`, older custom URL and linked website. Current video pages can be unavailable or renamed. Match actual channel identity, not subscriber counts from the 2026 concept map.
3. **System-name exact corpus scrape:** extract distinctive tokens from the preserved 74 Terminal41 pages, `/sys/` index photographs, original printouts, headers and original image metadata. This is far more defensible than inventing generic entity names. Assign string provenance and date.
4. **Search rare identity compounds with positive controls:** `AnSet`, `facility89b`, `7hg553`, `noahx200564` and `qpzympraddjjnymblns` via site-native public account indexes, archived profile URL patterns and permitted historical archive collections. Use 2016–2020 date controls and verify that engine can retrieve one known positive for the platform.
5. **Cross-platform linkage gate:** only label an account ARG-affiliated if it has an original-date Playdead/Terminal41 link, matched archived account metadata, publication of unreleased ARG text/media, or an original official referral. Generic gaming interest, same nickname, same avatar category or contemporary fan reposts are insufficient.
6. **Stop condition:** after documented queries, original-source controls and platform caveats, log the negatives; reopen only for new original archival evidence or discriminating associations. Preserve creative alias tests in DISCOVER, avoid inflating findings.

## Source links and provenance cautions

* [twinysam original-page mirror, metadata `AnSet`](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/dat/534brn9653f9j8mmd/index.html), [original viewgate](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms_main_viewgate.html), [viewgate_002](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms_main_viewgate_002.html).
* [Game Detectives ARG chronology](https://wiki.gamedetectives.net/w/Inside_ARG); [2018 Steam thread documenting Anthony name and Gmail](https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=53&l=hungarian); [2016 original unpacked asset report](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2).
* [BigDusty's 2026 visual puzzle map](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/block_descriptions_full.json), valuable as a discovery index but not independent 2016–2018 proof.
* [Own CL-09 source recovery audit](../conjecture-lab/2026-10-08-terminal41-unarchived-route-recovery.md) and authenticated `A-original-capture.bin` caveat. Never equate the GitHub connector's modified binary rendition with SHA-verified original bytes.
* [Raezore community search-method baseline](raezore-community-search-baseline-2026-10-13.md) is specific to CE-owner sourcing; already includes extensive historic owner alias searches. This report is a **different** inquiry into fictional ARG accounts and must not claim that handle search is newly invented or that research has been exhaustive.

**Findings maturity:** source strings **confirmed in preserved source**; relationships/alias continuity **hypotheses**; additional account discoveries **none independently confirmed**.
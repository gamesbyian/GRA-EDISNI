# CL-09: original 2020 site indexes expose lost Terminal41 routes and backups

_Research date: 8 October 2026. Source-first archival archaeology, not a recovered sticker foreground decoder._

## What was recovered

The current [Terminal41 snapshot](../data/terminal41-source-tree.json) contains **74 files** from the public `twinysam/INSIDE-ARG` mirror. Previous source-native consumer audits searched that surviving set correctly but, through no fault of the parser, could not identify resources outside its inventory.

The **original April 2020 conversation** includes four photographic/screenshotted artifacts recording the server's directory listing and state differences. The archived messages and image bytes are publicly preserved by `gamesbyian/playdead-unofficial-exports`, pinned to their original blob hashes. **We have now copied their original bytes, hash-checked, into this repository** at `archive/external/terminal41-2020-index/`. Their origin, sizes, and evidentiary limits are enumerated in [the machine-readable directory census](../data/terminal41-screenshot-index-gaps-2026-10-08.json).

Original unmodified screenshots:
- [System directory](../archive/external/terminal41-2020-index/sys-index.png), upstream Git blob SHA1 `48cdd698a5d9303609cd2659d020a0c31a52cffc` (119,780 bytes).
- [Terminate-terminal directory](../archive/external/terminal41-2020-index/terminate-terminal-index.png), `e3d7287527a5482cb58a41837873f396e0c79ee7` (40,251 bytes).
- [Data directory](../archive/external/terminal41-2020-index/dat-index.png), `a56809a9856020489a87ff38d114ae4a67d83964` (70,405 bytes).
- [Current versus backup contributor registry screenshot](../archive/external/terminal41-2020-index/breach-backup-contrast.png), `95bb5aaec9a9f2da0966744fbc80b67f7f358c99`.

The first two images were attached by the original index discoverer at approximately **11:41–11:42 on 21 April 2020, in the export's unspecified local timezone**. The `/dat/` directory screenshot was reattached the following day. The separately archived 5,092,410-byte, 224,295-line primary Discord source has Git blob `1889cc948f86f5a4455de0d7310b15cdb1b88b5c`. See original historic screenshots rather than assuming secondary timelines accurately represented the entire website.

## Additional historical names absent from the 74-file mirror

**At least 10 relevant directory/file targets** are missing from that pinned 74-file snapshot:

| Witness / path | Screenshot last-modified display | Current source status | Confidence |
|---|---|---|---|
| `/sys/all_sys_hibernate/` | 2019-04-15 15:01 | No preserved children | Exact name in original `/sys/` screenshot |
| `/sys/terminate_terminal/11/` | 2019-12-16 06:37 | No preserved children | Exact `11/` directory |
| `/sys/terminate_terminal/23/` | 2019-12-16 06:37 | No preserved children | Exact `23/` directory |
| `/sys/terminate_terminal/42/` | 2019-12-16 06:37 | No preserved children | Exact `42/` directory |
| `/sys/terminate_terminal/99/` | 2019-12-16 06:37 | No preserved children | Exact `99/` directory |
| `/dat/saf_dat_col_BACKUP.html` | 2019-04-16 13:59 | Not preserved; 1.9M displayed | Full visible link name |
| `/dat/breachlog_BACKUP.html` | 2019-04-16 13:53 | Not preserved; 285 displayed | Full visible link name |
| `/dat/breach_contribution_reg_BACKUP.html` | 2019-04-15 11:01 | Not preserved; 11K displayed | Filename recovered from truncated listing **plus** 2020 discussion and side-by-side comparison |
| `/sys/printreqstatus_BACKUP.html` | 2019-04-16 13:58 | Not preserved; 2.7K displayed | **Inferred** completion of visibly truncated `printreqstatus_BACKU…` |
| `/sys/printreqstatus_SD_BACKUP.html` | 2019-04-14 03:26 | Not preserved; 2.4K displayed | **Inferred** completion of visibly truncated `printreqstatus_SD_BA…` |

One additional directory **is preserved**: `/sys/terminate_terminal/41/`, displayed as last modified `2019-12-16 06:39`. All five numbered terminals in the image are **11, 23, 41, 42, and 99**. No assertion of five playable/interactive choices follows merely from an Apache directory listing.

The screenshot's "Last modified" column is server-supplied metadata, **not authenticated creation or release time**. Nonetheless the display places `all_sys_hibernate/` with the older April 2019 status pipeline, and the numbered terminal namespace alongside December 2019 sources close to the CE's shipment. This is an archaeological priority cue, not proof of causal relation.

## Primary-source testimony narrows meaning

The index discoverer's original [21 April 2020 archived conversation](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/Playdead%20Unofficial%20-%20ARG%20-%20solving%20%5B461275582970462209%5D.txt) says the other terminal IDs **led to a hibernating message** and explicitly distinguishes **41** from the others. At approximately 11:49, the participant wrote that other terminal routes "led to [systems hibernating]," immediately clarifying "everyone other then 41." These are eyewitness *text* reports, **not** captured HTTP source for the routes or evidence of a 3-way input surface.

More importantly, original messages already describe **"[all systems hibernating]" on 17 April 2019**, before the December 2019 CE. Thus the hibernation language is demonstrably **not a new CE-only receiver**. The numbered terminal names 11,23,42,99 may be dormant endpoints, not additional ways to accept slash/dash/dot inputs.

**23** is one of five numeric folder names, but that's the only direct relationship we can state. Assigning extra code significance to it without a typed input/operation would repeat a known numerological failure.

## Missing backup files are higher-value than missing hibernation pages

A [22 April 2020 primary screenshot](../archive/external/terminal41-2020-index/breach-backup-contrast.png) compares nonidentical **current** and **BACKUP** contributor registry pages. The earlier backup display is in a caching/completed but data-missing condition, while the other copy contains detailed contributor entries, changing percentages and transmitted hexadecimal strings.

This is strong evidence that **backup route data can capture a different historical *state***. It does *not* prove the unpreserved 1.9MB `saf_dat_col_BACKUP.html` contains different or lossless data. But such a genuine alternative captured payload is a much better prospect for restoring damaged information than brute-forcing unknown JPEG entropy bytes or manufacturing new missing physical stickers.

Prefer original snapshots, original backup files, contemporary disk/browser caches, or complete unmodified screenshots. Do **not** reconstruct 1.9 MB of content from a filename and displayed size.

## Read-only archive-recovery attempt and limits

A one-shot source-acquisition runner queried the public Internet Archive **availability** and **CDX** services for exactly six screenshot-derived route paths. All six availability requests succeeded at HTTP 200 with **empty `archived_snapshots` maps**. The corresponding CDX queries responded with HTTP 503 or timed out.

This proves **no snapshot was returned by that particular availability API**, not that the original server pages never existed, not that an archivist has no private copy, and not that every alternative archive was searched. The historic `534brn` source is itself absent from some public archiving systems despite contemporaneous screenshots, so absence of an API hit should not be mistaken for source nonexistence. Full provenance can be regenerated using [the bounded archival query script](../scripts/probe_lost_terminal41_archive_routes.py); it targets archive services **only**, never the current domain. No account login, original-site requests, or user outreach occurred.

## Concrete byte-source correction: A was still corrupted in *our* archive

A separate [canonical 534brn evidence audit](experiment-534brn-canonical-partial-evidence-alignment-2026-10-08.md) had already flagged an important integrity hole. The previously retained `A-connector-rendition-not-original.bin` measures **12,150 bytes**, source Git blob `f9cdbd18bbd8713adee89ad93a3551b6310fd7ba`. It is *not* upstream original A.

We directly acquired and hash-verified the true historical **12,140-byte** A payload from `gamesbyian/playdead-unofficial-exports`, original blob SHA `ce55c03ee972954f6e80f55a1a279bb85024f99b`, and committed it as [A-original-capture.bin](../archive/external/terminal41-534brn/A-original-capture.bin). A GitHub connector response using even its explicit **base64** option reproduced the altered 12,150-byte form, so merely reading the metadata's stated Git SHA is **not authentication**. The upstream Git blob identity was checked on raw `curl` bytes in the source runner, then checked again against the committed branch Git tree. Its exact byte identity is now verified.

We keep the old 12,150-byte rendition so the original 2026-10-08 canonical partial-token fixture remains reproducible and explicitly tagged as **rendition-assisted**. The [authentic-A recomparison](../scripts/audit_534brn_original_a_comparison.py) checks whether the alternative exact source changes any aligned candidate recovery, still reporting every restored value as **heuristic alignment-supported**, never as a uniquely proved JPEG byte. The canonical alignment and decoder are not automatically overwritten by a new candidate count.

## Priorities and decision gate

1. **Recover actual bytes** for `saf_dat_col_BACKUP.html` and backup printer/contributor states, preferentially from original 2020 public screenshots/files or archives. File existence and differing response contents are distinct proof obligations.
2. Treat `sys/all_sys_hibernate/` and other terminal numbers as **historical routing evidence**, not proven CE symbol readers. Only reopen them as a consumer if an authenticated source yields input instructions or a symbol-sensitive response.
3. Use the now-authentic original A capture in an explicitly **separate**, source-checked damaged-JPEG alignment audit; preserve all ambiguity, do not silently upgrade a fitted recovery to original pixel ground truth.
4. Continue seeking a source-authored **sticker foreground** consumer and mapping; the currently verified connection is nine sticker backgrounds → the `534brn` endpoint. The missing routes widen the source inventory but **do not supply the foreground mapping**.

**Conclusion:** this is a real enlargement of the known original Terminal41 namespace and a correction of the forensic byte provenance, not a newly solved CE foreground. These source acquisitions are more valuable than another unrestricted pattern search because the results can actually change which original evidence survives.

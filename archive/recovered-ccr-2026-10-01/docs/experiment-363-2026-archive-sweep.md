# Experiment 363 — 2026 public-archive sweep for sticker-relevant cues

_Status: completed triage, 1 Oct 2026. No model change._

A sweep of the 2026 messages in the public exports (`solving`, `solving-breakout`, `inside`) and of Terminal41 pages, looking for anything that could serve as an external cue for the sticker foreground.

## Sticker ledger sync

Upstream `twinysam/INSIDE-ARG` `stickers.md` (latest commit 4de72d7, 26 Sep 2026) lists the same 82 numbered stickers as `data/observations.csv`, with **0 symbol conflicts** and **0 new stickers**. Entries 164 and 476 differ only in Markdown formatting (a tab and a missing colon). The recent upstream edits (/223, -444, /324, -021, L34/U28) are provenance updates to stickers already recorded.

## Items checked

| item | source | outcome |
|---|---|---|
| CEO-door string as 4-sticker letter groups | solving-breakout, Jan 2026 | Excluded by raw data at all starts (Experiment 362). |
| `andreas/superSecret/image` audio → 610×376 RGB image | solving-breakout, 27 Mar 2026 | Real hidden content (concept art; present in day-one PS4 files), but it is a standalone game-file image. No sticker-registered parameter. aperson1's capacity argument holds: the stickers carry ≤ ~200 bits. |
| `[aux. dirs lookup:][HIDDE---..--./-/.-/-/././////…` | `loadSys/__.html`, first discussed June 2018 | Already explained historically as a hint to the hidden directories. It mixes dashes and dots, so it can't be a contiguous run of the sticker pattern: the 81/27 split means no contiguous window of the 108-cell pattern contains both. |
| `[aux. dirs lookup:][HI_:.-.-./-./-…error]` | `loadSys/___________DONE.html` | Same family and status as above. |
| Cover monitor 4 ("progress bar / battery") | post-359 scan residual question | See below. |

## Cover monitor 4

The post-359 scan left one bounded cover question open: does the fourth monitor (progress/battery display) match a pre-December-2019 ARG artifact, as the acorn, planet and diagnostic graph do?

Two Terminal41 progress sequences existed before the CE:

- `loadSys/_.html` → `__________.html` → `___________DONE.html` (ten steps then DONE), discussed in `solving` by 27 Jun 2018;
- `sys/activate_shutdown_protocol/commit/_.html` → `___________DONE.html` → `DONE_SD_CONFIRMED_01…09`, discussed by 13 Apr 2019. On 14 Apr 2019 pitch_bright referred to it as "the progress bar" being moved during the live event.

The best surviving scan (`INSIDE_A-75c1e61d8bc695be.JPG`, 6552×5040) resolves the monitor only to halftone-dot level. A single filled bar is visible, but its fill level and segment count cannot be measured, so the specific sequence and step cannot be identified. Historical owner descriptions disagree ("about 40%" vs "0%").

**Conclusion:** a pre-CE progress-bar artifact exists for the fourth screen, so all four monitors plausibly recap earlier ARG material. That strengthens the post-359 reading that the cover is a bridge back into the old ARG, not a key for the foreground. Settling the remaining step-level question needs a direct high-resolution photo of a physical cover, which is an acquisition item, not an analysis item.

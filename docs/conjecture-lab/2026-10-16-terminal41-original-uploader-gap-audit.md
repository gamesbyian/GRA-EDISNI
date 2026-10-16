# Original Terminal41 mirror uploader's missing-file disclosure

**16 October 2026. Mode: VALIDATE for the August 2023 Git commit's actual documentary contents; DEVELOP for interpretations of missing 2019–2020 server functionality.** This corrects the novelty wording in the earlier [complete-client census](2026-10-16-terminal41-full-client-receiver-census.md), not its source-graph measurement.

## Upstream original evidence

The upstream community repo `twinysam/INSIDE-ARG` added the Terminal41 mirror in its [18 August 2023 archive-upload commit](https://github.com/twinysam/INSIDE-ARG/commit/d0b11cf8c6462c9592bc141ee6a4dddc0a029da6). Its original commit message **explicitly lists files that were missing**, including the intermediate redirect target that our 16 October 2026 graph scan surfaced:

- `sys/index.html`;
- `dir/index.html`;
- `sys/activate_shutdown_protocol/commit/___________DONE_SD.html`;
- `sys/activate_shutdown_protocol/commit/___________DONE_SD_CONFIRMED.html`;
- `sys/activate_shutdown_protocol/commit/___________DONE_SD_CONFIRMED_10.html`;
- `sys/terminate_terminal/41/y/index.html`.

These are the uploader's reported **missing source files**, not a discovery of their original contents. In particular the `_CONFIRMED_10` filename is documentary evidence about a known missing file, **not** proof that a tenth historical interactive choice took place, or that the preserved nine redirects accepted sticker symbols.

The October 2026 source-graph scanner detects six unresolvable *link edges* in the pinned mirror. One is `DONE_SD.html`; the four numbered termination directories and `/sys/` comprise the others. **The two six-item lists are not equal**: the uploader enumerated missing **files**, including `dir/index.html` and two later shutdown-stage names that are not directed edges in the checked HTML; our six entries are outgoing **HTML navigation edges**, including directories already visible in April 2020 screenshot evidence. Keep these inventories separately typed.

This means the phrase **“newly discovered missing `DONE_SD.html`” was incorrect if understood as first knowledge by researchers**. October's genuinely new contribution is a reproducible, source-hash-pinned *complete link-graph census* that independently rediscovers a file already named in 2023. It is not a new-to-community filename.

## Versions and authenticity: eight important caveats

The same original upstream commit also says that eight supplied paths are **some version** (for example a text copy or archived rendering), **not original archival HTML**:

| Path or expected original name | What the uploader supplied or described |
| --- | --- |
| `comms_main_viewgate.html` | a version of the page |
| `sys/printreqstatus_005.html` | `sys/printreqstatus_005.txt` |
| `sys/printreqstatus_006.html` | `sys/printreqstatus_006.txt` |
| `sys/printreqstatus_008.html` | `sys/printreqstatus_008.txt` |
| `sys/printreqstatus_014.html` | `sys/printreqstatus_014.txt` |
| `sys/activate_shutdown_protocol/commit/___________DONE.html` | a version of the page |
| `dat/534brn9653f9j8mmd/index.html` | a version of the page |
| `sys/terminateall.html` | a version of the page |

This distinction changes the interpretation of our earlier **73/73 exact Git blob matches**. Those checks establish **byte-for-byte correspondence to the public *2023 uploaded mirror***, not correspondence to the original website's HTML at the time the ARG ran. We can say no HTML form controls appear in the *existing mirrored material*, but cannot extrapolate that null to missing originals, live server-side input, or archived outputs. This matters particularly for the printed Viewgate prompt and the damaged `534brn` payload.

A machine-readable source/limitation fixture is at [`data/terminal41-uploader-provenance-2026-10-16.json`](../../data/terminal41-uploader-provenance-2026-10-16.json); its offline checker, `python scripts/check_terminal41_uploader_provenance.py`, enforces six upstream missing files and eight version-limited paths against the 74-file manifest.

## Corrected conclusion and next action

The path `/sys/activate_shutdown_protocol/commit/___________DONE_SD.html` remains unpreserved, but it is a **known archival gap since 2023**, not a newly surfaced first-party clue. No sticker-specific operation, interface, text, image, or secret action can be inferred from these filenames alone.

Next non-sticker research should instead pursue (a) genuinely byte-original historical client/server assets from independently dated archives, (b) an original response whose semantics cannot be explained by the already-known printer/Terminal41 state, and (c) a source-authored instruction relating any of those inputs to foreground marks. The latest recovered [2018–2019 Playdead printer client](../experiment-483-original-printer-client-runtime.md) now materially advances item (a), although it is the **separate playdead.com site**, not the Terminal41 mirror.

No new stickers, owner searches, contacts or hypothetical missing data were used in this correction.

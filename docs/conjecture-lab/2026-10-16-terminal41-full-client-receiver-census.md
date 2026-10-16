# Full preserved Terminal41 client and scheme-progression audit (16 October 2026)

**Scope:** Existing-source, no-sticker-acquisition investigation continuing PX-12 / PX-M1 and Experiments 408, 478 and 480. **Research mode:** VALIDATE only for precise statements about this preserved snapshot; DEVELOP for any hypothetical lost server or CE-specific reader. **No decoded CE foreground or claimed new original website response.**

## Provenance and replay

This investigation treats the fixed `data/terminal41-source-tree.json` manifest as the complete *known mirror sampling frame*, not as a complete historical website. It records source repository `twinysam/INSIDE-ARG`, source tree `4de72d7c2f21bd9eb4144fda51281c84cbcb90c4`, and snapshot date 2026-09-29. The original manifest has **74 paths: 69 HTML files, four text files, and one binary PNG**. All **73 textual paths** are evaluated; the 19MB gate-98 PNG is explicitly excluded from the HTML-client test, not silently counted as source absence.

The [deterministic source census](../../scripts/audit_terminal41_complete_client_receivers.py) uses the Python standard library only. For every textual path it checks actual source bytes against the manifest's size and original Git blob SHA, then separately records real HTML form controls, script elements, inline event attributes, anchors, meta refreshes, literal input-like ASCII, textual references and working **links as distinct types**. The 17 status variants are additionally checked for actual `schem[n]` declarations and printed obtained/applied counts.

Reproduce from project root:

```
python scripts/audit_terminal41_complete_client_receivers.py --check --summary
python scripts/audit_terminal41_complete_client_receivers.py --json
```

**Evidence limit:** a local, source-matched HTML/text mirror may preserve accurately what a particular captured page displayed while omitting historic server-side PHP, cookies, query processing, POST routes, successful responses, different dated versions or hidden paths. A file not linked or present in the mirror is **not** evidence that its original route never existed. Printed prompts are not equivalent to HTML input widgets.

## Receiver-type distinction

The *original* Playdead website had a demonstrated **2018 browser print button** and conditional server POST interaction, as pinned in [Experiment 480](../experiment-480-original-print-transport.md). Contemporary accounts report `/print/prepare.php` and `/print/index.php`; saved JavaScript inserted successful returned content into `#print-content`, then called `window.print()`. Original server requests/responses and the 2018–2020 `/js/dist.js` bundle have **not** been recovered. That confirmed consumer is **not the same website** as the surviving `terminal41.link` mirror.

The two printed Viewgate `Input:[______________________]` surfaces each show **22 underscores** and contain no real HTML `form`, `input`, `textarea`, `select`, or `maxlength` control in those archived sources. This source-native negative was already established in Experiment 478; the full-source scanner generalizes the *inspection method* across the entire known Terminal41 snapshot.

A separate historical navigation idiom is explicit in `sys/terminate_terminal/41/terminate.html`:

```text
[terminate ermergency TERMINAL41][confirm(input)]
[/y/].[/n/]
```

This is a **printed path-based choice**, not a browser form in the archived HTML. The original 2020 community chronology reports `/sys/terminate_terminal/41/y/` as a reachable termination action, but its server response/path implementation is not in this 74-file snapshot. Consequently this is a real counterexample to the naive inference that *lack of a form rules out all historic URL-based interaction*. Neither a `/y/` choice nor an illustrated 22-slot prompt supplies an independently fixed **sticker-derived** command.

Likewise, HTML meta-refresh chains and ordinary `<a href>` directory listings are **navigation**, not fields accepting a proposed 9-, 27- or 108-character foreground input. The census reports them, separating captured destinations, uncaptured internal route references and external links.

## The 17 archived `printreqstatus` snapshots

Unlike a search confined to the final `_SD` page, these checks evaluate **all 17** preserved status variants, including the four `.txt` sources, for exact printed field values. The filename suffixes are snapshot labels, **not independently authenticated update times**. Direct source reads give the following progression in *file-suffix order*:

| Source variant(s) | Printed requirements obtained | Printed requirements applied |
|---|---:|---:|
| unnumbered, `_002`, `_003`, `_004`, `_005` | 0 | 0 |
| `_006` through `_012` | 1 | 1 |
| `_013`, `_014` | 2 | 2 |
| `_015`, `_016` | 3 | 3 |
| `_SD` | 4 | 4 |

The source family references indexed schemes **0–3 only**. Some individual versions omit an index (such as `_002` or `_014`), so no *individual* version should be presented as a full schema; the complete source family contains four named breach tracks `PLANET`, `LIFE`, `PROBE`, `CONDISCON`. There is **no fifth numbered `schem[4]`** in the preserved status progression.

**Interpretation:** This rules out a **fifth *ordinary numbered scheme in these 17 archived status texts***. It does not rule out an independently named fifth input, a later unpublished version, a new CE path, original backend special cases, or a different receiver entirely. The 0→4 story largely corroborates the earlier historical Game Detectives account; it is not a new independent server witness.

## An important archive-incompleteness control

April 2020 authenticated directory screenshots (already preserved in [CL-09](2026-10-08-terminal41-unarchived-route-recovery.md)) identify relevant **routes and directories missing from the 74-file mirror**, including the termination subdirectories `11/`, `23/`, `42/`, `99/`. The old directory listing itself has a server-looking `Last modified` column, but those timestamps are captured *page claims*, not independently verified file creation times. Existing image proof therefore prevents us from interpreting a link-missing result as a comprehensive search of all historic Terminal41 functionality.

The original `534brn` content also contains damaged JFIF-like text, not an HTML input control; treating it as an **artifact to read or repair** rather than a form to submit remains the sound source type. The independent `128 UNSOLVED` footer is meaningful, but Experiments 413–423 already establish that the surviving image bytes alone do not fix 128×128 or a sticker-indexed repair transform.

## New operational consequence

The next *non-sticker* work should target **input provenance rather than output resemblance**:

1. Recover original, explicitly dated 2018–2020 Playdead `/js/dist.js` or a successful `/print/index.php` response, including actual field names, transport type and any response-specific state. Do not send credential guesses to active endpoints.
2. Search **already archived historical HTML and preserved 2020 screenshots** for exact route commands, path/query/form shapes and downloadable source artifacts. Clearly mark gaps and unpreserved branches rather than asserting their inexistence.
3. Establish whether any **source-authenticated contemporary receiving contract** requires two/three glyph states, a 9/27/108-site mask, or a bounded operation. Only then test a previously frozen sticker projection, correcting for the number of alternatives examined.

**Stopping rule:** Do not infer a decoded CE output merely because a candidate resembles a route, checksum, 22-character field, PDF, directory, or printer code. Any static-client negative is scoped to captured files. This audit seeks no new stickers, owners or serials, and changes no physical observations, prediction registries or machine models.

## Disposition

The source-coverage and 17-version checks are reproducible; the historic positive controls, independent original server gaps, and status-family limitations are explicitly separated. **No foreground consumer is validated by this work.** Preserve this as a bounded closed-corpus receiver audit, then work on pre-existing historical source/binary recovery with source-hash and timestamp controls.

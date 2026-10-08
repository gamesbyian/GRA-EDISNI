# Destination-first follow-up: cover, damaged JPEG and Terminal 41 consumer audit

_8 October 2026. Companion to [destination portfolio](sticker-endgame-destination-investigation-2026-10-08.md). No raw sticker data or completion model modified._

## Outcome

The highest-value advance is a **negative consumer test with a historical-source correction**: the 74-path Terminal 41 mirror has 72 small text files and two large assets. All **72/72 text files** were read and screened for active client-side input surfaces, then the few apparent exceptions were inspected directly. None provides an HTML form, `<input>`, `<select>`, `<button>`, or POST handler. Two visually rendered `Input:[ ... ]` surfaces are literal textual placeholders, with **22 underscores** each. Forty-two pages are simple HTML meta refreshes. The sole JavaScript-bearing page, `sys/terminateall.html`, contains Google Analytics tracking, not a puzzle or authentication form.

This is a **strong limitation on a surviving client-side input consumer**, not a refutation of historically active Playdead backend endpoints, older unavailable page versions, or lost server responses. Source files are historical static captures rather than the original server implementation.

### Reproducibility and completeness

The source path census uses `data/terminal41-source-tree.json`, itself based on `twinysam/INSIDE-ARG` at a recorded 2026-09-29 snapshot. Per-path reads and flags are preserved verbatim as metadata (not copied source HTML) in:

- `data/endgame-interface-census-batch-00.json` (paths 0–17);
- `data/endgame-interface-census-batch-01.json` (18–35);
- `data/endgame-interface-census-batch-02.json` (36–53);
- `data/endgame-interface-census-batch-03.json` (54–71);
- `data/endgame-terminal41-interface-census-summary-2026-10-08.json` (overall counts and caveats).

All 72 individual fetches succeeded. Exclusions are the 19,360,240-byte gate-98 transmission PNG and 1,986,163-byte `dat/saf_dat_col.html` data payload. They are not described as inspected by this run. The scanner records simple HTML regex matches and is designed only to count literal page controls. JS implementations can hide dynamic DOM creation, so the sole script exception was manually reviewed.

## 1. Original mission/authentication system

### Four **explicitly labeled** schemes

The original status files show:

| Index | Printed breach tag | Source |
| --- | --- | --- |
| `schem[0]` | `PLANET` | `sys/printreqstatus_016.html`, `_SD.html` |
| `schem[1]` | `LIFE` | same |
| `schem[2]` | `PROBE` | same |
| `schem[3]` | `CONDISCON` | `_SD.html` |

The `_016` page leaves the fourth scheme at security failure while displaying the first three as breached; `printreqstatus_SD.html` labels all four breached and records print requirements obtained/applied = 4. The subsequent shutdown route has two consecutive redirect chains, including a set of nine `DONE_SD_CONFIRMED_09 ... _01` intermediary pages. Each intermediary is a fixed redirect without an input surface, as earlier Experiment 408 established.

The four-scheme arrangement is significant for endgame reasoning. It provides a **bounded original achievement system** and an **adversarial test for H3**: the stickers are from the later physical-CE phase, but this completed four-credential pipeline supplies no obvious fifth ordinary printer slot. A CE solution may continue after shutdown or interact with some different consumer; inventing an extra `schem[4]` is unjustified.

### Correction to an external research claim: the 22-character form

The vendored `archive/external/bigdusty/puzzles/viewgate-22char.md` (source `sashaok123/BigDusty_INSIDE_ARG_Map`) specifically describes a form with `maxlength=22`, and proposes the 22-character token `38546uy754j9j6tuk5fi34` from `saf_dat_col` as its input.

The actual available `terminal41.link/comms_main_viewgate.html` and `comms_main_viewgate_002.html` contain:

```text
Input:[ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ]
```

There are **22 underscores**, and **zero `<form>` tags, `<input>` tags or `maxlength` attributes**. The HTML page title is an emergency terminal status, not a form UI. This distinction is crucial:

- **supported:** the displayed terminal text has a 22-position placeholder; the reported candidate token is 22 characters long;
- **unsupported:** a preserved HTML text-entry control enforcing a 22-character maximum; proof the original site accepted the token;
- **still possible:** a now-lost backend or a different early live page had an input mechanism.

The external work remains a **candidate based on a real count coincidence** and an inaccessible/original blob assertion, not a confirmed recovered consumer. The content of the 1.99 MB `saf_dat_col` blob was not independently verified in this pass.

### Site terminator was not a password form

`sys/terminate_terminal/41/terminate.html` prints `[confirm(input)]` with `[/y/].[/n/]`. It contains no HTML form. `opts/confirm_shutdown_routine.html` redirects to a fixed commit path, and all nine `DONE_SD_CONFIRMED` steps are fixed redirects. `sys/terminateall.html` has a single Google Analytics `gtag` script, not an interactive puzzle handler.

Original printer-site `/print/index.php` POST behavior is a separate, independently established historical channel: a June 2018 contemporary Steam discussion documents POSTs to `prepare.php` and `index.php`, and the archived JS describes two-stage printing and answer validation. These are **not** mirrored as executable code in the static Terminal41 repository. It would be unsound to infer that the offline pages are evidence no interactive site ever existed.

### Causal/temporal issue

The status snapshots describe an already completed four-scheme break; the CE appeared in late 2019 and its background path was recognized in April 2020. Thus a sticker output that merely reproduces `LIFEDETECTED`, `NEWPLANETDISCOVERED`, `MULTIPLEPROBESDISPATCHED`, or `CONDISCON` would ordinarily be redundant in the original scheme. More plausible variants of the authentication hypothesis would require a **new after-shutdown stage**, a distinct key consumer, or a previously overlooked state not present in the 74-path mirror.

**Actionable reopening trigger:** an original archived form response, live screenshot showing an actual submit mechanism, original `print/index.php`/terminal protocol logic, or a client-server capture tying the 22-place display to real input.

## 2. Cover source-pair visual check

The previously documented Experiment 410 source pairs were re-opened directly as exact archived GitHub image blobs using their original paths. Their existence and content are no longer based solely on filenames in a prose description.

| Family | Archived cover crop blob | Archived comparison blob | Interpretation |
| --- | --- | --- | --- |
| Acorn | `assets/image-7be117e2c68d1b1e.png` | `assets/image-46edcfb62af0b550.png` | Both display a high-contrast abstract motif in a warm-colour monitor frame; cover crop is tiny, blurred, perspective distorted. |
| Planet | `assets/image-21b86ef8e34e269b.png` | `assets/wcil7mDWP1pLwAAAABJRU5ErkJggg-746d5444c3bdfeed.png` | Both present a round symbol/field, but the cover crop cannot validate an exact crop, orientation, or pixel transform. |
| Graph | `assets/image-d6d0d0f76ab751ca.png` | `assets/image-f443c3585a376c4f.png` | Comparison has a recognizable rising trend and orange plotting area; exact details in the tiny cover crop are insufficient to measure the transform. |
| Login | `assets/image-4484af09d4a602b3.png` | `assets/Sign_Screen_C_LoginWin-9052a6fc962e8024.png` | Monitor and source both show a horizontal orange bar in a rectangular frame; resemblance exists, exact geometry remains unproved. |

Additional physical cover photographs `assets/CxpDcJph-b2dd73639b37721f.jpg` and `assets/2GHkSP1h-7ff535c704c76102.jpg` were opened: they establish the scene and monitor/art placement, but are consumer photos (perspective/lighting confounders). The large `INSIDE_A-5d197786f158c567.JPG` blob was identifiable by SHA but returned an empty image payload through the image-fetch connector, so the 6552x5040 pair was **not** directly pixel-registered in this pass. Do not claim otherwise.

This confirms an actual **reference-board vocabulary** (puzzle images displayed on a physical cover) and refines what is missing. Perspective correction and canonical asset registration must precede any honest test for a repeated source-to-cover operation; inspection of low-resolution thumbnails cannot supply a pixel-level transform. The earlier Experiment 412 failure to find a recurring transform still stands. A decorative/reference-board explanation competes directly with a sticker-index explanation.

**Next physical test:** acquire high-resolution byte-level A/B scan locally with dependable provenance; isolate each monitor polygon; identify canonical game/printer source for each; estimate homographies using source *frames*, not sticker patterns; compute aligned residuals and cross-pair held-out matches. Reject comparisons that need arbitrary chosen masks to look meaningful.

## 3. `534brn...` damaged-JPEG endpoint

The `terminal41.link/dat/534brn9653f9j8mmd/index.html` mirrored page was directly inspected. It has an HTML envelope and damaged JPEG-like content under `<pre>`, an XMP fragment carrying `CreateDate 2016-12-16T14:12:24.351` and creator `AnSet`, and the distinctive `pe^!02un`/dots/footer plus `sys/ terminate terminal/ 41/ [conf.]` text. The source **has no HTML form, POST handler, or sticker-key placeholder**. The XMP date is editable asset metadata, not proof of the date Playdead authored the puzzle.

Earlier Experiments 413–423 are a decisive stopping boundary on naive restoration:

- the footer can be read as **128 UNSOLVED** by physical rotation;
- the JPEG's SOF dimensions each lie in **128..255** under the recorded corruption path;
- the decoded sampling implies 16x16-pixel MCUs;
- Experiment 423 found that **all 43** admissible total MCU counts satisfy the surviving entropy constraints, so the image dimensions/content remain underdetermined;
- the 128 clue is an interesting *native dimensional hint*, not validated 128x128 or a reversible damaged byte stream.

This audit finds no new interface accepting the sticker foreground. Therefore H1 remains strongest as an **identified next-stage asset** in the same CE chain, but **literal JPEG entropy repair using 108 sticker bits is especially weak** without independent storage redundancy or an intact copy. Possible alternate interpretations include the foreground selecting an already existing image/layer, selecting one of several externally recoverable artifacts, or identifying a transform applied to the corrupted page *as text*.

**Next exact test:** look for another independently preserved pre-corruption capture or reference with a controlled relation to the JPEG, not brute force of missing Huffman bits. Treat the alleged BigDusty 42x42 `Sleep` BMP via local mojibake reversal as a valuable but **unverified** reproducibility lead until its original bytes/scripts are available; do not conflate that other `saf_dat_col` file with proof about the damaged JPEG.

## Revised endgame rankings

1. **Cover as metapuzzle/reference or exact registration board:** known, explicitly clue-bearing physical artifact; highest feasible next *new cue* if high-res registration is recovered, although it may not consume stickers at all.
2. **CE-linked 534brn page as target of an external clue:** strongest direct pathway from solved sticker background to an unsolved web artifact, but no identified key ingress and a major corruption barrier.
3. **Compact sticker selector/index across an existing asset:** fits the 108-bit foreground upper bound and recurring cross-stage ARG practice; target and coordinate alignment missing.
4. **Original mission interface/credential or reboot state:** independently real designer precedent, but all 4 established scheme tags already breached and no new active form in the saved static mirror. Reframe as possible **post-shutdown** continuation, not re-entering known codes.
5. **Simple repeating image transform, known bunker code, existing nine-page countdown:** remain disfavoured/falsified by preceding experiments and current source-level control.

## Required future evidence and stopping gates

- **Cover**: exact perspective-registered comparisons across >=2 distinct source/monitor pairs with one source-first transform shared between them. Otherwise preserve it only as a reference clue, with zero numerical connection to the stickers.
- **JPEG**: a new intact capture, header/dimension registration independent of 128, source-equivalent media, or an explicit positional keying hint. Do not infer image pixels.
- **Mission interface**: historical client/server HTML or response with actual input structure, preserved backend protocol, or source-author statement specifying new credentials. Avoid interpreting printed underscores as submit controls.
- **22-char candidate**: independently verify the `saf_dat_col` token on source bytes and validate original HTML form/response; without both, no password claim.
- **Cross-puzzle test**: once an artifact independently fixes registration, test all physical-compatible sticker ensembles with null/shuffle controls. No semantic cherry-picking.

## Evidence/source links

- Archived original pages: https://github.com/twinysam/INSIDE-ARG/tree/master/terminal41.link
- Metadata/byte manifests: `data/terminal41-source-tree.json`, `data/discord-534brn-captures.json`
- Cover source images: https://github.com/gamesbyian/playdead-unofficial-exports/tree/master/assets
- Older in-repo tests: `docs/experiment-408-terminal41-nine-step-consumer-audit.md`, `docs/experiment-409-cover-operation-family-audit.md`, `docs/experiment-410-cover-monitor-source-inventory.md`, `docs/experiment-412-cover-repeated-transform-audit.md`, `docs/experiment-413-534brn-footer-128-unsolved.md`, `docs/experiment-423-534brn-mcu-constraint.md`
- Independently authored dossier requiring correction: `archive/external/bigdusty/puzzles/viewgate-22char.md`
- June 2018 printer form/POST contemporary account: https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=53

_No contact with owners or investigators was initiated. These are research findings; no claim of solved CE foreground or recovered missing JPEG image._


## 4. Chronology control: printer count versus website schema count

An important cross-check emerged from the [Game Detectives original 2018–2020 chronology](https://wiki.gamedetectives.net/w/Inside_ARG) and the archival status files.

- The four status labels `PLANET`, `LIFE`, `PROBE`, and `CONDISCON` correspond in subject to the original Xbox, PC/PS4, iOS and Switch printer branches. This is a compelling *architectural association*; precise per-submission site causation remains historically uncertain.
- The site reached the four-scheme shutdown state before the later CE URL recognition on 21 April 2020. The community chronology places the CE's physical arrival in December 2019, creating an overlap in which the stickers could have been designed to work with an already largely completed ARG website.
- The fifth platform's macOS printer messages emerged in June 2020, **after** the terminal shutdown. The [April 2026 code-level retail-binary audit](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) reports a fifth `SecretType.Cutout` enum value on macOS, but the developer code assertion has not been independently reproduced here.
- The community phrase `HIBERNATION IN PROGRESS REBOOT PENDING` therefore occupies a different historical *phase* than the four breached printer identities. Its exact decoding remains disputed, but the temporal ordering alone makes it unsafe to assume the stickers only encode another first-phase password.

**New endgame discriminator:** seek original post-shutdown links, physical-release follow-up media and macOS-era artifacts that define *continuation* grammar. An actual external consumer designed after the first four schemes would strengthen the mission-reboot hypothesis. No such consumer has yet been verified.

The published 2026 Chinese-language [MistARG chronology](https://www.mistarg.cn/topic/274/%E5%8F%91%E7%8E%B0-arg%E7%BC%96%E5%B9%B4%E5%8F%B2%E8%A1%A5%E5%85%A8%E8%AE%A1%E5%88%92-inside) independently assembles the same historical stage sequence, but explicitly cites Game Detectives and is a **derivative synthesis**, not an independent proof of Playdead's unpublished intentions.

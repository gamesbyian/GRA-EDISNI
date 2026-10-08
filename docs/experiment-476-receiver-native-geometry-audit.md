# Experiment 476: does the sticker foreground fit a native INSIDE ARG receiver?

_8 October 2026. Source-driven receiver census and fixed, deliberately permissive direct-format negative control. This is not a decoded sticker payload._

## Research question

Before translating dot/dash/slash into speculative letters, **which authentic physical, online, or in-game surfaces can plausibly receive the foreground**, rather than merely resemble a candidate output after fitting?

The strongest physical observations are the 108-period serial code, nine A–I background classes, 84 photographed/registered physical stickers covering 66 unique residue positions, and an apparent first-81 versus last-27 alphabet split. The potential receiver should be examined for a native **alphabet**, **geometry**, **choice/selection operation**, **entry point**, **chronology**, and **checkable response**. Matching one dimension is not equivalent to demonstrating a sender-to-receiver relationship.

## Finding 1: the Collector's Edition background itself is a strong destination link, but not an instruction for the foreground

The source-provenance audit in [Experiment 465](experiment-465-background-url-discovery-provenance.md) recovers a 2020 firsthand Discord account in which the nine faint printed background pieces were partially read, and the matching `dat/534brn9653f9j8mmd` path was then found through an Internet Archive site-map lookup. [Experiment 466](experiment-466-background-route-lookup-control.md) verifies the correct URL is an overwhelming nearest-string neighbor against a **retrospective**, answer-containing archive of 74 paths; this does not recreate the 2020 Wayback set.

**Direct observed chain:** CE 9 backgrounds → actual `534brn...` page. **Missing chain:** foreground → parameters/selector/index → exact part of the page → checkable next result.

The receiving page's historically preserved damaged JPEG/footer `128 UNSOLVED` supplies a **content target**, not a demonstrated 108-bit input field or error-correction schema. The sticker capacity, conditioned on the currently inferred two-symbol split, is at most 108 bits. It cannot be equated with an entire 128×128 raw monochrome image, which would require 16,384 independent bits. It *could* in principle select positions, a transform, a mask, or a reconstruction seed, but no such operation has been specified by the native source.

The original [`saf_dat_col` seven-field island](sticker-endgame-saf-dat-seven-field-audit-2026-10-08.md) contains an unambiguous **22-character** field adjacent to others, and the archived Viewgate displays **22 underscores**, but neither is a functional HTML form in preserved captures. A raw 108-bit-to-22-character packing alone cannot validate that token. The original printed four-scheme Terminal41 system was already in shutdown by the time of later macOS additions, limiting an ordinary fifth-password interpretation. Negative source search is constrained to surviving captures, not the original web backend.

**Status:** high-confidence *background-to-page* link; **low-confidence** *foreground-to-page reader*. Strongest local destination candidate, because it is the only named digital artifact physically linked from the **same sticker object**.

## A separate, independently verified receiver: Playdead's actual subscription-box-to-PDF system

Do not conflate the *Terminal41 mirrored status site*, where our surviving 73 static text files contain **no HTML forms**, with the **main Playdead website**. There really was a **functioning interactive submission pipeline** for printer puzzles on the latter. The independently published [Xbox Wire developer-facing account of 3 January 2019](https://news.xbox.com/en-us/2019/01/03/unsolved-secret-in-inside/) directly states that printer symbols were deciphered into text, entered into an ordinary email-subscription field on Playdead's website, and elicited a corrupted/noisy image in a **PDF**. The [Game Detectives chronology](https://wiki.gamedetectives.net/w/Inside_ARG) independently reports that the Xbox result `NEWPLANETDISCOVERED` was accepted there, with the iOS and PC/PS4 messages using the same overall mechanism.

This qualifies as a **real, historically demonstrated consumer type**: *arbitrary symbol carrier → short text → actual web intake → independently observable document response*. It solves the *existence* question for an ARG reader much more strongly than a hypothetical nine-input Terminal41 status page or merely printed Viewgate underscores.

But the January 2019 account explicitly concerns the **original game printer system**, before the December 2019 CE existed. It says that system was already solvable from the beginning. The form's current historical backend behavior, accepted phrase vocabulary, 2019–20 availability and any CE-specific extra acceptance state have **not** been recovered. The foreground's 108 binary-sector marks therefore cannot be presented as a validated new password simply because Playdead once accepted one. **A source-licensed plaintext readout and an independent CE-era response remain missing.**

**Most falsifiable receiver-oriented next step:** recover dated archived `playdead.com` **submission form / action endpoint** and the specific resulting PDF responses (including known **negative** submissions), with response metadata and contemporaneous accepted phrase inventory. First establish whether new answer classes or outstanding states existed when CE shipped; *then*, and only with a source-specified sticker readout, test whether the foreground produces a message that the historical receiver would have distinguished.

This route is **separate from the damaged `534brn` page** and its noninteractive preserved HTML. The two may be parts of a shared ARG progression but no source proves a sticker submission to either.

## Finding 2: the foreground is printer-like, but it is not three literal existing Xbox printer rows

The [source-fixture metadata](../data/printer-reference/metadata.json) establishes that the PC/PS4 printer has **32** separate 32-character full rows, while the Xbox printer has **35 unique 36-character full rows** and one duplicate used as the top/bottom of the original planet.

The H108 foreground has the right cardinality to form **three 36-character rows**, with original dot/dash/slash symbol types. That makes an Xbox-strip-shaped receiver an *economical geometric analogy*. But this is **not** equivalent to identifying a piece of the Xbox planet.

Experiment 476 freezes raw physical observations and compares each of the three consecutive 36-residue sections to **all 35 distinct Xbox full rows**, ignoring their unknown puzzle-specific solved row order, allowing any row to match any section, and allowing each Xbox row to be fully reversed independently. Question marks represent missing CE symbols and never count for or against a comparison. Source: `data/observations.csv`, `data/printer-reference/xbox-one-raw.txt`.

| CE section | Known/36 | Best conflicts, ordinary published Xbox orientation | Best conflicts, **allowing reverse** |
|---|---:|---:|---:|
| Residues **1–36** | **24** | **12** | **12** |
| Residues **37–72** | **23** | **10** | **9** |
| Residues **73–108** | **19** | **10** | **7** |

**No complete exact three-row reuse is possible even if all 42 currently unknown CE symbols are filled at will.** This is an actual, bounded *falsification*: each of the three sections conflicts with every candidate printer row at many **already observed physical** positions.

**What survives:** a three-line **overlay**, glyph reinterpretation, non-literal permutation, key/route selection or a different receiving printer sheet. That would require a source-specified registration and ideally the correctly ordered Xbox planet source grid. Applying shifts, permutations or colour legends until something looks like a picture would merely replace a closed simple test with unbounded multiple testing.

Reproduce with `python scripts/audit_native_printer_receiver_476.py --summary`. The script asserts 66 distinct physical residues, 35 unique Xbox 36-wide strips, 32 PC 32-wide strips, and exact forward/reversed mismatch bounds.

## Finding 3: the macOS `Cutout` is a historical *reader analogy*, not an independently verified CE continuation

The [original 2020 community research](https://github.com/twinysam/INSIDE-ARG) documents **16** macOS printer strips. The 16 literal printer lines contain exactly **34 dot marks**, and the published phrase `HIBERNATION IN PROGRESS REBOOT PENDING` also has **34 letters** excluding whitespace. This numerical agreement is real and reproducible from the [frozen original 16-line transcription](../data/experiment-476-macos-printer-control.json), but it does **not** reproduce the claimed E. E. Cummings poem overlay letter-for-letter.

An [April 2026 retail-code analysis](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) reports the macOS-only `SecretType.Cutout` enum arm in `PrintingPaperEasterEgg`, sixteen messages, solid/blank print materials and random unread-message selection. It **does not** report any in-engine poem decoder, and its author's attempts to reproduce simple overlay methods did not yield the published phrase. This analysis names binary classes and offsets, but this project has **not independently decompiled the retail macOS binary**. An externally performed poem operation would not need to live in the game engine.

The CE began shipping in December **2019** and macOS printer material was discovered in June **2020**. An intended CE-to-macOS continuation is chronologically possible only if Playdead planned the linked source, supplied a later instruction, or expected retrospective replay. No exact 108-symbol/16-line alignment or 34-character extraction rule has been found. The tempting `108=3×36` and `36−34=2` observations are merely cheap arithmetic; neither proves shared syntax.

**Status:** source-proven operation *style* (printer as physical encoding/overlay platform); **not** an independently registered foreground receiver.

## Finding 4: a previously underexplored nine-slot physical surface exists in the product

The publisher's [official Collector's Edition page](https://www.iam8bit.com/products/inside-collector-s-edition) documents an art-card set, fold-out poster and PlayStation 4 game. Its [publisher photograph](https://cdn.shopify.com/s/files/1/0580/0965/products/InsideCE_Lifestyle_00014_cf6a9295-f926-4f34-880f-2ddd6d75ce3d.jpg) **visibly presents nine separate creature/character concept sketches in approximately three rows by three columns**. Physical paper folds and printed illustration positions are a stronger coordinate prior than a grid invented on an unrelated image.

However the [standalone PS4 edition](https://www.iam8bit.com/products/inside-ps4-physical-game), which did not require ownership of the CE's distinctive numbered wrapper, independently advertises a fold-out poster. It is **not yet verified that both products have the exact same poster artwork**; nor does the currently available skewed publisher photograph establish labels, printed ordering, traceable A–I class registration, or instructions linking sticker foregrounds to these sketches.

**Bounded follow-up:** recover original high-resolution **unfolded front and back** poster print/photos; inspect authored folds, labels, tiny marginal text and orientation *without using sticker predictions*. Then use a source-defined A–I position correspondence and explicit transformation only if present. Nine marks alone are cardinality, not a consumer.

The [cross-edition cover audit](cover-cross-edition-dependency-audit-2026-10-08.md) supplies a further control: the reversible PS4 cover's ARG monitors are available to standalone owners too. The cover likely contains an independently consumable clue even without CE foreground stickers; a sticker overlay should not be assumed as its default explanation.

## A receiver map with typed edges

| Authentic source surface | Native structural evidence | Independent foreground connection | Biggest unlicensed leap | Verdict |
|---|---|---|---|---|
| **CE nine-background URL → `534brn` damaged page** | Same physical object already routes to exact ARG page, with unfinished image and `128 UNSOLVED` | **Object-level connection strong**, symbol-level unknown | How foreground selects/repairs/reads page | **Top target for source-fixed operation discovery** |
| **Playdead original website subscription→PDF** | Publisher-confirmed real form accepted earlier three printer passwords and returned corrupted-image PDF | No CE-authored plaintext mapping, CE-era response, or preserved endpoint behavior | Whether the CE was assigned a new accepted reply or already-solved system | **Real receiver type, CE-specific use entirely unproven** |
| **Xbox original printer/Braille** | Same three glyphs; 36-wide source strips; geometry/secondary layer historically validated | Alphabet + three-line width compatibility only | Original printed rows incompatible at ≥12/9/7 physical marks even after reversal; any overlay has no fixed registration | **Literal-row hypothesis closed; constrained overlay unlicensed** |
| **macOS `Cutout` printer** | Same message-bearing aesthetic; 16 strips; 34 dot marks with 34-letter claimed answer | No source-fixed foreground map | Time-separated release and disputed exact outside-game poem extraction | **Low, requires exact external reader** |
| **CE/standalone fold-out poster** | Official physical image visibly lays nine sketches in 3×3 | Same CE product ecosystem; nine-position grid only | No proven A–I coordinates, artwork equivalence, or instruction | **Worth original-print examination** |
| **Original SecretMap** | 2016 original asset witnesses, reported orb map; existing 14-orb control | No native texture bytes or CE-related reader | Target original texture and UV transform not in repo | **Blocked by original-byte acquisition** |
| **Reversible PS4 cover** | Independently advertised clue, four distinct monitor references | Same retail disc/edition family, no foreground alignment | Source-to-cover repeated transform not identified; standalone audience independent | **Investigate as self-contained clue first** |
| **Terminal41 22 underscores / SAF token** | Exact cardinality and authentic text island | No functioning saved form; no native raw 108-bit mapping | Original backend request semantics absent | **Bounded length coincidence, no intake gate** |
| **Already solved 14-command bunker lever** | Authentic three-choice input | Sticker shape legend historically proposed | Direct 108-cycle replay already excluded by symbol zones | **Specific direct reuse falsified** |

## A new design inference

The **strongest common Playdead ARG pattern is source-mediated, not direct substitution**. The original printer outputs often needed external row order, image geometry, password feedback, or another original artifact to become intelligible. The CE nine-background solution was actually **partly source-assisted**: April-2020 Wayback route discovery settled characters that remained ambiguous from the artwork (Experiment 465).

Thus the best live foreground model is not necessarily an English sentence hidden directly in 108 symbols. It could be a **sparse specification of how to use another already-present object**. But this is a **prior**, not evidence that our current POS3/4-cube machinery is the intended operation. The next productive task is to find a *real, independently authored input geometry and rule* in the damaged CE page or within genuinely CE-specific print artifacts.

**Distinct required breakthroughs**:
1. A **receiver**: an exact original artifact with an addressable surface, input slot, or source-native registration.
2. A **sticker-facing rule**: explicit physical, textual or historical link from CE foreground A–I/108 symbols to that surface.
3. An **output check**: recognizable, reproducible transformation/result not designed by inspecting the answer in advance.

The source-address/consumer for the historical Playdead printer form exists, but a CE-specific new accepted state and a foreground readout do not. For the physically co-located damaged page, the first two remain absent; that's the decisive research gap rather than another million model completions.

## Reproducibility and caveats

```bash
python scripts/audit_native_printer_receiver_476.py --summary
python scripts/audit_native_printer_receiver_476.py --output /tmp/experiment-476.json
```

Uses only saved physical sticker CSV, original printer reference strips and 16-macOS-line community transcription. Dedicated CI executes assertions and archives machine-readable output. **No new physical sticker, cipher key, platform binary decompilation, hidden-game input, image decode or validated external endpoint is claimed**.

The source printer row ordering is the order in a published raw reference fixture; the exact-row test is invariant under *which* row is used, but does not use reconstructed *spatial* Xbox order or possible shifted, transformed overlays. The MacOS source claims are not independently verified retail binary results. Official poster photo count comes from a perspective-skewed promotional image and remains a visual audit candidate.

# CE purchaser / receiving-surface audit: exact nine-bit classword pilot

*12 October 2026. DISCOVER / DEVELOP. No decoded sticker foreground, accepted code or new receiving mechanism is claimed.*

This is a receiver-first research experiment, not a constraint on the mystery. The working question is whether a collectively solved CE message could be **used** with assets ordinary buyers were given: packaging and print extras, physical PS4 INSIDE, Steam INSIDE/LIMBO, or the 2018-era web ARG. A buyer only received one sticker, so being able to *use a published solution* is different from being able to *collect the whole puzzle alone*.

## What purchasers actually had, and when

| Event | Evidence | Consumer implications |
| --- | --- | --- |
| March 6–8, 2018 preorder | Contemporary [Game Informer](https://gameinformer.com/b/news/archive/2018/03/06/whats-inside-the-375-inside-collectors-edition-box) and [PC Gamer](https://www.pcgamer.com/inside-collectors-edition-costs-375-and-contains-something-made-by-sex-doll-manufacturer-realdoll/) report a PS4 disc plus **INSIDE and LIMBO Steam keys emailed after purchase**. | Original preorder buyers potentially had PC game access well before the physical sticker. No evidence that these were special beta keys. Subsequent resales do not imply keys transfer. |
| June 4, 2018 website printer | [Game Detectives](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button) documents an input and print response. Existing [Experiment 480](experiment-480-original-print-transport.md) traces contemporary reports of two POST destinations, /print/prepare.php and /print/index.php. | A genuinely functional Playdead website text receiver existed. No original CE-era success response, fifth accepted category or preserved backend found. |
| November–December 2019 shipping | [November 25 owner discussion](https://www.reddit.com/r/PlaydeadsInside/comments/e1mdlm), [December 11 shipment announcement](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/), and [publisher contents](https://www.iam8bit.com/products/inside-collector-s-edition). | Physical sticker, reversible PS4 cover, poster, cards, figures, decorated box and disc entered circulation after the web printer ARG was already known. |
| Standalone PS4 edition | [iam8bit product](https://www.iam8bit.com/products/inside-ps4-physical-game) separately advertises 2,000 physical copies and a foldout poster. [Experiment 481](experiment-481-poster-cross-edition-gallery.md) notes reused promotional imagery. | A nine-sketch poster seen in CE advertising is not automatically a CE-exclusive reader; exact shipped poster equality and both reverse sides are unresolved. |
| PS4 title/disc identifiers | [GameFAQs](https://gamefaqs.gamespot.com/ps4/194097-inside/data) lists US digital CUSA-05297 and EU digital CUSA-02754, but **no CE physical product ID** in its CE row. [SerialStation](https://serialstation.com/titles/CUSA/05297) catalogs an INSIDE disc without establishing it is the CE disc. | Compare *actual* disc labels and original build manifests, instead of asserting the CE game uses an existing digital ID or a custom executable. |
| March–April 2020 sticker background solve | [Original community chronology](https://github.com/twinysam/INSIDE-ARG#9-piece-puzzle) documents the physical A–I background mosaic and April 21 association with the Terminal41 route dat/534brn9653f9j8mmd/. | Same physical sticker object demonstrably identified a web document. No proved foreground-to-JPEG operation or interactive form. |
| June 2020 macOS release | [Original chronology](https://github.com/twinysam/INSIDE-ARG#macos-printer-codes) dates additional Mac strips after the CE release. | A cross-platform continuation remains possible, but Mac strips cannot automatically be treated as a December 2019 purchaser's contemporaneous clue. |

**Source limitations:** archived website transport != surviving web backend; ordinary Steam entitlement != secret beta; physical PS4 disc != verified modified binary; standalone cover/poster similarity != identical shipped sheets. This audit neither elevates nor excludes any of those hypotheses. The [decoder/receiver atlas in PR #201](https://github.com/gamesbyian/GRA-EDISNI/pull/201) and [Steam investigations in PR #181](https://github.com/gamesbyian/GRA-EDISNI/pull/181) remain independent work.

## New exact classword experiment

**Source:** canonical data/observations.csv: 84 physical entries, 66 unique positions modulo 108, 54 body positions (1–81), 12 tail positions (82–108), zero conflicting repeated residues. The first 81 use slash/dash; the final 27 use slash/dot in the current physical observations.

1. **Unconditioned:** read each A–I class's nine body symbols in serial order, leaving '?' at each unobserved residue. To explore a concrete *typed receiver*, provisionally interpret slash=1 and dash=0 as a nine-bit unsigned integer. This conversion is an experimental convenience, not an author-supplied decoder.
2. **Conditional body grammar:** in each nine-cell serial frame, exactly one minority symbol appears in each interleaved triple (1,4,7), (2,5,8), (3,6,9), allowing **either slash or dash to be the minority independently per frame**. Enumerate 2×3³ frame possibilities before filtering on raw observations. The nine frame option counts are **1,1,2,1,1,3,3,1,1**; product **18** complete 81-cell bodies.
3. **Independent tail grammar:** within the last three occurrences of each class, assume exactly one slash and two dots; the current observed tail supports **18** completions. Together the conditional family contains 18×18 = **324** full 108-symbol strings, matching the simple family count in prior work. No recursive-machine assumptions are imported.

| Class | Direct known body symbols | Raw-compatible possibilities | Body-grammar address possibilities |
| --- | --- | --- | --- |
| A | 4/9 | 32 | 298, 302 |
| B | 8/9 | 2 | **382** |
| C | **9/9** | **1** | **58** |
| D | 5/9 | 16 | 147, 151, 155, 159, 211, 215, 219, 223 |
| E | 5/9 | 16 | 311, 319 |
| F | 7/9 | 4 | **407** |
| G | 4/9 | 32 | 305, 309, 313, 317, 369, 373, 377, 381 |
| H | 6/9 | 8 | **129** |
| I | 6/9 | 8 | 357, 365 |

Four words (B, C, F, H) are invariant **within this conditional 18-body grammar**. Only **class C** is wholly observed independently of the grammar, with body marks **---///-/-**, binary 000111010, decimal **58**. Invariant numeric value does not mean intended address.

### Bounded 128/256-domain incompatibility

Test all **18** compatible 81-cell bodies; then both fixed bit polarities and both whole-word directions. If *all nine complete nine-bit values* are supposed to be **unmodified direct indices** in a 128-entry or 256-entry table:

- **128 entries (7-bit)**: zero valid nine-address vectors under all four conventions. Each candidate has at least **six** out-of-range classes (some conventions eight or nine).
- **256 entries (8-bit)**: zero valid nine-address vectors under all four conventions. Each candidate has at least **three** out-of-range classes.
- **512 entries (9-bit)**: all 18 bodies fit, trivially, under every convention.

The 128-page footer's reported **128 UNSOLVED** text does *not* fix a 128-element address table or JPEG width/height. These exclusions say nothing about pixels in a 128×128 plane, modulo/wrapped addressing, selected subsets, 2D coordinates, shorter indices, different readout, compression, or another grammar. Source-native JPEG geometry is being studied separately in [PR #189](https://github.com/gamesbyian/GRA-EDISNI/pull/189).

### Control: is one directly complete class surprising?

As a deliberately simplistic null, uniformly choose 54 known locations among 81 body positions, ignoring the actual collector-acquisition process. An exact inclusion–exclusion calculation gives probability **0.1758864866** that at least one of nine disjoint nine-position classes is fully covered. The real sticker-survival mechanism is *not* uniform, so this is a modest caution against treating class C's completeness as special, not evidence against it.

## Next experiments driven by real receivers

1. **Recover original Playdead web client** (2018–20 dated dist.js and actual positive print-response bytes); establish the real accepted input grammar and historical state before testing candidate words. Revisit [Experiment 480](experiment-480-original-print-transport.md); no live password spraying.
2. **Compare CE and standalone PS4 retail versions** via photographed disc/internal IDs, publisher-disc data and dated build manifests. Source-documented delta first; analyze optional input/secret code only if real binary witnesses can be obtained. Existing offline reconnaissance: [game consumer pilot](consumer-binary-recon-pilot-2026-10-12.md).
3. **Inspect exact printed surfaces**: both sides of the two shipped poster variants, CE art-card set, reversible case and box varnish. Determine whether a native 3×3, nine-index or other read orientation is actually printed, without aligning to a hoped-for output.
4. **Test genuine indexed sources against invariant values** B=382, C=58, F=407, H=129 only if they possess a native 512-entry region and an author-supplied addressing convention. Replaying them on arbitrary pixel arrays would be post-selection. The related original damaged JPEG investigation is [PR #189](https://github.com/gamesbyian/GRA-EDISNI/pull/189).
5. **Keep the Steam branch research independent** in [PR #181](https://github.com/gamesbyian/GRA-EDISNI/pull/181); the existence of delivered Steam keys does not prove a concealed beta or acceptance of sticker output.

## Reproducibility

From repo root, Python standard library only:

    python scripts/audit_ce_classword_receivers.py
    python scripts/audit_ce_classword_receivers.py --output /tmp/ce-classword-audit.json

Canonical output: [data/ce-classword-receiver-domain-2026-10-12.json](../data/ce-classword-receiver-domain-2026-10-12.json). Program: [scripts/audit_ce_classword_receivers.py](../scripts/audit_ce_classword_receivers.py). The canonical observation file's Git blob SHA at inspection was **2bf9f1352c1632986e5c672b4832848fde1e6d0c**. Assertions deliberately fail on unexpected changes in corpus census, frame/tail completions or named invariants; newer confirmed stickers require an explicit re-audit, not silent automatic changes.

**Result:** a fully reproducible typed output census; four conditional nine-bit anchors and one unconditional anchor; an exact negative for two particularly simple address-space interpretations. No decoded text, working destination or CE-specific game input has been demonstrated.

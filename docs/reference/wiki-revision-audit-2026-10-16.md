# INSIDE/Playdead public wiki-revision audit: initial source-first fieldwork

**2026-10-16. Mode: DISCOVER.** Research hypothesis: a puzzle maker could place a concealed but publicly recoverable clue in an INSIDE wiki article, its revisions, talk pages, template parameters or image-upload records. Ordinary editing, fan theories, vandalism and rival ARG promotions are competing explanations. **This report supplies no evidence that Playdead has edited a wiki.**

## Primary-source findings

1. [Game Detectives old INSIDE ARG revision history](https://oldwiki.gamedetectives.net/index.php?title=Inside_ARG&action=history) is accessible and visibly lists **44 entries**, from **2018-07-04 03:31** to **2019-06-06 20:01**, ending at a 23,273-byte revision. Times as displayed, with no inference about editor location. This is **history-metadata coverage**, *not* a 44-diff/full-content audit.
2. **2018-11-16**: Editor Mayordoc added a video labelled *Doc's Invitation*, YouTube ID kdGIZPIKSos, and an external ARG invitation including “Hahahaha! Pirates! ARG!”. Three rapid edits, later reverted by Cdgoodwill on **2018-11-20**. [Contemporaneous diff](https://oldwiki.gamedetectives.net/index.php?diff=17942&oldid=17941&title=Inside_ARG).
3. **2018-11-23**: Editor AnonymousARG inserted an advertisement for *The_Vault*, with a claimed $10,000 prize and external Discord invite. Mattyb reverted it the same day. [Contemporaneous diff](https://oldwiki.gamedetectives.net/index.php?diff=17971&oldid=17949&title=Inside_ARG).
4. These are **positive controls for short-lived outsider ARG-related wiki edits**, not verified Playdead insertions. Their obvious self-promotion is a reason to discount an inference of Playdead authorship.
5. Representative ordinary maintenance: Thingy's **2019-05-10** edit removed a claim that a second printout appeared, calling it a **caching bug** ([diff](https://oldwiki.gamedetectives.net/index.php?diff=18870&oldid=17978&title=Inside_ARG)); later that day, the page described known Playdead website code submissions ([diff](https://oldwiki.gamedetectives.net/index.php?diff=18873&oldid=18872&title=Inside_ARG)); **2019-06-04** additions document existing gate-98 colour-overlap results and related Terminal41 paths ([diff](https://oldwiki.gamedetectives.net/index.php?diff=18936&oldid=18933&title=Inside_ARG)). These cases do not independently imply unusual activity.
6. [The INSIDE Fandom community wiki](https://inside.fandom.com/wiki/Inside_Wiki) advertises 23 articles, 66 files and 1,368 total edits, including [INSIDE ARG](https://inside.fandom.com/wiki/INSIDE_ARG). Its current articles were readable, but **revision history/API content could not be retrieved with the available browser tools**. No Fandom edit was audited in this pass.
7. [Wikipedia INSIDE](https://en.wikipedia.org/wiki/Inside_(video_game)), [Wikipedia Playdead](https://en.wikipedia.org/wiki/Playdead) and [PCGamingWiki INSIDE](https://www.pcgamingwiki.com/wiki/Inside) remain candidates, **with their revision bodies unharvested**. Retrieval failure is not an absence of clues.

**Result:** no independently attributable Playdead-authored wiki clue has been discovered. Two demonstrable outsider ARG-related historical insertions provide both an audit positive control and evidence that ARG-looking wiki text can arise from unrelated editors.

## Resolved apparent anomaly: nine removed ♻ annotations on iOS bitmap lines

A closer look at the [2019-06-03 Thingy revision 18924](https://oldwiki.gamedetectives.net/index.php?diff=18924&oldid=18923&title=Inside_ARG) reveals removal of exactly nine annotations appended to iOS printer glyph lines: `♻203, ♻206, ♻208, ♻205, ♻214, ♻206, ♻204, ♻208, ♻215`. These were **already present** in the [earliest article revision of 2018-07-04](https://oldwiki.gamedetectives.net/index.php?oldid=15953&title=Inside_ARG); the 2019 edit only cleaned them away.

The 24 glyphs spell the independently documented `MULTIPLEPROBESDISPATCHED`. Each mark is an **exact backward reference to the earlier occurrence of the same letter**: the numeric target minus 200 gives the previous character's 1-based ordinal. Explicitly:

| Current ordinal / letter | Annotation | Earlier ordinal / letter |
| --- | --- | --- |
| 7 / L | ♻203 | 3 / L |
| 9 / P | ♻206 | 6 / P |
| 13 / E | ♻208 | 8 / E |
| 16 / I | ♻205 | 5 / I |
| 17 / S | ♻214 | 14 / S |
| 18 / P | ♻206 | 6 / P |
| 20 / T | ♻204 | 4 / T |
| 23 / E | ♻208 | 8 / E |
| 24 / D | ♻215 | 15 / D |

The nine cited glyphs also reproduce the corresponding earlier bitmap shapes; the full first-source page displays all 24 lines. Thus **9/9 annotations have a simple repeat-lookup explanation**. This is no evidence of a hidden Playdead wiki edit; it is a source-traceable annotation of reused patterns (the significance of the initial 200-based numbering scheme is not independently established). The earliest page credits an external collaborative printer-code Google Doc for information in the article, but this alone does not prove which author or document first introduced these annotations. Recover historical Google Doc revisions only if further provenance is important.

**Methodological note:** this discovery was made by visual review *after* seeing the historical revision; it was not found by the predeclared automated anomaly scanner. A prospective detector for recycle-code syntax would be a post-hoc addition and should be scored separately from the frozen positive controls.

## Reproducible bounded auditor

A read-only, standard-library MediaWiki action-API tool is at [scripts/wiki_revision_audit.py](../../scripts/wiki_revision_audit.py), with [offline regression tests](../../tests/test_wiki_revision_audit.py) and [prioritized target registry](../../data/reference/wiki-revision-audit-targets-2026-10-16.json).

To run against an API from a network-enabled, rate-limit-respecting environment:

    python scripts/wiki_revision_audit.py \
      --endpoint https://oldwiki.gamedetectives.net/api.php \
      --title Inside_ARG \
      --max-revisions 1000 \
      --output wiki-inside-audit.json \
      --raw-output wiki-inside-revisions.json

    python -m unittest discover -s tests -p 'test_wiki_revision_audit.py'

**Execution status:** offline synthetic positive and negative tests passed during local development. **No complete real historical API harvest was executed.** The tool must be validated against the historical Game Detectives positive controls using real revision content before its detection recall can be asserted. Existing MediaWiki deployments differ in slot handling, access policies and API availability; fail closed rather than interpreting errors, caps, unexhausted cursors or blocked endpoints as zero findings.

Predeclared flags: additions of HTML comments, invisible/directional Unicode, new URLs, known ARG terms, and exact lines inserted then deleted within a configurable seven-day window. The first revision may generate many benign flags from baseline article content. Flagged text is a **review candidate**, not an ARG or authorship detection. The line-level diff loses some whitespace-only changes, so the second-stage pass must inspect raw byte/codepoint diffs and file-upload histories separately.

## Audit expansion order and controls

- **P0:** Harvest the complete Game Detectives INSIDE history and check the two 2018 edits. Preserve raw revisions and all cursor pagination data, bytes and hashes; record visible original page history separately from API completeness.
- **P0:** Attempt full INSIDE Fandom revisions and file histories, including the ARG page and major story/character/puzzle pages. Respect Fandom access restrictions; use approved public export/archives where available.
- **P1:** Wikipedia INSIDE and Playdead, their talk pages, and the relevant image histories. Run parallel controls on LIMBO pages and unrelated contemporaneous games.
- **P1:** PCGamingWiki INSIDE and LIMBO technical pages, preserving external-link redirects and revisions.
- **P2:** Non-English wiki editions and smaller wikis; choose by surviving 2016–2020 activity, not just modern page rank.
- **Controls:** At least two non-INSIDE Game Detectives ARG pages with similar dates and revision counts, and two unrelated game histories on the same platform. Measure short-lived links, vandalism and reversions. Include the two documented positives and non-ARG ordinary edits.

For any anomaly, store page, revision ID, date, source wikitext, neighboring revisions, exact addition/deletion, public file metadata and independent cue. Distinguish (a) source edit, (b) interpretive pattern, and (c) Playdead authorship. A username, odd edit timestamp, coincidental anagram or ARG-looking advertisement is not source attribution. Avoid contacting or attempting to identify pseudonymous wiki editors. If an operation emerges only after inspecting outcomes, label it **fitted/exploratory**, never a blind confirmation.

**Queue disposition:** maintain as a bounded, independent historical-evidence lane. Do not modify physical CE sticker observations or accept a new decoder from the current findings. Advance only on a source-linked anomaly or on a measured positive-control retrieval that closes the present coverage gap.

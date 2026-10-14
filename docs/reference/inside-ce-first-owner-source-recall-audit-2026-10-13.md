# First real-world CE owner-source recall audit (2026-10-13)

**Purpose:** Prevent already-known physical CEs being resurfaced as false new leads for Raezore when they appear through a different URL or historical platform. Use passive public posts only. **Do not contact owners or merge identities through inferred personal information.**

**Source of authority:** [community sticker list](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) (live at validation time), [Raezore search methods](https://github.com/twinysam/INSIDE-ARG/blob/master/raezores-research.md). **Machine-readable fixture:** [eight public source controls](../../data/reference/inside-ce-owner-source-recall-controls-2026-10-13.tsv). **Detector:** [same-platform public-handle crosscheck](../../scripts/crosscheck_inside_ce_public_handles.py). **Regression:** [four local tests](../../tests/test_inside_ce_public_handle_crosscheck.py) and [live canonical CI audit](../../.github/workflows/inside-ce-owner-recall-audit.yml).

## Public-search leads that initially looked new but are already canonical

1. **December 14, 2019, r/gamecollecting**: [“The INSIDE collector's edition finally came in!”](https://www.reddit.com/r/gamecollecting/comments/eaktdt/the_inside_collectors_edition_finally_came_in/) has an original arrival photo and first-person account by public Reddit poster **Knuckles316**. The post/thread URL is not literally in the canonical sticker file, but that handle is already documented as **lost L08**, with a different primary profile/source. The original photo is useful supplementary source provenance, **not a new sticker**. No legible sticker serial or symbol was established in this research.
2. **May 24, 2021, ResetEra**: [a side discussion about ARG postcards](https://www.resetera.com/threads/anyone-else-randomly-receive-black-and-green-postcards-that-are-art-of-an-arg-event-and-say-theyre-coming-likely-fortnite-related.430745/page-5) contains a CE purchase claim. Already reconciled to **-338**, user juxjuxjux, by Raezore in August 2026; URL already present in the canonical sticker entry. Not a lead.
3. **March 2026, Reddit resale discussion**: [several-months-later comment](https://www.reddit.com/r/PlaydeadsInside/comments/1l5x8rb/does_anyone_know_where_i_can_get_the_inside/) recounts a roughly $650 sealed CE acquisition. This is **Afaith_1**, canonically **L46**, lost sticker. It is not a new CE.
4. **June 2025 original sale / Reddit relisting**: [eBay item 376334499280](https://www.ebay.ca/itm/376334499280) and a later same-discussion seller account are already tied to sticker **470** in the canonical text. Reposts must not multiply physical CEs.
5. **July 2020, r/GameSale**: the seller's publicly documented handle **KoreanB_B_Q** is already the community's **U32**, so its listing URL cannot be treated as an additional unknown CE merely because our local research ledger used the discussion URL rather than the seller's profile.\n6. **September 22, 2026, r/oddheader**: [two sealed copies claimed](https://www.reddit.com/r/oddheader/comments/1wmvl0x/) by Shaxai are already canonical unknown **U47**. Neither numbered sticker is confirmed simply because the owner reported two copies.
7. **October 11, 2026, r/PlaydeadsInside art-book thread**: a lengthy first-person account of winning a sealed CE auction for **$400 and free shipping** is already flagged in our local lead ledger as part of the **/043** provenance discussion. It is not safe to promote this to a new physical copy; preserve the original commenter and transaction details for source-specific reconciliation rather than assuming another CE.

These examples identify a concrete false-novelty mode: *URLs missing from canonical notes do not imply owners missing from canonical notes*. Source URL, same-platform public handle, account transfer and physical object each have different identity rules.

## What the matcher proves and does not prove

The matcher extracts only **explicit public handles tied to a platform** from sticker entries: canonical Reddit profile links, typed `Reddit user X`, `Reddit comment from X`, `u/X`, public Twitter/X profile links, and typed `ResetEra user X`. It matches a new source's *explicitly supplied* public author against the **same platform**. It never links Reddit and X names because of similar spelling, guesses at real identities, scrapes follower lists, or infers that two posts document the same object.

A match is reported as `same_platform_handle_in_canonical_needs_review`, with possible existing sticker entries. That is a **triage warning only**. An unmatched alias is not proof of a fresh CE. An owner with two copies may still have multiple separate stickers. The extractor does not enumerate every prose nickname or editorial note in the sticker file; use Raezore's full list before reporting novelty.

## Verification fixture design

[Eight controls](../../data/reference/inside-ce-owner-source-recall-controls-2026-10-13.tsv) include six exact public known-handle outcomes, one historical source with no clear author attribution, and a pure announcement/no-purchase control. The CI workflow reads the current public canonical markdown via a read-only GitHub checkout, pins its SHA256 in output, and **fails** if expected known handles vanish or no longer match. It does not fetch individual Reddit comments, archived private posts, direct messages or any forum user profile.

Next: compare **actual search-provider retrieval** against these known controls, stratified into thread-only, reply-only, image-led and later-account alias leads. Treat a result as discoverable only when original *post text or media evidence* was actually returned, not when an exact URL was inserted into a test. Use this dataset to find previously missed evidence classes, then ship Raezore only independently sourced **unreconciled** leads.

**Current new confirmed physical sticker numbers from this audit: 0.**

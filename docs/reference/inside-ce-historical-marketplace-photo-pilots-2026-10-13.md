# CE marketplace image hunt, October 13, 2026: archival eBay and July GameSale results

**Research mode:** public-source-only DISCOVER; **physical observations added: 0**. This report brings together [PriceCharting archival-sale leads](inside-ce-pricecharting-historical-sale-leads-2026-10-13.md) and the [July 2020 GameSale archived sale](https://www.reddit.com/r/GameSale/comments/i0vgml/). All images and metadata were retrieved only from public sources with no accounts, seller outreach or paywall evasion.

## Exact historical eBay item IDs: no Wayback snapshot pointers

Source: [GitHub Actions run 38469912798](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38469912798) (one-off [PR #252](https://github.com/gamesbyian/GRA-EDISNI/pull/252), deliberately closed without merging the workflow). The canonical-item audit confirmed the previously reported **14 indexed sales = 7 source URLs absent by exact ID from the sticker ledger, 6 known canonical cases, 1 unrelated game**.

The public Internet Archive Availability API was queried at the secondary reported sale dates for **only seven** listed eBay IDs: `389713956842`, `294530200626`, `265253411400`, `136906990973`, `135573805762`, `335133327762` and `175640068701`. All seven responded with valid JSON and **`no-snapshot-advertised`**, each preserving the response SHA-256 in the 30-day Actions artifact. No source snapshot HTML or photos were retrieved. This is a negative nearest-snapshot API result, not a full Wayback CDX inventory, not proof the photos never existed, and not a contradiction of PriceCharting's historical dates.

**Actionable discovery lead status:** seven authentic indexed *item URL references* requiring original listing-media or independent source cross-checks. The two late-2025 / early-2026 entries share nearly identical titles and might be one relist. Never present these as seven copies.

## July 2020 long GameSale post: newly recovered unrelated Imgur photographs

- Original public [post `i0vgml`](https://www.reddit.com/r/GameSale/comments/i0vgml/), published **2020-07-30**, sells a broad mixed gaming collection. [One-run source probe](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38470221667), [artifact](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38470221667/artifacts/11850774031), reproduced a CE-specific excerpt around **body character offset 466**: *“Inside Collector's Edition”* and accompanying iam8bit / RealDoll Huddle description. This is credible **2020 CE resale text**, yet does not identify a numbered seal or a distinct physical owner versus U/L.
- Public [reply `fzw1kzj`](https://www.reddit.com/comments/i0vgml/_/fzw1kzj/) published **2020-07-31** links [Imgur album `p48PIzb`](https://imgur.com/a/p48PIzb). The thread's retrieved Arctic Shift comment tree contained nine comments and precisely one gallery link, archive SHA256 `2ae754d7353c87e8b5335be31ace5d1a4557841d9f56c22c862dee2466bc58ce`.
- Original media retrieval: [one-shot PR #254](https://github.com/gamesbyian/GRA-EDISNI/pull/254), [GitHub Actions 38470431101](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38470431101), 30-day original ZIP [artifact 11851397819](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38470431101/artifacts/11851397819). Public `gallery-dl` successfully fetched **12 original JPEG photographs**, filename order 001–012 and original gallery sidecar metadata, at either 2048×1536 or 1536×2048. Each photo is preserved, not merely a search thumbnail.
- **Manual visual examination of all twelve originals:** four unrelated PlayStation 2 games, each photographed as cover, opened case/disc, and back of disc: **Castlevania: Curse of Darkness**, **Ring of Red**, **Genji: Dawn of the Samurai**, **Obscure: The Aftermath**. **None** depicts the INSIDE CE, its Huddle, PS4 game sticker, a numbered white seal, or any new relevant physical object. The album is a **false-positive attachment in a general sale thread**. Gallery-link proximity to the phrase INSIDE in the post cannot associate this reply's media with INSIDE.
- Reference hashes sampled from original source bytes: image 001 `JkHcTlj`, SHA256 `2d95c1279c026d52582c59a865632b5e8f42d1c9e446c2a2d02dbfe923d0778e`; image 012 `oblXw9x`, SHA256 `a7aaf1b661e6cd3460a91a8f9c7e17a2b90a2a3a8134e33874f730f69634d076`. All twelve media files are preserved in the Actions archive for independent review.
- **Pipeline issue:** after correct retrieval, the reusable gallery validator rejected a legitimate `https://imgur.com/a/p48PIzb` URL because it permitted only `https://imgur.com/gallery/<id>`. Therefore **automatic visual comparison did not execute in that particular pilot**; the negative conclusion rests on actual manual visual inspection of the original twelve photos, not a claimed successful hash-comparison step. A dedicated tested fix now accepts the original exact `/a/<id>` form while retaining strict media and source provenance checks. The original photo bytes were preserved despite the failed indexing step.

## Lessons for future owner-photo search

1. **Mine archived replies and original album attachments**, not just post titles. The July album was invisible to the original post-metadata search.
2. **Verify the reply's object context independently**. A sale thread with an INSIDE CE can attach photos of PS2 games unrelated to the CE; otherwise visual systems will overcount ownership candidates.
3. **Keep known source duplicates separate from unresolved exact IDs**. The September GameSale postings were later reconciled to canonical U32; the 2025 eBay /223, 2022 L33, 2025 -444, 2023 L36, 2021 U23 and 2021 /333 sales had already been included by the sticker community.
4. **Do not use archive unavailability as proof of physical-media absence**. A failed paid-photo lookup or an empty Wayback nearest-snapshot response is an acquisition limitation.

### Outcome

**New source trails:** seven indexed historical eBay listing URLs and one historical July 2020 seller-related photo album. **Novel original INSIDE sticker photos: 0. Novel serial numbers: 0. Novel physical CE cases confirmed: 0.**

**For raezores:** The seven eBay item links are worth checking against personal/Discord seller research as a compact, properly qualified **source-lead batch**, especially the 2021 and 2023 entries. The July Imgur album should **not** be forwarded as an INSIDE sticker photo, although the actual July CE sale statement remains an unreconciled text-only lead.

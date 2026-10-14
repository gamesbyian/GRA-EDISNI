# October 2026 $400 INSIDE CE auction: original photograph recovery audit

**Investigation:** October 13, 2026 local (GitHub Actions execution October 14 UTC). **Original public acquisition claim:** [Reddit comment `pf7wee4`](https://www.reddit.com/comments/1vdbrus/_/pf7wee4/) by `Leading_Highlight553`, published October 11, 2026 at 10:52:15 UTC. **Status:** exact auction item number **not found**, original eBay photos **not recovered**, no newly proved physical CE or numbered sticker. This is a record of actual source access and unsuccessful retrieval, **not evidence that the October sale didn't occur**.

## Full primary source recovered, not just opening excerpt

One [bounded exact-post/comment recovery run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38494075387) retrieved the original **4,603-character** public statement, SHA256 `f72d3eef5cbb8afbcc6b4acedfc3951bf7bdf0260f4e7060392460412a200149`. The returned 14-comment thread was not flagged as partial.

New information from the *full* comment, beyond the previously logged 1,900-character excerpt:

- Buyer noticed an **eBay auction approximately one week before** posting October 11 (roughly October 4, date uncertain), beginning at **$400 with free shipping**.
- They report dozens of watchers and hundreds of page views. The buyer placed a high maximum bid using incremental bidding, but reports **no rival bidder**, so they won at **$400**.
- They also describe a separate September CE sale of about **$380**, apparently approximately three days after their birthday, date unknown.
- The original buyer comment contains **zero outbound URLs and zero 12-digit eBay item numbers**. No immediate comment replies were present in the retrieved archived thread. No seller images, listing title, seller name, receipt, numbered game wrapping or sticker image appear.

These are credible observations of **what the commenter said**, not independent verification of the marketplace's underlying auction record, successful delivery or a new physical CE. The longer text narrows the *auction appearance* window but does not establish an exact closing time.

## Four public marketplace searches: access versus relevance

[Bounded live GHA run 38493783965](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38493783965) executed four public HTML requests, each limited to two MiB and 20 seconds. Attempts targeted eBay's *sold/completed* search for `INSIDE iam8bit collector edition`, `INSIDE Playdead Huddle` and an auction-only variant; all **three returned HTTP 403**. Thus *nothing* about the number of October sold items can be inferred from eBay search here.

PicClick's public `?q=INSIDE+iam8bit+collector+edition` search returned **HTTP 200**, page SHA256 `6635b4a68cca8e10eb80d3bc268712cae3eec44c663f6d8d17a568aa453ff0cf`, but did not yield qualifying **full Huddle CE** listing matches. A second [search-layout diagnostic run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38493910633) tested three different term combinations. `inside realdoll` produced unrelated Real Littles dolls and clothing; `INSIDE collector's edition` was dominated by unrelated books/movies/other games; `inside iam8bit` returned two **PS4-disc-only-looking** listings by title:

- [PicClick 147632657006](https://picclick.com/INSIDE-Sony-PlayStation-4-iam8bit-Exclusive-147632657006.html), title: “INSIDE (Sony PlayStation 4) - iam8bit Exclusive - Brand New & Factory Sealed!”
- [PicClick 157829305544](https://picclick.com/Inside-PS4-Limited-Special-Edition-iam8bit-RARE-one-157829305544.html), title: “Inside (PS4) Limited Special Edition iam8bit (RARE one of 2000 copies worldwide)”.

Those titles appear to describe the **PS4 physical game**, not the giant Huddle CE box; their original media were not independently visually verified. The claim of “2,000 copies” relates to the PS4 physical edition; it must not be used as a proven sticker-serial/collector-box count. Neither resembles an auction for a full sealed CE at $400.

### Historical PicClick item-ID resolution experiment

A further [four-item pilot](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38494287559) tried rendering exact original eBay IDs as direct PicClick page paths with a generic surrogate title, using two *existing known* source controls (`257753799919` → /047 and `297682348686` → /223), plus two of the seven old PriceCharting unknown links (`389713956842`, `335133327762`). **All four yielded HTTP 403.** A noncanonical slug may be refused, or PicClick detail pages may block these requests; because even the controls failed, this experiment cannot make a meaningful claim that the historical sale/photo archives are missing.

**Conclusion:** PicClick search is publicly reachable, but neither its active results nor an arbitrary-slug item-ID probe has yet recovered the particular **October 2026 sold auction** or any of our historic missing seller photos.

## September $380 comment versus existing /047 listing: hypothesis only

The already-known [eBay item 257753799919](https://www.ebay.com/itm/257753799919), listed in September 2026, asked **$375 plus $13.99 shipping**, and the [community ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) assigns its physical numbered sticker **/047**, original known owner/alias `Uglord`/Tricky. Its date and price are near the buyer's secondhand “September ~$380” account. This is worth a **single existing-case reconciliation question**, but there is **no evidence** that the /047 *asking-price listing* sold, that it is the $380 reported transaction, or that the October $400 auction is related. Keep separate cases until exact eBay ID, closing status or photographs establish the connection.

## What would turn this into a stronger lead

A public **original eBay item ID or seller listing screenshot** for an early-October auction of unopened full CE at $400, preferably showing the wrapped PS4 game and white serialized seal, would permit the existing 82-photo canonical sticker matcher to distinguish new visual evidence from another resale of known serials. Public search-engine indexing may catch up in future, but repeated HTTP 403 eBay direct scraping, noisy active PicClick searches, and overloaded Arctic Shift keyword requests are not appropriate substitutes for a genuine original link.

The [machine-readable recovery audit](../../data/reference/inside-ce-oct2026-public-auction-media-recovery-audit.json) records source URL, exact full-comment digest, search page SHA values, all HTTP statuses, the two non-CE PicClick hits and the unproven September /047 near-match.

**Outcome:** full original buyer comment verified; **0 original October auction eBay item numbers**, **0 actual seller photo bytes**, **0 newly confirmed sticker numbers**, **0 additional physical CE cases proved**. Do not contact any buyer or seller based on this report.

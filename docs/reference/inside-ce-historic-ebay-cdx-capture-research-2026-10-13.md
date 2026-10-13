# Historical INSIDE CE resale listing photos: capture-index recovery lane

**2026-10-13.** Research mode: public original source IDs, archive metadata and photographic provenance, with **no inferred additional owners or stickers**.

The first bounded [Wayback Availability API pilot](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38469912798) returned no closest snapshot pointer for any of the seven eBay item IDs absent by exact match from the sticker ledger. This is **not** an exhaustive capture search. The user-facing marketplace report and original source IDs are in [the PriceCharting sale-ledger audit](inside-ce-pricecharting-historical-sale-leads-2026-10-13.md).

The Internet Archive's [public CDX Server API documentation](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md) describes a second, independent capture-index method. Its `matchType=prefix` permits alternate query strings and URLs beginning with the exact item permalink. Unlike single “closest” lookups, it can enumerate archived capture timestamps, original URL, HTTP status, MIME type and archive digest.

## What this changes

The new [CDX exact-item probe](../../scripts/external_evidence/probe_ce_ebay_cdx.py) issues **no more than seven** item-scoped public CDX requests by default, throttled to one every two seconds. Each request asks for up to 24 HTML-success index records beginning with `www.ebay.com/itm/<12-digit-ID>`; the response is capped at 512 KiB. Each reported capture must independently match an **exact 12-digit item ID on an eBay `/itm/` URL**. The parser rejects a different ID with the same prefix, spurious storefront/product URLs, wrong hosts, invalid timestamps, redirects, non-HTML media and non-200 statuses.

The probe preserves each response SHA-256, original eBay permalink, capture timestamp, digest, status and replay URL. CDX 403/429/503 stops later requests; 429 retry-after is retained. The manually runnable CE visual workflow has the separate opt-in `historical_ebay_cdx_check` flag, avoiding recurring network requests or CI cost. Offline regression tests include intentionally misleading URLs, malformed CDX JSON, duplicate captures and a simulated HTTP 429.

**Interpretation boundary:** a CDX capture URL is a *pointer* to a possible historical page, not verified original HTML, photograph, Playdead CE, physical seller, sticker or previously unseen serial. Original photos must be retrieved and visually reviewed through the existing evidence/media pipeline before any observation is proposed.

## If the index returns no items

Record whether each source genuinely returned an empty CDX header or failed to execute. Neither is evidence that all relevant captures are lost. Exact-number eBay links with an SEO slug preceding the item ID may not be discoverable via this narrow numeric-path prefix; a search/index query on other prefixes or independent public sale mirrors is a separate later experiment. Broad all-eBay-host CDX sweeps should not be attempted for seven IDs, since they are computationally enormous.

## Related publicly documented recovery methods

Public reseller-data archival sources sometimes provide original media identifiers, but may be subscription services. During research, [WorthPoint](https://www.worthpoint.com/) and [PicClick](https://picclick.com/) were identified as possible categories of third-party image archives; no claim of coverage for these exact IDs has been established. User-facing historical-sale images behind PriceCharting's paid Time Warp remain explicitly outside the public retrieval lane. eBay's [original-listing view help](https://kb.sellerchamp.com/en/articles/3439760-view-original-listing-using-ebay-item-id) is useful for fresh items, but the seven historical listings did not yield accessible old photos through the public search tools used here.

The practical proof target is an **exact original listing image URL with source-page attribution**. Until such bytes are retrieved, the seven remain seven potentially duplicate historical sale-source URLs, **not seven previously unrecorded physical editions**.

# INSIDE CE public completed-sale indices: seven source URLs not in original ledger

**Date:** 2026-10-13. **Research mode:** public historical-sale discovery. This report contains *original URL leads only*, not independent photographs, CE-owner identifications, missing stickers, or inferred physical edition counts.

## Primary public third-party index

[PriceCharting PS4 INSIDE Collector's Edition](https://www.pricecharting.com/game/playstation-4/inside-collector%27s-edition) publicly displays 14 completed eBay sale rows, including dates, titles and original outbound eBay item links. PriceCharting's **Time Warp original sale photographs require a paid subscription**; we did not obtain or infer those photographs. Their public metadata are independent of physical CE sticker visibility. A few sale titles are misclassified, including one completely unrelated `Ni no Kuni II` listing.

We collected the **14 exact item IDs** from the public table's outbound eBay links, stripped affiliate query strings, and checked exact 12-digit IDs against the community [canonical sticker ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md), not just broad web searches. Static source in [sale-index manifest](../../data/reference/inside-ce-public-historic-ebay-sale-index.json); deterministic full comparison in [audit_historic_ebay_ce_sales.py](../../scripts/external_evidence/audit_historic_ebay_ce_sales.py).

### Seven original eBay listing URL leads, not previously seen as exact item IDs in sticker ledger

| Public completed sale date* | eBay item ID (original listing) | Title gist |
|---|---|---|
| 2026-03-09 | [389713956842](https://www.ebay.com/itm/389713956842) | Inside CE, iam8bit, rare PS4 |
| 2026-01-03 | [136906990973](https://www.ebay.com/itm/136906990973) | Brand-new full CE with statue |
| 2025-12-31 | [135573805762](https://www.ebay.com/itm/135573805762) | Identical title to January 3; **possible relist of same CE** |
| 2023-11-30 | [335133327762](https://www.ebay.com/itm/335133327762) | iam8bit CE, brand new and complete |
| 2023-03-12 | [175640068701](https://www.ebay.com/itm/175640068701) | Brand-new original shipping packaging |
| 2021-11-15 | [294530200626](https://www.ebay.com/itm/294530200626) | CE + RealDoll, mint condition |
| 2021-09-14 | [265253411400](https://www.ebay.com/itm/265253411400) | Complete-in-box CE |

*Dates reflect PriceCharting's **secondary** eBay completed-sale table, not verified original listing capture timestamps. These item IDs' absence from the specific canonical `stickers.md` does NOT mean Raezores hasn't seen them elsewhere or that their physical copies aren't part of a known U/L or transferred serial.*

### Six eBay IDs already present in community ledger, a strong duplicate-control result

- [297682348686](https://www.ebay.com/itm/297682348686): known **/223**, Oct 2025.
- [144512270828](https://www.ebay.com/itm/144512270828): known **L33 (formerly U25)**, April 2022.
- [205387386884](https://www.ebay.com/itm/205387386884): known **-444**, April 2025.
- [304810014858](https://www.ebay.com/itm/304810014858): known **L36 (formerly U30)**, Feb 2023.
- [224665135284](https://www.ebay.com/itm/224665135284): known **U23**, Nov 2021.
- [154592369029](https://www.ebay.com/itm/154592369029): known **/333**, Sep 2021.

The **14th row** is unrelated *Ni no Kuni II* eBay [196542141679](https://www.ebay.com/itm/196542141679), and is excluded.

## Visibility and verification limits

Search-engine exact-ID queries returned **no independently indexed pages** for these seven IDs during this pass. Fetching original eBay page links through available public browser search produced restricted-URL failures, so actual item photos **have not been inspected**. Absence from the community ledger is only an initial research lead. No new serial, sticker, physical copy or owner is claimed.

Reconciliation priorities: check dated crossposts/transfer chains and current community U/L rows; prioritize any historically preserved images of the numbered PS4 wrapping, not a promotional image or a product-identical standalone PS4 copy. The two late-2025/early-2026 new-in-box entries with the same title might be one relist. Do not contact sellers or extract personal accounts.

## Archival path

[probe_ce_ebay_wayback.py](../../scripts/external_evidence/probe_ce_ebay_wayback.py) checks only Wayback Machine's [official public Availability API](https://archive.org/wayback/available), passing an exact listing URL and requested date. It respects slow requests and HTTP 429/503, stores snapshot pointers only and does **not** fetch image bytes, bypass subscription photo features or claim stickers. A snapshot pointer is an avenue for *later* original-media investigation; it is not itself photographic evidence.

Possible follow-up: seek independently archived original public listing photographs through web mirrors, auction aggregator snapshots, item-id public images, or Wayback captures, comparing every retrieved image against 82 original sticker photos and publisher controls. If archive API says no closest snapshot, that is an absent API pointer, **not proof an image never existed**.

**Current priority for raezores:** these seven eBay item IDs form a useful *unreconciled historical URL lead batch* once their validity and relationship to existing ownership/serial entries are explained. Do not send as seven new owners, or as newly read serials.

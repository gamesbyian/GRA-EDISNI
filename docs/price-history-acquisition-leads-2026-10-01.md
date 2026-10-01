# Price-history acquisition leads — 1 Oct 2026

## Why this pass

Experiment 359 moved the sticker project away from blind closed-corpus widening and toward genuinely new physical observations. Completed-sale history is useful because it can expose Collector's Editions that changed hands without ever entering the community sticker ledger.

This pass cross-checks the public PriceCharting sale history against the upstream `twinysam/INSIDE-ARG` sticker ledger before promoting anything.

## Reconciled sales

Two recent completed-sale records line up exactly with already-known stickers:

- **14 Oct 2025**, eBay item **297682348686**, `Iam8bit Inside collectors edition PS4`, $450. This is already upstream sticker **223**, discovered from the same eBay item on 14 Oct 2025.
- **9 Mar 2026**, eBay item **389713956842**, `Inside Collector’s Edition Iam8bit Rare PS4 PlayStation 4`, $735.25. This sale date matches upstream sticker **445**, discovered from eBay on 9 Mar 2026. The current upstream entry points to an archived listing rather than this PriceCharting item id, so treat the identity as highly likely but verify from images/provenance before declaring the item number canonical.

These are not new physical observations.

## Two unregistered completed-sale leads

PriceCharting exposes the underlying eBay item IDs even though the completed listings themselves no longer render through the ordinary eBay cache:

1. **31 Dec 2025** — eBay item **135573805762**
   - title: `INSIDE - iam8bit Collector's Edition - PS4 Game - Statue - Playdead - Brand New`
   - recorded sale price: **$1,600**
2. **3 Jan 2026** — eBay item **136906990973**
   - title: identical to the above
   - recorded sale price: **$1,600**

Neither item number appears in the current upstream sticker ledger or in GRA-EDISNI.

The two distinct eBay item IDs and separate completed-sale dates make these worth preserving as acquisition leads. They may represent two separate sealed Collector's Editions, two listings from one seller with multiple copies, or a relist/retransaction. Do **not** count them as two independent CEs until seller/photos/provenance distinguish them.

## Acquisition value

If either sale can be connected to a current owner, it is unusually promising:

- both were advertised as **Brand New**;
- the sticker is attached to the paper wrapping around the physical game within the Collector's Edition rather than requiring the Huddle itself to be unsealed;
- a buyer who retained the package may still have an intact sticker;
- the dates are recent enough that seller/buyer traces may still survive in marketplace caches, feedback pages, collector posts, or image mirrors.

## Next actions

Search by the exact eBay IDs first. Do not use broad seller outreach until identity is established.

For each item:

1. recover any cached listing image, seller handle, location, or feedback trace;
2. compare package photos against all known 2025–2026 listings to detect relists;
3. check whether either item is the source of an existing U-code or known sticker under a different listing id;
4. if a current owner becomes identifiable, hand the lead to the existing community acquisition lane rather than duplicating contact;
5. if photos expose the numbered sticker directly, record it as a physical observation and run the frozen discriminator tests before changing any model.

## Epistemic status

These are **acquisition leads, not sticker data**. Their value is that they point to recent physical copies outside the registered corpus.

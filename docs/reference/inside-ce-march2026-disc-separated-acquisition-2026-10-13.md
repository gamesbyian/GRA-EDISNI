> **16 October reconciliation:** This original-source report remains historically valid, but its novelty/outreach conclusion is **superseded**. The upstream [canonical lost L46 entry](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) explicitly names `Afaith_1`; the commenter confirmed the sticker was lost on 22 September 2026. The suggested disc-wrapper separation is unverified and cannot overturn this known case. [Corrected packet](inside-ce-raezores-public-lead-handoff-2026-10-13.md).

# INSIDE CE public March 2026 split-sale lead: buyer reportedly did not receive PS4 game

**Source-first discovery:** October 13, 2026. **Original comment published:** **2026-03-08 05:32:21 UTC**. **Review class:** potentially *previously unlisted public CE acquisition*, not a confirmed new serial or an additional physical copy. **Owner outreach:** none.

## The original evidence

- Original public Reddit [comment `o99qxpo`](https://www.reddit.com/r/PlaydeadsInside/comments/1l5x8rb/comment/o99qxpo/) from [June 2025 INSIDE CE availability discussion `1l5x8rb`](https://www.reddit.com/r/PlaydeadsInside/comments/1l5x8rb/). Public comment author: `Afaith_1`.
- The writer reports obtaining a **sealed INSIDE Collector's Edition** for approximately **$650** from a resale seller, negotiating a lower price because **the seller apparently retained the PS4 physical game**; the writer plays on Xbox and did not need a PS4 game. Their wording is ambiguous about exactly which side retained the disc, but the pricing/console explanation supports *game removed from this particular resale*.
- The quoted source passage, with trailing original phrasing preserved in the [machine-readable source lead](../../data/reference/inside-ce-2026-disc-retained-acquisition-leads.json), says **“I found a seller with a sealed box and was able to negotiate the keeping the physical disc ... the seller reduced the price and I was able to get a sealed collectors edition for around $650”**. This is a *self-report*, not an invoice, photo, direct owner confirmation or receipt.
- [Actions source verification 38491175914](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38491175914) queried the exact public Reddit discussion via Arctic Shift `/api/comments/tree`, rather than relying on Google/Reddit snippets. It returned **18** archived public comments, **no partial-tree flag**, and the target original comment by `Afaith_1` with `created_utc=1772947941`. Response SHA256 `37340bdeba812b4bc4491bb1507d651743063b497df9195fd2a88e36b4c87725`. No public same-author correction/confirmation followed within the retrieved thread. The source audit does not assert all deleted/missing future comments were searchable.
- An exact, case-insensitive *public pseudonym* match against the captured community [canonical sticker ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) found no `Afaith_1` entry. **Absence of that pseudonym does not prove this CE or account was unrecorded under a transfer, another handle, photograph, sticker number, or case identifier.**

## Why this matters specifically to the sticker hunt

The **white numbered sticker** seals the black-paper-wrapped physical PS4 game included in the CE shipping package. The larger premium contents box can remain sealed while its **separately wrapped game** is removed from the shipping container.

This deal might therefore have separated two materially relevant objects:

1. **Collector's Edition box and sculpture:** reportedly acquired by the public commenter.
2. **Original PS4 game, its black wrapper and the numbered sticker:** potentially retained by the seller, **but the original wrapper and sticker are not mentioned or pictured**. There is no proof whether the seller saved/discarded either item, whether the PS4 disc itself was unwrapped, or whether the numbered sticker was removed before transfer.

That does **not** prove two CE owners or two sticker cases. It poses a more productive *source-reconciliation question*: **was the numbered black game wrapper part of the retained component, rather than part of the buyer's sealed CE box?** An ownership search focused only on who currently displays the big collector box might overlook the person who last possessed the game wrapper.

**Do not conflate it with March 9, 2026 eBay sale item [389713956842](https://www.ebay.com/itm/389713956842).** That sale appears in a secondary PriceCharting completed-sales index on the following calendar date, but no original seller image, price match, account match or chain of custody links it to this public statement. The PriceCharting row also calls its condition `CIB`, not *disc excluded*. Date proximity alone is **not a transfer-chain connection**.

## Triage and handoff value

**Lead priority:** high among text-only historical acquisition reports. **Evidence confidence:** high that the public commenter actually made the dated statement; **low/unknown** as to whether this is a distinct physical edition, a completed sale, whether the seller retained the game wrapper, or whether a sticker survives. **Images:** none from this source; **numbers/symbols:** none.

For raezores, this is worth a **single source-first ledger/Discord reconciliation check** against existing 2026 resale and split-package cases. A concise source description is: *“March 8 2026, `Afaith_1` reports paying ~$650 for a sealed INSIDE CE after apparently leaving the PS4 physical game with the seller; could its stickered black game wrapper have stayed with the seller? Original public comment `o99qxpo`, presently absent by exact username from public sticker ledger. No serial/photo. Please check whether this transfer is already recorded.”* This is a proposed information packet, **not** permission for this agent to message or contact any owner.

## Durable test and reproducibility

[Source manifest](../../data/reference/inside-ce-2026-disc-retained-acquisition-leads.json) stores original permalink, precise comment ID/UTC date, comment archive SHA, evidence grade, explicitly ambiguous disc/sticker custody, and unverified relation to any listing. [Audit script](../../scripts/external_evidence/audit_public_ce_split_sale_leads.py) verifies permalink structure and response SHA, checks exact public-source pseudonym occurrence against canonical ledger, and never promotes sticker/copy counts. Its [offline regressions](../../tests/test_ce_public_split_sale_leads.py) reject bad domains, fabricated sticker claims, duplicate IDs and accidental handle-substring matches.

**Result:** **one newly surfaced, unreconciled public buyer statement** that may suggest a separated sticker-carrying component; **0 new serials**, **0 new sticker photographs** and **0 newly proven physical editions**.

# CE resale visual research: reconcile September 2020 posts with known U32

**Observed:** 2026-10-13. **Scope:** public historical sources, no owner outreach, no new sticker photo claims. **Primary controls:** [canonical community `U32` entry](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md), [original archival keyword pilot](inside-ce-first-cross-community-archive-pilot-2026-10-13.md).

## Corrected outcome

The first cross-community archive pilot surfaced [GameSale `iuutfq`](https://www.reddit.com/r/GameSale/comments/iuutfq) and [GameSale `izs23a`](https://www.reddit.com/r/GameSale/comments/izs23a), initially flagged `unreconciled-by-exact-url` because neither Reddit ID appears in the captured `stickers.md` ledger. A follow-up *source-first* web search revealed their unabridged public descriptions and original account context. Both were published by the same public account recorded by the community as **U32**. The December 2020 community discovery post is by that same account. This is an example of **new source URLs belonging to an already-known owner case**, not evidence of new copies.

| Public post | Date | Evidence | Reconciliation |
|---|---|---|---|
| [r/gameswap `irlw53`](https://www.reddit.com/r/gameswap/comments/irlw53) | 2020-09-12 | CE+Huddle offered in exchange for Limited Run Games editions. Same copy description as later GameSale posts. | Known U32 public seller account, likely relist. |
| [r/GameSale `iuutfq`](https://www.reddit.com/r/GameSale/comments/iuutfq) | 2020-09-17 | iam8bit INSIDE CE with Huddle and sealed game/figure, offered for $250 shipped or LRG trades. | Known U32 public seller account, likely relist. |
| [r/GameSale `izs23a`](https://www.reddit.com/r/GameSale/comments/izs23a) | 2020-09-25 | Title and contents description match September 17 sale, same account. | Known U32 public seller account, likely relist. |
| [r/GameSale `k4wyvu`](https://www.reddit.com/r/GameSale/comments/k4wyvu) | 2020-12-01 | Advertises the iam8bit CE with a Switch dock, $250 shipped for the CE. | Explicit original source of canonical U32. |
| [r/GameSale `1csyklf`](https://www.reddit.com/r/GameSale/comments/1csyklf) | 2024-05 | Later public resale account posting and transfer history. | Already recorded in canonical U32 with downstream 2024 purchaser. |

The source IDs, *not account contact details*, are preserved in the [curated known resale source register](../../data/reference/inside-ce-curated-known-public-sale-links.json). This is an explicit audited reconciliation by public source ID, not an automated identity graph. The relationship **same public selling account** is strongly supported; whether one account ever held multiple CE boxes cannot be resolved merely from repeated advertisements. No independent evidence here shows multiple copies.

**Other concrete negative control:** [eBay listing 257753799919](https://www.ebay.com/itm/257753799919) might look like a newly discovered sale, but canonical `stickers.md` already records it as **/047** with an existing transfer chain. The ledger alone suffices to prevent inflating owner/serial counts.

**Still unresolved:** [July 2020 r/GameSale `i0vgml`](https://www.reddit.com/r/GameSale/comments/i0vgml/) was already surfaced in the [October 12 owner hunt](inside-ce-native-owner-hunt-2026-10-12.md) and has not yet been attributed to U32 or any separate known owner case. It should stay `unreconciled` until exact post metadata and source photos establish a specific relationship. A seller listing from a different public account does not prove a different physical CE, since boxes transfer through resale.

## Permanent software change

The [market-search script](../../scripts/external_evidence/search_public_reddit_ce_media.py) and [exact-post probe](../../scripts/external_evidence/lookup_public_ce_resale_posts.py) now load an **opt-in, explicitly authored mapping** of original post ID to already-known case. This supplements the earlier strict URL-in-canonical-ledger check; it does not infer associations from names, textual similarity or newly discovered handles. For the three September posts and two canonical U32 URLs, candidates are classified `existing-curated-case-U32` and keep `curated_case_ref=U32`, while `i0vgml` remains unrelated/unreconciled. The source manifest also records the known /047 eBay listing for manual marketplace review.

This is a **deduplication and provenance improvement** with **zero newly confirmed numbered stickers, zero additional confirmed owners**. Do not forward the U32 resale reposts to raezores as newly discovered owner leads.

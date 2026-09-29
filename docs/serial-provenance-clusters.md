# Serial provenance clusters

_Status: archival assignment audit. This is about physical distribution history, not cipher semantics._

The community sticker ledger contains a few cases where multiple Collector's Editions can be associated with the same owner/seller. These are useful because they can test simple hypotheses about how numbered seals were assigned during kitting.

Source corpus:

- https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md

## Explicit multi-copy cases

### roma_kreu: 178 and 179

The ledger states that, after seller `roma_kreu` supplied a better image of sticker 178, the seller also supplied sticker 179, "revealing that he actually had two collector's editions."

Known seals:

- 178
- 179

Pattern:

- consecutive numbers;
- adjacent A–I image positions by the public image cadence (G/H).

This case is compatible with sequential label assignment, but by itself does not prove it.

### videogamescollection-824: five-copy seller lot

The ledger explicitly labels one eBay seller's copies as `1/5` through `5/5`.

Known readable seals:

- copy 2/5: 038
- copy 3/5: 193
- copy 4/5: 194
- copy 5/5: 252
- copy 1/5: sticker lost/unreadable in the current ledger

Known serial span:

- minimum 38
- maximum 252
- span 214

Sorted known differences:

- 38 → 193: +155
- 193 → 194: +1
- 194 → 252: +58

This is incompatible with the simple claim that **all five copies in this seller's possession carried one contiguous run of seal numbers**.

Caution: the ledger does not establish that the seller originally purchased all five copies in one preorder or received them in one fulfillment carton. The result constrains possession, not necessarily iam8bit's original assignment process.

## Other same-source pairs worth resolving

The ledger contains additional same-person/same-source-looking pairs, including:

- 182 and 184, both attributed to Roulette / the same Discord source;
- 247 and 248, both attributed to BishopNull / the same Discord source and date.

Before using these as distribution evidence, verify whether each pair represents:

1. two CEs simultaneously owned by the same person;
2. a seller plus a buyer;
3. two images obtained from a third party;
4. some other provenance relationship.

Do not silently promote matching usernames into a same-order claim.

## What the clusters currently support

The small sample fits a **mixed physical assignment picture**:

- at least one explicit two-copy owner has adjacent labels (178/179);
- one explicit five-copy seller lot contains both an adjacent pair (193/194) and labels separated by large gaps (38 and 252).

Therefore neither of these naive models is supported as a universal rule:

- "multi-copy owners always receive consecutive seals";
- "multi-copy owners never receive consecutive seals."

The likely useful distinction is between **label generation order** and **unit assignment order**. A printer could have produced a sequential label run while final kitting drew from that run in sheets, stacks, partial batches, or shuffled order.

## High-value archival questions created by this result

Ask the final kitting/label vendor:

- Were seals supplied on rolls, sheets, or individually cut?
- Were they physically ordered by serial?
- Did packers take the "next" seal or arbitrary seals?
- Were multiple CEs in one customer order packed together?
- Were leftover/overrun seals retained after fulfillment?

Ask iam8bit:

- Did multi-unit customer orders receive adjacent labels by design?
- Did fulfillment know or record which coded seal went to which order?
- Was the code applied before or after customer-order allocation?

## A potentially decisive future comparison

If original order records or owner receipts can identify **multi-copy single orders**, compare serial distances within those orders.

- Strong adjacency within same-order pairs would point toward sequential pack-out.
- Distances resembling random draws from the overall produced range would point toward shuffled or pre-kitted stock.
- Sheet-sized periodicity in distances could reveal the physical print imposition.

This is one of the few ways owner provenance can teach us about manufacturing without requiring any new sticker symbols.

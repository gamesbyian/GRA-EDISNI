# March 2020 iam8bit INSIDE CE waitlist thread: purchase retraction and false-owner control

**Observed:** October 13, 2026. **Historical discussion:** [r/PlaydeadsInside/fhvflq](https://www.reddit.com/r/PlaydeadsInside/comments/fhvflq/) from March 13–15, 2020. **One-shot archived comment query:** [GitHub Actions run 38473907863](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38473907863), [execution-only PR #264](https://github.com/gamesbyian/GRA-EDISNI/pull/264). Public Arctic Shift archival comment-tree response SHA-256 `5d5705ba5179355f90a8706bdd78721a157bc8e0d53a29d0ca5d72dbfd790742`. The API returned **17 comments**, no collapsed nodes reported (not a completeness guarantee).

## The apparently new purchase claim is contradicted by the same original account

- [Initial comment `fkeb0sa`](https://www.reddit.com/comments/fhvflq/_/fkeb0sa/): March 13, 2020, public author **`lengbleu`** says *“Just bought the damn thing.... It better be worth it!”*
- [Later comment `fkkj7it`](https://www.reddit.com/comments/fhvflq/_/fkkj7it/): March 15, 2020, **same author `lengbleu`** says *“I didn't buy it in the end”*.
- The original user ID and timestamps were checked against the same source archive; the comment-tree claims refer to the same public pseudonym and same Reddit thread. There is **no established purchase, physical receipt, or numbered sticker** here. Even if the initial phrase implied placing an order, the later public statement supersedes it as evidence of completed acquisition.

Another participant in the discussion, **`Raezoress`**, says they already had a CE bought on eBay. That public account is already present by exact name in the canonical community ledger; this is not an independent new owner report to send back to the same researcher. Its presence in the discussion was useful context but no unknown sticker number.

**Result:** zero newly confirmed owners, zero photos, zero sticker observations from this thread. Recording the contradictory public claim prevents repeated future false leads.

## Software improvement

The reusable [public same-thread claim audit](../../scripts/external_evidence/audit_public_ce_thread_claims.py) requests a **single exact public post ID** via the existing bounded Arctic Shift comment-tree endpoint and groups only the returned comments by same-thread public author. It distinguishes `purchase-asserted`, `purchase-retracted`, and `receipt-asserted` wording, with chronological original comment permalinks, UTC timestamps and explicit `physical_copy_confirmed=false` and `sticker_serial_confirmed=false`. It never infers ownership from keywords, contacts any user, crawls author profiles, or fuses identities across threads.

A purchase claim followed by retraction from the **same** original author becomes `same-thread-later-purchase-retraction-review`. A later comment by **another** user cannot retract someone's purchase: that adversarial case is covered by tests. A receipt statement is still treated as text-only and does not automatically prove a surviving sticker. Missing archived comments, deleted content, editing or transfer histories can affect interpretation.

The pilot also illustrates a distinct problem from duplicate image links: **conflicting time-ordered source assertions**, even when both original links are correct. The system should reconcile these before raising new-owner leads.

### Evidence boundary

Do not add `lengbleu` to the owner/sticker ledgers based on this thread. Do not send to raezores as an owner lead. The new regression prevents an isolated archived buyer quotation from being promoted without examining same-thread retractions.

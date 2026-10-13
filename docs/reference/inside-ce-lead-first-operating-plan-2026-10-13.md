# CE lead-first operating plan (2026-10-13)

**Objective:** Produce *new, actionable, public-source leads for Raezore* rather than a high count of unexecuted searches. No owner outreach by this project. Raezore's methods are the baseline, not an untouched discovery area.

## First pass: source validity before scale

The first open-web probe used broad quoted English phrases about receiving the INSIDE CE and found **no eligible new lead**. Its results were largely about *Microsoft Flight Simulator* and *Larian* collector editions: the English word INSIDE is ambiguous. This is a **measured query failure**, not evidence no owners exist. Subsequent broad queries must require Playdead, iam8bit, RealDoll, Huddle plus Playdead, or a known INSIDE ARG anchor, with platform-specific exclusions. Do not send these unrelated results to Raezore.

## Lead-first pipeline

1. **Discover** original public owner photos, period forum posts, reply threads, videos, auctions and archived records. Query in native language; preserve the exact original text.
2. **Retrieve** original source and original comments where authorized, including image media provenance, not just title snippets. Archive capture metadata and body retrieval are distinct.
3. **Rank** with [public lead triager](../../scripts/rank_inside_ce_public_leads.py): first-person owner/arrival/sale signals across English, Japanese, Chinese, Portuguese, Spanish, French, German and Russian, potential serial syntax and product anchors. Ranking is a *review aid*, not a classifier that can confirm owners.
4. **Deduplicate** by source URL, known canonical link and physical-object history; never equate repeated posts with new copies. Use existing [canonical-source comparison](../../scripts/triage_inside_ce_index_results.py) for exact URLs and same-thread context.
5. **Review** every candidate against [twinysam canonical stickers](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md), original media and evidence class: directly visible number/symbol, reported without image, owner claim, sale, historical product discussion, or unrelated.
6. **Package** only new or plausibly underdocumented public-source leads: original link, source date, language, short native excerpt, evidence claim, what is still unknown, possible duplicate, and one concrete next step for Raezore. Avoid private contact information or identifying alternate accounts.

## Immediate retrieval priorities

- Replies and quote-posts under 2019 shipping/unboxing announcements, especially first-person mentions that do not use the CE's full product name.
- Original public photographs and videos showing the Huddle, outer shipping wrapper, or label, even when captions are silent.
- Native Japanese, Chinese, Korean, Russian and European resale posts and seller photo archives; exclude unsubstantiated ownership inferences from marketing images.
- Dated archives of non-English gaming forums and collector databases. Test known-positive recall before bulk execution.

## Reporting discipline

- **Lead status:** unverified until source reviewed; zero confirmed stickers from this document.
- **Coverage:** report completed queries and successfully retrieved reply/media bodies separately. A planned 28,188-query manifest is not 28,188 completed searches.
- **Negative results:** valid only for the specific provider, phrase, time interval and content surface successfully searched.
- **No outreach:** deliver a useful original URL to Raezore; leave decisions about communication to the community.

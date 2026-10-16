# INSIDE CE: measured-search deployment and visual-review handoff

**16 October 2026.** This is an implementation/verification handoff, not a claim of a completed Brave campaign, bulk image crawl or new sticker. **No owner contact. No confirmed physical sticker.**

## What is now executable

### Original public-image reviewer

`scripts/external_evidence/build_visual_review_gallery.py` reads the existing `candidate-index.json` and `visual-matches.json`, then embeds source-diverse thumbnail previews into a **self-contained, JavaScript-free HTML** review gallery. The optional actual-media `ce-visual-provenance.yml` workflow now writes `visual-evidence-work/review-gallery.html` to its already-existing upload artifact.

- Source links and CDN URLs are included only as user-opened HTTPS links; image previews are local data URIs, so opening the HTML does not request remote images.
- Candidate files must remain under the explicit root; corrupt, unsafe or missing media yield a visible placeholder and a counter, not a quietly omitted photo.
- Reviews show the source batch, byte digest prefix, similar known physical/promotional/standalone image role, optional confirmed canonical case and original source URL. **Similarity is always review-only.**
- First pass selects diverse sources with candidate matches prioritized inside each source. Crucially **unmatched images are still sampled** to prevent reviewing only already known reposts.
- The paired `review-gallery.summary.json` documents inspected candidates, omitted candidates and missing/unsafe thumbnails. No OCR or automatic owner identification is performed.

Example after explicit opt-in image harvesting:

```bash
python scripts/external_evidence/build_visual_review_gallery.py \
  --index visual-evidence-work/candidate-index.json \
  --matches visual-evidence-work/visual-matches.json \
  --candidate-root evidence-work \
  --output visual-evidence-work/review-gallery.html --max-items 48
```

### Durable planned/attempted source accounting

`scripts/external_evidence/audit_search_attempts.py` consumes a **frozen tasks JSONL** and zero or more append-only observation-event JSONL files. It emits `run-summary.json`, `validated-events.jsonl` and `resume-pending.jsonl`. It does **not** execute searches or automatically retry refused providers.

- Real attempts require distinct `attempt_id`; success requires a response/normalized-payload SHA256. Duplicate attempts, nonexistent task IDs, unknown statuses and contradictory absence claims fail closed.
- Provider error and rate limit count as **attempted** but not successful. `not_attempted_after_provider_block` counts as **not attempted**. A single valid search-index page without documented pagination exhaustion **remains pending manual completeness review**.
- A retained original source is a different event class from a returned index URL. An image match never creates sticker proof.
- The live-capable `inside-ce-gold-recall.yml` workflow now runs a zero-API baseline journal for all **24** planned gold queries. Its `execute_index=yes` path converts only actually emitted normalized Brave results into provider-attempt events, with a GitHub run ID; the hash is *normalized result metadata*, explicitly **not original raw Brave HTTP or original photograph bytes**. Always-uploaded artifacts preserve the run status and any partial work.
- Resume remains **manual and explicitly authorized**. To merge across workflows, supply prior `validated-events.jsonl` as `--events`, plus new actual-results converted with `--brave-results` and a fresh `--run-id`. The manifest must remain unchanged across resumptions. No API key is needed to audit an already preserved result.

Zero-call readiness invocation:

```bash
python scripts/benchmark_inside_ce_discovery.py plan \
  --output search-output/inside-ce-gold-index-plan.jsonl
python scripts/external_evidence/audit_search_attempts.py \
  --tasks search-output/inside-ce-gold-index-plan.jsonl \
  --out search-output/source-attempts
```

## Bounded exploratory public web-search probe (this session)

An independent general web search was actually submitted with **eight broad domain-scoped queries**, based on the already frozen 12-control dataset (ResetEra, X/Twitter, CollecTit, Austrian Willhaben, YouTube, Reddit, eBay). Queries did **not** include sticker serials, user handles or original target post IDs. A source-level known positive was returned: original [Reddit display-case post `eers0x`](https://www.reddit.com/r/PlaydeadsInside/comments/eers0x), including the December 2019 comment that the owner's game wrapper had number **328** (existing G08). This is **one observed positive retrieval** and independently demonstrates that unprompted search vocabulary can surface numbered observations. The returned batches also contained nonmatching game-collector and marketplace entries, and another ResetEra report about the ARG, neither of which constitutes a new sticker.

**Measurement limitation:** the tool's aggregated search results do not expose a durable raw per-query web-index response, exhaustive page counts or a fixed ranking across all eight queries. Therefore **do not** enter invented response SHA256 or interpret missing returns as negative control misses in the machine-readable Brave benchmark; this session's probe is an *exploratory, non-comparable public web-provider result*. The source citation is the original Reddit URL, not a claim of eight validated search outcomes.

## Remaining gates before larger deployment

1. **Real scored provider recall:** GitHub connector here can inspect repository and Actions runs and manage PRs, but exposes **no workflow-dispatch action**. The official Brave search workflow still needs a deliberate `workflow_dispatch` run with `execute_index=yes` and an authorized `BRAVE_SEARCH_API_KEY` configured. Start at `start_index=0`, `max_queries=12`; the other 12 follow only after reviewing the first artifact and copying its manifest SHA. The two non-primary G05/G10 target URLs cannot pass exact original-photo recall until repaired.
2. **Original-media visual gold set:** Compare new gallery coverage to the existing 82+ known sticker photos, one original collector photo with no sticker, standalone-game examples and publisher promotional negatives. Test at least a few synthetic crop/rotation/low-contrast cases and measure held-out ROI recall before introducing expensive embedding/PDQ infrastructure.
3. **Incremental archival fallback:** ArchiveBox/Browsertrix, Common Crawl and Arquivo.pt offer promising *separate* historical media indexes, but should be piloted only on a small approved set with exact positive controls and recorded original bytes, not assumed to be installed or proven here.
4. **Independent source-candidate verification:** Before any Raezores report, reconcile original author, full current community sticker entry and transfer history, alias uncertainty and later retractions. An image similarity or unmentioned URL is not a new CE.

## Ready/blocked distinctions

- **Ready:** offline review HTML generation, CI tests, original-source URL/thumbnail safety rules, 24-query frozen planned/attempted reporting, opt-in existing image gathering and no-outreach guard.
- **Not yet measured:** actual Brave gold-query recall; whether ROI/embedding matching improves recoverable tiny serial stickers; retrieval of a novel serial. No other provider was silently executed by this PR.
- **Still blocked externally:** manual authorized workflow dispatch, some archived/social provider access and original sources missing at historical marketplaces.

**Desired first deployment artifact:** the first real 12-query Brave search results **plus** its provider-attempt ledger, evidence state and withheld-source gold evaluation, followed by at most 48 explicitly authorized public photos in a review-gallery HTML. Stop if searches are blocked or source bytes unavailable; retain the skipped remainder as pending rather than declaring no results.

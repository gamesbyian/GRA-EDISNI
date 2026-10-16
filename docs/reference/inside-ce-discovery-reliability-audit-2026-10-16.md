# INSIDE CE search discovery reliability audit, 16 October 2026

**Mode:** VALIDATE for source-code defects and synthetic controls, DISCOVER for additional retrieval failure hypotheses. **Source snapshot:** GRA-EDISNI main at c9571f8658ca0176e98249b41da67523b4e02042; Bluesky changes in independent [PR #288](https://github.com/gamesbyian/GRA-EDISNI/pull/288). This is an **audit of evidence acquisition**, not a new sticker decoding or owner confirmation.

## Why the Caswell case matters

Caswell's August 16, 2026 Bluesky post explicitly named INSIDE's Collector's Edition. The quoted generic phrase returned it as result 2/2 through the official primary Bluesky AppView search, without author-specific query terms. The prior absence from the working lead register therefore demonstrates a discovery-process gap, rather than grounds to conclude the source was inaccessible or never indexed.

There are **17 implementation groups** in the accompanying [source-by-source matrix](../../data/reference/inside-ce-search-pipeline-risk-matrix-2026-10-16.tsv). Each has its actual code and workflow, execution gate, known controls, failure modes, existing safeguards, recommended experiment and priority. The matrix spans native social discovery, broad web-index search, archived bodies/CDX, Reddit, YouTube/comments, image/media processing, reseller sources, local forums, link extraction and authorized Discord exports. It does not claim every individual script has received an independent end-to-end live test.

## Historical workflow-execution evidence

The GitHub Actions public run collection reported **10,141** total runs when inspected October 16, 2026; the same endpoint with **event=workflow_dispatch** returned **total_count=0**. Inspectable REST endpoints:

- https://api.github.com/repos/gamesbyian/GRA-EDISNI/actions/runs?per_page=100
- https://api.github.com/repos/gamesbyian/GRA-EDISNI/actions/runs?event=workflow_dispatch&per_page=100

Separately, 800 recent workflow runs on eight pages included green pull-request checks and offline search planners, with no manually dispatched runs in that sample. **This does not establish no searches were ever conducted**: live one-shot PR probes, browser research, historical community searches, other agents and local scripts have distinct execution routes. It does establish that **manual-dispatch-only campaigns have no documented runs in the queried Actions history**. In particular, 28,188 planned native-language forum/secondary tasks cannot be counted as completed searches. Many green workflow badges validate a plan or test harness, not an actual query.

## Five source-code defects found and fixed

1. **False-green media smoke:** Public media harvester recorded HTTP/extractor failure, then returned zero exit status. One-source GitHub smoke jobs therefore appeared successful despite failed or empty acquisitions. New payload-level health fields count acquired source files versus blocked/empty attempts. The existing public and social smoke workflows now pass --strict-selected so a failed/missing payload produces a nonzero job while their always-uploaded original evidence logs remain available. Multi-source non-strict harvests keep collecting partial evidence. Historical green jobs cannot now be relabeled failures without reviewing their original artifacts.
2. **Disappearing Wayback search tasks:** A Wayback CDX HTTP 403/429 previously stopped the loop before adding remaining planned tasks to the result. The audit preserves all later tasks as not_attempted_after_provider_block, retaining source URLs and windows. Synthetic 403 regression verifies four result records but only one actual request.
3. **Reddit candidate cap without disclosure:** The Arctic Shift cross-community scanner stopped adding relevant post candidates when max_total was reached yet still reported query status ok. It now reports new_candidates_omitted_at_cap, distinct_candidate_cap, and result_cap_reached separately from page-level possibly_truncated. A synthetic batch of five relevant posts with cap two explicitly accounts for the three missing candidates.
4. **Image scan silently skips pages:** Original HTML candidate extraction ignored invalid acquisition metadata, missing public source URL, and over-size HTML without storing any denominator. The output now counts source metadata, malformed entries, URL-less entries, HTML pages seen/read, pages skipped for size, and pages with/without image URLs. A zero-lead report can be recognized as a zero-body scan rather than evidence of no images.
5. **No common provider-run health contract:** An offline, schema-specific evaluator now supports Brave index JSONL, CDX JSONL, Reddit archive query audits, source acquisition JSON, HTML image candidate JSON, and Bluesky result JSON. It counts attempted, blocked, omitted, page-truncated, zero-payload and unrecognized outcomes. All output is explicitly bounded to search execution, not physical ownership or sticker confirmation.

New tests and existing source-specific tests protect these fixes. **No live third-party network call is needed** for the regression suite.

## Other important risks identified but not yet falsified end-to-end

**Web index and recall:** The Brave/index workflow defaults to planning. Gold positive controls have two nominally blind searches for twelve source URLs, but their effectiveness is unknown until permitted live execution. A result URL is not the original post body, video comments, image, or owner claim.

**Archival search:** An Availability API empty result or a limited CDX response is not an exhaustive Wayback absence. A metadata pointer is not usable historical content; MIME, response status, capture timestamp, digest, and original URL must accompany replay. Directory last-modified timestamps do not prove creation dates.

**YouTube and social:** A successful extractor process can yield no downloadable media; logins, anti-bot responses and failed automatic subtitles/comments must remain visible. Positive controls should include known historical videos, an original comment, and a readable photo, not just a playable video URL. The user does not want further owner outreach.

**Image searching:** Static image tags, srcset and OpenGraph fields miss JS-only assets, embedded media, removed pictures and unindexed photographs. The next audit must count how many extracted images are filtered by host allowlist, promotional-filename rules, per-page cap and byte budget; use images with verified retained physical labels as controls. CLIP relative rankings are not probabilities of ownership.

**Reddit and local forums:** The archive backend returns partial date-scoped results, 422 timeouts and possibly removed comments; source-native search and original post body recovery need independent measurement. Local SQLite searches cover only previously ingested WARC/HTML pages, not the whole forum and not images.

**Link extraction:** URL extraction from locally downloaded files ignores relative links and material not present in acquired HTML. A workflow still uses an optional link-discovery step with suppressed exceptions; that separate reliability gate and selection waterfall are future work.

**Discord/gated sources:** Explicit source permission and rights constraints are part of the search boundary. Never interpret an API entitlement failure as no results, and do not bypass it with unapproved proxies or credentials.

## Evidence lifecycle and rigorous follow-up

Track these states independently for every source: inventoried, search planned, entitlement verified, request sent, valid provider response, pagination exhausted or censored, original source text/photo/video retrieved, topic matched, ownership asserted, known-owner-object reconciled, sticker physically verified. Require both a numerator and denominator and separate post creation, indexing, archive capture, and retrieval dates.

Run a **small, controlled, permission-compliant positive-recall battery per source** before allocating large-scale query budgets. Freeze several historical exact public source targets, but withhold usernames, post IDs and distinctive URLs from their discovery queries. A zero-result provider response may be valid yet not exhaustive; 403/429/timeout and unexecuted are never negative results.

To inspect retained reports without network, use scripts/audit_ce_search_run_health.py with --kind and --input plus --output. The kinds are brave_index, wayback_cdx, reddit_archive, public_harvest, html_images, and bluesky. Its --strict option is for explicitly complete acquisition requirements, not for all useful exploratory runs. Results include counts, flags, evidence ceiling, and zero newly confirmed stickers. An expired artifact must be logged as unavailable rather than retrospectively called a completed search.

Recommended next fixes, in budget order: prove actual index-search known-positive recall; inspect archival/provider blockers; add a full image selection/exclusion waterfall; verify video/comment source payloads; then expand native queries only where baseline retrieval works. Avoid touching PR #288's live Bluesky lane until its own integration is verified.

**Present conclusion:** the search program has demonstrated operational blind spots and misleading success signals, but this audit has confirmed no new sticker, serial or new physical owner and cannot prove historical nonexistence of any public source.

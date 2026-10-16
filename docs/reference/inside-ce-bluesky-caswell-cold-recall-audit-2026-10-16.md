# Why an exact-title Bluesky CE owner lead escaped our searches

**2026-10-16; evidence-first discovery audit, not a new physical-sticker finding.**

## Known-positive and chronology

An independent 14–15 October Discord search recap supplied an August 16, 2026 [Tom Caswell public Bluesky post](https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i), reportedly containing "inside collector's edition" and a question about still needing the Huddle. The profile is publicly indexed as `tomcaswell.games` / `did:plc:msovagwqdq3ew2rrikvpqp7c`. The exact AT URI, original post text and August 16 timestamp are **now independently verified by the live getPostThread control** (details and run link below). Do not assume the CE remains in Caswell's possession, that the sticker survived, or that a press copy is distinct from canonical U/L entries. Ian has already sent this link to Raezores; no further contact is part of this experiment.

[Upstream canonical register](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) and [research methods](https://github.com/twinysam/INSIDE-ARG/blob/master/raezores-research.md) contained no text match for Caswell or GameSpot when checked 2026-10-15. Those are narrower than the full private community log and do not establish he was unknown to every participant.

### Proven repository gap, not postmortem guesswork

Our pre-existing [secondary-platform inventory](../../data/reference/inside-ce-ownership-secondary-platforms.tsv) **already included Bluesky**, assigned **P2**, with ATProto `searchPosts` as the proposed source-native route. Our [multilingual source planner](../../scripts/build_inside_ce_native_search_campaign.py) created **28,188 combined planned tasks**, including 30 social/resale platforms, and the [native campaign workflow](../../.github/workflows/inside-ce-native-search-campaign.yml) defaults to offline planning. Actual Brave-index searches require a separate explicit workflow dispatch and API quota. These tasks are not evidence that Bluesky's search index or original posts were checked.

Thus it is established that **our default workflow has no guaranteed Bluesky-native discovery**. It is *not* established whether Raezores personally ran Bluesky searches, whether a specific index contained the post in August, or whether any prior optional GHA run happened to retrieve it. Report those questions as unknown unless original logs verify them.

## Original protocol sources and why two APIs matter

- [Bluesky official ATProto lexicon: searchPosts](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/searchPosts.json): public search with `q`, `since`, `until`, `sort=latest/top`, cursor; exact query syntax and completeness are *unspecified*.
- [Official newer searchPostsV2](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/searchPostsV2.json): `query`, `sort=recent/top`, `allTime`, date bounds, filters and cursor. **allTime searches the full index rather than the recent-post window**; an important possible explanation for a two-month-old miss. Whether this unauthenticated endpoint is enabled must be measured and status-coded rather than assumed.
- [Official public AppView API host guidance](https://bsky.network/docs/api-directory/): unauthenticated public reads generally go to `https://public.api.bsky.app`.
- Original historical [pagination 403](https://github.com/bluesky-social/atproto/issues/3583) and [date-filter errors](https://github.com/bluesky-social/atproto/issues/3021) show why a successful first page is not proof of complete native coverage.

## Measurement design (source record is held out from searches)

The [bounded benchmark](../../scripts/audit_bluesky_ce_recall.py) freezes **eight category-level discovery expressions** before checking the known-positive body: exact words, quoted title, apostrophe-free title, Huddle+Playdead, Huddle+INSIDE, collector-edition+Playdead, iam8bit+INSIDE and RealDoll+INSIDE. Neither "Tom", his handle, his DID nor his post ID is present in a discovery query.

**One independent control:** `app.bsky.feed.getPostThread` for the exact AT URI `at://did:plc:msovagwqdq3ew2rrikvpqp7c/app.bsky.feed.post/3mta6ecjbvk2i`. If it succeeds, retain original text and post-created timestamp; if it fails, label source unverified by this run. It is **not** counted as blind discovery.

**Sixteen blind probes:** eight expressions, each through V1 latest and V2 recent with `allTime=true`, targeting the inclusive start Aug 1 and exclusive end Oct 16, 2026. Each samples the **first 50 posts only**, one page per query; source matches require the exact AT URI. Each record keeps query, endpoint, observed error/status, parsed count, approximate provider-reported hits, cursor presence and exact target rank if present. Cursor availability, hitsTotal or a return count of 50 are warnings of truncation, *not* evidence of exhaustive search.

**Hard limits:** zero network access by default; `--execute` is required, maximum 17 GETs, ≥1 sec spacing, 18-second timeout, ≤800 KB response, no credentials, no private APIs, no retries or proxy cycling; stop on rate limit 429 or payment gate 402; a search 401/403 blocks repeat calls to **that specific endpoint version**, but still tests the other independently documented version. A missing direct source (e.g., 404) does not block separate blind retrieval testing. Negative-result categories stay separate from blocked/failed/unexecuted queries.

### Reproduction

```bash
python -m unittest discover -s tests -p test_bluesky_ce_recall.py -v
python scripts/audit_bluesky_ce_recall.py --output /tmp/bluesky-plan.json
# Live public API requests ONLY with explicit execution:
python scripts/audit_bluesky_ce_recall.py --execute --max-requests 17 \
  --output /tmp/bluesky-measured.json
```

[Workflow](../../.github/workflows/inside-ce-bluesky-recall.yml) runs offline regression tests and, on the first PR introducing this audit, **one bounded live 17-GET check** with a 14-day research artifact. Later runs are explicit opt-ins; there is no timer or perpetual search. This PR-only test must be read as a **retrospective known-positive benchmark**, never a prospective new-owner discovery.

## Interpretation matrix

| Direct exact-post control | Blind search | Supported interpretation |
|---|---|---|
| Accessible with original text | Exact target URI found | Source-native retrieval works for at least one method and one sampled result page; historic community failure still unexplained |
| Accessible | No result, but successful API search and more pages | First-page/ranking/time-window or term matching missed it; run a bounded narrower retrospective diagnostic before blaming missing indexing |
| Accessible | Full finite search response without target | That exact query/version/window did not retrieve it in this run; not a global-index absence proof |
| Accessible | 401/403/429/5xx failure | Search-route capability/access limitation, **not** an observed missing index entry |
| Unavailable | Any failure/absence | Cannot even verify continuing source accessibility; historical indexing remains open |

No first-page result can establish full coverage; a source URL delivered by a web search is not evidence a post's text or CE sticker is present.

## Follow-on experiments contingent on actual results

1. **If direct control succeeds but wide-window searches miss:** freeze a second benchmark version, add Aug 15–18 narrow window under the same queries (only *diagnostic*, not an unbiased cold solve) and compare V2 `recent/top`, V1 `latest/top`, and first-page versus cursor traversal **subject to provider and fixed request budgets**.
2. **If native search finds Caswell:** measure what ordinary 2026-08 web-index queries returned by the provider using a separate dated index-positive control; do not claim web indexes were defective without a controlled execution.
3. **If both indexes miss:** build a rights-aware source-specific retrieval strategy for Bluesky, tested against *multiple independently known public controls*, especially posts with unremarkable captions, actual text/alt-text differences, changed handles, and deleted/reposted objects. A single one-off cannot estimate recall.
4. **For all 30 source surfaces:** record `planned`, `API_access_verified`, `query_executed`, `original_body_recovered`, `reconciled_with_canonical`, and `confirmed_sticker` separately; publish run counters and source-specific blind recall, not raw planned task count.
5. **Do not contact Caswell or any other apparent owners from this pipeline.** Any genuine public lead goes to human source-review with original URL, date, firsthand wording, possible known-case match and *no* inferred sticker symbol or number.

**Initial live observation, superseded by per-endpoint test in the next CI run:** [GitHub Actions run 38863537662](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38863537662) (2026-10-16 06:51 UTC) executed two actual public API GET requests: the exact original-post control **succeeded**, while the first V2 allTime search returned **HTTP 403**. It then stopped under the original broad access gate; therefore no V1 search was performed in that run and no conclusion about native keyword recall follows. The workflow's eight original synthetic checks were seven at this first run, all passing. The access policy and a new per-version regression were subsequently amended to avoid letting a V2 refusal suppress independent V1 tests. Subsequent exact-head CI outputs must be separately recorded; don't silently collapse the two experiments. Bluesky is provisionally promoted from P2 to **P1** because of a demonstrated missed known-positive and its low acquisition cost. Reassess after measured recall and source originality checks.


## Second live result: direct source verified; BOTH search versions access-denied

[Exact-head run 38864203210](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38864203210) on 2026-10-16T06:58:22Z passed **eight deterministic unit tests** and made **three actual GETs**:

1. Direct getPostThread succeeded for the expected AT URI, original handle and date. Original body: **"Do I still need Inside Collector’s edition jelly statue?"** The post creation timestamp is **2026-08-16T21:53:12.962Z**.
2. The newer searchPostsV2 keyword query (allTime=true) returned HTTP **403**.
3. The older searchPosts keyword query returned HTTP **403**. Fourteen later planned probes were marked *skipped_after_endpoint_access_failure* and made zero network calls.

**The source itself is now verified. Search absence is not measured.** Neither index returned a successful empty result, and the failure from our public GitHub Actions runner cannot be generalized to logged-in accounts or to the API's state in August.

### New lexical mismatch, distinct from API access

The literal body uses **U+2019 right curly apostrophe** (Collector’s). Our principal query contains **U+0027 ASCII straight apostrophe** (collector's). After only Unicode casefolding, a naive substring matcher does not find the query. Replacing curly apostrophes with ASCII apostrophes first yields an exact match. That is a real local-text-matching hazard, but **not** evidence that Bluesky's actual search index discriminates these characters, since our queries were refused. Treat the curly-quote variant as a retrospective diagnostic, not as a successful blind search.

The program still requires original-source/CE-object reconciliation and cannot infer that Caswell retains this Huddle, possessed a wrapping sticker, or represents an additional distinct copy. Ian already gave the lead to Raezores.


## Downstream triage error: search-hit scoring, independently reproduced

The existing [public-lead ranker](../../scripts/rank_inside_ce_public_leads.py) matched explicit possession verbs such as "I bought", "I own", "my" and marketing anchors (Huddle, iam8bit, Playdead, RealDoll). Caswell's **actual verified public text** has neither set: without a new rule it received **score 0** despite naming the INSIDE CE. Thus even a successfully retrieved search hit could be buried after stronger-scored sources. This is a measurable **post-retrieval triage omission**, distinct from the 403 retrieval barrier.

The PR adds two conservative rules with an explicit regression: "Do I still need" / comparable first-person keep-or-dispose questions as **possible ownership (weight 2)** and the distinctive "INSIDE Collector’s Edition" title including straight or curly apostrophe **(weight 2)**. The Caswell text now scores **4**, remains **unverified_public_lead**, and always has **new_confirmed_stickers = 0**. This fixes ranking of similar questions without claiming they retained the full edition or numbered sticker. A local punctuation-normalization experiment also demonstrates why direct exact-string matching is unreliable.

# Search architecture for every worldwide gaming-forum lead

**Status:** DISCOVER / operational design, not a claim that 483 sites were crawled  
**Source directory:** [483-entry forum inventory](../../data/reference/global-gaming-forums.tsv)  
**Per-site routing:** [483-entry methods matrix](../../data/reference/global-gaming-forum-search-routing.tsv)  
**Local corpus search implementation:** [software evaluation and SQLite/warcio importer](forum-search-software-stack.md). Extract once, query arbitrary later terms without remote searches.  
**Historical search and mirrors:** [archive/mirror research](global-gaming-forum-archives-and-mirrors.md) and [483-entry archival fallback matrix](../../data/reference/global-gaming-forum-archive-routes.tsv)  
**Query planner:** [plan_global_forum_searches.py](../../scripts/plan_global_forum_searches.py)  
**Bounded index executor:** [run_global_forum_index_search.py](../../scripts/run_global_forum_index_search.py)  
**Manual workflow:** [forum-search-plan.yml](../../.github/workflows/forum-search-plan.yml)

## Objective, unit of work and present state

Accept **arbitrary search terms later**, including non-English strings, numeric serials, punctuation and multiword phrases. Build one independently accountable `(community, query, method, scope)` search task for every selected entry in the global directory. Preserve source URLs, original posting dates, attached media, uncertainty and archival provenance. A genuinely comprehensive campaign must search **post bodies and titles**, not just homepages or game-title names, and separate native results from externally indexed fragments.

All **483** current entries have a primary/fallback route, an index scope, a GHA execution designation, an access gate and explicit limitations in the TSV. These recommendations are **algorithmic or platform-level routing hypotheses**, not per-site live confirmations. The parent forum inventory itself contains many unverified candidate destinations. A host may be dead, renamed or not support a gaming discussion section; such failures must remain visible in audit results.

The approach distinguishes **coverage attempted** from **coverage achieved**. No individual site should be certified as fully searched just because a search engine returned zero hits or a forum returned the first page. A `site:` query can surface historical evidence, but cannot prove absence; Wayback CDX indexes archived **URLs**, not forum-post full text. A multilingual AI pass expands recall and ranks evidence only after collection.

### A workable definition of thoroughness

For each eligible forum and each term: (1) identify a searchable destination or document its failure; (2) use the best *authorized* native search/query endpoint; (3) paginate across available results and year ranges when the site permits; (4) cross-check a licensed general web index; (5) inspect dated archives or mirrors for dead or migrated threads; (6) compare original threads, translations and images without duplicate source-lineage inflation; (7) retain an explicit coverage ledger with gaps. The search is as thorough as the publicly accessible corpus and permissions allow, **not mathematically exhaustive**.

## Routing table design and confidence boundaries

Every named row in the forum directory has exactly one corresponding row in `data/reference/global-gaming-forum-search-routing.tsv`. Join on `(community, url)` rather than position. Its columns:

| Field | Meaning |
|---|---|
| `community`, `url` | Exact directory join key |
| `primary_method` | Most promising first authorized search route |
| `fallback_method` | Alternative discovery route; usually an external indexed search |
| `platform_hint` | Engine/service/category clue, **not necessarily fingerprinted** |
| `classification_basis` | `host` for unmistakable host services, `unconfirmed_engine_hint` for platform hypothesis, `directory_type` for news sites, `type_inference` elsewhere |
| `index_query_scope` | Ready-to-use, independently checkable `site:` search restriction, sometimes narrowed to subreddit/Steam app/PTT board |
| `access_gate` | Required authorization/site-policy preflight before live automation |
| `gha_mode` | Recommended runner family; does **not** imply implemented live support |
| `directory_evidence` | Carried from global directory: `V`, `C`, `H`; **not method verification** |
| `known_limitations` | Reason a zero-hit result would not prove absence |

**Key diagnostic:** `forum_native_probe` occurs widely because identifying a traditional forum software package or search endpoint from its home-page URL alone is unreliable. For those sites, the *best next action* is a short browser-agent discovery probe before implementing site-specific searches. Assigning a guessed `search.php`, XenForo API or arbitrary endpoint without testing is worse than a clear unverified native-search plan.

### Primary method families

| Method code | Recommended site-specific execution | Completeness and gating |
|---|---|---|
| `reddit_research_access_gate` | Review Reddit's **May 2026** researcher-specific access guidance and October 2026 eligibility criteria before any direct/API corpus search; only then use an explicitly authorized method. Indexed discovery/snapshots remain partial and rights-restricted | Ordinary developer OAuth alone is not permission for systematic research. No native Reddit worker is currently authorized or deployed. See archive/mirror audit. |
| `steam_native_search` | Use the board's native Search Discussions UI or permitted browser session; restrict to application ID and inspect posts/older pages | Steam's forum search may be fuzzy; cross-check external index and original dates; no public universal full-text API assumed |
| `stackexchange_search_advanced` | Public Stack Exchange `/2.3/search/advanced?site=gamedev&q=...`; paginate with quotas/backoff; inspect answers and comments | Official API documented; question-body searches do not imply every comment has been queried |
| `discourse_search_json` | Verify the host really runs Discourse and that public `/search.json?q=...` is allowed; paginate; inspect `posts` and `grouped_search_result` | Optional per-host anonymously permitted JSON; browser UI when disabled; do not assume engine by URL alone |
| `phpbb_search` | Check `search.php` native advanced search for titles, message bodies, forum selection, date and result pagination | Version and search-index configuration vary; no guessed bulk endpoint |
| `xenforo_native_search` | Confirm XenForo fingerprint; search UI including posts/threads via a permitted browser session | XenForo REST requires an admin-issued API key; advertised search routes have historically been inconsistent, so avoid claiming a public API |
| `invision_native_search` | Discover IPS/Invision native search UI, recent posts, date scoping; only use REST when the site operator issues an appropriate key/OAuth | First-party REST is **per-community authorization**, not a free shared forum search API |
| `gamefaqs_board_search` | Locate title and platform board, search its threads/posts with UI, then other board variants and historical migrations | No single universal thread-body export; disappearing boards/pages are holes |
| `jvc_per_game_forum_search` | Find per-title French gaming boards first, then their native thread search and date boundaries | Large independently indexed board ecosystem; one forum is not all of jeuxvideo.com |
| `ptt_board_search` | Enumerate relevant named PTT gaming boards, use their searchable board history with date and public access checks | Board-only search; mirrors may omit/decorrelate source timestamps |
| `imageboard_archive_search` | Search currently indexed 5ch/2ch board titles, thread indexes and independent compliant archives | Threads expire; deleted originals and mirror bias impose hard incompleteness |
| `tieba_board_search` | Find title-specific Baidu Tieba then native in-bar search; retain Chinese translations | Captchas/login and indexed-only reach can block automation; never bypass |
| `bahamut_board_search` | Find title-specific Bahamut 哈啦區 and searchable thread pages, including Traditional Chinese | Separate game boards; deleted threads not recoverable from native search |
| `dcinside_gallery_search` | Discover DC Inside gallery(s), inspect built-in search and date windows in Korean | Gallery migrations and deleted posts; do not invent a global search API |
| `ruliweb_board_search` | Find relevant console/PC/general categories then run native Korean search | Multiple community subdivisions; verify per-board scope |
| `nga_board_search` | Identify Chinese game/topic board; use its own native search only where accessible | Login, geographic availability and permissions vary |
| `proprietary_platform_probe` | First-party UI/API identification for game indexes, VK-like platforms, regional boards and question sites | Site-by-site probe needed, not a generic scraper |
| `forum_native_probe` | Open an allowed public board, inspect forum software/search UI and operator rules, freeze verified search form/URL and pagination before any automated browser run | **Not yet a verified native method.** Probe failure changes route to index/archives and records a blocker |
| `article_index_then_comment_check` | Licensed web search for articles about the terms, then inspect article-level comments where public and permitted | Most news homepages are **weak leads**; indexed article content is not indexed comments |
| `vendor_qa_search` / `mod_site_search` | Use provider/native filters and distinguish Q&A or download descriptions from community replies | Different entity types; only discussion threads count as forum evidence |
| `archive_first` | Locate historical forum URL, migrations and surviving archive captures; search captured text only where allowed | Wayback CDX is URL capture discovery; missing capture or search index ≠ post absent |

There are 22 distinct primary method identifiers. Some candidates use broad platform-discovery classes where independent endpoint verification remains necessary. **The TSV is the exhaustive per-row mapping**; this guide intentionally avoids duplicating hundreds of nearly identical row descriptions.

## Workflow stages

### Phase 0. Campaign definition

Receive terms in an UTF-8 file, **one arbitrary query per line**. Queries are not automatically split on spaces, commas or slashes. Default `literal` mode quotes each query for an external index; optional `expression` mode keeps intended Boolean/search syntax. For multilingual expansion, supply an explicit new variant as another term and track its provenance (`source_term`, translation and locale). Never silently convert an encoded serial or symbolic string into a translated natural-language phrase.

Choose the eligible cohort (`V,C,H`, a conservative `V` pilot, or special regional subsets), budget and search period. For INSIDE history, useful strata are 2016–2018 (game release), 2019–2024 (collector's edition), and 2025–present; boundaries are search filters, **not evidence that content exists**. Treat historical search as a separate branch of work, since general indexes seldom expose all old results.

### Phase 1. Authorized site fingerprint / probe

1. Resolve final forum/subforum destination without assuming a 200 response proves relevant user discussion. Check site policy/robots, rate limits, public access, historical archives, access constraints and whether browser automation is appropriate.
2. Identify platform from observable site metadata, search form, page structure and documented API, recording evidence URL, date and source. Test with one harmless term before freezing an adapter. `unconfirmed_engine_hint` must remain a hypothesis until such a test.
3. Determine whether search covers *all posts*, titles only, first post only, current board only, or a filtered subset. Identify paging depth, relevance/time ordering, indexing cutoff and oldest accessible content. Capture both successful and failed queries.
4. If a site demands login, CAPTCHA, blocks bots or forbids automated retrieval, stop that automated path and switch to a permitted API, public index, manual review or archives. Do **not** proxy-hop, spoof identity, rotate accounts or solve captchas to evade controls.

Recommended agent tools: ordinary HTTP/API client for documented endpoints, headless browser when site's automation is permitted and page requires interaction, language-specific query expansion, bounded semantic extraction/translation, and artifact provenance recording. **AI is particularly useful for finding native search forms and evaluating thread relevance, not for inventing hits or asserting negatives.**

### Phase 2. Actual search passes

For each `(forum, term)`, the prioritized sequence is:

- **Native comprehensive pass:** run the site's authenticated/anonymous search only as authorized; enumerate every permitted result page or record the cap. Search titles and bodies separately when supported. Split by year if a query returns truncated results. Search directly related board variants.
- **External index cross-check:** use a licensed search provider's official API with the row's `index_query_scope` (e.g., `site:forum.example.tld "INSIDE"`). Multiple providers, if independently available, improve recall, but are not statistically independent samples of the full site corpus.
- **Archive / migration pass:** identify original URLs via indexed citations and archived URL lists, retrieve snapshots legally and check any available archived text for terms; dedupe captures by canonical thread and content digest. Archive wildcard lookup does **not** mean an archived post exists.
- **AI-assisted review:** classify relevant hits, language, dates, directly observed evidence vs claims, unique photos and repeats. Preserve original language and link. Translate only for analysis; never overwrite originals.
- **Result/reconciliation pass:** append evidence ledger and a coverage record. Zero matches means **zero found by these methods**, not universal absence.

For very large services (Steam, Reddit, Tieba, PTT, 5ch, Bahamut), the named URL often represents an *unbounded collection of user-created forums*. Scope its title-specific communities first rather than pretending every newly created per-game board is enumerable. Do not multiply the 483 lead count by arbitrarily guessed number of subboards and label it coverage.

### Phase 3. Evidence schema and provenance

Each gathered **hit** should have fields: `campaign_id`, `task_id`, `forum`, `query`, `query_variant`, `method`, `original_thread_url`, `post_url`, `archive_capture_url`, `post_date_raw`, `post_date_utc` if validated, `retrieved_at`, `original_language`, `original_excerpt`, `translation`, `media_url`, `source_lineage_id`, `relevance_label`, `confidence`, and `rights/access_notes`. Store only the minimum public excerpts necessary for evidence, consistent with source terms and project needs.

Each completed **task** needs an independent coverage log: `status` (`not_started`, `blocked`, `index_only`, `native_partial`, `native_pages_exhausted`, `archives_checked`), `probe_url`, `software_identification_witness`, `queries_issued`, `oldest_observed_date`, `newest_observed_date`, `result_pages_checked`, `declared_result_count`, `unreadable_pages`, `rate_limited`, `login_barrier`, `archive_capture_count`, `coverage_notes`, `method_verified_at`. A finding counts as first-hand only when its source and context substantiate that status. Zero-hit observations are negative **only within the stated accessible search scope**.

For INSIDE stickers, multiple posts circulating one image are still a single physical source unless provenance demonstrates otherwise; route new physical assertions through the project's existing observation discipline rather than mutating canonical data from scraped snippets.

## GitHub Actions execution: ready now vs dependent on credentials

The new [manual workflow](../../.github/workflows/forum-search-plan.yml) has **no schedule or push trigger**. It consumes multiple queries through `workflow_dispatch`, verifies the routing matrix, invokes the [offline planner](../../scripts/plan_global_forum_searches.py), and uploads a JSONL task manifest and JSON summary. It has a default task ceiling of **10,000**, which prevents accidentally expanding 483 sites × hundreds of terms into a runaway campaign. **No site is contacted** in the planner.

Example from the repo checkout:

```bash
printf '%s\n' 'INSIDE' 'collector edition' '/043' 'プレイデッド シール' > /tmp/forum-terms.txt
python scripts/plan_global_forum_searches.py \
  --terms-file /tmp/forum-terms.txt \
  --query-mode literal \
  --statuses V,C,H \
  --max-tasks 10000 \
  --output /tmp/forum-tasks.jsonl \
  --summary /tmp/forum-summary.json
python -m unittest discover -s tests -p 'test_global_forum_search_plan.py' -v
```

The planner joins the [archive fallback matrix](../../data/reference/global-gaming-forum-archive-routes.tsv) on exact community/URL keys and generates human-openable scoped search links for every `(forum,term)`, possible conditional-native links only for known adapter families, and a Wayback discovery link. `state=planned_unexecuted` is deliberate: these URLs are **work items, not evidence of searches completed**.

**Optional actual index lookup:** Set the GitHub Actions secret `BRAVE_SEARCH_API_KEY` (after acquiring a suitable approved plan), then select `execute_index=yes` and `max_index_queries` in the same manual workflow. The [bounded executor](../../scripts/run_global_forum_index_search.py) uses the official Brave **web search** endpoint only, with sequential requests, a minimum 1-second inter-request delay, a maximum 1,000 calls per dispatch, a configurable response cap and an immediate stop on 401/402/403/429. Default is **20** index calls. Results are marked `brave_web_index_only` and `partial_external_index_no_negative_evidence` and uploaded as artifacts. The workflow does **not** crawl any individual forum, run a native forum API, authenticate to Reddit, ask an AI to summarize full third-party content or bypass access limitations. It may incur vendor/API charges. No API key is stored in source.

**2026 correction:** Brave's documented default `search_lang=en` can bias multilingual results. The index executor now passes a per-forum two-letter language hint when available and uses `spellcheck=false` to reduce accidental rewrites of symbolic identifiers. Its output still needs first-party verification, especially for mixed-language markets. [API parameters](https://api-dashboard.search.brave.com/api-reference/web/search/get).

**Why Brave as the first indexed adapter:** Its current first-party documentation describes a supported official web-search API with authenticated, bounded `q` requests: https://api-dashboard.search.brave.com/api-reference/web/search/get . Google's legacy Custom Search JSON API is **closed to new customers** and slated for transition, so building new automation around it would create a short-lived dependency: https://developers.google.com/custom-search/v1/overview .

Later native workers can consume the same task JSONL and supply approved adapters. Execute in groups by **host** rather than one parallel GHA worker per task, to keep limits and prevent hammering the same domain. An eventual matrix with **8–32 host-shards per run**, per-host token buckets, persisted cursor/checkpoint, bounded retries/backoff, API-credential gating and per-host circuit breakers is preferable to 483 simultaneous workers. GitHub Actions has a documented **256 matrix-job limit**; a domain-sharded strategy avoids exceeding it. Check actual workflow concurrency and cost before enabling high-volume retrieval. The current implementation deliberately does not imply native workers exist.

## Platform mechanisms and technical references

- Discourse `GET /search.json?q=...`: https://docs.discourse.org/ (public status and actual host must still be tested).
- phpBB native query fields, all/any, titles/messages, date and forum scope: https://www.phpbb.com/support/docs/en/3.3/ug/userguide/user_search_forums_topics/ .
- XenForo REST credentials and per-install setup: https://docs.xenforo.com/manual/reference/rest-api . Its search route documentation and discussions should **not** be assumed to represent an uncredentialed, working search endpoint: https://xenforo.com/community/threads/api-endpoints-for-searching-threads-posts.207549/ .
- Invision Community REST per-site keys/OAuth: https://invisioncommunity.com/developers/api-reference/ .
- Stack Exchange advanced search official API: https://api.stackexchange.com/docs/advanced-search .
- Reddit current data restrictions, authentication and permission: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki and https://redditinc.com/policies/data-api-terms .
- Steam discussions native search support: https://steamcommunity.com/discussions/ (not an exhaustiveness guarantee).
- Internet Archive CDX URL scopes and response format: https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md .
- Brave Search API query and authentication: https://api-dashboard.search.brave.com/api-reference/web/search/get .
- GitHub Actions runner and matrix limits: https://docs.github.com/en/actions/reference/limits .

## Known gaps and next autonomous research tasks

**Immediate:** Consult the [archival corpus and site-specific mirror audit](global-gaming-forum-archives-and-mirrors.md) for Steam SPUF, UOL rescue, PTTweb, GameFAQs, Arquivo.pt and Common Crawl; verify actual forum capture coverage rather than presuming archives. Fingerprint the 239 `forum_native_probe` sites and the uncertain platform hints, correcting dead URLs and identifying true discussion boards; no changes to sticker data. Verify the 411 `C` rows before investing in expensive native searches. For each site, collect explicit dated example thread and actual search UI/API witness. The number of unprobed sites must fall over time, not remain disguised behind a universal fallback.

**Then:** Build separately approved native adapters by platform family (Discourse first, then phpBB, Invision/XenForo UIs and regional hosts) with fixture-based parser tests. Add resumable search cursors and source evidence schemas. Pilot across small language-diverse forums and measure retrieval recall against known historical positive controls, **not just counts of indexed hits**. A failure to find a known positive control is a concrete signal to improve the method.

**Finally:** Add cross-engine overlap audits, time-window completeness reports, missing-media tracking and a campaign ledger. For claims of a comprehensive search, the ledger must clearly name what was scanned, what was blocked and what remains unknown. Avoid treating percentages of indexed sites as percentages of possible historical posts.

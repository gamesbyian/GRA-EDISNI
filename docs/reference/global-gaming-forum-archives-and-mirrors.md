# Historical archives and mirrors for difficult gaming-forum searches

**Status:** source-supported architectural research, 12 October 2026 (America/Edmonton).  
**Source directories:** [original 483 sites](../../data/reference/global-gaming-forums.tsv), [primary query routes](../../data/reference/global-gaming-forum-search-routing.tsv), and **[483-item archival fallback matrix](../../data/reference/global-gaming-forum-archive-routes.tsv)**.  
**Parent architecture:** [global-gaming-forum-search-methods.md](global-gaming-forum-search-methods.md).  
**Research mode:** DISCOVER/DEVELOP; not a finding that 483 hosts are archived or searchable.  
**Question:** Where a site's current search fails, which indexed archives, mirrors, rescue datasets and corpus methods can retrieve its historical discussion for arbitrary future terms?

## What has been established, and what has not

**Established:** several *services and genuinely existing collections* can serve as an alternative to a site's own search. The highest-value newly identified forum-specific cases are ArchiveTeam's UOL Forums rescue (Brazil, 2018–19), ArchiveTeam's Steam Powered User Forums/“SPUF” rescue (2017; distinct from Steam Community Discussions), PTTweb.cc for PTT game boards, and GameFAQs' own permanent topic archives for certain modern game boards. Arquivo.pt is a rare public web archive with **actual archived-page full-text search**, not merely a URL history index. Common Crawl stores WARC and WET corpus content, so captured forum pages can be indexed offline. Archive.ph offers human-searchable snapshot URL/host discovery.

**Not established:** no live 483-host CDX sweep, capture-density census, bulk WARCs download or end-to-end recall evaluation was conducted in this session. The presence of a host name in the Wayback or Common Crawl index is not verified in this matrix. Equally, identifying ArchiveTeam's rescue project does **not** establish that its files can be downloaded from a GitHub Actions runner or freely republished under all circumstances. Every row's `host_capture_status` is deliberately `not_checked`. These are *candidate retrieval routes*, with different levels of supporting evidence.

**Research correction:** the prior forum-search plan had **not fully researched** mirrors, archive full-text systems, offsite rescue collections, language-specific archival search or Reddit's latest research-access rules. This document addresses those omissions using current first-party references, without claiming an exhaustive global audit or a deployed all-corpus scraper.

## Confirmed archive, mirror and dataset services

| Route | Searches **text** or **URLs**? | Application and concrete limits | Source |
|---|---|---|---|
| **Internet Archive Wayback CDX** | **URL/capture metadata**, not a general full-text index | Query `url`, `matchType=prefix/host/domain`, `from`, `to`, `fl`, `filter`, `collapse`, pagination/resume when supported. Then fetch replayable captures and index accessible text separately. | [CDX server reference](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md); [Internet Archive's own warning](https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine) |
| **Common Crawl CDXJ / URL Index** | Indexed **URLs and WARC locations**; content obtainable separately | Run per-crawl CDXJ probes; for bulk host/period enumeration prefer partitioned Parquet URL Index via DuckDB/Athena. Retrieve selected WARC records with location/offset/length and HTTP range requests, or obtain WET extracted text where present. **A capture is a sample**, not an entire forum. | [CDXJ](https://www.commoncrawl.org/cdxj-index), [URL Index](https://commoncrawl.org/url-index), [WARC/WAT/WET](https://commoncrawl.org/get-started) |
| **Arquivo.pt** | Actual archived **full-text** and URL/version search | First choice for relevant Portuguese/Portuguese-speaking forums and complementary historical sampling elsewhere. Query `site:`, exact phrases, time windows; `/textsearch` API is documented but per-version parameters and limits require verifying before writing a worker. Does not guarantee it harvested a particular Brazilian or non-.pt site. | [Arquivo.pt advanced search](https://sobre.arquivo.pt/en/help/advanced-search/), [official API](https://sobre.arquivo.pt/en/new-api-to-search-arquivo-pt/), [API CDXJ bulk collection](https://sobre.arquivo.pt/en/tag/api/) |
| **Archive.ph / archive.today** | Manual snapshot discovery by **host, URL, wildcard**; no dependable general text-search API established here | Secondary human-oriented snapshot check, especially vanished pages and media. Do not automate guessed endpoints or assert that host search is full-text. | [Archive.ph query guidance on homepage](https://archive.ph/) |
| **Library of Congress Web Archive** | Collection metadata and **URL-based archive discovery**, no general full-text across captures | Useful for specific US sites *if collection targeted them*. Access and collection coverage can be restricted. | [LoC search guidance](https://www.loc.gov/programs/web-archiving/for-researchers/searching-the-web-archive/), [full-text limitation](https://www.loc.gov/programs/web-archiving/for-researchers/) |
| **British Library UK Web Archive** | Not presently accessible to ordinary online users | May eventually offer historical UK gaming material, but **as of this audit the British Library reports access unavailable**. Do not include as active automated fallback. | [British Library October 2026 service status](https://www.bl.uk/services/legal-deposit/web-archiving) |
| **National archives and selective web collections** | Case-by-case URL or full-text search | Look for national collections, historical forums and local-language portals; confirm collections actually contain games discussions. The UK Government Web Archive supports full-text search but targets government sites, so usually **irrelevant** to gaming forums. | [UK Government archive search](https://www.nationalarchives.gov.uk/webarchive/find-a-website/how-to-find-an-archived-website/) |
| **Authorized live capture with Browsertrix / WACZ** | A new capture of **presently available content** | Useful for making a repeatable, legally permitted current snapshot. It cannot restore posts not accessible today, and browser screenshots of a thread are not an archival source for content already lost. | [Browsertrix crawl scopes](https://docs.browsertrix.com/user-guide/workflow-setup/), [WACZ items](https://docs.browsertrix.com/user-guide/archived-items/) |

### Concrete historical rescue cases

**Brazil, UOL Jogos / UOL Forums**: [ArchiveTeam UOL Forums](https://wiki.archiveteam.org/index.php/UOL_Forums) documents the December 2018 read-only transition and January 2019 shutdown. Its rescue tracked the *Jogos* and separate *beta Jogos* boards. The project estimates about **99% of requested ranges saved by shutdown**, but also discloses unretrieved items and trouble with exceptionally long threads. Names `archiveteam_uol` and `archiveteam_uolforum` identify deposited dataset collections; **content accessibility, record count and searchable text are not independently validated here**. This is a high-priority archive acquisition/inspection task because it directly covers the relevant INSIDE 2016–2019 window.

**Original Steam Powered User Forums (“SPUF”)**: [ArchiveTeam Steam Users' Forums](https://wiki.archiveteam.org/index.php/Steam_Users%27_Forums) records Valve's June 2017 shutdown and preservation datasets `archiveteam_steamforums`, `steamforums_spuf_archive_201706` and `steamforums_spuf_indices_201706`. It reportedly contained >1 million threads and 13 million posts. **Important:** SPUF was a *separate legacy forum*. These rescued pages are not mirrors of `steamcommunity.com/app/304430/discussions/` or the modern per-game Steam discussions. Search both corpus families, but never substitute one for the other. The INSIDE release in 2016 makes the historical SPUF time period relevant as a possible parallel channel, not proof of an INSIDE thread.

**Japanese 5ch / 2ch historical search:** [zzzsearch](https://zzzsearch.com/2ch/) currently displays a full-text search form which claims scope across original 5ch, Open2ch, 2ch.sc and older saved logs such as mimizun. [search2ch.info](https://search2ch.info/) separately advertises full-text search of historical and 1,000-reply threads; [kako.5ch.io](https://kako.5ch.io/) lists historical thread boards. These services may be more searchable than 5ch's own shifting platform, but their actual returned matches and 2016–2026 recall are untested. **2026 caveat:** a Japanese analysis dated April 30 reports 5ch's move to `5ch.io` on March 6, 2026 and advises caution about stability of older third-party engines ([Japanese report](https://www.kesu.jp/articles/surveillance/article-20240318/)). Search both historic `5ch.net` and current `5ch.io` URL lineages, and deduplicate source threads.

**Taiwan, PTT boards:** [PTTweb.cc](https://www.pttweb.cc/ptt-search) openly states that its search can cover `ptt.cc`, `pttweb.cc`, or both, backed by Google-powered retrieval; its interface also exposes native per-board title search. [PTT commenters explicitly refer to it as a backup](https://www.ptt.cc/bbs/ask/M.1709532503.A.D05.html), and `disp.cc` contains selective republications. **Do not conflate mirrored results with independent eyewitnesses.** Mirrors can retain content authors have deleted; record the deletion/provenance issue and do not systematically collect removed personal material as a workaround.

**GameFAQs:** [Game Board Archiving Active](https://gamefaqs.gamespot.com/boards/6-gamefaqs-announcements/41276959) documents native permanent archiving of **modern game-board** threads starting in 2008. [GameFAQs Archive](https://www.gamefaqsarchive.com/) exists as an independent, curator-contributed archive concentrated on historical topics, *not* a comprehensive mirror of the 2016–2026 forums. Prioritize the original platform's archived title boards, then external indexes and archived captures; check whether the specific board category has purging rather than universal retention.

## Per-forum identification and fallback decisions

The [483-row archival matrix](../../data/reference/global-gaming-forum-archive-routes.tsv) contains one-for-one keys `community` and `original_url`, a preferred historical search route, additional archives, known mirrored or rescued corpus and source link (where established), confidence/availability flags, Wayback URL, Common Crawl entry point, priority and handling notes.

**Evidence vocabulary:**
- `source_assurance=project_documented_data_not_inspected`: a specific rescue collection is documented, but bytes and searchability are not yet witnessed.
- `source_assurance=mirror_search_documented`: a working public mirror search is described by the service, without a promise of full historical coverage.
- `source_assurance=official_archiving_documented`: first-party site describes its retention policy for some boards.
- `source_assurance=global_service_only_no_host_capture_checked`: global archive exists, **forum capture unverified**.
- `source_assurance=archive_service_documented_host_not_checked`: full-text archive search exists, **host-specific capture unverified**.
- `host_capture_status=not_checked` applies to **all 483 rows**, until a probe actually establishes captures and date boundaries.

**Prioritize** known rescues and historical archives (P0), per-game and long-lived discussion boards that might contain first-hand INSIDE clues (P1), general or hardware discovery (P2), then weak article comment pages (P3). Priorities are *workload suggestions*, not probabilities of finding the solution.

**Special cohorts that need distinct treatment:**

- **Steam (6 entries):** game-id native browsing + search index + Wayback/Common Crawl for modern discussions; SPUF as an *additional historically adjacent dataset* only.
- **Reddit (56 entries):** web index discovery + permitted snapshots for source verification, and Reddit's authorized access process for any automated systematic research, rather than pretending that Pushshift/other bulk dumps are universally permitted.
- **PTT (7 entries):** native PTT board + PTTweb's independent search/mirror + Wayback/CDX; precise board name remains part of every query.
- **GameFAQs:** original per-title archived thread pages + external page index; old curator archive is optional and incomplete.
- **UOL Forums:** inspect ArchiveTeam deposited data and its recoverability before wasting effort on now-dead site search.
- **Portuguese-language and Portuguese-origin sites:** favor Arquivo.pt **full-text** in addition to normal Wayback/Common Crawl; 12 rows route Arquivo.pt first in this inventory, with others retaining it as a secondary lead. Neither country nor language predicts whether a page was actually captured.
- **Japanese 5ch (six entries):** [zzzsearch](https://zzzsearch.com/2ch/) exposes a named full-text cross-search UI for 5ch, Open2ch, 2ch.sc and multiple old-log providers. [search2ch.info](https://search2ch.info/) independently describes itself as a 5ch/2ch full-text historical search. [Kakolog at kako.5ch.io](https://kako.5ch.io/) exposes a board/thread historical index (its visible old thread timestamps suggest coverage is uneven or historical). These are **documented services, not verified exhaustive archives**, and 5ch's 2026 domain switch from .net to .io may compromise coverage. Check both Japanese original/mirror and English equivalents. Do **not** confuse Japanese 2ch boards with the unrelated Russian 2ch.hk.
- **Korean DC Inside:** native search and gallery indexing, with a [third-party research/browser helper](https://github.com/sendhyun/dcinside-deep-search) that follows visible "next search" pagination by user action; its own documentation warns the software may contain errors and it has not been audited as safe for unattended GHA operation. No trustworthy independent full historical corpus confirmed.
- **Chinese Tieba, Vietnamese gaming sites, other Brazilian closures and publisher migrations:** do not promote plausible mirrors without a defensible source. Start with URL/citation discovery and archived originals; verify any candidate mirror's origin, chronology, capture scope and publication status before importing.

## Recommended latest practical technical stack

### Discovery: cheap, high recall, bounded

Use an **official licensed web-search API** (current Brave endpoint or another contracted search engine) for `site:`, `intitle:`, `inbody:`, exact quotation, language-specific translations, and controlled date windows. [Brave documents operators](https://api-dashboard.search.brave.com/documentation/resources/search-operators) and [API parameters](https://api-dashboard.search.brave.com/api-reference/web/search/get), including `search_lang`, `country`, `freshness` and `spellcheck`. Importantly, **index page-age/date is not necessarily the original posting date**, and search phrases with slash, dash or leading zeros may be rewritten/tokenized. For exact identifiers, explicitly disable automatic spellchecking, retain the raw term, try alternate query operators, and independently verify in the page body.

**Current correction in code:** the query-planning script now includes the original forum language/region per task; the bounded Brave executor uses `spellcheck=false` and a two-letter `search_lang` hint where available. This improves multilingual recall over the original API adapter's undocumented reliance on an English default. It still requires tests with actual provider responses and deliberately does not infer a verified search outcome.

### Recovery: archive URL enumeration, selective record fetching, local index

1. Search **site-native available threads** where lawful and feasible, and collect timestamped positive controls.
2. Query **Wayback CDX** for archived URL/capture inventories by host/path and date. The CDX `fl`, `filter`, `collapse`, `matchType`, `from`/`to` parameters reduce discovery noise. Capture counts, status and MIME are coverage metadata, not textual matches. Keep different 2016–2024 snapshot dates.
3. Query **Common Crawl CDXJ** for a small number of target URLs/periods. For thousands of forum pages, switch to **partitioned Parquet URL Index** via DuckDB or Athena, avoiding excessive calls to a public CDXJ endpoint. Restrict partitions by crawl and host. The commoncrawl URL index identifies WARC storage/offset/length; fetch *selected* records or WET text, respecting terms and provider limits.
4. Search **Arquivo.pt's true archived full-text index** across dates and domains; use its official UI or documented `/textsearch` API. Validate parameter schema against the live version. Its multi-language holdings are complementary but incomplete.
5. For a documented rescue dataset, download only if access and rights permit; stream `WARC` or `WET` and create a **local text index**. [warcio](https://github.com/webrecorder/warcio) can iterate WARC/ARC records. Detect errors, revisit records, charset and non-text responses; do not extract only the Internet Archive replay wrapper.
6. For allowed current capture, use browser-based archiving (e.g., Browsertrix) under approved per-host scope with identified user-agent, request pacing and max-page budgets. This captures new evidence; does not resurrect inaccessible old content.

### Offline search against a preserved corpus

Maintain a raw/immutable document store keyed by `source_system, original_url, capture_timestamp, content_digest`, with extracted text, original language, original date, archive crawl date and collection license stored *separately*. Never replace original text with an English translation or LLM-generated summary.

Build at least **two complementary indexes**:

- Unicode language-aware token search (e.g. [OpenSearch ICU analyzer](https://docs.opensearch.org/latest/analyzers/language-analyzers/icu/) or SQLite FTS5 `unicode61`) for natural language in English, German, French, Chinese, Japanese, Korean, Thai and Arabic; maintain explicit locale/transliteration variants.
- **Exact substring, byte-wise and regular-expression search** for symbolic clues such as `/043`, `A10N7`, `B02`, `111/111/100` and serial-number typography. A full-text analyzer may split `/043` into `043` or remove punctuation. [SQLite FTS5 trigram](https://www.sqlite.org/fts5.html) supports substring retrieval, but **queries shorter than three Unicode characters require a linear scan or custom small-n-gram index**. Always preserve a raw exact-match pass.

Then add cross-language query expansions with traceable input terms; morphology, transliterations and spelling variants. For each source hit, capture minimal original snippets, dates, canonical URLs, WARC location/capture timestamps, original media URL and source lineage. Use semantic retrieval/AI only for reranking, topic classification and translating after exact/lexical collection. An LLM may identify plausible posts missed by literal terms but cannot attest a site was comprehensively searched.

### Quantifying completeness honestly

For each `host × time-window × corpus × query` record:

`captured_url_count`, `unique_article_count`, `first_capture`, `last_capture`, `material_downloaded`, `fulltext_extracted`, `indexed`, `earliest_original_post_date`, `latest_original_post_date`, `results`, `truncated`, `access_barrier`, `source_history`, `known_positive_controls_found`, `index_compared`, `remaining_holes`.

Run at least **one documented known-hit positive control** in each chosen language/engine cohort before treating a zero-result query as meaningful. Compare indexes and archives by canonical thread IDs, record both complementary coverage and duplicated evidence, and distinguish Wayback timestamp from post timestamp. A captured forum landing page in 2024 doesn't prove archived posts existed in 2019; a 2026 edit doesn't mean a 2016 post was newly authored then. No number of zero results can certify absence from posts that were never published to crawlers.

## GHA automation design: what belongs in a job

- One offline **planning** stage outputs `(forum, input_term, language, native_method, historical_route, index_query, source_witness, capture_status, access_gate)`. This can run cheaply whenever terms change. The existing [planner](../../scripts/plan_global_forum_searches.py) now joins archive routes on exact forum+URL; this refuses silent directory drift.
- One opt-in **licensed index** stage (existing Brave worker) may be budgeted separately. **No unrestricted site crawl** should be mixed with search API calls. Per-host permission and expected volume gate native/archive content acquisition.
- **CDX/URL-index probe stage:** future bounded workers request metadata only, record `capture_status`, timestamps, MIME, URLs and service errors. They do not guess that a Wayback wildcard listing means a full saved thread. ArchiveTeam rescue intake is a human/manual data-access validation until dataset location and rights are known.
- **WARC/WET and on-disk search stage:** separate one-off, checkpointed archival-analysis jobs, partitioned by host and capture date. Content can be huge; GitHub Actions' ephemeral disk and artifact retention are unsuitable for a permanent corpus. Store reusable indexed snapshots outside the repo, with checksums and retrieval manifests, subject to terms, then publish only compact findings/ledger as source-safe outputs.
- **AI relevance stage:** run only on rights-cleared, minimally retained text; redact private information, respect removed-post preferences, keep every claim linked to the original capture. No background autonomous access to Reddit research APIs without eligibility/permission; no CAPTCHA solving or proxy cycling.

This architecture is a roadmap, not a claim the full archive-index, WARC or native workers have shipped. Avoid 483 simultaneous forum visits, broad cross-domain crawling and fixed "100% coverage" thresholds when corpus ground truth is missing.

## 2026 platform policy correction: Reddit

As of [Reddit's May 2026 platform guidance](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data), Reddit states that its **official authorized avenue for academic research** is the *Reddit for Researchers* program; ordinary developer API permission does not automatically authorize systematic research. [Program eligibility, updated October 2026](https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program), emphasizes accredited-university affiliation, formal proposal, ethics documentation and institutional sponsorship (with narrow other exceptions). [Data API terms](https://redditinc.com/policies/data-api-terms) were revised July 2026. Do not label all 56 subreddit rows as ready-to-use `reddit_oauth_search`; the directory's per-site search matrix has been corrected to `reddit_research_access_gate` and `approval_required_no_native_worker`.

For nonacademic/hobbyist projects the specific authorized path must be checked before executing API-based bulk collection. Public search-engine *discovery* still requires adherence to content rights, access terms and deletion expectations; an unofficial Pushshift-style dump should not silently become the default workaround.

## Source audit and next milestones

**Source review completed:** direct first-party references for Wayback/CDX, Common Crawl CDXJ/URL Index and WARC/WET, Arquivo.pt APIs, Archive.ph host/URL lookup, ArchiveTeam SPUF/UOL projects, PTTweb.cc, native GameFAQs archives, Reddit 2026 access guidance, Browsertrix, SQLite/OpenSearch multilingual/substring search. This is a substantial upgrade over the previous route heuristic, **not a globally exhaustive survey of national archives or all site-specific mirrors**.

Next bounded tests, ranked by expected value:

1. **UOL Jogos rescue (P0)**: locate and verify actual ArchiveTeam WARC items; sample several 2016–2019 game-thread records; determine usage restrictions and ability to build a local index.
2. **INSIDE's 2016 Steam Community (P0)**: Wayback CDX prefix on app 304430 and Common Crawl URL index for selected crawls; benchmark live index against a known 2016 thread; search SPUF separately only as adjacent historic material.
3. **PTT/Bahamut (P0)**: compare PTT original vs PTTweb for one confirmed ordinary public game thread, then inspect Bahamut native search and archived URL inventory without assuming a mirror exists.
4. **Arquivopt Portuguese (P1)**: verify `site:` + full-text phrase searches against two dated positive controls for Brazilian/Portuguese gaming sites, documenting missing coverage as well as matches.
5. **GameFAQs historical topic archive (P1)**: identify INSIDE board; verify scope and 2016 post search versus ordinary current search and third-party historical curator archive.
6. **International samples (P1–P2)**: find 1–2 named archives/mirrors with source-confirmed preserved threads for Russian, Japanese, Korean and Vietnamese sites; add those only after inspection.
7. **Recall audit (P1)**: run frozen multilingual positive controls, compare native/Brave/Wayback/Arquivo.pt/CC overlap and count real newly recovered unique threads. Do not treat no index hit as a negative finding.

**Implementation gate:** do not promote a route to `host_captures_confirmed` or `search_works` without recording a query, observed returned URL, retrieval timestamp and original date source. A public archive *service* is a tool; a verified capture is evidence.

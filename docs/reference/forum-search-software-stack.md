# Software stack for worldwide forum search

**Status:** first offline indexing component implemented; optional retrieval tools evaluated (2026-10-12).  
**Scope:** INSIDE historical discussions, arbitrary Unicode terms, symbolic identifiers, 491 candidate forum locations, approved archives.  
**Related:** [per-site retrieval matrix](../../data/reference/global-gaming-forum-search-routing.tsv), [491 archive routes](../../data/reference/global-gaming-forum-archive-routes.tsv), [forum search methodology](global-gaming-forum-search-methods.md).

## Practical recommendation

Do **not** deploy a 491-domain crawler or a managed search server as the first step. The repository already produces explicit per-site search tasks and has a licensed web-index fallback. What was missing is a **persistent, independently searchable collection** of the public source text actually recovered by those workers. Search data once at acquisition, then run subsequent arbitrary queries offline for essentially zero per-query retrieval cost.

### Deployed in this repository

**SQLite FTS5 + Python standard library**, at [scripts/forum_local_search.py](../../scripts/forum_local_search.py), with optional, pinned **warcio 1.8.1** for WARC/ARC ingestion ([requirements](../../requirements-forum-archives.txt)). SQLite ships with Python on ordinary GitHub Actions Ubuntu runners, although FTS5/trigram availability is checked at runtime.

The tool creates a portable local SQLite file holding the original URL, host, source category, content hash, capture timestamp, original post date when established, forum, language, and extracted text. It builds two complementary indexes:

- **Trigram search with exact-substring verification:** accelerated literal fragments three or more Unicode characters long, including slash, dash, leading zeroes and multilingual text. A second \`instr(...)\` check prevents wildcard/index tokenization from being mistaken for a literal match. **One- and two-character queries**, or queries containing SQL LIKE wildcard symbols \`%\` or \`_\`, fall back to an exact linear scan rather than silently returning an incomplete result.
- **Unicode61 FTS5 token phrases:** useful for natural-language phrase queries, but unsuitable for proving exact punctuation, mixed writing systems or every CJK token boundary. Use \`--mode exact\` by default for codes or names with punctuation.

The tool ingests **prepared JSONL records** or locally supplied WARC/ARC (including compressed WARC) archives. Its WARC importer accepts public HTTP(S) 2xx HTML captures, applies a size and record cap, extracts all visible page text rather than assuming news-article extraction works on threaded forums, and labels records as \`warc_capture\`. That broad extractor may include navigation and repeated sidebars; future site-specific adapters should distinguish authors, post IDs and bodies.

**Every hit identifies its data source.** A capture date is never automatically treated as the date of a forum post. Identical content in multiple URLs or snapshots retains separate provenance, and importing exactly the same URL/capture/content again is idempotent. No live forum requests occur, and the database contains only materials supplied locally.

Usage:

\`\`\`bash
# Optional WARC reader, not needed for JSONL ingestion or searching
python -m pip install -r requirements-forum-archives.txt

# Ingest previously downloaded/authorized public forum captures
python scripts/forum_local_search.py --db /tmp/inside-forums.sqlite \
  ingest-warc --input /research/archives/public-forums.warc.gz --max-records 10000

# Or ingest rights-cleared, pre-extracted forum pages as JSONL
python scripts/forum_local_search.py --db /tmp/inside-forums.sqlite \
  ingest-jsonl --input /research/approved-forum-pages.jsonl

# Exact symbolic searches across all ingested source text
python scripts/forum_local_search.py --db /tmp/inside-forums.sqlite search \
  --term '/043' --term 'A10N7' --term 'プレイデッド' --term '貼紙'

# Ordinary contiguous token phrase, or host-restricted case-insensitive search
python scripts/forum_local_search.py --db /tmp/inside-forums.sqlite search \
  --mode phrase --term 'collector edition'
python scripts/forum_local_search.py --db /tmp/inside-forums.sqlite search \
  --term 'playdead' --ignore-case --host forum.example.org
\`\`\`

Sample JSONL input (one record per line):

\`\`\`json
{"url":"https://example.org/thread/123","forum":"Example Games","text":"Original post text /043","title":"INSIDE collector edition","source_kind":"verified_thread","language":"en","captured_at":"2020-06-10","original_post_date":"2019-02-01","source_collection":"named-public-research-collection"}
\`\`\`

Search returns JSON objects; \`coverage=only_documents_present_in_local_database\` and \`scope=offline_ingested_corpus_only\`. No count is described as a worldwide forum search. The [synthetic regression suite](../../tests/test_forum_local_search.py) includes symbolic strings, East Asian text, language casefolding, capture/post-date separation, deduplication and compressed WARC ingestion. [CI workflow](../../.github/workflows/forum-local-corpus-tests.yml) runs those tests when relevant files change.

**Data lifecycle:** do not commit a massive local SQLite database, third-party WARC, copyrighted posts or personal data into git. Store source archives in access-controlled artifact storage, subject to permitted retention and licensing; GitHub Actions artifacts have a retention period and are not a permanent source-of-truth storage service. Commit compact manifests, checksums, source links and rights-cleared extracts only. Use the same corpus digest and import version across comparison runs.

**Post-retrieval source triage:** [the CE index-hit triager](../../scripts/triage_inside_ce_index_results.py) normalizes source URLs, keeps Reddit post-level identity distinct from its thread, and warns about the separately marketed standalone PS4 edition. It generates an *unreviewed* queue after authorized searches and never creates a physical sticker confirmation. See [evidence controls](inside-ce-edition-product-differentiation-and-triage.md).

## Evaluated tools to integrate next (not deployed yet)

| Priority | Software | Why it matters | Activation decision |
|---|---|---|---|
| 1 | [cdx_toolkit](https://github.com/commoncrawl/cdx_toolkit) | Unified CDX discovery for both Internet Archive and Common Crawl; can select and save WARC subsets | Install as a separate **metadata first** worker with proven 2016–2024 positive-control capture results. Never confuse URL matches with archived post-text matches. |
| 1 | [DuckDB](https://duckdb.org/) | SQL over Common Crawl's Parquet URL Index, much more efficient than issuing huge numbers of individual CDX requests | Use once CDX hit discovery becomes a throughput bottleneck. Partition by crawl and host; watch S3/Athena/transfer costs. |
| 1 | [ripgrep-all](https://github.com/phiresky/ripgrep-all) and [ripgrep](https://github.com/BurntSushi/ripgrep) | Immediate reconnaissance through recovered ZIP, PDF, HTML, document and other archive directories; caches extraction | Run once on archive acquisition, then import stable textual findings into SQLite. Do not treat a search in compressed WARC members as a guaranteed structured parse. |
| 2 | [Trafilatura](https://trafilatura.readthedocs.io/) | Extracts article body and optionally comments from HTML | Test against real forum page fixture: article-focused heuristics can silently discard reply content. Preserve raw page/visible text as a recall control. |
| 2 | [Scrapy AutoThrottle](https://docs.scrapy.org/en/latest/topics/autothrottle.html) | Per-domain concurrency, conservative pacing, request scheduling and resumable item processing | Only for sites whose rules allow automated public collection. No proxy rotation, CAPTCHA circumvention or bypassing login restrictions. |
| 2 | [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright) | Javascript-rendered public forum text, integrated with Scrapy's scheduler | Add browser overhead only when static HTML and authorized native APIs fail and automation is allowed. |
| 2 | [Browsertrix](https://docs.browsertrix.com/) / [pywb](https://github.com/webrecorder/pywb) | Reproducible capture and replay of publicly available pages | Useful for audit/provenance and reprocessing, but neither restores missing historical pages. |
| 3 | [OpenSearch](https://opensearch.org/) or [Tantivy](https://github.com/quickwit-oss/tantivy) | Bigger BM25/multilingual ranking and facet indexes | Defer until measured SQLite corpus/query size requires it. They do **not** replace exact substring search. |
| 3 | [SearXNG](https://docs.searxng.org/) | Aggregate metasearch UI | Not a substitute for authorized provider APIs or a complete historical corpus. Provider reliability and terms still apply. |

**AI's proper layer:** cluster or classify already discovered original threads, translate while preserving originals, detect the same screenshot or quotation reposted in different languages, and propose query expansions. Avoid running embeddings-first as the only retrieval technique: encrypted codes, serial numbers and short symbolic strings frequently have no useful semantic similarity representation. Require lexical/exact candidate retrieval first and preserve original source lines.

## Correctness gates before scaling

1. **Known positives:** freeze dated forum posts known to contain a chosen term; run exact and natural-language searches against local ingested captures, and compare with native/forum/index search. Determine whether missing hits arise from uncaptured pages, extraction, indexing, query translation or ranking.
2. **Body-level fidelity:** test posts/replies from several platforms (Discourse, XenForo, phpBB, PTT, Japanese boards, Steam), with quoted content and image alt/link metadata. Plain visible HTML text may flatten reply structure; add source-specific parsers only after fixtures show need.
3. **Dedup and source lineage:** hash identical captures; never count a mirror or translation as an independent physical sticker sighting. Compare old/new posts by original thread ID and provenance, not merely URLs.
4. **Reproducibility:** pin parser/library versions when a campaign is launched; log WARC collection ID, bytes/checksum, SQLite schema revision, query mode, candidate universe, exact terms, and output count/truncation.
5. **Access and legal:** obey each forum's access conditions and archive rights, including current Reddit research program limitations. Scraping/crawling must never be used to defeat site protections.

### What this implementation does not claim

It **does not yet** fetch WARC records from CDX itself, run Scrapy, conduct unrestricted site crawls, collect all 491 communities, reconstruct authors from forum HTML, automate translations or persist a shared full corpus between GHA runs. The immediate shipped value is a reproducible, searchable local collection once allowed data are supplied. That directly addresses the expensive repeated-query problem while preserving a clear path to richer retrieval later.

## Primary software references

- [SQLite FTS5 trigram and short-query caveats](https://www.sqlite.org/fts5.html)
- [warcio streaming ARC/WARC](https://github.com/webrecorder/warcio)
- [Common Crawl URL Index and DuckDB/Athena](https://www.commoncrawl.org/url-index)
- [cdx_toolkit archived-page extraction](https://github.com/commoncrawl/cdx_toolkit)
- [ripgrep-all archive adapters](https://github.com/phiresky/ripgrep-all)
- [Scrapy AutoThrottle](https://docs.scrapy.org/en/latest/topics/autothrottle.html)
- [scrapy-playwright public JS rendering](https://github.com/scrapy-plugins/scrapy-playwright)
- [Trafilatura comments extraction](https://github.com/adbar/trafilatura)

# INSIDE CE historical retrieval: dated controls and bounded archive probes

**Mode:** DISCOVER. **State:** code + positive controls prepared, not a completed 483-forum archive scan. **Date:** 2026-10-13.

This is the second practical acquisition stage after [the 50-native-language CE ownership program](inside-ce-native-owner-hunt-2026-10-12.md) and [the offline SQLite/warcio indexer](forum-search-software-stack.md). It establishes whether known original **URLs** were captured in the 2016–2026 web archives before investing in WARC downloads and searches. The new [14-control dataset](../../data/reference/inside-ce-archive-positive-controls.tsv) includes five classes: known sticker serial discussions; first-person owners without sticker photos; preorder/non-owner negative controls; unverified original 2019 Twitch unboxing archive; and post-2019 marketplace/ARG discussions.

## Additional source-first findings

1. **Dec 23 2019 original owner comparison:** [r/PlaydeadsInside CE display case thread](https://www.reddit.com/r/PlaydeadsInside/comments/eers0x) reports **328**, and the same conversation separately identifies the **standard PS4 physical release** as lacking the CE wrapping and numbered sticker. Existing canonical [328](../../data/observations.csv) is **-328/D**, so the first-person comment is corroboration and a potential source-lineage link; it does not add a serial. Unlike an inferred product-spec comparison, this is a dated owner discussion.

2. **Mar 13 2020 original iam8bit waitlist sales:** [forum discussion](https://www.reddit.com/r/PlaydeadsInside/comments/fhvflq) includes a person reporting a successful purchase on the waiting list, but another participant says they **cancelled** after researching the contents. The former is a useful **unreconciled conditional buyer** pending a post/author-to-U/L cross-check, and the latter is an explicit **negative control**. The discussion also contains an existing owner who reports buying from eBay and giving up their waitlist place; no new sticker number is visible.

3. **2019 preorder / Oct 2026 lost follow-up:** [September 2019 CE preorder thread](https://www.reddit.com/r/PlaydeadsInside/comments/czc89n) includes a 2026 reply about thrown-away wrapping. The corresponding account is already canonical **lost L05**. This is a test of long-running ownership conversations, NOT a new recovered serial.

4. **Aug 13 2020 Brazil / Argentina-adjacent ARG awareness:** a [Brazilian self-identified Reddit participant](https://www.reddit.com/r/PlaydeadsInside/comments/i8tt42) mentions the printer, Morse and codes associated with the CE in English. It demonstrates an international ARG audience but **no CE ownership claim**. Search native Portuguese discussion venues rather than labeling non-English interest as physical evidence.

5. **Oct 11 2026 Brazilian-language search seed:** a [Portuguese CE owner solicitation](https://www.reddit.com/r/PlaydeadsInside/comments/1x3fe8h) asks whether anyone in Brazil owns the CE. This is a **community request**, not a recovered owner. It offers literal Portuguese phrasing for future regional forum work.

These five additions are in the [17-row evidence/lead ledger](../../data/reference/inside-ce-owner-search-ledger-2026-10-12.tsv). No new physically observed sticker, new validated residue or inferred production count was added.

## Metadata tool

The opt-in [Wayback CDX metadata probe](../../scripts/probe_inside_ce_wayback_cdx.py) selects dated source controls or the [483-forum archival matrix](../../data/reference/global-gaming-forum-archive-routes.tsv), and queries historical capture **metadata** only. It records original URL, timestamp, status, MIME, digest and sample limit; it **does not retrieve page bodies, inspect archived comments or claim full historical coverage**. Each original URL is searched independently within two broad windows, **2016–2020** and **2021–2026**. The maximum is 50 source URLs, two bounded CDX metadata requests per source, and a minimum two-second delay between actual requests. HTTP 429/403/401/503 stops the run, with no circumvention.

Example, offline planning (default):

```bash
python scripts/probe_inside_ce_wayback_cdx.py \
  --inventory controls --max-sources 6 \
  --output /tmp/inside-ce-cdx-plan.jsonl
python -m unittest discover -s tests -p test_inside_ce_wayback_cdx.py -v
```

Explicitly permitted network metadata lookups:

```bash
python scripts/probe_inside_ce_wayback_cdx.py \
  --inventory controls --max-sources 6 --per-window-limit 12 \
  --delay-seconds 2 --execute \
  --output /tmp/inside-ce-cdx-results.jsonl
```

The [GitHub Actions workflow](../../.github/workflows/inside-ce-archive-cdx.yml) runs synthetic tests and offline planning on code changes. Its manual `workflow_dispatch` can run real CDX metadata requests by choosing `execute=yes`; default remains `no` until an explicit run and access policy are resolved. Its uploaded JSONL file is a bounded **URL discovery artifact**, not a local corpus of post bodies.

## How to use any actual recovered captures

For each source, record whether a capture is present, its date, MIME and URL before trying to access it. A blank CDX list or HTTP error is **not evidence the original page was never archived**; URL canonicalization (mobile, old.reddit, http/https, queryless, shortlinks), robots/noarchive rules, path migrations and captures in other systems can change results. No systematically retrieved Reddit dataset should be inferred from public metadata. If an original archived page can be accessed and retained under relevant terms, import it using [scripts/forum_local_search.py](../../scripts/forum_local_search.py), preserving the post's own date separately from its capture date, and compare the exact sticker strings `328`, `306`, `171`, `125` and historical comment contents with the original thread.

**Remaining work:** acquire archival evidence with verified permissions, add URL-variant discovery and Common Crawl probes, capture/replay selected full HTML/WARC, measure how often native-web-archive passes recover a known historical positive control, and reconcile potentially distinct resale owners with the canonical physical/U/L ledger. Do not equate the number of successful CDX queries, forum pages or scanned languages with the number of unique CE copies.

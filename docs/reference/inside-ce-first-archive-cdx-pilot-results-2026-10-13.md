# First real historical INSIDE CE archive audit: observed results

**Date:** 2026-10-13. **Workflow:** [run 38441436347](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38441436347). **Artifact:** inside-ce-first-cdx-pilot, ID 11835003067. **Raw record:** inside-ce-cdx-initial-pilot.jsonl inside the GitHub Actions ZIP (downloaded and inspected). **Reproducible results:** [eight-row TSV](../../data/reference/inside-ce-first-cdx-observed-results-2026-10-13.tsv). **Probe:** [bounded CDX worker](../../scripts/probe_inside_ce_wayback_cdx.py).

## Measured archive availability

The PR-triggered one-shot workflow checked four dated, public, non-Reddit CE forum threads (controls C04, C14, C15, C16). It issued two bounded, status-200 Wayback CDX metadata requests per original URL, in windows 2016–2020 and 2021–2026, maximum eight capture rows each, separated by at least two seconds.

| Source | 2016–2020 | 2021–2026 |
|---|---|---|
| [C04: GameFAQs CE announcement discussion](https://gamefaqs.gamespot.com/boards/194097-inside/76386967) | **One successful 200/text-html capture metadata record** | TimeoutError |
| [C14: ResetEra RealDoll mention](https://www.resetera.com/threads/game-soundtracks-on-vinyl-45rpm-all-new-cartridge.446/page-16) | URLError | URLError |
| [C15: Cheap Ass Gamer April 2020 waitlist email](https://www.cheapassgamer.com/threads/official-collectors-edition-compilation-xi-2020.371308/page-17) | URLError | URLError |
| [C16: Cheap Ass Gamer March 2018 pre-order discussion](https://www.cheapassgamer.com/threads/indie-limited-obscure-physical-release-deals-and-discussion-thread.357745/page-79) | TimeoutError | Successful response with zero matching status-200 captures |

**Eight requests:** 2 successfully parsed metadata responses, **one actual capture record** and one empty capture-list response; 6 network/timeout errors (four URLError, two TimeoutError). The GHA job was green because it correctly recorded failures rather than pretending the entire data collection succeeded.

### Exact witnessed historical GameFAQs capture

- Original URL: https://gamefaqs.gamespot.com/boards/194097-inside/76386967
- Archived capture timestamp: **20190306051337**, meaning 2019-03-06 05:13:37 UTC.
- CDX response recorded status **200**, MIME **text/html**, digest **MHNUGWQN4H3TEOTD2U3ZFVLWYUZJHLTC**.
- Original discussion appeared in **2018**; archived capture occurred in **2019**. These dates must remain distinct.
- Provenance: workflow run 38441436347, artifact 11835003067, control C04, window 2016–2020.

**What this proves:** the Internet Archive has indexed at least one historical HTML capture of this specific thread URL. **What it does not prove:** that the original post body can be replayed today, that every reply was archived, that anyone received a CE, or that a sticker serial is recoverable. An attempt to retrieve the archived page body through our web interface did not succeed.

Likewise, a successful zero-result response for C16 in 2021–2026 only describes the **exact URL/window/filter and one provider**. It is not a global no-archive claim. Timeout and network failures provide **zero coverage evidence**.

## Implications and next executable checks

1. Try **one bounded retrieval of the exact known GameFAQs archived HTML**, recording HTTP result, capture timestamp and content digest, before attempting full site-wide crawling. Page text must be inspected and compared with the original thread. Do not treat the CDX digest as a newly discovered sticker clue.
2. Diagnose Wayback connectivity without aggressive retries, proxy cycling or CAPTCHA bypass. The present eight-request sample shows broad unattended archive probing would mostly produce **unknowns**, not credible absence claims.
3. Run cross-provider positive-control checks using Common Crawl's official CDXJ WARC locations, or archived full-text indexes such as Arquivo.pt where regionally appropriate.
4. Keep first-party text, historical capture metadata, first-person owner evidence, and physical sticker observations in **separate ledgers**. No sticker, polarity, production count or decoding-model result is altered by this metadata check.
5. Measure provider success, capture count, body recovery, extracted original text and known-hit recall independently. A single pass/fail 'searched' label is misleading.

For a new offline plan, use the existing probe with the dated control IDs C04,C14,C15,C16 and a per-window limit of eight. The completed live run explicitly enabled execution and allowed a two-second delay. New network attempts require their own bounded purpose and should be recorded independently of this baseline.

The artifact provides **the first observed archival capture witness**, not a recovered sticker or a completed archival full-text search.

## Follow-up: archived HTML actually retrieved (2026-10-13)

The original metadata-only finding was extended by a second, independently source-pinned one-record experiment, [GitHub Actions run 38443126621](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38443126621), artifact ID 11836207996. Its five synthetic checks all passed before it requested a single raw Wayback replay URL for the known 2019 GameFAQs capture.

**The archived HTML replay succeeded:** HTTP 200, response content type text/html;charset=utf-8, **38,546 downloaded bytes** and **3,081 characters of extracted visible text**. SHA256 of the returned HTML body was **20aafc7b365e81404a1c651c7ecede556a33635fc637dccdb586e8f0d49ff164**. Eight small keyword-context excerpts were retained as a research artifact. The original HTML is not committed to the repo.

The extracts included an original GameFAQs thread titled *Collector's Edition announced*, a forum author labeled JonnyBoyFF, the first-party iam8bit product URL, and contemporary Playdead and RealDoll discussion. They confirm **an actual retrievable period discussion**, not merely an archived URL listing. The extracted text **did not establish CE receipt or disclose a numbered sticker**. Do not infer that the named forum commenter was an owner merely because they shared the announcement.

Machine-readable immutable witness: [GameFAQs archived HTML recovery JSON](../../data/reference/inside-ce-gamefaqs-archived-html-recovery-2026-10-13.json). The recovery program and tests are [here](../../scripts/retrieve_inside_ce_known_wayback_body.py) and [here](../../tests/test_inside_ce_archive_body.py).

**This supersedes only the earlier statement that the archived page text could not be retrieved.** The 8 CDX request results above remain unchanged. It now makes sense to validate repeatable extraction and historical thread-body completeness on a few more positive controls, **not** to announce that 491 forum histories are archived or searched.

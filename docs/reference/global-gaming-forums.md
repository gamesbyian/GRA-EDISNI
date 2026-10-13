# Global video-game forums and discussion-board census

**Research mode:** DISCOVER (source discovery, not semantic validation)  
**Compiled:** 2026-10-12; updated 2026-10-13  
**Last updated:** 2026-10-13 (7 new verified gaming communities).  
**Temporal eligibility:** evidence of at least one relevant post/activity on or after **2014-10-12**, or potential eligibility awaiting confirmation  
**Data:** [global-gaming-forums.tsv](../../data/reference/global-gaming-forums.tsv)  
**Archival research and per-forum mirror routes:** [archive/mirror audit](global-gaming-forum-archives-and-mirrors.md) and [491-row historical fallback matrix](../../data/reference/global-gaming-forum-archive-routes.tsv). Where specific rescued datasets exist they are named, but no per-host capture availability has yet been established.  
**Per-forum search method:** [491-route search matrix](../../data/reference/global-gaming-forum-search-routing.tsv) and [AI/GitHub Actions search architecture](global-gaming-forum-search-methods.md). Each entry has a recommended method, fallback, search scope and access gate. Most assignments remain platform-level inferences requiring per-site verification; the plan/workflow does not itself certify searches.

## Purpose and coverage

This is a deliberately wide, language-inclusive search inventory for finding first-hand discussion of video games, including *INSIDE* (2016), Playdead, the collector's edition, visual clues and ARG-related puzzle mechanisms. It is **not a census of all extant forums on Earth** and is **not a list of 491 confirmed living forums**.

The expanded inventory contains **491 named community or discussion leads** distributed across **59 region/market labels** and **53 language-tag variants**. It spans large general forums, per-game forum indexes, national portals, enthusiast hardware/game subforums, game-specific support boards, independent game-development communities, archival boards, subreddits and sites with article comment discussions. Numerous entries still need historical activity, URL and topical verification.

| Status | Count on 2026-10-13 | Interpretation |
|---|---:|---|
| `V` | 76 | A relevant, publicly indexed discussion/forum surface or dated gaming discussion was found during discovery, sometimes through source/search excerpts. **Not a promise of current activity**, working logins or complete historical access. |
| `C` | 411 | Candidate forum or discussion lead. **Not independently established** to have video-game discussion on/after the cutoff or an accessible URL. May be an outdated URL, wrong category, redirected property or dead board. |
| `H` | 4 | Historical lead with claimed activity or closure inside the twelve-year eligibility window. Its listed URL may be a successor or historical-source page rather than a functional board. |

These are evidence-status codes, **not** probabilities, independent confirmations, or confidence scores. `V` is a discovery-level finding and still deserves an open-and-inspect check before citing a particular thread as evidence.

The TSV has six columns: `region`, `language`, `community`, `url`, `type`, `evidence_status`. `region` means geographic association/search market, **not** proof of hosting country, users' citizenship or linguistic exclusivity. Mixed language tags such as `en-tl` and `bn-en` are descriptive and not formal BCP 47 declarations.

## Inclusions and exclusions

**Primary target:** browser-accessible, persistent discussions on video games: conventional threaded forums; gaming categories inside broader boards; game-specific discussion forums; public message boards and imageboards; community question/answer boards. Eligibility for closed properties requires some evidence of activity **since 2014-10-12**. A source's *existence today* is not itself evidence of relevant gaming discussion today.

**Secondary search surfaces, distinguished by type:** Reddit communities (`subreddit`), game-centered discussion indexes (`game-index`), games press sites with discussions (`comments`), publisher/developer communities (`official`), and engines' development boards (`gamedev`). Their inclusion increases recall, but a mere magazine homepage in `comments` is **not verified to support discussion**. These should be triaged only after forum-quality targets.

**Not systematic targets:** chat-only private Discord servers, Telegram/WhatsApp groups, Facebook groups, video-only YouTube channels, commercial storefronts without persistent discussion threads, ordinary news pages without comments, gaming companies without community features, and known pre-2014 closed boards. Some uncertain candidates may nonetheless be misclassified; move or delete them upon inspection. The directory does not imply outreach to owners or players.

For closed, migrated and post-2014 historically relevant forums, use dated posts, archival snapshots, successor migrations and contemporaneous citation trails. The archive may be the only usable entry point. In particular, a recently closed forum can still contain 2016 INSIDE-era testimony.

### Type taxonomy

The `type` field distinguishes `general`, `game-index`, `game`, `platform`, `retro`, `hardware`, `MMO`, `genre`, `mobile`, `indie`, `modding`, `gamedev`, `ARG`, `official`, `subreddit`, `anonymous-board`, `discussion`, `qa`, `comments`, `archive-index`, `historic`, `simulation`, `sim-racing`, `deals`, `support` and other narrow labels. Classification represents a discovery use-case, not an independent site audit. Any `comments`, `deals` or `support` row is a **weak search lead** until a dated, pertinent user exchange is located.


**New firsthand-source addition (2026-10-13):** [Cheap Ass Gamer forums](https://www.cheapassgamer.com/forums/) have a live, verified XenForo search interface and a March 2018 INSIDE CE preorder statement, plus an April 2020 remaining-stock email reproduced in a separate thread. Source discussion witnesses: [2018 collector purchasing discussion](https://www.cheapassgamer.com/threads/indie-limited-obscure-physical-release-deals-and-discussion-thread.357745/page-79) and [2020 collector compilation](https://www.cheapassgamer.com/threads/official-collectors-edition-compilation-xi-2020.371308/page-17). No new sticker established.

## High-value verified discovery entry points

Links below are **examples with inspectable search/discussion landing pages**, rather than independent evidence that every listed subforum posted about *INSIDE*.

| Language/market | Discussion entry point | Reason to prioritize |
|---|---|---|
| Global / English | [INSIDE's Steam Discussions](https://steamcommunity.com/app/304430/discussions/) | Direct per-game discussion and 2016-era threads. |
| Global / English | [r/PlaydeadsInside](https://www.reddit.com/r/PlaydeadsInside/) | Known Playdead/INSIDE and collector's-edition ARG discussion. |
| Global / English | [GameFAQs Boards](https://gamefaqs.gamespot.com/boards), [ResetEra](https://www.resetera.com/forums/gaming-forum.7/), [NeoGAF](https://www.neogaf.com/forums/gaming-discussion.2/) | Historical and contemporary multi-game discussion. |
| Japanese | [5ch PC games](https://egg.5ch.io/game/), [5ch network games](https://itest.5ch.io/subback/netgame) | Broad, dated Japanese-language thread indexes; archive availability varies. |
| Chinese (Simplified) | [NGA](https://nga.cn/), [Baidu Tieba game categories](https://tieba.baidu.com/f/index/forumpark?ct=1&pci=0&pcn=%E6%B8%B8%E6%88%8F) | Many per-title and broad discussion communities; search native game name. |
| Chinese (Traditional) | [Bahamut](https://forum.gamer.com.tw/), [PTT Games](https://pttgamer.com/boards) | Highly relevant Taiwanese game-specific boards and archives. |
| Korean | [Ruliweb](https://bbs.ruliweb.com/), [DC Inside galleries](https://gall.dcinside.com/) | Distinct styles of discussions and index archives. |
| French | [jeuxvideo.com Forums](https://www.jeuxvideo.com/forums.htm), [Gamekult](https://www.gamekult.com/forum), [Hardware.fr](https://forum.hardware.fr/hfr/JeuxVideo/liste_sujet.htm) | Large historic forum footprints. |
| German | [GameStar Community](https://www.gamestar.de/community/), [4Players forum](https://forum.4pforen.4players.de/) | Deep game threads and period-specific reporting. |
| Spanish | [ElOtroLado Multiplatform](https://www.elotrolado.net/foro_multiplataforma-general_22) | Long-lived Spanish-language forum archives. |
| Italian | [Everyeye](https://forum.everyeye.it/invision/) | Broad Italian gaming forum. |
| Polish | [GRYOnline Forum](https://www.gry-online.pl/forum/gry/) | Substantial Polish-language historical discussions. |
| Turkish | [DonanımHaber forums](https://forum.donanimhaber.com/) | Large Turkish enthusiast community with games. |
| Arabic | [TrueGaming Boards](https://www.true-gaming.net/boards/), [Arabic Game Developer Network games](https://www.agdn-online.com/threads.aspx?forumid=26) | Dated Arabic threads, including 2025 posts. |
| Portuguese (Brazil) | [Outer Space](https://forum.outerspace.com.br/), [Gamer Nation](https://gamernation.org/), [HardMOB](https://www.hardmob.com.br/forum.php) | Brazilian forum histories, including documented 2018–2024 closures. |
| Vietnamese | [GameVN](https://forum.gamevn.com/), [VOZ console forum](https://voz.vn/f/console-gaming.22/) | Dedicated gaming boards with long-running native-language discussion. |
| Malay / English | [Lowyat Gamers Hideout](https://forum.lowyat.net/GamersHideout) | Southeast Asian gaming categories. |
| English (Nigeria) | [Nairaland Gaming](https://www.nairaland.com/gaming), [2016 pages](https://www.nairaland.com/gaming/437) | Especially strong: current threads plus retrievable 2016 forum pages. |
| English (South Africa) | [MyBroadband Gaming](https://mybroadband.co.za/forum/forums/gaming.86/) | Large national gaming forum archive. |

**Caution:** This table is a sampling guide. A forum that is indexed or presently reachable may have anti-bot restrictions, pagination gaps, missing images, deleted posts or migrated history.

## Search plan for INSIDE / Playdead / sticker code archaeology

1. **Start with the direct game audience.** Inspect [INSIDE Steam Discussions](https://steamcommunity.com/app/304430/discussions/) and [r/PlaydeadsInside](https://www.reddit.com/r/PlaydeadsInside/) for 2016, 2017–2020 and 2021–2026 separately. Then the major generalist boards for 2016 launch and 2019 collector's-edition material. Preserve dates and quoted context; do not interpret absence from indexed search as absence from the forum.
2. **Search across languages and titles.** Combine `INSIDE`, `Playdead`, `LIMBO`, `iam8bit`, `collector's edition`, `sticker`, `ARG`, `code`, `cipher`, `puzzle`, `secret ending`, `hidden ending` with equivalents: Japanese `インサイド`, `プレイデッド`, `シール`; Chinese `Inside 游戏`, `贴纸`, `密碼`, `密码`; Korean `인사이드`, `플레이데드`, `스티커`; French `édition collector`, `autocollant`; German `Sammleredition`, `Aufkleber`; Spanish `edición coleccionista`, `pegatina`; Portuguese `edição de colecionador`, `adesivo`; Russian `наклейка`, `код`; Arabic `ملصق`, `شفرة`; Turkish `çıkartma`, `şifre`. Translations are **search expansions**, not canonical game titles.
3. **Use site-restricted searches.** Patterns: `site:forum.gamer.com.tw Inside Playdead`, `site:forum.gamevn.com "INSIDE"`, `site:forum.outerspace.com.br "INSIDE" "adesivo"`, `site:boards.steamcommunity.com` (check actual URL and index), `site:steamcommunity.com/app/304430/discussions/ sticker`. When the Google/Bing index fails, run the forum's own search and try a different transliteration.
4. **Look for physical object sightings, not only speculative solutions.** Prioritize contemporaneous photographs, serial numbers, collector's-edition packaging posts, 2019–2024 sale photos, translated code rumors, source files, original links, archived attachments and previously uncollected sequences. Treat user claims and image crops as leads until source provenance is checked.
5. **Track migrations.** Check old forums' closing posts, surviving mirrors, archive.org CDX / Wayback snapshots, new domains, changed paths and explicit Discord migrations. The [September 2026 Gamer Nation closure census](https://gamernation.org/t/lista-de-foruns-de-games-em-atividade-que-foram-encerrados-ou-migraram-para-o-discord/42145) is useful for the Brazilian market, but closure dates are member-reported and uncertain in parts.
6. **Log findings separately from the directory.** For a promising historical thread capture: `community,language,original_url,archive_url,thread_title,author_public_handle,post_date,access_date,original_text_excerpt,translation,photo_link,material_relevance,certainty`. Redact any information not needed to substantiate the artifact; public handles are not required for sticker identification. Distinguish a firsthand 2019 photo from a 2026 repetition of a Discord conjecture.
7. **Do not imply physical confirmation or cross-corpus independence.** Reddit reposts, forum quotations, wiki copies, and screenshots of the same photo all count as a single source lineage unless their physical origins differ. Any discovered sticker belongs in the existing observation/provenance procedure rather than being pasted into canonical `data/observations.csv` immediately.

### Search priority heuristic (a proposed workflow, not evidence)

For a candidate forum, prioritize `direct game relevance > documented 2016–2024 thread/search access > language/geographical novelty > site indexing/retrievability > likelihood of original photographs`. A narrow historical forum with a dated image is substantially more informative than a broad contemporary media portal without thread-level access.

## Integration of the attached *Worldwide Video-Game Forum Census* report (12 October 2026)

**Provenance:** User-supplied `deep-research-report (1).md`, titled *Worldwide Video-Game Forum Census*, describing a separately researched **184-endpoint** census. Only the supplied Markdown report was available for ingestion. It references CSV, JSON, ZIP, schemas and charts at paths from a separate execution environment; **those backing files were not attached here**, so the claimed 184 full individual records could not be diffed or imported. The report excerpts expose named endpoints and a cross-sectional table; only those substantiated in its text were candidates for incorporation. Do **not** claim all 184 entries were compared.

**Newly added entries (11):** [VOGONS](https://www.vogons.org/), [Racketboy](https://racketboy.com/forum/), [Nintendo Life forums](https://www.nintendolife.com/forums), [Pure Xbox forums](https://www.purexbox.com/forums), [MMORPG.com forums](https://forums.mmorpg.com/), [Speedrun.com forums](https://www.speedrun.com/forums), [HLTV forums](https://www.hltv.org/forums), [Neo-Arcadia](https://neo-arcadia.com/forum/), [GPForums NZ](https://www.gpforums.co.nz/), [Game Development Stack Exchange](https://gamedev.stackexchange.com/) and [Gamereactor España](https://www.gamereactor.es/foro/). The first seven are reported as inspected current forum surfaces in the attachment (`V` by discovery status); the others are candidates until directly checked (`C`). The report explicitly corrects Neo-Arcadia's forum entry point.

**Refined URLs for already-listed sources (five):** GameVN → `https://gamevn.com/forums/`; SAGamer → `https://sagamer.co.za/forum/`; Kaskus → `https://www.kaskus.co.id/forum/44/games`; ArabHardware → `https://forum.arabhardware.net/`; Whirlpool → `https://forums.whirlpool.net.au/forum/21`. These are *report-suggested canonicalizations*, not fresh HTTP reachability test results. Their pre-existing discovery grades were retained.

**Other genuinely useful methods** from the report: distinguish forum size from thread count and concurrent users; record newest observed gaming-post dates independently from inferred activity level; distinguish game publisher ownership from independent site moderation; note public-readable vs login-walled discussion, RSS/API availability, and historical archive links without pretending wildcard Wayback queries prove snapshots exist. The proposed extended schema appears in the maintenance section above. These fields were **not fabricated** for existing rows.

**Temporal caveat:** The attachment calls its October 13, 2026 snapshot contemporaneous, but it was provided late on October 12 in America/Edmonton. Its claimed October 13 same-day observations may reflect time-zone or timestamp inconsistency and have **not been independently confirmed**. No precise newest-post dates or reported membership counts were ingested as verified facts.

**Scope warning:** The attachment's `184 endpoints`, `40 high-confidence records` and `44 dated records` are statistics claimed for its own unseen structured dataset; they should not be added to, or treated as validation statistics for, the project's TSV. Its emphasis on specialist retro, speedrunning and esports venues is a valuable correction to our earlier coverage.

## Future validation and maintenance

A complete audited directory needs per-row verification of **URL reachability**, **actual user discussion**, **last relevant post date**, **archive accessibility** and **original/successor location**. At present none of these fields is systematically recorded. Do not upgrade `C` to `V` by assumption; attach a supporting dated thread link or preserved archive witness when validating. Demote or remove categories that no longer host discussion. A `V` row may later require demotion if the observed page was not genuinely a gaming discussion surface.

A stronger future schema could extend the TSV with `last_game_post_utc`, `activity_witness_url`, `verified_at`, `live_or_archived`, `forum_native_search`, `archive_cdx_url`, `indexed_for_2016`, and `insider_relevance`. Keep absent evidence blank rather than inventing dates. Resolve cross-links and changed domains, not merely HTTP 200s; a redirected homepage can produce an apparently healthy but useless result.

Known blind spots: dedicated regional game forums outside dominant national languages; India beyond English; Indonesian-language independent forums; smaller African gaming boards; Arabic and Persian archived boards; nonindexed platforms; old BBS/imageboards; language-specific platform subforums within very large directories; publisher community migrations; and many deliberately closed or inaccessible archives. In a complete worldwide crawl there would be thousands of game-specific subreddit/Steam/official-forum instances; this inventory selects **representative gateways rather than pretending to enumerate every game**.

## Source / evidence starting points

These are externally discoverable forum landing pages and contextual references, **not row-by-row proofs**:

- [Steam INSIDE general discussions](https://steamcommunity.com/app/304430/discussions/) and [r/PlaydeadsInside](https://www.reddit.com/r/PlaydeadsInside/) for project-specific material.
- [Nairaland Gaming](https://www.nairaland.com/gaming) and [the 2016 archive page](https://www.nairaland.com/gaming/437).
- [TrueGaming Arabic Boards](https://www.true-gaming.net/boards/), [a dated April 2025 discussion](https://www.true-gaming.net/boards/threads/%D9%85%D9%88%D8%A7%D9%82%D8%B9-%D8%A7%D9%84%D8%A3%D9%84%D8%B9%D8%A7%D8%A8-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D9%88%D9%85%D9%8F%D8%B9%D8%B6%D9%84%D8%A9-%D8%A7%D9%84%D9%81%D9%90%D8%A6%D8%A9-%D8%A7%D9%84%D9%85%D9%8F%D8%B3%D8%AA%D9%87%D8%AF%D9%81%D8%A9.62222/), [AGDN games subforum with dated 2025 posts](https://www.agdn-online.com/threads.aspx?forumid=26).
- [September 2026 Portuguese-language forum survival/closure inventory](https://gamernation.org/t/lista-de-foruns-de-games-em-atividade-que-foram-encerrados-ou-migraram-para-o-discord/42145).
- [South African MyBroadband index](https://mybroadband.co.za/forum/) and [Brazil Outer Space](https://forum.outerspace.com.br/).
- [GameDetectives INSIDE ARG reference wiki](https://wiki.gamedetectives.net/index.php?title=Inside_ARG). **This is a reference source, not an additional forum row.**

**Editorial rule:** Maximize recall without silently inflating verified coverage. Every row should be actionable as a lookup target; those that are demonstrably irrelevant, inaccessible before 2014, or unrelated to gaming should be removed rather than retained for a larger count.

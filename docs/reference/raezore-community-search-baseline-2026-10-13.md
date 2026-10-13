# Raezore's existing CE-owner search: method baseline and reproducibility gaps

**Reviewed:** 2026-10-13. **Primary source:** [Raezores' research methods](https://github.com/twinysam/INSIDE-ARG/blob/master/raezores-research.md), last updated **2026-10-11**; source SHA **8367668c865b14970f7357f7d94bfad6dcc6f077**.  
**Canonical outcomes:** [twinysam sticker list](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md).  
**Our machine-readable discovery program:** [CE native-language campaign](inside-ce-native-owner-hunt-2026-10-12.md) and [local search methods](global-gaming-forum-search-methods.md).  
**Epistemic status:** A description of *methods practiced*, not an exhaustive query-history export, measured coverage audit, or proof every historical CE owner has been found.

## Important correction to our novelty claims

The community has already done much more than English Google searches. Raezore reports persistent CE-owner discovery **since the March 2018 announcement**, including searching comments/replies/old profiles, Google Images and reverse-image provenance, dated searches, YouTube and old video comments, original publisher social posts/quotes/replies, eBay sold listings, Facebook groups/Marketplace, Reddit, Discord, owner/alias tracing across platforms, translations and variant spellings, international marketplaces, notifications and follow-ups. Raezore says **ChatGPT was added in April 2026** for additional queries/translation, plus recurring searches and canonical sticker cross-checking. These are *established community techniques*, not innovations of our October 2026 program.

The report also documents years of **individual owner contact**, including translated conversations, refusals, sellers relaying messages, and sometimes months-long follow-up. **Our project has a distinct, intentionally passive/public-source-only approach**: no owner outreach, direct messages, private groups, undisclosed personal contact identifiers, or attempts to contact people through other accounts. Do not imply our passive approach exhausts the community's richer human contact graph.

### Evidence and retrieval crosswalk

| Raezore source-supported method | Community-reported real use | Our current implementation | Missing measurable capability |
|---|---|---|---|
| Product-name variants | INSIDE CE, Playdead, iam8bit, RealDoll; *Huddle*, *statue*, *figure*, collecter's/Collectors, special/limited/deluxe edition | 50-locality native queries and broad proper-name anchors; **nine additional exact sourced families added Oct 13** | Evaluate each query against dated true-positive controls and unrelated-title false positives; don't treat a full search-manifest count as coverage |
| Original posts **and nested replies** | YouTube unboxing comments, Oddheader's 2026 video, Reddit descendants, articles, Facebook pages and quote posts | Source routing and URL/comment normalization; index results and archives | Actual page/reply-body ingestion with pagination, chronology and comment IDs; web-index title hits cannot prove reply completeness |
| Image-led discovery | Google Images, reverse-image, Huddle/box/art-card photos, thumbnails without useful text; reused publisher art and image reposts | Candidate URL search, known WARC HTML extraction, source-side caution | Permission-respecting **image candidate registry** with URL/media hash/perceptual-hash clusters, media origin and independent sticker-readable status |
| Historical resale | eBay active/sold photos and buyer/seller transfer chains; Facebook Marketplace, PriceCharting, regional secondhand sites | Source directory, price-history lead table and duplicate URL triage | Original listing IDs/archived images, cross-marketplace object-linking; no assumption that 13 sales = 13 physical CEs |
| Account/provenance comparisons | Alternate handles, users claiming >1 CE, gifts of partial contents, repeat sales | Canonical URL and same-thread contextual reconciliation | Explicit claim graph with **source statement**, **object**, **transfer event**, **confidence**; no inference that same handle = same owner or new person = new CE |
| International searches | Local terms, language help, Russian StopGame traffic, VK, collecting platforms | 50 language profiles and 491 gaming communities + 30 other public platforms | Human/native-speaker validation and **per-site measured retrieval quality**; local terms alone do not establish actual search of a site |
| Temporal follow-ups | Posts back to March 2018, old videos with recent replies, owner messages months later, recurring alerts | Historical CDX probes, resumed index batches and deduplication | Separate **post date, edit date, reply date, discovery date, archive timestamp**; positive-control recall and reliable source-capture windows |
| Sticker statuses | Image-identifiable, *reported number/symbol without image*, lost, unknown, uncertain preorder and transfers | Physical ledger left untouched; pending source-review queue always zero new confirmations | Map review output into existing canonical identified/reported/lost/unknown taxonomy only after independent original evidence review |

**Specific results Raezore attributes to these methods:** ResetEra research led to Metsallica's **/296** image; linked a differently named account to previously documented **-338**; collector-site images produced sticker records; StopGame-assisted contact led to **L40**; Facebook Marketplace produced a documented CE; Oddheader’s 2026 video generated owner/lost/reported-number follow-ups. Those *examples* support the method classes above. The report does not provide a complete list of exact search expressions, dated queries, number of results inspected, inaccessible pages or missed-result rates.

## What our program can add rather than duplicate

**A. Observable search coverage, not merely more searches.** Freeze an independently sourced *positive-control* collection spanning reply-level Reddit owners, comments under older unboxings, older non-Playdead videos, verified archival forum thread bodies, Japanese/Chinese/Portuguese discussion, and original marketplace photos. For each source/term/provider, record whether the target was searchable, whether source content was actually retrieved, and why it was missed. Negative results are legitimate **only within a verified search scope**.

**B. Off-index reply and image retrieval.** Most of our 28,188 prepared queries currently lead to commercial web-index search, not proof that indexed snippets include replies or picture-only posts. Before pursuing dozens more text-query variants, establish permitted native reply/comment search, public-media provenance and archived webpage extraction. In particular search original posts *and subsequent replies over time*. Preserve image origin, seller listing ID and duplicate-image clusters without assuming different social accounts represent different CEs.

**C. Source-specific queries from demonstrated behavior.** Raezore's *Huddle*, *statue*, *figure* and edition-variant tactics are now in our query generator, each once per source rather than repeated across 50 native profiles for a multilingual site. These are **previously community-used terms**, not newly discovered search ideas. In site-specific passes, pair with original local-language forms when a native speaker or actual period post supports them; English CE marketing names may still be copied into foreign-language listings.

**D. Preserve claim units and object identity.** A public poster claiming they bought a CE is a source statement. A seller listing is a resale event. An eBay photo with sticker is a physical observation if independently readable. A reported number/symbol without an image remains **reported**, not directly image-confirmed. A CE seller and subsequent buyer are generally the *same* physical object. Repeated tweets/quotes/messages or different names should not inflate observations.

**E. Avoid exploiting the contact graph.** Raezore’s approach includes outreach and DMs and works because of community relationships; our authorized scope is retrospective public-source observation. Do not implement identity-resolution scraping, contact lookup or account-link chasing of unrelated profiles. Original publicly linked source provenance is enough for an unresolved lead.

## Query-generation change tied directly to this report

The planner now includes nine additional marketing/collector term combinations per community (quoted source-context where useful): INSIDE + Huddle, Huddle + iam8bit, Playdead + statue/figure, INSIDE + *collecter's edition* and *Collectors Edition*, iam8bit + special edition, Playdead + limited edition, and Playdead + deluxe edition. Source: Raezore’s **How I do the searches**, not original speculation.

The previous **23,499 planned tasks** (11,250 community + 12,249 secondary) rise to **28,188 planned tasks** (15,669 community + 12,519 secondary) across 491 gaming-community entries plus 30 social/video/collector sources, with **28 expression families**. Nine additions are deduplicated across the 50-language profiles on a multi-language source; if a category is constrained to a subcampaign, record a new manifest hash and a new resume offset.

**Planned means unexecuted.** Full execution still needs permitted access, original content retrieval, original-source reconciliation, quota/budget controls and a measured evaluation. No source statement in Raezore’s report establishes any new physical sticker number in this review.

## Best next experiment

Take 8–12 **already-known original dated sightings** discovered by different mechanisms (e.g. ResetEra images, YouTube reply reported symbol, Facebook Marketplace sale, old Twitter quote post, native-language StopGame-related post, collectedit listing, unboxing sticker frame). Build a small gold-standard evidence fixture with a known source URL, post/comment identity, dated provenance, expected source field and rights/access gate. Test our retrieval routes *without hardcoding the exact post URL as the answer*. Compare site-native search, authorized web-index, archived URL/body retrieval and reverse-image pathways, recording which actually finds the true original. Iterate on the first systematic failure before scaling to 28,188 independent queries.

This gives us a measurable answer to the real question: **what class of sticker/owner evidence can our tooling recover that the community's years of searches have not already surfaced?**

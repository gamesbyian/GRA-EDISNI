# INSIDE Collector's Edition ownership and ARG: multilingual discovery campaign

**Research mode:** DISCOVER (public source discovery), with canonical-ledger reconciliation before any physical claim.  
**Prepared:** 2026-10-12 (America/Edmonton)  
**Canon for comparisons:** [twinysam/INSIDE-ARG stickers.md](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md); our own [physical observations](../../data/observations.csv).  
**Next-stage archival controls:** [dated capture metadata controls and bounded Wayback probe](inside-ce-archive-cdx-positive-controls-2026-10-13.md).  
**New assets:** [50 native-language search profiles](../../data/reference/inside-ce-native-search-lexicon.tsv), [484-forum native campaign planner](../../scripts/build_inside_ce_native_search_campaign.py), [30 additional social/video/resale platforms](../../data/reference/inside-ce-ownership-secondary-platforms.tsv), [source-backed preliminary lead ledger](../../data/reference/inside-ce-owner-search-ledger-2026-10-12.tsv), and [manual/CI workflow](../../.github/workflows/inside-ce-native-search-campaign.yml).

## What we want to discover

Find *every reasonably recoverable public mention* of Playdead's INSIDE Collector's Edition, its partnership with iam8bit/RealDoll, the unsolved ARG and sticker mechanism, especially **firsthand** statements of buying, receiving, owning, unboxing, storing, gifting or selling a CE. Find **any explicit three-digit sticker number/symbol/background**, original sticker photographs, sales images, auction archives, out-of-context social media sightings, unboxing video frames or posts discussing edition numbering and production counts.

These are **different evidence types**. A person saying they *ordered* one is not proof they *received* it; having a sealed PS4 disc is not necessarily owning the CE; the physical sticker may have been discarded while the collector's box remained sealed. Treat a sticker's **printed number** as physical evidence and a community “edition number” as an unverified interpretation. A CE moving between sellers and buyers remains the **same object**. Multiple photographs or cross-posts of one sticker are not independent instances.

This campaign makes **no owner outreach, tagging or messaging**. Public archival observation is sufficient for discovery; do not collect personal contact details, addresses, private groups or private-message contents.

## Why the historical evidence changes the query plan

1. [December 2019 shipping discussion](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/now_shipping_finally/): recipients spontaneously discussed shipment and reported sticker numbers **306, 171 and 125**. These are already present in the canonical physical ledger. They are crucial *historical positive controls* for code-bearing searches and for comparing full-thread versus post-only indexing. Original shipping language and sticker-specific questions occur together, but an index of thread titles alone would miss the numbers.
2. [November 2019 CE update](https://www.reddit.com/r/PlaydeadsInside/comments/e1mdlm): contemporaneous purchase admissions, including a participant who later identifies as Harry Darger, already tracked as canonical lost sticker **L04**. This exemplifies why owner claims must be compared with historical handles and status changes, not counted as new stickers.
3. [July 2020 r/GameSale offer](https://www.reddit.com/r/GameSale/comments/i0vgml/): a seller describes an INSIDE CE with figure and sealed PS4 game. Its *exact thread ID* is not present in the canonical sticker document checked October 12, 2026, making it an **unreconciled public resale lead**, not a proven additional edition. Obtain source-accessible image/history and check for duplicate objects before elevating.
4. [Original December 14, 2019 Twitch unboxing VOD reference](https://www.twitch.tv/videos/521529035): linked by a CE recipient in the contemporaneous [shipping discussion](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/now_shipping_finally/). The exact VOD ID does **not** appear in the canonical sticker ledger examined, and its recording could not be retrieved with the available web tools. This is a potential original *visual archive*, not evidence of a new sticker or a currently recoverable recording.
4. [December 2020 r/GameSale offer](https://www.reddit.com/r/GameSale/comments/k4wyvu/): already canonical **U32**. A sale's existence or a new repost must never inflate ownership totals.
5. [June 2025–2026 buying discussion](https://www.reddit.com/r/PlaydeadsInside/comments/1l5x8rb/does_anyone_know_where_i_can_get_the_inside/): includes sealed CE resale assertions and follow-ups; important claims are already tied to known records such as **/047**, while other comments require post-level attribution. Different sellers/buyers in one thread cannot be assumed to own different stickers.
6. [August–October 2026 artbook discussion](https://www.reddit.com/r/PlaydeadsInside/comments/1vdbrus/i_want_an_art_book_for_inside/): public resale and sealed ownership claims; canonical **L46** refers to one account, and the October 11 acquisition already traces to previously known **/043**. Comments mentioning only the sealed standalone PS4 game are **not** CE ownership.
7. [September 2026 black-wrapper explanation](https://www.reddit.com/r/PlaydeadsInside/comments/1wruv2d/psa_you_dont_need_to_open_your_inside_collectors/): sticker is on the wrapping of the included PS4 game within the shipping box, not necessarily on the sealed collectible figurine. Search native descriptions of *shipping box, black paper, sleeve, outer seal, numbered sticker* in addition to CE product names.
8. [February 2021 temporary official listing](https://www.reddit.com/r/PlaydeadsInside/comments/lfcms4/inside_collectors_edition_avaliable_on_8bit_right/): discussion reports the product being offered at the original $375 price after the initial shipment period. Do not assume all legitimate first-time purchases must be from 2018–2019 preorders.
9. [September 2019 intended-buyer thread](https://www.reddit.com/r/PlaydeadsInside/comments/czc89n/anybody_managed_to_snag_themselves_one_of_those/): a first-person account says UK shipping restrictions prevented purchase; *interest* alone is not ownership. Other comments in that thread later connected to canonical **-267**.

**Source status:** these are historical positive-control and potential-lead pointers, not newly discovered numbered physical stickers. The corpus remains unchanged. Search-engine retrieval dates, community repost dates, and original post dates must remain separate.

## Native-language design: author from regional conversational idiom

The [lexicon](../../data/reference/inside-ce-native-search-lexicon.tsv) independently expresses first-person **purchase**, **receipt**, locally natural **edition terminology**, **sticker/seal**, **serial**, **riddle/ARG**, **resale**, **unboxing**, and **black wrapper** concepts in **50 written locale profiles**. This includes differentiated Brazilian and European Portuguese, Argentina/Mexico/Chile/Colombia/Peru Spanish, Simplified/Traditional/Hong Kong Chinese, Japanese, Korean, Vietnamese, Thai, Arabic, Persian, Hebrew, Turkish, Polish, Ukrainian and many others.

Examples of intentionally natural source-language wording:

| Locale | Original-language terms to combine with `Playdead` / `iam8bit` |
|---|---|
| Japanese | `届きました`, `コレクターズエディション`, `シール`, `開封動画`, `黒い封筒` |
| Traditional Chinese | `我買了`, `典藏版`, `貼紙`, `編號`, `開箱` |
| Korean | `드디어 받았습니다`, `한정판`, `스티커`, `일련번호`, `개봉기` |
| Brazilian Portuguese | `acabou de chegar`, `edição de colecionador`, `adesivo`, `número de série` |
| French | `je viens de recevoir`, `édition collector`, `autocollant`, `déballage` |
| German | `ist angekommen`, `Sammleredition`, `Aufkleber`, `ausgepackt` |
| Arabic | `وصلتني`, `نسخة لهواة الجمع`, `الملصق`, `الرقم التسلسلي` |
| Turkish | `elime ulaştı`, `koleksiyoncu sürümü`, `çıkartma`, `seri numarası` |
| Russian | `мне пришло`, `коллекционное издание`, `наклейка`, `распаковка` |

Crucially, **the query planning does not simply translate an English sentence**. It uses each language's authored purchase, receipt, packaging and selling vocabulary, then selects language/region-specific forum targets. Hybrid-language countries use both relevant vernacular profiles. For global or multilingual surfaces, **all 50 native-language profiles** are now generated rather than silently omitting languages without a country-specific gaming forum. Local-language site restrictions still apply to regional forums.

This is a **starting lexicon, not a claim of native-speaker proofreading**. Informal spellings, spelling inflections, code-switching, common abbreviations and colloquial local product names should be expanded per-site after actual source examples. Search phrases can fail through strict quoted multi-term AND logic; run broad title/product-anchor and site-native iterations before treating them as exhausted.

### Additional 2018 geographical lead: iam8bit UK link

A contemporary [Cheap Ass Gamer 2018 collector-edition catalogue](https://www.cheapassgamer.com/threads/official-collectors-edition-compilation-ix-2018.366036/page-59) lists INSIDE Collector's Edition as linked to **both “iam8bit” and “iam8bit UK”**. The latter hyperlink redirects to an old `goo.gl/NHiBDv` short URL through a CAG exit gateway. This establishes *a publicly listed UK-related purchase link* in 2018, **not** an actual purchasable UK allocation, confirmed shipping eligibility, a successful order or an additional production batch. Contrast with the [September 2019 firsthand account of being refused UK shipping](https://www.reddit.com/r/PlaydeadsInside/comments/czc89n/anybody_managed_to_snag_themselves_one_of_those/). Those statements can coexist if the catalog link was speculative, changed, expired or otherwise inaccessible. Future historical URL work should resolve archived destinations of the UK shortened link and check 2018–2019 British collector-board discussion before concluding that all potential CE owners were originally in the United States.

## Search strata, scoring and false-positive defense

Candidate query categories include original purchase, arrival, edition mention, owner posts without game title, sticker photo, explicit number, number without title, ARG/riddle discussion, offered for sale, unboxing, black wrapper, wrapper without title, broadly co-mentioned collector edition, unboxing without game title and sticker plus number. **Every site receives multiple independent formulations**, not a translated single English query.

Use direct proper-noun anchors `Playdead`, `iam8bit`, `RealDoll`, and the relevant local CE terms, plus the source-native broader `INSIDE` title. Without these anchors, “inside” means countless other things: GameVN’s index returns NBA The Inside; Taiwanese game searches find LAMY pens called JETSTREAM INSIDE. These are verified *false-positive controls*, not candidate Playdead records.

**Temporal cohorts:** March–June 2018 reveal and preorder; November 2019–2020 initial fulfillment/unboxings; 2020–2022 leftover stock, gifts and resale; 2023–2026 later transfers, rediscovered sealed collectors and ARG resurges. Search old posts **and later replies to those posts**, independently recording publication dates.

**Source classes:**

- **Physical fact:** readable sticker photo with number, symbol, background and traceable physical provenance.
- **Firsthand owner claim:** publicly claims bought, received, unboxed or sold; photo can strengthen but doesn't establish serial.
- **Potential owner:** preorder or collection photo without sufficiently identified CE; preserve without promotion.
- **ARG/sticker interpretation:** puzzle discussions, hypotheses, useful diagrams and references, but not new physical observations.
- **Non-owner/negative:** wanted to buy, cannot ship, ordered but canceled, only PS4 standalone, or a known repost.
- **Duplicates/transfers/lost:** compare canonical `U##`, `L##` and actual serial; never count multiple social handles or sales as multiple CEs without independent objects.

Search **photograph descriptions and original image context**, not only prose. Original CE sticker photos may appear in eBay product listings where sellers know nothing about the ARG; the canonical sticker ledger documents exactly such findings. Photos from official marketing may show a poster or contents also shipped in other versions. Never manufacture a sticker identification from a blurry crop.

## Wider source universe

The existing [484 community directory](../../data/reference/global-gaming-forums.tsv) misses large quantities of public **YouTube comments and unboxing video descriptions, image posts, Facebook public product comments, Twitter replies, old eBay listings, collector catalogues and music forums**. The new [30-surface extension](../../data/reference/inside-ce-ownership-secondary-platforms.tsv) indexes such leads as a separate cohort with API/permission gates and native-language scopes.

High-value positive examples from the canonical research history: YouTube unboxing screenshots, iam8bit promotional post comments, collector listing sites (CollecTit), archived WATMM music forum buyer posts, Twitter/Instagram photo replies, multiple eBay resale images and an Austrian Willhaben listing. A strict “gaming forums only” strategy would systematically miss many of these.

**Do not use unsupported scraping** of restricted APIs, private groups, login barriers, removed posts or pages. Reddit bulk research has a 2026 research-access gate; native platform APIs and market completed-sale history each have separate rights/availability. A source-index lead is not permission to download, mirror, or retain a large third-party corpus.

## Execution and automation

The new [planner](../../scripts/build_inside_ce_native_search_campaign.py) joins every source to the existing forum and archive route matrix, emits reproducible UTF-8 JSONL tasks, verifies unique task IDs, and fairly interleaves **locale and source-site tasks** so a small paid-search budget does not exhaust one platform or language. Current full plans: **8,955 forum queries** plus **10,755 social/video/resale queries** across 15 query categories and 50 native locale profiles. They are proposed queries, not executed retrievals. The manual [GitHub Actions campaign workflow](../../.github/workflows/inside-ce-native-search-campaign.yml) runs offline tests and emits planned work. It supports optional limited **official Brave Search API** index lookups only when the user explicitly enables paid searches and has configured the API key.

Example:

```bash
python scripts/build_inside_ce_native_search_campaign.py \
  --output /tmp/inside-ce-forums.jsonl \
  --secondary-output /tmp/inside-ce-social-resale.jsonl \
  --summary /tmp/inside-ce-plan.json \
  --max-tasks 20000

python -m unittest discover -s tests -p test_inside_ce_native_campaign.py -v
```

The tasks are **planned_unexecuted**. Even after an index lookup, `index_search_success` only means a query returned results, not that every forum message has been searched. A major later execution effort must check each source's native search, post-body coverage and archives, and benchmark against the 2019 known positive-control sticker threads.

### Initial search results and gaps

The pilot manually investigated dozens of targeted English and native-language combinations across Reddit, GameFAQs, ResetEra, Korean/Japanese/Chinese/Vietnamese and European-language forums. Strong direct evidence came from old Playdead Reddit posts and collectors' resale comments, while many non-English queries found unrelated games and consumer goods. **No new three-digit sticker has been physically confirmed in this sweep.** The July 2020 GameSale offer is a worthwhile unreconciled first-person historical lead; additional records mostly trace to known stickers/lost/unknown classifications.

The [lead ledger](../../data/reference/inside-ce-owner-search-ledger-2026-10-12.tsv) records source URLs, source-supported claim type, canonical relationship, follow-up research action and `new_confirmed_stickers=0`. It does not include speculative identifications of private people.

## Priority next actions

1. **Preserve dated original positive controls** for the shipped 2019 serials and exact 2020 buyer/owner claims. Compare them to the canonical ledger automatically; source-lineage duplicates must be demoted.
2. **Investigate the July 2020 GameSale thread** using publicly retrievable dated images/archives, checking other canonical sales before claiming a new CE.
3. **Roll out native-language owner/ad delivery terms** on relevant regional forums *and* region-specific resale sites, especially Japan, Taiwan, Korea, Brazil, Mexico, Germany, France and Italy. Keep terms native and preserve non-English snippets and product spellings.
4. **Use historical URL discovery and image search**, not solely indexed prose, to find unindexed seller photos and original owner unboxing footage.
5. **Upgrade from planned queries to measured retrieval** by validating search-provider credentials and access policy, then running bounded time- and platform-stratified native/web-index/archival passes; maintain truthful incomplete coverage and test against known 2019 posts.

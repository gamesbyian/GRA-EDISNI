# INSIDE CE: photo provenance and measured source recall

**Prepared:** 2026-10-13. **Status:** tools implemented and submitted for CI; no bulk social posts or marketplace photos downloaded. Based on [Raezore's methods](https://github.com/twinysam/INSIDE-ARG/blob/master/raezores-research.md), including photo-first discoveries and long-lived forum/video reply searches.

## Intended output: a short, original-source handoff to Raezore

Deliver a handful of sources not obviously accounted for by the canonical sticker list, with exact public URL, date, firsthand statement or public picture, comparison against the current source ledger, and unresolved status. Do not count a different social account, old resale listing, repeated photograph or secondhand buyer as another physical CE. No owner messaging/outreach is part of this program.

## 1. Offline image provenance

The [media index](../../scripts/index_inside_ce_public_images.py) groups locally supplied public images using original-file SHA256, pixel-normalized SHA256, and 64-bit dHash/aHash perceptual candidates. It compares metadata and aspect ratio, preserves media source URL and original publication/capture dates, and flags potential copies of known official iam8bit marketing photos.

It requires [Pillow](../../requirements-ce-media.txt) and an explicit TSV manifest with: asset_id, file_path, source_url, source_kind, published_at, captured_at, permission_basis. Allowed source kinds include official_marketing, owner_public_post, public_resale, public_review, community_repost and unknown_public. Source URLs must be HTTP(S), file paths must remain inside the specified local root, and the caller must have reviewed retention/access conditions. The tool **never downloads media**, scrapes social accounts, analyzes faces, reads edition numbers, or contacts anybody.

Image similarity is not object identity. An image can be cropped, reused by another seller, shared by its first owner or lifted from promotional material. The index records all perceptual matches as **review-only**, with new_confirmed_stickers always 0.

For scale, a dHash search splits its 64 bits into eight blocks of eight bits. Any two hashes differing in seven or fewer positions must share at least one block, so the approximate matching candidate scan maintains complete recall *within the chosen dHash radius*, while avoiding many unnecessary comparisons. The second aHash and aspect checks still apply. A chain of pairwise matches can bridge different images; clusters are not proofs.

Example local command (assuming approved files already exist):

    python -m pip install -r requirements-ce-media.txt
    python scripts/index_inside_ce_public_images.py \
      --manifest /research/authorized-public-images.tsv \
      --root /research/authorized-images \
      --output /research/ce-photo-review.tsv \
      --summary /research/ce-photo-pairs.json

A historic **marketing-image negative control** is the [iam8bit CE showcase](https://www.iam8bit.com/products/inside-collector-s-edition) and the [2019 Polygon preview](https://www.polygon.com/2019/12/12/21013222/inside-real-doll-iam8bit-limited-edition-contents/), which both feature InsideCE_Lifestyle marketing assets. Different sites hosting these publisher images do not represent two owner photographs. The standalone PS4 edition also uses CE-linked image asset names, so neither a game-case picture nor a CE asset filename can establish collector-set ownership.

## 2. Blind source-discovery recall

The [12-example frozen gold fixture](../../data/reference/inside-ce-discovery-gold-controls.tsv) uses known community source records across ResetEra, X/Twitter, CollecTit, Austrian Willhaben, eBay, YouTube, Reddit and Instagram. It includes positively observed numbered stickers, a known lost sticker and an owner with an unreported number. They are **not new leads**.

The [benchmark planner](../../scripts/benchmark_inside_ce_discovery.py) emits 24 provider-search tasks, two per case, **without supplying the exact known source URL, post ID or author name as search terms**. The offline evaluator checks the returned URLs against those held-out known source URLs and classifies exact_source_found, related_topic_only, not_in_returned_index_hits, search_failed_or_unavailable, and not_executed. A same-video match is not the same YouTube comment. A same-Reddit-thread result is not the original poster. An index miss is *not* a historical absence claim.

    python scripts/benchmark_inside_ce_discovery.py plan \
      --output /research/ce-gold-query-plan.jsonl

Once and only once permitted licensed index searches have actually run on that plan:

    python scripts/benchmark_inside_ce_discovery.py evaluate \
      --input /research/ce-gold-index-results.jsonl \
      --output /research/ce-gold-recall.json \
      --summary /research/ce-gold-recall-summary.json

Do not report measured recall before execution. An index hit recovers a URL, not necessarily its full post text or sticker photo. Evidence acquisition and verification remain separate.

## 3. Highest-value next extraction

Raezore already uses reverse image searches, multilingual wording, marketplace alerts, social comments and alias reconciliation, along with direct owner outreach. Our contribution is **measured coverage**, indexed original replies and historical images that may have escaped commercial indices, and deduplicated source candidates requiring fewer manual checks.

Prioritize an actual test of a few known examples from the image and reply categories before scaling the 28,188-query native-language campaign. Then use failures to select original permitted discussion pages, picture-only public posts, regional resale archives and historical video comments for additional retrieval. A rehosted photograph never proves a different sticker; an owner stating a serial without an image is only a reported serial until corroborated.

**All automated outputs retain 0 new confirmed stickers until original evidence is independently reviewed.**

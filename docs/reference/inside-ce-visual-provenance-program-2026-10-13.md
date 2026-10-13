# INSIDE CE visual discovery and photographic provenance

**Started:** 2026-10-13. **Research mode:** DISCOVER for web/image lead finding; no physical sticker observations are created here. **Scope:** public, passive image evidence only. No owner outreach, private galleries, account-linking speculation, or contact-detail extraction.

## What was already in the repo

- [Physical sticker originals](../../archive/stickers/README.md): at baseline 82 distinct manifest-listed community-original images, plus clearly labeled derived edits/resizes. Always use the CSV manifest, never filename guesses or mixed original/derived observations.
- [External acquisition](../external-evidence-acquisition-plan.md): original-file preservation, public downloads via `yt-dlp`/`gallery-dl`, hash inventory, source statuses; [video frame extraction](../../scripts/external_evidence/extract_frames.py).
- [Native-language public owner hunt](inside-ce-native-owner-hunt-2026-10-12.md), [Raezore method baseline](raezore-community-search-baseline-2026-10-13.md), [CE versus standalone differentiation](inside-ce-edition-product-differentiation-and-triage.md), [manual public evidence intake](../manual-external-evidence-acquisition.md).

**The gap:** no dedicated CE photographic index, first-party promotion negative-control register, image-URL extraction from acquired HTML, perceptual-repost triage, or optional semantic scene ranking. These are complementary to the pre-existing image and reverse-image search work already carried out by Raezore, not a claim to have invented those methods.

## What is built

| Component | File | Output / role |
|---|---|---|
| Canonical sticker reference ingestion | [visual_index.py](../../scripts/external_evidence/visual_index.py) | SHA-256 verifies every `community-original/canonical_input=yes` row in `archive/stickers/manifest.csv`; attaches known serial, A–I background, symbol and immutable source URL. |
| Marketing/promotional image control corpus | [inside-ce-visual-sources.json](../../data/reference/inside-ce-visual-sources.json) | Four exact source-backed URLs: first-party iam8bit Huddle/box photo, first-party flat-lay, first-party PS4/poster photo and explicitly labeled syndicated press copy of an art-card photograph. These are **negative controls** for inferred ownership. |
| Bounded public reference acquisition | [fetch_visual_references.py](../../scripts/external_evidence/fetch_visual_references.py) | HTTPS host allowlist, redirected-host check, image content-type verification, 20-MiB and pixel limits, full-byte SHA-256 and per-source retrieval statuses. Downloads stay in disposable work directory. |
| Public HTML image discovery | [discover_html_images.py](../../scripts/external_evidence/discover_html_images.py) | `img`, lazy-loading URLs, `srcset`, `og:image`, Twitter preview images and image links from **already harvested** public HTML with precise page/source ID. Never treats extracted URL as a fetched photo. |
| Repost matching and triage | [visual_index.py](../../scripts/external_evidence/visual_index.py) | Exact byte matches, conservative two-hash whole-frame agreement, overlap-window possible crops, exact duplicate groups, review queue CSV, machine-readable matched provenance. |
| Novel-photo semantic ranker | [visual_semantic.py](../../scripts/external_evidence/visual_semantic.py) | Optional local/cached CLIP zero-shot relative rankings for CE wrapper, red foam box, Huddle, miniatures, unboxing scenes versus publisher marketing / PS4-only / game imagery. **No posterior odds or ownership proof.** |
| CI and optional research run | [ce-visual-provenance.yml](../../.github/workflows/ce-visual-provenance.yml) | Synthetic offline tests on PR; manual dispatch retrieves public reference controls and optionally one source, extracts HTML links, indexes images, uploads 14-day original/derived evidence artifacts. |

### Local quick start

Requires Python 3.12+ and Pillow:

```bash
python -m pip install "Pillow>=10,<13"
python -m unittest discover -s tests -p 'test_ce_*py' -v

# Fetch first-party marketing controls only (optional; network, allowlisted).
python scripts/external_evidence/fetch_visual_references.py

# Compare public downloaded images against original stickers and official promo controls.
python scripts/external_evidence/visual_index.py \
  --candidates evidence-work --output visual-evidence-work

# Recover image URLs *mentioned* by already downloaded public HTML pages.
python scripts/external_evidence/discover_html_images.py \
  --acquired evidence-work --output visual-evidence-work/html-image-leads.json
```

`evidence-work` is produced by the existing `harvest_public.py` tool or can be a directory of separately approved public media. An absent `visual-reference-work` is allowed, **reported as missing** rather than declared successful. `visual-evidence-work/reference-index.json` documents precise reference bytes and roles; `candidate-index.json` stores candidate file fingerprints and original source URL; `visual-matches.json` lists suggested relationships; `review-queue.csv` is intended for human verification and reconciliation against the canonical ledger. No script modifies `data/observations.csv` or sticker master files.

The manual [CE visual provenance / image discovery workflow](../../.github/workflows/ce-visual-provenance.yml) defaults to source ID `none`, so its first run only checks originals, downloads public controls and creates an empty candidate index. Supplying an existing acquisition-manifest source ID such as `youtube-ledger-02-Mhxynz-LoAI` harvests media metadata/thumbnail by default; `include_media=true` is explicit and may produce large original video files. For video footage, use [extract_frames.py](../../scripts/external_evidence/extract_frames.py) to prepare image frames before invoking `visual_index.py`. Do **not** re-harvest human-reviewed negative footage without a new source or relevant timestamp.

### Optional new-scene ranker

```bash
python -m pip install torch transformers
python scripts/external_evidence/visual_semantic.py \
  --index visual-evidence-work/candidate-index.json \
  --candidate-root evidence-work --limit 200
```

This uses `openai/clip-vit-base-patch32` if **already cached**. Downloading the model requires the explicit `--allow-model-download` flag. Do not silently add an unpinned model-fetching step to GitHub Actions or commit weights. Ranker scores are *relative logits among chosen prompts*, not probabilities; the model is not trained on sticker serial reading and cannot independently distinguish all first-party marketing photography from owner photography.

## Image-hunting protocol

Search **objects that visually indicate the full CE**: opened protective black wrap with numbered label, large red premium box and custom foam, pale silicone Huddle on a stand, miniature Boy, art-card fan, foldout sketch poster and mixed unpacking scenes. Distinguish genuine CE context from a **standalone INSIDE PS4** photo. The latter contains a PS4 game and poster but is officially a separate product. The 2,000-copy standalone edition figure must never be applied to the CE stickers.

Search and reverse-search full photographs **and purposeful crops** in parallel. Source-first positive controls include [official iam8bit CE listing](https://www.iam8bit.com/products/inside-collector-s-edition), [official standalone PS4 listing](https://www.iam8bit.com/products/inside-ps4-physical-game), and historical photos in `archive/stickers/originals/`. Use Lens/Bing/Yandex/TinEye manually or via explicitly authorized APIs; their results are *discovery leads*, never acceptance evidence. A scrape-only Google Lens wrapper is an optional research adapter with legal/operational fragility, not a guaranteed persistent API. Avoid rehosting user-uploaded photographs to third-party tools without checking consent and privacy.

A practical crop search ladder: (1) whole CE arrangement, (2) red box + foam, (3) isolated Huddle silhouette, (4) opened shipping wrap, (5) numbered sticker with A–I background, (6) individual art card or Boy statue. Photograph-specific identical/cropped-repost matches are more informative for linking **the same photograph** than for establishing the **same physical copy**. Separate exposures of one object can look different. Conversely two different stickers can share background artwork and look similar. Never collapse serials or accounts based on hash similarity.

### Triage requirements

1. **Marketing reuse:** if a candidate matches an iam8bit/press image, mark `promotional-reuse-review`. A business reposting the marketing image establishes no ownership.
2. **Known sticker photograph:** if a candidate matches a canonical photo, mark `known-sticker-photo-repost-review`. Keep original serial association as a *lead to check* rather than attributing the candidate page to that owner.
3. **Unmatched image:** review imagery and *original source context* for owner photographs, wrapper/sticker visibility and any newly printed number; image unmatched does not prove ownership.
4. **Serial evidence:** require readable original full sticker image or explicit independently attributable firsthand report; preserve exact URL, image bytes/hash, date, author statement and duplicate/transfer links. OCR and CLIP scores are not primary sticker evidence.
5. **Review and reconciliation:** compare against `stickers.md`, existing `U/L` cases and transfer chains. Send only materially new, public, source-backed leads to raezores. No unsolicited contact with owners.

### Measurement before broad automation

Use a **frozen positive-control rediscovery suite** from 10–12 *already known* CE sightings spanning seller images, social previews, unboxing thumbnails and physical sticker photos, plus at least 10 known negatives (official marketing and standalone PS4). Measure retrieval coverage separately from perceptual matching recall, semantic ranking top-K, source provenance completeness, and the number of novel leads after canonical reconciliation. Freeze controls **before** thresholds/prompt tuning. Current PR offers mechanics and synthetic tests; it does **not** claim those public-web recall measurements have yet been run.

## Open engineering work

- Real-world threshold calibration and crop retrieval against labeled source sets (synthetic tests alone cannot establish recall).
- Consent-conscious external reverse-image result adapters, if a stable legal supported interface is available.
- Acquisition of previously indexed external photo URLs using narrowly defined source allowlists; archived pages may contain dead image URLs.
- Optional object-level localization for new-angle box/Huddle photos (semantic CLIP is a coarse relevance ranker, perceptual hashes are for nearly identical frames).
- More first-party image controls from exact original listing HTML, each individually sourced and classified.
- Cross-marketplace object provenance graph and owner/publication chronology, with no identity inference from image matches.

**Current status:** a reusable pipeline is implemented, but downloads, real-world recall and new-owner discoveries must be reported separately and only after their respective workflow/test artifacts are inspected.

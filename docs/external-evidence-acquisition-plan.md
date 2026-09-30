# External Evidence Acquisition Automation Plan

_Date: 2026-09-29_

## Purpose

Turn the project's growing set of public and authenticated provenance leads into a reproducible acquisition pipeline rather than a sequence of one-off manual downloads.

The pipeline should preserve original evidence bytes where feasible, record provenance and acquisition metadata, generate review-friendly derived material, make failures explicit, and periodically re-check fragile links without treating downloader output or OCR as evidence.

This plan complements the external-corpus intake work in PR #56 and the Discord archaeology work in PR #55. It should consume their manifests rather than duplicate their research conclusions.

## Principles

1. **Originals are immutable evidence.** Preserve the highest-quality source bytes available before transcoding, cropping, OCR, enhancement, or frame selection.
2. **Derived artifacts remain reproducible.** Contact sheets, crops, frame ranks, OCR hints, screenshots, and metadata are generated from preserved originals and must identify their source.
3. **Verification beats file presence.** Known Git objects are verified with Git blob SHA-1, not plain-file SHA-1. Other files should receive SHA-256 and byte-size records.
4. **Acquisition failure is data.** Login-required, removed, redirected, extractor-broken, geo-blocked, and rate-limited results should be recorded explicitly instead of disappearing from the queue.
5. **Authentication is least-privilege and ephemeral.** Personal browser sessions stay local/self-hosted. A dedicated research-only account may supply a narrowly scoped cookie jar to GitHub Actions through an encrypted repository secret when needed; it is materialized only in runner temporary storage, never committed or uploaded as evidence. Passwords, personal browser profiles, Playwright storage-state files, and unrelated session tokens never enter Actions.
6. **Automation assists interpretation; it does not manufacture evidence.** OCR, image embeddings, sharpening, super-resolution, and ranking may prioritize human review but are never themselves proof of a sticker number or symbol.
7. **Do not overwrite history.** Each acquisition creates a timestamped record. Subsequent runs may diff against prior snapshots.
8. **Discovery is recursive.** Newly collected captions, comments, descriptions, HTML, and metadata should be mined for previously untracked URLs, usernames, post IDs, video IDs, and quoted/replied accounts.

## Execution environments

### GitHub Actions: public lane

Suitable for:

- public YouTube metadata, captions, thumbnails, comments where exposed, and best-available streams;
- exact raw GitHub assets and hash verification;
- public URL availability audits;
- ffmpeg frame extraction and contact sheets;
- metadata normalization and SHA-256 inventories;
- lead discovery from acquired text/JSON;
- artifact upload for later review.

GitHub-hosted runs must not receive personal Facebook/Instagram/X browser sessions. The one current exception is the dedicated research-only YouTube cookie secret used to cross YouTube's anti-bot gate; it is not tied to the user's personal account and is never written into the evidence artifact.

### Local or self-hosted authenticated lane

Suitable for:

- Facebook groups and individual posts requiring login;
- Instagram comments or posts blocked to anonymous extractors;
- X/Twitter pages requiring an authenticated session;
- browser-rendered captures of fragile social pages;
- Playwright HTML/screenshots/network context where downloaders fail.

Authentication state belongs in ignored local paths only.

### Repo analysis lane

Suitable for:

- frame extraction and frame-quality ranking;
- contact sheets;
- perceptual-hash deduplication;
- perspective-corrected crops;
- contrast/channel/sharpening variants;
- OCR-as-hint;
- comment snapshot diffs;
- media/source manifests;
- URL and username discovery.

## Source-specific strategy

### YouTube

Primary extractor: `yt-dlp`.

For each video preserve, where available:

- best source video/audio streams without needless re-encoding;
- `info.json`;
- description;
- thumbnails;
- human and automatic captions;
- comments and reply relationships;
- upload/channel identifiers;
- actual downloaded codec/resolution/format IDs.

Priority corpus:

- iam8bit official INSIDE Collector's Edition unboxing: `zhCdGdqCIRU`
- Inside Gaming CE unboxing: `AO2YQCl5qFM`
- Oddheader September 2026 mystery video: `ZqYhhptmhmo`
- historical ledger videos:
  `eXxklNxsVWw`, `Mhxynz-LoAI`, `fu7gmuJQKXM`, `jQUf8yhqEc4`,
  `ahCmqg1hhSA`, `G4z5r4rZH2w`, `Pbkq8Ey_s0k`, `d23bAqGtImo`,
  `Y7OqMKBbM2Y`, `uP5nSeyac_o`, `gqlQaHgRaHg`.

The Inside Gaming source is especially important because the historical ledger records a sticker as lost but partially visible in footage. Once the approximate interval is identified, extract every native frame across a bounded window, then rank/deduplicate only for review. Never discard the complete dense extraction.

Oddheader comments should be snapshotted repeatedly and diffed. New owner reports may arrive after the video itself is archived.

### General social media

Primary first-pass extractor: `gallery-dl`.

Use it for public/accessible Instagram, X/Twitter, Facebook, and VK media where supported. Preserve attached media and metadata. Browser screenshots are supplementary presentation/provenance aids, not substitutes for original attached media.

Secondary Instagram extractor: `Instaloader`, particularly for shortcode posts, carousels, captions, metadata, and authenticated comments when gallery-dl is incomplete.

### Browser-rendered evidence

Fallback: Playwright on a local or self-hosted machine.

A capture should retain:

- exact requested URL and final URL;
- acquisition timestamp;
- page title;
- rendered full-page screenshot;
- saved HTML;
- extracted outbound links/media URLs;
- optional HAR/network trace when useful;
- note identifying whether login was required.

Do not store auth state beside captures.

### Terminal 41 raw assets

The exact `terminal41.link/dat/saf_dat_col.html` file is a critical verified acquisition.

Expected:

- size: 1,986,163 bytes
- Git blob SHA-1: `349b818fce618ef55c404bedfb602b1d03f29a48`

Verification must use Git blob semantics:

`sha1("blob " + byte_length + NUL + bytes)`

or equivalently `git hash-object FILE`.

PR #56 also records the 19,360,240-byte Terminal 41 transmission PNG with blob SHA `127d8772912ffc499e5afaffe321d5bab7e920df`. Use the same verified-fetch machinery.

## Repository layout

Temporary/public workflow output should use a deterministic tree such as:

```
evidence-work/
  <source-id>/
    original/
    metadata/
    captions/
    comments/
    frames/
    contact-sheets/
    derived/
    acquisition.json
    hashes.sha256
```

Do not commit large acquired media automatically. Upload it as workflow artifacts first, then deliberately vendor high-value evidence or store it in the project's chosen archival location.

Committed small provenance records belong under the existing `data/`, `docs/`, and `archive/external/` conventions established by PR #56.

## Acquisition metadata

Every source acquisition should record at minimum:

- source ID;
- requested URL;
- final URL if known;
- acquisition UTC timestamp;
- extractor and version;
- result classification;
- HTTP status where applicable;
- output filenames;
- byte sizes;
- SHA-256 values;
- known expected Git blob SHA and whether it matched;
- authentication required: yes/no/unknown;
- notes/failure text.

Suggested result classes:

- `ok`
- `login-required`
- `removed`
- `redirected`
- `rate-limited`
- `extractor-broken`
- `network-error`
- `hash-mismatch`
- `manual-review`

## Frame archaeology

Use `ffmpeg`/ `ffprobe` rather than screenshots as the primary video-analysis path.

Generate:

1. broad interval samples for reconnaissance;
2. scene-change candidates;
3. dense native-frame runs around suspicious intervals;
4. contact sheets for human scanning;
5. source-preserving crops;
6. optional derived enlargement/contrast/channel/sharpening variants.

Ranking may use blur/sharpness, exposure, perceptual similarity, scene difference, and crop similarity. Ranking is a convenience layer only. Full originals and dense-frame runs remain available.

For tiny stickers/numbers, OCR is explicitly non-authoritative. It may produce candidate strings used to rank frames, but any claimed reading must be visually verified against source frames.

## Comment archaeology

Store complete timestamped comment snapshots before filtering.

For repeated snapshots:

- diff by stable comment ID;
- preserve parent/reply relationships;
- flag newly added comments;
- rank keywords only for review;
- keep the unfiltered snapshot.

Initial review vocabulary may include `sticker`, `number`, `collector`, `edition`, `mine`, `photo`, `box`, `iam8bit`, and plausible serial-number patterns, but the pipeline must not discard non-matching comments.

## Discovery spider

Every text/JSON/HTML acquisition should be scanned for:

- absolute URLs;
- YouTube video IDs;
- Instagram shortcodes;
- X/Twitter status IDs;
- Facebook group/post IDs;
- usernames/handles where unambiguous;
- quoted/replied accounts.

Compare discoveries with canonical manifests and emit an untracked-leads report. Do not automatically promote every discovered link to canonical evidence; human review decides whether it belongs.

## GitHub Actions

Two lanes are appropriate:

### Scheduled audit

A lightweight scheduled/manual workflow:

- performs HEAD/GET probes without downloading large media;
- records live/redirected/login-required/removed/error states;
- uploads an audit JSON artifact;
- does not mutate canonical evidence automatically.

### Manual public harvest

A manually dispatched workflow:

- chooses one source ID or all public targets;
- installs `yt-dlp`, `gallery-dl`, and uses system `ffmpeg`;
- fetches public metadata/media according to the target manifest;
- verifies known raw assets;
- writes acquisition metadata and hashes;
- uploads the output as a short-retention Actions artifact.

Large, high-value results should then be deliberately promoted into archival storage.

## Security / privacy

Never commit or upload:

- cookies;
- Netscape cookie jars;
- browser profiles;
- Playwright `storage_state.json`;
- passwords;
- API tokens;
- Facebook/Instagram/X session tokens.

Use ignored local paths such as `.evidence-private/` and `playwright/.auth/`.

If a self-hosted runner is later added, isolate it from unrelated repositories and avoid exposing personal browser state to arbitrary PR code.

## Live acquisition status and ownership

Snapshot: 2026-09-29. This section is the execution-facing status surface for PR #57. PR #56 owns archival intake/vendor decisions and is being actively updated by another agent; do not duplicate that work here.

### Do now in PR #57

- **Inside Gaming CE unboxing:** authenticated full-media harvest is active now. When the artifact lands, locate the partially visible lost sticker, extract a bounded dense native-frame window, preserve all source frames, and generate review aids.
- **Historical YouTube ledger corpus:** harvest metadata/thumbnails first for all remaining ledger videos plus the official iam8bit making-of/reveal; then acquire media/comments where they can add owner/sticker provenance.
- **Public social corpus:** run the public extractor across all X/Twitter, Instagram, and VK targets; preserve successful originals and classify blocked/no-media targets for manual follow-up.
- **Lead discovery:** run URL/account discovery over every acquired text/JSON/caption/comment artifact and reconcile new leads into the manifest after review.
- **Oddheader comments:** preserve comment snapshots for owner discovery. The video itself is human-reviewed negative for unknown sticker imagery.

### Already acquired / resolved enough to stop reacquiring

- **Terminal 41 saf_dat_col.html:** exact 1,986,163-byte upstream file is acquired and verified against Git blob SHA-1 349b818fce618ef55c404bedfb602b1d03f29a48.
- **iam8bit CE unboxing (zhCdGdqCIRU):** authenticated metadata/description/thumbnail acquisition works. Human review says the video contains no unknown sticker information, so no further frame archaeology is planned absent a new concrete reason.
- **Oddheader 2026 video:** authenticated metadata/caption/comment acquisition works. Human review says the video contains no unknown sticker information; retain it for owner/comment provenance only.
- **YouTube auth/tooling:** dedicated research-account cookies plus Node/EJS challenge solving work on GitHub-hosted Actions.
- **Public X proof-of-path:** the KaydHendricks status has successfully yielded original media and metadata; expand this to the rest of the X queue.

### Human-only / external dependency

- **Facebook groups/posts:** logged-in group search and original-media preservation remain human-browser work. The Limited Printed Games group is highest priority because sticker #002 came from there.
- **#stickers-solving Discord export:** absent from the current 1.7 GB public export. Acquire only if moderators/community can provide it; this is the largest remaining Discord corpus gap.
- **Production-side source material:** outreach to iam8bit/Playdead/packaging vendors for variable-data sticker source files, proof sheets, scripts, or imposition assets remains potentially transformative but is not an automated scraping task.
- **BigDusty local-only artifacts:** Tier 29 scripts/logs and the claimed 42x42 Sleep BMP remain external recovery targets unless PR #56 acquires them first.

### PR #56 archival lane, do not duplicate while active

PR #56 owns the canonical external archive, canonical binary-asset manifest, Terminal 41 transmission PNG/sticker-binary acquisition, BigDusty archive archaeology, and decisions about which acquired originals belong in Git versus workflow artifacts/external storage. PR #57 should hand it verified acquisition outputs and provenance rather than independently vendoring the same assets.

## Implementation phases

### Phase A: foundations

- Add this plan.
- Add machine-readable acquisition target manifest.
- Add exact Git-blob verifier.
- Add URL audit helper.
- Add public harvester wrapper.
- Add frame-extraction helper.
- Add lead-discovery helper.
- Add GitHub Actions audit and manual-harvest workflows.
- Add secret/auth ignore rules.

### Phase B: immediate corpus harvest

- Acquire all listed YouTube metadata/captions/thumbnails/comments.
- Acquire best available source streams where practical.
- Fetch and verify `saf_dat_col.html`.
- Fetch and verify Terminal 41 transmission PNG.
- Attempt public gallery-dl capture of Instagram/X/VK targets.
- Record login-required failures explicitly.
- Generate broad video contact sheets.

### Phase C: targeted archaeology

Human review on 2026-09-29 established that the iam8bit Collector's Edition unboxing and the Oddheader INSIDE mystery video contain no unknown sticker information. Keep them as provenance/context sources, but do not spend further frame-archaeology budget on them unless new evidence gives a concrete reason to revisit.

- Identify the Inside Gaming sticker interval and extract every native frame around it.
- Run frame ranking/deduplication and preserve the full dense source set.
- Preserve Oddheader metadata/comments for owner-discovery and historical context, not sticker-frame discovery.
- Review public social acquisitions for CE/sticker visibility.
- Promote valuable originals and provenance records into the external archive.

### Phase D: authenticated/manual recovery

- Run authenticated local/self-hosted captures for Facebook groups/posts and blocked Instagram/X sources.
- Search the two Facebook groups for INSIDE, Playdead, iam8bit, RealDoll, Huddle, and Collector's Edition.
- Preserve original media plus page/thread context.
- Add newly discovered owner leads to the canonical manifest.

### Phase E: recurring maintenance

- Scheduled availability audit.
- Periodic Oddheader comment snapshots while the current owner-discovery wave is active.
- Untracked-lead reports after new corpus ingestion.
- Re-check extractor failures after downloader updates.

## Completion criteria

This plan is substantially implemented when:

- every known source has a canonical manifest entry;
- public sources can be harvested or classified with one command/workflow;
- authenticated sources have a documented local capture path;
- exact raw assets are cryptographically verified;
- videos can be converted into reproducible contact sheets and dense frame sets;
- comments can be snapshotted and diffed;
- new links can be surfaced automatically;
- no authentication material is required in the repository;
- high-value evidence can be traced from conclusion back to immutable source bytes.

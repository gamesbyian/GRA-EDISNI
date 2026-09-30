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

- **Inside Gaming CE unboxing:** full media and native-frame forensics are complete enough for current purposes. Canonical lost entry L14 is slash-confirmed; the serial zone is physically occluded by fingers throughout the useful sequence. L14 background-tile classification is paused while PR #61 builds canonical A-I masters.
- **Historical YouTube ledger corpus:** metadata/description/thumbnail sweep is complete for all 11 ledger videos. Authenticated CE-media reconnaissance is complete for 02/03/04/05/06/09/10/11; targeted forensics are recorded for the lost/unresolved entries. Video 07 (L17) is the remaining justified one-source media candidate; videos 01 and 08 are owner/provenance sources rather than frame-mining targets. The separate iam8bit making-of/reveal remains age-restricted.
- **Public social corpus:** broad sweep and first-pass mining are complete. Eight X/Twitter targets yielded original media; only ItsaMeFernando contained a readable sticker and independently reconfirmed canonical 324 = slash. Other X targets are now classified against canonical provenance. Instagram remains login-required, VK produced no useful media, and tiny classification-only outputs are not acquisitions.
- **Lead discovery:** run URL/account discovery over every acquired text/JSON/caption/comment artifact and reconcile new leads into the manifest after review.
- **Oddheader comments:** a full authenticated snapshot is preserved (3,180 comments in the current artifact). The normalized queue is `data/oddheader-owner-leads-2026-09-29.json`. Unverified 369=dot is the highest-value verification lead because it would contradict the current invariant residue-45 dash prediction if physically confirmed; 427=dot is a useful residue-103 hidden-state discriminator. Both remain quarantined until physical photos exist.

### Already acquired / resolved enough to stop reacquiring

- **Terminal 41 saf_dat_col.html:** exact 1,986,163-byte upstream file is acquired and verified against Git blob SHA-1 349b818fce618ef55c404bedfb602b1d03f29a48.
- **iam8bit CE unboxing (zhCdGdqCIRU):** authenticated metadata/description/thumbnail acquisition works. Human review says the video contains no unknown sticker information, so no further frame archaeology is planned absent a new concrete reason.
- **Oddheader 2026 video:** authenticated metadata/caption/comment acquisition works. Human review says the video contains no unknown sticker information; retain it for owner/comment provenance only.
- **YouTube auth/tooling:** dedicated research-account cookies plus Node/EJS challenge solving work on GitHub-hosted Actions.
- **Public X proof-of-path:** completed across the current queue; statuses now distinguish original-media acquisitions, no-media extractor results, and already-canonical provenance.

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
- Terminal 41 transmission PNG/raw-archive acquisition is delegated to PR #56; consume its result rather than duplicating it.
- Public gallery-dl social sweep completed; do not repeat broadly unless extractor behavior changes or a concrete new target appears.
- Record login-required failures explicitly.
- Generate broad video contact sheets.

### Phase C: targeted archaeology

Human review on 2026-09-29 established that the iam8bit Collector's Edition unboxing and the Oddheader INSIDE mystery video contain no unknown sticker information. Keep them as provenance/context sources, but do not spend further frame-archaeology budget on them unless new evidence gives a concrete reason to revisit.

- Inside Gaming/L14 native-frame forensic pass completed; serial is geometrically occluded and background classification is paused pending PR #61 A-I masters.
- Run frame ranking/deduplication and preserve the full dense source set.
- Preserve Oddheader metadata/comments for owner-discovery and historical context, not sticker-frame discovery.
- Public social acquisitions reviewed and reconciled against canonical provenance.
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


## 2026-09-29 mining checkpoint

The historical acquisition sweeps have moved from “running” to a mined/manual-dispatch posture.

- Historical CE full-media reconnaissance completed successfully for ledger videos 02, 03, 04, 05, 06, 09, 10, and 11. Preserve the existing Actions artifacts; do not repeat those multi-gigabyte downloads without a concrete new reason.
- Ledger video 10 (`uP5nSeyac_o`) has been reviewed across its complete 6.683-second source at dense 0.25-second coverage and is negative for a visible numbered sticker.
- Ledger video 03 (`fu7gmuJQKXM`) is already tied by the canonical ledger to physical sticker 242 = dash, background H. The whole-source 2-second sampling did not independently resolve the serial, so preserve that result as a sampling limitation rather than a negative evidence classification. Ledger video 11 (`gqlQaHgRaHg`, IGN) is canonical U01: targeted native review around 53.1-53.4 s reconfirms slash, while fingers occlude the lower/serial side throughout the useful exposure.
- The lightweight historical metadata/thumbnail sweep successfully covered all eleven ledger videos. The iam8bit making-of/reveal remains age-restricted for the research account and should stay classified as blocked/authenticated rather than silently successful.
- Public X extraction yielded original media for KaydHendricks, TheAnnaTheRed, hubalubalu, triplizard, ItsaMeFernando, MinnMax, frmlssndmpty, and nicelyneatly. Visual mining found no new sticker observation; the Fernando original independently confirms already-canonical 324 = slash.
- Tiny status-only X outputs are not acquisitions. Instagram outputs from the public lane are login-required, and the VK lane produced no useful media.
- Oddheader comment claims 427 = dot and 369 = dot remain quarantined as unverified owner claims pending physical-photo provenance.
- L14 background-tile classification is intentionally paused. PR #61 owns the canonical A-I tile-master reconstruction; resume L14 classification only after those masters are available.
- PR #56 remains the archival-intake/vendor owner. This branch should consume or hand off provenance, not duplicate its raw-source promotion decisions.

Near-term mining order: finish reviewing the already-acquired CE recon artifacts before any new dense downloads; cross-reference Oddheader owner leads against canonical/Discord ownership history; then pursue only sources that can plausibly add a new physical sticker or owner provenance.


### Lost-sticker video forensics and owner-lead sweep

The existing authenticated artifacts now support a targeted lost-entry forensic lane without new downloads:

- **L12 / ahCmqg1hhSA**: dash reconfirmed around 124 s. Native 10 fps review plus perspective rectification does not resolve a serial.
- **L13 / G4z5r4rZH2w**: dash reconfirmed around 143 s. The serial-print zone is physically exposed in several relatively frontal frames; registered/rectified inspection yields only unstable gray blobs, not defensible numeral strokes. This is a strong candidate for original/raw-footage recovery because geometry is not the limiting factor.
- **L35 / Y7OqMKBbM2Y**: dash reconfirmed around 129 s. Motion/obliquity destroys serial detail; no serial is defensible.
- **L11 / jQUf8yhqEc4**: the acquired source has been inspected through the high-probability unboxing/black-wrapping phase to roughly 356 s, with dense inspection around 156-228 s. No defensible sticker face, symbol, or serial was recovered.
- **221 / Mhxynz-LoAI** is already a canonical physical observation (221 = slash, background E); do not spend new acquisition effort merely re-proving it.

Oddheader owner discovery now has a finite, provenance-stable shortlist rather than a generic comment-mining task:

- 427 = dot, @Douleur873: unverified claim, no photo. Serial 427 maps to residue 103, where the frozen matrix is state-dependent and modally prefers dot (10/14 states), making a physical photo a useful hidden-state discriminator.
- 369 = dot, @Byokugen: unverified claim, no photo. This is now the highest-value owner verification lead because serial 369 maps to H108 residue 45, while the frozen matrix predicts invariant dash there; a genuine dot photo would directly falsify part of the current reconstruction.
- @HAL-iv2kd: says a newly bought CE sticker was discarded; remembers slash and thinks one serial digit was 4. Recollection only.
- @time_travel_01: says they own an unopened CE.
- @cultuschoco: says they bought a CE for themselves.
- @BOBDOLE480: says a friend owns an unopened CE.
- @Blorbious: says they have a sealed box.
- @z304legend: says they have a copy but do not want to open it.
- @jakeduggins5141: said they had a copy/card but explicitly declined follow-up; do not prioritize further outreach.
- @billlee1821: says their sticker was already contributed; resolve identity/history before any outreach.

Exact-handle checks against the current canonical sticker-ledger snapshot found no match for the newly surfaced owner handles above. That absence is not proof that their stickers are new; Discord identity drift and different usernames remain possible.

Acquisition priority from this point should favor owner/photo provenance and original/raw footage for L13 over additional generic corpus accumulation.


The normalized owner/provenance work queue is now `data/oddheader-owner-leads-2026-09-29.json`. It records stable YouTube comment/channel IDs, claim type, photo status, canonical-handle cross-reference result, H108/model relevance where applicable, priority, and the next evidence action. Future agents should update that queue rather than re-mining the entire Oddheader snapshot from scratch.


### Single-source manual media escalation

Use `.github/workflows/targeted-youtube-media-recon.yml` when one specific YouTube source has passed lightweight triage and deserves full media. It is manual-dispatch only, validates an exact manifest `source_id`, acquires only that source, creates whole-source sample/scene reconnaissance, and can optionally create a bounded 5 fps focus window. This prevents a single justified lead from re-running the historical eight-video batch.

Current first candidate: `youtube-ledger-07-Pbkq8Ey_s0k` (L17). Metadata shows a 172-second Kyle Hilliard recording-booth video; the canonical ledger confirms his CE/sticker was later lost but records no symbol. This is a proportionate one-source visual check.

Do not escalate `youtube-ledger-01-eXxklNxsVWw` merely for frames: it is the 2025 Oddheader retrospective and its value is owner/comment discovery. Do not escalate `youtube-ledger-08-d23bAqGtImo` merely because the Huddle appears at 7:22: later owner contact already establishes the sticker was lost and only supplies a ~90%-sure slash recollection, not physical imagery.


For lightweight owner discovery, use `.github/workflows/targeted-youtube-comments.yml` to snapshot one manifest-listed YouTube source without re-running the hard-coded Inside Gaming/Oddheader pair. The first high-value candidate is `youtube-ledger-01-eXxklNxsVWw`: its 2025 Oddheader retrospective demonstrably caused later owner contributions 072 and 476, and the canonical ledger still contains unresolved commenter U45.


U45 owner provenance is now stronger: the same YouTube account `@hoodratthings4088` (channel `UCSfDy7vqionpbw5Z8-eHexw`) that produced the unresolved 2025 owner lead states in the 2026 Oddheader snapshot that they still have a copy and “contributed my codes years ago.” Raezores asked for the sticker number or historical submission identity, with no later answer in the current snapshot. Treat U45 as an identity-reconciliation task, not a new observation.

### Lost-sticker video forensic checkpoint

Targeted native-frame review has now closed four historical lost-video leads without inventing serials:

- **L11 / L16 (`jQUf8yhqEc4`)**: full 19-minute source sampled end-to-end, with 0.5-second coverage of the 200–240 s black-wrapper handling interval. No readable sticker face/serial appears. Keep symbol and serial unknown from this source.
- **L12 (`ahCmqg1hhSA`)**: native 1080p/60 fps review around the historical ~124 s pointer confirms the dash symbol. No stable serial digits are readable.
- **L13 (`G4z5r4rZH2w`)**: native 1080p/60 fps review around ~143 s gives the clearest sticker face of the set and confirms dash, but still no defensible serial digits.
- **L35 / U02 (`Y7OqMKBbM2Y`)**: dense/native review around ~129–133 s confirms dash; the number area is compromised by hand/forearm occlusion and motion blur.

These are now explicit forensic negatives for serial recovery from the available YouTube encodes. Future work on those serials should prefer alternate/raw footage or independent owner photos, not stronger image processing of the same pixels.

Oddheader owner/serial leads were also exact-searched against both the current repository corpus and the mined `gamesbyian/playdead-unofficial-exports` fork. No indexed match was found for the 427/369 claimants or the other named owner leads. This reduces the chance of obvious duplicate outreach but does not constitute proof that the owners were never represented historically.

### Oddheader comment-mining refinement

The authenticated 3,180-comment snapshot has now been mined beyond the first obvious serial claims.

- `@hoodratthings4088` is not a fresh owner lead: the current community ledger already tracks the same person as **U45**, based on an older YouTube comment. Their new Oddheader comment says they still have a copy and contributed their code years ago; Raezores has already asked them to resolve the missing identity/sticker mapping.
- `@BOBDOLE480` reports a friend with an unopened Collector's Edition. Raezores has already replied explaining that only the outer shipping carton needs opening. Treat this as an active indirect lead and avoid duplicate outreach while waiting for a response/photo.
- `@jakeduggins5141` initially said they had a copy and asked to be contacted, but then twice declined requests to provide the sticker details/photo. Treat as declined and do not pursue further unless they re-engage voluntarily.
- A terse self-reply from `@DwellerFree` says `476 /`, but sticker **476 is already physically documented as dash (background H)**. The comment is context-poor and contradicted by stronger physical evidence, so it is quarantined rather than treated as a competing observation.

This pass found no additional short-form serial/symbol owner claims beyond 369, 427, and the ambiguous 476 comment.

### Lightweight incident-video reconnaissance

For historical videos that are not CE unboxings but merely contain a Huddle or other owner clue, use `.github/workflows/historical-ce-lightweight-recon.yml` before any full-resolution acquisition. It accepts a single source target and acquires only a <=240p video stream, then samples the complete source at 1 fps plus scene changes.

This was validated on L17 / `Pbkq8Ey_s0k`: run `36666370632` reviewed the complete 172-second source and found no CE packaging, black wrapping, or numbered sticker anywhere in the video. Full-resolution escalation is therefore not justified for that source.

The same reusable lane is now being applied to L30 / `d23bAqGtImo`, whose Huddle is historically visible around 7:22. The purpose is narrowly to determine whether sticker-bearing packaging appears anywhere near the Huddle or elsewhere in the source before spending on denser acquisition.

### Owner-comment snapshot lane

The YouTube comment workflow is now single-target rather than a fixed two-video matrix. It supports the 2025 Oddheader roundup (`eXxklNxsVWw`), Inside Gaming, and the 2026 Oddheader mystery video, with manual dispatch for future refreshes.

The 2025 Oddheader roundup is a high-value owner-discovery source because its historical comments already led to physical sticker observations 072 and 476 plus unresolved U45. A fresh authenticated comment snapshot is therefore being mined for additional owner claims, serial/symbol reports, or replies that resolve U45. Current run: `36667932888`.

### 2025 Oddheader comment snapshot result

Authenticated run `36667932888` captured **1,166 comments** from `eXxklNxsVWw` and was mined for ownership, sticker, serial, symbol and packaging language.

The only clearly fresh CE-owner lead is `@PsychOsmosis` (`UCb4w58w_rLCmvYQLpGtKXQA`), who says they own an INSIDE Collector's Edition and may still have the original packaging somewhere. There is no reply/outreach in the captured thread, and exact-handle searches found no match in the current GRA-EDISNI corpus or the `gamesbyian/playdead-unofficial-exports` fork.

The other high-signal ownership comment is `@hoodratthings4088`, already cross-referenced to canonical unresolved U45. No additional defensible serial/symbol claims were found in this snapshot.

### #stickers-solving gap resolved

The previously missing Discord channel is now publicly available upstream. `twinysam/playdead-unofficial-exports` commit `928242dc548e766e50c93f0bdcaa52ddbc7cfc42` (`Add #stickers-solving`, 2026-09-29) adds a 2,509-line transcript plus attached assets/scripts for channel `ARG / stickers-solving` (`1552077397493424272`).

The user's fork predates that upstream commit, so the first mining pass used the immutable upstream commit directly rather than rewriting or disturbing the existing fork mining branches. Reconcile the fork separately when safe.

First-pass durable results:

- direct community provenance for the labeled background-piece order: `I A B / C D E / F G H`;
- explicit contemporary discussion of the **9×12 manufacturing-sheet explanation** for H108/background-column structure, with a physical sticker measurement and backing-sheet description proposed as discriminating evidence;
- an explicit methodological rejection of reconstructing lost physical sticker facts from owner memory/purchase geography alone;
- a frozen historical prediction that stickers **197, 198, 200, 203, 205** should be dots under the then-current community model, with **200** named as the preferred discriminator. None currently has a canonical physical sticker row, so this remains genuinely prospective rather than retrospectively scored.

The transcript also preserves the then-current 82-found / 42-lost / 35-open-owner snapshot and multiple hypothesis/negative-result discussions. Continue targeted mining for provenance, owner leads, manufacturing clues, and historical predictions; do not indiscriminately promote community models into current-project conclusions.

### Historical provenance recovered from older Discord exports

Targeted follow-up through the older exported `#tldr` and `#solving-breakout` channels recovered the original lineage behind two facts that had recently been treated mostly as inherited community knowledge.

**A-I background puzzle provenance.** On 2020-03-20, `elronodelp` documented that high-resolution sticker photos could be separated into nine relief/background classes A-I and that representative images from those classes reconstructed another view of the initial Morse printer. On 2020-04-28, `pitch_bright` posted the contemporaneous `Sticker Puzzle Solution` composite. The preserved asset (`assets/StickerSolution-dc12d5e516ca4922.png`, blob `2d9fd5b60faa3d5fdb25ebc63ab3f77be3138b46`) visibly fixes the spatial order as `I A B / C D E / F G H` and shows the solved path `dat/534brn9653f9j8mmd/`. This provenance has been handed to PR #61 without touching its live master-building work.

**108-cycle lineage.** The earliest surviving explicit 108-era work found in the exported `#solving-breakout` history is from `lime8159` on 2022-12-23: a `3x36` sticker rendering, followed the same night by discussion of 216 versus 108 and the observation that 216 only adds redundant data if the symbols repeat every 108. On 2022-12-24 they said they were increasingly confident in 108 while explicitly cautioning that 12x9 dimensions were not established. In November 2023, the same user attached `sequence_prob-bb1047802f422f07.txt` and reported a roughly `1e-8` historical probability for 108 under that calculation; another participant reported a less extreme but still sub-0.1% result. Keep those old p-values as provenance only: the current project has its own better-specified null analyses.

**Authenticity/provenance caution.** A 2026 discussion asked how fake sticker submissions were excluded. Community responses pointed mainly to distinctive relief/print appearance and source context, not a formal authentication protocol. Therefore current acquisition should continue to privilege original physical photos, owner/source chains, and repeated-structure consistency over isolated text claims.

The recovered upstream `#stickers-solving` attachment audit found no new physical sticker observation: the only direct sticker photo in that newly added batch is 003 = dash, already canonical. Other inspected attachments are layout/model/cipher visualizations, screenshots, packaging context, or user-generated research artifacts.

### Blocker reclassification

A canonical-ledger cross-check substantially reduced the apparent blocked-social backlog.

- All nine specific Instagram post targets are already resolved in the canonical ledger, either to a physical sticker observation (187, 296, 384, 223) or a confirmed-lost provenance trail (L15, L21, L32, L34, L35). Login is now an **archival-original-media** issue only for those URLs, not a sticker-information dependency.
- Instagram account targets `mattpopcollector182` and `bathroomgamers` are likewise already resolved to canonical physical stickers 125 and 334 respectively.
- The Facebook story for johnny_iuccy is already canonical 223; the DaniaGames shared post is already L34. Those specific URLs are archival-only. The two private Facebook collector groups remain useful manual **owner-discovery pools**, because they historically produced multiple stickers/owner leads.
- The VK lead `bigdaffymonster` is already canonical L40/U34; the owner confirmed through VK on 2026-05-04 that the sticker was lost. Failed public VK media extraction is archival-only.

This means the genuinely research-blocking social work is now concentrated in **new-owner discovery** and unresolved current claims (notably the unsupported 369 and 427 claims, U45 identity resolution, PsychOsmosis, and other unopened/current-owner leads), rather than recovery of every historical Instagram/Facebook/VK original.

### Unresolved-owner acquisition checkpoint

A canonical Uxx coverage audit showed that the acquisition manifest had accumulated many resolved historical social URLs while omitting several genuinely unresolved owners. The manifest now explicitly tracks recent/public U27, U32, U33, U35-U38, U40-U47 sources where evidence can still be mined without duplicating owner outreach.

Results from focused probes:

- **U27 / MinnMax 2022 charity auction:** a narrow media probe plus English auto-caption transcript recovers the winning bidder token as **Mike M**. During the INSIDE CE auction the hosts repeatedly address Mike/Mike M, perform "going once / going twice", thank Mike after the close, and later state the item was sold. The video only displays an official iam8bit prize card and contains no winner sticker image. Contemporaneous public MinnMax supporter listings identify community supporter **Divorced Cougar (Mike M)**; treat that as a strong contextual handle match, not an explicitly verified auction identity. Ben Hanson already notified the winner historically, so do not duplicate outreach.
- **U33 / doctornowhere:** original 1536x2048 X media acquired. It confirms the Huddle and red INSIDE CE box in the owner's possession but exposes no sticker-bearing black wrap/game surface.
- **U44 / Squee:** the archived 2018 forum page is acquired and pins the ownership statement to Squee's "I bought this..." post linking the iam8bit CE. No sticker photo appears.
- **U46 / Stephen Sinnott:** authenticated snapshot contains 615 comments and preserves `@stephensinnott2591` / `UCm2r-OsdlwU_eU8FDOMTs3Q` saying "I have the Huddle." The captured reply thread contains no sticker number/photo.
- **U41-U43 / PriceCharting:** all three public offer pages are now acquired. They verify collection/listing provenance for `lvncqw`, `vrxqyq`, and `jotonic`; all display the same generic product cover image rather than owner sticker media. U43 is labelled "New Item, Box, and Manual", which is marketplace metadata and must not be converted into a sticker-survival claim.
- **U32 Reddit:** direct repository fetch is reproducibly HTTP 403, but stable public/index evidence preserves KoreanB_B_Q's 2020 sale history. Current purchaser `skorba71` remains unresolved and already contacted.
- **U35 / PSNProfiles:** direct fetch is HTTP 403.
- **U40 / PlayStation Instagram:** public extraction hit repeated HTTP 429 and yielded no media. This remains provenance/access evidence, not a confirmed owner sticker.

The operating priority is now unresolved **current-owner evidence**, not archival perfection for sources whose sticker status is already canonical. Existing outreach history must be checked before any contact recommendation.

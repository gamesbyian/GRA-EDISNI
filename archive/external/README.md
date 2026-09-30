# External research corpus intake

Snapshot date: 2026-09-29

This directory preserves high-value external research material and tooling needed to reconstruct the INSIDE ARG / Collector's Edition sticker investigation without depending on mutable web pages.

## Rules

- Preserve exact upstream provenance: source repository/path, ref and blob SHA.
- Vendored copies are evidence snapshots, not project-authored conclusions.
- Prefer exact source artefacts and executable material over prose summaries.
- Large media, social-platform content and licensing-sensitive material should normally be represented by manifests, hashes, retrieval notes and source URLs until a justified archival copy is available.
- Do not treat an external claim as verified merely because it is preserved here.

## Preserved corpora

### BigDusty INSIDE ARG Investigation Map

Preserved under `archive/external/bigdusty/`.

Current intake includes:
- project README;
- six puzzle dossiers: stickers, terminal41, printer, viewgate token, breach hashes, transmission/chip imagery;
- `data/block_descriptions_full.json`;
- `data/canvas.canvas`.

Why: this is the strongest independently structured 2026 research corpus found outside the canonical twinysam documentation. It also records negative experiments and several local-only reproducibility gaps.

Important missing assets to pursue:
- local `code/loose_scripts/*` referenced by the dossiers;
- `code/predict_648_chain.py`;
- sticker GUI / GPU search artefacts;
- Tier 29 mojibake reversal scripts and logs;
- exact source blob and recovered 42x42 “Sleep” BMP;
- local Wayback mirror paths referenced in the notes.

### twinysam/INSIDE-ARG

Preserved under `archive/external/twinysam-inside-arg/`.

Current intake includes:
- current ARG overview;
- current sticker ledger;
- Raezores research methodology.

Why: this is the canonical historical/public documentation and current owner/sticker provenance ledger.

Next preservation targets:
- relevant `terminal41.link/` mirror files;
- sticker images and edited references needed by current experiments;
- historically interesting fork-only/deleted material after diffing forks;
- issue/discussion artefacts containing unique hypotheses.

### Rooster Teeth archive

Preserved under `archive/external/rt-archive/`.

Current intake includes the Inside Gaming Features metadata JSON containing the 2020-01-25 item “The Inside Collector's Edition.”

Why: the canonical sticker research identifies Inside Gaming footage as a potentially lost physical-evidence source. The metadata confirms an archived programme entry that can be pursued for footage/frame extraction.

### inside-noclip

Preserved under `archive/external/inside-noclip/`.

Current intake includes:
- README;
- Cheat Engine table;
- helper Lua;
- upstream license.

Why: this gives camera/player manipulation instrumentation for INSIDE and may be useful if external-consumer or physical-scene hypotheses require inaccessible geometry or clean captures.

## Reference-only / manifest-first sources

Do not blindly vendor these. Preserve URLs, identifiers, dates, relevant excerpts, hashes where available, and acquisition status.

- Game Detectives INSIDE ARG page and linked working documents.
- Steam “Compilation of Secrets and Mysteries” threads and early number/cipher discussions.
- MistARG Chinese-language retrospective.
- Xbox Wire 2019 ARG feature.
- iam8bit Collector's Edition product page and promotional material.
- Playdead Unofficial Museum.
- public Reddit threads, YouTube videos/comments, eBay listings, X/Twitter posts, Instagram posts.
- Facebook groups: Limited Printed Games, Video Game Vinyl Collectors, Collector's Edition Video Game Boxsets Enthusiasts!.
- Oddheader INSIDE episode and comment/owner leads.
- Russian/StopGame/VK and other multilingual owner-hunt leads.

## Immediate acquisition queue

1. Reproduce and preserve BigDusty local-only experiments, especially Tier 29 byte/mojibake reversal and the claimed 42x42 BMP.
2. Inventory and preserve the twinysam `terminal41.link/` mirror, prioritising `saf_dat_col`, breach registry, viewgate pages, printreqstatus snapshots and `534brn9653f9j8mmd` assets.
3. Diff historical INSIDE-ARG forks for deleted/renamed files, obsolete notes and lost attachments.
4. Acquire the Inside Gaming Collector's Edition video or the best surviving copy and extract sticker-region frames.
5. Build a social/video evidence manifest with stable IDs, dates, owner-copy provenance and duplicate-footage relationships.
6. Keep PR #55's Discord-export archaeology canonical for Discord-derived material; do not duplicate its recovered files here.

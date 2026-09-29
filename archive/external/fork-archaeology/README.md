# INSIDE-ARG fork archaeology census

Snapshot date: 2026-09-29

Purpose: preserve and classify historical public snapshots of `twinysam/INSIDE-ARG` without duplicating identical trees unnecessarily.

## Canonical current source

- `twinysam/INSIDE-ARG`
- current README blob: `97476d5b0a47a51eee05bb4a6cfee657ad922218`
- current sticker ledger blob in canonical source at intake: `0b12cea77679ff937611dade334a60c6807dfb46`
- current Raezores methodology blob: `2ff09eeff1f15985f2e6823d794641e19c01f53e`

## Forks / historical snapshots found

### Raezores/INSIDE-ARG
- README blob: `2accefe3581faf1af9031d15655f98dd3375ce00`
- no `stickers.md` or `raezores-research.md` at current fork head
- preserved: `archive/external/fork-archaeology/Raezores/readme.md`
- interpretation: early historical state, worth keeping because it predates the later dedicated sticker ledger.

### cualquiercosa327/INSIDE-ARG
- README: `e0b24a4d9998674205a2b59eb1bed0212f6ad925`
- stickers: `60082ac7af7cbffa60ed923a164c95ada7bd0eed`
- Raezores methodology: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/60082ac7-cualquiercosa327.md`

### otanim/INSIDE-ARG
- README: `e0b24a4d9998674205a2b59eb1bed0212f6ad925`
- stickers: `5c52e73ad38e47e4525e59195dcecb646e0eb065`
- methodology: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/5c52e73a-otanim.md`

### BKR42/INSIDE-ARG
- README: `e0b24a4d9998674205a2b59eb1bed0212f6ad925`
- stickers: `201ce96d8ffc0a0c92267d9605807132b6a73f7b`
- methodology: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/201ce96d-BKR42.md`

### Akiraiscool/INSIDE-ARG
- README: `e0b24a4d9998674205a2b59eb1bed0212f6ad925`
- stickers: `cf2a37df851efc124695adaec0338efa2792ef7a`
- methodology: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/cf2a37df-Akiraiscool.md`

### PitchBright/INSIDE-ARG
- README: `e0b24a4d9998674205a2b59eb1bed0212f6ad925`
- stickers: `e197b2a58e7eb34a18cd01408340467bc5704144`
- methodology: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/e197b2a5-PitchBright.md`

### Alberto-X/INSIDE-ARG
- README matches current canonical README blob: `97476d5b0a47a51eee05bb4a6cfee657ad922218`
- stickers: `466b133f4962b9594ddb0188ca9cb1db5642b720`
- methodology remains older: `e117a4571135bd38090f409c6486286ef4b8c948`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/466b133f-Alberto-X.md`

### Mn0ky/INSIDE-ARG
- README matches current canonical README
- methodology matches current canonical methodology
- stickers: `fede23441b7f1685983a0c2b07e6798574d7f06f`
- preserved sticker snapshot: `archive/external/fork-archaeology/sticker-ledgers/fede2344-Mn0ky.md`

### ikkraa112/INSIDE-ARG
- README, stickers and methodology match Mn0ky at audited head.
- no duplicate snapshot vendored.
- useful as corroboration that `fede2344...` was a propagated public state.

## What this establishes

The forks are valuable mostly as chronology, not as independent evidence. Multiple distinct sticker-ledger blob SHAs survive publicly, giving reconstructable historical states of the owner/sticker hunt. Identical blobs across forks should not be counted as independent observations.

## Next fork-archaeology work

- diff preserved sticker snapshots semantically to recover which entries appeared between states;
- inspect old commits around each fork head for deleted image paths, owner leads and note changes;
- search fork trees for files absent from current canonical master;
- record dates for each distinct sticker-ledger state so the provenance lineage becomes chronological rather than merely structural.

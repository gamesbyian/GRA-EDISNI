# SecretMap original-asset recovery boundary and native-orb registration protocol

_Date: 2026-10-08. Separate, source-only experiment. No sticker completions._

## Decision

The July 2016 `SecretMap` extraction has a real historical witness but **we still do not have the original game asset**. The canonical 2016 Unity resource is neither in the project's documented game-code acquisition set nor in the 2,725-file `gamesbyian/playdead-unofficial-exports` archive tree examined today. That tree contains precisely **one** `.dds` file: the already-preserved 256×32 `BoardText` texture. The `SecretMap` and `Sign_SecretMorse` DDS images were republished as illustrations in Chinese articles, but no direct native data in these searched repositories. Searching GitHub names `SecretMap_916`, `SecretMap #44506.dds` and analogous phrases produced no additional game-asset repository in the bounded search.

Consequently the present evidence **cannot distinguish** a two-dimensional orb map, a 3D-projective schematic, a decoration or some other purpose at original-coordinate accuracy. The watermarked 2018 screenshot does not encode trustworthy scene-space coordinates. Counting red pixels in it and then fitting a free affine transform to 14 orb sites would be invalid source-after-target parameter selection.

## Independent source witnesses

- [July 2016 Steam original extraction exchange](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2): `SecretMap_#916` identified, its role debated.
- [3DM July 16 2016](https://www.3dmgame.com/gl/3577786.html): derivative witness, `SecretMap #44506.dds`; alternative interpretation as projected 3D scene.
- [9game March 2018 republication](https://www.9game.cn/news/2199070.html): illustrated repost with [SecretMap witness](https://image.9game.cn/2018/3/2/19669991.jpg). This is not native DDS.
- [Already archived real BoardText](https://github.com/gamesbyian/GRA-EDISNI/blob/main/archive/external/inside-2016-game-assets/BoardText_13309-b0922098d7c08dbe.dds): positive example proving other source assets can be preserved and independently decoded; no evidence of `SecretMap` within it.
- [Previous native asset/source-intake work](secretmap-boardtext-source-intake-2026-10-08.md), which cites blob identities and their limits.

These are not three independent proofs that the image is an orb map. The Chinese pages demonstrably derive from the international 2016 investigation.

## Prospective test, now committed

`scripts/audit_secretmap_registered_orbs.py` implements a controlled **maximum one-to-one matching** between independently collected native SecretMap marks and the fourteen known secret orb sites.

Input:
- source path + original exact hash and game build (to be acquired);
- marks with distinct IDs and *native* coordinates;
- separately sourced known orb points with IDs and common units;
- explicit **frozen** 2×3 registration matrix with provenance, before sticker comparison;
- preregistered tolerance in the same units.

Output:
- one-to-one marker↔orb matches (no one orb reused to absorb multiple marks);
- unmatched original marks and unmatched orbs;
- distances and provenance.

**No registration solver is included**: selecting a transform to minimize residual against fourteen desired sites is exactly the circular-fitting failure this experiment is intended to avoid. The program rejects missing source provenance and registrations not marked frozen.

A synthetic self-test is included to demonstrate duplicate marks cannot both be credited to one orb and that an unfrozen registration fails, but the committed script has **not been run from the repository** during this connector-only source pass. No original SecretMap input JSON exists, and therefore no real-orb outcome or “remaining marks” is claimed.

## Decision gates

1. **Native source**: actual original asset bytes with hash, game build, texture dimensions, pixel/channel interpretation and scene/mesh transform. Until this is obtained, stop claims about map coordinates or how many original marks represent secrets.
2. **Existing-game null**: compare markers against the fourteen known secrets using the above frozen geometry. Complete coverage would explain the map without requiring any CE-specific use.
3. **Meaningful unexplained residue**: a genuinely extra original mark or visual feature must have independent native semantics or consistent external location; a leftover caused by poor registration or missing orb coordinates is not automatically intentional.
4. **Sticker bridge**: only after steps 1–3, look for a pre-existing typed 9, 27, 108, A–I, or serial-number interface. No such interface is established presently.

## Original acquisition next steps

The most direct path is lawful extraction from a **version-pinned user-owned PC build** using a Unity asset browser, which would require access to the actual installed build; do not substitute unrelated downloadable Unity game assets. Search the complete original 2016 `postimg` gallery via archive snapshots as an alternative to the degraded 2018 repost. Preserve exact byte provenance and original use in scene when available.

**Current outcome:** new reproducible negative-control protocol and documented blocked acquisition. No native SecretMap recovery, registration result, sticker interpretation or new secret-ending content. Shift to other targets if exact asset evidence cannot be acquired.

## Contemporary July 2016 fourteen-marker explanation (Experiment 478)

The original [July 2016 extracted-texture discussion](https://www.reddit.com/r/PlaydeadsInside/comments/4sav9x/curious_textures_found_in_the_game_files/) does not merely label the asset `SecretMap #44506.dds`. One contemporary commenter already reports seeing a possible **fourteenth marker**, and another proposes the extra dot indicates the existing **large final orb**. This provides a clearly dated, ordinary-original-game interpretation years before Collector's Edition stickers existed.

This source changes the correct **null to test first**, not the results of any native image analysis: original DDS and scene UV bytes remain unrecovered, the posted image is not authoritative geometry, and other 2016 contemporary commentators proposed non-map/3D readings. A future original texture extraction must count marks **before** viewing the CE foreground, then test the thirteen small orb sites plus the large final orb using independently registered scene coordinates. Only unexplained, independently established residual marks justify reopening the CE correspondence lane.

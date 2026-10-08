# INSIDE: original-game asset census and destination-affordance audit

_Date: 2026-10-08. Research-only. No game binaries, complete asset bundles, missing sticker values or guessed keys were obtained or modified._

## Result

The 2016 **original-game asset** lane yields a more constrained set of plausible CE sticker destinations than searching the fiction or printer outputs generally. It includes already-decoded text, already-consumed gameplay instructions, duplicated/reused set dressing, possible developer self-reference, and a few unresolved assets without any known sticker-facing input grammar.

**No positively identified original 2016 asset in this bounded census yet supplies an independently demonstrated 108-sticker / nine-A–I / 81+27 address or a new game input accepting such a code.**

That is an evidence limitation, not proof that the original game contains no consumer. The full retail Unity bundles and gameplay assembly have not been acquired or inspected. This census is grounded in dated contemporary extraction reports rather than pretending asset bytes were obtained.

Machine-readable inventory: `data/original-game-asset-consumer-inventory-2026-10-08.json`.

## 1. Establish source identities, not just thematic resemblance

Primary contemporary reports are unusually useful:

- July 14–15 2016 [original Steam asset extraction discussion](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2): user-reported texture names, strings, locations, asset-index tags, possible roles.
- July 23–27 2016 [early cross-game mystery compilation](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=2): multi-place tune and separate Morse texture discussion.
- July 2016 [Chinese asset report](https://www.3dmgame.com/gl/3577786.html) and [GamerSky discussion](https://www.gamersky.com/handbook/201607/779252.shtml): contemporary translation/derivation of the same two extracted assets, `Sign_SecretMorse` and `SecretMap`, with **different exporter-generated identifiers**.

The 2016 Steam labels include `Sign_SecretMorse_#944` and `SecretMap_#916`; the Chinese report uses `Sign_SecretMorse #3372.dds` and `SecretMap #44506.dds`. There is no authorial reason to treat `944`, `916`, `3372`, or `44506` as clue coordinates. Their variation is a strong warning that extractor indexes are **provenance metadata**, not stable puzzle payloads.

Source independence caveat: the Chinese pages recount the international community's work and often reuse the same discoveries. These are extra preserved witnesses, **not** statistically independent confirmation of purposeful ARG meaning.

## 2. Historical game-asset accounting

| Source artifact | Information actually reported | Independent ordinary role | Remaining possible work |
|---|---|---|---|
| `LetterCode_001/002/003` | Three 5×5 column-first Polybius fragments spell the E. E. Cummings poem title | A deliberately encoded original-game literary reference; decoded since 2016 | Verify first fragment's placement/absence before reusing poem as a later key |
| `BoardText_#292` | `ENTER CODE SEQUENCE`, other smaller text disputed | Known 14-orb board and secret-bunker sequence | Source-code check for *another* input beyond the existing solved lever |
| `SecretMap_#916` | Extracted graphic apparently resembles the hidden-orb billboard/map | Possible existing secret-orb map | **Highest-value visual asset** to recover unchanged and overlay against 14 known orb positions; unexplained marks after accounting for orbs would be meaningful |
| `Sign_SecretMorse_#944` | Source decoded by players as `GLADBLAD` | Potential creator-domain or personal easter egg; July 2016 solvers already noticed `tobbermix.gladblad.dk` associated by them with a Playdead artist | Independently verify actual artist relationship and exact source glyphs; avoid treating a signature as a narrative answer |
| `letters_#838` | `Fordsjh Gjfhdfdjfhd Ujhdfr B02` | The **same text** appears on a laboratory window, sonic shield, and CEO plaque; plausible shared prop/label texture | First confirm all locations use the *same texture*, rather than counting them as three independent ciphers; retrieve exact pixels and image orientation |
| `SIGN_GirlLab_A_#935` and `COOKIE_Custom_forGirlInWindow_01_#368` | `Rorschach Desgn Noah x200564` | Both are representations of the **same** lab wording (glass and projected/shadow form) | Establish exact lettering and whether ordinary rendering explains the mirror/inversion; no independent second plaintext |
| `OTHER_TrainLetters_#888` | `A10N7`, with `L08` separately seen on an overturned train | Transport/sector labels, plausibly production set dressing | Audit full label set and standard signage before inventing arbitrary coordinates |
| `FX_ScreenKaypro_#742` | In-game older-computer display art with no recovered canonical content in this pass | Functional/decorative computer UI | **Second-best source-image candidate**; match exact monitor source/scene and identify *native registration*, not similarity alone |
| `MORSE_text` and `MORSE_space` | 2016 game/trailer lines with space texture reported as blank paper | Probably existing printer-code presentation apparatus; relation to `Sign_SecretMorse` **not established** | Recover both files and scene usage; do not mistake two `MORSE`-named textures for separate unseen puzzles without proof |
| Repeated orb/tape/radio tune | Known three-direction 14-command password, repeated at several orbs | Already decoded and functionally consumed by 2016 bunker lever | Only re-open with independently identified **new** game handler or distinct cue |

One negative finding matters more than any count: at least two supposed clusters of encoded textual evidence are **source-duplicate content**. The `Rorschach` pair are different renderings of the same text, while the Ford wording is reportedly reused across three distant props. This must not be treated as five independent clues validating a cross-game cipher.

### Specific under-explored endgame possibility: an artist signature

The 2016 `Sign_SecretMorse` example demonstrates that an enigmatic source asset can turn into a readable, externally pointed word without connecting to INSIDE's fiction at all. The contemporaneous discussion links `GLADBLAD` to a purported Playdead artist's web domain. The attribution was **a solver observation**, not independently verified developer confirmation.

This raises the serious *alternative outcome class* that a CE sticker answer could be a creator signature, portfolio artifact, hidden dedication, thank-you, or production story. That is consistent with a distinctive physical collector's product, and it avoids assuming every puzzle reveals the Huddle's secret origin. It remains **speculative** until the stickers or an author-supplied key points there. Do not infer the CE code spells `GLADBLAD`.

### Why visual candidate `SecretMap` has the most useful falsification test

Rather than guess words for the Ford inscription, first recover the exact `SecretMap` texture from a legally obtained retail Unity bundle or preserved 2016 extraction. It has a **natural interpretation** (map of secrets), a definite **existing target set** (fourteen collectibles/orbs), and an independently plausible **null model** (all marks represent already-known secrets, leaving zero unexplained residual marks).

Source-first protocol:

1. Preserve raw asset bytes, Unity version, full asset path/name, texture dimension and digest.
2. Restore the original texture display/orientation using container metadata and scene mesh UV coordinates where possible; record every transform.
3. Count and register only visually distinguishable marks **before looking at the CE sticker master**.
4. Compare registered marks to the already identified secret-orb positions; log matched, extra, and uncertain marks.
5. An **independently anchored, reproducible unexplained sublayer** could become a genuine external indexing surface. If all marks map to known orbs, retire `SecretMap` as an unused CE consumer.

The key assumption is that “map” is not merely a visual/mesh rendering artefact. Chinese-language commentary already proposed it might be a warped 3D export; no screenshot is sufficient to settle this.

## 3. Quantitative source-first cover control

The prior conversation supplied an 18 MB `inside-cover-source-audit.zip`, containing previously generated 2200×1692 overviews of the A and B cover sides. These are **derived** and resized from the original high-resolution scans, not untouched 6552×5040 evidence.

A reproducible test `scripts/audit_inside_cover_monitor_census.py` takes that **supplied ZIP as argument** and examines one manually bounded monitor region. Orange/display cores are separated by their red-versus-green/blue contrast, with 5×5 closing and connected-component area filtering. The exact region, threshold list, output rectangle coordinates and negatives are frozen in `data/original-cover-four-monitor-control-2026-10-08.json`.

Across **eight threshold combinations**:
- A clue-facing artwork: **four** discrete orange luminous monitor panels.
- B outward-facing artwork: **zero** components in the identical spatial window.

Nominal detected orange-core bounding rectangles in 2200×1692 source-preview coordinates:

| x | y | width | height | orange area |
|---:|---:|---:|---:|---:|
| 379 | 988 | 32 | 28 | 787 |
| 753 | 972 | 35 | 26 | 694 |
| 1166 | 1021 | 40 | 27 | 703 |
| 1276 | 1106 | 49 | 40 | 1732 |

**Interpretation:** the previously described *four*-monitor topology is real and stable in the scanned artwork, unlike an invented nine-monitor grid. The test **does not** imply that four screens mean the four Terminal41 schemes: two direct lexical matches (planet/life) and less direct graph/login associations do not supply a shared functional key. Source-first monitor-to-asset registration remains open and must account for scale/perspective.

Selection-bias caveat: the ROI was set *after viewing the image*. Robustness thresholds show measurement stability, **not surprise under an independent image null**, proof of authorial design, or an achieved sticker decode. The opposite cover side is a presentation negative control, not a semantic null for four monitored outputs.

Actual local assertion run returned eight out of eight passing threshold scenarios with all four expected A components and zero B counterparts. No other arbitrary layout or OCR search was performed.

## 4. Candidate hypotheses that survive original-asset screening

**Keep alive, highest information gain:**

1. A **new, CE-specific directive** for some existing image/status asset, especially the known `534brn...` page already reached by the nine background tiles. This is still the only direct demonstrated sticker→external-object edge.
2. A **retrospective key for one specifically located original-game asset** if source inspection exposes a native geometry not explained by known orb/map/other game mechanics. `SecretMap` has a strong immediate null and `FX_ScreenKaypro` has a plausible cover-monitor match.
3. A **physical-production or creator/meta easter egg** that communicates an answer about authorship or a making-of event, not lore. The old `GLADBLAD` case provides a precedent for non-narrative output, but no CE linkage.
4. A **continuation into existing ARG media**, with the compact foreground serving as an index/operation, not a raw high-resolution media file.

**Actively disfavoured on present evidence:**

- Multiplying repeated Ford/shadow labels into several independent ciphertexts.
- Treating exporter `#NNN` IDs as intentional numeric cipher inputs.
- Treating audio cues for the already-solved bunker code or the ordinary status billboard as evidence of new CE code entry.
- Using four cover monitors, nine poster figures, or the arbitrary number 12:12 as sufficient registration to project the full CE master.
- Free scanning all interesting old-text strings for lucky sticker English fragments.

## 5. Highest-value next checks, in order

1. Obtain a **version-pinned original game resource archive** (asset list, not a guessed decoder) and hash/inspect only `SecretMap`, `FX_ScreenKaypro`, `BoardText`, `MORSE_text`/`MORSE_space`, `LetterCode_001`, and repeated `letters` labels. Confirm scene uses and whether any genuinely extra coordinates remain.
2. Recover **exact source bytes** for the high-resolution A/B cover scans so monitor homography is feasible; align independently identified existing source graphics. Only after a shared transform appears may sticker registration be tested.
3. Independently audit the artist-domain connection for `GLADBLAD` to calibrate how often original INSIDE encoded props point to meta-level acknowledgments rather than the game's fictional system.
4. Compare dated 2016 extraction variants (including Chinese .dds exporter IDs) against the same retail build to remove false numeric connections and provenance confusion.
5. Stop original-asset sticker hunting if no independently addressable source property survives its existing-game explanation. Shift back to CE-native physical structure and its **verified** Terminal41 background destination.

### Reproducibility and source restrictions

- This asset catalogue is a **primary-forum-source index**, not a completed Unity asset dump. No full `Assembly-CSharp` or original binary asset textures are in this branch.
- The image census runs locally with Python + OpenCV + NumPy and accepts the previously supplied ZIP; it need not modify/rehost third-party photograph bytes.
- Historical 2016 sources:
  - https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2
  - https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=2
  - https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=6
  - https://www.3dmgame.com/gl/3577786.html
  - https://www.trueachievements.com/forum/viewthread.aspx?tid=814124
  - https://inside.fandom.com/wiki/CEO
  - https://inside.fandom.com/wiki/The_Pulse
- Manufacturer/user evidence for cover and poster: `docs/cover-cross-edition-dependency-audit-2026-10-08.md` on main; original independent sources cited there.

No sticker was completed or promoted, no owner contacted, no active PR modified. The recommendation is about **which external item can be tested without creating a target from the stickers themselves**.

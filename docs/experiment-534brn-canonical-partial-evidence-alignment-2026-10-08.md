> **CL09 source correction (8 October 2026):** The original upstream A capture, `ce55c03ee972954f6e80f55a1a279bb85024f99b`, is now preserved **byte-identically** as [`A-original-capture.bin`](../archive/external/terminal41-534brn/A-original-capture.bin) (12,140 bytes). The previously used 12,150-byte connector rendition remains for reproducibility of the older frozen fixture. With the **same** heuristic alignment and unchanged B/P inputs, true A yields **245** candidate fills instead of **238**: 9 gained / 2 lost offsets, 13 changed normalized B positions, 10 conflicts unchanged. The source-authenticated result is in [CL09 original A delta](../data/534brn-original-a-delta-2026-10-08.json), replayed by [the new audit](../scripts/audit_534brn_original_a_comparison.py). **Neither 238 nor 245 is a uniquely recovered JPEG-byte count**: previous tie-breaking ambiguity remains. This report below is the prior rendition-based experiment, preserved to avoid silently rewriting its fixed result.

# Damaged 534brn page: canonical constraints and archival correction (8 October 2026)

**Research purpose:** preserve independent source evidence and enumerate which bytes are genuinely observed, rather than invent a visually plausible JPEG. The canonical token mask is `data/534brn-canonical-partial-evidence-2026-10-08.json`. This is **not** a working JPEG and must not be opened as if one were repaired.

## 1. Exact sources, and a new acquisition-integrity issue

Three genuinely distinct historical capture families A/B/P survive as described in Experiments 316 and 337, plus the independent XMP metadata fragment. This branch now retains the small samples:

| Source | Upstream original Git blob SHA | Local archive | Integrity |
|---|---|---|---|
| A: older question-mark HTML | `ce55c03ee972954f6e80f55a1a279bb85024f99b` (original **12,140 bytes**) | `archive/external/terminal41-534brn/A-connector-rendition-not-original.bin` | **Not byte-identical**: 12,150-byte tool rendition, SHA `f9cdbd18bbd8713adee89ad93a3551b6310fd7ba` |
| B: replacement-character HTML | `f12c02c49f4c3f7589419fe8e20d655f7b95a9f4` | `archive/external/terminal41-534brn/B-original-capture.bin` | **Byte-exact**, SHA matches |
| P: partial JPEG-like text | `9580913d043ca3efd54a01a38a9cff5767ea8ee7` | `archive/external/terminal41-534brn/P-partial-capture.bin` | **Byte-exact**, SHA matches |
| X: XMP metadata | `b6f5ffed946d9d19dfd0a5d90a8b18759a90c496` | `archive/external/terminal41-534brn/X-xmp-fragment.bin` | **Byte-exact**, SHA matches |

All four are originally hosted at [gamesbyian/playdead-unofficial-exports](https://github.com/gamesbyian/playdead-unofficial-exports/tree/master/assets), pinned by their Git blob identities. Tool-based base64 transfer was checked by making a fresh Git blob and comparing SHA; **A fails equality** despite displaying its original SHA in metadata, while B, P and X pass.

This means Experiment 337's source identity claim must be narrowed: the connector's 12,150-byte A rendition reproduces its reported token counts, but it has **not** been proved byte-identical to the 12,140-byte original. Its differences may be localized or consequential; the bit-for-bit upstream A bytes must be obtained in a runtime that does not transform them.

Do not disguise A as the original or overwrite its source SHA. The different filenames in the archive resolving to the *same* original A blob also produced the same changed rendition through this connector.

## 2. Reproducible canonical partial-token representation

The new `data/534brn-canonical-partial-evidence-2026-10-08.json` stores one positional stream of **12,052 normalized tokens**, from B's first `JFIF` through the end of `pe^!02un`, inclusive.

- `hex_pairs_64_per_line`: a pair of hexadecimal digits for known/candidate bytes, `??` for unknown tokens;
- `source_flags_64_per_line`: **B** (known in B), **A** (A-only candidate), **P** (P-only candidate), **D** (same A/P candidate), **C** (A/P conflict, unknown), **U** (unknown across sources);
- `conflicts`: alternative values at ten disagreement sites;
- `recovered_sites`: all 238 candidate fills with source and normalized B-relative location.

The baseline fixed-alignment counts:

| Status | Count |
|---|---:|
| B original known | **10,057** |
| A only | **149** |
| P only | **10** |
| A and P agree | **79** |
| Unknown | **1,747** |
| A/P disagreement (kept unknown) | **10** |
| **Total** | **12,052** |

B originally has **1,995** unknown tokens; the selected alignment fills **238**, leaving **1,757** unknown including ten contested. These are *token positions in the normalized corrupted capture*, not 12,052 guaranteed original JPEG byte offsets. The first token is `JFIF`, **not** a JPEG SOI marker. HTML wrapper, zero/space and original-high-byte damage prevent interpreting the entire stream as a directly decodable JPEG.

`scripts/rebuild_534brn_partial_evidence.py` checks the four pinned sources' Git object SHA, repeats the original 12-byte anchor/edit alignment *offline*, recomputes all tokens and flags, compares every byte/status to the frozen artifact, and fails on drift.

## 3. Important falsification: alignment ambiguity affects nearly all recovered values

Experiment 337's original wording **“238 exact B-unknown byte positions”** and **“hard lower bound”** was too strong as a model-independent conclusion. Its dynamic programming selects one cheapest path through unknown-heavy areas; no uniqueness of positional alignment was demonstrated.

New adversarial evaluation reused the same source-normalization, unique known-anchor rule, edit costs (unknown can match for zero; known mismatch costs three; insertion/deletion cost one), and start/end markers. Only tie-breaking convention or anchor length varied.

| Frozen variant | Candidate recoveries | A/P conflicts |
|---|---:|---:|
| 12-byte anchors, prefer diagonal in equal-score path | 238 | 10 |
| 12-byte anchors, prefer upward move when tied | 265 | 10 |
| 12-byte anchors, prefer leftward move when tied | 265 | 31 |
| 10-byte anchors, diagonal tie rule | 238 | 10 |
| 14-byte anchors, diagonal tie rule | 238 | 10 |

Among 238 baseline fills, **18 retain identical position and value across all five**, while **220 vary or disappear** under at least one legitimate equal-score tie-breaking alternative. Original 10- and 14-byte anchor choices alone leave all 238 unchanged, but anchor robustness **does not establish edit-path uniqueness**.

The full result, method details and samples live in `data/534brn-alignment-sensitivity-2026-10-08.json`. The companion `scripts/audit_534brn_alignment_sensitivity.py` reproduces the five exact runs from the locally preserved files without network. Its assertions validate the numeric results, and it emits the complete list of 18 five-way-consistent candidate values. Being five-way-consistent is **not** proof of unique correctness across *all* optimal alignments.

This is a substantive revision, not mere cautionary language. **Treat the 238 aligned positions as candidates until a unique optimum proof, independent header/parser alignment or fresh uncorrupted source resolves the ambiguity.** The 10 values simultaneously contested by A and P remain explicitly unknown under the baseline.

## 4. Historical visualization and byte-source inventory

GitHub's original 2,725-file research export includes files named as if all were JPEG recovery. Distinguish them by blob identity and inspected actual content:

| Archived artifact | Identity / measured fact | What it is *not* |
|---|---|---|
| `assets/534brn9653f9j8mmd-985ba09db545de5d.png` (aliases `StickerSolution-*.png`) | Exact identical 767,381-byte Git blob `2d9fd5...`, valid **1032×1250 PNG**. It **visibly shows the CE nine-background-tile solution**, labelled A–I with the already-known Terminal41 address. | **Not an intact reconstruction of the damaged page.** Filename coincidence is misleading. |
| `assets/534brn9653f9j8mmd-1d6905b88dafcb0e.bmp` and `...ec9713cd42aff3d5.jpg` and another `_1-...jpg` | Identical blob SHA `21649d...`, recorded **3,963,914 bytes** under three extensions. Connector did not return bytes, so true file signature/dimensions are unknown. | Three filenames **do not** imply three independent copies or valid BMP/JPEG streams. |
| `assets/bmp_raw-9319ae5383d5f216.png` | Actual **42×42 PNG**, blob `9315424...`. | Not a direct damaged JPEG original; derivation/source relation unproven. |
| `assets/bmp_raw.v3-9332c9797250a2ab.png` | Actual **423×423 PNG**, blob `296c6f...`, enlarged/composited image with contrast and bright green/black markings. | Not native recovered dimensions; the 423×423 displayed pixel geometry is derivative. |
| `assets/image_data_orig-c7c6d38639f4c541.bmp`, `image_data_fixed-839bf39f5488e91f.bmp` | Real **42×42 BMP** byte signatures; first recurs under `image-6cc...` and `test1-...`; second is a variant. | Distinct derivative experiments, not independent JPEG high-byte captures. |
| `assets/blue_difference-f51ef2a3e8c25c2f.bmp` | Actual **42×42 PNG**, despite `.bmp` extension. | Extension alone cannot classify the input. |
| `assets/4_bmp-fc9ec34700f13a85.txt` | ASCII-space-mangled BMP-like header, invalid ordinary width if interpreted as binary without restoration. | Not a clean BMP by virtue of the `BM` magic alone. |
| `assets/4_bmp_fixed-13d4968f30bf9a6a.txt` | Actual 42×42 BMP signature despite `.txt` extension. | Likely one attempted repair/format conversion, not the original JPEG. |

The 42×42 derivatives may relate to separate `saf_dat_col` BMP investigations; no exact source-byte lineage to `534brn` JPEG has been proven. Therefore **do not use their visual motifs, counts or dimensions as if they constrain the damaged JPEG's original pixels.**

Previously documented structural limits remain: the `128 UNSOLVED` footer is a separate source-native possible dimensional clue, each SOF dimension's low byte remains unknown in 128..255, and Experiment 423 shows *all 43* geometric MCU-count possibilities survive the entropy constraints. No extra JPEG pixels are inferred in this pass.

## 5. Follow-up with highest information gain

1. **Recover byte-exact A original** through an actual Git protocol checkout or unmodified Git blobs API. Compare against the presently vendored 12,150-byte adapter rendition. If differences are outside the payload, freeze and prove that; do not assume it.
2. **Enumerate possible values over all optimal alignment paths**, at least within uncertain/high-overlap short gaps, instead of selecting a path by editorial preference. Some source-compatible recoveries may be invariant even where offsets move, but the current five-way 18 count is only a conservative subset of tested paths, not a proof bound.
3. **Provenance-audit the three-extension ~3.96MB derivative** by retrieving raw file signature and identifying the original producing tool, so it can be placed in the right lineage class. Do not promote it to raw capture on filename.
4. Seek truly independent historical captures, media fragments or source byte fields. More re-exports of the same A/B/P blob families contribute zero new information.
5. Test author-supplied geometry or image-registration clues only after byte evidence is stable, rather than choosing JPEG replacement bytes based on a recognizable picture.

No missing sticker symbols, JPEG entropy bytes or dimensions were guessed. Original raw physical sticker data unchanged.

# CL-12: external SAF DEFLATE workbench is a reproducible hypothesis generator, not a recovered backup

_8 October 2026. Third-party source audit. No sticker glyphs or speculative missing-symbol fills used._

## Source located

A separate public project, [burning-lnkr/saf_dat_col](https://github.com/burning-lnkr/saf_dat_col), was published on 25 September 2026. Inspected fixed revision: [`cdb41453d0c2a61d09dcf341adb7e30762c7c2a6`](https://github.com/burning-lnkr/saf_dat_col/tree/cdb41453d0c2a61d09dcf341adb7e30762c7c2a6). The project provides a static-browser byte workbench, deterministic Python build instructions, JavaScript codecs, archived repair recipes, 17 recorded candidate payloads and internal tests. Its source-control tree includes `README.md`, `data/index.json`, `tests/validation.json`, `js/codec.js`, `js/render.js`, `js/worker.js` and `tools/build_standalone.py`.

**Most significant provenance finding:** The `data/saf_dat_col.utf8.bin` input is **exactly the same original April 14, 2019 capture** already in our own repository: 1,986,163 bytes, Git blob SHA-1 `349b818fce618ef55c404bedfb602b1d03f29a48` and SHA-256 `53cd286fce00071b7a9b75ddbcec2f285d2e893718fc1226d5cea35fa4a6cd6c`. The alternative `data/community.bin` (1,249,229 bytes) is attributed by its author to a later extracted community-edited/fixed text file, not the screenshot-attested but missing `saf_dat_col_BACKUP.html`.

This project supplies **new computational methods and conditional outputs**, but **no demonstrably new original server payload bytes**. This matters after [CL-11](2026-10-08-saf-dat-col-archival-duplicates.md) showed the other contemporary text presentation was an information-deleting derivative and a 2023 site ZIP was byte-identical with already archived pages.

## What can be independently verified from the public repo

The bundled candidate index advertises **10 candidates from the original capture** and **7 from the community-derived input**, with output lengths around 11.7 MB. The default `original_combined` candidate has **11,779,416** resulting bytes and fixed SHA-256 `14bbfcec0f7d5a343c0fbd26b548e63ecc93d60db8a730573ca93231249c5b0a`. The browser can visualize the assumed output as 5,000-pixel rows of 15,001 bytes with three interleaved sample components and a one-byte row prefix, mapping magnitudes 7 and 4 into grayscale intensities.

The repository records self-consistency tests in `tests/validation.json`, including independently inflated streams with standard zlib and hashes of source-derived output images. I inspected **the authored README, index and test results**; I did **not** independently execute its 17 stream-reconstruction tests during this pass.

Crucial boundaries stated by the source project itself:

- LZ77 historical dictionary contents are not known. Some reconstruction paths substitute zero history or other models.
- Several DEFLATE block terminators are **synthetic**.
- Invalid/incomplete headers, ambiguities over missing CR and spaces/NUL, and copy-history alternatives yield multiple distinct possible streams.
- Width, row stride, channel interpretation, grayscale magnitude mapping, repetition and postfilter choices are **rendering assumptions** rather than source-authored raster metadata.
- Matching a candidate's fixed output SHA-256 or producing a valid PNG proves a recipe is reproducible, **not that this was Playdead's authored image**.

Thus 17 candidate payloads are not 17 independent source captures; nor is a valid DEFLATE stream by itself an intended sticker-foreground receiving artifact.

## What this contributes to our research

This third-party workbench has a reproducible **source-position / literal-versus-copy lineage viewer**, explicit ambiguity-bit probes and multiple fixed conditional decompressions. Those are genuinely useful analytical *tools*. They may let us separate **invariant source-literal bytes** from history-filled content, and test whether an apparent output feature persists under a predeclared family of repair assumptions rather than being created by a convenient history seed.

There is one worthwhile bounded future experiment:

1. Freeze the *existing* 17 candidate list and its published provenance flags, without modifying any missing source bytes to create a desired image.
2. Project outputs into **source-literal versus copy-dependent** positions and record stable byte/string/structural features across the original-source candidates only. Keep separately classified community-derived branches.
3. Require any proposed feature to survive the same predeclared set of alternate repairs; report denominators and alternative explanations.
4. Compare any surviving *source-stable instruction* with the direct physical CE `534brn` route **only if a textual consumer or typed operation is independently established**.

This is an opportunity to **test robustness**, not a claim the workbench reveals the missing 2019 backup or a CE sticker decoder. Importing its rendering parameters and iteratively moving them until a recognizable picture emerges would merely repeat unlicensed visual fitting.

The repo source itself is external software with an MIT-licensed implementation; its bundled historical image/source inputs have their own provenance and rights. We link rather than vendoring duplicate 2 MB assets or copying third-party decoder code without a practical integration need.

## Classification

**Source authenticity:** original SAF input matches our existing byte-pinned record.

**Historical independence:** no newly attested `saf_dat_col_BACKUP.html` or other separate original server response.

**New capability:** rigorous, inspectable stream-reconstruction **hypothesis tooling** with documented data lineage and internally reproducible 17-variant candidate set.

**CE receiver:** no direct evidence the physical slash/dash/dot stickers address this compressed stream.

See the frozen [CL-12 machine-readable source audit](../../data/conjecture-lab-saf-external-workbench-audit-2026-10-08.json). The missing-backup acquisition remains the higher-confidence source recovery path.

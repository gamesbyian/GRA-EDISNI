# CL-11: do alternative saf_dat_col captures preserve the missing backup or extra original bytes?

_8 October 2026 | historical primary-source comparison | no sticker-symbol inference_

## Two contemporaneous 2019 source files, compared byte-authentically

The [original April 2019 Playdead Discord conversation](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/Playdead%20Unofficial%20-%20ARG%20-%20solving%20%5B461275582970462209%5D.txt) carries two substantial text attachments both referring to `terminal41.link/dat/saf_dat_col.html`:

| Contemporary capture | Original Discord local timestamp | Source Git blob SHA-1 | Source bytes / storage |
|---|---|---|---|
| `saf_dat_col-fd944ab391ff5415.txt` | **14 April 2019 13:13** | `349b818fce618ef55c404bedfb602b1d03f29a48` | **1,986,163**, valid UTF-8 with BOM; uploader explicitly said obtained by **curl** |
| `INSIDE_saf_dat_col-40304e7acab3c363.txt` | **16 April 2019 17:24** | `6ca8c90711a54944850fdaf94a0ead1fab887686` | **2,053,806**, valid **UTF-16 LE** with BOM; posted as saved/copied page text |

The April 14 original is already preserved byte-for-byte in this repo as `archive/external/twinysam-inside-arg/terminal41.link/dat/saf_dat_col.html`. The April 16 file was genuinely attached by a historical participant before the CE sticker puzzle but is **not** the independently screenshot-documented `saf_dat_col_BACKUP.html`.

A larger encoded file does not necessarily preserve more information. Exact Unicode decoding shows **1,265,969 characters** in the April 14 source and **1,026,902 characters** in the April 16 source. Both contain **precisely 1,900 U+FFFD replacement characters**.

### The decisive within-damage comparison

Split each decoded text at every U+FFFD replacement mark, and within each resulting segment remove Unicode whitespace, without changing any remaining Unicode characters or their order. The two sources each yield exactly **1,901** corresponding segments.

- **1,896 / 1,901 segments are exactly identical** after this normalization.
- In **all 1,901 / 1,901 segments**, every remaining April 16 character appears **in the same relative order** within the corresponding April 14 segment. This was tested via deterministic monotone subsequence matching, not visual spot inspection.
- The only five differing segment numbers are **0, 1149, 1209, 1240, 1252**. The second copy removes, respectively, **274 / 27 / 142,681 / 264 / 84,540** non-whitespace characters, while preserving the order of everything retained.

The differences include the original HTML wrapper (`<!DOCTYPE html>` etc.), an internal closing-HTML-tag area and several large sections where a browser's interpretation/copy path evidently omitted characters. There is **no additional non-whitespace code-point stream** in the April 16 file relative to its paired earlier segments. The 1,900 replacement-mark boundaries and their order are the same.

**Result:** the UTF-16 attachment is a **lossier presentation of the same already available corrupted content**, not an independent different set of still-readable original bytes. This is a source-character lineage statement, **not** a proof that each server response, whitespace character, or original byte sequence was identical. It specifically does not license restoration of the 1,900 replaced values or treatment of the April 16 copy as the missing backup.

If future evidence shows that a whitespace-only change encodes a genuine separate source field, that is outside this deliberately conservative non-whitespace test. No such field is currently documented.

## January 2023 complete website ZIP: direct all-file comparison

At **1:59 a.m. on 25 January 2023**, a Discord researcher uploaded `terminal41-1d9539e0649bc7c8.zip`, describing it as the collected Terminal41 website pages found **mostly through the Internet Archive** and explicitly omitting the 19MB gate-98 PNG due to Discord's 8MB attachment limit. This is a substantial piece of legitimate third-party source archaeology worth testing against our later 74-file mirror.

Original ZIP SHA-1 (Git blob) `4f8958bd45a0e8874483b33e46e56a6a3b37a2f1`, **1,605,024 bytes**. We decompressed and enumerated **all 71 regular files**, then compared their actual payload bytes to files under `archive/external/twinysam-inside-arg/terminal41.link/`.

| Metric | Verified |
| --- | ---: |
| ZIP regular files | **71** |
| ZIP uncompressed content bytes | 2,087,894 |
| Present in existing repo mirror | **71** |
| Exact byte-identical contents to mirror | **71** |
| Nonidentical payload or unique path | **0** |
| Explicit `BACKUP` filename in ZIP | **0** |

The 2023 archive is a valuable corroboration of **historical preservation fidelity**, not an alternate collection of missing routes or backup payloads. Its 71 HTML/text sources are **fully represented in the current mirror**; neither it nor the 2019 UTF-16 presentation gives us the original `saf_dat_col_BACKUP.html` bytes.

## Important mislabeled-attachment trap in April 2020

Two files whose filenames look like saved HTML copies of `breach_contribution_reg` and `...BACKUP` are **actually PNG image data**, not HTML source bytes. The two original files posted around **15:38 on 21 April 2020** were:

- `assets/Terminal41.link-day-breach_contribution_re-d8f992b8122788b4.html`, Git blob `0f0c805f03b59b4fa1140217e7b5990496ec560e`;
- `assets/Terminal41.link-day-breach_contribution_re-9621e434e1914143.html`, Git blob `6a2ee6f76c0953167760bff98acd5d9ac38b5160`.

Despite their `.html` suffixes, both begin with the **PNG signature** `89 50 4e 47 0d 0a 1a 0a`. The original conversation calls them images: an investigator subsequently says the attached files were actually PNGs and compared the different screenshot frame sizes. The images can document rendered page status, but cannot be treated as uncorrupted **raw backup HTML**. CL-09 already preserves a related comparison screenshot in the repo.

## Reproduce independently

[Machine-readable ledger](../../data/conjecture-lab-saf-dat-col-original-captures-2026-10-08.json) freezes the original upstream Git blob identities, exact Unicode normalization rule, full 1,901-segment census results, archive ZIP 71/71 status, and the April 2020 screenshot-artifact classification.

[Reproducer](../../scripts/audit_saf_dat_col_capture_lineage.py) uses only the Python standard library. Its no-argument form verifies the small fixture against the already committed original April 14 copy; its full forensic mode accepts original byte-authenticated April 16 and January 2023 downloads:

```bash
python scripts/audit_saf_dat_col_capture_lineage.py
python scripts/audit_saf_dat_col_capture_lineage.py \
  --apr16 /path/to/INSIDE_saf_dat_col-40304e7acab3c363.txt \
  --jan2023zip /path/to/terminal41-1d9539e0649bc7c8.zip
```

Original files remain [available in the source archive](https://github.com/gamesbyian/playdead-unofficial-exports/tree/master/assets). The research process fetched and byte-verified them in [GitHub Actions CL-11 source replay](https://github.com/gamesbyian/GRA-EDISNI/pull/173) without permanently adding more than 5MB of duplicate binary data to the repository. The one-shot fetch workflow is removed before merging; the source IDs, fixture and replay persist.

## Implication for foreground research

The nine CE sticker backgrounds physically direct to `dat/534brn9653f9j8mmd`, but neither historical `saf_dat_col` capture nor the 2023 ZIP supplies the missing **typed instruction** for consuming foreground dot/dash/slash marks. A false backup lead has been carefully closed, not decoded.

**Next:** seek the actual **screenshot-attested `saf_dat_col_BACKUP.html`** contents or a genuinely distinct archived response. Unlike copying previous variants of the same 1,900 U+FFFD corruption events, that acquisition could add independent evidence. Investigate original Apache backups, foreign web archives, contemporary saved browser caches or old disk snapshots, while remaining strict about source byte hashes, provenance and date.

**CL-11 conclusion:** two large apparent alternative sources add **zero demonstrated missing non-whitespace codepoints or Terminal41 pages**, because one is an information-deleting text rendering and the other is a perfect copy of existing archival material. The unresolved original backup remains a legitimate, independently evidenced missing source, not a newly decoded sticker artifact.

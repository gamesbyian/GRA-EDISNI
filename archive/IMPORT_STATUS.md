# Archive import status

Last audited: 2026-09-28 (America/Edmonton)

This file records the migration of INSIDE Collector's Edition sticker-cipher artifacts from the project's Google Drive folder and available ChatGPT Project/Library files into this repository.

## Google Drive project folder

Source folder ID: `11eQEkw6qYlESO9RY5kp3Tz3dnctrD1YW`

The folder currently contains 10 files plus the nested `INSIDE Sticker Cipher Research Files` folder. All 10 top-level files have been copied into `archive/drive/`:

- the three canonical Google Docs, exported as DOCX
- Unknown Sticker Lead Ledger, exported as DOCX
- CT/X-ray Candidate Contacts, exported as DOCX
- Unaccounted Sticker Hunt, exported as DOCX
- TEMP INSIDE image recovery, exported as DOCX
- final mystery presentation PPTX
- verification workbook XLSX
- supplementary evidence CSV

## Research-files folder

Source folder ID: `17M62PsS0LtSpEBljmjlSHtwLgSF6bNsq`

The Drive folder currently exposes 134 file entries. Some entries are duplicate uploads with the same filename/content. The repo archives unique payloads by filename under `archive/research-files/`.

At this audit, all 127 unique research filenames exposed by Drive are present in the repo, including the two large ZIP bundles that initially exceeded the direct connector transfer path.

The two oversized ZIPs were imported byte-for-byte through a one-shot GitHub Actions handoff using temporary authenticated Drive download references, with exact byte-size checks before commit:

1. `h108_marked_printer_stage1_artifacts.zip`
   - Drive file ID: `1xoQMWQy3POvLv1H4kJzC772g0EVkBuef`
   - size: 11,617,658 bytes
   - repo path: `archive/research-files/h108_marked_printer_stage1_artifacts.zip`

2. `INSIDE_Sticker_Cipher_Research_Artifacts.zip`
   - Drive file ID: `1WZ0JunCvFU0wxTNSIoMNVLopMp29D_j_`
   - size: 21,053,771 bytes
   - repo path: `archive/research-files/INSIDE_Sticker_Cipher_Research_Artifacts.zip`

The temporary import workflow was removed after the successful transfer.

Duplicate Drive entries with the same filename are intentionally not duplicated in Git; the goal is preservation of unique artifacts, not preservation of redundant Drive upload objects.

## ChatGPT Project / Library artifacts

The current project surface exposed three additional INSIDE-specific files that were not part of the Drive folder and were not already represented by filename:

- `archive/project-files/sealed-ce-nondestructive-imaging-leads.md`
- `archive/project-files/inside-arg-discussion-post.md`
- `archive/project-files/inside_tile_seam_metrics.csv`

A Library copy of `INSIDE_Sticker_Mystery_Supplementary_Evidence.csv` was also found, but it was already archived from the Drive folder. `c_class_source_inventory_v2.csv` was already present in `archive/research-files/`.

Generic Library search hits such as unrelated `index.html` and JSON files were not imported merely because their indexed text contained the word "inside"; only artifacts clearly tied to this investigation were migrated.

## Migration policy

- Preserve original binary formats when practical.
- Export native Google Docs as DOCX for archival fidelity.
- Preserve research CSV/PNG/TXT artifacts verbatim.
- Avoid redundant duplicate uploads when filename/content is already represented.
- Record any connector-limited omissions here.

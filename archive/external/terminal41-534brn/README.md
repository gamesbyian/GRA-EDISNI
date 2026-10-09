# Terminal 41 `534brn9653f9j8mmd` damaged-page capture preservation

This directory contains only **source captures and a consciously non-byte-identical rendition** needed to regenerate the evidence mask.

The known original Git blobs are in [gamesbyian/playdead-unofficial-exports](https://github.com/gamesbyian/playdead-unofficial-exports/tree/master/assets), at source snapshot `5e5897e2ce70dad5a2bd85e459770637cb36610f` (their SHA identities are content-addressed and reproducible).

| File | Size | Git SHA of file committed here | Original SHA | Original-byte fidelity |
| --- | ---: | --- | --- | --- |
| `A-original-capture.bin` | **12,140** | **`ce55c03ee972954f6e80f55a1a279bb85024f99b`** | same | **YES**, true raw archived and Git-SHA checked (CL09) |
| `A-connector-rendition-not-original.bin` | 12,150 | `f9cdbd18bbd8713adee89ad93a3551b6310fd7ba` | `ce55c03ee972954f6e80f55a1a279bb85024f99b` (12,140 bytes) | **NO**: tool changed ten bytes of total size; cannot treat as exact original |
| `B-original-capture.bin` | 16,922 | `f12c02c49f4c3f7589419fe8e20d655f7b95a9f4` | same | **YES** |
| `P-partial-capture.bin` | 8,760 | `9580913d043ca3efd54a01a38a9cff5767ea8ee7` | same | **YES** |
| `X-xmp-fragment.bin` | 2,804 | `b6f5ffed946d9d19dfd0a5d90a8b18759a90c496` | same | **YES** |

No file in this directory is a pristine JPEG or a solution. CL09 now preserves the **true exact original A** alongside the previous nonidentical connector rendition. The source Git blob hash was checked both on the GHA original raw bytes and against the resulting repository file. **Do not delete the rendition** until dependent frozen historical analyses are migrated, because the old canonical fixture deliberately used its changed bytes.

This source has historically been copied through HTML and Unicode transformations: neither `?` nor `EF BF BD` should be interpreted as an original JPEG pixel or entropy byte. Details in [canonical partial evidence audit](../../../docs/experiment-534brn-canonical-partial-evidence-alignment-2026-10-08.md).

To reproduce local checks in a full repository checkout, invoke:

```sh
python scripts/rebuild_534brn_partial_evidence.py
python scripts/audit_534brn_alignment_sensitivity.py
python scripts/audit_534brn_original_a_comparison.py
```

The **original A** recomparison yields **245 alignment-supported candidate fills** (nine newly present, two lost, thirteen affected positions). The earlier **238** rendition-based snapshot remains frozen for its original input. The 12,052-token mask, source flags, 238 alignment-supported candidate fills, and explicit conflicts are in `data/534brn-canonical-partial-evidence-2026-10-08.json`. The 5-way sensitivity check finds only 18 candidate values stable under tested variants. The mask **does not produce a valid or complete JPEG**.

Media/source-rights note: these are research copies of archival material attributed to Playdead/its ARG and historical collectors; this archive does not confer a software/artwork reuse license.

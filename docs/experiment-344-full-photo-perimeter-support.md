# Experiment 344 — full-photo physical-perimeter observability audit

_Status: completed and reconciled from the successful PR #81 perimeter workflow, 30 Sep 2026._

## Question

Experiment 325 established that the consensus background-tile masters cannot test a PC-style physical margin/check-bit channel because those masters deliberately crop away the sticker perimeter.

Before searching any perimeter for stable marks, ask the prerequisite question:

> Do the archived original sticker photographs preserve enough of the physical sticker quadrilateral, at sufficient resolution and without source-border clipping, to support a replicated perimeter comparison?

This is an **observability** test only. It does not search for edge symbols, select a margin feature, or score any candidate code.

## Inputs

- the 82 manifest-authorized `community-original` sticker photographs;
- the existing sticker-quadrilateral detector from `scripts/build_background_tile_masters.py`;
- preregistered geometric quality gates from the original PR #81 workflow.

The successful source run was GitHub Actions run `36777513388`, artifact `11127420173`. Its exact summary and per-photo rows are preserved as:

- `data/perimeter-support-exp344-report.json`
- `data/perimeter-support-exp344-photos.csv`

The runnable audit is now preserved on current main lineage as:

- `scripts/audit_full_photo_perimeter_support.py`
- `.github/workflows/audit-sticker-perimeter-support.yml`

## Preregistered usability gates

A detected quadrilateral is accepted only if:

- minimum corner clearance from the source-image border is at least 0.5% of the short image axis;
- minimum detected sticker side is at least 160 px;
- maximum/minimum side ratio is at most 1.35;
- detected quadrilateral area is 12%–98% of the source image.

Uncertain geometry fails closed.

## Result

Across 82 original photographs:

- **35** pass all full-perimeter observability gates;
- **all 9 A-I tile classes** have at least two independently usable photographs;
- every class therefore has replicated physical-perimeter support.

Usable counts by class:

| class | original photos | usable full-perimeter photos |
|---|---:|---:|
| A | 7 | 5 |
| B | 13 | 4 |
| C | 11 | 3 |
| D | 7 | 4 |
| E | 8 | 3 |
| F | 12 | 4 |
| G | 5 | 2 |
| H | 9 | 5 |
| I | 10 | 5 |

The most common failure is source-border risk: the detected sticker touches or crosses the source image boundary, so the physical perimeter cannot safely be treated as observed.

## Interpretation

Experiment 325's observability block is now removed.

The corpus **can** support a replicated, support-aware physical-perimeter feature test for every A-I class. This does not mean that a margin/check-bit channel exists. It means such a test is now empirically licensed without relying on inpainted master pixels or single-photo accidents.

The next R2 test should therefore be narrowly preregistered:

1. rectify only the 35 usable photographs;
2. define perimeter bands before inspecting class-conditioned results;
3. compare repeated photographs of the same A-I class for stable edge-localized features;
4. require cross-photo replication within class before promoting any feature;
5. use between-class controls and image-registration nulls;
6. preserve negative results.

Do not optimize a threshold, edge width, polarity, or feature location because it produces a desired foreground ordering or machine result.

## Provenance / reconciliation note

PR #81 originally called this Experiment 339, but main subsequently assigned Experiment 339 to row-selector null calibration. The perimeter code and successful artifact were therefore reconciled onto current main as Experiment 344 rather than merging the stale numbering conflict directly.

The old branch's unrelated `Verify machine` PR run failed while the dedicated perimeter audit succeeded. The current reconciliation is based on current main and preserves the successful audit outputs explicitly.

## Reproducibility

Locally, with image dependencies installed:

```bash
python scripts/audit_full_photo_perimeter_support.py \
  --json artifacts/perimeter-support/report.json \
  --csv artifacts/perimeter-support/photos.csv
```

The GitHub workflow installs `numpy`, `opencv-python-headless`, and `pillow` and uploads the generated CSV/JSON.

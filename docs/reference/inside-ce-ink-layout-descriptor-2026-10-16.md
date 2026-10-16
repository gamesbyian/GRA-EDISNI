# INSIDE CE: OCR-free printed-layout descriptor, source-first second stage (16 October 2026)

**RESEARCH ONLY. Does not recognize a sticker, symbol, printed number, owner's identity, or solve the ARG.**

## Motivation and lessons from analogous systems

The previous [OpenCV paper geometry pilot](inside-ce-geometric-proposals-external-research-2026-10-16.md) and [SAHI-inspired tiling](inside-ce-sliced-geometry-pilot-2026-10-16.md) can find tiny generic bright-paper shapes, but cannot tell a physical INSIDE sticker from product packaging or a printed shipping ticket. Their 4/4 and 3/4 simulated false visual prompts are warning signs, not proof of acceptable specificity.

Document-analysis literature, including [connected-component text-line detection](https://pubmed.ncbi.nlm.nih.gov/27623582/), [OpenCV scene text components](https://docs.opencv.org/5.0/extra_modules/text_detect.html), and [OpenCV packaging label inspection](https://github.com/gunaprakshkethineni/goods-in-label-ocr), suggests examining *where* dark printed marks appear within a prospective paper object before attempting OCR or general model training. Source claims from other label projects are not transferred as detector accuracy: those projects often rely on deliberately formatted or generated labels.

We know the INSIDE CE paper sticker has a distinctive **large central minimalist black symbol** and **small bottom printed three-digit serial**. That physical format is worth examining, but it is also easy for ordinary numbered tickets and cards to imitate. Thus **ink layout is a descriptive feature, not a verified sticker signal**.

## Implementation

[visual_ink_layout.py](../../scripts/external_evidence/visual_ink_layout.py) is a deterministic, CPU-only, no-model, no-OCR source-constrained analyzer of **already-acquired candidate paper crops**. It normalizes each proposed crop to 192×192 grayscale (preserving orientation) and computes descriptive statistics in fixed normalized zones: upper paper margin, center mark zone, lower print zone and outside-edge band. Metrics include dark-pixel fractions, largest connected component sizes/counts, median paper luminance, a fixed dynamic ink threshold, and Laplacian detail/blur proxy.

No digit is decoded. Neither `central mark` nor `bottom print` is interpreted as evidence of one particular sticker; these are *positions* only. We do not tune a decision threshold or assign a confidence score.

The script consumes the existing candidate index and sliced-paper proposals, verifies the original acquired file SHA256 and safe root, bounds-checks each region in EXIF-oriented source pixels, and attaches a descriptive `ink_layout` to up to eight proposal boxes per photo for no more than 48 photos. Files absent or with changed source digests are explicitly censored. Inputs that falsely claim a sticker is already verified fail closed. It does **not** fetch public media itself.

The manual `CE visual provenance` workflow's explicit `run_sliced_pilot=true` path now generates `sliced-ink-layout-proposals.json`. The offline contact sheet shows numbers like **center dark 0.080; lower dark 0.013**, explicitly *NOT sticker proof*. This is for human-review triage, not an automatic rejection gate.

## Descriptive benchmark, without fitting

[benchmark_ink_layout_exploration.py](../../scripts/external_evidence/benchmark_ink_layout_exploration.py) scores **11 existing SHA-pinned original physical sticker photo regions**, spanning three mutually disjoint original-photo lists:

- Five older source templates: **003, 037, 038, 065, 125**.
- Four independent frontal positives: **039, 047, 063, 118**.
- Two newly introduced tiny-scene source originals: **021, 171**.

It also scores **eight synthetic paper/packaging negatives** at previously recorded shape bounds from the prior scene generators, including numbered tickets, printed bars, a game case and bright mock product art. The benchmark reports raw region features and class-wise *descriptive distributions* (min, median and max) without defining a binary pass/fail classifier or selecting cutoff values.

These original positives have all been inspected during previous methods. The negative paper objects are generated. Consequently **classification accuracy, production false-positive rate and novel camera-photo sticker sensitivity remain unmeasured**. The benchmark is useful for finding whether features are completely nondiscriminative or fragile, not for claiming a recognition system works.

## Reproduction, real-media limitations and next steps

Ordinary PR CI (no web requests):

```bash
python scripts/external_evidence/benchmark_ink_layout_exploration.py \
  --repo-root . --out visual-evidence-work/ink-layout-exploration.json
```

After explicit approved original public-image acquisition via existing manual workflow:

```bash
python scripts/external_evidence/visual_ink_layout.py \
  --candidate-index visual-evidence-work/candidate-index.json \
  --candidate-root evidence-work \
  --proposals visual-evidence-work/sliced-paper-proposals.json \
  --out visual-evidence-work/sliced-ink-layout-proposals.json
```

**Critical next empirical hurdle:** compile independently original, legally accessible images of (a) white cards and product packaging with dark marks and serial-like print and (b) tiny, partly obscured real sticker papers. Pin their original SHA, annotate native-space crop bounds without looking at the classifier and test source-level recall and **false visual prompts per photo**. No image absent from an acquisition report may be called a tested negative.

A useful improvement might be human reviewer ranking based on layout differences, but only after an **entirely new separately frozen** positive/negative set can demonstrate the ranking improves actual novel-source inspection per unit cost. Purely learning from the 11 known stickers and generated negatives would yield a dangerously comfortable model.

**At authoring:** the descriptor and no-network benchmark are in PR; numerical descriptive results must be taken from the exact-head CI output. No new serial or owner found.

## First measured descriptive result, and an annotation confound

[Exact-head CI run 38964862642](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38964862642) passed **158 no-network tests** and generated the full 11-original/8-generated-region descriptor report. Printed zones were **not** used to create a classifier or select a threshold. Median normalized dark-pixel fractions were:

| Zone | 11 genuine old sticker photo crops | 8 simulated unrelated paper/product crops |
|---|---:|---:|
| Center symbol area | **0.115087** | **0.062823** |
| Lower printed-number area | **0.016589** | **0.014833** |
| Top margin | **0.000000** | **0.000000** |
| Outer edge | **0.125456** | **0.000000** |

**The bottom-zone medians are almost indistinguishable.** Lower print density is even **zero in at least one already known genuine sticker**, so a strict "bottom text must be visible" filter would discard actual positives. Center dark density spans 0.002095–0.122985 for originals versus 0–0.263943 for synthetic negatives, with major overlap. No class-separation threshold is justifiable from these numbers.

The large difference in **edge darkness** is an especially dangerous confound. Our real original crops were manually annotated within photographs with the sticker surrounded by dark wrapper/shadow, whereas several generated negative objects had clean artificially tight crop borders and no comparable dark background. A classifier trained here could be learning the *photo crop protocol*, not the difference between an INSIDE sticker and normal print. Do **not** promote that feature until independently photographed paper/packaging negatives have comparable margins and lighting.

Therefore this experiment **does not establish discriminatory printed-layout features**. A useful next measurement is to score genuine same-camera negative paper, preserve a standardized paper-plus-background crop margin for *both* classes and quantify per-zone missingness on tilted/occluded stickers. The run artifact preserves all eleven original-source SHA hashes and zone features, and no new CE serial or owner.


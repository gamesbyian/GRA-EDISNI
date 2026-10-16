# INSIDE CE: physically distinct sticker-region holdout benchmark, 16 October 2026

**Mode: VALIDATE generalization, not SEARCH for new serials.** This benchmark asks whether a localizer initialized with known physical sticker-paper crops from **003, 037, 038, 065, 125** can find the paper boundaries in completely **different original photographs** of **039, 047, 063, 118**. Every serial is already canonical. Source bytes and box annotations are SHA-pinned, and the evaluator checks there is no serial overlap between reference and test photographs.

[Independent holdout manifest](../../data/reference/inside-ce-sticker-region-independent-holdout.csv) | [Benchmark script](../../scripts/external_evidence/benchmark_sticker_region_holdout.py) | [Initial ROI pilot](inside-ce-sticker-region-recall-pilot-2026-10-16.md)

The four test images were visually inspected in their original, unmodified public-community copies. Annotated rectangular paper extents are normalized to image dimensions. They are all approximately frontal full-sticker/large-sticker photographs on dark paper. **This is a realistic positive-control step beyond synthetic composites, but not yet the final problem of detecting a very tiny 1–5%-area sticker in a wide cluttered photograph.** The four photographs differ in original source, crop, lighting, symbol, serial, image size, quality and surroundings.

## Frozen scoring, not adjustable success criteria

- For each test photo, perform the exact current **1600 coarse + 1200 refined windows** using 5 reference photos, 4 right-angle rotations per reference and eight reportable suggested regions.
- Compute intersection-over-union of each proposed region against the manually inspected **paper boundary**. Report whether *any* of top eight suggestions reaches IoU **0.25**, **0.40**, or **0.60**, plus top-one IoU, maximum top-eight IoU, raw suggestions and search-denominator counters.
- Do not convert the known serial of a held-out photo into a newly recognized serial. Do not retune thresholds for the four frozen examples without marking any change and developing a **separate, newly held-out independent set**.
- Successes and failures alike are reported. Tests enforce ground-truth integrity, disjoint reference IDs, pinned original SHA and honest grade, **not a predetermined positive accuracy claim**.
- **Negative-class false-positive rate remains unmeasured.** A white game case, white parcel, printed graphic or generic numbered ticket can resemble our paper stickers, so even 4/4 positive hit recall would not establish a useful deployment-grade visual detector.

## Reproducing

```bash
python scripts/external_evidence/benchmark_sticker_region_holdout.py \
  --repo-root . \
  --max-windows 1600 --max-refine-windows 1200 --top-k 8 \
  --output visual-evidence-work/region-independent-holdout.json
```

A regular, no-network pull-request job in `ce-visual-provenance.yml` executes this exact experiment and publishes the full JSON as a **30-day artifact**, permitting source-pinned independent review without API keys, browser or downloading collector media. No live search, scraping or owner outreach is involved.

## What to do with the results

A miss on a real sticker at top-eight/0.40 IoU means this particular fingerprint approach is not ready even for relatively easy frontal paper localization. Diagnose the *actual* missed window, missing scale, hash-score ordering, negative lookalikes and budget before scaling; do not blame a shortage of Internet searching.

A hit establishes localization feasibility on that **one known photographed object**, not source independence at Internet scale, classification specificity or ownership. Subsequent work: diverse independent photoreal negatives, background-only hard controls, sticker appearances occupying <10% of frame, JPEG blur/perspective, and alternative PDQ/embedding/corner-feature approaches if this method misses. Continue to use current community [numbered/L/U] reconciliation for any genuinely novel public lead.

**At document creation:** benchmark implemented and source annotations fixed; numerical measured recall belongs to the exact-head CI artifact, not to speculation or synthetic unit tests.

## Measured first exact-source CI run

[Original retained benchmark run 38957046067](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38957046067), executed on PR #303 source head `0eb597f2f35caa71536934edc631a4dd48525489`, scored the four genuine original photographs without provider retrieval. Logged summary:

- **Four of four** had at least one top-eight proposed box with **intersection-over-union ≥ 0.60** versus the manually fixed paper boundary. Consequently the ≥0.40 and ≥0.25 counts were also 4/4.
- **Mean best top-eight IoU = 0.70789**; fixed scan budget 1600 coarse plus 1200 refined windows; five other source photos as references, 20 rotated fingerprint variants.
- **No independent negative original photos evaluated.** False-positive rate is **not measured**; no serial was automatically read or sticker confirmed. These images mostly contain large, frontal papers, not tiny off-axis stickers in clutter.
- The source run passed 137 no-network tests in 10.166 seconds and uploaded `region-independent-holdout.json` as the retained 30-day artifact. The result is not a measurement of unlabeled public web-photo discovery.

This positive feasibility result warrants the next experiment: **real independent image negatives and genuine very-small-in-frame positives**, keeping the existing IoU targets, source IDs and current scan budget unchanged. Do not optimize further against these four now-observed holdout outcomes and call them unseen.

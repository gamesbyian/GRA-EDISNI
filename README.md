# GRA-EDISNI

Working repository for the INSIDE Collector's Edition sticker-code investigation.

## Purpose

This repository is the fast, executable research memory for the project.

The long-form Google Docs remain the historical archive:

- INSIDE Collector’s Edition Sticker Cipher Investigation Plan
- INSIDE Collector’s Edition Sticker Cipher — Results & Observations
- INSIDE Collector’s Edition Sticker Puzzle — Investigation Diary

Git is for compact state, reproducible analysis, experiment indexing, and session handoff. Do not mirror the full prose archive here.

## Start here

A new research session should normally read, in order:

1. `AGENTS.md`
2. `docs/current-state.md`
3. `docs/research-queue.md`
4. `data/machine-spec.json`
5. `docs/experiment-ledger.md` only as needed

Then run:

```bash
python scripts/verify_machine.py
```

## Research evidence map

For a conceptual view of what has been tried and what would discriminate the rival decoders:

- [Experiment 476 source-native receiver audit](docs/experiment-476-receiver-native-geometry-audit.md): direct Xbox 36-row reuse falsification, pinned Mac printer source, CE nine-sketch poster and ranked external reader gaps.
- [Experiment 466 background URL codebook control](docs/experiment-466-background-route-lookup-control.md): fixed 74-route retrospective lookup that clarifies how partial sticker artwork can become a uniquely identified destination without blind complete decoding.
- [Concept-map cross-link leverage audit](docs/concept-map-crosslink-leverage-2026-10-08.md): focus questions, two missing bridges, backward consumer joins, typed negative evidence, decision priorities.
- [Conjecture-led research audit](docs/conjecture-led-research-audit-2026-10-08.md): evaluates whether strict evidence gates are suppressing useful unsupported working hypotheses; proposes a separate exploratory/conditional/validation protocol.
- [Conjecture Lab](docs/conjecture-lab-protocol.md): active DISCOVER/DEVELOP/VALIDATE separation and [three worked first-sprint hunches](docs/conjecture-lab/2026-10-08-first-sprint.md), including an exact 324-master address-reader counterfactual.
- [Conjecture Lab second pass](docs/conjecture-lab/2026-10-08-second-sprint.md) and [progression audit](docs/conjecture-lab/2026-10-08-progression-analysis.md): observation-only 74-path lookup exclusion, balanced Q4 hypothesis, native printer checks, and selected 189/252/315 arithmetic curiosity with selection-aware controls.
- [CL-07 FULL historical gate-98 six-colour reconstruction](docs/conjecture-lab/2026-10-08-gate98-complete-six-layer-reconstruction.md): source-authenticated historical image **2,577/2,577 bright pixels** exactly matched with **zero extras** using six isolated original RGB layers. Sixth (#020206) needed a 32px translation correction and a 23px offcanvas sparse projection. Full original colour/offset selection remains retrospectively fitted; the CE foreground is not solved.
- [CL-06 original gate-98 2019 reconstruction](docs/conjecture-lab/2026-10-08-gate98-historic-multi-offset-reconstruction.md): authenticated original source and pre-CE composite show five colour-filtered, separately positioned image panels; exact-pixel recovery 2,070/2,577 historical white pixels (80.3%) with zero false positives, while a proposed sixth colour fails its simple extraction. Not a CE foreground receiver.
- [CL-05 recovered native gate-98 phase and planet positive control](docs/conjecture-lab/2026-10-08-gate98-native-phase-positive-control.md): exhaustive 256-phase black-pixel audit found authentic offset (4,12), reproduced a recognizable historical planet scan, corrected CL-04's assumed (0,0) origin and false colour-cube emphasis, and reran fixed sticker readers with negative results.
- [CL-04 authentic gate-98 receiver test](docs/conjecture-lab/2026-10-08-gate98-original-pixel-results.md): original source byte-hash, historical 16-pixel lattice, newly identified localized seven-colour 0xCF family, and two explicitly speculative 512-bank receiving rules tested against all banks; both lack a complete readout.
- [Four monitors/four breached schemes conjecture](docs/conjecture-lab/2026-10-08-cover-four-schemes.md): source-adjacent hypothesis that the cover recalls original completed ARG stages, with explicit missing PROBE/CONDISCON correspondences.
- [Experiment 458 prospective discriminator atlas](docs/experiment-458-common-mask-prospective-discrimination.md): identical evidence mask across seven dependent candidate projections, with exact disagreement residues and frozen predictions.
- [Experiment concept map](docs/experiment-concept-map.md): carrier → decoding mechanism → downstream consumer, history and critical distinctions.
- [Hypothesis-by-test coverage matrix](docs/hypothesis-test-coverage-matrix.md): operation families, comparison designs, negative results and specific missing evidence.
- [Evidence record cards](docs/evidence-register-view.md) and [structured CSV](data/sticker-evidence-register.csv): each curated test's source, dependence, corpus vintage, result and limitation.
- [Method and codebook](docs/evidence-map-method.md): scope, data dictionary, quality/appraisal criteria, refresh procedure.
- [Historical experiment title index](docs/experiment-title-index.md): navigation-only transcript of the compact [canonical ledger](docs/experiment-ledger.md).

The matrix is a curated decision map, **not** a score of theory truth, a systematic review of all original scripts, or independent confirmation of model-derived claims. Unmerged PRs remain provisional. Structural verification: `python scripts/check_evidence_map.py`.

## Operating posture

Assume no new sticker will ever surface. The current 66 observed H108 residues plus the reconstructed symbolic family are the critical path.

Structural prediction comes before semantics. The historical preferred grammar had 14 physical state masters before sticker 427 was confirmed; Experiment 418 leaves **10** live U5 masters on the current 84-record/66-residue observation snapshot. Experiment 280 also documents alternative transition-equivalent primary gauges under weakened physical grammar. Do not select a state or gauge because it produces an attractive word, image, or number.

The current mechanism is a typed registered selector/routing/canonicalization machine. The terminal `100` is mechanically established; downstream plaintext is not. Any external-consumer search must follow `docs/external-consumer-audit.md`: the external artifact supplies the cue first, rather than treating `100` or the surviving conditional hidden states as generic keys.

## Canonical responsibility split

- **Google Docs:** full historical record, narrative, provenance, detailed experiment write-ups.
- **This repo:** current truth, exact formulas, scripts, ledgers, bounded research queue, reproducible artifacts.

If the two disagree, investigate the discrepancy. Do not silently overwrite either history.

## Naming

`GRA-EDISNI` is `INISDE-ARG`-style reversal wordplay, but filenames and code should use plain descriptive English.

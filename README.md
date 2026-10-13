# GRA-EDISNI

Working repository for the INSIDE Collector's Edition sticker-code investigation.

**Speculative-revival research (9 October 2026):** [36 ranked old-idea revivals](docs/speculative-revival-portfolio-2026-10-09.md), [SR-03 nonbijective nine-digit keypad pilot](docs/speculative-sr03-keypad-revisit-pilot-2026-10-09.md), and source-driven [SR-04 body/tail domain preflight](scripts/speculative_tail_operator_preflight.py). These are *candidate designs*, not decoded CE foreground.\n\n## Purpose

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

- [CL-VLEN-03 streaming run-length instruction campaign](docs/conjecture-lab/2026-10-12-streaming-rle-instructions.md): a **real executable program**, with alternating unary opcode/operand runs and `EMIT`, `REPEAT`, `REVERSE`, optional `STOP`; exact finite-state accounting of 108 grammars across primary 81, tail 27 and collapsed full 108 symbols. None shows exceptional grammar-specific compatibility after 120 matched frame shuffles per region; a 14-number lever-shaped output does not distinguish the data. [Executable parser with exhaustive tiny-string oracle](scripts/conjecture_lab_streaming_rle.py), [compact summary](data/conjecture-lab-streaming-rle-summary-2026-10-12.json) and [full results/witnesses](data/conjecture-lab-streaming-rle-2026-10-12.json). No Playdead opcode table claimed.



- [CL-VLEN-02 class-run and reference instruction campaign](docs/conjecture-lab/2026-10-12-class-run-command-campaign.md): **462 exact three-opcode grammars** on the raw 84-record/66-residue corpus; 126 exact local run-statistic decoders fail, 23 of 336 reference interpreters remain compatible, and the best retrospective program loses against 119/120 and 118/120 matched shuffled controls. Physically held-out marker and class-group controls perform worse than one-hot-only baseline. [Executable analysis](scripts/conjecture_lab_class_run_programs.py), [summary](data/conjecture-lab-class-run-summary-2026-10-12.json) and [full archive](data/conjecture-lab-class-run-programs-2026-10-12.json). No decoded instruction claim.



- [Recovered 2019 GameFAQs INSIDE forum HTML](data/reference/inside-ce-gamefaqs-archived-html-recovery-2026-10-13.json): 38,546-byte archived page, independently hashed, 3,081 characters extracted, eight source excerpts; no new CE owner or sticker confirmed.
- [First measured INSIDE CE Wayback capture audit](docs/reference/inside-ce-first-archive-cdx-pilot-results-2026-10-13.md): eight real public CDX requests, a dated 2019 GameFAQs capture record, one no-match response and six provider errors (not absence claims).
- [INSIDE CE dated archive controls and CDX metadata checks](docs/reference/inside-ce-archive-cdx-positive-controls-2026-10-13.md): 16 original-source controls, 27 source/ownership/context lead records, bounded opt-in Wayback capture probes and synthetic CI validation.
- [CE edition-source differentiation and indexed lead triage](docs/reference/inside-ce-edition-product-differentiation-and-triage.md): first-party CE vs standalone PS4 distinction, cautious source dedup and automated post-search candidate review.
- [Raezore-ready CE owner lead shortlist](docs/reference/inside-ce-raezore-lead-handoff-2026-10-13.md): original public sources ranked by firsthand ownership, exact-case uncertainty and reusable photo evidence, with known lost L08 suppressed.
- [CE image-provenance indexing and blind known-positive source recall](docs/reference/inside-ce-image-provenance-and-gold-source-recall.md): local perceptual photo clustering, twelve confirmed-source controls and duplicate-resistant evidence handling.
- [Raezore's community search baseline and methodological coverage gaps](docs/reference/raezore-community-search-baseline-2026-10-13.md): source-audited history of search methods since 2018, an accurate overlap audit and a positive-control retrieval program.
- [Native-language INSIDE CE ownership hunt](docs/reference/inside-ce-native-owner-hunt-2026-10-12.md): 50 native locale profiles, 491 forum and 30 public marketplace/social search surfaces, GHA planning workflow, source-backed ownership/ARG lead ledger.
- [Forum search software stack and offline corpus index](docs/reference/forum-search-software-stack.md): tested SQLite FTS5 exact-symbol/multilingual search, optional warcio WARC ingestion, CI regressions, and researched CDX/DuckDB/crawler alternatives.
- [Public 2017 Steam forum preservation ZIP inventory](data/reference/inside-ce-archival-collection-candidates.tsv): two separately indexed ~4 GB SPUF files, uninspected and **not** modern Steam Community archives.
- [Worldwide gaming-forum archives and mirrors](docs/reference/global-gaming-forum-archives-and-mirrors.md): 491-row [historical fallback matrix](data/reference/global-gaming-forum-archive-routes.tsv), documented Steam/UOL rescue datasets, PTT mirrors, Arquivo.pt full-text, Common Crawl and 2026 access/coverage best practices.
- [Automatable multilingual forum search plan](docs/reference/global-gaming-forum-search-methods.md): per-forum methods for all 491 leads, [routing matrix](data/reference/global-gaming-forum-search-routing.tsv), safe query planner and opt-in indexed GHA workflow.
- [Worldwide gaming-forum discovery directory](docs/reference/global-gaming-forums.md): 491 multilingual forum/discussion leads, [machine-readable TSV](data/reference/global-gaming-forums.tsv), evidence-status caveats, and a source-first INSIDE archival search procedure.

- [CL-VLEN-01 variable-width and instruction-stream audit](docs/conjecture-lab/2026-10-12-variable-length-program-grammars.md): deterministic 3/5-bit prefix-code and opcode interpreters, exact raw-corpus run bounds, best-of-family shuffled controls, plus one-slash class-tail reconciliation after physical sticker 427 (36 historical assignments now 18). [Executable workbench](scripts/conjecture_lab_variable_length_grammar.py), [compact results](data/conjecture-lab-vlen-summary-2026-10-12.json) and [full machine-readable audit](data/conjecture-lab-variable-length-grammar-2026-10-12.json). This is a DISCOVER/DEVELOP experiment, not an identified decoder.



- [2026-10-09 Wow!-signal inscription audit](docs/conjecture-lab/2026-10-09-wow-signal-environmental-inscriptions.md): bounded first-person Big Ear encoding test of `A10N7`, `L08`, and `B02` against the 1977 positive control. Literal Big Ear encoding fails on written zeros and envelope shape. New byte-identical archives of the A10N7/L08 scene pair and B02 montage provide *low-resolution* visual evidence; the speculative 0/O + 1/I alternative has **no peak-shape discrimination** under its matched 26/26 alphabet control. Original full-resolution textures remain missing. Includes [deterministic replay](scripts/audit_wow_signal_inscriptions.py) and asset-source follow-ups.

For a conceptual view of what has been tried and what would discriminate the rival decoders:

- [Experiment 476 source-native receiver audit](docs/experiment-476-receiver-native-geometry-audit.md): direct Xbox 36-row reuse falsification, pinned Mac printer source, CE nine-sketch poster and ranked external reader gaps.
- [Experiment 466 background URL codebook control](docs/experiment-466-background-route-lookup-control.md): fixed 74-route retrospective lookup that clarifies how partial sticker artwork can become a uniquely identified destination without blind complete decoding.
- [Concept-map cross-link leverage audit](docs/concept-map-crosslink-leverage-2026-10-08.md): focus questions, two missing bridges, backward consumer joins, typed negative evidence, decision priorities.
- [Conjecture-led research audit](docs/conjecture-led-research-audit-2026-10-08.md): evaluates whether strict evidence gates are suppressing useful unsupported working hypotheses; proposes a separate exploratory/conditional/validation protocol.
- [Conjecture Lab](docs/conjecture-lab-protocol.md): active DISCOVER/DEVELOP/VALIDATE separation and [three worked first-sprint hunches](docs/conjecture-lab/2026-10-08-first-sprint.md), including an exact 324-master address-reader counterfactual.
- [Conjecture Lab second pass](docs/conjecture-lab/2026-10-08-second-sprint.md) and [progression audit](docs/conjecture-lab/2026-10-08-progression-analysis.md): observation-only 74-path lookup exclusion, balanced Q4 hypothesis, native printer checks, and selected 189/252/315 arithmetic curiosity with selection-aware controls.
- [CL-12 external SAF DEFLATE workbench provenance audit](docs/conjecture-lab/2026-10-08-external-saf-deflate-workbench.md): discovered third-party 17-candidate, source-mapped repair/visualization toolkit. Original SAF input exactly matches the archived April 14 file; 11.78MB candidate payloads rely on conditional history, synthetic endpoints and raster parameters, not an independently recovered 2019 backup or sticker receiver.\n- [CL-11 original saf_dat_col source-lineage audit](docs/conjecture-lab/2026-10-08-saf-dat-col-archival-duplicates.md): April 14 curl page and April 16 UTF-16 copy share all 1,900 Unicode replacement marks; latter is a deletion-only non-whitespace subsequence in 1,901/1,901 segments. A January 2023 Terminal41 ZIP contains 71/71 byte-identical already mirrored pages and no backup. Missing original `saf_dat_col_BACKUP.html` remains genuinely unlocated.
- [CL-10 original A adversarial JPEG alignment](docs/conjecture-lab/2026-10-08-authentic-a-adversarial-jpeg-alignment.md): new byte-true A gives 245 heuristic JPEG fill candidates, but **only 18/245** agree across the same five alignment conventions, exactly as few robust candidates as the older rendition. Not a full JPEG or sticker decode.
- [CL-09 primary April 2020 Terminal41 site-index archaeology](docs/conjecture-lab/2026-10-08-terminal41-unarchived-route-recovery.md): original byte-verified screenshots prove 10 omitted page/directory targets (including 1.9MB `saf_dat_col_BACKUP.html`, hibernation and four non-41 numbered terminals); original 12,140-byte damaged `534brn` A source recovered, changing heuristic candidate fills 238→245 but not yielding a full JPEG or sticker decoder.
- [CL-08 source-only gate-98 registration negative](docs/conjecture-lab/2026-10-08-gate98-source-only-registration-negative.md): native 16px colour phase and pairwise overlap do **not** recover historically correct six-layer registrations; 136, 1,148 and 2,233 better wrong shifts for three source-colour pairs. Phase constrains offsets modulo 16, not whole-lattice position.\n- [CL-07 FULL historical gate-98 six-colour reconstruction](docs/conjecture-lab/2026-10-08-gate98-complete-six-layer-reconstruction.md): source-authenticated historical image **2,577/2,577 bright pixels** exactly matched with **zero extras** using six isolated original RGB layers. Sixth (#020206) needed a 32px translation correction and a 23px offcanvas sparse projection. Full original colour/offset selection remains retrospectively fitted; the CE foreground is not solved.
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

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

- [Experiment concept map](docs/experiment-concept-map.md): carrier → decoding mechanism → downstream consumer, history and critical distinctions.
- [Hypothesis-by-test coverage matrix](docs/hypothesis-test-coverage-matrix.md): operation families, comparison designs, negative results and specific missing evidence.
- [Evidence record cards](docs/evidence-register-view.md) and [structured CSV](data/sticker-evidence-register.csv): each curated test's source, dependence, corpus vintage, result and limitation.
- [Method and codebook](docs/evidence-map-method.md): scope, data dictionary, quality/appraisal criteria, refresh procedure.
- [Historical experiment title index](docs/experiment-title-index.md): navigation-only transcript of the compact [canonical ledger](docs/experiment-ledger.md).

The matrix is a curated decision map, **not** a score of theory truth, a systematic review of all original scripts, or independent confirmation of model-derived claims. Unmerged PRs remain provisional. Structural verification: `python scripts/check_evidence_map.py`.

## Operating posture

Assume no new sticker will ever surface. The current 65 observed H108 residues plus the reconstructed symbolic family are the critical path.

Structural prediction comes before semantics. Under the preferred exact-POS3 grammar there are 14 physical state masters; Experiment 280 shows the same transducer has four transition-equivalent primary completion gauges (56 masters total) if that physical grammar is weakened. Do not select a state or gauge because it produces an attractive word, image, or number.

The current mechanism is a typed registered selector/routing/canonicalization machine. The terminal `100` is mechanically established; downstream plaintext is not. Any external-consumer search must follow `docs/external-consumer-audit.md`: the external artifact supplies the cue first, rather than treating `100` or the 14 hidden states as generic keys.

## Canonical responsibility split

- **Google Docs:** full historical record, narrative, provenance, detailed experiment write-ups.
- **This repo:** current truth, exact formulas, scripts, ledgers, bounded research queue, reproducible artifacts.

If the two disagree, investigate the discrepancy. Do not silently overwrite either history.

## Naming

`GRA-EDISNI` is `INISDE-ARG`-style reversal wordplay, but filenames and code should use plain descriptive English.

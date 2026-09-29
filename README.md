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

## Operating posture

Assume no new sticker will ever surface. The current 65 observed H108 residues plus the reconstructed symbolic family are the critical path.

Structural prediction comes before semantics. Do not select one of the 14 physical completions because it produces an attractive word, image, or number.

The current mechanism is a typed registered selector/routing/canonicalization machine. The terminal `100` is mechanically established; downstream plaintext is not.

## Canonical responsibility split

- **Google Docs:** full historical record, narrative, provenance, detailed experiment write-ups.
- **This repo:** current truth, exact formulas, scripts, ledgers, bounded research queue, reproducible artifacts.

If the two disagree, investigate the discrepancy. Do not silently overwrite either history.

## Naming

`GRA-EDISNI` is `INISDE-ARG`-style reversal wordplay, but filenames and code should use plain descriptive English.

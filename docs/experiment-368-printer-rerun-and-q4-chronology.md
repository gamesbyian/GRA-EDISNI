# Experiment 368 — printer-stream reuse rerun and Q4 grammar chronology

_Status: completed, 1 Oct 2026. Two follow-ups from Experiments 366 and 367._

## Part 1 — Experiment 15 rerun on all 65 residues

Experiment 15 parsed only 64 of the 65 known residues and asked to be rerun. The label-ordered printer tables were not reachable offline, so this rerun uses the two tables preserved as Discord attachments (`data/printer-strings/`): the 32 long PC strings in acorn order (the 9 short strings are missing) and all 47 unique Xbox strings. A confirmation with the complete reference tables follows the Part 1 results.

Preregistered design (script docstring): forward/reverse × all 6 symbol bijections; Family A slides each individual string along the cyclic H108 (statistic: longest zero-mismatch window, in known residues); Family B compares the full cycle with the concatenated table (best matches of 65). Null: 1,000 within-zone symbol permutations, seed 368.

| table | statistic | real | null median | null 95th | P(null ≥ real) |
|---|---|---:|---:|---:|---:|
| PC | A longest perfect window | 15 | 0 | 0 | 0.025 |
| PC | B concatenated best/65 | 43 | 42 | 45 | 0.366 |
| Xbox | A longest perfect window | 10 | 10 | 13 | 0.540 |
| Xbox | B concatenated best/65 | 41 | 42 | 46 | 0.889 |

**Concatenated streams (Experiment 15's actual test):** null for both platforms on the full 65 residues. Experiment 15's rejection stands.

**The PC Family-A window is not promoted.** It is a single placement: PC acorn line 5, reversed, symbols relabelled (`/`→`.`, `-`→`/`), starting at residue 76. It spans the zone boundary and matches the observed slash run at residues 78–81 followed by the dot-dominated tail. A stricter null that keeps every 9-cell row intact and permutes rows within each zone gives the same P = 0.025. So the score is driven by one structural feature of the real grid, the slash-ending last body row adjoining the dot tail, which any similarly shaped string would match. With four statistics tested, P = 0.025 is within chance (≈0.1 after correction), and 9 PC strings are missing from the table.

### Confirmation with the complete reference tables

Later on 1 Oct 2026 the complete Game Detectives tables were added in `data/printer-reference/` (all 41 PC strings, 48-row Xbox listing, publication order). They contain exactly the 32 long PC strings and 47 Xbox strings used above, plus the 9 short PC strings. Rerun (same seed and nulls):

| table | statistic | real | null median | null 95th | P(null ≥ real) |
|---|---|---:|---:|---:|---:|
| PC (all 41) | A longest perfect window | 15 | 7 | 10 | 0.025 |
| PC (all 41) | B concatenated, publication order | 44 | 43 | 45 | 0.259 |
| Xbox (48 rows) | A longest perfect window | 10 | 10 | 13 | 0.540 |
| Xbox (48 rows) | B concatenated, publication order | 44 | 43 | 46 | 0.306 |

The short PC strings raise the null baseline but create no new real match; the same single PC line-5 window drives the 0.025. Conclusions unchanged. Family B on publication order is reported for completeness only, because publication order is not a solved order.

## Part 2 — can chronology tighten Experiment 366's ~27:1?

Experiment 366 found the incumbent fits 7/330 shuffled Q4 arrangements against 192/330 for the tail-only family: at most ~27:1, because the incumbent's grammar may have been fitted to the same cells.

Q4 sticker first-recorded dates (upstream `stickers.md`):

| serial | residue | symbol | first recorded |
|---|---:|---|---|
| 095 | 95 | . | 05.01.2020 |
| 097 | 97 | . | 06.01.2020 |
| 193 | 85 | . | 09.01.2020 |
| 194 | 86 | / | 09.01.2020 |
| 312 | 96 | / | 25.01.2020 |
| 306 | 90 | . | 26.02.2020 |
| 206 | 98 | . | 25.03.2020 |
| 092 | 92 | . | 11.04.2020 |
| 324 | 108 | / | 29.05.2020 |
| 413 | 89 | . | 10.12.2021 |
| 317 | 101 | / | 24.12.2025 |

The incumbent investigation began on 27 Sep 2026 (creation of the Results and Plan documents), with all 11 Q4 stickers already public. The nearest community proposal of a tail index, the "9+3" readout of 22 May 2026 (Experiment 351), also postdates every Q4 sticker and never stated the one-slash rule.

**Conclusion:** no Q4 sticker has ever been a genuine prospective test of either family. The ~27:1 cannot be tightened from chronology; it stays an upper bound. Only a new Q4 sticker can test it.

## Discriminating acquisition targets

Among the 16 unobserved Q4 residues, the incumbent forces a symbol where the tail-only family does not at exactly two:

| residue | class | incumbent | tail-only | serials ≤ 600 |
|---:|---|---|---|---|
| 82 | A | `.` | `.` or `/` | 82, 190, 298, 406, 514 |
| 93 | C | `.` | `.` or `/` | 93, 201, 309, 417, 525 |

A **slash** at residue 82 or 93 would falsify the incumbent outright. A dot is consistent with both, but favours the incumbent. Residues 83, 87, 99, 104, 105 and 107 are forced identically by both families and cannot discriminate.

## Reproducibility

```bash
python scripts/audit_printer_stream_reuse_rerun.py   # Part 1, ~35 s
python scripts/audit_q4_holdout_selection_null.py    # Experiment 366 basis for Part 2
```

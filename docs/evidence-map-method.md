# Evidence Map Method, Coding Manual, and Update Policy

**Version:** 2026-10-08 (pilot reconciled through Experiment 465; Experiment 459 remains separate active work). **Type:** internal research-evidence *inventory and decision map*, adapting principles from systematic evidence and gap maps. This is **not a formally conducted systematic/scoping review**, a GRADE certainty assessment, or a meta-analysis.

## Objective and boundary

Question: *Which distinct, source-motivated decoding mechanisms for the INSIDE Collector's Edition sticker foreground have been examined, with what type of test, and which missing evidence would distinguish surviving mechanisms or validate an endgame consumer?*

**Scope screened for this revision:** all 444 canonical numbered experiment titles currently in `docs/experiment-ledger.md` (1–460, gaps 341, 434–447 and currently unmerged 459); detailed reports selectively read and cited in the evidence register; current research state, original experiment code, physical source data and merged PRs #140, #142–144 and #149. PR #141 was closed as a duplicate with its unique methodological caution reconciled. The full title index is generated in `docs/experiment-title-index.md`. **This is not an exhaustive line-by-line original source or script audit of 443 experiments.** The claim register remains a curated 35-evaluation pilot.

**Inclusion:** a fixed observation or historical provenance relevant to a decoder; a bounded falsifiable test or negative result; a model-family comparison; a prospective prediction; a source-constrained external consumer; an open PR with testable claimed results clearly marked pending. **Exclusion:** undocumented intuition as a verified result, repeated narrative restatements of the same experiment, code not tied to a finding, unconstrained visual or semantic guesses, and downstream consequences presented as independent support for their own premises. Retain excluded hypothesis narratives in other docs; do not label them falsified merely because they lack a register row.

**Sources and hierarchy:** primary physical observation (highest for raw symbols), time-stamped pre-model archive for historical operation *provenance*, exact reproducible report/script for bounded conditional conclusions, retrospective comparison for descriptive results, and open PR summaries as **unmerged/pending**. A confirmed physical observation can falsify a fixed conditional prediction; it does not automatically vindicate a rival model.

## Framework (separate axes, no category mixing)

### Three facets of a candidate pipeline

1. **Carrier/organization:** H108 periodic serial registration; A–I background; body/tail 81/27 split; 12×9, 9×12, 3×3 tiles, 4 cubes. These are observations or *representations*, not rival decoding mechanisms.
2. **Decoding operation (mutually exclusive primary family label per evidence record):** ORDER (reorder or shift), GEOMETRY (spatial glyph code, incl. Pigpen), TAIL (one-index selected line), RECURSIVE (POS3, repeated selectors, route), CONVENTIONAL (standard Trifid/Morse/Braille consumer), DIGIT (external numeric indexed lookup), LEVER (in-game directional command), OVERLAY (XOR/perimeter/cover combination), CUBE (explicit cross-cube transfer/depth/quarter operation), PUNCH (Hollerith/punch conversion). **BASE** is shared physical/historical context rather than a decoder. **CROSS** is a special *test-design* code for studies comparing multiple decoder families at once; it must not be interpreted as an eleventh competing decoder.
3. **Consumer/output:** registered word, instructions, image, coordinates, external URL, lever input, other interface, or **unresolved**. No output is presumed in advance. An encoding reformat without an externally fixed reader is not a solved output.

A compound theory may involve multiple operations. Record its **first discriminatory operation** as its primary family and preserve secondary operations in the finding/scope. Avoid double counting its observations across families.

### Register data dictionary

The authoritative curated rows are in [`data/sticker-evidence-register.csv`](../data/sticker-evidence-register.csv). One row = **one auditable finding/question/evaluation**, not one experiment, citation, or independent piece of evidence.

| Field | Interpretation |
|---|---|
| `record_id` | Immutable claim-level identifier R001, R002...; never recycle |
| `family` | One primary decoder code above, or BASE for common context, or CROSS for a multi-family comparator; CROSS is **not** a decoder |
| `question` | Narrow subquestion or property evaluated |
| `test_design` | Literal operation/test class, including exploratory or formal conditional |
| `independence` | Physical novelty, archives, same-corpus reuse, full-data selection, internal result, pending |
| `assessment` | Finding **scope** (e.g., rejects-fixed-grammar / compatible / underidentified / pending), not overall theory confidence |
| `experiment_ids` | ID(s) this record summarizes; `none` permitted for a purely narrative PR |
| `source` | Relative path on main for merged findings or PR URL for pending; link to inspect original |
| `source_state` | `main` or `open-pr`; never mix them in one row |
| `corpus` | Input vintage/mask, e.g. `historical-82-65`, `physical-84-66`, pre-427 ensemble |
| `dependency_cluster` | Same underlying observations/operation being retested; **do not count cluster rows as independent** |
| `finding` | Bounded outcome in words, with numbers only where documented |
| `scope_limit` | Explanatory limit or principal bias/circularity |
| `needed_evidence` | Narrowest usable external cue, frozen new test, or competing comparator |

**Missing value policy:** Empty matrix cell means *not mapped in this curated register*, never “proved untested.” `pending` means reported on an unmerged PR, not an executed/reproduced test certified by this map. `rejects-fixed-grammar` excludes that implementation, **not** the entire theory family. `compatible` is never coded as confirmation. Same-corpus leave-one-out after full-data selection is not blind validation.

### Critical-appraisal flags

For each row inspect (a) provenance and physical independence, (b) parameter and hypothesis-selection timing, (c) shared observation mask and duplicate-residue leakage, (d) appropriate null or trivial prediction baseline, (e) decoder complexity/flexible orientations, (f) directness of the measured outcome to the puzzle endgame, and (g) reproducibility. The register carries the critical limitations as specific fields, rather than forcing a misleading numerical evidence grade. No independent second coder or reliability statistic is claimed for this pilot.

**Historic discovery-channel rule:** Record whether a supposed external endgame was (a) *blindly read from the clue* before source search, (b) *recognized among source-enumerated alternatives* after seeing candidate answers, or (c) *verified by an independent operating consumer*. Experiment 465 provides a real documented example of type (b) for the Collector's Edition background: the exact URL was reportedly surfaced through a website index after earlier partial sticker readings. Strongly associated physical evidence need not be a full blind decode.

**Causal/evidence dependency rule:** If R001 proves repeat compatibility and R010 fits a conditional machine to those repeated stickers, R010 does not add a second independent empirical confirmation of the repeat. Likewise 329, 330, 339 and 340 share a selection episode; 378–391 and 418 follow one frozen external candidate, not multiple confirmations.

### Matrix interpretation

The [coverage matrix](hypothesis-test-coverage-matrix.md) shows *availability and design* of selected tests, and gives readable links to the claim register. It never sums generic “positive cells”, ranks theories by experiment count, or treats absent tests as negative outcomes. The strictest outcome level is **independent, frozen consumer that yields a verified next action/answer**; that box is currently empty.

## Updating this research map

1. Check `main` and all open PRs for ID collisions and unmerged results; keep a timestamp and the corpus vintage.
2. Read actual report and its script/fixture before upgrading `pending` to `main`. If code was not re-run, say so. Preserve failures and supersessions.
3. Add new claim-level rows rather than rewriting an old falsified prediction to fit newly observed stickers; if conclusion changes, link its dependency cluster and record the correction.
4. Pilot ambiguous categories on a small set of records first, update definitions before broad relabeling, and request independent review of disputed records when possible.
5. Update high-level coverage cells from register IDs; do not copy titles into multiple “study counts.” For new studies use the exact same withheld physical residues, null and baseline for head-to-head comparisons.
6. Treat 'gap' explicitly as: **no documented test**, **untested but testable**, **test exists but not discriminating**, **test flawed/confounded**, or **requires unavailable external/physical evidence**. A gap is not automatically an experiment worth doing.
7. Run `python scripts/check_evidence_map.py` and review diffs before merging. The script checks IDs/statuses, source paths and input counts, not scientific truth.
8. Record update dates and corpus changes in the mapping PR. Refresh after new owner-confirmed symbols, new merged research PRs, or an independent operation cue. Avoid idle periodic rewriting.

## Research-method precedents (analogies, not certification)

- **Campbell Collaboration (White et al., 2020):** [Guidance for producing a Campbell evidence and gap map](https://doi.org/10.1002/cl2.1125). Relevant adaptations: explicit framework and eligibility; transparent coding dictionary; pilot classifications; links back to studies; separate evidence availability from effect/direction.
- **3ie:** [Evidence gap maps](https://3ieimpact.org/evidence-hub/evidence-gap-maps). Links to underlying reports, filters for study design/confidence, ongoing-study identification, and avoiding duplicate future research.
- **PRISMA-ScR (Tricco et al., 2018):** [Scoping review reporting checklist](https://www.prisma-statement.org/scoping). Relevant adaptations: describe sources, screening, data charting, limitations and update state. We do **not** claim to satisfy PRISMA-ScR here.
- **Fredlund et al. (2024):** [Methodological review of evidence and gap maps](https://doi.org/10.1002/cesm.12096). Notes recurring weak points in gap definitions and updating practice.
- **Steegen et al. (2016) multiverse methodology:** [Increasing transparency through a multiverse analysis](https://doi.org/10.1177/1745691616658637). Relevant warning: conclusions that depend on chosen preprocessing/grammar should be shown across reasonable specifications, not the prettiest one. No comprehensive multiverse was run in this map.

The INSIDE ARG is not clinical intervention research, so intervention-effect confidence algorithms, clinical PICO, and numerical quality grades do not transfer automatically. Their *transparency and review-design principles* do.

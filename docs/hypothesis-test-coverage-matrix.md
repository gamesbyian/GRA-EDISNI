# Cross-Hypothesis Test Coverage and Discrimination Matrix

Snapshot: **2026-10-08**, main indexed through Experiment 423; open-PR 424, 426, 448–456 findings labeled pending. Companion: [concept map](experiment-concept-map.md). This is a structured synthesis of the indexed experimental reports and PR summaries, **not** a fresh run of their executable tests.

## What counts as coverage

- **T**: directly tested using a fixed operation; **N**: explicit null, negative control or counterexample; **C**: compatibility only; **P**: frozen prospective or independent masked test; **H**: historical operation provenance; **M**: model-internal/derived and not a cross-family test; **–**: no direct test identified in the indexed record.
- Cell references indicate experiments, not independent votes. A single study may occur in many cells. A negative result rejects the **specified implementation** only, not every conceivable member of its family.
- An operation can be objectively reproducible and still be selected on the very observations used to evaluate it. **Do not sum row/cell counts to estimate evidence strength.**

## Family definitions

| Code | Candidate explanation | Essential variable |
|---|---|---|
| F1 | Periodic serial carrier / manufacturing code | H108 period, print run, phase, A–I ownership |
| F2 | 2D image/row rearrangement | orientation, row/column permutation, registration, visual criterion |
| F3 | 3×3 geometry / 3D four-cube spatial correspondence | cube coordinates and cross-cube spatial transform |
| F4 | Tail-as-one-of-three selector without recursion | tail polarity, selected row/column/indexed feature |
| F5 | Primary POS3 plus Q4 recursive routing machine | POS3 constraints, two selections, Q3 route, terminal |
| F6 | Pigpen or other spatial letter glyphs | codebook, D4 symmetry, polarity, 9/12-cell slicing |
| F7 | Braille/Trifid/Morse direct conventional cipher | fixed alphabet, symbol polarity, axis/order |
| F8 | Digit-based cross-artifact indexing (534brn, Xbox) | registered digit-to-class and position mapping |
| F9 | Native mark-to-lever / game command consumer | .=L, -=R, /=U plus source-licensed order |
| F10 | External overlay/XOR/cover/check bits | specified aligned template and logical operation |
| F11 | Punch-card/Hollerith conversion | fixed hole-row mapping and downstream punch reader |
| F12 | Endgame instructions/coordinates/URL/pointer/physical action | authoritative endpoint consumer |
| F13 | Total-count/23 numerology | real manufacturing count and 23-driven grouping |

## Shared test-axis coverage

| Test axis | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A. Reproduces physical serial/symbol observations | T 297,421 | C 326 | C 18; pending 448 | T 317 | T 96,239,418 | C 328 | T/N 402–405 | C 378 | C 342 | C 419 | pending 424 | – | C 301 |
| B. Historically licensed decoding operation | H 297,301 | H 315,364 | H 351,373 (coordinates only) | H 315,376 | H 315 (carrier only); N 353,356–357 for later recursion provenance | H 351 (3-coordinate precedent, not Pigpen codebook) | H 351,402 | H 368–384 | H 342–343 | H 361–372,409–412 | H community suggestion, pending 424 | H 21,61,338; pending 144 | H 301 (endpoints do not follow) |
| C. Fixed-null/randomization calibration | T 12,421 | N 298,345,347 | pending 448,453 | N 339–340 | N 41,46,92,162,267 and others (often conditioned) | N 328,335 | N 394 | – | – | N 346,419 | pending 424 (information redundancy, not p-value) | – | – |
| D. Search-space / identifiability quantified | T 5–8,297 | T 298,345,347 | T 18; pending 450–453 | T 317–335 | T 159–172,226,250,294,303–314,365–367 | T 328,334–335 | T 394,402–405 | T 378–390 | T 342–343 | T 396,419 | pending 424 | – | pending 426 |
| E. Predicts independently hidden physical sticker | T 420–421 (period repeat) | N 360 | pending 454 (relative baseline essential) | P 336 (not yet fulfilled) | P/T 418 (new dot prunes families); T 323 conditional hideout | – | – | P/N 391,418 (E2 falsified) | – | – | – | – | – |
| F. Exact alternative-family side-by-side comparison | – | T 360–364 (acorn control) | pending 456 (depth vs quarter) | T 323,331,339–340 | T 323,331,367,390,418 | T 327–335 | T 402–406 | T 390,397–401,418 | T/N 342–343 | T/N 396,419 | pending 424 vs original ternary indicators | – | pending 426 vs 9/27/81/108 scales |
| G. Distinctive output with externally fixed consumer | – | N 361–364 | – | – | M 117–145 terminal 100 only | – | N 402–405 | T 378–390 conditional, not unique and later falsified E2 | N 342–343 known bunker word | N 409–412 no shared cover transform | – | – | – |
| H. Unambiguous final message/action validated | – | – | – | – | – | – | – | – | – | – | – | – | – |

**Reading the table:** A shared match to physical data is not a contest if families have different free parameters. Row E distinguishes prediction from after-the-fact compatibility. Row G deliberately demands a consumer chosen independently of the attractive outcome. **No family has crossed Row H.**

## High-information head-to-head tests

| Rival families | Experiment(s) | Observed distinction | What can be concluded | What cannot |
|---|---|---|---|---|
| H108 periodicity vs accidental repetitions | 7, 297, 301, 420–421 | Exact historical repeats, 20 same-residue pairs agreeing; period 108 privileged within bounded scans | Carrier repeat strongly supported | Print run endpoint or semantic decoder |
| Tail-only F4 vs incumbent F5 | 323, 329–340, 367 | Incumbent forces more held-out observed Q4 cells under its chosen grammar; row-one-exception rival survives a subset, but its four forced LOO successes follow by construction | Real predictive footprint differs; frozen row family retains its testable C-tail predictions | Independent vindication of recursively selected model |
| Original F5 vs external 534brn-selected F8 | 378–391, 418 | External transform selects a different family; newly observed 427-dot defeats its frozen E2 pair | Genuine prospective falsification of one specified cross-artifact mapping | All possible 534brn uses are false |
| F2 continuity vs actual acorn ordering | 345,347,360–364 | Even a strong canonical score on a positive control is not recoverable by blind score maximization | Generic order optimization is an inadequate decoder | All clue-constrained image orderings fail |
| F6 literal Pigpen vs observed marks | 327–328 | Every A–I body mixes slash/dash stroke families, incompatible with standard literal Pigpen strokes | Direct two-symbol ink model excluded | Arbitrary positional/category mappings excluded |
| F7 direct Morse/Trifid vs full completion ensembles | 402–405 | Frozen vanilla registrations produce structural impossibilities across U2 | These exact cheap direct ciphers closed | Any keyed or clue-provided alternate encoding |
| F10 ordinary XOR overlay vs entropy of unknowns | 419 | Deterministic 27-to-81 overlay does not prune candidate masters | Readout exists but alone conveys no selection | A separate independently registered overlay cannot work |
| F3 depth-selected readout vs quarter-selected instruction | Pending 450–456 | Alternative instructions yield disjoint master families and incompatible predictions at residues 50/54/93 | A sharply prospectively testable rivalry is available | Either instruction is independently author-proven |
| F11 punch card vs raw ternary | Pending 424 | Fixed mapping re-encodes original indicators without adding information | Conversion alone supplies no decoding discrimination | An externally specified punch-card apparatus is impossible |
| F13 621/648 versus endpoint-free model | Pending 426 | 621=23×27, 648=6×108 are arithmetically elegant | Named endpoints can be compared transparently | Any is a real manufacturing endpoint |

## Discrimination priorities, deliberately not a numeric score

**P0, strongest evidence leverage:** Preserve and make legible the frozen *opposing* symbol predictions before any future observations. The cube depth-vs-quarter branch identifies residues 50/54/93 (pending PR #143); the frozen row selector challenges residue 84/102 (336); incumbent U4/U5 distinction at residue 82 (422). The existence of multiple incompatible predictions is more useful than another internal uniqueness theorem.

**P1, use existing corpus now:** Reconstruct **one identical observation mask and null** for F2/F3/F4/F5/F6 on raw stickers, with the number of operation parameters and their provenance logged. This would expose whether family comparisons are truly symmetrical. Only include independently motivated, fixed operations; do not optimize each family until it looks meaningful.

**P1, independent consumer discovery:** Search archival sources for an exact operation *and its parameters*: row order, orientation, digit mapping, overlay offset, readout convention or target apparatus. This can defeat several families without new physical stickers. Report operation-class precedent separately from specific parameter provenance.

**P2, image/source evidence:** Compare individually preserved full-perimeter photos (344–346) with preregistered line/artwork geometry and independent-sample replication. A null grayscale edge channel does not exclude other specific, preregistered metadata channels.

**P2, deeper family falsification:** For the purported 3D scheme require an observation-only cube signature that survives mask/census-matched nulls **and** improves blinded prediction over trivial symbol-majority baselines. Pending PR #143's raw-copy tests explicitly show why correlation significance and predictive utility can disagree.

**Lower priority until new cue:** arbitrary alphabets, English-likeness search, 23 grouping, free-form overlay registration, unconstrained semantic outputs, and additional proofs of machine uniqueness conditional on the same starting axioms.

## Test proposal template for future cross-family audits

| Required field | Example discipline |
|---|---|
| Evidence snapshot | physical ledger commit SHA and known/unknown/duplicate counts |
| Compared families | codes F2/F3/F4/F5; literal grammar from frozen scripts |
| Shared target | same withheld residues, same symbol vocabulary, same scoring rule |
| Parameter ledger | each axis orientation/label/polarity: independently cued or fitted |
| Baselines | class/zone/symbol majority and census-matched masked null |
| Selection correction | tuning/test separation or selection-conditioned exact null |
| Predictions | list coverage, accuracy, log loss if probabilistic, exclusions and abstentions |
| Negative outcomes | explicit exclusion/falsification; “compatible” not a win |
| Provenance | script, immutable input, outputs, experiment ID, PR and source citation |
| Conclusion | local grammar rejected / family narrowed / still underidentified |

## Caveats requiring attention before merging the overview

1. The main ledger contains **422 numbered entries**, not necessarily 423: experiment 341 is absent. Unindexed older branch/PR experiments may account for other gaps.
2. The current map is a **title-index-based synthesis** with detailed selectively consulted recent reports and PR summaries. Do not describe it as an exhaustive independent review of 423 full reports and scripts.
3. The cube results in #142/#143 and punch-card/endpoint conclusions in #140/#141 remain **pending** until merged and independently checked.
4. “420–421 replication” denotes **same-residue physical agreement**, not wholly independent evidence of a decoder.
5. The most consequential missing cells in the coverage table are G/H, external consumers and validated outputs, rather than another operation-internal M-only theorem.

# Closed-corpus sufficiency and serial-coverage audit (12 October 2026)

**Mode: DEVELOP.** Mathematical feasibility and sampling audit, **not** a demonstrated Collector's Edition erasure code, verified edition size, decoded foreground, or proof of solvability. Physical snapshot: **84 observations / 66 distinct H108 residues / 42 unknown residues**, highest observed serial 597. Reuses the existing exact completion enumerators from Experiments 365/366/418.

## What the serials tell us

A physical serial s represents residue 1+((s-1) mod 108). Six hundred physical stickers contain 108 distinct foreground positions and 492 repeated placements, if H108 holds throughout. The present 84 specimens include 16 repeated-residue groups, 20 replication pairs, and zero conflicting physical marks. Repetition supplies confirmation, but repeating an entirely unseen residue does not disclose its value. No error-correcting *parity* operation has yet been demonstrated.

The new exact generating-function dynamic program counts every set of 84 physical serials sampled uniformly without replacement from each *hypothetical* print-run length. Entries report coverage of at least the **66** observed independent H108 positions:

| Hypothetical maximum serial | Mean unique | SD | P(unique >= 66) |
| ---: | ---: | ---: | ---: |
| 597 | 61.319 | 2.879 | **7.173%** |
| 600 | 61.306 | 2.880 | **7.114%** |
| 621 | 61.239 | 2.883 | **6.819%** |
| 648 | 61.211 | 2.884 | **6.698%** |

As a sensitivity check, condition on the observed number of discoveries in the six successive 108-serial bands: **19/18/17/19/10/1**. Within each band, assume exchangeable serials. An independent exact two-category hypergeometric DP obtains **61.703 expected unique** and **P(unique >= 66) = 9.035%** for all four endpoints. The equality across endpoints occurs because the sixth band has exactly one observed serial. It does not validate an endpoint.

The actual acquisition process is not a probability sample. Owners, listings, research, publicity and selection bias alter discovery rates. **Interpret 7–9% as a null-model diagnostic, not a p-value for the publishing process.** Under either diagnostic the observed coverage is moderately better than random, hardly an inexplicable serial distribution. The model cannot establish the size of the physical edition, whether undiscovered residues are special, or the intended human solve path.

## Parity: what would be sufficient?

**Without further constraints**, the 42 missing positions, each binary within its respective slash/dash or slash/dot zone, have **2^42 = 4,398,046,511,104** complete H108 foreground assignments consistent with all known marks.

An imagined known linear encoder over GF(2) could represent k independent payload bits across the 108 foreground positions. Given **66 independently observed positions**, a decoder could reconstruct k bits if the corresponding observed-bit submatrix has full column rank. For a hypothetical uniformly random binary generator, the exact full-rank probability is the product of (1-2^(i-66)) for i in 0..k-1:

| Hypothetical k payload bits | P(full rank from our 66 positions) |
| ---: | ---: |
| 50 | 99.9985% |
| 60 | 98.4456% |
| 62 | 93.8791% |
| 64 | 77.0102% |
| 65 | 57.7576% |
| 66 | 28.8788% |

This demonstrates **mathematical possibility**, assuming an independently known coding matrix. It offers **no positive evidence** of linearity, a particular parity count, a known generator, or a Playdead encoding method. It does not guarantee decoding for *all* possible 66-position masks.

The phrase "fewer than 82 parity symbols among 600 stickers" can mislead: 82 ordinary parity symbols could correct **at most 82 erased encoded symbols**, not 518. Multiple physical instances of the same H108 cell are replication, not a demonstrated algebraic parity check. A compact payload plus a separately signalled decoder might nonetheless be quite sufficient.

## Existing model-specific information: do not confuse assumptions with discovery

The repo's *already-existing* exact enumeration scripts give these **conditional** completion counts on the current 66-residue corpus:

| Declared family | Compatible complete masters | Remaining log2(count) bits | Minimum *correctly selected* extra foreground coordinates to identify every master |
| --- | ---: | ---: | ---: |
| U0: zone-binary raw | 2^42 | 42 | 42 absent other constraints |
| U1: per-frame 3/6 or 4/5 + one-slash Q4 | 557,280 | 19.09 | not established here |
| U2: one minority per physical column + one-slash Q4 | **324** | **8.34** | **10** |
| U3: established polarity / POS3 | **108** | **6.75** | **8** |
| U4: first recursive closure | **12** | **3.58** | **5** |
| U5: second recursive closure | **10** | **3.32** | **5** |

Sources: scripts/build_completion_universe.py, scripts/audit_completion_universe_layers.py, docs/experiment-365-completion-universe.md, docs/experiment-366-universe-layer-audit.md and docs/experiment-418-sticker-427-prospective-prune.md. Historical counts in older prose can predate the physical dot at serial 427. Conditional completion counts are **not posterior probabilities** and do not separately confirm their own structural premises.

Under U2–U5, many absent symbols are fixed by the model but **no complete master is uniquely determined by the physical marks**. Their predictive strength is real *inside the declared family*; an independent source must identify the correct family and, ultimately, the output operation.

## Interpretation and next hard test

The strict claim "more stickers are required" is **unproven**; so is the strict claim "the existing corpus determines the intended answer". The relevant criterion is *answer identifiability*, not uniqueness of every foreground sticker. Some viable completions could share one downstream output under a genuinely independent readout.

Keep the **closed-corpus** research posture. The next discriminating computation is a **family-invariant consumer audit**: fix a historically sourced receiving artifact and input-formation rule *before* inspecting its outputs; evaluate every member of U2/U3/U5 and relevant alternative grammars, and check whether their distinct missing-cell values affect that receiver. If every viable candidate yields the same accepted output, full sticker recovery would be unnecessary. Do not choose the consumer because it produces an attractive result.

## Reproduction

Run from repository root:

    python scripts/audit_closed_corpus_sufficiency.py --json
    python scripts/build_completion_universe.py --write
    python scripts/audit_completion_universe_layers.py

The new audit uses Python's standard library, an exact integer combinatorial normalizer, an exact band-conditional probability DP, an exhaustive six-item synthetic control, and a fail-fast frozen-data guard. It changes **no** physical ledger, predictions, corpus provenance, theorem or machine settings.

# PX-08: Exact no-new-sticker erasure and completion boundary

**Date:** 16 October 2026. **Mode:** DEVELOP, closed-corpus exact enumeration by independent-choice proof. **Source:** `data/observations.csv`; reproduce with `python scripts/audit_perspective_erasure_bound.py --check` or `--json`.

## Premises, deliberately weaker than the incumbent

1. Treat the direct 84 physical records as 66 observed unique locations on an H108 cycle, with 20 observed same-residue pairs all agreeing (Experiment 421).
2. Grant the simple **conditional** observation-motivated sector alphabet: residues 1–81 may be slash/dash, and residues 82–108 may be slash/dot.
3. **Do not** assume one-minority-per-frame, the U2/U5 generators, Q4 depth, parity, physical-production sheet order, candidate text, or a receiving artifact.

These assumptions define a purposely broad parent language. The sector restriction is extrapolated to missing cells; it is not itself verified at each unseen site.

## Exact observed coverage and freedom

| Region | Allowed marks under conditional grammar | Known unique residues | Unseen unique residues | Count of possible fillings |
|---|---|---:|---:|---:|
| Body 1–81 | `/` and `-` | 54 | 27 | `2^27` |
| Tail 82–108 | `/` and `.` | 12 | 15 | `2^15` |
| **Total** | Two options per missing cell | **66** | **42** | **`2^42 = 4,398,046,511,104`** |

The known body positions contain 32 slash and 22 dash. The known tail positions contain four slash and eight dot. Consequently, even each region's **total number of slashes** remains free within broad ranges: **32–59** body and **4–19** tail, conditional on this grammar. The physical census does not force a global slash total.

Without imposing the zone rule at unseen positions at all, the literal three-glyph assignment space is **`3^42`**, larger still.

## Proof of exact conditional count

Under this minimal parent grammar every unobserved residue is independently assigned one of two allowed glyphs, and every observed residue remains fixed. The 108-period repetition only copies the chosen glyph to other serials with the same residue; it creates no relationship **between** different unobserved residues. Thus choosing each one of the 27 body and 15 tail binary alternatives specifies exactly one full H108 master, and each such master is consistent with the physical observations. All **`2^(27+15)`** assignments are different. The script checks the observed mask, sector classification, known counts and the exact power-of-two cardinality.

Therefore **no currently missing glyph is forced by the combination of H108 recurrence and 81/27 sector restriction alone**. Any asserted unique full message, image or program requires an additional hypothesis: structural grammar, external key, selective readout, error correction, or original decoder instructions.

## Why this matters for the intended player

The popular inference “the cycle is only 108 long, so it should be recoverable without nearly all copies” has an important hidden dependency. **Periodicity reduces a possibly 600-label print run to 108 distinct positions; it does not repair erasures between those 108 positions.** The deliberate distribution scheme could have used genuine ECC or a sparse semantic decoder, but the period and sector split alone are *not* such a mechanism.

The far smaller **U2=324** and **U5=10** completion families are useful exact **conditional** calculations under additional, stronger grammars (post-427 values). Their compression of this broad space is not independent proof that those grammars were authored. Revisit [completion-universe study](../experiment-365-completion-universe.md) and [Q4 erasure ablation](../experiment-474-q4-erasure-scope.md) before claiming recovery from a partial corpus.

## Counterfactual decisive next step, without acquiring stickers

To make the foreground identifiable from *existing* source material, an independent artifact would have to provide (i) a specific coupling rule making some missing positions redundant, (ii) an externally fixed list of only a few read positions that happen to be observed, (iii) an original codeword/receiver constraint, or (iv) a verified next-stage input that scores a finite set of frozen candidate outputs.

A plausible-looking bitmap or word selected after inspecting the same 66 positions does not reduce this observational freedom as evidence. This proof deliberately does not rule out those more informative sources.

**Disposition:** Exact erasure baseline completed, no new sticker sought or required. PX-08 remains active because evaluating *which* source-native redundancy or readout could actually exploit the partial data is a separate experiment.

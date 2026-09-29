# Research Queue

_Current queue begins after Experiment 240._

## Operating directive

Assume no new sticker will ever surface.

The mechanical transducer is the current baseline. Do not reopen semantic fishing. Work should either:

1. reduce the supplied axioms further;
2. prove uniqueness in a broader nearby family;
3. expose a new completion-invariant native operation;
4. improve reproducibility / independent verification;
5. reconstruct the intended human solve with fewer assumptions;
6. recover genuinely independent archival/manufacturing evidence.

## Priority 1 — broaden uniqueness audits

The current mechanical model is compact, but some uniqueness statements remain conditional on declared native families.

**Progress through Experiment 245:** the recursion assumptions have been materially hardened.

- First pass: in the 729-member family `B(f(q),g(S),j)`, POS3 validity plus p-factorization leaves 49 broad survivors; restricting both coordinate maps to shell-preserving permutations forces `g=identity`, leaving only the six relabelings of external q. Fixing physical q labels leaves the canonical identity/identity substitution uniquely.
- Second pass: in the 729-member family `B(f(S),g(S),j)`, 25 arbitrary-map pairs produce completion-invariant POS3 terminals, but the permutation-preserving subfamily has exactly one survivor: identity/identity, yielding terminal `100`.

Remaining high-value ingredients:

- primary local column-POS3 grammar itself;
- the single unresolved frame-polarity completion at `q=1,d=2` under weaker-than-staircase grammars;
- canonical Q3 shell orientation;
- broader recursion parents that are not expressible as independent ternary coordinate maps.

**Experiment 246 removes outer no-self registration from this list.** Under POS3, raw observations force 8/9 frame polarities. With the established `d<=q` staircase, they force 25/27 primary trits, including all 18 outer trits; all 18 already satisfy no-self.

Goal: determine whether the present transducer remains uniquely or near-uniquely selected without smuggling in its own representation.

Stop a branch when extra parameter freedom grows faster than the constraints it resolves.

## Priority 2 — proof pack / theorem graph

**Experiment 241 completed the first explicit dependency graph** in `docs/theorem-graph.md`. Continue turning the graph into executable assertions and use it to expose hidden circularity.

The graph currently integrates Experiments 215, 220, 231, 233, 237, and 238 and separates:

For each current claim mark:

- supplied observation;
- supplied local grammar;
- derived theorem;
- descriptive algebraic closure;
- observer-only fact;
- closed semantic branch.

Goal: one minimal theorem chain from corpus-facing axioms to terminal `100`.

This is partly epistemic hygiene and partly a route to discovering remaining redundant assumptions.

## Priority 3 — independent implementations

**Experiments 242–243 satisfy the first major independence target.** `scripts/verify_native_model.py` reconstructs the machine in native `(x,y,p,g)` coordinates from the request/grant relation and shares no generator code with the Boolean `XYZG` implementation. `scripts/compare_models.py` then confirms exact equality of the full 14-master sets.

Still desirable: a genuine constraint/enumeration implementation reconstructed from lower-level axioms rather than either state parameterization.

Independent implementations must reproduce:

- 14 legal masters;
- all 82 classified stickers;
- 95 invariant / 13 variable cells;
- recursive rank 14→3→1;
- terminal frame9 / `100`;
- observer rank 14.

Disagreement is a bug or hidden assumption and should stop downstream work.

## Priority 4 — human solve reconstruction

Experiment 246 materially improves the likely human entry path: the primary object can now be presented as “the stickers visibly determine almost the entire ternary lattice” rather than as a heavily inferred reconstruction.

Now that the machine is theoremized, reconstruct the shortest plausible human path without using conclusions before they are discoverable.

Current likely path:

1. serial→A-I cadence;
2. H108 fold;
3. 12 A-I rows;
4. 9+3 alphabet split;
5. common POS3 ternary encoding;
6. primary registration;
7. Q4 depth selector;
8. recursive address substitution;
9. canonical Q3 shell;
10. second-pass canonicalization.

Explicitly identify which steps are visible from raw marks and which require hypothesis testing.

Do not require group theory, T3, MDL, or observer algebra for the intended path.

## Priority 5 — broader alternative-machine search

Construct nearby machines that preserve:

- the same carrier/address geometry;
- ternary positional coding;
- similar state burden;
- similar recursion budget.

Ask whether equally simple alternatives explain all observed cells but terminate elsewhere or lack the current route structure.

This is the strongest remaining closed-corpus adversarial test.

Use exact enumeration or SAT/SMT-style constraint solving if the family becomes too large for direct loops.

## Priority 6 — archival/manufacturing lane

This is opportunistic, not critical path.

High-value artifacts:

- original sticker/prepress source;
- numbering/variant spreadsheet or script;
- print proof / imposition sheet;
- vendor job ticket;
- direct production explanation.

Useful question:

> Did production merely replicate the 108-state master, or does a surviving source artifact reveal how that master was authored?

Do not treat generic 108-up printing examples as an explanation of the internal machine.

## Closed branches

Do not reopen without an independent cue:

- XML;
- MIX;
- MISS / MISSION / MISSING;
- generic Braille continuation;
- terminal ASCII `?`;
- 621 / 648 arithmetic;
- generic alphabets;
- arbitrary bitmap fitting;
- generic Boolean pointer combinations;
- T3 ordinary map composition;
- terminal printer-mask optimization;
- known INSIDE decoder families already audited in Experiment 240.

## Safe stopping condition

If every broader structural family either:

- reproduces the same transducer;
- requires materially more description freedom;
- or becomes too unconstrained to discriminate,

then the current mechanical crack should be treated as the project endpoint unless independent evidence supplies a semantic continuation.

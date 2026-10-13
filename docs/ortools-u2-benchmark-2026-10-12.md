# Exact U2 pilot: OR-Tools CP-SAT versus existing enumerator

_12 October 2026. DISCOVER/DEVELOP. No new physical sticker, CE decoder or validated receiving artifact._

Following the initial Z3 tail pilot in [PR #182](https://github.com/gamesbyian/GRA-EDISNI/pull/182), try [Google OR-Tools CP-SAT](https://github.com/google/or-tools) against a **less trivial but still exactly enumerable** family. Its [official solver documentation](https://github.com/google/or-tools/blob/stable/ortools/sat/docs/solver.md) describes explicit solution callbacks with one worker and no optimization objective.

The fixed experiment is the broad 3/6 primary minority-per-column + one-slash-per-class tail model (the repo's U2 family, explicitly **conditional** on those rules). Encode 108 slash-vs-other Boolean variables, equality for all 66 observed residues, a per-frame choice of 3 or 6 slashes with per-physical-column counts 1 or 2, and exactly one slash across each 3-cell class tail. The model does not import the incumbent recursively generated states.

`scripts/benchmark_ortools_u2.py` independently enumerates the same family with the preexisting `enumerate_sticker_completion_ensembles.py` combinatorial functions. It requires equality of **every one of the 108-cell candidate strings**, not only matching cardinalities. The current corpus is expected to produce **324** U2 masters, compared with the historically larger count before sticker 427. It hashes the sorted complete candidate set, reports non-portable runtimes and fails loudly on incomplete CP-SAT enumeration or a changed corpus.

Run separately from the main verification matrix:

```sh
python -m pip install ortools==9.15.6755
python scripts/benchmark_ortools_u2.py
```

Or inspect the short [dedicated CI job](../.github/workflows/ortools-u2-benchmark.yml) and its JSON artifact. The code has been syntax checked locally, but the optional package was unavailable there; GitHub Actions constitutes the real solver execution check.

**Promotion rule:** If CP-SAT exactly agrees with the established enumerator, it becomes a reusable search engine for *harder independently motivated constraints*, without conferring any new confidence on the 3/6 grammar. If it is slower on this 324-member case, retain the pure Python method for this model. The next useful comparison is a harder, source-cued registration/permutation family where exact enumeration becomes expensive. Never optimize for recognizable output without matched nulls and provenance.

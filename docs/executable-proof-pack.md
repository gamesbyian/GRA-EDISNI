# Executable proof pack

This is the runnable companion to `docs/theorem-graph.md`.

The goal is narrow: make it harder for a future edit to introduce circular support, silently pull observer/algebra facts into the transition proof, or let the three current implementations drift apart.

Run:

```bash
python scripts/verify_proof_pack.py
```

The runner reads `data/theorem-obligations.json`, parses the theorem graph, checks its dependency structure, verifies that terminal node `T6` has no `R`, `A`, or `S` ancestors, and then runs six existing independent checks:

- the Experiment 246 raw-primary reconstruction, including the derived outer no-self result;
- the canonical Boolean machine verifier;
- the native `(x,y,p,g)` verifier;
- exact Boolean/native master-set comparison;
- raw 216-candidate reconstruction through recursive POS3 closure;
- exact raw/canonical/native master-set comparison.

This is not a fourth implementation of the machine. That would add another body of code capable of sharing the same mistake. The proof pack instead makes the independence relationships explicit and executable.

## Coverage rule

All theorem-class nodes on the dependency path to terminal `T6` must be claimed by at least one executable check in the manifest. Observation and grammar nodes are represented structurally rather than treated as derived assertions.

Observer, algebra, and semantic branches may have their own executable checks, but they are forbidden as ancestors of `T6`. If a future model legitimately changes that boundary, the theorem graph and manifest must be changed together and reviewed as an epistemic change, not merely a code refactor.

## What this catches

The pack fails if:

- a theorem table references an unknown theorem node;
- the theorem graph contains a dependency cycle;
- a node's declared class disagrees with its ID;
- `T6` stops depending on one of the currently declared transition inputs;
- an observer/algebra/semantic node becomes upstream of `T6`;
- a terminal-chain theorem loses executable coverage;
- a required verification script disappears;
- any independent implementation/reconstruction check fails.

## What this does not claim

A green proof pack does not prove that the supplied grammars are the uniquely intended human assumptions. Priority 1 and Priority 4 still attack that problem. It proves a more practical property: the current stated theorem chain is internally wired the way the documentation says it is, and the independent executable realizations still agree on the machine family and terminal.

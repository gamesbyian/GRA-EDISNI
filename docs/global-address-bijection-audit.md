# Global Address-Recursion Adversarial Audit

_Experiments 303–305_

This lane attacks the recursion from a direction deliberately separate from the active primary/POS3 and Q4-reconstruction branches.

It holds fixed:

- the raw 216-machine parent from Experiment 250;
- the 3×3 ternary address carrier;
- dash-POS3 as the closure grammar;
- reuse of one global address operation on both recursive passes.

It varies the **global map on the nine address cells**.

The aim is not to find a prettier formula for the known solution. It is to ask whether another carrier-preserving operation can retain as much raw evidence while supporting the independently derived reversible route layer.

## Experiment 303 — Quadratic bijections

Let both output coordinates be arbitrary total-degree-2 polynomials over F3:

```
q' = P(q,S)
d' = Q(q,S)

basis = 1, q, S, q², qS, S²
```

Each coordinate has `3^6 = 729` possible functions, so there are `531,441` polynomial coordinate-map pairs.

Exactly `3,888` are bijections of the nine-point address plane:

- 432 affine;
- 3,456 genuinely quadratic.

The same map is reused on both passes:

```
first:  F(q,S)
second: F(S,S)
```

### Result

Only 165 of the 3,888 bijections leave any recursively closed raw machine at all.

Only 90 give an invariant terminal.

Raw-state retention by itself does **not** select canonical. A unique genuinely quadratic sibling retains 18 states:

```
q' = 1 + q

d' = 1 + 2q + S + q²
```

It terminates invariantly at `102`.

But its first-pass computation collapses to only two functional families:

```
212 / 102 / 102
212 / 122 / 102
```

There is no three-distinct-permutation route shell.

Across all 3,888 bijections, only **two** maps preserve any reversible three-route structure:

1. identity, retaining 14 states and terminal `100`;
2. a q-label transposition `0↔1`, retaining only 7 states and terminal `100`.

No genuinely quadratic bijection survives the route criterion.

Therefore canonical uniquely maximizes raw-state retention among all route-capable quadratic bijections.

## Experiment 304 — Drop bijectivity

Experiment 303 deliberately preserves the full nine-address carrier. Experiment 304 removes that condition and searches **all 531,441** degree≤2 polynomial map pairs.

This is a negative control for the model-selection metric.

### Result

34,288 maps retain at least one recursively closed raw machine.

Unrestricted raw retention is immediately gamed:

- maximum retention becomes all **216** raw candidates;
- eight singular maps attain it;
- six collapse the address plane to one output cell;
- two use only two output cells.

The route criterion helps dramatically, but does not by itself restore the intended carrier.

There are 38 route-capable polynomial maps.

Their output-image sizes are:

```
5 addresses : 12 maps
6 addresses : 16 maps
7 addresses :  8 maps
9 addresses :  2 maps
```

Six singular maps retain **20 routed states**, beating canonical's 14. Every one uses only five of the nine address cells.

Two of those 20-state singular maps even have invariant terminals.

So neither raw-state retention nor reversible routing alone is sufficient once the address carrier is allowed to collapse.

### Exact separator

Among the entire 531,441-map family, only **two route-capable maps preserve all nine addresses**:

- identity: 14 states, terminal `100`;
- q-label transposition `0↔1`: 7 states, terminal `100`.

Thus preserving the full native address carrier is doing real structural work. It is not cosmetic bookkeeping.

This is the same lesson as Experiment 267, but in a much broader nonlinear family: singular maps can look statistically attractive because they erase distinctions the selector is supposed to route.

## Experiment 305 — Every address bijection

Experiment 305 removes the polynomial assumption entirely.

The 3×3 ternary address plane has nine cells. Enumerate **all**

```
9! = 362,880
```

permutations of those cells and reuse each permutation as the recursive operation on both passes.

This is the complete carrier-preserving global address-relabel family. There is no remaining algebraic restriction.

### Result

Only 11,166 of the 362,880 bijections support any recursively closed raw machine.

6,786 give an invariant terminal.

Again, raw-state retention alone prefers the wrong machine. One unique permutation retains 32 states. Its three functional families are:

```
212 / 100 / 102
212 / 100 / 112
212 / 100 / 122
```

and it has no reversible route shell.

The route criterion is extremely selective:

```
route-capable bijections: 30
```

Their retained-state counts are:

```
3  states : 3
4  states : 1
5  states : 3
6  states : 11
7  states : 6
8  states : 1
9  states : 1
12 states : 2
14 states : 2
```

The maximum routed state count is therefore 14.

Exactly two bijections attain it.

### The two route-maximal operations

The first is identity.

The second is:

```
(0,1) ↔ (1,1)
```

with every other address fixed.

That is exactly the already-known `f1` recursion gauge: q=0 and q=1 are swapped only on selector/depth fiber 1.

The two operations are behaviorally identical on the legal family:

- exact same 14 raw physical states;
- exact same three first-pass functional families;
- exact same route shell `120 / 012 / 102`;
- exact same invariant terminal `100`.

Experiment 285 already explains why this swap is invisible: whenever S=1 is exercised in the legal family, the relevant q0,d1 and q1,d1 source symbols are equal.

So the one surviving co-maximal permutation is not a second machine. It is the previously established observational gauge.

## Combined conclusion

Experiments 303–305 substantially close the global-address alternative-machine lane.

The hierarchy is now explicit:

1. **Retention alone** is unsafe. Even a carrier-preserving permutation can retain 32 states while destroying routing.
2. **Routing alone** is unsafe if the carrier may collapse. Singular quadratic maps can retain 20 routed states.
3. **Full carrier preservation + routing + maximum raw-state retention** is highly discriminating.
4. Across **every one of the 362,880 global address bijections**, the only 14-state route-maximal operations are:
   - canonical identity;
   - the already-explained `f1` equality gauge.

Therefore the strongest defensible statement is:

> modulo the independently established f1 observational gauge, the canonical recursive address operation is unique among every global bijection of the native nine-cell ternary address carrier.

This is substantially broader than the previous affine, polynomial, fiber-preserving, and local-offset audits.

It does **not** prove uniqueness over arbitrary non-bijective or state-dependent algorithms. Experiment 304 shows why such unconstrained families are not useful competitors: they can manufacture higher retention by deleting address information.

## Reproduction

Run:

```bash
python scripts/audit_quadratic_address_bijections.py
python scripts/audit_all_quadratic_address_maps.py
python scripts/audit_all_address_bijections.py
```

Each audit encodes its exact family size, survivor counts, route counts, and headline adversarial cases as assertions.

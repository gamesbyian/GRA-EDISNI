# Experiment 314 — selector-controlled local q-shear audit

_Date: 2026-09-29_

## Question

After Experiment 313 closed constant local translations of both address coordinates, the smallest genuinely state-dependent extension is a local **shear** controlled only by selector value:

```
F_j(q,S) = (q + c_j S, S) mod 3
```

with one ternary coefficient `c_j` at each A–I cell.

The same operation is reused on both passes. This gives state dependence without introducing a hidden-state oracle, special terminal decoder, or arbitrary lookup table.

## Exact family

Nine cells, three coefficients each:

```
3^9 = 19,683
```

operations.

The audit starts from all 216 raw-compatible primary×selector candidates and applies ordinary POS3 closure plus the established reversible-route criterion.

Executable audit:

`scripts/audit_local_selector_shear.py`

## Result

Raw retention again over-rewards degenerate operations.

The maximum raw-state count is:

```
20
```

but every operation retaining more than 14 states is route-degenerate.

Exactly **99** shear operations preserve any reversible route shell:

| retained states | route-capable operations |
|---:|---:|
| 6 | 36 |
| 7 | 36 |
| 12 | 18 |
| 14 | 9 |

The route maximum is therefore 14.

All **nine** route-max operations are observationally identical to canonical:

- same 14 raw physical survivors;
- same three first-pass functional families;
- same route shell `120 / 012 / 102`;
- same invariant terminal `100`.

## Exact gauge

The nine route-max operations are simply:

```
c_E ∈ {0,1,2}
c_F ∈ {0,1,2}
all other c_j = 0
```

so the gauge has size:

```
3 × 3 = 9
```

The invisibility is exact and easy to explain.

### E

Every raw-compatible selector has:

```
S_E = 0
```

Therefore:

```
q + c_E S_E = q
```

for every coefficient. The shear term is never activated.

### F

Every raw-compatible selector has:

```
S_F = 1
```

At physical F and depth 1, all three source q values contain slash for every one of the six raw-compatible primary payloads:

```
q0 = /
q1 = /
q2 = /
```

So changing q by `c_F` cannot change any symbol read there.

The E/F freedom is therefore an exact operation gauge, not merely a tie on the final 14 states.

## Interpretation

Experiment 314 tests the first tightly bounded selector-dependent coordinate coupling beyond constant translations.

It produces no new functional rival.

The pattern from the broader adversarial program remains intact:

1. extra coordinate freedom can retain more raw states;
2. those larger families lose the reversible route structure;
3. maximum routed retention stays at 14;
4. surviving co-maximal rules are explainable equality/unused-input gauges.

Within this shear family:

> canonical is unique up to independent ternary E/F shear gauges.

## Stopping consequence

Do not broaden next to arbitrary per-cell functions `q' = f_j(q,S)` merely because they can be enumerated or quotient-compressed. That would introduce many independent parameters without a new physical clue.

Priority 5 has now closed:

- all global carrier bijections;
- natural local selector permutations;
- local additive translations of both coordinates;
- the minimal selector-controlled local q shear.

A further adversarial family should be pursued only if its additional state dependence has an independent structural rationale.

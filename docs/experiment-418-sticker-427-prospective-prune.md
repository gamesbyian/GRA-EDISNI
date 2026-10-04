# Experiment 418 — sticker 427 prospective prune

_Status: completed prospective physical validation, 4 Oct 2026._

A Collector's Edition owner has confirmed the foreground symbol on **sticker 427**:

```
427 = dot
```

The background tile image is still unknown and is therefore **not** entered as an observed image class.

Because `427 mod 108 = 103`, this adds a physical foreground observation at H108 residue **103**.

## Live ensemble impact

Replaying the current coherent completion machinery with residue 103 fixed to dot produces:

| ensemble | before | after |
|---|---:|---:|
| U2 | 648 | **324** |
| U3 | 216 | **108** |
| U4 | 20 | **12** |
| U5 | 14 | **10** |

The observation therefore removes exactly half of U2 and U3, 8 of 20 one-shot U4 states, and 4 of 14 recursive U5 states.

The recursive terminal remains:

```
100
```

for every surviving U5 state.

## Prospective 534brn result

Experiment 391 froze a sharp prediction before this confirmation:

```
residue 103 = slash
```

for **both** masters selected by the `534brn` target `112/012/120`.

The physical observation is instead:

```
residue 103 = dot
```

Replaying the frozen target after adding 427 leaves:

| ensemble | target survivors |
|---|---:|
| U2 | **0** |
| U3 | **0** |
| U4 | **0** |
| U5 | **0** |

So the previously selected E2 pair is prospectively falsified under its frozen registration and the one-slash-per-depth-stack carrier assumptions. This is a useful negative result: the physical evidence has now decided the test that Experiments 390–392 deliberately set up.

Do **not** rescue the pair by changing the registration after seeing 427. A future external artifact could license a new registration, but the old one has failed its physical prediction.

## Additional tail consequence

Residue 103 belongs to the D depth stack:

```
85, 94, 103
```

Residue 85 was already observed as dot. With 103 now also dot, the independently supported one-slash-per-depth-stack model forces:

```
94 = slash
```

This is a model-derived prediction, not a new physical observation. Its physical serial family is:

```
94, 202, 310, 418, 526, 634
```

## Operational consequence

The live weighted/completion program should now use **42 unobserved residues**, U2=324, U3=108, U4=12 and U5=10. The old E2 panel is retired. Historical experiments that used E2 remain valid as records of what was frozen and predicted before the new observation.

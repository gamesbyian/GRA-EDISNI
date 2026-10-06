# Experiment 429 — lag-23 autocorrelation audit

## Question

Does the H108 foreground have unusual self-similarity at displacement 23?

For each of the 10 live canonical masters, compare every residue with the residue 23 positions later modulo 108. Rank the mean exact-symbol agreement against all lags 1..107.

## Result

Lag 23 mean agreement:

```
0.3898148148
```

Across the 107 non-zero lags, lag 23 ranks **36th** by agreement.

The strongest lags are small local offsets, led by ±2 and ±1, which is unsurprising given the native 3×3 / 9-cell carrier structure.

So 23 is not a privileged foreground autocorrelation distance.

## Disposition

Negative.

There is no evidence here for using 23 as a shift, overlay displacement, or repeat interval inside H108. This further isolates the live 23 hypothesis to total-count / grouping geometry rather than an internal foreground period.

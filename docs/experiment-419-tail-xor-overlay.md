# Experiment 419 — tail XOR overlay and 4×27 geometry

_Status: completed bounded community-proposal test, 4 Oct 2026._

A community solver proposed two related observations:

1. the known dots are heavily concentrated in the final three rows of the conventional 12×9 layout, motivating a possible narrow carrier such as 4×27;
2. repeat the final three slash/dot rows over the first nine slash/dash rows and combine them as an XOR-style overlay.

The supplied diagram makes the second operation exact enough to test without visual fitting.

## Frozen XOR operation

Use canonical 12×9 serial order.

For body rows 1–9:

```
slash = 0
dash  = 1
```

For tail rows 10–12:

```
slash = 0
dot   = 1
```

Repeat the three tail rows three times over the nine body rows:

```
tail 10 -> body 1,4,7
tail 11 -> body 2,5,8
tail 12 -> body 3,6,9
```

Then XOR corresponding cells.

The result is a 9×9 binary surface.

On the physically observed corpus alone, 24/81 XOR cells currently have both inputs known: 9 are 1 and 15 are 0. The remaining 57 depend on one or more missing sticker observations.

## Exact ensemble replay

| ensemble | masters | distinct XOR surfaces | invariant XOR cells | variable |
|---|---:|---:|---:|---:|
| U2 | 324 | 324 | 52 | 29 |
| U3 | 108 | 108 | 55 | 26 |
| U4 | 12 | 12 | 58 | 23 |
| U5 | 10 | 10 | 60 | 21 |

The operation therefore does **not** collapse the completion universe. Every master remains distinguishable after XOR.

That is still useful: the proposal creates a compact visualization of exactly which body/tail relationships differ between candidates.

## Strong regularity

Every U4 and U5 XOR surface contains exactly:

```
36 ones
45 zeroes
```

More strikingly, the three 3-row / 27-cell q blocks always have weights:

```
9 / 12 / 15
```

This is exact across all 12 U4 states and all 10 U5 states.

It initially looks like an independent pattern, but it is algebraically downstream of the current machine assumptions.

Under exact POS3 polarity, the body q blocks contain:

```
q0: 15 dashes
q1: 12 dashes
q2:  9 dashes
```

For a G5-valid selector, the selected nine cells in each q block contain exactly three dashes. The XOR leaves those selected cells unchanged and flips the other 18 cells. Therefore a q block with T body dashes becomes:

```
3 + (18 - (T - 3)) = 24 - T
```

giving:

```
24-15 = 9
24-12 = 12
24-9  = 15
```

So the elegant staircase is a useful **visual checksum of G5 validity**, but not independent evidence for G5.

## Why this operation is still valuable

The tail-as-overlay idea is historically better motivated than arbitrary bitmap manipulation. Community solvers had already noticed that the dot region behaves unlike the first 81 symbols and suspected it might be decoding/registration metadata. The May-2026 9+3 proposal likewise treated the small tail as a selector or aid acting on the larger body.

This XOR is therefore worth preserving as a bounded representation even though it does not solve the code.

Its best uses are now:

- visualization of remaining completion uncertainty;
- prospective comparison when a new sticker fixes an XOR cell;
- testing an independently supplied consumer against the 9×9 derived surface;
- checking whether another artifact explicitly calls for parity/XOR/compositing.

Do not rank the 12 or 10 surfaces by visual attractiveness.

## 4×27 / Morse suggestion

The 4×27 orientation is structurally natural:

```
rows 1-3 = 81-cell slash/dash body
row 4    = 27-cell slash/dot tail
```

So it should remain in the representation catalogue.

But a literal printed-symbol Morse reading of the fourth row has a basic problem: that row has only slash and dot. Standard written Morse needs dot, dash, and some form of separation, or else a separately specified pulse-timing convention.

A 27-cell binary telegraph/Morse interpretation is not impossible. It simply needs an independent rule saying which state is signal, which is gap, and how run lengths encode dot/dash/letter spacing. Without that cue, choosing the convention after inspecting outputs would reopen the arbitrary Morse fishing already closed by Experiments 403–405.

## Result

Preserve the XOR overlay as a legitimate deterministic derived surface.

Do **not** promote it to a decode yet. The next useful positive would be an external clue that explicitly licenses parity/XOR, compositing, or a binary timing grammar.

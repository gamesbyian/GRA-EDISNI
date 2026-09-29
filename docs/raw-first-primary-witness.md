# Raw-first 34-residue POS3 view

_Status: human-facing support for Experiments 259–262._

This view deliberately hides the solved ternary lattice and the `q,d` labels.

Start only from:

- the established H108 fold;
- the natural consecutive 9-residue frames;
- the physical A–I arrangement:

```
I A B
C D E
F G H
```

A middle dot means the minimum witness has no observed sticker at that cell.

## Frames 1–9

### Frame 1 — residues 1–9

```
· · /
- - /
· · ·
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 1

### Frame 2 — residues 10–18

```
- · ·
- / ·
· · /
```

Exact-POS3 completions:
- slash-minority: 1
- dash-minority: 0

### Frame 3 — residues 19–27

```
· · /
- · ·
- · ·
```

Exact-POS3 completions:
- slash-minority: 3
- dash-minority: 0

### Frame 4 — residues 28–36

```
/ · /
/ - /
· · ·
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 1

### Frame 5 — residues 37–45

```
· - ·
/ · ·
/ · -
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 1

### Frame 6 — residues 46–54

```
· / /
/ · ·
· · ·
```

Exact-POS3 completions:
- slash-minority: **1**
- dash-minority: 8

This is the only frame where both polarities survive. The slash-minority choice is locally fully determined; the alternative leaves substantial freedom.

### Frame 7 — residues 55–63

```
· · /
- · /
· · ·
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 3

### Frame 8 — residues 64–72

```
· · ·
/ · ·
/ - -
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 1

### Frame 9 — residues 73–81

```
· · -
- / ·
· / ·
```

Exact-POS3 completions:
- slash-minority: 0
- dash-minority: 1

## What is visible before solved notation

Eight of the nine frames allow only one exceptional-symbol polarity under exact POS3.

The ninth frame allows both, but one polarity yields a single completion while the other yields eight.

Therefore a purely local worksheet rule:

> keep a polarity only if it admits an exact one-exception-per-column completion; when both survive, prefer the more determined completion

recovers all nine frame polarities from this 34-residue view.

Only after that step should the worksheet reveal that the resulting polarity sequence is the simple triangular staircase `d<=q`.

## Why this matters

The staircase no longer needs to be the first clever abstraction a human invents. A plausible route is:

1. arrange raw marks into the nine consecutive physical frames;
2. notice that one-exception-per-column strongly constrains symbol polarity;
3. resolve the lone tie by local determinacy;
4. then notice that the nine recovered polarities themselves form a simple 3×3 staircase.

That is a more human-shaped discovery path than presenting the staircase as an unexplained global rule.

## Limits

This still assumes the solver is already testing:

- H108;
- the A–I physical layout;
- exact POS3 as a candidate local grammar.

It is not evidence that those earlier recognitions are inevitable.

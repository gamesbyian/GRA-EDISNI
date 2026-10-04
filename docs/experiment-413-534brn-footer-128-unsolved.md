# Experiment 413 — the 534brn footer reads “128 UNSOLVED”

_Status: completed exact glyph/run-length audit, 4 Oct 2026._

The unresolved `534brn` page contains, immediately after the damaged JPEG-like payload:

```
pe^!02un
........
..
.
```

In April 2026 a community member suggested reading this backwards as “128 unsolved.”

That suggestion is substantially better than it first appears.

## 180-degree glyph reading

Rotate the eight-character string through 180 degrees.

The character order reverses:

```
pe^!02un
   ->
nu20!^ep
```

Under the ordinary upside-down glyph correspondences visibly built into those characters:

```
n -> u
u -> n
2 -> s
0 -> o
! -> l
^ -> v
e -> e
p -> d
```

the result is exactly:

```
unsolved
```

The three following dot runs have lengths:

```
8
2
1
```

The same 180-degree reading reverses their order:

```
1 2 8
```

So the complete footer reads:

> **128 UNSOLVED**

This is not a generic cipher search. The transformation is supplied by the glyph construction itself.

## Why this matters

The number 128 is attached directly to the still-unresolved damaged JPEG page.

Experiment 414 checks whether 128 has a native structural target in that JPEG rather than treating it as a free number key.

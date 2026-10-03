# Experiment 375 — G5/G6 burden shift after native coordinate typing

_Status: completed synthesis audit, 2 Oct 2026._

Experiments 373–374 materially change where the remaining uncertainty sits.

## G5

Previously, the reset treated G5 as using the tail selector as a depth substitution on the body, with the choice of body axis still model-level.

That is now too pessimistic.

The historical twelve-square representation gives each A-I class a nine-cell primary body plus three-cell tail. In native serial coordinates, those positions are:

```
primary: (Q,d) = 00 01 02 10 11 12 20 21 22
tail:    (Q,d) = 30 31 32
```

Experiment 317 independently supports one slash selecting one of the three tail positions. Therefore the selector value is physically a **d-position**.

If the tail/index is applied to the preceding body without changing coordinate type, the only direct operation is:

```
d = S(j)
```

while Q and j remain registered.

That is exactly G5.

So the unresolved G5 burden is no longer “which coordinate should the selector replace?” It is only:

> was the tail intended to index the body at all?

That remaining premise has substantially better provenance than before: the historical 9+3 proposal explicitly treated the final three positions as a smaller index into the larger first-nine domain, and the Xbox puzzle supplies a Playdead-authored precedent for local positional selection.

## G6

The same analysis makes G6 more clearly conditional.

After G5, the three surviving surfaces are indexed by **Q**.

Reusing `S(j)` to choose among them requires treating a d-coordinate as a Q-coordinate. That is not native type preservation; it is a new identification between two distinct ternary axes.

Experiments 291/322/269 remain important because once such a second selector-conditioned read is admitted, the operation is highly constrained. But those experiments do not supply the missing d-to-Q identification or the decision to repeat.

So G6 should now be described as:

> a mechanically strong, historically unsupported cross-axis recursion/coercion.

## Evidence-first stopping point

Experiment 374 shows that stopping after G5 leaves a highly structured six-state object:

```
1 x 2
0 y 2
1 z 0
```

with middle column in:

```
002 010 020 110 112 220
```

This is therefore the preferred evidence-first endpoint until an independent cue says to identify d with Q, repeat the selector, recurse, or otherwise consume the Q axis.

The recursive machine is not discarded. It remains the strongest developed continuation and still reaches the 14-state family and invariant terminal `100`. Its terminal should simply remain explicitly conditional on G6.

## Practical consequence

Future external-consumer work should search two surfaces in parallel, without conflating them:

1. **one-shot typed surface:** the six-state 3×3 family from Experiment 374;
2. **recursive conditional surface:** terminal `100` and associated route shell.

An external artifact that independently presents a repeat/recursion or d-to-Q identification would upgrade G6. An artifact that naturally consumes the one-shot 3×3 family could instead terminate the machine earlier.

This is a useful fork, not a failure to choose.

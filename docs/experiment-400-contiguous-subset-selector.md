# Experiment 400 — contiguous 9+3 subset selection is a hard negative

_Status: completed bounded two-layer test, 4 Oct 2026._

The May-2026 discussion proposed a very specific architecture:

- first nine bits encode a larger domain;
- final three bits encode a smaller selector;
- the selector chooses something inside the larger first-nine structure.

Experiment 373 later showed that the tail selector is physically a **d-coordinate**.

There are nevertheless two cheap ways to partition the first nine positions into three groups of three.

## Two natural partitions

In native `(Q,d)` order, the first nine cells are:

```
Q0d0 Q0d1 Q0d2
Q1d0 Q1d1 Q1d2
Q2d0 Q2d1 Q2d2
```

A type-preserving tail selector `d=S(j)` selects the **strided d-rail** across Q. That is G5.

The obvious competing interpretation selects one **contiguous Q chunk**:

```
S=0 -> Q0d0,Q0d1,Q0d2
S=1 -> Q1d0,Q1d1,Q1d2
S=2 -> Q2d0,Q2d1,Q2d2
```

That is the cheapest literal “pick one of three subsets” alternative.

## Bounded readout

After selecting the contiguous three-bit chunk for each class, ask whether it naturally encodes a ternary position through either:

- exactly one dash;
- exactly one slash.

No semantic decoding follows. The selected chunk either has a clean one-of-three position or it does not.

Run across:

- U2 / 648;
- U4 / 20;
- U5 / 14;
- E2 / 2.

## Result

For the **one-dash** interpretation:

```
U2  0 valid completions
U4  0
U5  0
E2  0
```

For the **one-slash** interpretation:

```
U2  0 valid completions
U4  0
U5  0
E2  0
```

No completion makes all nine selected chunks into clean ternary codes.

## Interpretation

This is a useful structural negative.

The historical “larger domain + smaller selector” intuition survives, but its cheapest cross-axis implementation does not.

The contrast is now sharp:

- tail selecting the **d rail** preserves the selector's native coordinate type and produces G5;
- tail selecting a contiguous **Q chunk** fails universally.

That gives another independent reason not to treat the three ternary axes as freely interchangeable.

## Consequence

Close contiguous first-nine chunk selection.

Do not try arbitrary partitions of the nine body cells into three subsets just because the completion ensembles make them cheap to enumerate.

Reopen only if an external artifact specifies a different partition.

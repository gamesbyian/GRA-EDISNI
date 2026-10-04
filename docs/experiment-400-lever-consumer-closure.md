# Experiment 400 — the stable nine-command output was already exhaustively tested at the lever

_Status: completed historical-consumer closure, 4 Oct 2026._

Experiment 398 produced a robust historically licensed nine-symbol feature:

```
--/--/-/-
```

Under the independent Collector's Edition sleeve / lever mapping:

```
/ -> U
- -> R
. -> L
```

that becomes:

```
RRURRURUR
```

Before treating this as a possible new lever code, the historical lever-testing record needs to be consulted.

That record closes the obvious consumer.

## The 2023 exhaustive lever run

In November 2023, community solvers executed an exhaustive three-symbol lever search using a De Bruijn-style construction.

The discussion explicitly records:

- the naive 14-command space as roughly 60 million when shorter strings/redundancy are considered operationally;
- the reduced De Bruijn run as roughly **4.7 million** combinations;
- the workload split into 20 segments;
- completion of the final segment on 12 Nov 2023;
- the final report: **all codes done, no results**.

The exact ternary length-14 space is:

```
3^14 = 4,782,969
```

which matches the reported 4.7-million search scale.

A De Bruijn traversal covering every length-14 ternary word also contains every shorter ternary word as a substring. The historical discussion itself explicitly notes that the run should cover 13-, 12-, 11-command and shorter combinations.

Therefore the nine-command word:

```
RRURRURUR
```

was necessarily exercised during that completed search.

It produced no new bunker-door result.

## Anti-bruteforce caveat

The community discussed the possibility of an anti-bruteforce lock.

The historical testers reported that the **known** bunker code continued to open the door after hours of failed inputs, which argues against a simple lockout mechanism invalidating the search.

This is not proof against every possible stateful condition, but it makes the ordinary “hidden standalone lever code” interpretation a strong negative.

## Consequence for Experiment 398

The stable digit-index sequence remains real as a derived feature:

```
--/--/-/-
```

What is closed is its cheapest semantic consumer:

> enter `RRURRURUR` at the ordinary secret-ending lever to unlock a previously unknown result.

That interpretation has already been physically tested in-game as part of an exhaustive search.

## Why this is useful

This is exactly the workflow the weighted-completion sandbox is supposed to produce:

1. derive a robust feature across uncertain completions;
2. identify an independently motivated consumer;
3. check the consumer against historical evidence;
4. kill the interpretation cleanly if reality already tested it.

No extra cipher layer is needed to rescue the lever idea.

## Status

Preserve Experiment 398's nine-symbol output as a robust derived feature with **no currently live lever consumer**.

Reopen lever semantics only if a new artifact specifies a different game state, initialization, timing/state transition, or a sequence longer than the historically exhausted range.

# Experiment 401 — the stable digit-index lever sequence was already tested in-game

_Status: completed historical replay audit, 4 Oct 2026._

Experiment 398 produced an unexpectedly stable historical-index output:

```
--/--/-/-
```

Under the independently historical sleeve/lever mapping:

```
- -> R
/ -> U
. -> L
```

that becomes:

```
RRURRURUR
```

At first glance this looks like exactly the kind of nine-command candidate that could reopen the lever consumer.

The 2023 archive lets us test that directly.

## Historical brute-force campaign

In October–November 2023, community members generated a ternary De Bruijn-style lever sequence covering the candidate command space and divided it into 20 sections for physical in-game execution.

The surviving archive includes raw command streams for sections:

```
10, 11, 12, 13, 14, 17, 18
```

Historical messages document those sections being run and ultimately report:

> all codes done, no results.

Rather than rely only on the abstract De Bruijn coverage claim, search the **actual surviving tested command streams** for the exact Experiment-398 sequence.

## Exact result

`RRURRURUR` occurs:

```
section 10: 19 times
section 11:  4
section 12:  4
section 13: 10
section 14:  3
section 17:  6
section 18: 60
```

Total in the surviving archived tested sections alone:

```
106 occurrences
```

So the exact nine-command sequence was not merely theoretically covered by the brute-force design. It appears repeatedly in preserved command streams that were actually run in-game.

No new lever-area result was reported.

## Conclusion

This closes the most obvious consumer for Experiment 398.

The stable sequence:

```
RRURRURUR
```

is **not** a plausible undiscovered in-game bunker lever code under the ordinary lever-input behavior tested in 2023.

That is a strong historical negative.

## Scope

Do not overextend the result.

This does **not** falsify:

- the historical symbol-to-lever geometry itself;
- the possibility that sticker marks describe lever directions in another context;
- a sequence requiring some independently cued timing/state/setup not present in the 2023 tests;
- a non-game consumer that merely uses the same three-direction alphabet.

It specifically closes:

> direct use of the Experiment-398 stable nine-command sequence as a hidden bunker lever trigger.

## Consequence for the weighted sandbox

Experiment 398 remains a robust derived feature, but its cheapest semantic consumer is dead.

Preserve `--/--/-/-` as a stable indexed signature. Do not spend effort trying nearby lever permutations or timing variations without a new cue.

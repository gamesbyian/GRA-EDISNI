# Experiment 408 — Terminal41's exact nine-step chain is not a nine-symbol consumer

_Status: completed external-consumer audit, 4 Oct 2026._

After Experiment 398 produced a robust nine-symbol signature, the external-consumer search should pay attention to independently existing **nine-position** structures.

Terminal41 contains one exact candidate:

```
___________DONE_SD_CONFIRMED_09.html
...
___________DONE_SD_CONFIRMED_01.html
```

Nine objects is the right cardinality. That is enough to inspect the mechanism, but not enough to claim a match.

## Exact source audit

All nine archived pages were inspected as source.

Their behavior is:

```
09 -> 08 -> 07 -> 06 -> 05 -> 04 -> 03 -> 02 -> 01
01 -> PROT6y723g90ty9r80234_confirmed_0385729128474.html
```

Each page is essentially a zero-delay HTML meta refresh.

Across the nine pages there are:

- no forms;
- no input fields;
- no selectors;
- no per-step symbol choices;
- no alternate branch targets;
- no payload that varies according to an entered state.

So the nine-page structure is a fixed countdown/transition chain.

## Why this matters

Experiment 398 gives a stable nine-symbol output:

```
--/--/-/-
```

A nine-step Terminal41 object is superficially tempting as its consumer.

But a consumer needs somewhere for the nine values to matter.

This chain has none.

Its nine states are temporal/progression states, not nine addressable symbol slots.

Therefore:

> exact 9↔9 cardinality is present, but the interface grammar is absent.

That closes this candidate cleanly.

## Guardrail

Do not assign the nine sticker symbols to the nine redirect pages merely because the counts match.

Reopen only if another Terminal41 artifact supplies a genuine nine-choice, nine-value, or nine-address input surface.

## Broader lesson

The external-consumer program should continue to distinguish:

- **same cardinality**, which is cheap;
- **same typed interface**, which is evidence.

Terminal41's shutdown chain passes the first and fails the second.

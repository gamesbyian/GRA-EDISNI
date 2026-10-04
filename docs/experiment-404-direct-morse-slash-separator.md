# Experiment 404 — slash-as-Morse-separator is a hard negative

_Status: completed bounded historical replay, 4 Oct 2026._

In September 2026, while discussing the reconstructed H108 stream, the community explicitly asked:

> are the slashes intended as spaces for the morse code?

That is specific enough for a cheap ensemble test.

## Frozen family

Use:

- serial H108 order;
- slash as character separator;
- collapse slash runs as separators;
- the other two sticker marks as Morse dot/dash;
- test both possible dot/dash polarities;
- accept standard International Morse A–Z and 0–9 tokens.

No cyclic shift, row permutation, plaintext scoring, or punctuation extension is admitted.

## Result

Across both polarities and all:

```
648 U2 completions
```

valid complete Morse parses:

```
0
```

The negative has a simple invariant witness.

Every U2 completion contains:

```
residues 69..76 = /------/
```

So slash-separated parsing necessarily contains a six-mark token:

```
------
```

or, under opposite polarity:

```
......
```

Neither is an A–Z Morse letter or a 0–9 Morse digit.

The failure does not depend on any of the 43 missing stickers.

## Interpretation

This closes the cheapest interpretation of the foreground as ordinary serial-order Morse with slash separators.

That is stronger than “the text looked wrong.” The grammar fails before text exists.

## Reopening trigger

Morse should reopen only if another artifact independently supplies:

- a different traversal;
- a fixed grouping;
- a role for repeated slashes other than ordinary separators;
- or a specific nonstandard Morse alphabet.

Do not search cyclic starts or arbitrary reorderings simply to break the six-mark witness.

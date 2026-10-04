# Experiment 414 — “128” lands exactly on the damaged JPEG's unresolved dimension field

_Status: completed cross-capture JPEG-header audit, 4 Oct 2026._

Experiment 413 decodes the footer of the `534brn` page as:

```
128 UNSOLVED
```

There is a striking independently derived place for that number to act.

## Recovered SOF shape

The three genuinely distinct damaged capture families A, B and P were retokenized under the already established corruption model:

- bytes `0x80..0xFF` become unknown;
- NUL `0x00` is represented as space `0x20`;
- line-wrap bytes are ignored.

Each capture contains exactly one occurrence of the same JPEG SOF0-shaped sequence:

```
?? ?? 20 11 08 20 ?? 20 ?? 03 01 22 20 02 11 01 03 11 01
```

Interpreted through baseline JPEG structure:

- unknown/unknown = damaged `FF C0` marker;
- `20 11` = original length `00 11`;
- `08` = 8-bit sample precision;
- `20 ??` = height `00 ??`;
- `20 ??` = width `00 ??`;
- `03` = three components;
- component 1 uses `2×2` sampling;
- components 2 and 3 use `1×1`.

The two dimension low bytes are unknown precisely because they were in the destroyed high-byte range.

Therefore both dimensions independently lie in:

```
128 .. 255
```

This reproduces the December-2025 community forensic conclusion directly from all three capture families.

## The new connection

The page itself says:

```
128 UNSOLVED
```

and the unresolved JPEG header contains two dimensions whose only surviving constraint is:

```
128 <= dimension <= 255
```

So 128 is not merely another ARG number that happens to exist somewhere.

It lands exactly on an unresolved native JPEG field.

That makes:

> **128 as an image-dimension clue**

a strong hypothesis.

## Important restraint

One number does not by itself prove:

```
width = 128
height = 128
```

The header has two independently lost low bytes.

The evidence currently supports:

- at least one intended connection between 128 and the unresolved image geometry;
- `128×128` as the simplest candidate if an independent square-image cue exists.

It does **not** yet justify filling both bytes with `0x80` merely because a square is aesthetically convenient.

## Why this could matter operationally

For the baseline `2×2 / 1×1 / 1×1` sampling shown by the SOF component descriptors, a 128×128 image would have an 8×8 MCU lattice:

```
64 MCUs
```

That is notable because the December-2025 forensic discussion independently reported “almost 64” repeated bit-pattern groups and speculated the image was near 128×128.

That observation is supportive but not yet formalized enough to use as a proof of square dimensions.

## Next exact test

Do not reconstruct pixels.

Instead:

1. audit the entropy/scan structure for a dimension-sensitive MCU/block count;
2. test 128×128 against every surviving structural byte constraint;
3. compare 128×128 with 128×N, N×128 and other 128..255 candidates;
4. only then promote exact dimensions.

This is now a much sharper JPEG-recovery lane than generic byte guessing.

# Experiment 416 — exact 64 MCUs would uniquely prove 128×128

_Status: completed conditional geometry proof, 4 Oct 2026._

Experiment 414 establishes:

```
128 <= width  <= 255
128 <= height <= 255
```

and recovers the SOF component sampling structure:

```
Y  = 2×2
Cb = 1×1
Cr = 1×1
```

That gives a 16×16-pixel maximum coding unit.

## MCU count as a dimension discriminator

For this sampling scheme:

```
MCU columns = ceil(width / 16)
MCU rows    = ceil(height / 16)
```

Within the surviving dimension range, each axis has between 8 and 16 MCUs.

The smallest possible total is therefore:

```
8 × 8 = 64
```

But there is a useful uniqueness fact.

Within `128..255`:

```
ceil(d / 16) = 8
```

only when:

```
d = 128
```

because `129` already requires 9 MCUs.

Therefore:

> **if the damaged entropy stream can be shown to contain exactly 64 MCUs, the dimensions are uniquely 128×128.**

No other width/height pair in the surviving header domain can produce 64.

## Historical connection

On 20 Dec 2025, before the footer/field connection was made, community JPEG analysis reported **almost 64** repetitions of a bit pattern interpreted as possibly empty chroma behavior and speculated that the image was near 128×128.

That observation is now much more interesting.

But “almost 64” is not an exact count and the repeated unit has not yet been formally proven to be one MCU.

So it cannot be promoted retroactively.

## Next forensic target

The JPEG-recovery lane now has a very crisp test:

1. identify the scan start and entropy grammar without guessing pixels;
2. determine whether the repeated structure is truly MCU-aligned;
3. count complete MCUs;
4. if the count is exactly 64, promote `128×128` from candidate to derived header value.

This is preferable to filling both dimension bytes with `0x80` merely because the footer says 128.

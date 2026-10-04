# Experiment 417 — the damaged JPEG scan corridor is now bounded

_Status: completed structural JPEG audit, 4 Oct 2026._

Experiment 416 reduces the exact-dimension problem to one useful question:

> are there exactly 64 MCUs?

Before attempting entropy decoding, the scan boundaries need to be recovered from the lossy text captures.

## Start of scan

Under the known corruption model, a standard three-component baseline SOS segment:

```
FF DA 00 0C
03
01 00
02 11
03 11
00 3F 00
```

appears as:

```
?? ?? 20 0C 03 01 20 02 11 03 11 20 3F 20
```

Capture B contains exactly one such sequence at normalized token 7975.

Capture P contains exactly one at token 580.

Therefore their entropy payloads begin immediately after those 14 tokens:

```
B: 7989
P:  594
```

A does not preserve this exact pattern cleanly enough because its question-mark replacement path destroys additional ASCII distinctions, but Experiment 337 already aligns A to B.

## End of image

In all three captures the ASCII footer begins with:

```
pe^!02un
```

Immediately before it are exactly two unknown normalized tokens.

That is precisely the expected damaged representation of:

```
FF D9
```

JPEG EOI, because both bytes lie in the destroyed high-byte range.

This gives a strong EOI-shaped boundary candidate directly before the footer.

For B the bounded normalized entropy corridor is therefore:

```
7989 .. 12283
```

or 4295 normalized tokens.

For P:

```
594 .. 4749
```

or 4156 normalized tokens.

The different normalized lengths reflect the already documented capture-path differences; they are not independent image sizes.

## No restart shortcut

A JPEG DRI segment would begin:

```
FF DD 00 04
```

and therefore normalize to:

```
?? ?? 20 04
```

No such DRI-shaped sequence occurs before SOS in B or P.

So the easy route:

> read restart interval → count restart markers → count MCUs

is unavailable.

## Consequence

The 128×128 question has reached a clean technical boundary.

We now know:

- SOF shape;
- sampling geometry;
- dimension domain;
- SOS location;
- likely EOI location;
- exact normalized entropy corridor;
- no restart-interval shortcut.

The next valid step is a **constraint decoder for the entropy stream** that tracks possible standard-Huffman block boundaries through known/unknown bytes without guessing pixel values.

That is a real forensic problem, not image-completion fishing.

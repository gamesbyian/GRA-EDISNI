# Experiment 410 — 9+3 serial-digit self-consumer

_Status: completed bounded in-domain consumer test, 4 Oct 2026._

Experiment 399 froze a historically proposed representation:

- first nine cells of each A-I word encode a larger binary number;
- the final three cells encode a smaller one-of-three selector.

The historical analogy was “page number plus a smaller choice inside the page.”

There is one unusually natural **sticker-native** version of that idea that does not require an external book or arbitrary modulus:

> use the large value in the same three-digit decimal format as the Collector's Edition serial numbers, then let the tail position choose one of those three decimal digits.

## Frozen operation

For each A-I class:

1. interpret the first nine marks as a binary integer with slash=1 and non-slash=0;
2. zero-pad that integer to three decimal digits;
3. take the physical one-slash tail depth `d=0,1,2`;
4. select decimal digit `d`;
5. concatenate the nine selected digits.

No digit arithmetic, keypad reduction, rotations, language scoring, or further cipher is admitted.

## Ensemble result

The operation compresses the completion families:

```
U2   648 masters -> 318 distinct nine-digit outputs
U4    20 masters ->  16 outputs
U5    14 masters ->  12 outputs
E2     2 masters ->   2 outputs
```

In alphabetic A-I order the two E2 outputs are:

```
320130397
328130397
```

In native physical `IABCDEFGH` order they are:

```
732013039
732813039
```

Again, the only disagreement is class C.

So the apparently very different numeric representation has collapsed onto the same physical uncertainty:

> residue 84 versus residue 102.

## What this buys us

This is a genuinely bounded use of the weighted completions.

It gives us a frozen answer if an external artifact later asks for:

- nine decimal digits;
- one selected decimal digit per A-I class;
- or a large-number/small-selector interface explicitly tied to CE serial formatting.

We do not need to reconstruct it after seeing the consumer.

## What it does not buy us

Neither E2 output is currently tied to an independently known downstream object.

There is no license to:

- treat it as a phone number;
- apply DTMF again;
- take moduli;
- convert to coordinates;
- search arbitrary number databases;
- or feed it into another cipher.

The exact outputs were checked against current repository/archive code search with no useful exact hit, but absence from search indexing is not evidence by itself.

## Status

Preserve as:

> a sticker-native, historically motivated 9+3 derived interface whose complete uncertainty is the same single 84/102 bit.

That makes it useful for future consumer matching, not a decode today.

# Experiment 402 — historical 3×36 Trifid replay is a hard negative

_Status: completed bounded historical replay, 4 Oct 2026._

On 30 Dec 2022, the community tried a concrete Trifid interpretation of the sticker stream.

The proposal was:

- arrange the 108 symbols as **3×36**;
- each vertical three-symbol column corresponds to one Trifid letter;
- expected output length: 36 letters.

The historical partial was reported as:

```
--cus------------h--b--ts-----------
```

That gives us a rare old hypothesis with enough frozen output to test against the modern completion ensembles.

## Cheap standard family

Do not introduce a keyword.

Use only the standard 3×3×3 alphabet cube and exhaust the representation freedoms that were genuinely unspecified:

- all 6 bijections from `- / .` to coordinate digits `1,2,3`;
- all 6 permutations of the three coordinate axes.

That is exactly:

```
36 decoder configurations
```

Run each against all:

```
648 U2 completions
```

using the historical 3×36 registration.

No language scoring is involved. A completion/configuration either reproduces the seven historically claimed letters at positions 3,4,5,18,21,24,25 or it does not.

## Result

Total survivors:

```
0
```

No U2 completion under any of the 36 cheap standard direct-cube Trifid decoders reproduces the old partial.

There is an even sharper failure.

The first two historical letters alone:

```
position 3 = C
position 4 = U
```

uniquely force, inside this cheap family:

```
- -> 1
/ -> 3
. -> 2

coordinate order -> third, first, second
```

Under that uniquely forced decoder, **every one of the 648 U2 completions** gives the 27th cube cell at position 5 rather than historical `S`.

So the conflict appears immediately at the third claimed letter.

## Interpretation

This closes the simplest faithful replay of the 2022 Trifid idea.

That is valuable because complete missing-sticker ensembles could otherwise make a 36-letter classical-cipher surface dangerously tempting.

The correct conclusion is:

> standard unkeyed direct-cube Trifid over the historical 3×36 layout is incompatible with the current broad physical completion universe and the historical partial output.

## What remains technically possible

A keyed Trifid alphabet, a nonstandard period, or full fractionation/transposition could define much larger families.

Those are not currently licensed.

Do not brute-force arbitrary Trifid keys looking for English.

Reopen only if the exact historical solver settings, key, period, or another independent Trifid cue is recovered.

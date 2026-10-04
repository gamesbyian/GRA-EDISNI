# Experiment 423 — damaged JPEG entropy does not determine the MCU count

_Status: completed exact structural constraint audit, 4 Oct 2026._

Experiment 417 bounded the surviving scan corridor and Experiment 416 established a crisp conditional:

> if the damaged JPEG can be shown to contain exactly 64 MCUs, then the independently recovered 128..255 width/height domain and 16×16 MCU geometry force 128×128.

This experiment performs the missing structural entropy test.

## Decoder

The decoder uses only the cleaner preserved **P** capture and the same loss model already frozen by Experiments 316, 337 and 417.

It does not reconstruct coefficients or pixels.

The 4,156-token entropy corridor is interpreted under these constraints:

- the baseline scan is Y 2×2 plus Cb/Cr 1×1, hence six blocks per MCU;
- the preserved DHT material is compatible with the standard JPEG Annex-K baseline Huffman tables;
- each stored U+FFFD token stands for one unknown original byte in `0x80..0xFF`;
- a stored space can represent original `0x00` or `0x20`, matching the documented text-loss path;
- entropy `0xFF` must be followed by stuffed `0x00`;
- CR/LF wrapper breaks are removed as in the existing normalized stream;
- no restart markers are introduced.

The automaton tracks only legal Huffman/block boundaries and the number of completed six-block MCUs. Amplitude bits are consumed but never decoded into coefficient values.

## Result

The loss is far too large for MCU counting.

Every complete MCU count from:

```
16 through 300 inclusive
```

has at least one entropy completion compatible with the surviving P capture.

That is **285 consecutive counts**.

The independent SOF evidence restricts each image axis to 128..255 pixels. With 16×16 MCUs, each axis therefore occupies 8..16 MCU positions. The distinct possible total MCU products are:

```
64, 72, 80, 81, 88, 90, 96, 99, 100, 104, 108,
110, 112, 117, 120, 121, 126, 128, 130, 132, 135,
140, 143, 144, 150, 154, 156, 160, 165, 168, 169,
176, 180, 182, 192, 195, 196, 208, 210, 224, 225,
240, 256
```

All **43/43** survive the entropy constraints.

So:

```
64 is feasible
64 is not unique
entropy gives zero discrimination among the geometrically possible MCU totals
```

## What this means for `128 UNSOLVED`

Experiment 416 remains mathematically correct: **if** 64 MCUs were independently established, 128×128 would follow.

Experiment 423 shows that the surviving damaged entropy stream cannot establish that premise. The old “almost 64 groups” observation therefore cannot be upgraded to an MCU count from the surviving captures.

The footer reading **128 UNSOLVED** remains unusually well aligned with the damaged SOF dimension fields, but the current evidence stops at:

> 128 is a strong source-native dimension clue, not a proved 128×128 reconstruction.

## Stopping rule

This forensic branch is now closed at the exact structural boundary.

Do not proceed by choosing replacement bytes, optimizing for a recognizable image, or guessing DCT coefficients.

Reopen only if at least one of the following appears:

1. a less-lossy capture recovers additional entropy bytes;
2. an independent artifact fixes square geometry or both axes;
3. a source clue explicitly identifies 128×128;
4. a genuinely independent JPEG field or metadata fragment narrows the dimensions further.

That is the appropriate stopping point for the `534brn` JPEG lane.

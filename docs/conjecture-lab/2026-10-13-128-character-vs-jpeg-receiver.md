# CE foreground to 128-character code, or 128-pixel receiving image?

**Date:** 13 October 2026. **Mode:** DISCOVER / DEVELOP. This deliberately explores the proposed 128-character Steam beta password rather than requiring an advance clue. No password guesses were submitted, no missing sticker observations were promoted to fact, and no hidden branch is claimed.

## Why 128 is relevant, and what it actually says

The original Terminal41 image reached from the nine sticker-backgrounds has an **upside-down footer**. Rotating `pe^!02un` through 180 degrees reads `unsolved`; reversing three neighboring dot-run lengths `8,2,1` gives `128`. These are actual source-studied facts, not a word chosen by fitting a sticker model. See [Experiments 413–414](../experiment-413-534brn-footer-128-unsolved.md) and [414](../experiment-414-534brn-128-dimension-clue.md).

The original damaged JPEG SOF0-shaped header has a native destination for the number: the two lost dimension bytes, each constrained to 128–255. Baseline 2×2 chroma-subsampled coding would have **64 MCUs if and only if the image were 128×128** in that dimension domain; [Experiment 416](../experiment-416-128-mcu-uniqueness.md) proves the implication. The exact MCU count has NOT been recovered. A 128-character password is an **additional invented interpretation of 128**, not equally strong independent evidence.

### Steam technical distinction

Valve [documents password-concealed beta branches](https://partner.steamgames.com/doc/store/application/branches) but gives no documented public maximum beta *access code* length in that reference. A 128-character code's acceptance remains **unverified**, especially on the INSIDE client/version in 2026. Historical Steam forum reports of 64-character **account-login password** issues are a different mechanism and cannot establish beta-access-code limits. Do not confuse Steam activation keys, account passwords, game-version beta codes or in-game puzzle entries. No live Steam tests were performed.

## Three explicit candidate 128-character pipelines, not invented passwords

Reproduction from the main-source data fixtures:

```sh
python scripts/conjecture_lab_128_output_consumer.py
```

The script asserts the existing **84 physical observations, 66 distinct positions and 42 unknown residues** of a 108-position cycle, reads the historically preserved 128 footer and JPEG dimensional constraints, and prints a JSON audit without printing guessed access codes.

### H128-CYCLE: 128 literal marks from the 108-symbol foreground

Read 128 consecutive cyclic foreground symbols, starting at any of 108 phase offsets. This uses the observed period, not an invented cipher. **The last 20 output characters are necessarily identical to the first 20** in this representation (positions `i` and `i+108`), regardless of phase. It contains only 108 distinct source positions, including **42 physically unresolved positions**. The extra 20 characters are deterministic repeats, not new evidence. This is a distinctive, source-derived *format prediction* for any proposed direct 128-position transcription.

The foreground consists of two visibly separated binary-looking alphabets (slash/dash in the first 81, slash/dot in the last 27), although extending that to unknown cells is conditional. One natural output mapping is `slash=1, non-slash=0`; other choices remain viable. A prospective independently identified 128-character *literal cyclic* transcript must carry the 20-character equality. This constraint does **not** apply to hashes, permutations or expansion, and cannot reject the overall Steam idea.

### H128-HEX: 128 hexadecimal characters via 512-bit digest

A standard SHA-512 digest is *exactly 128 hexadecimal characters*, since 512 bits divided into four-bit hex digits gives 128 symbols. The script shows this property using two **synthetic** completions of the missing bits and checks that each produces a 128-character digest; it deliberately does **not** output either digest as a credential or suggest that one is correct.

This possibility is computationally ordinary but adds a major **invented operation**. In particular, 128 hex characters do **not** require 512 independent sticker bits. Their entropy would remain bounded by what the 108 source positions and any external input already contain. Nothing found in the CE sources supplies SHA-512, a character-case convention, a salt, the ordering of incomplete symbols, or an accepted 128-hex-digit beta interface. So this is a constructive possibility **without evidence of intent**.

### H128-ROW: nine Q4 depth trits address a row of a hypothetical 128×128 recovered image

Under the existing **conditional one-slash-per-A-I-class Q4 model**, the nine Q4 depth selectors have **18 physical-observation-compatible** assignments. In the native physical class order `IABCDEFGH`, interpret nine base-3 digits as one big-endian integer. The values range from **4,652 to 19,250**, so **none directly indexes an image row 0..127**. A *new*, unlicensed address reduction is required.

As a deliberately generous variant, taking the integer **modulo 128** produces 18 distinct candidate rows:

```text
0, 5, 17, 23, 32, 38, 44, 50, 56,
62, 71, 77, 89, 94, 95, 110, 112, 127
```

Those numbers identify possible row *indices*, not pixels. The damaged JPEG is not yet recovered as a trustworthy 128×128 raster, so no original 128-character/binary-row candidate exists to check. A binary row would be 128 **bits** represented by 128 `0/1` characters, not a uniformly variable 128-character ASCII or alphanumeric password. It remains possible that 128 would denote **columns, geometry, width, image grid or stage number** rather than textual length. The modulo operation and grouping are speculative and should not be counted as decoder evidence.

## Exact capacity boundaries

| Proposed output object | Independent output information for arbitrary values | What an H108 binary sticker alone can provide |
|---|---:|---|
| 128 binary digits | 128 bits | At most 108 raw bits; 20 bits require redundancy/side information |
| 128 hexadecimal characters | 512 bits | Only a tiny subset of all 128-hex strings by deterministic expansion |
| 128 arbitrary ASCII bytes | 1,024 bits | Cannot encode arbitrary output without external data or structure |
| 128×128 monochrome bitmap | 16,384 bits | Must be a key/selection/reconstruction recipe, not raw bitmap data |

These bounds are **not impossibility claims** about deterministic expansion, highly structured texts, preexisting images, or a keyed output. The currently observed 66 positions reveal at most 66 binary bits before additional model constraints, not the whole 108-bit master.

## Decision and next independent tests

1. **Prioritize the image interpretation:** recover/verify an exact **64-MCU** JPEG or an authentic 128×128 original raster. That could discriminate the native dimension hypothesis independently of output-word aesthetics.
2. **Inspect an authentic Steam beta field/client or official technical definition for length/charset constraints** before upgrading the 128-character beta consumer. No login-password inference and no automated guessing.
3. **If a genuine 128-character historical input field or content line is found**, test the frozen H128-CYCLE first20/last20 periodic equality *before* fitting additional cipher transforms.
4. **If a verified 128×128 image becomes available**, test the frozen 18 Q4 candidate rows against explicitly sourced extraction rules. The modulo-128 reduction must stay tagged **invented bridge**; avoid retuning it against favorable pixels.
5. **If SHA-512 is independently cued**, recover a reproducible exact 108-bit source completion and byte-packing convention before generating a candidate. Otherwise a 128-hex output is only a mathematical demonstration.

**Disposition:** 128 is materially better grounded as a **possible damaged-JPEG dimension** than as the exact length of a Steam beta code. A 128-character target is still a worthwhile, explicit DISCOVER hypothesis, not something to forbid. No fixed hypothesis about a 128-character decoding has been positively validated.

# Experiment 337 — 534brn A/B/P exact loss-map alignment

_Date: 30 Sep 2026_

## Question

Experiment 316 established that the surviving `534brn9653f9j8mmd` captures are not four independent images. It left one exact next step:

> align the genuinely distinct A, B, and P captures while treating replacement positions as explicit unknowns.

The aim here is **byte recovery**, not image reconstruction.

## Sources

Pinned upstream repository:

- `gamesbyian/playdead-unofficial-exports`
- commit `5e5897e2ce70dad5a2bd85e459770637cb36610f`

Captures:

- A: blob `ce55c03e...`, the question-mark lossy HTML representation;
- B: blob `f12c02c4...`, the U+FFFD + HTML-wrapper representation;
- P: blob `9580913d...`, the later partial U+FFFD representation.

The script fetches the source blobs through GitHub's contents API with base64 encoding so no text decoder touches the evidence bytes.

## Conservative normalization

For alignment only:

- every A literal `?` byte is treated as an unknown token;
- every stored B/P UTF-8 `EF BF BD` replacement triple is treated as one unknown token;
- CR/LF line wrapping is removed;
- HTML entities are **not** decoded;
- no missing byte is inferred from JPEG semantics.

Known bytes are aligned using unique 12-byte anchors. Gaps between anchors use edit alignment where an unknown may match any byte, known mismatch is more expensive than insertion/deletion, and known-known disagreements are preserved.

## Pairwise result

### A against B

From `JFIF` through the shared terminal marker `pe^!02un`:

- **0 known-known conflicts**;
- A supplies **238 known bytes** at positions where B has an unknown;
- B supplies **391 known bytes** where A has an unknown;
- 1,757 aligned positions are unknown in both representations.

This establishes that A is genuinely complementary despite being lossy.

### P against B

P lacks the beginning of the JPEG-like stream. Its earliest unique 12-byte known anchor maps P token 2 to B token 7,389; from there through the shared terminal:

- **0 known-known conflicts**;
- P supplies **99 known bytes** where B is unknown;
- B supplies **99 known bytes** where P is unknown;
- 1,877 aligned positions are unknown in both.

So P is not merely a cleaner-looking duplicate. It carries exact complementary byte evidence.

## Three-capture union

Within B's JFIF-to-terminal payload span, B contains **1,995 unknown tokens** after collapsing each stored U+FFFD sequence.

Cross-capture recovery gives:

- A recovers 238 B-unknown positions;
- P recovers 99;
- their union touches 248 positions;
- A and P both recover 89 of those;
- they agree at 79;
- they disagree at 10.

Those 10 disagreements are left unknown.

Therefore the safe result is:

> **238 exact B-unknown byte positions are recoverable from the surviving alternate captures.**

The unresolved count falls from 1,995 to **1,757** within the compared payload span.

This is a hard lower bound. No JPEG grammar, entropy decoding, visual optimization, or guessed pixel was used.

## What changed

The earlier practical state was “multiple lossy representations may contain complementary information.”

That is now demonstrated quantitatively.

The next forensic stage may build a synthetic constraint stream containing:

- every B known byte;
- the 238 safely recovered exact bytes;
- explicit unknown tokens everywhere else;
- explicit conflict tokens at the 10 A/P disagreements.

Only then should JPEG structural constraints be applied.

## Reproducibility

Run:

```bash
python scripts/audit_534brn_loss_map.py
```

It writes:

`data/534brn-loss-map-summary.json`

The script is pinned to the upstream repository commit and asserts the hashes and counts above.

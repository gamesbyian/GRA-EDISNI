# Experiment 316 — exact 534brn capture-family byte forensics

_Date: 2026-09-29_

## Question

Do the multiple preserved `534brn9653f9j8mmd` files in the public Discord export contain genuinely independent damaged-image evidence, or are most of them wrapper/derivative variants of the same lossy capture?

This experiment is deliberately narrower than image recovery. It does not guess JPEG pixels. It asks what bytes are actually preserved and which historical files are duplicates or deterministic edits.

## Sources and method

Source repository:

- `gamesbyian/playdead-unofficial-exports`
- inspected commit: `5e5897e2ce70dad5a2bd85e459770637cb36610f`

The GitHub contents API was requested with `encoding=base64`, so counts below operate on the stored blob bytes rather than on a Unicode text rendering.

The content-addressed path inventory is in:

`data/discord-534brn-captures.json`

Primary unique blobs tested:

| label | blob | stored bytes | role |
|---|---|---:|---|
| A | `ce55c03e...` | 12,150 | historical `original` HTML family |
| B | `f12c02c4...` | 16,922 | historical `_1` HTML family |
| E | `35eb550d...` | 17,017 | historical `experiment` HTML |
| H | `88dca8c5...` | 16,915 | historical `hidden` HTML |
| P | `9580913d...` | 8,760 | later partial `message-*.txt` family |
| X | `b6f5ffed...` | 2,804 | preserved XMP metadata fragment |

## Exact byte counts

| capture | UTF-8 replacement triples `EF BF BD` | literal `?` bytes | CRLF pairs | NUL bytes | `&gt;` | `&lt;` | `<!--` / `-->` |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 2,152 | 68 | 0 | 0 | 0 | 0 / 0 |
| B | 2,047 | 24 | 171 | 0 | 10 | 12 | 4 / 4 |
| E | 2,047 | 24 | 177 | 0 | 10 | 12 | 4 / 4 |
| H | 2,047 | 24 | 171 | 0 | 10 | 12 | 3 / 3 |
| P | 1,976 | 20 | 24 | 0 | 0 | 0 | 0 / 0 |

This immediately separates several kinds of damage that had been discussed somewhat interchangeably.

- A did **not** preserve high bytes faithfully: it contains thousands of literal question marks instead of U+FFFD sequences.
- B/E/H preserve thousands of explicit UTF-8 replacement characters, plus HTML entities and inserted line endings.
- P avoids the HTML entity/comment layer and has far fewer line breaks, but it still contains 1,976 replacement characters. It is therefore a cleaner **partial text-path capture**, not a pristine JPEG byte stream.
- None of these stored captures contains a NUL byte.

## B and E are the same damaged payload

B and E share a 16,703-byte exact suffix.

Their first difference is in the HTML head. E changes the charset spelling and inserts a 95-byte CSS `<style>` block. The JFIF marker moves from byte 274 in B to byte 369 in E, exactly the same 95-byte offset.

From the shared wrapper point before the binary-looking content through the end, the bytes are identical.

**Conclusion:** `experiment-1a30...` is not an independent image capture. It is a presentation-wrapper variant of B and contributes no additional damaged JPEG payload bytes.

## H is exactly B with one HTML-comment delimiter pair removed

B and H have:

- a common prefix of 13,927 bytes;
- a common suffix of 2,258 bytes;
- total lengths differing by exactly 7 bytes.

B contains four `<!--` openers and four `-->` closers. H contains three of each.

Exact reconstruction succeeds by deleting from B:

- the `<!--` at byte 13,927;
- the corresponding `-->` at byte 14,661.

Those seven deleted bytes transform B **exactly** into H.

**Conclusion:** the historical `hidden` file is a deterministic HTML-display derivative of B, not an independent damaged JPEG capture.

## A is a distinct lossy transform

A has recognizable `JFIF`, `Exif`, `AnSet`, and terminal `pe^!02un` material, but its damaged-byte representation is fundamentally different:

- 2,152 literal question-mark bytes;
- no U+FFFD replacement triples;
- no HTML entity encodings;
- no HTML comment delimiters;
- the HTML document closes before the binary-looking tail.

A therefore cannot be treated as a clean raw JPEG merely because it lacks U+FFFD. The high-byte loss has simply been represented differently.

It may still contain complementary information where B's HTML parser altered ASCII-sensitive sequences, so A remains worth alignment against B/P. But its `?` positions are unknown-byte placeholders, not recovered values.

## P is the highest-value surviving partial payload, but still lossy

P begins after the SOI/EXIF area and visibly enters around JPEG quantization/Huffman structures. It:

- has no HTML wrapper;
- has no `&gt;`/`&lt;` entities;
- has no HTML comment delimiters;
- has only 24 CRLF pairs;
- still has 1,976 U+FFFD replacement characters;
- ends at byte 8,752 with literal `pe^!02un`.

This supports the July/August-2026 community description: P avoided some HTML-parser damage and spurious line wrapping, but it lacks the beginning/end and still passed through a lossy character conversion.

The separate XMP fragment X preserves structured metadata including creator `AnSet` and should be used only for deterministic metadata/header constraints, not as image-payload evidence.

## What this closes

The archive does **not** contain four independent versions of the damaged JPEG among B/E/H-style HTML files.

At minimum:

- E collapses to B plus CSS;
- H collapses to B minus one comment-delimiter pair;
- duplicated filenames within each blob family add zero evidence.

Future forensic work should therefore compare only the genuinely distinct information channels:

1. A: question-mark lossy representation;
2. B: replacement-character + HTML-parser representation;
3. P: cleaner partial text-path representation;
4. X and other metadata fragments: deterministic header/metadata constraints.

## Next exact test

Align A, B, and P with replacement positions treated as explicit unknowns rather than characters.

For every aligned byte position, classify it as:

- exact agreement;
- exact disagreement;
- unknown in A only;
- unknown in B/P only;
- HTML-entity/comment transformation;
- CR/NUL/space ambiguity;
- genuinely absent from one capture.

Only after that loss map exists should any JPEG entropy reconstruction be attempted.

## Epistemic consequence

The old shorthand “the JPG is corrupted and irrecoverable” is too coarse, while “we found a cleaner copy” is too optimistic.

The accurate state is:

> multiple lossy representations survive; most named variants are duplicates or deterministic wrapper edits; P removes important HTML damage but still contains nearly two thousand unknown-byte replacements. Exact cross-capture alignment may recover some deterministic bytes, but no current evidence supports reconstructing missing image content by guesswork.

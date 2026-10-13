# Terminal41 marked-record omission, correction and salvage: source forensics

**12 October 2026. DISCOVER source evidence; DEVELOP only for the explicitly simulated tag-filter operation. NOT a CE sticker decoder.** This is an independent original-ARG evidence lane that complements the closed-corpus parity investigation in [PR #190](https://github.com/gamesbyian/GRA-EDISNI/pull/190), the receiver atlas in [PR #201](https://github.com/gamesbyian/GRA-EDISNI/pull/201), and the weaker original-site token controls in [PR #206](https://github.com/gamesbyian/GRA-EDISNI/pull/206).

## Source and finding

The original preserved Terminal41 artifact \`terminal41.link/dat/breach_contribution_reg.html\` contains **literal authored text about marked-record omission, error correction, and data salvage**. This is a distinct source, **not** the 534brn damaged-JPEG page. The current repository archive contains an original-text copy at:

\`archive/external/twinysam-inside-arg/terminal41.link/dat/breach_contribution_reg.html\`.

Its historical source entry is pinned in \`data/terminal41-source-tree.json\` under original source-tree Git SHA \`4de72d7c2f21bd9eb4144fda51281c84cbcb90c4\`. The audit prints the current archived-copy Git blob SHA and whether it matches the original source metadata. It does not silently assume equality.

The literal source markers are:

\`\`\`text
[Omit][MARKED]
[Transmission halted - contributor reg.][-o /MARKED][-o -m "*"]
[Transmission reloaded][err. corr.(1)]
[Investigate][MARKED]
[Transmission halted - contributor reg.][-i /MARKED][-i -m "*"]
[Transmission commence(+1+)]
[DATA salvage commence -s -X -X]
\`\`\`

These **exist in an original Playdead ARG-themed source page**; they are stronger historical evidence that the author deliberately used **error-correction and selective omission terminology** than a similarity inferred from CE symbol frequency. Nevertheless, this page is authored fiction/display text. There is **no verified executable erasure-code algorithm, no parity check matrix and no demonstrated CE input**.

## Provenance/chronology gate: archived in 2023, not dated by source syntax

I checked the **original upstream GitHub path history** directly:

- Source repo: [twinysam/INSIDE-ARG](https://github.com/twinysam/INSIDE-ARG).
- `terminal41.link/dat/breach_contribution_reg.html` appears in the upstream archive-upload commit [`d0b11cf8c6462c9592bc141ee6a4dddc0a029da6`](https://github.com/twinysam/INSIDE-ARG/commit/d0b11cf8c6462c9592bc141ee6a4dddc0a029da6), **18 August 2023** (`Uploaded terminal41.link archive`).
- The `534brn9653f9j8mmd/index.html` mirror file also enters the upstream repository in that same archive-upload commit.

This dates **repository preservation**, *not* original website authorship or publication. The footer/terminal chronology and contemporary 2018 mission pages are compatible with earlier content, but **a pre-December-2019 original live page/capture witness for this particular registry has not been recovered here**. Consequently the marker/correction operation is demonstrably part of the *archived original-site material*, not proven to have been available as a CE-era clue. This is a substantive qualification on treating the page as an instruction source for stickers shipped in 2019.

## Exact stage census

The page visibly presents 64-character uppercase hexadecimal-looking records (256 raw representational bits per record), some with \`[*]\`, \`[alt]\`, \`[alt][alt]\`, or \`[/]\` suffixes. These might be hashes, random data, encrypted records or generated noise. A 64-character hexadecimal display **does not identify SHA-256** or a specific cryptosystem.

A deterministic parser segments at the page's **own authored action markers**, with **no arbitrary 108-sticker segmentation**:

| Native source stage | Displayed 64-hex records | Unique values | Star-marked | Alternate-labeled |
| --- | ---: | ---: | ---: | ---: |
| Before \`Omit MARKED\` | **68** | 66 | **7** | 4 |
| Omission/halt echo | **2** | 1 | 1 | 0 |
| After \`err. corr.(1)\` reload | **31** | 27 | 2 | 0 |
| After transmission resumes | **32** | 31 | 0 | 0 |
| **Total** | **133** | **118 overall** | **10** | **4** |

Twelve distinct 64-hex values recur, yielding 15 *extra repeated occurrences* overall. The 133 total includes one \`[/]\`-suffixed echo that a narrower asterisk/alt-only parser would otherwise miss. There are **no naturally labeled 108-site panels here**. Do not promote 133≈108+25 into a clue without further source.

## What can be replayed vs what cannot

**Nominal authored tag filter (genuinely source-licensed syntax):** the first 68 records contain exactly seven \`[*]\`-marked entries. If \`[-o /MARKED][-o -m "*"]\` is interpreted as "omit starred records", it retains **61 of 68** records. This is a directly reproducible *tag operation*, although there is no proof the original server actually ran that command.

**Identity witness at halt:** the halted display repeats the last starred first-stage 64-hex value twice, once tagged \`[*]\` and once tagged \`[/]\`. The same value thus appears with different wrappers. That is an actual source-visible *record-versus-tag separation*. It is not a parity check or repair demonstration.

**Reload chronology:** none of the seven initially starred values reappears verbatim in the post-reload or post-resume data. But some unmarked values also disappear; the later stages are not a simply filtered replay of the original first 68 records. Exactly **four distinct hex values** are common to pre-omit and post-reload stages, and exactly **one** is common to pre-omit and post-resume. Those overlaps do not prove what original bytes were corrected.

**Local edit check:** among 118 distinct 256-bit displayed values, the minimum pairwise Hamming distance is **98 of 256 bits**. The four \`[alt]\`-labeled values each have nearest *other* displayed values **102, 104, 106 and 106 bits** away. There are no immediately obvious one-bit or small-bit local alternatives in the displayed 256-bit strings. If these are actual cryptographic digests, a source-level one-character correction would of course result in a radically different digest, so this observation **does not refute** any hypothetical correction upstream.

## Direct CE class-address receiver: falsified without any missing sticker reconstruction

The registry offers **133 physical displayed records**. A cheap proposed reader would interpret each class A–I's native **nine primary body symbols** as a raw nine-bit integer (0..511), and use each integer to select one of the 133 records. The nine body positions per class are fixed by the independently physical serial/A–I cadence. The candidate reader is not original authorial instruction, so treat it as a bounded negative.

Using **only the 84 physical sticker records (66 unique H108 positions)**, leave every unobserved body mark entirely free. Test the four conventional ways to read a binary strip (serial vs reverse order; slash=1 vs dash=1) and both zero-/one-based row addressing. For each class, compute exact possible extrema from all unknown bit choices.

| Raw nine-bit reading | Physically guaranteed class values outside native 133-row range |
| --- | --- |
| Serial order, slash = 1 | **B, D, E, F, G, I** (6/9) |
| Serial order, dash = 1 | **A, C, D, E** (4/9) |
| Reversed order, slash = 1 | **B, C, D, F, G, H, I** (7/9) |
| Reversed order, dash = 1 | **B, C, H** (3/9) |

The counts apply identically to indexing 0..132 and 1..133. As a particularly concrete example, the **physically observed B-class body template is `/?//////-`**, with only one unknown body mark. Treating slash as a 1 in serial order gives **minimum binary value 382**, already above the entire 133-row address space.

### What if each nine-bit class word contains an omitted parity/check bit?

Because the page itself uses `err. corr.(1)` and `Omit MARKED` language, I also granted a *broader but still bounded* possibility: every class's nine-bit body word contains **one shared-position non-address bit**. Discard that position, interpret the other eight bits directly as a registry index, and test all **nine choices of discarded position × two serial directions × two symbol polarities = 36 configurations**.

For each combination, *unknown physical bits are free*, and a common dropped position must apply across **all nine** classes. Results:

| Bit polarity / traversal | Best of nine positions to discard | Minimum classes still guaranteed outside 133 rows |
| --- | --- | ---: |
| Forward / slash=1 | Position 1 | **2** |
| Forward / dash=1 | Position 4 | **1** |
| Reverse / slash=1 | Position 5 | **2** |
| Reverse / dash=1 | Any position 1–9 | **1** |

**Zero of 36** configurations can give valid direct registry row addresses for all nine classes. This is a stronger negative than the full nine-bit gate because it allows an arbitrary common parity/check-bit slot without using or learning that bit. Dropping more than one bit, changing bit positions per class, or applying modulo/lookup arithmetic could alter the outcome, but those extra operations have no source authorization. Nor does `err. corr.(1)` establish that *any* sticker bit is parity.

The existing [address gate script](../scripts/audit_registry_nine_bit_address_gate.py) now checks all 36 cases as well as the four original full-nine-bit conventions with frozen expected minima and synthetic controls.

**Conclusion:** No full nine-A–I direct row-address interpretation is type-compatible with this original registry under **any** of those four simple untransformed conventions, *regardless of the missing stickers*. Modulo 133, bit truncation, hashing, addressing only some classes, or using triplets instead of full nine-bit words remains logically possible, but **none is specified by this source**. Adding such a transformation merely to rescue the hypothesis would weaken it.

A separate standard-library [physical-only indexed receiver gate](../scripts/audit_registry_nine_bit_address_gate.py) runs this without POS3, U2, U5, recursion, or model-completed mark assumptions. This is a productive use of closed-corpus research: a precise impossible receiver mapping despite unresolved stickers.

## Relationship to the CE's 108-repeating sticker symbols

The page establishes a **real historical operation vocabulary**:

- *Data may be incomplete* (the page explicitly labels \`dat loss\` with several percentages).
- *Records can be marked or omitted by tag*.
- *Alternate records and exact duplicates occur*.
- *An error-correction and data-salvage stage is explicitly described*.

But do not collapse those into a theorem that Playdead used algebraic erasure coding on stickers. To promote an actual CE bridge, we still need at least one **independent native field/address** connecting a sticker's serial/symbol/A–I class to a displayed registry record, a documented parity/checksum rule, a printed operation on the CE material, or an authenticated downstream receiver.

The code's *nominal tag filtering* should nevertheless be saved as an operation family worth considering **if** the CE foreground can be independently partitioned into *payload vs marks vs control operations*. That is a narrower, historically better-grounded premise than assuming all 108 marks are raw encrypted plaintext. It does not require collecting another sticker to inspect.

**Potential source-first next checks** (do not count as evidence before performed):

1. Search original game assets and CE art for explicit \`MARKED\`, \`Omit\`, \`corr.\`, \`alt\`, \`DATA salvage\` or equivalent glyph/tag vocabulary, especially labels that fix 3×3 geometry.
2. Determine from original dated captures whether \`breach_contribution_reg.html\` was visible before CE release in 2019; source repository preservation alone does not prove contemporaneous CE-artist cross-reference.
3. Study the site's own \`-o\`/\`-i\` command convention and compare with other original pages, distinguishing generic fictional terminal syntax from actionable authored operations.
4. If a native address join appears, trial exact 66-residue and U2/U3/U5 receiver mappings **without refitting checksum parameters or ordering**. Otherwise keep this page as mechanism precedent only.

## Reproduction

\`\`\`sh
python scripts/audit_terminal41_marked_recovery.py --self-test
python scripts/audit_terminal41_marked_recovery.py --output /tmp/terminal41-marked-recovery.json
python scripts/audit_registry_nine_bit_address_gate.py --output /tmp/terminal41-direct-address-gate.json
\`\`\`

The standard-library script reads the pinned original-text copy, enumerates the natural stage breaks, distinguishes exact 64-hex strings from their suffix tags, computes identity overlaps and bounded Hamming-distance negatives, and tests a tiny deliberately constructed marked-operation positive control.

No CE serial data, parity hypothesis, source bytes, original game logic, authorial chronology claim, or existing research result is changed. Source markers are real; actual application to the stickers remains **unproven**.

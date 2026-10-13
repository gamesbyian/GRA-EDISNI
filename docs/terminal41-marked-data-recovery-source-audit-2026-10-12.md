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
\`\`\`

The standard-library script reads the pinned original-text copy, enumerates the natural stage breaks, distinguishes exact 64-hex strings from their suffix tags, computes identity overlaps and bounded Hamming-distance negatives, and tests a tiny deliberately constructed marked-operation positive control.

No CE serial data, parity hypothesis, source bytes, original game logic, authorial chronology claim, or existing research result is changed. Source markers are real; actual application to the stickers remains **unproven**.

# CL-RGB-01: literal RGB palette and channel-key preflight

**12 October 2026 | DISCOVER/DEVELOP | Frozen input: 84 physical records / 66 H108 residues | No CE decoder discovered**

## Question and capacity

Could the serial-numbered INSIDE CE stickers transmit RGB values or channel instructions for reconstructing a pre-existing image? The background class A–I is determined by serial modulo 9, so it provides position/registration, not nine independent alternatives per symbol. The observed foreground has a 108-period structure: positions 1–81 use slash/dash and positions 82–108 use slash/dot.

An *unconstrained* ternary 108-character string could carry at most 108 log2(3) ≈ 171.2 bits. Under the explicit positional grammar tested here, the first nine 3×3 frames yield **27 trits** and Q4 supplies **nine separate slash-depth selectors**. This is **36 trits ≈ 57.1 bits**, enough for six RGB triples with channel components 0–8, but not six arbitrary 24-bit RGB values.

All six historical gate-98 exact-colour keys are in the range 0–8 per component. That is an intriguing numerical fit and **not evidence** that the CE carried them.

## Fixed palette and grammar

The retrospective CL-07 reconstruction used these six authentic gate-98 colour keys and independent offsets:

| RGB key | Source offset |
|---|---|
| (3,1,1) | (16,36) |
| (1,4,1) | (1045,57) |
| (3,3,3) | (14,851) |
| (5,1,5) | (18,1638) |
| (3,3,0) | (1121,787) |
| (2,2,6) | (1155,1755) |

They are **not CE-predicted values**. Gate-98 was solved before the CE, and the six-layer reconstruction was checked against a previously known 2019 reference image. This experiment tests only a narrow, hypothetical *literal reuse* of the historical colour list.

The conditional encoding is:

1. Arrange each of the nine primary frames (residues 1–81) as **IAB/CDE/FGH**. Place one minority slash or dash per **physical column** (ICF, ADG, BEH), keeping polarity free. The minority's row 0/1/2 is one trit.
2. In Q4 (residues 82–108), each **A–I background-class depth stack** contains exactly one slash and two dots. Slash depth gives one additional trit. The final three frames **are not assumed to obey the primary minority pattern**.
3. Append the nine A–I depth trits to the 27 primary trits. Choose primary serialization frame-major or column-major.
4. Decode the 36 trits in either colour-major order (six consecutive 6-trit words) or channel-major order (three 12-trit channel planes, each with six two-trit values). A digit pair encodes a channel as either **3a+b** or **a+3b**, range 0–8. Apply one of the six global RGB channel permutations.

These **2 × 2 × 2 × 6 = 48** readout rules are the full declared family. The six historical colours are compared as an unordered set. No chosen-after-output bank, crop, per-colour permuting, scalar, arbitrary rotation, XOR, interval search, or extra transport layer is added.

## Exhaustive physical result

Input: frozen [9 October physical observations](../../data/conjecture-lab-h108-66-residue-freeze-2026-10-09.csv). No hypothesized missing stickers are inserted.

| Metric | Result |
|---|---:|
| Primary-compatible word counts, frames 1–9 | 1,1,2,1,1,3,3,1,1 |
| Primary completions | **18** |
| Q4 A–I selector options | 3,1,3,1,1,1,2,1,1 |
| Q4 completions | **18** |
| Combined conditional assignments | **324** |
| Rules per assignment | **48** |
| Total readouts | **15,552** |
| Zero target colours present | **15,276** |
| Exactly one target colour present | **276** |
| Two or more target colours present | **0** |
| Complete six-colour matches | **0** |

The lone potential colour is (3,1,1), never more than a single member of the six-colour set. Multiple completions and readout conventions are highly dependent; treating 15,552 as independent chance trials would be invalid.

The script verifies a constructive positive control: the six known colours **can** be converted to exactly 36 trits, physically encoded into a complete **108-sticker symbol cycle** respecting the primary one-minority-per-column and Q4 one-slash-per-class rules, and decoded back to their six RGB triples. This synthetic master deliberately does **not** claim to match the real observed stickers. The negative result arises from the observed physical restrictions, not insufficient capacity or a decoder unable to represent the target palette.

## Related channel-sampling control already done

An important neighbouring test exists, rather than needing to reinvent it: [CL-05's native gate-98 phase audit](2026-10-08-gate98-native-phase-positive-control.md) recovered source-grid origin (4,12), stride 16, on the **actual original gate-98 PNG**, then reused two conditional sticker machine states to address all 64 consecutive row-major 512-pixel banks and let Q4 depth select one R/G/B component. There were **zero banks with nine printable ASCII bytes** and zero banks with nine exact nonblack 0/207 palette keys; the highest per-bank nonblack count was 3/9. This is a well-defined negative of a *specific invented* 512-site bank reader, not a negative for all RGB-component address schemes.

Thus both routes now have negative controls: (A) the present **sticker-transmits-six-literal-colours** packing family and (B) the earlier **sticker-selects-nine-source-pixels-within-a-512-site-bank** lookup. A new channel hypothesis should change an operation because an independent original asset supplies it, not because an earlier readout was uninteresting.

## What the negative result does and does not say

**Ruled out inside this defined family:** direct six-colour gate-98 key transmission by the specified 36-trit positional reader, even under alternative major orders, trit endianness and global channel permutation.

**Still live:** another colour palette; a nonliteral source-cued transformation; channel selection rather than transmitted RGB values; source sampling with sticker-specified coordinates; sparse registration, mask selection, XOR/OR layers, or instructions whose values reside in an external image. No sticker foreground-to-consumer operation is identified.

The next experiment should be **source-first**: inspect the CE-background-linked damaged Terminal41 image at the /dat/534brn9653f9j8mmd/ route and identify a native nine-slot receiving surface, registration, colour keys or channel semantics **before** applying sticker values. Gate-98's independently established (4,12) phase and 16px sample stride are an authentic *historical analogue*, not a licence to invent CE banks. An open search over image regions with fitting against desirable pictures has an effectively enormous parameter budget.

A genuine image-channel consumer must specify: source byte provenance; nine positions or a native bank rule; channel assignment and alignment; a fixed readout or compositing operation; independent expected output; and matched-null controls. Preserve missing stickers as unknowns and accept outputs only if they survive alternate compatible completions or a source-specified selection mechanism.

## Reproduction

Run the standard-library script from the repository root:

    python scripts/conjecture_lab_rgb_palette_preflight.py --check-frozen
    python scripts/conjecture_lab_rgb_palette_preflight.py --check-frozen --output /tmp/rgb-preflight.json

The frozen assertion checks all key counts, and the script validates physical serial-residue consistency and within-residue agreement. Code: [RGB audit](../../scripts/conjecture_lab_rgb_palette_preflight.py). Source-positive control: [CL-07 historical six-layer reconstruction](2026-10-08-gate98-complete-six-layer-reconstruction.md).

**Status:** reproducible conditional negative; no changes to the physical ledger or the incumbent machine spec.

# CL-04: original gate-98 PNG byte-level research results

_Date: 8 October 2026. Modes: DISCOVER and DEVELOP. [Research setup](2026-10-08-native-receiver-archaeology.md). Original source [inside the archived community repository](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms/gate/98/transmission_id41786174541g1f561f4186454544fdrfd532430980980000000000000000k.png)._

**The complete original data and negative-test outputs are retained**, rather than only a remembered visual impression:

- [All 128 speculative 512-bank RGB readouts and original source colour census](../../data/conjecture-lab-gate98-exact-pixels-2026-10-08.json).
- [All 128 speculative exact-palette bank readouts and eight-colour census](../../data/conjecture-lab-gate98-cf-palette-2026-10-08.json).
- [Authenticated source analysis script](../../scripts/conjecture_lab_gate98_real_pixels.py), [unbiased lattice enrichment test](../../scripts/conjecture_lab_gate98_palette_enrichment.py), [0xCF palette counterfactual](../../scripts/conjecture_lab_gate98_cf_palette.py).
- Authenticated original-source [pixel replay workflow](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37857345114), [spatial enrichment workflow](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37857717320), and [0xCF palette workflow](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37857882404). These were one-shot, temporary PR workflows; reproducible scripts survive even if the network workflow is retired.

## Source authentication succeeded

The exact source downloaded by GitHub Actions is a `19,360,240`-byte `RGBA` PNG, 2048×4096 pixels. It matches the upstream Git **blob SHA-1** `127d8772912ffc499e5afaffe321d5bab7e920df`. Its independently calculated SHA-256 is `db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded`.

Reading the fixed, historical **(0,0) + 16-pixel stride** gives 128×256 = **32,768** sampled sites, with **19,742 distinct exact RGB colours**. All 32,768 sampled sites have alpha **255**. Black `#000000` occurs at **1,829** sampled sites. The RGB data clearly cannot be described as a three-colour, text-ready pixel table.

The original image was not added wholesale to this repo: it is already byte-preserved at the pinned community-upstream blob and is nearly 20 MB. The small replay data, content hashes and deterministic reader are saved here.

## New source-first finding: a seven-colour 3-bit RGB family at level 207

After seeing unusually frequent exact colours `#CFCF00`, `#CFCFCF`, `#00CFCF`, `#CF00CF`, etc., we **deliberately hypothesized** the full 3-bit colour palette with each R/G/B channel either 0 or **207 (0xCF)**. This was **selected after pixel inspection**, not an independently sourced command.

Every one of its seven nonblack combinations appears in the authentic image's stride-16 samples:

| 3-bit RGB | Exact colour | All sampled sites | Top 64 rows (0–63) | Last 192 rows |
|---|---|---:|---:|---:|
| 001 | `#0000CF` | 85 | 83 | 2 |
| 010 | `#00CF00` | 81 | 80 | 1 |
| 011 | `#00CFCF` | 92 | 92 | 0 |
| 100 | `#CF0000` | 77 | 77 | 0 |
| 101 | `#CF00CF` | 85 | 85 | 0 |
| 110 | `#CFCF00` | 103 | 103 | 0 |
| 111 | `#CFCFCF` | 93 | 92 | 1 |
| **All nonblack** | | **616** | **612** | **4** |

The density of these exact nonblack colours in the upper 128×64 sampled region is **459 times** their density in the other 128×192 sampled positions: `(612/8192)/(4/24576) = 459`. The source therefore contains a **strong spatially localized discrete-colour family**; this is a genuine measurement from authenticated original image bytes.

This is intriguing because the historical pixel puzzle used black plus six other **exact RGB colours** to extract seven overlays. But our observation of seven *nonblack* `0xCF` values plus black is **eight distinct candidates**. We do **not** know whether the six additional historical filter colours were exactly these, or which one would be excluded. Do not claim the historical solver's seven hex codes have been independently reconstructed.

**Critical adversarial caveat:** this is strong *upper-image regional segregation*, **not evidence that these colours occur only on the 16-pixel lattice**. A separate whole-source colour-enrichment audit found zero colours with at least eight sampled hits that were exclusive to the lattice, and measured the abundant `#CFCF00` at only ~**1.23×** the density expected from its off-grid occurrences. The 0xCF family may describe a flat-colour region of the source artwork, rather than added steganographic marks specifically on sampled coordinates. The historic 16-pixel extraction is real, but our specific 0xCF hypothesis is not thereby proven an extraction key.

## Direct sticker tests on the original pixels

The CL-02 balanced family is now verified to be the incumbent's existing `p=0,G=0` hidden-state pair, not an independent mechanism. Nine class-address values (9-bit slash=1 forward, A–I order):

```
state 0100: 302, 382, 58, 215, 311, 407, 305, 129, 357
state 1100: 302, 382, 58, 151, 311, 407, 369, 129, 357
tail depths:   1,   2,  0,   1,   0,   1,   0,   2,   2
```

The two variants' address differences are **D: -64** and **G: +64** when the hidden state flips, because their two unknown bit values lie at the same 9-bit position (bit 6). That is a structural consequence of the stickers, not a source-provided `64` instruction.

### Test 1: take one raw RGB component as an ASCII byte

Group the 128×256 sampled lattice into **64 consecutive row-major 512-site banks**. The candidate nine-bit class numbers choose one site within each bank. Q4 depth 0/1/2 provisionally selects R/G/B byte. Count printable ASCII bytes across all 64 banks for each master.

- For each master, **maximum printable characters in any nine-byte readout = 5**.
- There is **no bank** with nine printable ASCII bytes in either master.
- All 128 outputs, including their exact RGB values, bank numbers and escape/hex representations, are saved in the first fixture.

This is a **negative for the exact frozen row-major 512-bank RGB-byte-to-ASCII reader**, not a negative for source image masking or any other reader. The source never told us to use ASCII.

### Test 2: use 0xCF three-bit colour classes as the output alphabet

For each sampled pixel, accept only `RGB ∈ {0,207}³` and let Q4 depth choose the corresponding bit. Across **all 64 banks**, neither candidate supplies nine exact-palette site matches:

- In **both** masters, the largest *nonblack* code-colour count in any nine-site readout is **3/9**, at bank 9, involving A=`#CF00CF`, B=`#CF0000`, and H=`#CFCFCF`.
- Counting black as an eighth legitimate palette value would misleadingly increase the maximum to **7/9**, but that occurs at bank 63 dominated by **ordinary black background** and does not encode seven distinct information-bearing marks. **Black is abundant outside the special upper image region** (1767/1829 black grid hits are below row 63).
- The palette script retains every bank's exact source RGB values and class-specific Q4 bit output; the entire result is saved in the second fixture.

This is an **exact negative for the specific invented 512-bank/3-bit colour lookup requiring all nine positions to be palette-marked**. It also illustrates why a visually compelling partial hit must be compared against the actual background's palette distribution rather than selectively counted.

## What we learned and what survives

**Source-first gains:** we have now actually inspected an original, byte-authenticated ARG receiving-artifact candidate at pixel level; the source has a real spatial 16-pixel extraction history and a sharply segregated seven-nonblack-colour cube. Two transparent, complete speculative nine-address readers can be checked and both fail their predeclared full-read conditions. No new sticker physical observations were introduced.

**Unresolved bridge:** the *original artwork* has not provided an authorial bank `0..63`, A–I-to-pixel indexing, Q4-to-channel binding, alphabet mapping, or CE-era checkable response. The source predates the CE. Its authentic three-bit colour properties make it a worthwhile operation analogue, **not a confirmed receiver**.

**Next step:** recover the exact *historical seven RGB selection values and crop bounds* from primary Discord-source attachments, using only the 2018 material to lock those parameters. Reproduce the already-known gate-98 route extraction on authentic pixels as a **positive control**. Only then ask whether the sticker code can act as a second-stage key, with separate frozen predictions and matched nulls. In parallel the physically linked damaged `534brn` page remains a better *destination* than gate-98, despite its missing reader.

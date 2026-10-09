# CL-08: can original gate-98 panels register themselves without the 2019 answer?

**8 October 2026 | Negative result for a strict, testable source-only operation**

[CL-07](2026-10-08-gate98-complete-six-layer-reconstruction.md) exactly recreates **all 2,577** bright-pixel sites in a dated June 2019 Game Detectives solved-image witness, using six exact RGB colour layers and separately translated source coordinate sets from the byte-authenticated 2048×4096 Playdead gate-98 PNG.

But those six offsets were *found while looking at the already decoded witness*. CL-07 is an authentic **historical positive control**, not a source-blind registration mechanism. The next question is whether the **original source-image alone** can select those offsets by simple, natural **overlap maximization**.

## Protocol, with leakage boundary

The six RGB values here are already known from the solved image. Their **selection was target-assisted**. The narrower source-only part of this test is the *registration score*, which only reads raw colour positions from the original PNG:

1. For each colour, read **every exact RGB pixel** in the original source. The source SHA-256 is `db67f13634004b8f3914aae6e06bd40f01e4f71531d689603d0f1f3be2a99ded`.
2. Select only pixels at that colour's strongest **source-derived 16×16 phase**. Six source-native phase-and-cardinality checks are frozen. These are independent of the historical reference's text pixels (although candidate colours came from that reference).
3. For each pair, build a histogram of source coordinate differences `(x_B-x_A,y_B-y_A)` over **every 1,002,001** shifts in `dx=[600,1600]`, `dy=[-500,500]`. This coarse rectangle captures the source's two-column arrangement without using the correct exact offsets.
4. Rank all 1,002,001 proposed alignments by the **number of coincident original source marks**, without looking at the 2019 image.
5. Only **after** constructing the source-only histogram, query the historical *known-correct* relative displacement determined by CL-07. It had no part in scoring.

Frozen source-native colour phases and selected-site counts:

| Colour | (x mod 16,y mod 16) | Phase-only pixels |
| --- | --- | ---: |
| `#030101` | (4,12) | 121 |
| `#010401` | (9,1) | 325 |
| `#030303` | (2,11) | 176 |
| `#050105` | (3,12) | 432 |
| `#030300` | (5,11) | 735 |
| `#020206` | (4,1) | 396 |

This excludes colour-matched artwork at all other phases. The source has **62,958** ordinary `#050105` pixels and **58,006** `#030300` pixels across the whole original picture; taking all those without phase filtering makes raw registration even more vulnerable to accidental matches. Only the phase-filtered controls form the primary test.

## Exhaustive displacement controls

| Original colour pair (A → B) | Correct historical delta (B minus A) | Original-source overlap at correct delta | **Shifts scoring strictly better** | Best *wrong* delta / overlap |
| --- | --- | ---: | ---: | --- |
| `#050105` → `#020206` | (+1137,+117) | 52 | **136** | (+1201,+133) / 88 |
| `#030303` → `#030300` | (+1107,−64) | 24 | **1,148** | (+1155,−256) / 65 |
| `#030101` → `#010401` | (+1029,+21) | 5 | **2,233** | (+917,+37) / 59 |

All top wrong offsets are in the same original-source search rectangle, and all obey the corresponding source phase difference modulo 16. The plausible sharp 16-pixel registration peaks therefore **cannot choose which multiple-of-16 shift is correct**.

The same experiment **without** phase filtering gave, respectively, **136 / 1,184 / 2,239** translations scoring strictly better than the correct historical ones. Restricting to the actual source-native 16px phases improves some ranks only marginally. Selecting the wrong shift by maximizing overlapping dark dots is not a valid reproduction of the historic authored operation.

Frozen code and data: [source-only registration script](../../scripts/conjecture_lab_gate98_source_only_alignments.py) and [source phase/shift evaluation fixture](../../data/conjecture-lab-gate98-source-only-registration-control-2026-10-08.json). The standard-library fixture validator can run without source bytes; full pixel replay accepts `--source` and NumPy/Pillow, and does *not* load the 2019 witness:

```bash
python scripts/conjecture_lab_gate98_source_only_alignments.py
python scripts/conjecture_lab_gate98_source_only_alignments.py --source /path/to/byte-pinned-gate98.png
```

## What was and was not disproven

**Narrow, real negative:** Given the six historical exact RGB colours, original-source native 16px colour-phase selection, and the broad 2-column displacement search range, **maximizing pairwise exact pixel overlap fails to recover the correct translations** in all three predeclared pairs. Source-native colour phases can specify a **congruence class modulo 16** but fail to specify an **absolute output registration**.

This *does not* falsify CL-07's full six-layer image reconstruction, which was proved by comparison to an authentic, independently dated historical image. It does *not* refute more sophisticated spatial, typography, or source-metadata cues if new **independent, source-fixed rules** emerge. It certainly does not prove anything about a CE sticker foreground transformation.

**Research lesson:** recovering how Playdead's earlier image can be reconstructed retrospectively does not by itself tell us how its original solvers were meant to find that reconstruction. Fitted colours and offsets are useful provenance-backed exemplars but **must not silently become sticker-decoder premises**.

## Next investigation priority

Search for a contemporary 2018 pixel-layer extraction walkthrough, dated screenshot showing original paint-program selection boundaries, source authorial metadata, or original registration instructions. In the CE domain, demand **a sticker-native or `534brn`-native registration rule** rather than trying arbitrary shuffles of A–I until letter shapes emerge. Treat the two source phase congruence classes and six observed panels as a documented **operation class**, not a uniquely determined mechanism transferable to nine sticker tiles.

**Conclusion:** Historical 2019 gate-98 text is fully reproduced as a bright binary image; source-only pairwise translation matching does **not** recover the alignment key. That missing key is the real intellectual frontier.

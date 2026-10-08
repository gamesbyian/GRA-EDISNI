# Experiment 457: shifted-versus-exact cube coordinates

Discord reports: same coordinate 52% vs 40–44% random; +X 24% vs 31–38%; +Y 41%; +Z 35%. Direct same-versus-X contrast was reported at p=0.001–0.013. Those numbers are from the community, not independently reproduced here.

## Independent strict null (current 66 residue corpus)

The updated physical observation ledger gives 33/64 exact corresponding-coordinate matches, consistent with the earlier exact restricted-shuffle audit.

For each physical 3×3 grid IAB/CDE/FGH, compare a source to either the identical coordinate or its shifted target *on exactly the same subset of source observations with both targets known*. Permute every observed symbol independently within its (cube, A–I class) depth stack while preserving each stack's observed colour multiset and exact missing-value mask. Exactly 331,776 joint shuffles exist.

The following tail fractions use the **difference in matched-pair counts** between exact and shifted coordinates. They are exact enumerations under that null, not significance corrected for selecting comparisons after exploration.

| Shift under explicit physical coordinate convention | Wrap? | Shared observations | Exact matches | Shift matches | Difference | Tail fraction |
|---|---|---:|---:|---:|---:|---:|
| Physical row +1 | No | 23 | 15 | 9 | +6 | 0.016397 |
| Physical row +1 | Yes | 36 | 19 | 13 | +6 | 0.035940 |
| Physical column +1 | No | 20 | 9 | 3 | +6 | 0.031250 |
| Physical column +1 | Yes | 41 | 20 | 15 | +5 | 0.229408 |
| Depth +1 | No | 27 | 18 | 11 | +7 | 0.070240 |
| Depth +1 | Yes | 37 | 21 | 15 | +6 | 0.104420 |

These results were computed by an independent full 331,776-shuffle enumeration on the 84 physical record / 66 residue CSV. The Discord-reported 24% +X shifted match rate is **not** reproduced by these straightforward XY conventions; the source author's exact shift/index formula, coordinate registration and edge-wrapping convention are still needed.

### What follows

The within-same-support exact-versus-shift contrast appears for some coordinate rules, especially positive row or nonwrapped column, but not all. A strong unconditional "registration" conclusion would overstate this because:

1. Several shift directions and wrap conventions are effectively separate tests.
2. Matching observations differ when comparing raw shifted percentages unless the intersection mask is enforced.
3. Preserving cube-by-letter colour counts does not preserve the complete primary frame's physical-column grammar.
4. Both completion-selection and the tested transform family were developed after seeing these 65–66 observed residues.

Do not confuse 0.0164 with a post-selection corrected p-value, or treat nonmatching coordinate conventions as a direct refutation of the Discord calculations.

### Next discriminating input

Request the exact transformation mapping each 1-based H108 residue in one cube to its shifted comparison residue in another cube, with a statement of whether 3×3 boundaries wrap and whether shifted pairs are counted in both directions. Then re-run:

- exact community geometry on the current 66-residue observation mask;
- exact strict within-(cube,letter) null;
- one-minority-per-column completed-master null on exactly the same support;
- simultaneous family-wise max-statistic across all four declared shifted operators;
- Q1–Q3-only analysis to avoid confusing primary slash/dash with tail slash/dot.

Current result: narrowed structural test, not a solved 3D arrangement or new readout.

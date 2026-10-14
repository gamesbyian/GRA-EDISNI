# Discord row-order visual search (14 October 2026)

DISCOVER only: these are heuristic image candidates, not a decoded image. Row order is changed, never individual cells; white is unknown and excluded from adjacent-colour scoring.

The screenshot shows the 108 positions from sticker residue 1. Two yellow positions exceed the older community transcription after correcting its zero-index phase: residue **103**, now confirmed via sticker 427, and residue **45**, *unconfirmed in the repository's physical observation ledger*. Verified-only views mask residue 45. The as-shown variants retain the screenshot exactly.

## Visual galleries (GitHub viewable SVG)

- [Verified 12×9](verified-12x9.svg)
- [Verified 9×12](verified-9x12.svg)
- [As pictured 12×9](as-shown-12x9.svg)
- [As pictured 9×12](as-shown-9x12.svg)

These SVGs are self-contained browser-viewable candidate galleries: original ordering, and dynamic-programming-optimal ordering under three simple seam objectives (same-colour matching, rarity-weighted matching, and aligned colour-edge continuity). Their objective implementations are *illustrative follow-on renderings* and are not pixel-identical to the independent local PNG contact sheets.

## Original longer quantitative experiment

The local experiment (not yet reproduced by CI in this branch) used exact Held-Karp optimization on all 9! or 12! orders, plus 500 row-mask/census-preserving randomized-control optimizations per verified shape. Its weighted-objective maxima were 35.70 (12×9) and 21.85 (9×12), against matched-control means 36.05 and 27.31; respectively 53.3% and 89.0% of controls equalled or exceeded the real maxima. The as-pictured test with 250 controls gave 55.0% and 97.2%. No recognizable image was identified. These numbers are historical outputs of the local run and **are not scores of the SVG gallery's separately implemented objectives**.

Pre-existing relevant experiments in [the experiment ledger](../../experiment-ledger.md): **345, 347, 360, 362, 363**. They show nonexceptional sticker row continuity and demonstrate on Playdead's solved acorn puzzle that maximally coherent orders may still be wrong.

## Questions for the Discord

1. What is the provenance of residue **045** marked yellow? Owner confirmation, fitted prediction, or chart error?
2. Is there an independent ordering cue, shape, outline, visual target, or side/margin signal worth using instead of generic same-colour continuity?

Source remains the physically supported ledger in `data/observations.csv`; the gallery has **not** changed that ledger.

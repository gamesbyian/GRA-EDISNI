# Experiment 325 — Physical edge-channel observability audit

_Status: completed R2 fail-closed audit, 30 Sep 2026._

## Question

R2 asked whether the canonical A-I background masters contain a sticker-native edge or margin channel analogous to the PC printer puzzle's side/check-bit marks.

Before measuring edge patterns, the first question is simpler:

> Do the current master products actually preserve the **physical sticker perimeter** needed to test that hypothesis?

## Consensus masters

The canonical consensus builder first rectifies a detected sticker quadrilateral to a square canvas, then deliberately crops the common background-print field:

```python
x = 10% .. 90%
y = 12% .. 76%
```

The stated purpose is to exclude the serial area and reconstruct the shared faint background artwork while masking the large foreground symbol.

Therefore the consensus masters discard:

- the outer 10% on both left and right;
- the outer 12% at the top;
- the lower 24% of the rectified sticker;
- the serial region;
- the actual physical sticker boundary.

Their `*-support.png` files answer an important question, but only **inside that cropped artwork field**: which reconstructed artwork pixels are supported by accepted photographs.

They cannot tell us whether the original sticker perimeter contains side marks, margin check-bits, wrapper registration features, or other boundary metadata.

## Historical 846shEE evidence masters

The evidence-preserving masters do not solve this problem either.

They are cropped from the already assembled historical `846shEE` composite using measured cell boundaries. Their transparency masks correctly preserve which **background artwork** pixels are directly visible beneath the historical foreground symbols and labels.

But those crop edges are boundaries in a solved composite. They are not the original physical margins of nine separate stickers.

So they are excellent evidence for the A-I artwork itself and poor evidence for a physical edge channel.

## Existing seam result

The archived seam metrics remain valuable:

- coarse canonical percentile: 92.98%;
- medium: 99.91%;
- fine: 99.98%;
- edge: **99.998%** among 3x3 permutations.

That is extremely strong support for the canonical `IAB/CDE/FGH` artwork assembly.

It does **not** establish a second check-bit layer. The metric measures ordinary image continuity between artwork tiles.

## Result

**The current canonical master products cannot validly test a PC-style physical edge/check-bit hypothesis.**

This is a fail-closed result, not evidence that no such channel exists.

Running edge detectors, binary thresholds, or pattern searches on the master borders would answer the wrong question because those borders were created by the reconstruction crop.

## Correct next experiment

A valid physical-edge audit must return to the manifest-authorized original photographs and use a different preprocessing path:

1. detect and rectify the full sticker quadrilateral;
2. preserve the physical perimeter;
3. preregister a narrow perimeter band before looking for marks;
4. keep serial text and foreground-symbol masks separate from that band;
5. measure direct photographic support for each edge;
6. test repeatability across independent stickers of the same A-I class;
7. distinguish stable edge features from the already-known continuous background artwork;
8. fail closed where perspective, glare, crop loss, or support is insufficient.

No inpainted master pixel should enter that test.

## R2 consequence

The existing R2 phrase “support-mask-aware master-edge analysis” was too optimistic. The masters are support-aware, but their edge is not the physical sticker edge.

The valid follow-up is now:

> **full-photo physical-perimeter audit with support accounting.**

Until that is done, the repository should classify a PC-style sticker edge/check-bit channel as **unmeasured**, not absent and not supported.

Machine-readable disposition:

`data/edge-channel-observability.json`

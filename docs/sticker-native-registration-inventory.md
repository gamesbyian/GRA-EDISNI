# Sticker-Native Registration and Side-Channel Inventory

_Status: R2 initial inventory, 30 Sep 2026._

## Purpose

Identify every **directly observed** sticker-native channel that could constrain ordering, registration, selection, masking, or layered interpretation of the foreground.

No model-predicted foreground cell is used here.

## 1. Serial number

Every physical sticker carries a serial number.

Observed role already established:

- serial phase determines the repeating A-I background class;
- physical observations support a short foreground recurrence of 108.

Potential registration role:

- absolute serial;
- serial modulo 108;
- serial modulo 9;
- relative order among pooled stickers.

Constraint strength: **high**, because it is printed on the object.

Open question: does authorial intent use serials only to align repeated material, or as an actual address/index into a second structure?

## 2. A-I faint background image class

The nine background image classes cycle with serial phase and assemble in the historically recovered physical arrangement:

```
I A B
C D E
F G H
```

This is a solved layer of the **same physical sticker**.

The newly committed evidence-preserving masters and consensus masters make this layer directly inspectable without inventing hidden pixels.

Important evidence:

- `artifacts/background-tile-evidence-masters/` preserves only pixels directly visible in the historical 846shEE reconstruction;
- `artifacts/background-tile-masters/` gives consensus reconstructions with support and inpainting masks;
- the historical canonical 3x3 assembly has exceptionally strong seam continuity in the archived seam audit. The existing metrics report canonical percentiles of 92.98% (coarse), 99.91% (medium), 99.98% (fine), and 99.998% (edge) among 3x3 permutations.

Reset interpretation:

The background is not generic decoration. It is a demonstrated spatial carrier with a known orientation.

What is **not** yet established is whether the solved background layer also tells us how to order or operate on the foreground.

## 3. The 81 / 27 alphabet boundary

Across the 108 foreground positions:

- residues 1–81 use slash/dash;
- residues 82–108 use slash/dot.

This is a direct observation-level asymmetry.

Historically, solvers noticed it and proposed:

- checksum/error-correction roles;
- barrier/visual-aid roles;
- a separate second stage;
- a 9+3 layered encoding where the smaller part selects within the larger part.

This is currently the strongest sticker-native candidate for an analogue of the PC puzzle's side/check-bit channel.

It establishes that the final 27 positions are **different in kind**.

It does not establish what operation they perform.

## 4. Per-background-class 9+3 traces

Because each A-I class recurs every nine serial positions, each background class naturally owns twelve H108 residues:

- first nine in the slash/dash body;
- final three in the slash/dot tail.

This is exactly the historical May-2026 9+3 decomposition, expressed without any machine interpretation.

Observation-only traces:

| Class | body residues | observed body | tail residues | observed tail |
|---|---|---|---|---|
| A | 1,10,19,28,37,46,55,64,73 | ?--?-/??? | 82,91,100 | ??? |
| B | 2,11,20,29,38,47,56,65,74 | /?//////- | 83,92,101 | ?./ |
| C | 3,12,21,30,39,48,57,66,75 | ---///-/- | 84,93,102 | ??? |
| D | 4,13,22,31,40,49,58,67,76 | -/?-/???/ | 85,94,103 | .?? |
| E | 5,14,23,32,41,50,59,68,77 | /--/??/?? | 86,95,104 | /.? |
| F | 6,15,24,33,42,51,60,69,78 | ?/-?/-/// | 87,96,105 | ?/? |
| G | 7,16,25,34,43,52,61,70,79 | /???/??-/ | 88,97,106 | ?.? |
| H | 8,17,26,35,44,53,62,71,80 | ?/-?--?-/ | 89,98,107 | ..? |
| I | 9,18,27,36,45,54,63,72,81 | /-?/??/-/ | 90,99,108 | .?/ |

The table is intentionally sparse. Question marks mean no physical foreground observation at that residue.

Two points stand out without importing any model:

1. the 9+3 split is aligned exactly with the A-I cycle;
2. the tail is much more sparsely observed than the body, including entirely unobserved A and C tail triples.

That means any tail-based interpretation must be judged carefully for underdetermination.

## 5. Physical 3x3 background position

A-I is not merely a label sequence. Each class has a recovered physical cell in the 3x3 printer image.

Therefore every foreground observation has an independently known spatial coordinate inherited from its background class.

Possible uses that are legitimate to test:

- ordering rows/columns by the solved background geometry;
- treating foreground marks as a second layer drawn over the same 3x3 carrier;
- asking whether boundary/edge cells have a special role;
- testing whether tail marks reference background locations.

Illegitimate shortcut:

- choosing a transform because it makes the current machine look clean.

## 6. Foreground symbol shape itself

The marks are literally slash, dash, and dot, not abstract colors.

Historical solvers explicitly warned that rendering them as colors could hide why Playdead chose those shapes.

Potential physical information includes:

- orientation of slash;
- horizontal dash;
- point/dot;
- line versus point;
- directionality or geometry.

No special semantics are currently established.

This channel should be tested before reducing everything to arbitrary categorical values.

## 7. Packaging orientation and placement

The sticker sealed the black paper/wrapper around the game.

This gives the sticker a physical orientation and context, but current project evidence does not yet establish that:

- rotation relative to the package is consistent enough to encode information;
- sticker placement varies meaningfully;
- wrapper edges provide a repeatable registration mark.

Status: **possible but currently weak**. Do not promote without measurements from original photographs.

## 8. Tile edges, seams, crop geometry, and print registration

The new masters make it possible to inspect:

- artwork continuation across canonical A-I seams;
- whether any printed border/edge feature is shared between classes;
- whether foreground placement is registered to the same local artwork coordinate system;
- whether crop/print offsets carry repeatable information.

Current documentation establishes strong canonical image continuity but does not yet identify a second independent margin/check-bit layer on the stickers.

This is a direct R2 follow-up target.

## 9. Repetition / overlap agreement

Multiple physical serials sometimes occupy the same H108 residue and agree on foreground symbol.

This supplies:

- registration validation;
- repeat-cycle evidence;
- error detection.

It does not by itself define an ordering transform.

## 10. Channels deliberately excluded from R2

These are not observation-native:

- POS3 values;
- Q4 selector depths;
- hidden-state bits;
- route words;
- terminal `100`;
- prediction-matrix fills;
- gauge choices;
- model-derived completions.

They may later be tested **against** a side-channel hypothesis, but they cannot supply its initial cue.

## R2 provisional ranking by evidentiary independence

### Strongest

1. serial phase / mod-9 A-I alignment;
2. solved physical A-I 3x3 geometry;
3. 81/27 symbol-alphabet boundary;
4. literal slash/dash/dot shapes.

### Strong but mainly validation

5. H108 repeats and overlap agreement;
6. seam continuity of the solved background assembly.

### Plausible but not yet demonstrated

7. packaging orientation;
8. foreground placement relative to local background artwork;
9. print/crop edge features.

## Immediate tests unlocked

### R2.1 — background-position overlay

For each of the twelve serial layers over A-I, plot only physically observed foreground marks onto the solved 3x3 background coordinates.

Goal: look for registration/boundary regularities without filling unknowns.

### R2.2 — tail-as-metadata tests

Treat each class's final three observed/unknown cells as metadata about its preceding nine cells and test simple roles:

- select one of three rows;
- select one of three columns;
- select one of three 3-cell rails;
- choose orientation/rotation;
- choose one of three masks.

Do not require POS3 or recursion.

### R2.3 — literal-symbol geometry

Test operations using slash orientation, dash orientation, and dot as point/stop without first mapping them to arbitrary digits.

### R2.4 — physical-edge audit

Experiment 325 shows the consensus masters cannot answer this question: their reconstruction crop intentionally removes the physical sticker perimeter, and the 846shEE evidence-master edges are boundaries of an already assembled artwork composite.

The valid test must return to manifest-authorized original photographs, rectify the full sticker quadrilateral, preserve a preregistered perimeter band, and track photographic support directly. Fail closed where crop, perspective, glare, or registration prevents edge recovery. See `docs/experiment-325-edge-channel-observability.md`.

## R2 conclusion

The reset now has a concrete candidate analogue for historical side/check-bit metadata:

> **the slash/dot tail aligned to the already-solved A-I spatial carrier.**

That is only a candidate role. The next work should test low-description operations by which those three per-class tail positions could constrain or select something in the preceding nine body positions, without importing the incumbent machine's exceptional-position or recursive assumptions.

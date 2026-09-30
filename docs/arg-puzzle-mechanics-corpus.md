# INSIDE ARG Puzzle-Mechanics Corpus

_Status: initial reset corpus. Extend from primary/archived sources, not analogy alone._

This document records **operations that demonstrably solved or materially advanced other INSIDE ARG components**. It is intended to constrain what counts as a Playdead-plausible move while preventing cargo-cult reuse of old tricks.

## Operation families already demonstrated

### Metadata-driven ordering

The iOS printer emitted pieces whose hour-of-day metadata supplied their order. Correct ordering reconstructed 5x5 glyphs and a phrase.

**Reusable lesson:** metadata outside the apparent payload may define sequence order.

**Do not infer:** that serial order is wrong merely because another puzzle needed reordering.

### Boundary/check-bit constrained permutation

The PC printer/acorn work used sparse side marks to constrain row ordering. Historical discussion explicitly describes the sides as the feature that made the arrangement possible and as check-bits. The rearranged object exposed an acorn and 41.

**Reusable lesson:** margin structure can be functional registration metadata.

**Sticker-specific question:** does any independently observed sticker/background/packaging feature play the role of a side channel?

### Geometry first, interpretation second

The Xbox printer required an intended spatial arrangement before a secondary dash layer became readable as Braille.

The CE's own background puzzle likewise required assembling nine faint image classes before the printer/path image became legible.

**Reusable lesson:** a mark stream can be secondary to a physical/spatial carrier.

### Code as operation

The Switch printer produced an instruction that became a sequence of physical controller connection/disconnection actions.

**Reusable lesson:** intermediate output need not be prose. It can specify what to do next.

### Prior-stage output as selector

Terminal 41 exact-RGB filtering reused values produced by an earlier stage to select image layers.

**Reusable lesson:** cross-puzzle information flow is real when the earlier stage supplies exact parameters.

### Externally cued generative transform

The PC object exposed an acorn and 41; the acorn is a named Game of Life seed and 41 specifies the generation. A later construction used that generated state in an overlay.

**Reusable lesson:** highly nontrivial transforms can be intended when the artifact itself supplies both transform identity and parameter.

**Do not infer:** permission to try Life or arbitrary cellular automata on unrelated material.

### In-world reference as overlay key

The macOS line used an E. E. Cummings reference as the text source, with puzzle marks selecting letters.

**Reusable lesson:** lore/reference material can be payload-bearing if the puzzle points to a specific source.

### Carrier conversion

Historical ARG work includes image-to-audio/spectrogram style transitions and later game-file evidence of audio/image dual use.

**Reusable lesson:** media type is not sacred.

**Sticker relevance:** low until a sticker-native cue asks for a carrier conversion.

## Recurring design grammar

The solved cases support a recurring sequence:

1. identify the carrier or ordering metadata;
2. reconstruct/register an intended object;
3. read a second layer only after registration;
4. obtain a phrase, path, selector, instruction, or transform cue;
5. feed that output into a later artifact or operation.

This pattern is a design prior, not a decoder.

## Sticker-specific candidate consumer: secret-ending lever

The 21 Mar 2021 public sticker discussion supplies a candidate consumer from outside the foreground corpus itself.

The Collector's Edition sleeve was historically interpreted as displaying the same three marks in the geometry of the secret-ending lever:

```
dot left
dash right
slash top
```

That yields the concrete command mapping:

```
. = left
- = right
/ = up
```

This is **not a solved puzzle component** and should not be placed in the table of demonstrated historical techniques. It is, however, exactly the kind of external cue the reset asks for: a separate artifact supplies a semantic type and a three-way operation without consulting the current machine.

Experiment 342 closes only the cheapest direct replay of the known normal bunker password. The broader question, whether a separately cued ordering/subset of sticker marks forms a lever sequence, remains licensed.

## Implications for the sticker foreground

Highest-priority questions now become:

1. Is the A-I background layer merely already-solved decoration, or also registration metadata for the foreground?
2. Does the foreground contain a boundary/order channel analogous to PC side marks?
3. Is 108 intended as a flat cyclic code, twelve 3x3 objects, four groups of 27, nine columns of 12, or an arrangement selected by another artifact?
4. Does the slash/dot tail encode an operation on the slash/dash body, and can that be motivated without POS3?
5. Does `dat/534brn9653f9j8mmd` or another background-layer output supply a key, ordering, orientation, or consumer for the foreground?
6. Did community solvers already articulate one of these relationships before the present machine model?
7. What exact information would an original owner, versus the pooled community, have possessed?

## Evidence rule for cross-puzzle transfer

A historical mechanism may increase the prior for an operation class. It may not supply missing parameters.

For example:

- "Playdead used row permutations before" makes a sticker-native row-order cue worth seeking.
- It does not justify testing all row permutations for the prettiest output.
- "Playdead used Game of Life before" makes an explicit Life/acorn clue meaningful.
- It does not justify cellular-automaton fishing.
- "Playdead reused prior outputs as selectors" makes exact cross-artifact correspondences important.
- It does not justify treating arbitrary previous answers as keys.

## Source trail already in-repo

Start from:

- `docs/discord-historical-technique-inventory.md`
- `docs/human-solve-reconstruction.md`
- `docs/community-conventions.md`
- `archive/external/bigdusty/puzzles/`
- `archive/external/twinysam-inside-arg/`
- `archive/discord/2026-09-29/`

For every new mechanics entry, preserve the underlying message, screenshot, file, or upstream document whenever possible.

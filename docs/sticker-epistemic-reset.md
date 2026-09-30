# Sticker Mystery Epistemic Reset

_Status: active workstream, 30 Sep 2026._

## Why this reset exists

The project has accumulated a highly structured mechanical interpretation of the sticker foreground. That work remains valuable evidence, but it must no longer organize the search by default.

Newly imported community history changes the prior. Other INSIDE ARG components were often solved by:

- recovering an intended geometry before interpreting payload;
- using side or margin marks to constrain ordering;
- reusing outputs from one stage as selectors or keys for another;
- applying externally cued transforms such as a Game of Life seed/generation;
- treating an apparent code as an instruction or routing operation rather than plaintext;
- combining physical, temporal, platform, or in-world metadata with the raw marks.

The foreground model must therefore compete against simpler and historically demonstrated Playdead puzzle grammars.

## Reset rule

Until this workstream closes, distinguish four layers rigorously.

### Layer 0 — direct sticker facts

Admit only things that can be read directly from physical/public sticker evidence or from a source artifact whose provenance is explicit.

Current examples:

- sticker number;
- foreground mark slash, dash, or dot;
- faint A-I background image class;
- the A-I background cycle with serial number;
- the physical A-I assembly recovered by the community;
- repeated sticker observations at the same H108 residue;
- the observed slash/dash versus slash/dot alphabet split;
- source, date, image provenance, packaging context.

Do not use machine vocabulary in Layer 0.

### Layer 1 — community-attested operations and historical observations

Record what solvers actually tried or successfully used, separately from whether the operation is valid for the sticker foreground.

Examples already attested in the archive:

- sorting/reordering rows;
- using edge/margin marks as check-bits for row order;
- reconstructing spatial images before decoding;
- arranging 108 foreground positions as twelve 3x3 squares;
- separating the first 81 positions from the final 27;
- comparing the sticker problem to the acorn/printer puzzle;
- treating repeated image classes as a spatial carrier;
- trying shifts, intervals, Braille, and predictive filling.

A historical attempt is evidence about discoverability and Playdead-specific priors, not evidence that the same operation is correct here.

### Layer 2 — candidate puzzle grammars

Competing explanations belong here. No family receives incumbent status merely because the repo already contains more machinery for it.

Minimum live families:

1. spatial assembly / image reconstruction;
2. ordering or permutation constrained by side information;
3. layered registration followed by secondary-symbol decoding;
4. serial/index/address lookup;
5. positional ternary or other local coding;
6. recursive selection/routing;
7. cross-puzzle keying or selector reuse;
8. externally cued generative transform;
9. physical/manufacturing organization that is puzzle-relevant;
10. hybrids of the above.

The present POS3/selector/recursive machine is one member of this layer.

### Layer 3 — consequences of a chosen model

Predicted unseen symbols, hidden states, gauges, route shells, terminal 100, arbiter interpretations, and similar constructs live here.

They can test a model prospectively. They cannot be fed back as independent reasons to prefer the model that generated them.

## Observation versus inference audit

The following distinctions are now mandatory.

| Claim | Reset status | Reason |
|---|---|---|
| A-I image class repeats with serial period 9 | observation / externally reconstructed carrier fact | directly supported by the public ledger and solved background layer |
| A-I physical layout `IAB/CDE/FGH` | externally reconstructed fact | historically solved and archived |
| foreground has a strong 108-repeat structure | observation-supported structural claim | supported by repeated physical observations and historical community work |
| first 81 positions use slash/dash while the final 27 use slash/dot | observation | direct from populated H108 residues |
| twelve 3x3 foreground blocks are a natural layout | historically attested organization | community tried this before the current model |
| each primary column is POS3 | hypothesis / local grammar | not a raw fact |
| Q4 is a depth selector | hypothesis | downstream interpretation |
| `d<=q` frame-polarity staircase | model-derived description | depends on selected grammar and closure |
| recursive substitution `(q,d,j)->(q,S(j),j)` | hypothesis | strong within its tested family, not externally supplied |
| route shell `120/012/102` | model-derived | consequence of the selected operation and criteria |
| terminal `100` | model-derived | consequence of the selected machine |
| request/grant or MUTEX interpretation | descriptive semantic analogy | not physical evidence |
| hidden state `XYZG` | model representation | not directly observed |
| predicted unknown sticker foregrounds | model predictions | prospective tests, never observations |

## What the acorn precedent actually contributes

The useful precedent is more specific than "try Game of Life."

Historical printer solving shows a Playdead puzzle grammar in which:

1. raw rows did not arrive in an obvious order;
2. sparse side/margin marks constrained the permutation;
3. correct ordering produced a coherent image;
4. that image contained an acorn plus 41;
5. the acorn and number then cued a Game of Life construction at a specific generation;
6. that generated object participated in a later overlay.

This establishes several authoring habits: ordering metadata can sit beside payload, intermediate outputs can be instructions, and a later transform can be precisely cued by an earlier visual result.

It does **not** justify applying Life, generation 41, or arbitrary row permutations to H108 without a sticker-native cue.

## Playdead-mechanics comparison

Use solved or substantially solved ARG components as a design-vocabulary corpus.

| Historical component | First useful organization | Secondary operation | External cue? | Output type | Sticker relevance |
|---|---|---|---|---|---|
| iOS printer | time-indexed 5x5 glyph slices | order by hour | yes, timestamp | plaintext phrase | strong precedent for metadata-driven ordering |
| Xbox printer | geometric reconstruction | Braille after registration | geometry/marks | phrase | strong precedent for two-layer decoding |
| PC printer/acorn | row permutation constrained by side marks | acorn + 41, then Game of Life | yes | phrase/next-stage object | very strong precedent for boundary metadata and generated transforms |
| Switch printer | Morse-like instruction | physical controller connect/disconnect sequence | yes | operational sequence | precedent for "code as action" |
| Terminal 41 RGB image | exact-value filtering | recombine non-colliding layers | prior RGB values | image/path | precedent for outputs reused as selectors |
| macOS poem overlay | registered text overlay | select letters at dots | in-world poem | phrase | precedent for externally supplied text before extraction |
| CE background layer | collect nine image classes | assemble `IAB/CDE/FGH` | sticker serial/image class | path `dat/534brn9653f9j8mmd` | direct same-object precedent |

## Simplicity test for every live hypothesis

A candidate should be documented against these questions before expensive expansion:

- What raw facts force or motivate its first non-obvious operation?
- Could a competent 2019-2022 solver plausibly discover that operation?
- Does another solved Playdead puzzle demonstrate the same kind of move?
- How many arbitrary conventions, orientations, label choices, or thresholds are required?
- Does missing sticker data naturally degrade the solve, or does the model require reconstructing a huge hidden object?
- Does it make a prospective prediction that can be checked against held-out or newly recovered evidence?
- Does it produce a recognizable intermediate object, operation, path, address, or next-stage input?
- Can a simpler rival explain the same observations?
- Is the apparent confirmation genuinely independent of the assumptions used to derive it?

No aggregate score should automatically select a winner. The questions are an audit checklist.

## Immediate discriminating tests

Run cheap tests before extending the incumbent machine.

### R1 — historical-ordering audit

Reconstruct, from archived Discord and public writeups, every explicit proposal to reorder H108 rows/blocks, especially any reference to:

- side pixels;
- check-bits;
- alternating margins;
- "like the acorn";
- same layout/order as a printer puzzle.

For each proposal, reproduce the exact operation on observation-only data and record whether the required ordering cue exists in the sticker artifact.

### R2 — boundary-channel inventory

Enumerate all sticker-native information adjacent to the foreground sequence that could serve as registration or ordering metadata:

- A-I class;
- serial modulo 9;
- physical 3x3 background position;
- transitions between slash/dash and slash/dot zones;
- packaging orientation or sticker placement;
- any printed edge, seam, crop, or image-boundary feature recoverable from the background masters.

Do not derive a boundary channel from predicted foreground cells.

Maintain both 12x9 and 9x12 foreground views. The 12x9 layout is a useful registration convention because columns share A-I classes, but that convenience is not evidence of intended read direction. The transpose exposes nine 9+3 class traces and the native 81/27 split as 9x9 + 9x3.

A bounded geometric candidate family is permitted: first-nine spatial structure plus three-cell selector/index, including Pigpen/Rosicrucian-style alphabets. Before inspecting any letter-like output, fix the allowed transform family (D4 only unless an external cue adds more), the class order, and the template mapping.

### R3 — solved-puzzle operation replay

Implement only historically demonstrated operation classes against the raw/partial H108 object:

- externally constrained reordering;
- spatial registration followed by secondary-layer reading;
- selector/key reuse where the key comes from another artifact;
- exact-value or exact-class filtering;
- generated transform only when an explicit sticker/ARG clue supplies its parameters.

Record negative results. Avoid free parameter sweeps that manufacture visual targets.

For geometric-alphabet tests, distinguish literal-stroke interpretations from categorical occupancy interpretations. A literal-stroke test must respect the actual slash/dash orientations; a categorical test needs an independent rule saying which symbol means filled/empty or which body cells become cipher edges. Freeze any such rule before reading outputs, then use held-out classes/frames where possible.

### R4 — incumbent-model assumption burn-down

For every supplied premise in the current theorem graph, classify it as:

- directly observed;
- historically motivated;
- generic simplicity prior;
- selected because it preserves the machine;
- genuinely derived from independent evidence.

Any premise in the fourth category is a circularity risk and gets a targeted alternative-family test.

### R5 — holdout comparison across hypothesis families

Use the existing sticker holdout machinery, but compare multiple grammar families rather than variants of POS3 alone.

A family earns attention if it predicts withheld physical foregrounds or independently recovered historical structures without tuning on those targets.

### R6 — "what did Playdead expect players to possess?" audit

Reconstruct the information state available at likely solve times.

Ask separately:

- what could be solved with one Collector's Edition;
- what required pooling multiple owners;
- what became possible only after enough stickers were catalogued;
- whether the design appears to expect a near-complete global set;
- whether another ARG artifact could have supplied missing organization.

This directly tests the possibility that the foreground puzzle is simple globally but hard under our 82-sticker sample.

## Quarantine policy

Do not delete or rewrite prior experiments. Preserve them as a mature hypothesis family.

During the reset:

- the prediction matrix remains frozen and usable for prospective validation;
- `machine-spec.json` remains a specification of the incumbent model, not a statement that the mystery is solved;
- terminal `100` is not privileged as the next-stage search token unless an external artifact independently asks for such an object;
- negative historical tests remain valuable and should not be rerun without a new cue;
- new observations must enter the raw ledger before interpretation.

## Exit criteria

The reset closes only when:

1. the historical solving record has been mined into reproducible operations;
2. solved neighboring ARG mechanics have been catalogued at operation level;
3. the current machine's premises have been audited against that corpus;
4. plausible simpler families have received cheap falsification attempts;
5. surviving families have been compared on independent evidence and prospective prediction;
6. the research queue states clearly which assumptions remain live.

The likely outcome may still be the current ternary machine. If so, it should return as a survivor of the reset, not as its starting premise.

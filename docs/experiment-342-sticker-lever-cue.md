# Experiment 342 — historical sticker-symbol lever cue and direct replay test

_Status: completed bounded R3 consumer test, 30 Sep 2026._

## Why this matters

The reset has been asking for an **independent consumer** of the three sticker marks rather than assigning them abstract numerical meaning because a model likes the result.

The historical Discord export contains a much stronger candidate than the Pigpen idea.

On 21 Mar 2021, while discussing the still-unsolved sticker foreground, `aperson1` connected the three sticker symbols to a Collector's Edition sleeve image and the three-position lever used for INSIDE's secret ending.

The claimed geometry is:

```
slash  = top
dot    = left
dash   = right
```

and the lever positions are:

```
top   = U
left  = L
right = R
```

So the clue supplies a concrete, externally motivated command mapping:

```
/ -> U
. -> L
- -> R
```

This predates the present reconstruction by years and does not depend on POS3, the current machine, the prediction matrix, or the Pigpen discussion.

## Provenance

Source archive:

- repository: `gamesbyian/playdead-unofficial-exports`;
- channel: `ARG / solving` / `461275582970462209`;
- immutable export blob: `1889cc948f86f5a4455de0d7310b15cdb1b88b5c`;
- historical discussion: 21 Mar 2021;
- referenced assets:
  - `assets/INSIDE_B-f038cdd5970802f8.JPG`
  - `assets/unknown-70a6031fe54449cd.png`

The same discussion explicitly proposes that the sticker symbols could be a code for the lever and then asks how the sequence should be recovered.

Machine-readable provenance is preserved in `data/sticker-lever-cue.json`.

### Evidence discipline

There are two distinct claims:

1. **Historical fact:** the community identified a sleeve/game geometry matching dot-left, dash-right, slash-top to the lever's left/right/up positions.
2. **Hypothesis:** the sticker foreground is intended to be consumed as lever commands.

The first raises the prior of the second. It does not prove it.

The source images should be treated as the ultimate visual evidence for the geometry; this experiment records the historical observation and tests a consequence without claiming authorial intent from Discord consensus alone.

## Cheapest direct test

The normal secret-ending bunker password is historically recorded as:

```
UURLRRRUUURLLL
```

Under the sleeve/lever mapping this becomes:

```
//-.---///-...
```

Test whether this 14-command word occurs as a contiguous window anywhere in the cyclic H108 sticker sequence, using physical observations only and leaving unknown residues as wildcards.

### Canonical forward sequence

Exact compatible H108 starts:

```
0
```

The closest starts still contain two physical contradictions:

- start 47: 8 of the 14 positions are observed; residues 59 and 60 contradict;
- start 101: 6 positions are observed; residues 4 and 5 contradict.

### Reverse sequence

Exact compatible starts:

```
0
```

Best mismatch count is one.

### Symbol-mapping sensitivity control

Even if the sleeve mapping is ignored and all six bijections between `{U,R,L}` and `{/,-,.}` are tried, **none** yields an exact contiguous forward or reverse placement of the canonical 14-command word.

So the negative result is not an artifact of choosing the historical direction labels.

## Cyclic-start sensitivity

There is one caveat. Historical discussion of the looping secret-ending song sometimes treated its starting note as potentially arbitrary.

If all 14 cyclic rotations of the command word are admitted under the historical mapping, one exact wildcard-compatible placement appears:

```
rotated code: LLLUURLRRRUUUR
H108 start:   98
known cells:  5 / 14
```

That is far too weak to count as evidence. It appears only after adding another degree of freedom and is constrained by five observed cells.

Preserve it as a sensitivity result, not a lead.

## Result

The simplest lever-consumer hypothesis is now split cleanly:

**Closed:**

> fourteen consecutive sticker residues directly replay the already-known normal bunker password in its canonical forward/reverse form.

**Still live:**

> the three sticker symbols are lever commands, but the foreground supplies a different sequence, requires an independently cued ordering/selection step, or targets another lever interaction.

The second family is important because the consumer and symbol semantics are supplied outside the present machine.

## Interaction with 9+3 / Pigpen work

This historical cue changes the priority of the geometric lane.

Pigpen requires inventing a codebook registration and currently licenses 14,400 candidate A-R strings before language scoring.

The lever hypothesis starts with a concrete sticker-native alphabet consumer:

```
/ = up
- = right
. = left
```

That should be tested before reopening semantic Pigpen decoding.

It may also explain why the marks were drawn as distinct literal shapes rather than arbitrary colors, although that remains an interpretation rather than a demonstrated design fact.

## Next bounded tests

Do not brute-force arbitrary sticker permutations into lever sequences.

Useful next work must obtain ordering or selection from an independent source, such as:

- serial/period structure already physically established;
- the solved background-art path if it demonstrably supplies an order;
- another historical message explicitly connecting sticker ordering to lever input;
- another CE/ARG artifact that gives a start point, subset, or traversal.

Without such a cue, searching combinations for a lever sequence would merely recreate semantic fishing in a three-letter alphabet.

## Reproducibility

```bash
python scripts/audit_sticker_lever_replay.py
```

# Experiment 479: twelve-position A–I class words as lever commands

_Date: 2026-10-08. Negative controlled consumer test, not a new lever password._

## Why the class-word reading is licensed to test

The historical 12×9 arrangement uses nine A–I background classes.
Reading **down one fixed class** yields **twelve symbols**:
nine from the slash/dash primary sector followed by three from
the slash/dot tail. This is already a historically attested
registration, not a newly optimized permutation.

Under the preserved April-2020/March-2021 physical sleeve/lever
proposal `/=up, -=right, .=left`, such a class word **can include
all three action directions**. That avoids the mathematical barrier
against producing Left from a Q4-selected *primary-only* readout
(Experiments 342, 343, 451 and 476).

This makes the nine naturally ordered class words worth a cheap
*hostile positive-control replay*, without claiming that a twelve-move
word is an independently authorized new input.

## Frozen options before testing

- Native class order: alphabetical `ABCDEFGHI` or physically solved
  row-major `IABCDEFGH` (the physical square is `IAB/CDE/FGH`).
- Read each complete 12-position class from t=0 through t=11,
  concatenating the nine class words. Also allow reversing that
  entire 108-character stream.
- A **fixed real consumer reference**: the original bunker lever's
  known fourteen-command word `UURLRRRUUURLLL`.
- Test any of 108 cyclic start offsets. The conservative reference
  keeps the actual password's original orientation. As a deliberately
  generous sensitivity test, allow all 14 rotations of the password
  and all 14 rotations of its reversal.

No other class permutation, per-class rotation, symbol substitution,
appended delimiter, new password, game input handler or visually
selected candidate phrase is searched.

## Results

| Class order | Stream direction | Raw-compatible windows for exact original word | Raw-compatible rotated/reversed windows | Full matches among 324 compatible masters |
| --- | --- | ---: | ---: | ---: |
| `ABCDEFGHI` | forward | **0** | **3** | **0** |
| `ABCDEFGHI` | reverse | **0** | **3** | **0** |
| `IABCDEFGH` | forward | **0** | **3** | **0** |
| `IABCDEFGH` | reverse | **0** | **3** | **0** |

All three raw-compatible rotated/reversed positions in each stream
agree with only **5, 5 or 6 actually observed foreground stickers**;
all other required cells are missing in the partial corpus. **However,
these weak partial matches are already impossible under the sector
alphabet convention itself:** the first 81 sticker positions can only
issue U/R and the last 27 only U/L. This necessary restriction
rules out every such partial placement without filling *any* missing
sticker or assuming the one-minority-per-column model.
The four rows are **symmetrically related**, not four independent
replications.

The structural family comprises **18** primary nine-frame bodies
obeying the physically observed one-minority-per-column grammar
times **18** observation-compatible one-slash tail selectors.
Across every one of its **324 full strings**, neither of the
two native class orders, neither reading direction, any of
108 possible cyclic starts, nor any of the 28 password
orientations produces the original bunker word even once.

The stronger independent result is that **zero of the 28 original
password orientations at any of the 108 starts** is compatible with
the native sector alphabets in **either** natural class order and
reading direction. Thus even an *arbitrarily selected completion*
of all 42 missing stickers, respecting the observed sector split,
cannot produce the known original bunker password in these two
fixed column orderings. The 324-member column/Q4 grammar check is a
consistency check, **not the premise needed for the impossibility**.

The class-word idea *does* make U/R/L available somewhere in a longer
sequence, but that is insufficient for this particular known 14-move
password and does not supply a separate source-authored input.

## Interpretation

The physical class-word readout is a **new type-compatible interface
candidate**, but **not** an established downstream instruction.
The fact that a short sequence of twelve moves can contain Up,
Right and Left is only an alphabet test. The actual demonstrated
original game input uses fourteen moves and has already been solved.
There is no independently reported second handler that would
accept the twelve moves for a single class or a concatenation
of class words.

One could manufacture hits by permuting the nine class columns,
rotating each class independently or choosing a different
14-character target. Those options lack a source-native cue
and are specifically **not** reopened here.

The tiny 5–6-observation matches in the partial corpus illustrate
why relying only on observed stickers can even miss an already-known
alphabet contradiction. A classword readout could still have a distinct
untested, independently cued input. Neither a missing 14-command
sequence nor a new in-game handler has been identified. Candidate completeness and a fixed consumer
are both necessary, not sufficient, validation gates.

## Reproduction

```bash
python scripts/audit_classword_lever_consumer.py
```

The standard-library script reads the 84-record/66-residue
canonical observations, enumerates the raw-compatible
18×18 exact masters through the already verified completion
helpers, checks all physically observed placements,
and asserts that both the alphabet-only and complete-master
results have zero matching placements. It will fail if
the corpus or grammar changes.

The same result was independently enumerated using a
separate JavaScript implementation on the fetched physical CSV
before this code was authored. Source records and replay
orientation were frozen in this report; no new physical symbols
or decoded endpoint were introduced.

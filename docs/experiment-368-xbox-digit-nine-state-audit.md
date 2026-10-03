# Experiment 368 — Xbox residual digit nine-state audit

_Status: completed bounded cross-puzzle audit, 2 Oct 2026._

## Trigger

The solved Xbox One printer planet leaves a conspicuous residual layer after the message letters are isolated. The published Braille-ASCII transcription contains 67 decimal glyphs, but **no 5**:

```
9N879763
087E894W26
09817986469
PL663AN79ET
976828'9126
7DI89829812
!CO792412-
984VE3229
679RED6
```

The observation is interesting for the CE because deleting 5 from the decimal alphabet leaves exactly nine glyphs, while the sticker background channel has exactly nine image classes A-I.

## Exact census

Digit counts:

| glyph | count |
|---|---:|
| 0 | 2 |
| 1 | 4 |
| 2 | 9 |
| 3 | 3 |
| 4 | 4 |
| 5 | **0** |
| 6 | 10 |
| 7 | 9 |
| 8 | 11 |
| 9 | 15 |

The transcription has 88 cells total, of which 67 are decimal glyphs. The observed decimal alphabet is therefore exactly `012346789`.

As a descriptive sanity check only, if 67 positions were iid uniform decimal draws, a pre-specified digit would be absent with probability `0.9^67 = 0.0008595`; the chance that at least one of ten digits were absent would be about `0.0085806`. These are **not inferential p-values** for the puzzle, because the characters arise from a spatial Braille pattern rather than an established random decimal process.

## What transfers cleanly to the CE

The physical CE ledger independently confirms that the background channel is an exact nine-state serial cycle:

`001=A, 002=B, ... 009=I, 010=A, ...`

All 82 classified physical stickers in `data/observations.csv` match that recurrence.

So there is a legitimate, tightly bounded historical-design observation:

> A solved pre-CE INSIDE puzzle produces a residual readout whose decimal subset contains exactly nine glyph identities; the later CE uses a nine-state background alphabet.

That is worth preserving as a possible design echo.

## What does **not** follow yet

There are `9! = 362,880` bijections from the Xbox digit set to A-I. Exhaustively enumerating them is computationally trivial, but it would currently prove nothing.

A mapping test needs paired observations. At present there is no independently supplied rule that says which Xbox Braille cell corresponds to which sticker serial, residue, A-I tile, frame position, or CE readout position. Without such an alignment, searching 362,880 labelings and choosing an attractive one is pure relabeling freedom.

This corrects the tempting but over-strong next step: **do not run a 9! mapping search until an external alignment or common consumer exists.**

## Braille-ASCII caution

The digits in the Xbox transcription are not known to be decimal numbers in the semantic sense. They are ASCII labels for six-dot Braille patterns in the decoded field. In standard Braille ASCII, the glyph `5` denotes one particular dot pattern (dots 2-6). Its absence may therefore be a geometric consequence of the planet's overlay rather than a deliberately omitted decimal value.

That makes the right question narrower: is the missing Braille cell pattern itself constrained by the construction, and is there any independently evidenced reason to associate the resulting nine observed digit-glyph states with the later nine CE backgrounds?

## Result

**Keep open as a bounded design-echo hypothesis; do not promote to a decoder.**

The missing 5 is real and previously under-documented. The 9↔9 cardinality match is exact. But there is currently no licensed cross-puzzle pairing that can turn the cardinality match into a falsifiable digit→A-I mapping.

### Reopening condition

Reopen direct mapping only if one of these appears independently:

1. a historical Discord/source message assigning meaning to the Xbox residual digits;
2. a recovered Xbox solved-order artifact that provides a second registration coordinate linking cells to a 3×3 or nine-state scheme;
3. a CE artifact that explicitly supplies numeric/Braille labels for A-I;
4. a common downstream consumer that accepts both a nine-state Xbox readout and the A-I channel.

Until then, treat the observation as evidence about Playdead's design vocabulary, not as missing sticker data.

## Reproducibility

Run:

```bash
python scripts/audit_xbox_digit_nine_state.py
```

It rewrites `data/experiment-368-xbox-digit-nine-state-audit.json` and fails loudly if the missing-digit fact or CE A-I recurrence changes.

# Experiment 369 — Xbox Braille orientation and nine-state residual

_Status: completed bounded structural audit, 2 Oct 2026._

## Question

Experiment 368 established the exact fact that the solved Xbox planet's Braille-ASCII transcription contains 67 digit cells using nine of the ten ASCII digit glyphs, with only `5` absent.

Before treating that nine-state residual as a possible design echo of the CE A-I background alphabet, ask a cheaper question:

> Is "nine digits, missing 5" simply an orientation-invariant property of the same Braille cells?

If so, the observation would be much less interesting.

## Braille-ASCII meaning of the missing glyph

The ASCII glyph `5` corresponds to six-dot Braille pattern `010001`, i.e. raised dots **2 and 6**.

So the observation is more precisely:

> In the independently correct orientation of the Xbox Braille field, no decoded cell has exactly dots 2+6 among the cells that land in the ASCII decimal range.

The decimal labels themselves should not be treated as numeric values.

## Geometry-preserving orientation control

The correct orientation is not selected to make the digit observation work. It is independently fixed because it makes the embedded letter channel read `NEWPLANETDISCOVERED`.

Keeping the same 2×3 Braille cells and applying the four rectangle symmetries gives:

| orientation | digit cells | distinct ASCII digits | missing |
|---|---:|---:|---|
| correct / identity | 67 | **9** | **5** |
| left-right mirror | 54 | 7 | 1,2,9 |
| top-bottom mirror | 14 | 5 | 2,4,6,7,8 |
| 180° | 10 | 4 | 0,1,2,4,6,7 |

Only the independently established correct orientation produces a nine-state decimal subset.

This is the strongest useful result from the follow-up. The 9-state observation is not a trivial consequence of the planet's underlying cell multiset.

## Broader descriptive relabeling null

As a deliberately over-broad sanity check, permute the six Braille dot labels in all `6! = 720` ways and ask only how many distinct ASCII digit glyphs result.

Distribution:

| distinct digit glyphs | dot permutations |
|---:|---:|
| 0 | 4 |
| 1 | 36 |
| 2 | 112 |
| 3 | 104 |
| 4 | 148 |
| 5 | 144 |
| 6 | 68 |
| 7 | 52 |
| 8 | 32 |
| 9 | 16 |
| 10 | 4 |

Only **20/720 = 2.78%** of arbitrary dot relabelings yield at least nine distinct decimal glyphs.

Among the sixteen exactly-nine cases, the missing glyph is:
- `9` in 8 permutations;
- `5` in 4;
- `3` in 2;
- `2` in 2.

This 720-way family is **not** historical evidence and should not be read as a p-value. It merely shows that the observed nine-state decimal support is not generic under relabeling of the same cells.

## Interpretation

Experiment 369 upgrades the observation slightly:

- the correct message-bearing orientation is independently fixed;
- that orientation uniquely maximizes decimal-glyph diversity among the four actual rectangle symmetries;
- the resulting support happens to contain exactly nine digit identities;
- the absent identity is Braille dots 2+6 / ASCII `5`.

That is a more specific structural coincidence than "there are lots of numbers."

It still does **not** establish that Playdead intentionally encoded a nine-state secondary alphabet, and it supplies no digit→A-I mapping. Experiment 368's guardrail remains intact.

## Next bounded question

The best next question is historical rather than combinatorial:

> Did 2018 solvers discuss the non-letter Braille cells as information, noise, filler, or a second channel?

A source saying they were deliberately generated, constrained, or left unresolved would materially change the status of this hypothesis. A source explicitly calling them meaningless filler would weaken it.

A second useful path is reconstruction of the exact 36-row Xbox planet and cell grid, so the missing 2+6 pattern can be localized geometrically rather than treated only as a frequency fact.

## Reproducibility

Run:

```bash
python scripts/audit_xbox_braille_orientation.py
```

It writes `data/experiment-369-xbox-braille-orientation-audit.json`.

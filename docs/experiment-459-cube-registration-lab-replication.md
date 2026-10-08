# Experiment 459: direct replication of the community Cube Registration Lab

## Provenance and exact pair definitions

On 8 October 2026, a Discord researcher shared the self-contained offline
**Cube Registration Lab** HTML together with four screenshots. The submitted
HTML and images are research inputs; its complete third-party artwork, font
payloads and implementation are **not redistributed** in the repository.

I inspected the JavaScript formulas and independently reconstructed the exact
pair sets. The critical definitions, which resolve Experiment 457's earlier
geometry discrepancy:

- Cube `c = floor((n−1)/27)`, layer `z = floor(((n−1)%27)/9)`, A–I
  letter `LET[(n−1)%9]`.
- Physical 3×3 layout `IAB/CDE/FGH`, whose row-major string is
  `IABCDEFGH`; alternative alphabetical layout is `ABCDEFGHI`.
- The x coordinate is `slot%3` (horizontal); y is `floor(slot/3)`
  (vertical).
- Any **unordered** pair of two distinct observed positions, taken
  from **different cubes**, is eligible. A shift matches if its axis
  changes by **either +1 or −1**, with the other two coordinates unchanged.
  Defaults: no edge wrapping; separate controls exist to enable wrapping
  and restrict cube pairs.
- "Flat column" compares equal A–I letters at **different depths**
  across different cubes, regardless of their XY coordinate labels.
- Only both-collected endpoints count. For each shift the support and
  denominator are its **own** set of eligible observed pairs.
  In the app's final comparison column, observed exact and shifted
  fractions are subtracted, with the same strict null assignment
  used for both fractions, **but not a shared observation-pair mask**.
- Strict shuffle D preserves observed foreground colour counts within
  each cube × A–I class, leaving unknown positions unknown. There are
  exactly **331,776** distinct assignments at both snapshots. Symbol
  mapping: `G = /`, `R = -`, `Y = .`.

This resolves why the earlier equal-support directed-shift comparison
had different percentages: it measured a **different statistic**.

## Full reproduction of the original 65-residue HTML input

| Layout | Same spot | X | Y | Z | Flat |
| --- | ---: | ---: | ---: | ---: | ---: |
| Physical IAB/CDE/FGH | **33/63** (52.4%) | **21/68** (30.9%) | **31/74** (41.9%) | **28/81** (34.6%) | **43/114** (37.7%) |
| Alphabetical ABC/DEF/GHI | **33/63** (52.4%) | **20/83** (24.1%) | **29/70** (41.4%) | **28/81** (34.6%) | **43/114** (37.7%) |

These reproduce all four supplied screenshots, including the much lower
alphabetical X rate (the user's previous textual X=24% came from
alphabetical layout, while their physical-layout screenshot showed X=30.9%).

The exact strict D null gives same-spot mean **43.783%** and
one-sided `P(rate>=33/63)=0.0606192` over 331,776 assignments.

Native physical-layout exact-versus-shift **rate** contrasts:

| Shift | Actual exact minus shift, percentage points | D-null mean difference | Exact one-sided tail |
| --- | ---: | ---: | ---: |
| X | 21.50 | 10.08 | **0.05324** |
| Y | 10.49 | 3.47 | 0.12558 |
| Z | 17.81 | 1.19 | **0.04047** |
| Flat | 14.66 | 1.31 | 0.06062 |

Alphabetical X instead yields 28.28 points above the shifted rate,
null-mean difference 13.06 points, and tail **0.01317**. This matches
the user's supplied alphabetical comparison screenshot.

A deliberately **limited** multiple-contrast diagnostic takes the
maximum mean-centered, null-SD-standardized exact-minus-X/Y/Z rate
contrast over both explicitly supplied layouts (six tests in total).
Exhaustive re-enumeration of all 331,776 assignments yields an observed
max Z of **2.50654**, reached by alphabetical X, and
`13,024/331,776 = 0.0392554` assignments with an equally or more
extreme maximum.

This is an exact within-this-six-tests family-wise shuffle tail, **not**
a global or discovery-adjusted probability. The community has also
explored other nulls, wraps, custom layouts and operators, and the
alphabetical X result was noticed retrospectively.

## Update from original lab 65 to canonical observed 66 residues

The lab HTML has 65 positions: G=36, R=22, Y=7. The independently
confirmed dot at **residue 103** adds one Y, not another missing
primary symbol. The current canonical 84-record corpus has 66 unique
residues.

| Layout | Same spot | X | Y | Z | Flat |
| --- | ---: | ---: | ---: | ---: | ---: |
| Physical | **33/64** (51.6%) | 21/72 (29.2%) | 31/77 (40.3%) | 28/83 (33.7%) | 43/118 (36.4%) |
| Alphabetical | **33/64** (51.6%) | 20/84 (23.8%) | 29/73 (39.7%) | 28/83 (33.7%) | 43/118 (36.4%) |

The D permutations remain 331,776 and most tails remain identical,
because the additional dot's within-(cube,letter) group is uniform;
the available pair denominators change. Updated same-position D-null
mean is 43.099%; upper tail remains 0.060619.

## Apply the exact lab relation to the 324 structural completions

The 324 raw-observation-compatible full masters under the physical
one-minority-per-primary-column body grammar and one-slash-per-Q4-depth
grammar consist of 18 distinct primary bodies × 18 Q4 selector codes.
They are **candidate guesses**, not recovered sticker readings.

Instead of restricting to the original visible pairs (on which every
compatible completion necessarily has the same score), compare
all complete 108-symbol pair relations under the lab's exact definitions.

| Full-master relation, physical layout | Full-grid pairs | Mean match rate across 324 masters | Range |
| --- | ---: | ---: | ---: |
| Same spot | 162 | **40.83%** | 37.04–45.68% |
| X | 216 | 33.74% | 30.09–37.50% |
| Y | 216 | 31.93% | 27.31–35.19% |
| Z | 216 | 30.12% | 26.39–33.33% |
| Flat | 324 | 32.54% | 29.94–34.57% |

**All 324** full masters have same-spot agreement strictly greater
than each of X, Y, Z and Flat, whether the physical or the alphabetical
layout is chosen. This is **not independent support for cube geometry**:
the selected grammar already enforces 3×3 spatial structure and
the full-grid denominators include many inferred, unobserved stickers.

Notably, fully specified physical-layout same-spot agreement is
40.83% on average, substantially lower than the present observed
51.56%, illustrating observation-mask and conditioning effects.

## Reproduce

```bash
node scripts/audit_cube_lab_replication.js
python scripts/audit_cube_lab_completion_ensemble.py
```

The first script reproduces pair counts and all exact strict shuffles,
including six-test max-Z correction, using only the canonical
observation ledger and the frozen definition "omit residue 103"
to recover the original 65-position input. The second enumerates all
324 complete candidate masters via the previously committed
standard-library ensemble helpers. Independent Node and Python
implementations were run against the supplied lab input and the
physical corpus during analysis. Repo-script CI execution is not
claimed until checks run.

## Conclusion and stopping rule

- The supplied HTML resolves the coordinate ambiguity and the original
  screenshots are quantitatively reproducible.
- A same-spot registration excess persists relative to several
  shifted rules, including on a six-comparison family-wise strict-null
  test, but the post-selection qualification is substantial.
- All candidate masters reproduce a same-spot preference automatically
  when fully completed. This is an expected property of the
  structural family, **not a new decoding operation**.
- Keep exact pair-generation separate from matched-pair causal
  contrasts. Neither is inherently wrong, but their denominators and
  nulls answer different questions.
- A useful next test would evaluate specific, previously frozen
  symbol predictions using the new physical lab observations, or
  a historically cued image/overlay/lever consumer, rather than
  retrospectively tuning layouts or sorting attractive outputs.

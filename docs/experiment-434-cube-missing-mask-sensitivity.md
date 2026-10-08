# Experiment 434: the observation mask can inflate apparent cube correspondence

## Motivation

The Discord cube work found 33/63 same-position known-symbol matches,
later updated to 33/64 with residue 103. The primary first-three-cube
subset has 24/40 same-position slash/dash matches. Experiment 433
shows this aggregate correlation does not predict masked primary
residues better than the simple majority baseline.

Can the unknown positions themselves change the story under broad
already-established, non-machine-specific completion grammars?

## Physical observations and exhaustive conditional ensembles

Only 54 of the 81 primary residues are physically observed. Every
cross-quarter pairing among Q1,Q2,Q3 shares one local (depth d, A-I j)
coordinate; there are 27 coordinates times three pairs = **81** fully
specified primary-cube comparisons. Only **40** are currently directly
observable, of which 24 match.

Three conditional families are compared.

| Allowed completion assumption | Complete primary sequences | Possible matching comparisons, out of 81 |
| --- | ---: | ---: |
| Only preserve directly observed / and - | unrestricted | **35–63** |
| Every 9-cell frame has exactly three of one symbol and six of the other (either polarity) | **12,960** | **37–53** |
| Plus exactly one minority symbol per physical 3×3 column | **18** | **43–51** |

The unrestricted range 35–63 is calculated by independent
enumeration of each 3-cell cross-quarter triad (never by assuming the
unknown 41 pair comparisons can be assigned independently). A fully
specified binary triad has either one or three matching pairs.

### Distribution across constrained completions

Under the 18 column-constrained primary completions, the exact
81-pair match histogram is:

| Matching pairs | Completion count |
| ---: | ---: |
| 43 | 4 |
| 45 | 4 |
| 47 | 6 |
| 49 | 2 |
| 51 | 2 |

The mean is **46⅓ / 81 = 57.20%**, lower than the directly observed
**24/40 = 60%**. The broader 12,960 primary completions have mean
**44.4667 / 81 = 54.90%** and range 37–53/81.

These percentages are not probabilities for what the missing
stickers *actually* are. All models were inferred retrospectively
from overlapping physical evidence, and candidate masters are
correlated rather than independent draws from a manufacturing prior.

### Particularly revealing A-I class: E

Of the nine potential cross-quarter comparisons at A-I letter E
(three depth layers × three pairs), only three are currently visible;
all **three match**. But across all 18 column-constrained complete
primary bodies, exactly **five of the nine** E comparisons match.
The four remaining matches and mismatches are not independent
variables, because every primary frame obeys its local one-minority
constraint.

This gives a concrete mechanism by which sparse sticker recovery can
make shared coordinates look more homogeneous than the completed
structure. In particular, the missing E residues 41,68,77 produce
clear disagreements between literal cube copying and the
column-constrained family (Experiment 433).

## Interpretation

- Current cross-cube match counts are consistent with numerous very
  different unobserved completions.
- The full primary cube agreement can decrease when missing cells are
  filled according to independently motivated 3×3 placement rules.
- Neither the currently observed 60% agreement nor the conditioned
  completed-body rates establish an intended 3D geometry.
- Individual-symbol holdouts and prospective physical residues remain
  the appropriate validation level. Fitted attractive visual
  projections, arbitrary rotations, or completion weights cannot
  replace that evidence.

## Reproduction

Run: `python scripts/audit_cube_missing_mask_sensitivity.py`.

The script enumerates all primary bodies in each family, rechecks
observed-only bounds by 27 local triads, and asserts the class-E
result. Counts were independently enumerated using the current CSV
before authoring the script; Python checkout execution is pending.

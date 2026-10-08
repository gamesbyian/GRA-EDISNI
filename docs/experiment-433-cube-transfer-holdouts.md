# Experiment 433: can cube registration predict unseen sticker symbols?

## Trigger and scope

Discord collaborators found a small excess of same-position symbol agreement
across the four 3×3×3 sticker quarters. Experiments 431–432 showed this
excess weakens under stricter cube×A–I census-preserving shuffles and does
not uniquely distinguish identity from every rotated/reflected registration.

This experiment asks a more discriminating question: **Does any simple,
explicit, geometry-motivated cross-cube transfer operation predict individual
primary sticker symbols better than ordinary slash/dash majority?**

No missing stickers are guessed using machine-derived states. The only
data source is the 84-record/66-residue observed CSV. The twelve Q4
physical observations are excluded from direct transfer because they
use the distinct slash/dot alphabet; otherwise a "same colour" comparison
would be physically inhomogeneous.

The operation menu is fixed *before comparing the holdout scores*:
identity, reverse depth, cyclic depth+1 control, 180° XY rotation,
horizontal XY reflection, cyclic column+1 control. The last two cyclic
operators are negative controls, not authorially cued transducers.
The physical XY layout is the historically solved IAB/CDE/FGH order.

## Test 1: single-residue-held-out cross-cube transfer

For each of the 54 currently observed primary residues, remove that
residue, then read the corresponding coordinates in the other two
primary quarters using one frozen candidate transform. Predict only
when at least one physically known symbol is available **and all
available peers agree**. Otherwise abstain.

The training-only slash/dash majority is the matched baseline,
evaluated on exactly the same covered residues. It is always slash
given the observed primary census.

| Operation | Covered physical residues | Correct transfer guesses | Majority correct on identical positions |
| --- | ---: | ---: | ---: |
| identity | 33 | **22** | **23** |
| reverse depth d→2−d | 35 | 19 | 23 |
| cyclic depth+1 | 32 | 14 | 21 |
| XY rotation 180° | 35 | 22 | 20 |
| XY horizontal reflection | 38 | 18 | 24 |
| cyclic XY column+1 | 35 | 15 | 20 |

The 180° orientation gives only two additional correct guesses versus
the matched baseline, at a different coverage set than identity.
Because the operation was among several explored alternatives, that
small retrospective gain is not an independent discovery.

For the identity rule, the paired correctness discordances against the
global slash baseline are 6 where copy alone is right and 7 where
majority alone is right (16 both right, 4 both wrong). The identity
rule supplies no incremental practical advantage here.

## Test 2: genuinely held-out entire cube after selecting the operation

For each primary target quarter Q, hide *all* its symbols during operation
selection. Compare the other two quarters under the same six fixed
candidate transforms. Choose whichever has the highest Laplace-smoothed
cross-quarter agreement \`(matches+1)/(pairs+2)\`, resolving ties in
the fixed operation order. Only then apply that operation to the held-out
quarter; vote using the other two quarters' available known symbols.

| Hidden quarter | Selected from the other two | Correct/covered | Training-quarter majority |
| --- | --- | ---: | ---: |
| Q1 | rotate 180° in XY | **5/10** | 4/10 |
| Q2 | identity | **8/12** | 10/12 |
| Q3 | identity | **6/10** | 7/10 |
| **combined** | | **19/32** | **21/32** |

This is materially stronger evaluation than picking the best geometry
using all 54 target labels. Within the small frozen menu, operation
selection fails to generalize better than majority. The menu itself
originated after exploratory work on the corpus, so this still is
not a pristine externally preregistered test.

## Test 3: exact cube×letter shuffle null for the predictive operation

Instead of approximating independent Bernoulli events, independently
reshuffle observed symbols *within each* (cube, A–I class) group.
The 16 nonuniform groups permit exactly **331,776 distinct joint
reassignments**, preserving each group's slash/dash or slash/dot
census and all known/unknown positions (the same strictest null
used in Experiment 432).

Recompute the leave-one-residue-out identity-copy vote for every
reassignment, including dynamic abstentions. At the actual observed
placement identity copying gives **22 correct out of 33 covered**, versus
23/33 for the majority baseline.

Under the full exact null:
- Mean usable guesses: **31**;
- Mean correct copying guesses: **16⅓**;
- Fraction with copy *accuracy* at least 22/33: **34,560/331,776 = 0.10417**;
- Fraction with improvement over matched majority at least the observed
  **−1**: **129,024/331,776 = 0.38889**;
- Among the **76,800** assignments with exactly 33 covered sites,
  fraction with ≥22 correct: **18,816/76,800 = 0.245**.

Thus a small apparent raw agreement excess does not turn into a
convincingly useful decoder. These tail fractions are conditional and
retrospective, not confirmatory significance levels.

## Freeze six concrete prospective disagreements

Among the **27 unobserved primary residues**, simple identity copying
has available non-conflicting known peers for 19. The independent
one-minority-per-physical-column family assigns a single symbol at 11
of those 19; the two operations agree at five and **disagree at six**.
The other eight have both slash and dash within that grammar.

| Residue | A–I | Copy prediction | Exact physical-column-family symbol | Physical serials ≤600 |
| ---: | :---: | :---: | :---: | --- |
| **11** | B | / | **-** | 11,119,227,335,443,551 |
| **33** | F | / | **-** | 33,141,249,357,465,573 |
| **41** | E | - | **/** | 41,149,257,365,473,581 |
| **64** | A | - | **/** | 64,172,280,388,496 |
| **68** | E | - | **/** | 68,176,284,392,500 |
| **77** | E | - | **/** | 77,185,293,401,509 |

All six physical-column symbols match the preferred symbols in the
existing frozen machine prediction matrix. Residue 41 additionally
lies on a known primary physical gauge support and is therefore
less clean for comparing broader model families than 11,33,64,68,77.
These are **discriminator predictions**, not calibrated probabilities;
there is no justification for favouring copy forecasts given its
holdout failure.

The strongest as-yet-unobserved physical test of the native Q4 one-slash
grammar remains residue 94 (slash), forced by physical dots at residues
85 and 103. Previously frozen acquisition priorities still apply.

## Interpretation and stopping condition

The direct cubic registration idea fails the requested move from
aggregate correlation to withheld-symbol prediction. No tested operation
has earned the right to generate a new decoded message, image, lever
command, or unique master.

A fresh external geometric cue could reopen a *specific* transform.
Absent such a cue, further variants would multiply retrospective
comparison opportunities without adding evidence. Preserve negative
results and the six frozen cross-family discriminators.

## Reproduce

\`\`\`bash
python scripts/audit_cube_transfer_holdouts.py
\`\`\`

This runs exact counts, entire-cube holdouts and all 331,776 strict shuffles.
It asserts key expected numbers and stops on corpus changes.
The figures were independently calculated against the canonical
CSV before writing the script; the committed Python version requires
checkout-level execution.

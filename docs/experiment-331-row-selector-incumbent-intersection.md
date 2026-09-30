# Experiment 331 — frozen row-selector × incumbent structural intersection

_Status: completed cross-family comparison, 30 Sep 2026._

## Question

Now that Experiment 329's row-selector family is frozen and Experiment 330 has tested it without further tuning, how does its structure intersect the mature incumbent reconstruction?

This comparison does **not** alter either family. It asks whether their independently frozen selector domains and completed body behavior agree, conflict, or partially overlap.

## Selector-domain comparison

The frozen row family permits these tail-selector positions:

```
A  0/1/2
B  2
C  2
D  1/2
E  0
F  1
G  0/2
H  2
I  2
```

Across the incumbent's 14 legal hidden states, the Q4 selector domains are:

```
A  1/2
B  2
C  0/2
D  1/2
E  0
F  1
G  0/2
H  2
I  2
```

So:

- **7 of 9 class domains match exactly:** B, D, E, F, G, H, I;
- A is a row-family superset: `0/1/2` versus incumbent `1/2`;
- C is a row-family subset: `2` versus incumbent `0/2`;
- all nine domains have non-empty intersection.

That is a substantially tighter structural relationship than the generic 9+3 architecture alone.

## Hidden-state intersection

Applying only the selector-domain overlap to the incumbent keeps the seven states with `G=1`:

```
0001 0011 0101 1001 1011 1101 1111
```

Then enforce the already-frozen row-family condition that the selected body row contains exactly one exceptional mark.

Six incumbent states remain:

```
0011 0101 1001 1011 1101 1111
```

The sole rejected `G=1` incumbent state is `0001`. In that state the incumbent D selector chooses row 2, whose completed body row is `///`, violating the frozen one-exception condition.

Thus the two families have a nontrivial six-state exact intersection rather than merely sharing the observed cells.

## What becomes newly predicted?

Compare the six shared states with the full 14-state preferred incumbent family.

Only two previously variable residues become invariant:

```
84  = .
102 = /
```

Residue 93 was already invariant dot in the incumbent.

Therefore the complete cross-family C-tail prediction is:

```
84 / 93 / 102 = . . /
```

No additional primary/body residue becomes invariant. The structural intersection sharpens precisely the two C-tail cells already identified prospectively by Experiment 329.

## Interpretation

This result is interesting but must retain the provenance warning from Experiment 329. The row-family's one-exception rule was noticed after the row/column outputs had been inspected, so the 7/9 domain agreement is not a pristine preregistered discovery.

What has changed is that the family is now frozen and its relationship to the incumbent is explicit:

- it reconstructs the incumbent selector domain exactly at 7/9 classes;
- it is broader than the incumbent at A;
- narrower at C;
- and its full completed-body constraint selects 6/14 incumbent hidden states.

That makes it a useful **cross-family prospective probe**, not a reason to retroactively claim the incumbent has been independently proved.

## Operational consequence

Residues **84 and 102** are now especially valuable physical acquisitions.

A future C-tail sticker gives the following direct test of the frozen row rival:

- residue 84 must be dot;
- residue 93 must be dot;
- residue 102 must be slash.

The incumbent alone allows both values at 84 and 102 across its hidden-state family. Therefore either observation can genuinely discriminate the frozen row-selector family from incumbent states outside their six-state intersection.

Do not tune the row family after such an observation. A contradiction is a falsification event.

## Reproducibility

```bash
python scripts/audit_row_selector_incumbent_intersection.py
```

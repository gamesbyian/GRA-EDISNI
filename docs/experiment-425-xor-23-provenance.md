# Experiment 425 — provenance of the U4 “23 variable cells”

## Question

Experiment 419's tail-XOR overlay has exactly **23 variable cells** across the 12 U4 completions. Is that 23 a deeper structural invariant, or does it arise incidentally from the particular residues still unresolved at U4?

This question became salient after Experiment 424 noted that the literal IBM 029 period code `12-8-3` has labels summing to 23.

## Exact decomposition

The XOR surface has 81 cells. A variable body residue affects exactly one XOR cell. A variable tail residue is repeated over three body rows, so it can affect exactly three XOR cells.

At U4 the unresolved master residues are:

- body: `22,25,55,58,61` = 5 residues;
- tail: `82,84,88,91,100,102,106` = 7 residues.

Before support overlap this gives:

```
5 + 7×3 = 26
```

Three output cells are influenced by both a variable body residue and a variable tail residue:

- body 25 + tail 106 → XOR row 3, column 7;
- body 55 + tail 82 → XOR row 7, column 1;
- body 61 + tail 88 → XOR row 7, column 7.

Therefore the exact union is:

```
5 + 7×3 - 3 = 23
```

## Layer comparison

The same bookkeeping explains the whole Experiment-419 sequence:

| layer | variable body | variable tail | raw supports | overlaps | variable XOR cells |
|---|---:|---:|---:|---:|---:|
| U2 | 9 | 8 | 33 | 4 | 29 |
| U3 | 5 | 8 | 29 | 3 | 26 |
| U4 | 5 | 7 | 26 | 3 | **23** |
| U5 | 5 | 6 | 23 | 2 | 21 |

So 23 is not stable across the completion hierarchy. It appears at U4 because that layer happens to leave seven tail residues variable while retaining the same five variable body residues and three support overlaps.

## Interpretation

The count is **exact and explainable, but not independently selected**.

The canonical XOR registration determines how residue uncertainty fans out onto the 9×9 surface. The U4 machine constraint determines which residues remain variable. Their intersection happens to have support-union size 23.

There is no additional rule in Experiment 419 that prefers 23, and adjacent layers immediately move to 26 and 21.

Therefore the relation to Experiment 424's Hollerith `12+8+3=23` should currently be classified as a genuine numerical coincidence between two independently defined constructions, not a mechanical connection.

That is still worth recording because a future external clue could promote 23 from coincidence to a shared authorial marker. But Experiment 425 supplies no such bridge.

## Disposition

Preserve the recurrence. Do not use it as evidence for either the Hollerith hypothesis or the XOR overlay without an independent “23” or arithmetic cue.

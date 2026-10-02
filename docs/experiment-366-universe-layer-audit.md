# Experiment 366 — completion-universe layer audit

_Status: completed, 2 Oct 2026._

## Question

Experiment 365 made several completion populations explicit. Which missing sticker values are already forced by the broad U2 structural universe, and which values become fixed only when later assumptions are introduced?

This matters because an invariant across 648 observation-supported structural completions has a different epistemic status from an invariant that appears only after the recursive machine is assumed.

## Layers

The audit compares:

- **U2:** 648 masters, 3/6 one-per-physical-column primary structure plus one-slash Q4;
- **U3:** 216 masters, adding the established primary polarity staircase and exact POS3;
- **U4:** 20 masters, adding first recursive closure;
- **U5:** 14 masters, adding second recursive closure.

All 65 physically observed residues are fixed in every layer. The counts below concern only the 43 physically unseen residues.

## Invariant growth

| layer | candidates | unseen residues fixed | unseen residues variable |
| --- | ---: | ---: | ---: |
| U2 | 648 | **24** | 19 |
| U3 | 216 | **28** | 15 |
| U4 | 20 | **29** | 14 |
| U5 | 14 | **30** | 13 |

The transitions are remarkably sparse.

### U2 → U3

Adding the established polarity staircase and exact POS3 fixes exactly four additional unseen cells:

- 49 = `-`
- 50 = `-`
- 52 = `-`
- 54 = `-`

### U3 → U4

First recursive closure fixes exactly:

- **93 = `.`**

### U4 → U5

Second recursive closure fixes exactly:

- **82 = `.`**

After that, the 13 remaining variable residues are exactly:

```
22, 25, 55, 58, 61,
84, 88, 91, 94, 100, 102, 103, 106
```

This is the familiar canonical hidden-state-variable set.

## Main interpretation

The preferred machine has 30 physically unseen residues invariant across its 14 canonical states.

Experiment 366 shows that **24 of those 30 are already invariant in U2**, before the incumbent primary polarity staircase, recursive substitution, route shell, or terminal `100` are used.

Only six additional fixed values arise later:

- four from U3's exact polarity/POS3 representation;
- one from first recursion;
- one from second recursion.

This is useful epistemically. It means most of the preferred completion's apparently sharp predictions are not consequences of deep recursion. They are consequences of the much broader observation-supported 3×3 occupancy and one-slash tail structures.

It does **not** make the U2 premises raw observations. U2 still assumes common 3/6 occupancy and one-per-physical-column structure. The point is comparative: the extra machine machinery accounts for much less of the invariant completion than might be assumed from looking only at U5.

## Minimum identifying sticker sets

For each layer, the audit exhaustively tests combinations of currently unseen variable residues until it finds sets whose foreground signature uniquely identifies every candidate master.

| layer | candidates | raw binary information lower bound | actual minimum sticker count | number of minimum sets |
| --- | ---: | ---: | ---: | ---: |
| U2 | 648 | 10 | **11** | 1,080 |
| U3 | 216 | 8 | **9** | 216 |
| U4 | 20 | 5 | **6** | 180 |
| U5 | 14 | 4 | **5** | 48 |

The printed code is therefore not a maximally efficient arbitrary binary identifier of these candidate populations. Correlations between physical residues prevent the theoretical `ceil(log2 N)` lower bound from being attained.

For U2 and U3, the stronger factorized lower bound explains the extra bit: the candidate space separates into independent primary and Q4 factors, and each factor has its own binary identification requirement.

For U4 and U5, the extra required observation arises from the actual correlated code structure.

## Exact interchangeable residue relationships

Some unseen cells carry exactly the same information within a universe.

At U2:

- 22 and 25 are complements;
- 50 and 54 are identical;
- 88 and 106 are complements;
- 94 and 103 are complements.

At U5 the hidden-state correlations become richer:

- 22 and 25 are complements;
- 84 and 102 are complements;
- 88 and 106 are complements;
- 91 and 100 are complements;
- 94 and 103 are complements.

These are useful for acquisition planning. Within the stated universe, obtaining both members of one exact complement/identity pair does not provide two independent binary facts.

## Consequence for acquisition

Sticker value should be evaluated against the universe relevant to the question.

If the immediate goal is to test the broad U2 structure, residues already invariant across U2 are valuable as **hard falsification tests**, but they do not distinguish the 648 internal candidates. Variable U2 residues are the ones that reduce that population.

If the goal is to identify the canonical U5 hidden state, only five suitably chosen variable residues are required in principle, not thirteen. There are 48 minimum five-residue identifying sets.

Do not interpret equal weighting of candidate masters as a physical probability distribution. These are exact combinatorial partitions.

## Reproducibility

Run:

```bash
python scripts/audit_completion_universe_layers.py
```

Output:

`data/experiment-366-universe-layer-audit.json`

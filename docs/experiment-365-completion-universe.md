# Experiment 365 — layered completion universe

_Status: completed first implementation, 2 Oct 2026._

## Question

There are 43 H108 residues with no physical foreground observation. Rather than choose one preferred completion, can we represent **every completion that survives progressively stronger, explicitly named assumptions**, and make those universes reusable for future tests?

Yes.

The important distinction is between:

- a raw combinatorial possibility;
- an observation-compatible structural possibility;
- a machine-compatible possibility;
- a physically gauge-equivalent printed representation.

These must not be collapsed into one bucket.

## Fixed coordinates

The 43 missing residues are binary once their residue is known:

- residues 1–81 use slash/dash;
- residues 82–108 use slash/dot.

Background A-I is not another unknown. It follows mechanically from residue/serial phase.

For a working physical range 1–600, a logical residue expands to serials

```
r, r+108, r+216, ...
```

up to 600. Those are opportunities to observe the same H108 cell, not separate logical completion variables.

## Universe ladder

### U0 — raw binary space

With only the 65 physically observed H108 residues frozen, the other 43 cells admit:

```
2^43 = 8,796,093,022,208
```

foreground completions.

This layer remains symbolic. Enumerating trillions of explicit strings adds no value.

### U1 — historical/common-census primary + one-slash Q4

Experiment 348 gives exact observation-compatible counts for the two surviving common primary frame censuses:

- 3/6: 12,960 primary completions;
- 4/5: 18,000 primary completions.

The observation-compatible exact-one-slash-per-A-I-class Q4 family has 36 completions.

Therefore:

```
(12,960 + 18,000) × 36 = 1,114,560
```

complete H108 masters.

This universe is represented **factorially**, not dumped as a million-row artifact.

### U2 — 3/6 one-per-physical-column + one-slash Q4

Now add only the spatial structure supported by Experiment 350:

- common 3/6 primary census;
- exactly one minority cell in each physical column;
- either primary frame polarity remains allowed wherever observations permit;
- one slash per A-I Q4 depth stack.

The nine primary frames have observation-compatible option counts:

```
1, 1, 2, 1, 1, 3, 3, 1, 1
```

whose product is **18**.

The nine Q4 class traces have selector-depth option counts:

```
3, 1, 3, 2, 1, 1, 2, 1, 1
```

whose product is **36**.

So the complete universe is:

```
18 × 36 = 648
```

H108 masters.

All 648 are materialized in `data/completion-universe-u2-648.csv`.

Each master is encoded by the 43 missing cells only. Bit `i` corresponds to `unknown_residues[i]`; 1 means slash and 0 means the other legal symbol (dash in the primary region, dot in Q4). The code therefore fits in 43 bits / 11 hexadecimal digits.

### U3 — established primary polarity + exact POS3

The existing raw-machine enumeration supplies the next narrowing:

- 6 primary payloads;
- 36 selectors;
- **216** raw candidate machines.

This imports the established `d <= q` polarity staircase rather than leaving frame polarity open.

### U4 — first recursive closure

Applying only the first registered selector/POS3 closure reduces 216 to **20**.

### U5 — second recursive closure

Applying the second registered closure reduces 20 to the familiar **14 canonical complete masters**, all with terminal `100`.

These are already generated independently by `scripts/enumerate_raw_machine.py` and `scripts/generate_master.py`.

## Physical-representation axis

The 14 canonical masters are not the entire physically plausible representation family.

There are two transition-invisible primary gauge bits:

- residues 6↔8;
- residues 41↔45.

There are also two exact canonical-transducer Q4 polarity gauges on the completely unobserved A and C stacks.

Treating those four binary choices independently gives:

```
14 × 4 × 4 = 224
```

exact transition-equivalent physical masters.

This is a **representation expansion around U5**, not another nested subset of U2. In particular, primary gauge moves can leave the preferred one-per-column physical representation while preserving transition behavior.

The broader coupled F+I Q4 branch remains separately classified because it changes the canonical route shell. Do not silently fold it into the exact-gauge count.

## Immediate information map

The 648-member U2 universe gives a useful assumption-light acquisition ranking.

Six unobserved residues split U2 exactly 324/324 and therefore carry the full one bit of single-sticker information:

```
22, 25, 88, 94, 103, 106
```

Several others split 432/216 and carry about 0.9183 bits.

This ranking is **not a probability statement**. It answers only:

> if every U2 completion is treated as one combinatorial candidate, how evenly would this physical observation partition the candidate set?

The generated JSON preserves exact symbol counts, entropy, background class, and all physical serials ≤600 for every missing residue.

## Why this is useful

Future tests can now be run against an explicit candidate population instead of one preferred master.

Examples:

- ask whether a proposed overlay/consumer property occurs in 1, 10, or 600 of the 648 broad structural masters;
- identify properties invariant across all 648;
- compare the 648-family result with the 216, 20 and 14 machine layers;
- score newly found stickers by how many candidates they eliminate;
- search for pairs/triples of residues that distinguish candidate families;
- separate discoveries caused by the observation-supported 3×3 geometry from discoveries that appear only after recursion is assumed.

Semantic image recognizability is still not a valid selection criterion. The completion universe is a **testing surface**, not a license to pick whichever candidate looks nicest.

## Reproducibility

Run:

```bash
python scripts/build_completion_universe.py --write
```

Query one missing residue:

```bash
python scripts/build_completion_universe.py --query-residue 22
```

Outputs:

- `data/experiment-365-completion-universe.json`
- `data/completion-universe-u2-648.csv`


## Minimum complete U2 discriminator

U2 factorizes exactly into 18 primary completions × 36 Q4 completions. Because each newly observed sticker contributes one binary foreground value, any set that distinguishes all U2 masters needs at least:

```
ceil(log2 18) + ceil(log2 36)
= 5 + 6
= 11 stickers
```

That lower bound is achievable.

One exact minimum discriminator is:

```
primary: 22, 49, 50, 55, 58
Q4:      82, 84, 88, 91, 93, 94
```

The five primary residues assign a unique signature to all 18 primary completions. The six Q4 residues assign a unique signature to all 36 tail completions. Together the eleven-bit signature is unique across all 648 U2 masters.

This is a combinatorial identification result inside U2, not a claim that Playdead intended solvers to obtain those exact eleven stickers. It is immediately useful for acquisition prioritization, however: this set is sufficient to resolve the entire broad one-per-column/one-slash universe without invoking recursion.

# Conjecture Lab, second pass: raw address limits and balanced selector hypothesis

_8 October 2026; follow-up to [first sprint](2026-10-08-first-sprint.md). CL-01 v2 and CL-02 v2. Code: [exact reproducible audit](../../scripts/conjecture_lab_raw_bounds_balanced_tail.py). Mode: DISCOVER/DEVELOP, not solution validation._

## Executive results

1. **An actual observation-only impossibility:** the already known physical slash/dash marks disallow direct nine-bit class lookup into a zero-based **74-entry** array in all four ordinary bit directions/polarities. This no longer relies on the primary-column grammar, Q4, POS3, recursion, or guesses about missing sticker cells. A larger dataset, offset, keyed transform or different grouping remains possible.
2. **A genuinely new deliberate hunch:** suppose Playdead balanced the nine Q4 one-slash depth choices so each of the three levels occurs exactly three times. Of the 18 Q4 codes compatible with current observed marks under the one-slash condition, **only two** have 3/3/3 balance. This is a selectable theoretical constraint, *not a newly discovered regularity*; no observed Q4 marks directly certify equal depth census.
3. **The conjecture now exposes a sharp operation conflict:** in the exact Experiment-450 A∩B physical-column family, balancing Q4 intersects its selected-depth one-dash-per-column rule in **two full masters**, both with the same tail and one identical 27-symbol selected readout. But it intersects the *separately specified, simple* row-exception rule in **zero full masters**. The latter is Experiment 450's simple row criterion, **not** the full Experiment-329 frozen row-selector implementation.
4. **Spatial Latin-square negative:** the solved A–I physical layout `IAB/CDE/FGH` cannot give one of each depth on every physical row or column, because B and I are already fixed to Q4 depth 2 in the first row, and B/H are both depth 2 in the third physical column. The weaker global 3/3/3 count remains possible. Do not confuse those.

## Critical reconciliation: the two masters were already inside the incumbent

An independent generator comparison, added **after** developing the balanced hunch, shows that both A∩B∩S+balance masters are **exactly existing live incumbent states `0100` and `1100`**, satisfying `p=0, G=0`. The associated selected 3×3 surface coordinates decode, under the existing column-one-dash ternary rule, as `102 / 002 / 120`, the already documented incumbent first-pass family for `p=0` (see `scripts/verify_machine.py`). The triple 189/252/315 is the slash=1 *binary* representation of those same three selected surfaces.

This is a substantive dependency correction: **the guessed balance constraint picks out an old machine branch, not an independently reconstructed competing machine or a new physical confirmation**. The pair can still be a productive *conditional* hunch for consumers and future marks. Its attractiveness cannot be added to the established machine's evidence count.

## CL-01 v2: the direct 74-entry index fails before selecting a model

Assume only this decoding proposal:

- nine consecutive primary frames of the H108 code, addressed by each A–I class;
- `/` and `-` are bits;
- read nine class bits forward or reverse, with slash either 1 or 0;
- treat the resulting integer literally as a **zero-based** index into the currently preserved 74 distinct Terminal41 paths.

For each class and convention, leave every physically unobserved bit *free*. Its minimum numerical value is obtained by setting every unknown binary bit to 0; no relationship among unobserved cells is imposed. Therefore the maximum of the nine minimum class addresses is an unavoidable lower bound on the size of any table that could accept **all nine** reads.

| Direction / slash bit | Physically unavoidable largest address, at least | Minimum 0-based table size | Class establishing lower bound |
|---|---:|---:|---|
| Forward / 1 | 382 | **383** | B |
| Forward / 0 | 453 | **454** | C |
| Reverse / 1 | 466 | **467** | F |
| Reverse / 0 | 327 | **328** | C |

In the native forward/slash=1 convention, observed class B is `/?//////-`; even treating the missing bit as zero gives `382`. C is fully known `---///-/-` and gives `58` (slash=1) or `453` (slash=0). This short, independently checkable pair already explains why a literal nine-address lookup into the archived 74 routes cannot work.

**Comparison with previous CL-01:** if the additional A∩B structural constraints are imposed, the forward/slash=1 minimal table expands from 383 to **408** entries; the negative for 74 holds without those constraints.

### Important epistemic distinction

The 74 paths are a **modern preserved archive inventory**, not a demonstrated original enumerated record table. This proves an impossibility for that *proposed direct reader*, not for all nine-bit book ciphers, all Terminal41 artifacts, or even the original website. Inverting slash bits and reading direction were all chosen for a fair bounded control, not authorial candidates with measured prior probabilities.

**Working consequence:** if the intended output really consists of nine direct nine-bit addresses, the project should seek a genuine **512-position source domain** (or an independently described smaller but at least 383-position table for the native observed data) and then separately establish a three-channel reader. This is a hypothetical source requirement, not evidence a 512-entry source exists.

## CL-02 v2: pretend the nine selector depths are balanced 3/3/3

### Why try this?

A human who notices nine A–I class labels and exactly one slash in each three-cell Q4 stack might guess that the three possible selector positions are used equally often. This is a deliberately invented symmetry prior: distribute nine selections into three groups of three. It is familiar, finite, expressible without the incumbent machine, and cheap to test.

This is an example of the desired method: **assume a regularity without proof, follow it to a contradiction or a discriminating prediction, then keep the evidentiary labels honest**.

### Exact tail result

On the 84-record/66-residue physical snapshot the Q4 one-slash assumption has **18** compatible nine-depth strings. Exactly these two are globally balanced:

```
021101022
120101022
```

Positions are native A–I; 0/1/2 mark the depth row of the slash. The reason is transparent: B,H,I are forced to depth 2, D,F to depth 1, and E to depth 0, so the three remaining variable classes A,C,G must supply two 0 choices and one 1 choice. G has only 0/2 possible, so G=0; A and C split the 0 and 1.

A stronger, attractive `3×3` Latin-square guess **fails**. In physical `IAB/CDE/FGH`, I and B already share selector depth 2 in one physical row, while B and H share depth 2 in one physical column. Physical-row or physical-column one-each-depth is impossible no matter how the remaining stickers complete.

### Cross the invented balance with previously defined grammars

Use Experiment 450's A∩B parent: exactly one minority mark per physical column in each 3×3 primary frame, plus Q4 one slash per class. The **324** masters split into 18 primary bodies × 18 Q4 depth strings. Reapply two *existing* and distinct operations:

- **S:** native-Q4 selected-depth body surface has exactly one dash in each of its three physical columns, in all three primary quarters;
- **R:** Q4-selected primary quarter has a one-exception triple across its three depths for each class (the **simple row-exception condition in Experiment 450**, not the exact historical row-family test in 329).

| Conditional master family | All Q4 codes | After speculative 3/3/3 balance |
|---|---:|---:|
| A∩B | **324** | **36** |
| A∩B∩S | **12** | **2** |
| A∩B∩R | **108** | **0** |
| A∩B∩S∩R | **6** | **0** |

Both A∩B∩S∩balance masters have the **same Q4 tail: `120101022`**. Their primary bodies disagree at only physical H108 residues **22** and **25**, exactly the unobserved symbols making those two complete masters distinct.

Moreover, the proposed *selected-depth consumer* produces exactly the same 27-mark string on both masters (Q1, Q2 and Q3 in A–I serial class order):

```
-/-////-/
-//////--
/--///-//
```

That output is **conditional and chosen through the one-dash-per-column requirement itself**. A repeated dash census and the compact output cannot serve as independent validation. The result nevertheless supplies a useful controlled **working assumption**: under A∩B∩S+balance, a definite output exists even though two physical completions remain. That is a good starting point for an explicitly exploratory consumer search, rather than stopping solely because the number 3/3/3 is unsupported.

### Frozen *conditional* physical predictions

For the A∩B∩S+balance pair, among the missing residues the following Q4 positions are fixed:

| Q4 class/role | Missing residue | Predicted foreground |
|---|---:|:---:|
| A, depth 0 | **82** | dot |
| A, depth 1 | **91** | slash |
| A, depth 2 | **100** | dot |
| C, depth 0 | **84** | slash |
| C, depth 1 | **93** | dot |
| C, depth 2 | **102** | dot |
| G, depth 0 | **88** | slash |
| G, depth 2 | **106** | dot |

These are **new candidate-specific forecasts** conditional on the after-inspection balance assumption. They must be kept separate from Experiment 458's previously frozen model-family predictions. A later observation of any opposing symbol would falsify this exact `A∩B∩S+3/3/3` pair, not all Q4 readings. No owner outreach required or requested.

The two masters differ only at residues **22 and 25**, which provide a direct two-way resolution of their complete codes but **do not change the selected-depth output**. This is a useful distinction: a physical discriminator can distinguish manufacturing/code variants without distinguishing their downstream alleged message.

### Should this now be preferred?

**No.** A 3/3/3 depth census is an invented elegant restriction. Under the accepted one-slash condition, it happens in 2/18 possible Q4 codes, but choosing that symmetry because it is humanly attractive does not turn the 2/18 ratio into a statistical discovery. The result becomes interesting if a source or an independently discovered operation *uses three balanced depths*, if a new physical sticker supports this exact frozen pair, or if its invariant 27-mark output reaches a separately checkable consumer.

It also creates a real conflict with the simple R criterion. That is useful because it forces a substantive *choice of theories* rather than endless algebraic strengthening of one incumbent architecture.

## CL-02 v3: can the invariant 27-symbol readout be recognized in historical printers?

The answer-assisted balanced-selector theory produces this single three-row word across both surviving full masters:

```
-/-////-/
-//////--
/--///-//
```

It has **nine dashes** among 27 positions, partly because the *selected-depth rule itself demands three dashes per quarter*. Reading each class vertically across Q1/Q2/Q3 produces these triples:

| Class | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| Q1/Q2/Q3 | `--/` | `//-` | `-/-` | `///` | `///` | `///` | `//-` | `--/` | `/-/` |

The equal classes (A/H, B/G, D/E/F) look intriguing as geometry; they are still outputs of two rules chosen from the same corpus. In a physical 3×3 grid the classes that *never* carry a selected dash are D/E/F; the classes selected twice are A/C/H, and those selected once are B/G/I. These three groups are merely a consequence to investigate, not a newly discovered independent glyph alphabet.

**Provisional consumer guess:** perhaps the 27 symbols are a contiguous fragment of an already-known PC/PS4 or Xbox printer line, instead of a completely new plaintext. This is a human-scale target-assisted suggestion; the original printer strings are known beforehand, and there is no authorial alignment cue.

The [matched-null printer comparison](../../scripts/conjecture_lab_printer_substring_control.py) checks all 27-character contiguous windows in the **32 published 32-character PC/PS4 printer rows** and **36 listed 36-character Xbox rows** (552 windows total), accepting forward, reversed, symbol-inverted, and inverted-reversed views. The closest match differs at **six of 27 marks**, and **there are zero exact matches**. In a seeded control of 4,000 uniformly reordered nine-dash candidate strings with the *same four allowed variants* and same 552 target windows, **2,705/4,000 (67.625%)** match at least as closely. Hence the six-mismatch nearest match is mundane under this permissive exploratory search.

**Disposition:** the fixed 27-symbol readout cannot be an unchanged 27-symbol segment of those archived full printer lines under these four conventions. Reordering several rows, combining image layers, adding a source-specific transform, or using other original printer material remains untested. The source-controlled near-match does not confer any evidence for the balanced-tail conjecture.

## Next speculative directions now enabled

1. **CL-02 v3, output-as-seed:** provisionally treat the *fixed* 27-mark readout as three nine-cell data layers, not as a text or lever password. Try exactly a few human-plausible three-stage image/readout rules (native A–I 3×3 arrangement; three 3×3 bitmap panels; positions of the nine dashes). Label operations invented and test whether their output predicts a previously unseen feature of the 534brn page or cover. Never optimize alignments to familiar source art and then claim independent confirmation.
2. **CL-01 v3, source requirement:** test whether any authenticated original INSIDE/Terminal41 artifact offers a 512-slot indexed atlas, three-channel data fields, or a genuine nine-record address reader. Do not treat a random image of width 512 or a source containing 512 bytes as sufficient.
3. **Adversarial human pathway:** the balance hypothesis is easier to explain to a human than two recursive substitutions, but the particular selected-depth one-dash criterion remains unmotivated by external instructions. Write the *actual rule-delivery mechanism* that would allow a 2019 solver to know when and why to apply both assumptions.
4. **Control:** keep the unchanged source-first receiver audit and the no-further-endgame hypothesis in competition. Existing falsifications and null controls have not been superseded.

## Reproducibility and negative scope

```sh
python scripts/conjecture_lab_raw_bounds_balanced_tail.py
```

The script asserts the current 84/66 observations, the 74 archive-path inventory, all four raw-only address bounds, the Experiment-450 parent intersections, the two selector codes, the fixed output, and the exact two missing-body differences. Any new sticker evidence should cause a review of the frozen run rather than silently updating these assertions. This is not a new numbered canonical experiment or externally decoded plaintext.

# CL-OPS-03: three-bit A–I register with tail-directed one-site edits

_14 October 2026. DISCOVER / conditional DEVELOP. **No new sticker observation, decoded word, authenticated Playdead instruction, valid program, or unique completion claimed.**_

## Why this test

The 27 last positions (slash/dot) could command a process on the 81 earlier slash/dash positions, rather than provide a final picture. This follows the banner-font negative [CL-BANNER-03](2026-10-14-multisymbol-glyphs/README.md). The older [CL-OPS-02](2026-10-12-nine-trit-stream-and-selector-control.md) already tested whether tail trits rotate or shift **whole nine-bit body classes between classes**, with every version failing. **Here the hypothesis is different**: within *each fixed A–I image class*, its nine early positions are read as three successive three-bit states; the same operation executes twice *within that class*, with the final three slash/dot positions supplying a single one-of-three write address. This has physically testable consequences independently of any output word.

The physical corpus is **84 sticker records, 66 H108 distinct residues, including 36 slashes, 22 dashes, eight dots and 42 unknown sites**. The eighth dot is sticker 427 at residue 103. Source is the unmodified [physical observations](../../data/observations.csv). Residue 045 remains unconfirmed; it is **not** imported.

## Independent structural obstruction (before selecting an op dictionary)

Read original modulo-nine image class **C** at residues:

- row 0: 003, 012, 021 => **---** (all physically known);
- row 1: 030, 039, 048 => **///** (all physically known);
- row 2: 057, 066, 075 => **-/-** (all physically known).

A register that begins with a uniform three-bit state and applies **only a coordinate permutation and optionally a uniform complement** must remain uniform after any number of applications. It can change \`---\` into \`///\`, but **cannot** then produce \`-/-\`. Thus **every pure rotation, reflection, strided shuffle or global-inversion-only *generative* controller within this fixed A–I class / three-phase geometry is already contradicted**, even if its operation may vary by class or phase. This proof does not depend on the one-slash-per-tail-class hypothesis.

The proof does **not** exclude free literal bits at every step, nonuniform write masks, data-dependent local operators, different geometric groupings, selectors used only for a readout, or an entirely different type of puzzle.

## The bounded follow-on: one addressed bit can change

Under the **conditional** one-slash-per-class tail grammar, there are exactly **18** physically compatible selector combinations for the nine classes. A selector is a depth \`s in {0,1,2}\` for its class; physical observations constrain some but not all selectors. Unknowns are never filled in the observations.

A hypothetical three-bit register starts from a freely chosen three-bit seed **separately for each class**, then performs two transitions. A *single globally shared* rule across all nine classes consists of:

- \`p\` = one of six coordinate permutations of three positions;
- \`c\` = either no complement or global bitwise complement;
- \`(w1,w2)\` = one of \`00, 10, 01, 11\`: whether the addressed bit \`s\` is toggled immediately after applying \`p,c\` in transition 1 and transition 2.

Formally, \`state[t+1][i] = state[t][p[i]] XOR c XOR (w[t] AND (i==s))\`. No symbol is silently repaired. In total this is **6 × 2 × 4 = 48 global codebooks**. For each one, every compatible selector and every one of eight starting states is evaluated *exactly*, and the minimum number of contradictions with the 54 physically known body positions is counted.

### Results

| Write schedule | Lowest physical contradiction count |
| --- | ---: |
| Neither transition, \`00\` | **9** |
| First only, \`10\` | **7** |
| Second only, \`01\` | **9** |
| Both transitions, \`11\` | **4** |

No valid zero-conflict program exists anywhere in this 48-model family. The winning *near miss* is the single fixed permutation \`p=(2,0,1)\` (cyclic reindex), **no complement**, and a write to the tail-selected position after **both** transitions. It disagrees with existing physical observations at **012, 039, 051 and 072**. Those numbers are **contradictions**, never missing-site predictions or evidence to replace.

The four contradictions are spread across A–I classes **C (two), F (one), I (one)**; the other classes have physically compatible *local* seeds and selector settings under this **global-but-fitted** codebook. Local fits are conditional witnesses for the invalid overall program, not source-authored completions.

### Matched nulls: 10,000 runs per design

Hold the observed tail data and the exact physical missing-site mask fixed. Permute **known slash/dash labels only within the named grouping** and re-select the lowest physical contradiction count across the *same 48 codebooks*, all tail-compatible selectors and local seeds for every null sample.

| Null grouping | Controls with best contradictions ≤ observed four | Tail fraction |
| --- | ---: | ---: |
| Nine complete nine-site **A–I class body words** | **304/10,000** | 3.04% |
| Nine consecutive **serial nine-site frames** | **387/10,000** | 3.87% |
| 27 fixed **three-site class states** | **187/10,000** | 1.87% |

These are modest **retrospective near-fit signals**, conditioned on these selected nulls. They are emphatically **not a 1.87% probability of chance or evidence Playdead used this language**. The hypothesis family, framing and decision to permit a one-bit write were chosen after looking at the corpus, including the decisive class-C counterexample; the shuffles only correct for the 48-model selection *within this family*, not for the preceding and ongoing search across many families. Also, all 48 programs are already **strictly falsified as exact decoders**.

The tight three-site null is important: it preserves the physical slash/dash census **within each three-bit state**, so a score advantage cannot be credited merely to each state's observed symbol-count distribution. But it does not preserve all other possible machine constraints or tell us which source operation is intended.

## Decision and next test

This is a strong **negative** for any fixed, value-uniform 3-bit permutation/complement generator in the natural class-local three-phase geometry. Letting the tail select a *write site* makes the observed evidence closer to a consistent two-transition mechanism, but **still cannot explain the physical code**. Introducing further arbitrary exceptions to erase the four contradictions would be overfitting; do **not** extend the grammar just because it almost fits.

A genuine next opening requires one of:

1. An **independent source-authored write/erase/toggle operation** or orientation/ordering instruction, recoverable from the Collector's Edition cover, printer, 534brn HTML, game, or surrounding historical puzzle.
2. A separate **readout consumer/output constraint** for the class-state words that can score meaningfully without generic letter-fitting.
3. A specific **new physical sticker** validating a frozen, separately motivated model. Never change residue 012/039/051/072 because an invented controller disagrees.

The class-C proof also supplies a simple human-level discriminator for proposed mechanisms: **does the rule ever introduce nonuniformity into a uniform state?** If not, it cannot generate all three class-C phases here.

## Reproduce and audit

[Executable Python](../../scripts/conjecture_lab_intra_class_write_controller.py), standard library only. It checks exact physical counts and the C class witness, exhaustively enumerates all 48 global programs and class-local eight-seed start states, asserts the optimum and the four error residues, and reruns three independently seeded null families.

Run from repository root:

    python scripts/conjecture_lab_intra_class_write_controller.py --test
    python scripts/conjecture_lab_intra_class_write_controller.py --null-replicates 10000 --output data/conjecture-lab-intra-class-write-controller-2026-10-14.json

[Archived machine-readable control histograms](../../data/conjecture-lab-intra-class-write-controller-2026-10-14.json) preserve the exact results and falsifying residues. No changes were made to \`data/observations.csv\`, to older numbered experiment results, or to any prediction matrix.
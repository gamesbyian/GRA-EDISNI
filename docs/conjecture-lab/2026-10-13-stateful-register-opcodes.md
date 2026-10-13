# CL-VLEN-08/09: The CE foreground as an executable nine-register program

_13 October 2026. Two independent DEVELOP experiments, with exact structural impossibilities and selection-aware negative controls. No new sticker observation, Playdead opcode, password or genuine consumer identified._

## Motivating player-level conjecture

A useful alternative to plaintext is a **tiny machine that operates on previous and subsequent sticker groups**. Assemble the nine faint A–I background images, treat each as the name of a nine-bit register, and let its three late slash/dot marks select one operation. Executing those nine instructions transforms the currently held register into the next one, following the cyclic class sequence A→B→C→D→E→F→G→H→I→A. Because the physically assembled art is `IAB/CDE/FGH`, its cyclic row-major traversal I→A→…→H→I has the same adjacent transitions, merely rotating the start. A class's 9-bit value is not assumed to encode a letter. An operation might *move, mirror, invert, erase, overwrite or combine* prior marks.

**Explicit assumptions:** Alphabetical/cyclic class execution, each tail triple selecting exactly one of three commands, one globally shared command dictionary and no extra printed opcode legend are **invented interpretations**, not established Playdead facts. Class H's last three symbols `. . ?` and class I's `. ? /` force selector position 2 under the one-slash hypothesis. That factual conditional detail gives surprisingly short impossibility proofs.

**Physical corpus:** `data/observations.csv`: 84 confirmed records, 66 distinct H108 positions and 42 unobserved. First 81 body positions are slash/dash; last 27 control positions slash/dot. All physical absences are variables, never replaced with inferred truths. A notable feature of the raw record: class **B has 8/9 body sites observed** and class **C has 9/9**, making class-to-class transformations much more testable than arbitrary global 108-bit readings.

## CL-VLEN-08: reversible nine-bit state operations

**Fully specified machine:** Let each nine-bit body field be a state `S[A]` to `S[I]`. Commands are chosen from eight predeclared **global, source-free transformations**:

- Identity;
- Invert all nine bits;
- Cyclic shift by +1 or -1 site;
- Cyclic shift by +3 or -3 sites;
- Rotate its 3×3 site arrangement by 90 degrees;
- Reflect the 3×3 site arrangement.

Choose three **distinct** primitives and assign them to the three selector positions, giving `8×7×6 = 336` full dictionaries. Every chosen command must map the *whole* nine-bit current state to the next class's nine-bit state. Exhaustively enumerate the 512 possible nine-bit states where necessary, all 18 physically possible one-hot tail choices and all 336 dictionaries. This is a stateful program, not nine separate icon decodings. Test code independently verifies shift inverses, 3×3 geometric identities and synthetic nine-class programs.

**Exact outcome:** **0/336** dictionaries permit any full physically compatible cyclic execution. Matched shuffles of the 54 observed body labels, preserving exact observed-position masks and preserving label counts within their nine-site frames, within each class or across the whole 81-body region, yield **0 survivors in every one of 250 shuffles for each of the three controls**. This is an exact rejection of these reversible dictionary candidates, but *not an exceptional difference from shuffled observations*.

**A simpler and stronger proof:** Class B's nine-bit body `/ ? / / / / / / -` has **7 or 8 slash bits**. Class C's fully observed `- - - / / / - / -` has **exactly 4**. Every proposed operation either preserves Hamming weight, giving 7/8, or bitwise complements, giving 2/1. Consequently *no allowed command can implement even B→C*. This proof eliminates all 336 dictionaries and **does not depend on any one-hot tail assumption**, beyond the broader existence of some command mapping the complete state. Nor does it require new physical stickers.

**Important boundary:** Shift, rotation, mirror and invert do not erase or create arbitrary marks. Any credible nine-register interpreter needs a genuinely information-changing operation, an external operand, class-dependent masks, or some other mechanism that changes more than ordering and polarity. A single global reversible pixel-shuffler cannot do it.

## CL-VLEN-09: a more expressive stateful three-opcode XOR-mask language

Relax the weight-conservation restriction *generously*. Define **three arbitrary nine-bit masks**, `M0`, `M1`, `M2`. Under selector `k[j]`, execute:

`S[(j+1) mod 9] = S[j] XOR M[k[j]]`

A global mask can toggle many bits simultaneously; its nine values are **unknown variables**, not optimized from an English target or imported from U2/U5. All three masks must be shared across classes and the program must close after nine instructions. Under 18 physically allowed tail selector completions, this can be solved **exactly**, independently for each of the nine body-bit positions, as a 12-variable GF(2) system (9 class-state variables plus 3 mask bits). Gaussian elimination preserves every observed known mark. Rank accounting correctly conditions on the mandatory nine-command cycle rather than treating its closure as an independent positive signal.

**Exact outcome:** **0/18** tail selector completions can give a physically consistent nine-class program even with free 27-bit global XOR opcode parameters. The most permissive selector completion satisfies only **2 of 9** independent body-position systems. Across 250 frame-preserving, 250 class-preserving and 250 region-preserving body-symbol shuffles, **all** controls also have zero completely compatible programs. The negative is structurally common within this overconstrained code grammar, not independent corroboration of Playdead's chosen mechanism.

### A remarkably short, prospective-independent contradiction

There is an even simpler mathematical proof applicable to **any globally shared self-inverse command**, not merely XOR:

1. Under the one-slash class-tail conjecture, **H** has two observed dots in tail positions 0 and 1, so its selector must be 2. **I** has an observed dot in tail position 0 and observed slash in tail position 2, so its selector must also be 2.
2. Consecutive cyclic transitions H→I and I→A therefore execute *the same command twice*.
3. Suppose command 2 is an involution, `O₂(O₂(S)) = S`. This holds for fixed XOR masks, complements, reflections and many simple swap operations.
4. It necessarily predicts `S[A] = S[H]` at **all nine corresponding body positions**.
5. Directly observed **residue 10 = dash** (class A, second body position) and **residue 17 = slash** (class H, the same body position) already contradict that equality.

Only those **two body-site observations** are needed after adopting the two selectors and the cyclic execution assumption. This does **not** depend on 42 missing stickers, a selected full-word completion, or any guessed output. The result licenses a focused prediction about the type of instruction language: at least this twice-repeated command cannot be a simple involution, *unless* execution order or operand behavior differs from the posited model.

## What these negatives actually suggest (DEVELOP)

A productive program would need to escape both impossibility mechanisms in a principled manner, not by adding free parameters until something reads English:

1. **Three-cycle relative operators.** A 120-degree rotation, mod-3 shift, trit increment or 3-way router is *not* an involution. When H and I both issue command 2, applying it twice can change the state rather than restore it. This is one reason a ternary instruction machine deserves continued testing. But the B→C count obstruction still applies if operations are pure permutations on nine binary positions, so something must also write/erase/change value.
2. **Write or combine operations.** Operations such as `S' = ROT(S) XOR DATA`, `S' = S AND MASK`, or `S' = S XOR (S shifted by three)` can change Hamming weight. An operand may be encoded in the remaining two 3-bit body segments or supplied by an original ARG artifact. Pin the source of every operand before treating any model fit as evidence.
3. **Address-dependent instructions.** Rather than transforming body B into body C exactly, the command can tell the reader *where to go* within the previously solved background mosaic, printer image or damaged `534brn` page. CL-VLEN-07 tested one explicitly invented nine-room torus route, and it was not exceptional, but it has a much clearer authentic-consumer path than unconstrained plaintext fishing.
4. **Direction- or stack-dependent command meaning.** An opcode can refer backward, forward, or to a previous decoder configuration. The same glyph at H and I then need not be the same involutive transformation because state or operands differ. Such a model should specify state initialization, termination and a true physical holdout check.
5. **No further foreground endgame.** The entire command-machine story might be elegant fiction. Keep that alternative as a live control while source archaeology seeks an actual receiving artifact.

**Avoid the false inference:** The shared B→C weight contradiction only refutes *complete-state permutation/inversion generators*. The H/I two-step argument only refutes *same-command self-inverse* execution under a cyclic class traversal. Neither refutes sequential code, finite-state transducers, prefix-coded integer streams, 3×3 overlays, relative graphics commands, arbitrary affine transducers or an independent game/software receiver.

## Reproducibility

```sh
python scripts/conjecture_lab_stateful_classes.py --test
python scripts/conjecture_lab_stateful_classes.py --nulls 250 --output data/conjecture-lab-stateful-classes-2026-10-13.json
python scripts/conjecture_lab_xor_commands.py --test
python scripts/conjecture_lab_xor_commands.py --nulls 250 --output data/conjecture-lab-xor-commands-2026-10-13.json
```

Both programs use only the Python standard library, read raw physical observations, fail loudly if the base physical snapshot or synthetic invariants drift, and produce deterministic structured results. The XOR workbench checks exact GF(2) rank, an inconsistent synthetic data fixture, a compatible fixed synthetic program and the small H/I→A involution witness. Full experiment data preserve all selected conditional assumptions, matched-null counts and incompatibilities.

**Disposition:** No decoded CE message or commands. But the physical sample is already sufficiently informative to make *specific*, falsifiable statements about whole classes of executable languages. Continued research should use that power, without requiring another owner photograph as a prerequisite.
# CL-VLEN-11–16: from stateful instructions to the minimum-edit nine-picture tape

*13 October 2026. DISCOVER and DEVELOP. This report is a conditional research programme, **not** a solved CE sticker code, an independent validation, or a new physical sticker observation.*

## The move this campaign makes

Earlier VLEN investigations tested variable 3/5-wide tokens, unary run lengths, one-hot tail selectors, reference back, copying, inversion, basic recurrence and whole-register transformations. The negative results did **not** exclude genuinely contextual instructions: the same opcode could write different bits depending on the previous or current register, or a command could modify the next command's interpretation. Rather than presume the payload is words, this campaign implements three genuinely modifying languages and measures a source-adjacent lower-complexity possibility.

**Carrier and normalization:** Only `data/observations.csv` is used: 84 independently recorded physical observations, 66 distinct H108 residues, 42 unknown positions. Nine A–I *body* words each have nine slash/dash positions; corresponding *tail* triples use slash/dot. The nine-class cycle also matches the community-assembled image order `IAB/CDE/FGH` after a cyclic rotation, but **a cyclic executor is a conjecture**, not an authored instruction. Exactly 18 class-tail one-slash selector vectors are compatible with the current physical observations. They are an optional *conditional* ingredient in the first three experiments, never an observation.

All test scripts use only known raw glyphs. Model-completed bits remain *conditional witness values* and are never written to the physical ledger. Source-native authorial cues and endgame receivers remain missing.

## CL-VLEN-11: two-register context-dependent XOR commands

Machine: the nine A–I words are nine-bit registers. At each class, its selected tail position chooses a read offset from one of five simple triples: `(-1,0,1)`, `(0,1,2)`, `(0,3,6)`, `(-3,0,3)`, `(0,1,3)`. Four distinct bitwise recurrences depend on the current and previous registers. Each is tested forward/reverse and with/without a global complement constant, for **5 × 4 × 2 × 2 × 18 = 1,440** fully enumerated conditional programs. Because the rules are XOR-linear, a standard-library GF(2) elimination algorithm enforces every physical body mark exactly; its independent small-matrix brute-force oracle is included.

**Result:** **0/1,440** programs can match all 54 physically known body marks and cyclic closure. In **25** native-nine-frame shuffles and **25** within-class-count shuffles, none has a compatible program either; zero acceptance is not exceptional under these severe restrictions. This family specifically escapes the old H→I→A involution objection because opcodes consume changing operands, but still fails for other exact observed constraints. No broader stateful-language rejection follows.

Files: [code](../../scripts/conjecture_lab_contextual_feedback.py), [machine-readable result](../../data/conjecture-lab-contextual-feedback-2026-10-13.json).

## CL-VLEN-12: nonlinear nine-bit write programmes, anchored by known class C

Class **C has all nine** slash/dash body marks physically observed (`---///-/-`). This permits a complete initial register without any imputation. Each transition applies one of **all 256 three-input elementary Boolean rules** to neighbouring register bits. The current class's tail selector chooses the neighbourhood's centre displacement (`-1`, `0`, `+1`), under all six assignments of those moves to selector positions, cyclic/open nine-bit boundaries, forward/reverse class order and 18 tail-selector completions. **256 × 6 × 2 × 2 × 18 = 110,592** candidate programs, simulated through a full nine-class cycle. Rule 110 is included, not privileged.

**Result:** **0/110,592** complete programmes satisfy all photographed body marks. The lowest-retrospectively-fitted candidate makes **12** directly observed bit errors. Across 20 frame-preserving label shuffles **17/20** score at least as well, and across 20 class-preserving shuffles **16/20** score at least as well. The 256-rule nonlinear semantics were separately verified against a scalar interpreter for hundreds of random states; vectorized execution uses NumPy, a **research-only optional dependency**, not a new core repository requirement.

Files: [code](../../scripts/conjecture_lab_nonlinear_register.py), [results](../../data/conjecture-lab-nonlinear-register-2026-10-13.json).

## CL-VLEN-13: a small numeric register machine with operands

Give the class-tail selector a numeric *immediate* from five predeclared offset triples, with all six opcode label permutations. The next nine-bit register is calculated from the previous **two** registers, using modular addition, subtraction, XOR or rotated-operand combinations, all modulo 512. The fully known class C anchors execution; the predecessor B in forward order has only one unknown bit, and D in reverse order has four. Enumerate these as possibilities, not fabricated observations. Demand the program finish a true closed cycle, including agreement with the *same exact predecessor state*, not merely its observed mask.

**Result:** 77,760 complete programs across these formats; **zero exact fits**. Closest candidate incurs **12 bit-level errors** under the declared scoring scheme, including exact-cycle closure. Of 16 class-preserving shuffled controls, 3 tie or exceed this best; of 16 original-nine-frame shuffles, 6 tie or exceed. These are limited descriptive controls, not calibrated global hypothesis probabilities. Notice that allowing *two changing operands and actual arithmetic writes* still does not by itself produce a correct raw readout.

Files: [code](../../scripts/conjecture_lab_arithmetic_vm.py), [results](../../data/conjecture-lab-arithmetic-vm-2026-10-13.json).

## CL-VLEN-14: unusually economical A–I tape edits

Instead of guessing an instruction dictionary, ask a direct complexity question: treat each class's nine-bit body as the state of a nine-track tape and require each successive class to be obtained by individually writing/erasing bits at fixed depth positions. How few total writes are required for a **closed** A→B→C→D→E→F→G→H→I→A cycle, using *any* fillings of currently missing stickers?

This is exactly decomposable over each of nine body-depth columns. For every depth, enumerate all `2^9 = 512` possible class-bit patterns, retain those compatible with direct observations and count circular 0↔1 transitions. Add their minima. There is no use of U2, U5 or any conditional completion family.

- **Exact minimum total writes: 20**, with **48** mathematically minimizing complete 81-bit body objects.
- The nine depth-column minimum costs are **2/4/2/2/2/2/2/2/2** (sum 20).
- Under that *invented minimum-write* prior, 21 of 27 missing early physical foreground marks would be fixed, and six remain ambiguous across the 48 optima. These are **conditional conjecture predictions, not confirmed stickers**.
- **10,000** shuffles retaining each original nine-site frame's observed mask and symbol counts: mean minimum cost **26.4258**; only **162/10,000** obtain cost ≤20.
- **10,000** shuffles retaining each background class's mask and counts: mean **27.0024**; only **383/10,000** obtain cost ≤20.

These measures were **chosen after many other grammar experiments**. Therefore the raw tail frequencies **do not constitute pre-registered discovery p-values**; nor are the two shuffle controls independent evidence. Nonetheless this is a potentially useful *descriptive* structural fact because it uses the original class order rather than selecting a reordered stream for smoothness.

**Adversarial physical holdout:** hide each of the **54 known body positions**, recompute all minimum-cost completions and use the exact fraction predicting slash. The mean Brier squared error is **0.26353**, with **five zero-probability wrong calls**. A simple leave-one-out Laplace-smoothed global slash-frequency baseline has Brier **0.25030**, *better than this edit decoder*. Among 1,000 independently shuffled presentations, only 16 frame-shuffles and 18 class-shuffles obtain holdout Brier as low as the real corpus's. That means a structural correlation may be present but **not yet an adequate predictive decoder**, and raw acceptance/compression are not substitutes for this failure.

Files: [exact bit-tape DP](../../scripts/conjecture_lab_minimal_tape_edits.py), [full observations, 48-completion constraints and 10k controls](../../data/conjecture-lab-minimal-tape-edits-2026-10-13.json), [LOO controls](../../scripts/conjecture_lab_tape_validation.py) and [LOO results](../../data/conjecture-lab-tape-holdout-2026-10-13.json).

## CL-VLEN-15: does the independently given class order matter?

Fix A as the cycle's starting class, and identify a circular order with its reverse. Exactly `(9-1)!/2 = 20,160` distinct class cycles remain. Score each against exactly the same known glyphs with the same minimum-edit metric (no grammar fitting or missing-sticker imputation). The actual A→…→I→A order scores **20**; **46** alternate cycles score strictly better (18), and another **360** tie it. Thus **406/20,160 = 2.014%** score at least as well. The community art's row-major `IAB/CDE/FGH` is merely a cyclic rotation of the native class order, not a newly optimized order.

Removing each entire class before scanning 8-class cycles gives sensitivity counts among 2,520 unoriented orders: A **223**, B **230**, C **523**, D **56**, E **10**, F **305**, G **114**, H **521**, I **149** tie or beat the natural order. Several classes matter more than others; the effect is not completely uniform across the corpus. Among eight distinct orientations/boustrophedon readings of the 3×3 mosaic tested, source row-major/reverse is lowest (20), while alternatives score 22–30. Those additional comparisons are also exploratory and correlated.

Files: [exhaustive order rank script](../../scripts/conjecture_lab_tape_order_rank.py), [complete order distribution](../../data/conjecture-lab-tape-order-rank-2026-10-13.json).

## CL-VLEN-16: how large must each edit instruction be?

Now require that no transition may write more than `k` of nine bits. This is an **exact** 512-state reachability program anchored by fully observed C, carried through all nine classes to exactly the starting C state. All 512 possible states are maintained according to physical observations, rather than selecting a U2/U5 completion.

- `k=0`, `1`, `2`: fail; `k=3` **fails at the D→E transition** after reaching D from C.
- `k=4`: **works**. The minimum total writes even under that per-step budget remains exactly **20**.
- One mathematically compatible 20-write witness across A→I requires per-step edits **3, 3, 4, 4, 1, 1, 1, 1, 2**. Its register contents are documented in JSON, not promoted to new photographed marks.
- Matched controls (100 each) find `k≤4` in **56/100** frame-shuffles and **53/100** class-shuffles, so a four-write step budget itself is not exceptional.

An even sharper physical local witness: B→C must change at least **three observed positions**, at within-word indices **0, 2 and 6**. These three positions lie in no single ordinary row, column or diagonal of a 3×3 layout. A tail command that edits *only one entire 3-cell row, column or diagonal* therefore **cannot** implement this transition, irrespective of the missing stickers.

Files: [exact bounded-writer DP](../../scripts/conjecture_lab_bounded_writer.py) and [results](../../data/conjecture-lab-bounded-writer-2026-10-13.json).

## Three speculative player experiences worth making executable next

**A. The self-modifying printhead.** Imagine placing the nine reconstructed CE miniatures in their `IAB/CDE/FGH` grid. The foreground at each background class is a nine-position printable state. The three late symbols might not select a letter; they could choose *a class of write operations*, while preceding runs of lengths three or five supply a **write-address and byte mask**. A player moves through the nine images, writing at most four pixels per step until the tape returns to its initial state. It would explain the natural nine-class order and the observed 20-write economy. The invented bridge is the address decoder: without an actual Playdead drawing, cover marking or on-screen handler specifying how to choose writable sites, the programme is too flexible. A genuine solution should prescribe one unique 20-write witness (or a different source-fixed count) **without optimizing against the known stickers**.

**B. The nine-station transmitter.** Each sticker class is a station transmitting a nine-bit packet; the 27 tail symbols could choose how packets *differentially update* one another. The unknown foreground bits might then be recovered by a parity or short error-correcting programme. Pure XOR feedback and uniform checksum grammars were already excluded by their exact physical contradictions. A productive revival needs an independent *nonlinear* receiver that uses an unobserved source operand, not a free table of 512 instructions. Test whether `534brn`'s original source physically supplies one.

**C. Instructions acting on the reader, not on the stickers.** The endgame could instead use the classes as an order in which to operate on the **already-solved CE background**, the authentic original 32×32 printer artwork or the damaged `534brn` file. Under this story 20 could be a side effect of manufacturing a registered command stream, not a target. Recover a source-native 9-slot or 27-slot input affordance, and test it without completing unobserved sticker symbols to fit the answer.

## Unresolved and frozen boundaries

- This campaign does **not** establish that Playdead used edit distance, wrote 20 bits, or intended the A–I layout as a temporal programme. It establishes an exact *raw-corpus statistic* and its sensitivity to chosen controls.
- Holdout prediction is **worse than a trivial marginal-frequency baseline**; do not add the 21 tentative predictions to the physical register or treat their certainty under one optimization objective as independent validation.
- The many tested grammars and many prior experiments make nominal lower-tail frequencies vulnerable to selection effects. Future VALIDATE work needs an actual external cue or untouched prediction; a new 108-word model selected because it scores 18 changes instead of 20 is not evidence.
- Native source archaeology should seek a *functioning consumer*, a 9×9 alignment cue, bit-writing/change notation, a four-wide write capacity, or a command for iterating A–I pictures. These must pre-exist and be authenticated rather than fabricated post hoc.

### Reproduction

```sh
python scripts/conjecture_lab_contextual_feedback.py --test
python scripts/conjecture_lab_contextual_feedback.py --shuffles 25
python scripts/conjecture_lab_nonlinear_register.py --test   # research-only numpy dependency
python scripts/conjecture_lab_nonlinear_register.py --nulls 20
python scripts/conjecture_lab_arithmetic_vm.py --test
python scripts/conjecture_lab_arithmetic_vm.py --nulls 16
python scripts/conjecture_lab_minimal_tape_edits.py --test
python scripts/conjecture_lab_minimal_tape_edits.py --nulls 10000
python scripts/conjecture_lab_tape_validation.py --nulls 1000
python scripts/conjecture_lab_tape_order_rank.py
python scripts/conjecture_lab_bounded_writer.py --test
python scripts/conjecture_lab_bounded_writer.py --nulls 100
```

All reports are deterministic with fixed random seeds and standard-library scripts except for the research-only NumPy nonlinear class-writer. Scripts assert canonical observation volume/masks. No CI expansion was added, to avoid multiplying Actions workload while independent agents are using the repository.
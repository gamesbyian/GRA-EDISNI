# CL-VLEN-05/06: CE classes as packets, and four 27-cell machine states

_13 October 2026, exploratory DISCOVER/DEVELOP. No claimed recovered CE decoder, no new observation and no Playdead-sourced command dictionary._

## Why change the questions?

The previous CL-VLEN-01–04 models demonstrated that readily invented command languages parse many completions but are not independently validated. More interesting is whether the apparent *format* of the sticker carriers can be the decoder's grammar. These two experiments make a deliberately optimistic conditional assumption, construct real encoders or executable machines from it, and then subject those exact models to unfriendly matched controls. They do not reuse U2/U5 completions or a hidden target string.

**Physical snapshot:** `data/observations.csv`, 84 records, 66 unique residues and 42 unknown H108 positions. Body 1–81 contains 54 observed slash/dash marks; tail 82–108 has 12 observed slash/dot marks. The alternate binary interpretation slash=1, dash/dot=0 is imposed for these counterfactuals only. Distinct glyphs are retained as raw source data. Faint background class labels A–I provide an independently observed way to gather each class's 9 body sites and 3 tail sites.

## CL-VLEN-05: nine data marks plus three check/control marks

**Adopted hunch (INVENTED BRIDGE):** Each class is a systematic `(12,9)` data/check packet. Imagine the three late marks are the result of a 3-input Boolean operator on rows or columns of the nine earlier marks. Every class uses the *same* operation, even when the values differ. A purchaser who recognizes nine repeated background pictures could regroup stickers accordingly. This is a credible possible *form*, not a source-authenticated code family.

**Frozen search:** 144 choices: physical 3×3 body read by three rows or three columns; three phase offsets; XOR, majority, OR, AND, exactly-one and all-equal; two data polarities; two tail polarities. For each class, enumerate **all 512 nine-bit bodies**, calculate the proposed three tail output bits and count only complete states agreeing with known physical marks. Independent truth-table assertions test all 144 × 512 cases. There is no use of the machine-derived sticker completions.

**Results:** exactly **2/144** formatted descriptions satisfy all physically known marks. They are polarity-equivalent versions of the same shifted-column XOR packet. The nominal selected best model has log2 Bayes factor **+3 bits** (eightfold evidence against unconstrained independent-body-and-tail *for that prechosen model*, not after selection among 144 models). Specifically, its allowable whole-nine-bit body counts by background class A–I are **32 / 1 / 1 / 4 / 8 / 2 / 16 / 4 / 2**. This is an attractive partial completion exercise, not a discovery.

Matched shuffles keep the original observed-position mask while preserving observed symbol counts at different levels, and rerun the *entire 144-model selection* each time (400 fixed-seed replicates per control):

| Control | Shuffles with >=2 compatible models | Shuffles whose selected best Bayes factor >= actual |
| --- | ---: | ---: |
| Body each A–I class; tail each native 9-site frame | **251/400** | **253/400** |
| All twelve native 9-site frames | **250/400** | **266/400** |
| Original 81/27 alphabet regions | **280/400** | **291/400** |

The permitted packets are less remarkable than most shuffled competitors. Under **leave-one-known-observation-out** model refitting across all 66 unique residues, the selected grammar is trainable on every fold but assigns *zero* probability to the actual withheld mark in **11 of 66**, with Brier score **0.337121**. Thus even a compatible global XOR grammar can generalize poorly when chosen from a family after inspecting the physical sample. The 11 failures are meaningful failures of held-out predictive discrimination, **not** errors in the physical record.

**Exact scope:** Reject interpreting this particular surviving shifted-column XOR as supported by physical correlation. Other parity-check codes, Reed–Solomon-like symbols, CRCs, class-to-class checks or symbol ordering remain untested. Importantly, *absence of exceptional fit is not proof of absence of a real checksum*, particularly given 42 unknowns.

## CL-VLEN-06: 108 as four consecutive 27-cell automaton generations

**Adopted hunch (BORROWED ANALOGY + INVENTED BRIDGE):** Playdead's previously solved acorn/GAME OF LIFE instruction was an executable rule for transforming a carrier. The CE 108-symbol period has the exact shape **4 × 27**. Perhaps the 27 slash/dot marks are an initial or final state, with the 81 slash/dash marks representing three adjacent generations. Instead of asking whether 27 marks constitute plaintext, make them a *machine state*. This is an imaginative but non-presumed historical link: the real acorn puzzle operated on the original 32×32 PC printer image, whereas this hypothesis operates on a hypothetical 27-cell tape not authenticated anywhere else.

The script tests **all 256 Wolfram elementary cellular-automaton truth tables** with both cyclic and open-zero 27-cell topologies. It exhaustively fills unknown seed positions but never invents them as observations. It tests forward time Q0→Q1→Q2→Q3 and reverse time Q3→Q2→Q1→Q0, where each Q is a consecutive 27-symbol quarter. No hidden image, adjustable per-generation shift, arbitrary source byte or 128/41 magic number is fitted. A second independent scalar cellular-automaton implementation tests all 256 rules against vectorized evolution on both topologies.

The four quarters have **19 / 17 / 18 / 12** physically observed marks. Forward has only **2^8=256** admissible seeds, whereas reverse has **2^15=32,768**. The exact best-of-rule/seed/orientation results:

| Time | Topology | Known observations beyond seed | Fewest contradictions | Best original-rule ID |
| --- | --- | ---: | ---: | ---: |
| Q0→Q3 | Ring | 47 | **11** | 109 |
| Q0→Q3 | Open strip | 47 | **11** | 109 |
| Q3→Q0 | Ring | 54 | **9** | 110 |
| Q3→Q0 | Open strip | 54 | **11** | 77 |

**No rule/seed matches all directly observed marks** under these narrow models, so the literal "four consecutive elementary CA generations, fixed order, no intermediate transform" idea is impossible under the raw corpus. Merely guessing a familiar rule such as Rule 30 or Rule 110 cannot fix this contradiction. The best after inspecting 256 rules, two boundaries and both directions still misses nine already-known marks.

For each null sample, the original known-position mask is preserved and known symbols shuffled within either each original **nine-site frame** or each **27-site quarter**. The score is the fewest physical contradictions across **the same full selected rule/topology/direction/seed family**, not agreement with an output chosen after seeing it. Over 30 exploratory shuffles each, **16/30** frame-conditioned and **15/30** quarter-conditioned controls achieve *at least as good* a best-of-family score as the physical data. This is an intentionally small reference sample, sufficient to show the near-matches are not striking, **not** a calibrated population significance assertion.

**Exact scope:** The negative applies to direct four consecutive 1D ECA states in the specified natural registration. It does not close 2D Life, masked rather than entire states, unequal generation gaps, a 3×9 lattice, nonlinear stateful command streams, physical printer-art interaction or an original clue supplying the correct update rule. Those are legitimately different hypotheses, not exceptions smuggled into this failed model.

## Three imaginative but explicit machine narratives

The experiments support going deeper *without claiming discovery*:

1. **Postage-stamp instruction cards.** Nine faint pictures are not character backgrounds but **addresses** or registers. A class's three late marks select which of three nine-bit body subcircuits is an instruction; the other two could be operands. A command such as `ROTATE LEFT`, `SELECT NEXT BACKGROUND`, `READ PREVIOUS FRAME` or `REPAIR ONE MISSING BIT` can change how *later* classes are handled. A credible decoder must specify whether previous outputs are mutable, where execution starts, how cycles halt, and how it survives missing stickers. The earlier 160 literal copy/reverse/invert generator variants failed, so the next interpreter should have a genuinely changing program counter or state, not a rebadged identical transform.
2. **Error syndrome as a treasure-map coordinate.** Suppose the 27 late marks aren't 27 data bits, but nine 3-bit *syndromes* for nine 9-bit blocks, indexing *which of nine* earlier ARG objects or artifacts is to be combined with each foreground class. That demands an independent original nine-item array or native receiving device. Testing against arbitrary English words is weak; testing against a source-authenticated nine-object list is discriminating.
3. **A four-stage miniature printing press.** Four 27-position quarters might be not four outputs of one fixed ECA but four **layers or memory banks**. One quarter is the printhead program, two are working images and the last is a routing map. Original INSIDE puzzles demonstrated source-authorized geometric overlays and physical-controller instructions. Search specifically for original 27-slot, 3×9 or nine-by-three physical/software structures; only such a clue justifies a new family of program interpreters.

Other creative hypotheses worth pursuing **in parallel, not as restrictions**: a three-state turtle walker, reversible shift-register tape (including LFSR seeds), universal prefix integers, a stack of overloaded 3/5 commands, class-local CRC/check digits, a fixed 108-step musical/motion score, a nine-channel interleaver, a **self-referential packet** whose tail selects where its own header resides, one-character-of-nine-background pixel addressing, and a redaction/repair mask for the actual 534brn damaged JPEG. Each should have a concrete failure condition and an external consumer whenever possible.

## Next discriminating tests

- **Stateful 27→81 controller, not uniform copying:** implement class-local 3-bit opcodes that update a shared program counter/rotation or select *different* operations for subsequent classes. Enumerate termination and feedback consistently; demand a known-mark holdout and matched controls.
- **Mixed-width repair packet:** field widths 1/3/5 or Huffman/unary self-delimiting integers, where control bits select a currently active decoder for subsequent words. Evaluate on raw observations, never U5-only fillings.
- **Source-bound 3×9/27 geometry:** independent CE artwork, original PC/PS4 printer raster, 534brn page and official original packaging photos must supply a frozen registration before any fitted pixel readout counts as validation.
- **Error correction as a transmission design:** check a meaningful class of linear/cyclic BCH/CRC-like 81+27 codes with exactly computed rank and withheld predictive constraints, retaining nonuniform observation masks. Avoid arbitrary full-rank maps, which trivially fit.
- **Consumer-first original site archaeology:** preserve actual code/request contract for the historical Playdead printer field and Terminal41 archives, explicitly separating 2019 functional inputs from static pages. The native bunker lever is a real but *already solved* 14-action consumer.

## Reproduction

```sh
python scripts/conjecture_lab_class_ecc.py --test
python scripts/conjecture_lab_class_ecc.py --shuffles 400 --holdout --output data/conjecture-lab-class-ecc-2026-10-13.json
python scripts/conjecture_lab_27cell_ca.py --test
python scripts/conjecture_lab_27cell_ca.py --reverse --nulls 30 --output data/conjecture-lab-27cell-ca-2026-10-13.json
```

The standard-library checksum experiment and `numpy`-based 27-cell CA experiment are reproducible from `data/observations.csv`. Unlike the standard-library crypto scripts, the CA workbench requires `numpy >= 2` for `np.bitwise_count`; this work is **not** added as an unguarded dependency to the existing Python 3.12 core verify job. All local assert-driven truth-table/oracle checks passed. Both scripts read the exact original observations and generate JSON summaries with fixed seeds. Conditional fits are never promoted to physical evidence.

**Disposition:** Two new computational conjecture families explored, both with exact negatives and a conspicuous absence of a post-selection advantage. Continue with *genuinely stateful control flow* and especially *independent source-native receiving instructions*. Do not turn the matching shifted XOR packet or the CA rule-110 coincidence into new project premises.
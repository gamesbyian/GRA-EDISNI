# CL-VLEN-07: Nine pictures as rooms, selector trigrams as routing instructions

_13 October 2026. DISCOVER/DEVELOP; an explicitly invented decoder/receiver. It is not an authenticated INSIDE game area, code or route._

## A new use for the same physical object

The CE foreground accompanies nine independent faint image classes. The background's original, community-solved 3×3 registration **IAB / CDE / FGH** makes it possible to treat the nine picture classes as nine named *nodes*. The final three foreground positions in each class may act as one of three operations, using the historically explored conditional one-slash-per-class reading. Rather than interpreting any selected three bits as text, try giving the tail a *spatial action*.

**Conjectured player walkthrough (invented):** Assemble the already-solvable nine-picture mosaic, read one of three instructions associated with each image, walk from image to image according to the instructions, and record the resulting path. This would permit nine distributed sticker submessages to combine into a physical procedure, and it could operate without the complete 108-bit foreground. No original CE instruction has yet authorized the movement vocabulary, toroidal wrap, start tile or stopping rule.

## Frozen and executable control contract

1. Gather each A–I class's last three serial residues, at 82+j, 91+j and 100+j (j=0..8). Require **exactly one slash in each three-site class tail**, with the other two dots. This is an **adopted conjecture**; 18 completions are physically compatible after sticker 427, but earlier experiments found this compatibility weak against structural nulls.
2. Each slash location gives an instruction value 0, 1 or 2. The same operation must apply whenever the same value occurs, regardless of class.
3. The nine images are cells of a **3×3 board**. The canonical puzzle background is `IAB/CDE/FGH`; `ABC/DEF/GHI` is a deliberate foil.
4. The board is a mathematical **3×3 torus**, with wrap-around at its edges. This was invented to allow closed nine-step routes, not found on an original source artifact.
5. Two instruction families: (a) the six assignments of literal community-inspired `up, left, right` movement to the three opcode values; and (b) all **8 × 7 × 6 = 336** injective assignments of three nonzero translation vectors (including diagonals) to those values.
6. Starting at class **A**, a nine-step interpreter follows its opcode at each visited class. A successful complete tour visits every one of the nine named images exactly once and returns to A. Starting at another node would not change whether a one-cycle graph exists; it merely rotates the traversal.

Every candidate is an explicit executable transition graph. The workbench also compares the compiled successor table with an independent coordinate-by-coordinate walker on two board arrangements. The whole nine-site routing rule must work consistently; there is no class-specific mapping or fitted goal string.

## Raw-data results

| Hypothesis | Actual one-hot-compatible 18 tail completions, canonical `IAB/CDE/FGH` | Foil `ABC/DEF/GHI` |
| --- | ---: | ---: |
| Six assignments of literal up/left/right | **0 nine-node tours** | **0** |
| All 336 assignments of any three 3×3 translations | **4 nine-node tours** | **0** |

One literal speculative witness among the four permissive tours assigns the three commands to **up-left, up-right and up**, using one physically compatible set of unknown selector choices (class A/C remain unobserved). This is mechanically interesting because all three instructions advance one layer upward while different x directions move across each row. However, the choice of wrapping board and selecting three translations from eight is highly flexible.

## Exact null, including post-selection

The 12 physically observed tail marks include four slashes and eight dots. Hold **their exact 12 serial positions fixed**, enumerate every one of the `choose(12,4) = 495` allocations of these same labels, leaving all 15 unobserved tail positions unfilled. Recompute all one-hot-compatible class selector completions and optimize across the **same 6 and 336 movement dictionaries**. No 81-body marks enter this control, because this particular program reads only the 27 control marks and nine background classes.

- **280/495** shuffled allocations admit any one-hot completion at all.
- On canonical `IAB/CDE/FGH`, **156/495** shuffles achieve at least the physical tally of **four** nine-room tours in the unrestricted 336-dictionary search.
- Since actual literal up/left/right tour count is **zero**, **495/495** controls attain an equal or higher score. Thus the cheap direct version is an exact physical negative, not a statistical signal.
- On the artificial alphabetical `ABC/DEF/GHI` board, the current tail produces zero tours even under all 336 dictionaries; that contrast is purely *retrospective* and does not provide independent confirmation for the original artwork layout.

**Disposition:** The picture-as-router conceit survives as a vivid conditional explanation for what the 27-bit changed-symbol tail might do, but there is no nonrandom evidence for this specific interpreter. Do **not** treat the four retrospective tours as predicted routes, developer-intended graphics, or new decoded paths. Its best contribution is a *proposed receiving mechanism with an explicit end condition*.

## Three ways to make the idea more discriminating

- **Source-bound move set:** If the reversible cover, supplied poster, or original INSIDE screenshot supplies *exactly three* relative movement arrows with orientations, freeze them rather than searching 336 translations.
- **Stateful turtle instead of translated cells:** Commands change orientation, select the next image to inspect, or mutate the prior nine-bit class payload; a move may apply to earlier and later instructions differently. This is a **genuinely new grammar** and must derive an independently checkable trace, not simply another path chosen for legibility.
- **Readout from an independently known object:** If the nine images represent nine patches in an original printer file or nine physical objects in the CE, trace the route over *that* exact image, not an arbitrary mosaic invented for convenient Hamiltonian closure.

## Reproduce

```bash
python scripts/conjecture_lab_picture_router.py --test
python scripts/conjecture_lab_picture_router.py --output data/conjecture-lab-picture-router-2026-10-13.json
```

Pure Python standard library; complete 495-member observed-tail permutation null. No unobserved foreground mark enters the raw corpus as a fact.
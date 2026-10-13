# CL-VLEN-17: Why a short opcode needs a variable address

_13 October 2026. DISCOVER/DEVELOP only. A mathematical property of an invented A–I tape/one-hot interpretation, not an independently sourced Playdead instruction._

## Motivation

CL-VLEN-14–16 found that the observed first 81 stickers can be regarded as nine cyclic nine-bit register states, with a minimum total of 20 individual bit edits. A compatible 20-edit witness needs no more than four edits **in each transition**. It is tempting to give the final three-symbol one-hot class selector a literal interpretation: choose one of three predefined four-site write stencils, editing any subset of that chosen stencil. This is a meaningful *instruction program*, and a small finite calculation can test it without guessing plaintext.

The distinction matters: **how many sites an instruction actually changes on one use** is not the same as **how many distinct sites the instruction must be capable of changing across multiple uses**. A fixed-address opcode can have four sites available; a dynamic opcode could have a four-site immediate mask that changes depending on the previous run or current register.

## Exact physical obstruction

Use `data/observations.csv` only (84 records, 66 H108 residues). Nine class words are `1+j+9t`, for class `j=0..8`, depth `t=0..8`. The tail selectors are the **18 current physically compatible** one-hot assignments over the final three class positions, not asserted to be genuine Playdead control bits. Treat each class's command as acting on the preceding nine-bit body state to yield the following class state in cyclic A→...→I→A order.

For each transition, let `D[class]` be the set of **physically forced changed depth indices**: indices where both source and target marks have been directly observed and disagree. Unseen sites impose no constraints on `D`.

If opcode position `q` always writes only within one fixed set `M[q]` of physical depth positions, then, necessarily:

`union(D[class] for class with selector[class]=q) subset of M[q]`.

Enumerate all 18 compatible selector assignments, take those three unions and minimize the maximum site count over `q=0,1,2`.

**Exact answer: the minimum possible maximum fixed opcode footprint is 5.** Therefore **no three fixed four-site write stencils** can reproduce the physical observations under this specific class cyclic/one-hot design, even though a dynamic four-write-per-step program can.

The concrete directly observed **B→C transition already changes depths 0, 2, 6**. No ordinary single row, column or diagonal of a 3×3 board contains those three indices, so a command that merely selects one such three-cell line is also contradicted directly. The global five-site lower bound is stronger because it incorporates repeated opcode reuse across multiple transitions.

### Minimum-20-edit completions

Enumerate all **48** physically compatible minimum-total-write body completions, multiplied by all **18** tail selector vectors: **864** joint conditional scenarios. For each one, derive the *entire* nine-bit actual transition differences, and calculate the smallest fixed writable-site sets capable of covering all uses of each opcode.

Among these 864 scenarios the smallest possible maximum reusable opcode footprint is **6**, not 4. The distribution of required maximum footprints and one witness are retained in the JSON. This six-site bound is conditional on the invented minimum-total-edit prior; the five-site lower bound requires only known physical marks plus the one-hot, A–I cyclic-register conjecture.

## Controls and interpretation

Across 10,000 permutations preserving observed masks and marks per original serial nine-site frame, **5,420/10,000** achieve a minimum max footprint of five or less. For 10,000 within-class symbol-count permutations it is **4,171/10,000**. The observed footprint is **not exceptional** under either control; its importance is **logical incompatibility** with the fixed four-address opcode schema, rather than evidence that Playdead intentionally used five or six editable addresses.

## New conjectures made viable by the contradiction

- **Opcode + immediate address:** the class's final three marks select *how to write*, while a preceding three-, five- or other-width run encodes the **address or mask**. Four bits suffice to identify one of the nine 3×3 positions, and five-bit groups give room for a small address plus modifier. We have no source-native evidence identifying the codebook, phase or direction.
- **State-derived address:** the same three-symbol instruction chooses a rule such as "flip the first two zeroes from the last written bit". It can operate on different physical sites during B→C and H→I without being a self-inverse transformation or owning a fixed four-site stencil.
- **Variable cursor / printhead:** a glyph run increments a cursor; the next opcode toggles a small number of sites starting there. The physically solved CE printer-style background makes this worth exploring *as a player-facing conjecture*, but the source lacks a confirmed cursor start, write semantics or stop rule.
- **Commands acting on an external artifact:** the nine bits might not be a state trace at all. The tail could instead select a process applied to the original printer, Terminal41 `534brn` source bytes or shipped cover. The fixed-stencil contradiction would then be irrelevant; do not overextend it.

**Next actual discriminators:** find an independently authored nine-position cursor, four-write affordance or mask in original Playdead material; freeze which side of the body carries a three-/five-symbol immediate; then run an original-source-specific interpreter against all known marks and physically held-out predictions. Do not interpret the six-site mask as a newly decoded foreground or silently add conditional bits to `data/observations.csv`.

## Reproduce

```sh
python scripts/conjecture_lab_opcode_address_footprint.py --test
python scripts/conjecture_lab_opcode_address_footprint.py --nulls 10000
```

[Executable source](../../scripts/conjecture_lab_opcode_address_footprint.py) · [Complete selector, union-mask and null-control atlas](../../data/conjecture-lab-opcode-address-footprint-2026-10-13.json) · [Parent campaign](2026-10-13-contextual-instruction-and-minimal-write.md).
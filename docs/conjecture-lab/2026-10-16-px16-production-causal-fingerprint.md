# PX-16 / PX-C1: closed-corpus sticker-generation causality pilot

**Date:** 16 October 2026. **Mode:** DEVELOP, observation-only for the calculations and conditional for production history. **Status:** bounded pilot performed; broader PX-16/PX-C1 portfolios remain active. **No fresh sticker discovery or outreach.**

## Question and design

Given the fixed physical corpus, which compact deterministic address models for the foreground are actually contradicted, and can the remaining visible serial, background and glyph relationships distinguish *when* and *by whom* the stickers were generated or assigned?

Reproduction: `python scripts/audit_perspective_production_causality.py --check` and `--json`. Data: `data/observations.csv`; independent comparison: [Experiment 421](../experiment-421-h108-replication-audit.md), [manufacturing provenance](../archival-manufacturing-evidence.md), [serial custody clusters](../serial-provenance-clusters.md). All pair counts include the actual 84 physical observations, **not** guessed values for 42 unseen residues or assumed sale totals.

The study explicitly compares six **address-only determinism** models, using the same records and no arbitrary parameters selected to increase agreement. Each model says that records with the same proposed address must have the same printed symbol. A single contradictory pair falsifies that *fixed deterministic model*, not a noisy/non-deterministic generalization.

## Exact results

| Address used to choose glyph | Distinct observed addresses | Conflicting address groups | Total physical pairs sharing address | Disagreeing pairs | Verdict |
|---|---:|---:|---:|---:|---|
| A–I picture class / serial phase modulo 9 | 9 | 9 | 372 | 190 | Contradicted |
| A–I class + early 81 / final 27 sector | 16 | 12 | 280 | 125 | Contradicted |
| A–I class + 27-residue quarter | 33 | 16 | 87 | 34 | Contradicted |
| Serial modulo 27 | 26 | 14 | 127 | 47 | Contradicted |
| Serial modulo 54 | 46 | 10 | 54 | 17 | Contradicted |
| Serial modulo 108 | 66 | 0 | 20 | 0 | Consistent on observed pairs |

The first two show that the foreground is **not simply a glyph assigned to a background tile class**, including the tempting four-quarter/zone simplifications. An easy-to-check same-background, same-sector contradiction is **002 = slash** and **182 = dash** (both class B and within the first 81 positions). Another is class A's **037 = dash** vs **154 = slash** within the same 27-position quarter. The exact JSON output includes a first contradictory witness for each addressed family.

The class labels are observed for **82/84** records and match serial phase **82/82**; two photographs have no physical background class recorded. This is a verification of the **known 9-cycle**, not a new background-class observation for /043 or dot-427. There are **16 repeated H108 residues** and **20 internally agreeing physical pairs**, already established independently by Experiment 421. No new significance claim is attached to those 20 pairs.

The last line is a **consistency** statement. An arbitrary lookup with 108 positions is sufficiently flexible to fit the known records; the original physical period test gives separate, stronger evidence for recurrence. Consistency alone does not show how a printer generated this structure, whether a message is present, or whether a player can decode it. Nor does it show that 108 is the only possible period without conditioning on alternatives and historic selection.

## Three competing production DAGs

These are hypotheses about *causal process*, not competing readouts. Each can generate the same `serial → tile/glyph` record, including the period-108 recurrence.

### DAG A: authored data, preprinted serial sheets or rolls

`author-controlled label master → print complete serial/tile/glyph label stock → CE-specific black game wrapping → final kitting → owner`

A printer can use 108 foreground entries and nine repeating background tiles on pre-imposed sheets. No later computing during kitting is needed. Print order does **not** determine which customer gets which serial: label stock could be stacked, cut, or mixed.

### DAG B: authored data, per-package print-on-demand

`master specification → packout requests next serial → print serial/tile/glyph on demand → seal black game wrap → customer allocation`

The very same serial-to-artwork/glyph function can be evaluated at print time. It is observationally identical in the final label; neither serial adjacency nor H108 proves a physical preprinted roll or software generation.

### DAG C: independently produced stock, nonsequential packout

`master specification → labeled stock → independent physical reorder/store → packers select labels → black game wrapping → shipment`

This also generates identical printed labels. Custody sources supply mixed suggestive but nondecisive data: **178/179** are owned together; a five-copy resale lot includes **038,193,194,252**. Those observations contradict the universal **current co-possession means contiguous serials** assertion, but do not establish original receipt order, printing order or packer behaviour.

### An observational-equivalence proof

Let `S` be any set of serial numbers and `g(s)` any deterministic mapping to tile/glyph. A printer can (A) pre-render and store each `(s,g(s))`, (B) calculate `g(s)` just before printing, or (C) print the same labels first and permute physical stock before applying each label. Conditioned on the final labels' serial numbers, all three produce the **same distribution of visible `(serial, tile, glyph)` records**. This remains true even if every one of the 108 distinct positions is physically observed. Only independent evidence of timing, separation, stock or order assignment can orient these causal arrows.

That proof deliberately refuses to make a claim about the hidden *semantic origin* of `g`: one can choose it to encode a message, image, program, metadata or nothing at all while preserving the same physical corpus. Model complexity and clues from outside the stickers may make these possibilities more or less economical, but the observed label table does not decide the direction.

## Existing physical-production constraints

- The numbered seal closes the **black-paper-wrapped PS4 game**, separate from the Huddle and the ordinary PS4 edition. As established in the manufacturing dossier, this localizes **application** to CE-specific wrapping/kitting, while **printing** could happen elsewhere or earlier.
- The outer package's marketing and RealDoll silicone role do not identify the seal author, ink vendor, label printer or person applying it.
- A contemporary reported iam8bit comment that copies were numbered “in their own way” is a **secondhand account by an owner**, not recovered first-party production instructions.
- Neither highest observed serial **597** nor seller serial distances establish a total production quantity, 108-serial print-sheet imposition or sale-order assignment.

## Discriminating evidence that does not require any new stickers

1. **Print-layer provenance:** original sticker artwork separations, imposition sheets, source project file or vendor documentation could show when number, foreground symbol and background class were composed.
2. **Wrap-stage ordering:** existing contemporary unboxing or packout footage in the repository could document whether printed stock was attached before/after game wrapping or original serial allocation.
3. **Existing source metadata:** product photography/archived job record with a legible sequence identifier, registration guide, stock format or page impose marks, if authenticated, distinguishes a roll/sheet production stage from print-on-demand.
4. **Verified historic ordering records:** one order explicitly containing multiple copies with separately documented label serials and shipment details would constrain assignment, though a single adjacent pair remains weak.

The work deliberately does **not** search for or request new sticker photos. It also does not assert that vendor archives exist or that the known owner/provenance cluster can be upgraded without new primary metadata.

## Decision and stopping boundary

**Disproved (literal, deterministic):** symbol as a function of A–I alone, A–I+sector, A–I+quarter, serial mod27, or serial mod54 on the current corpus. These are not models of the full machine and do not reject externally keyed/higher-state variations.

**Supported as a physical regularity:** H108 consistency (20/20 same-residue pairs) and A–I period-9 correspondence, reusing prior experiment results.

**Not identifiable:** preprinted master stock vs print-on-demand vs labels shuffled during kitting; upstream message vs structural computation vs intended player action. No amount of additional **pure output-only serial/glyph observation** can resolve that *unrestricted* causal distinction. Restrict the next experiment to original production files, already-archived unboxing/printing media or an independently specified receiving operation.

**Follow-on:** [original player path audit](2026-10-16-px12-expected-player-paths.md) asks which generation stories would also yield a *discoverable* 2019–2020 solve. [Capstone synthesis](2026-10-16-pxm1-causal-explanation-frontier.md) protects the no-extra-endgame explanation.

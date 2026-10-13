# Exhaustive selected-period null over every testable CE serial cycle

*12 October 2026. DISCOVER/DEVELOP statistical control. No sticker decode or receiver identified.*

## Why this supplement exists

[The owner-local / global-message audit](ce-owner-local-vs-common-consumer-2026-10-12.md) found 18 extra repeated physical observations that agree perfectly with an H108 foreground. Its simple probability calculation conditioned on the **already noticed** period 108, so it did not account for trying other periods and retaining only the attractive one.

This experiment computes an exact conservative **selection union bound** using all periods distinguishable by the **existing serials**, without a fitted message completion or simulation.

## All-period search domain

The smallest recorded serial is **2**, the largest **597**, and their difference is **595**. For every period p > 595, all 84 observed serials have different residues modulo p; a zero-conflict statement would have **zero repeated observations**. Thus **p=1..595 exhausts every positive integer period with even one observable collision**.

For each p, compute repeat support as **84 − number of distinct residues modulo p**. The observed H108 support is 18. The statistic tested is:

> Does **any** p=1..595 yield at least **18 extra colliding observations**, *all* of whose glyph labels agree?

The support threshold is chosen from the actually observed H108 support. This is a descriptive/post-hoc reference statistic, not a historically preregistered analysis.

## Zone-preserving artificial null

Preserve all 84 known serial positions and their current body/tail assignments (based on p=108); independently shuffle exactly:

- **44 slashes and 28 dashes** among 72 primary-sector physical observations;
- **4 slashes and 8 dots** among 12 tail-sector physical observations.

This explicitly models **random glyph assignment conditional on the observed serials and zone counts**, not Playdead's production process, sticker survival/collector acquisition, or independently random owners.

For a candidate p, partition all observed serials by residue modulo p. Each group must be monochromatic to have zero contradictions. A group containing both primary and tail members can use only a **slash** because the alphabets overlap only at slash. A primary-only group can choose all slash or all dash. A tail-only group can choose all slash or all dot.

Use exact integer-valued dynamic programming to count assignments with the fixed total slash counts in the two zones. Every period shares the same denominator:

\[
D=\binom{72}{44}\binom{12}{4}=37399079244620030691600.
\]

No independence assumption is made among different periods.

## Results

| Metric | Exact result |
| --- | ---: |
| Possible distinguishable periods | 595 |
| Periods with at least 18 observed extra collisions | **137** |
| Of those, periods for which *some* label assignment could have zero conflicts | **27** |
| Actual conflict-free period meeting threshold | **108 only** |
| Numerator for fixed p=108 | 217839326948876160 |
| Sum of individual null numerators over all 137 eligible periods | **377822188953098255** |
| Exact conservative union upper bound | **0.000010102446279006965** |

By Boole's inequality, the probability **under the stated null** of seeing *any* zero-conflict period with at least 18 repeated observations is **no greater than**:

\[
P_{\mathrm{null}}(\exists p) \le
\frac{377822188953098255}{37399079244620030691600}
\approx 1.0102446279\times10^{-5}.
\]

This bound covers the selection among **all observable periods**, not just p≤216, and doesn't multiply dependent p-values. The true event probability could be smaller because compatible assignments for different p overlap. The numerator is a sum, not an exact disjoint-event count.

The separate **joint image-class + symbol** check already rules out period 197 while leaving H108 and its harmonic 216; this null calculation intentionally uses **symbols only**, conservatively, rather than treating a printed class assignment as random.

## Interpretation and limits

The observation is highly inconsistent with this **particular random glyph-label process**, even after accounting for period search. The statistical test does *not* demonstrate that a particular completed foreground model, printer, webpage, art card, Steam branch, or individual serial-number receiver is intended. It cannot separate all forms of deterministic manufacturing, common prior, hidden repeated instructions, error correction, or random production processes not captured by independent label shuffle.

A person possessing only one sticker can still use it as a personal lookup input if a genuine serial-receiving artifact is found. Conversely, the unusually well-supported period 108 is compatible with a *collectively recovered* message which any purchaser could later use. This audit ranks neither story as true.

**Future experiment:** investigate real historical owners' serial-entry surfaces, web form response contracts and authentic CE printed instructions. Preserve two-stage hypotheses, including collective nine-piece background URL → individual serial-specific lookup, as conjectures until an actual handler has been demonstrated. The closely linked damaged Terminal41 web page has no verified surviving functional input.

## Replay and auditability

    python scripts/audit_ce_period_selection_null.py \
      --output /tmp/ce-period-selection-null.json
    python -m unittest discover -s tests -p 'test_ce_period_selection_null.py' -v

[Script](../scripts/audit_ce_period_selection_null.py) and [exact machine-readable counts](../data/ce-period-selection-null-2026-10-12.json). Uses the same pinned 84 physical sticker rows as the other CE buyer/receiver audits, with no inferred missing symbols or source-side passwords. The script includes a tiny explicit group-choice oracle and hard regression assertions for the numerators and denominator.

**Research status:** fully quantified conditional repetition evidence; **zero new evidence identifying a downstream consumer**.

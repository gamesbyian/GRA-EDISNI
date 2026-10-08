# Experiment 367 — evidence basis of the early closed branches (Experiments 1–245)

_Status: completed audit, 1 Oct 2026. Extends Experiment 365 using the Google Docs Results & Observations log (1–245); 246–297 are machine-internal and live in repo scripts/branches._

## Source

`INSIDE Collector's Edition Sticker Cipher — Results & Observations` (Drive file `1GTcKnBaiYf4gXCy_tCvseDapZOq8SlHYTmwaphP1HPU`), exported as text on 1 Oct 2026: 245 numbered experiments, 312 sections. Every experiment behind an entry in the research-queue "Closed branches" list was read in full.

## Finding 1 — the "known INSIDE decoder families" closure is machine-conditioned

The closed-branch entry *"known INSIDE decoder families already audited in Experiment 240"* refers to an audit whose **only target was the incumbent's terminal object** (`100` / raw `---//////`). Experiment 240's own Target section: "Canonical terminal: normalized payload 100, raw native A-I serial word ---//////." Image masking (Exp 122), Xbox-style Braille, iOS bitmap reshape, Switch Morse, RGB/ASCII, spectrogram, pixel sampling, external-text overlay and URL continuation were all evaluated as consumers **of that terminal**.

So Experiment 240 says nothing about whether those operations decode the **raw sticker grid** under some other model. If the incumbent is wrong, the closure does not transfer.

## Finding 2 — raw-grid tests of Playdead's methods exist, but only in their most direct forms

| exp | method | basis | result |
|---|---|---|---|
| 4 | iOS 600-cell bitmap direct overlay | raw | negative for direct overlay |
| 13 | direct Braille on the 9×12 reshape | raw, unknowns open, 5,000-shuffle null | 5.46% of shuffles score as well: **weak, not closed** |
| 13 | 81/27 alphabet split | raw | p ≈ 6.6 × 10⁻⁸: strong structural fact |
| 15 | consecutive Braille grouping | raw | deprioritised; Braille kept for cued rearrangement |
| 15 | contiguous PC/Xbox printer-stream reuse | raw, 300-run null | null (27.7% of shuffles match as well); parsed 64 not 65 residues, rerun recommended by the doc itself |
| 16, 17 | Boolean summary / row-XOR-column generation | raw | rejected for the simple forms |
| 22 | Switch run-length Morse | raw, unknowns as wildcards | 0/432 schemes valid: rejected |
| 22 | direct ternary Morse | raw | **inconclusive** (too few complete groups) |
| 22 | 12-cell columns as 4×3 compact-font glyphs | raw | rejected for that font family |

These are sound. But no raw-grid test exists for any of these methods **after an independently cued rearrangement**, which is how the Xbox (Braille) and PC (acorn) puzzles actually worked. That gap is legitimately cue-gated, not closed.

## Finding 3 — word-level closures are sound, but partly for circular reasons

- **XML** was selected after inspecting base-27 outputs of 36 legal Q4 completions (Exp 92, 163). The doc retires it because "the recursive/diagonal architecture excludes C=1", which is a machine-conditioned reason. The independent reason is that it was a post-hoc pick from 36 completions; that alone justifies retiring it.
- **MIX** came from six machine-filled primary completions (Exp 163) and **MISS** from a chosen raised-dot polarity on a machine-registered 3×2 residual (Exp 94, 112, 163). Both were model-dependent, post-hoc selections and were never raw evidence. Retiring them is correct.
- **621 / 648** are production-count numerology (Exp 163); correctly treated as external hypotheses.

## Finding 4 — Experiments 246–297

These are machine-internal derivations and uniqueness audits (gauge, recursion, route shell, polarity). They are explicitly conditional on the incumbent family by construction and make no claims about raw-grid decoders.

## Corrections applied

- `research-queue.md` closed-branch entry for Experiment 240 annotated: closed **as consumers of the incumbent terminal only**; raw-grid tests exist only for the direct forms listed above.

## Consequence for the closed-branch list

The list remains a reasonable guard against semantic fishing, but two entries were too broad:

1. "known INSIDE decoder families (Exp 240)": machine-conditioned; raw-grid status is "direct forms rejected or weak; cued forms untested".
2. "generic Braille continuation": correct for post-hoc continuations, but raw direct Braille (Exp 13) was **weak (5.46%)**, not refuted. It should reopen if a cue supplies an ordering, as the Xbox puzzle did.

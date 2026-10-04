# Experiment 396 — boundary/check-bit registration across coherent completions

_Status: completed bounded sandbox test, 4 Oct 2026._

The PC printer puzzle demonstrates a useful Playdead operation family: sparse marks at the sides of rows constrain how the rows should be assembled.

The weighted-completion sandbox finally lets us ask whether the complete sticker foreground could contain an analogous registration channel without filling blanks by hand.

## Frozen family

Use the native nine class words.

Each A-I class contributes a 12-cell foreground word, giving nine rows of length 12.

For each row test only fixed symmetric edge widths:

- 1 cell from each side;
- 2 from each side;
- 3 from each side;
- 4 from each side.

These edge strings are treated only as potential registration signatures.

Two independently natural row orders are evaluated:

1. serial/community order `A B C D E F G H I`;
2. solved background physical order `I A B / C D E / F G H`, flattened as `I A B C D E F G H`.

No semantic scoring is used.

## Questions

For every U2, U4 and externally selected E2 completion:

1. do the edge signatures uniquely identify all nine rows?
2. if edge similarity is used as a continuity/check-bit criterion, is either known natural order actually optimal?

The ordering metric is fixed before inspection: total Hamming distance between adjacent edge signatures.

For nine rows, the minimum possible Hamiltonian path cost is computed exactly by dynamic programming.

## Result: edge signatures are not robust row IDs

Widths 1–3 **never** give nine unique row signatures anywhere in U2.

At width 4:

- U2: 243 / 648 masters have nine unique signatures;
- U4: 4 / 20;
- E2: 0 / 2.

So even fairly wide margins do not consistently function as nine distinct row labels.

## Result: the known orders are never boundary-optimal

Across edge widths 1–4:

- A-I order is a minimum-Hamming path in **0** U2, U4 or E2 completions;
- solved physical `IABCDEFGH` order is a minimum-Hamming path in **0** U2, U4 or E2 completions.

This is not a near miss.

At width 1, for example, A-I exceeds the optimum by an average of 4.5 edge mismatches in U2; physical order exceeds it by 4.17.

At width 4 those average excesses rise to about 18.04 and 17.38 respectively.

The external E2 pair is not exceptional in a helpful direction.

## Interpretation

The complete guessed ensembles do **not** reveal a cheap analogue of the PC printer's side/check-bit mechanism at the obvious sticker-word boundaries.

That closes a tempting approach before arbitrary subset search begins.

The correct conclusion is narrow:

> fixed symmetric edge signatures of the native 12-cell A-I words do not robustly encode the known A-I or solved physical row order.

It does not prove that no registration metadata exists anywhere in the sticker puzzle.

## Reopening trigger

Reopen boundary ordering only if an external artifact or historical source identifies:

- a specific edge position;
- a specific asymmetric margin;
- a checksum/check-bit relation;
- or a non-Hamming compatibility rule.

Do not search arbitrary boundary subsets until one of those parameters is supplied independently.

## Sandbox lesson

This is exactly what the weighted-completion program is for.

A single guessed complete sheet could make some edge pattern look suggestive. Across the actual coherent model ensemble, the proposed registration mechanism has nowhere stable to stand.

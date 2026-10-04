# Experiment 397 — direct 534brn DTMF selector replay is a hard negative

_Status: completed consumer-first sandbox test, 4 Oct 2026._

The new exploration program prioritizes externally specified consumers and selectors.

The strongest available external artifact is still `534brn9653f9j8mmd`.

Its nine digits are registered to the native nine CE classes, and historical May-2026 discussion independently licenses two ternary coordinates from a standard DTMF keypad:

- keypad row;
- keypad column.

That suggests one very cheap new interpretation we had not tested directly:

> perhaps the external DTMF value is itself the depth selector `d` for each sticker class, replacing the sticker tail selector `S(j)`.

This is exactly the sort of thing the weighted ensemble makes cheap to test without pretending the missing stickers are known.

## Frozen operation

For each native class `j`:

1. take its registered `534brn` digit;
2. convert it to DTMF row or DTMF column;
3. use that ternary value directly as body depth `d`;
4. retain each of the three primary Q layers;
5. ask whether the resulting physical 3×3 surface has exactly one dash per column and therefore decodes as POS3.

Test both native DTMF coordinates and nothing else.

Run across:

- U2 / 648;
- U4 / 20;
- U5 / 14;
- E2 / the two externally selected `534brn` masters.

## Result

The result is unusually decisive.

For **DTMF row**:

```
U2: Q0 0 hits, Q1 0 hits, Q2 0 hits
U4: Q0 0 hits, Q1 0 hits, Q2 0 hits
U5: Q0 0 hits, Q1 0 hits, Q2 0 hits
E2: Q0 0 hits, Q1 0 hits, Q2 0 hits
```

For **DTMF column**:

```
U2: Q0 0 hits, Q1 0 hits, Q2 0 hits
U4: Q0 0 hits, Q1 0 hits, Q2 0 hits
U5: Q0 0 hits, Q1 0 hits, Q2 0 hits
E2: Q0 0 hits, Q1 0 hits, Q2 0 hits
```

Not one completion produces even a single valid primary POS3 surface.

## Interpretation

The `534brn` digits do not simply substitute for the sticker tail in G5.

That is a useful hard negative because the hypothesis had:

- an independently relevant prior-stage artifact;
- a historically licensed ternary coordinate;
- the exact coordinate type needed by G5.

It still fails before semantic interpretation.

This pushes the stronger `534brn` finding back toward its current best description: an external **coordinate relation / registration discriminator**, not a replacement selector stream.

## Guardrail

Do not now try:

- digit modulo tricks;
- telephone-letter mappings;
- DTMF frequencies;
- arbitrary permutations of the nine values;
- nonlinear digit→depth functions.

The two native DTMF coordinates exhaust the cheap historically licensed selector family.

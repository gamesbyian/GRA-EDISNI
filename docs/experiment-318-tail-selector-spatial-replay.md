# Experiment 318 — Observation-only tail selector spatial replay

_Status: completed reset R3 test, 30 Sep 2026._

## Question

Experiment 317 established, from physical observations alone, that every A–I tail is compatible with exactly one slash among its final three cells, with 36 global completions. The next cheapest question is what that marked position could mean if it is a selector.

This experiment replays two simple spatial meanings without consulting the incumbent machine:

1. **row/chunk:** position 0/1/2 selects the corresponding consecutive three-cell chunk of the preceding nine cells;
2. **column/rail:** position 0/1/2 selects the corresponding column when those nine cells are laid out as a 3x3 grid.

## Inputs and exclusions

Input: `data/observations.csv`.

Explicitly excluded:

- predicted unknown foregrounds;
- `machine-spec.json`;
- POS3;
- recursive closure;
- route criteria;
- terminal `100`;
- visual/plaintext target optimization.

Unknown physical cells remain `?`.

## Result

Both interpretations survive all 36 observation-compatible tail completions.

Across those completions:

| interpretation | observed cells exposed |
|---|---:|
| row/chunk | 18–22 |
| column/rail | 18–21 |

The five classes whose tail position is already physically forced give:

| class | tail position | row/chunk | column/rail |
|---|---:|---|---|
| B | 2 | `//-` | `//-` |
| E | 0 | `/--` | `///` |
| F | 1 | `?/-` | `///` |
| H | 2 | `?-/` | `--/` |
| I | 2 | `/-/` | `??/` |

B is presently non-discriminating; E/F/H/I demonstrate that the two readings are genuinely different.

## Interpretation

This is a useful negative/discriminating result.

The observation corpus does not presently select row/chunk over column/rail. Row/chunk exposes at most one more known cell, which is not an independent reason to prefer it. Choosing whichever extracted words look more attractive would reintroduce semantic fishing.

The historical 9+3 proposal therefore survives as a compact selector architecture, while the selector's spatial meaning remains open.

## Reproducibility

Run:

```bash
python scripts/replay_tail_selector_spatial.py
```

The script asserts the 36 tail completions, the five forced tail positions, and the observed-cell ranges above. It also emits the physical residue supports on which the forced row/column readings differ.

## Next discriminating test

Test the third simple family already named after Experiment 317: three fixed masks tied to the independently solved A–I background geometry.

The masks must be declared from that geometry before inspecting foreground outputs. Do not optimize masks for plaintext, incumbent-machine survival, or visual resemblance. If the solved background geometry does not uniquely motivate a small mask family, record that failure rather than sweeping masks.

# Experiment 322 — Exhaust one-shot G6 selector maps

_Status: completed R4 G6 attack, 30 Sep 2026._

## Question

Experiment 291 compared four human-scale second-step choices after G5:

- fixed q=0;
- fixed q=1;
- fixed q=2;
- q=S.

That made literal selector reuse look uniquely selective, but the tested family was not exhaustive.

The natural finite completion is every deterministic one-shot selector map:

```
q = f(S)
```

with `f:{0,1,2}->{0,1,2}`.

There are exactly `3^3 = 27` such maps.

This family is still small and human-legible. It allows relabeling or collapsing selector values, but does not introduce cellwise rules, state-dependent logic, route targets, or arbitrary address transforms.

## Inputs

Start from the 20 raw-compatible first-pass machines produced by G5.

For each of the 27 maps, measure only:

1. how many of the 20 machines still produce a valid dash-POS3 surface;
2. how many distinct decoded output words remain.

No expected state count, terminal word, route shell, identity map, or hidden-state structure is supplied as a target.

## Result

Eight maps produce a nonempty **completion-invariant** output, meaning every surviving machine gives the same decoded word.

The maximum survivor count among those maps is **14**.

Exactly two maps achieve that maximum:

| map f(0)f(1)f(2) | survivors | invariant output |
|---|---:|---|
| `002` | 14 | `100` |
| `012` | 14 | `100` |

The accepted machine sets are exactly identical.

The two maps differ only at selector value `S=1`:

- `002`: S=1 reads q=0;
- `012`: S=1 reads q=1.

That is the already-established `f1` observational gauge: on every accepted machine, the q=0 and q=1 cells reachable when S=1 carry the same physical symbol.

So the apparent twofold ambiguity does not represent two different functional machines.

## Interpretation

Literal self-reuse `q=S` is not uniquely forced.

A weaker statement is sufficient:

> after G5, consume the selector once more through a deterministic map q=f(S); require a valid completion-invariant POS3 output while retaining the maximum raw-compatible state family.

That criterion yields one functional solution modulo the known S=1 gauge.

This removes the strongest circularity concern around G6. The exact identity map is a **representative choice**, not a uniquely observable operation.

The surviving functional content of G6 is therefore better stated as:

- selector-conditioned readout of the remaining q coordinate;
- maximum-retention completion invariance;
- unique modulo the established f1 equality gauge.

## What this does not prove

The experiment still does not supply an external reason why the tail should be reused as a q-selector at all.

It weakens **which selector-conditioned map** is required. It does not independently establish the broader decision to consume the selector a second time.

That higher-level choice remains a generic operation/simplicity prior until historical or external evidence motivates it.

## R4 consequence

G6 no longer deserves the classification “selected because it preserves the machine” in its exact identity-map form.

It should be treated as a **generic selector-conditioned information-reduction prior**, with a known two-representative observational gauge.

The main upstream reset target therefore moves to G5:

> why should the one-of-three tail index be used as an address/depth substitution at all?

## Reproducibility

Run:

```bash
python scripts/audit_g6_selector_map_family.py
```

The script exhausts all 27 maps and asserts:

- 20 G5 first-pass candidates;
- 8 nonempty completion-invariant maps;
- maximum invariant retention 14;
- only `002` and `012` attain that maximum;
- both produce invariant `100`;
- both accept exactly the same 14 machines.

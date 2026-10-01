# Experiment 362 — CEO-door nameplate string vs. four-sticker groups

_Status: completed bounded negative, 1 Oct 2026._

## Source of the proposal

`solving-breakout`, 3–4 Jan 2026 (santiface, darkmatter_11). The in-game CEO door nameplate reads `Fordsjh Gjfhdfdjfhd Ujhdfr B02`. It was first noted in `solving` on 27 Jun 2018 and called a cipher. With a trailing space, the text part has 27 characters, and 27 × 4 = 108. darkmatter_11 noted that the slash/dot rows roughly line up with `Ujhdfr`.

## Test

Read the 108-cell pattern as 27 consecutive groups of four, one group per character. A necessary condition for any letter-per-group reading is that **every occurrence of the same character maps to the same four-symbol group**.

- Data: raw observations only, with unknown cells as wildcards; no completion or machine assumption.
- Freedom allowed: all 108 cyclic starts; four spelling variants (with/without trailing space, with ` B02`, without spaces).

## Result

**0 compatible starts for every variant.**

At the proposed alignment (start 0), `f` appears at characters 0, 10, 13, 16 and 24. Sticker position 3 is a dash where position 43 is a slash, so the first two `f` groups already disagree. The `f` at character 24 falls in the slash/dot rows, so it can never match an `f` in the slash/dash rows. More broadly, the 81/27 alphabet split forbids any letter from repeating across that boundary in this reading, and `f`, `j`, `h` and `d` all do.

The nameplate looks like placeholder keyboard-mash (name, title, room `B02`) and has been in the game since 2016, before the CE existed. This result is consistent with that.

## Reproducibility

```bash
python scripts/audit_ceo_door_string.py
```

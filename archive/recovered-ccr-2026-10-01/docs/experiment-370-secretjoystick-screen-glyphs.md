# Experiment 370 — SecretJoystick screen glyphs

_Status: completed, 1 Oct 2026. Answers the question left open by Experiment 369; negative for the cover-to-lever symbol mapping._

## Source

Texture renders of `FX_ScreenKaypro` and `FX_ScreenKaypro_Sign1/2/3` from INSIDE's game files, posted in #hacking in reply to the question drafted in this session and relayed by the project owner on 1 Oct 2026. The respondent describes them as "the 4 screens of the cut secret console". Archived in `archive/discord/2026-10-01/`:

```
19cf05a1abc15b085826d331f676b27880d8c3696f928c65ea670658ef3e2cff secretjoystick-screen-neutral-kaypro.png
e4a6b59cc9e62f78e22ebae44f907ec98d67d66f951e184c2544edea271c8fa7 secretjoystick-sign-left-slash.png
db7210acfed1c7ec3b4319d29c302c8402a606eac0bd6c623c84108b0390a9bb secretjoystick-sign-right-brace.png
d591a3361ee5a7c5d19e21a304cc6c3ba13b214c5b64634edae150fddf1d44d3 secretjoystick-sign-up-equals.png
```

## Result

| inspector field | direction | texture shows |
|---|---|---|
| `screenTextureNeutral` | — | Kaypro boot screen: `KAYPRO 63K CP/M Version 2.2G`, `HELLO?`, `A0>dir` listing of the standard Kaypro system disk (MOVCPM, PIP, SUBMIT, …, SBIOS) |
| `screenTextureUp` (Sign1) | Up | `=` |
| `screenTextureLeft` (Sign2) | Left | `/` |
| `screenTextureRight` (Sign3) | Right | `}` |

Timing (respondent): each glyph appears 0.1 s after a pull and returns to the neutral screen 0.18 s after release (matches `screenToNeutralDelay` = 0.18).

## Comparison with the CE cover-clue mapping

The 2020–2021 community reading of the CE cover (Experiments 342/343) was slash = up, dot = left, dash = right.

| direction | cover-clue reading | console glyph |
|---|---|---|
| Up | `/` | `=` |
| Left | `.` | `/` |
| Right | `-` | `}` |

- **0 of 3 directions agree.** The only shared glyph, `/`, is assigned to Left in the game but to Up in the cover reading.
- Neither the dot nor the dash appears on the console at all.

## Consequence

1. **The game does not confirm the sticker-symbol ↔ lever-direction mapping.** The console's own glyph set is `= / }`, not the sticker alphabet `/ - .`. The cover-to-lever reading loses its strongest possible support and now rests only on the cover's spatial arrangement of the three marks.
2. Combined with Experiment 369 (one stored password, the known code), the lever lane is **closed as a sticker consumer** at the game-data level. Reopen only if another artifact independently ties the sticker marks to lever input.
3. The neutral screen's Kaypro CP/M imagery fits the ARG's retro-terminal motif (Terminal41, the printer), but it supplies no sticker-specific parameter.
4. The glyphs themselves (`=`, `/`, `}`) are recorded as data. No interpretation is promoted. Under the console mapping the stored password would display as `=}///==}/}}}==`; this is noted for completeness only.

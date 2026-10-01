# Experiment 369 — SecretJoystick component data (game files, via #hacking)

_Status: completed, 1 Oct 2026. Closes the "second lever code" lane; opens one narrow texture question._

## Source

Inspector screenshot of the `SecretJoystick` component from INSIDE's level data, supplied in reply to the #hacking question drafted in this session and relayed by the project owner on 1 Oct 2026. Preserved as `archive/discord/2026-10-01/secretjoystick-inspector.png` (sha256 `1ae1ac274e61b1b975327721f34e925a87474507c86e88032c32bdc5919ee617`). Respondent's summary: the component **only checks for 14 consecutive inputs matching the already-known code**.

## What the component shows

| field | value |
|---|---|
| `animDevice` | `SecretJoystickConsole` (animations Lowered / Raise / Raised / Left / Right / Up) |
| `animGate` / `animGateOpen` | `SecretBasementDoor` / `OpenUp` |
| `audioPrefix` | `_farm_field_secretSecret` |
| `screen` | `Screen` (MaterialInstance) |
| `screenTextureNeutral` | `FX_ScreenKaypro` |
| `screenTextureUp` | `FX_ScreenKaypro_Sign1` |
| `screenTextureLeft` | `FX_ScreenKaypro_Sign2` |
| `screenTextureRight` | `FX_ScreenKaypro_Sign3` |
| `screenToNeutralDelay` / `pullCacheDuration` / `grabDelay` | 0.18 / 0.15 / 0.3 |
| `password` | `PullDir[14] { Up, Right, Left, Left, Left, … }` (truncated in the inspector) |

## Findings

1. **One device.** The "joystick terminal with a screen" (Oddheader, 05:35) is the bunker lever console itself: the same component opens `SecretBasementDoor` and uses the farm-field secret audio. There is no separate second terminal in this component.

2. **The stored password is a rotation of the known code.** The community code `UURLRRRUUURLLL`, rotated to start at its 10th input, gives `URLLLUURLRRRUU`. That is the only rotation consistent with the visible prefix Up, Right, Left, Left, Left. Together with the respondent's report that the component checks the last 14 consecutive inputs, this explains why the community's rotated version opens the door. It also matches the 2019 Discord remark that the song "doesn't necessitate we enter it … starting on a particular note".

3. **No second code.** The component holds exactly one 14-input password. Together with eropkol's 24 Sep 2026 finding, the hypothesis "the stickers encode a different code for this lever" is closed at the game-data level. Experiment 343 had already excluded the known code (all rotations) as a contiguous sticker window, given the alphabet split.

4. **Open, narrow question: what do the three signs look like?** The console screen swaps to a distinct texture per direction: `Sign1` = Up, `Sign2` = Left, `Sign3` = Right. The CE cover clue maps slash = top/up, dot = left, dash = right. If `FX_ScreenKaypro_Sign1/2/3` depict **/ . -** respectively, the game itself confirms the sticker-symbol ↔ lever-direction mapping, with the stickers' alphabet literally being the lever's screen glyphs. If they depict something else, the cover-to-lever reading loses its strongest support. This is a single texture lookup for anyone with the extracted assets.

## Consequence

- The lever is now best understood as a **symbol vocabulary source** rather than a second code consumer. Any sticker-lever link would be about what the three marks mean (directions), not a hidden password for this door.
- With the 81/27 split, the slash/dash body would be Up/Right moves and the slash/dot tail Up/Left moves. Whether that directional reading leads anywhere still needs an independent cue; this experiment does not supply one.

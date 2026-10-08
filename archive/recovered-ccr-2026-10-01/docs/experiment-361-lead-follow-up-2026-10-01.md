# Experiment 361 — follow-up on the three open leads after Experiment 360

_Status: completed triage, 1 Oct 2026. No model change._

## 1. Missing Discord channels

The public exports end on 28 Sep 2026 and cover only `solving`, `solving-breakout`, `tldr` and `inside`. Three channels that matter here are **not** exported:

- `#stickers-solving`: created 22 Sep 2026 for foreground cracking attempts;
- `#sticker-hunting`: new sticker and owner finds;
- `#hacking`: game-internals discussion, including the lever/joystick implementation.

`.github/workflows/discord-one-shot-archive.yml` has **never been run** (0 workflow runs as of 1 Oct 2026). It needs the `DISCORD_BOT_TOKEN` secret and a server administrator to install the read-only bot (see `docs/discord-archive.md`). Guild ID from the archived links: `460626942190813184`. When dispatching, set `channel_names` to `stickers-solving,sticker-hunting,hacking`.

This is a human step. It cannot be completed from a research session.

## 2. `saf_dat_col`

State of community work, from `burning-lnkr/saf_dat_col` at commit `cdb4145` (25 Sep 2026):

- The data after `</html>` is treated as a damaged DEFLATE stream from a PNG. The default repair inflates 11,779,416 bytes, read as 5000 px wide, 3 channels and 785 rows with a 1-byte filter prefix.
- A local render of the default candidate (`original_combined`, filter residual magnitude) shows coherent image structure: a light diagonal band across the top third and recurring block textures lower down. That supports "real compressed image" over "noise", but no picture is yet recoverable.

Sticker-link check (bounded):

- The only symbol-alphabet content in the readable HTML is two all-slash tapering blocks. One has line lengths `27 21 16 12 8 5 3` (lines 2915–2921) and the other runs `43 39 35 31 27 23 19 15 12 8 5 3` (lines 3007–3018). Two isolated 39-slash lines and two 7-slash lines also appear.
- None contains dashes or dots, a 108/12×9/9-period layout, or anything else that registers with the sticker foreground. The same tapering style decorates other Terminal41 pages, such as the dot taper on `534brn`. The leading 27 and the 43 (acorn width) are noted but give no cue under `external-consumer-audit.md`.

Result: there is no independent cue linking `saf_dat_col` to the sticker foreground. It remains the most recoverable damaged artifact, and that work belongs to the DEFLATE-repair effort, not to this repository.

## 3. Lever / joystick consumer

New 2026 evidence from the public `solving` export:

- 24 Sep 2026, eropkol: the bunker-door combination lives in level data as script public fields, and **only one combination** is stored there. Oddheader's apparent "second combination" was a mistake. This weakens "the stickers are a second code for the same bunker lever" from untested to unsupported by game data.
- Separately, datamined content contains a second "joystick terminal" with a screen (Oddheader, "Secret Joystick Terminal", 05:35). A 22 Sep 2026 post proposes that the four cube formations and the "ENTER CODE SEQUENCE" board share the joystick's left/right/up/neutral layout.

Open question that is now the live form of the lever lead: **does the screen joystick terminal display or consume slash/dash/dot symbols?** If it does, it would be the first independently supplied consumer for the sticker alphabet. Settling it needs the game files or the `#hacking` channel. Neither is available here.

## Combined outcome

No lead produced a cue that licenses reopening the foreground semantics. The cheapest next human actions are:

1. run the Discord export for the three channels above;
2. ask in `#hacking` whether the screen joystick terminal's script data contains `/`, `-` or `.` glyphs or 108/36/12-length sequences.

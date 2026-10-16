# Steam password-protected beta branch as a CE sticker consumer (12 October 2026)

**Mode:** DISCOVER / DEVELOP (unvalidated receiving-artifact hypothesis). **Finding:** Steam provides a real password-to-game-build consumer; no CE relationship or secret build has been demonstrated.

## Independently verified platform mechanics

Valve's Steamworks branch documentation states that developers can create app branches, assign build content, and password-protect a branch so that its *name and description are not available* to an account until the password is entered. Steam desktop game Properties > Game Versions & Betas exposes the password field. The field in the supplied INSIDE screenshot is standard Steam UI, not INSIDE game code. Branch passwords are distinct from Steam activation keys and from in-game codes.

Sources:
- https://partner.steamgames.com/doc/store/application/branches
- https://partner.steamgames.com/doc/store/testing

## INSIDE-specific externally visible evidence (observed 2026-10-12)

SteamDB's INSIDE (app 304430) depot page currently reports:
- public branch, build 17981020, updated 2025-04-14;
- `local` / Local Content Server, build 1330646, dated 2016-09-12;
- `privatebranches = 1` in app configuration.

Source: https://steamdb.info/app/304430/depots/

**Important ambiguity:** The private count is compatible with the already listed `local` branch, and may represent that branch. It cannot be counted as evidence of a *third*, undiscovered ARG branch. SteamDB's observable metadata may also be incomplete or lag behind Steamworks, so absence of an exposed secret branch is not a proof that one never existed.

## Hypothesis and assumptions

H-SB1: Playdead might have intentionally configured a password-protected Steam branch as the CE sticker puzzle's receiver. The sticker sequence or an intermediate ARG output yields its branch password; successful entry unlocks a modified build or ARG continuation.

Assumption stack:
1. Steam password field is an independently existing suitable interface (**verified**).
2. An appropriate branch existed during/after 2019 and was maintained for the intended audience (**unverified**).
3. An ARG artifact explicitly directs solvers to Steam/game versions, or independently yields a candidate passphrase (**unverified**).
4. The CE foreground contains enough information to derive that passphrase (**unverified**).

Do not elevate H-SB1 merely because its output could be text. The older Terminal41 destination has stronger artifact-specific linkage via the nine backgrounds. This is an alternative or possible subsequent endpoint.

## Discriminating research and stop conditions

1. **Metadata interpretation (high priority):** Verify `privatebranches` semantics against other known Steam apps with *one visible passworded/local branch* and against Steamworks/SteamDB history. Establish whether a count of 1 can be wholly accounted for by `local`. Preserve URLs/screenshots and observed timestamps.
2. **Historical timeline:** Inspect INSIDE SteamDB app/branch history near 2016, 2019 CE release, 2020–2021 ARG discoveries, and any documented changes in 2025/2026. Branch visibility/absence is only an observational limit.
3. **Independent clue discovery:** Search original Playdead/iam8bit promotional and ARG sources, contemporaneous Discord/forum archives, localization and site artifacts for `Steam`, `beta`, `branch`, `version`, `build`, `test`, `password`, and plausible non-English equivalents. Preserve dated citations.
4. **Bounded manual control:** A user who owns INSIDE may voluntarily check independently documented ARG passphrases in their own Steam client, one by one, recording exact input and Steam response. Do not automate guessing, enumerate passwords, bypass authorization, or infer that a failed guess falsifies the branch hypothesis. Start only with externally sourced answers; `NEWPLANETDISCOVERED` is a historical candidate, **not** a predicted sticker plaintext.
5. **Positive verification:** A Steam acceptance response, unlocked branch name and build number, downloaded build manifest, and independently observed game/content difference would establish a real receiver. Establish the *CE linkage separately* (independent cue or uniquely derived CE readout).
6. **Negative/priority gate:** If historical branch evidence gives only a generic `local` test branch and no Steam-directed clue, keep the hypothesis on a low-effort watchlist. Do not allocate foreground decoding or password search effort to it.

## Relationship to existing evidence

- Competes with source-native foreground consumers and Terminal41 as a *receiving mechanism*, not a decoding grammar.
- Neither the 108 cycle nor A–I artwork implies a password syntax or expected length.
- A branch successfully unlocked by a known unrelated ARG code would still require proving intentional CE sticker linkage.
- No changes to physical observations, closed-corpus completions, machine specification, prospective predictions or canonical experiment numbering.

**Status: technologically feasible, weak case-specific evidence; recommended action: metadata provenance + independent historical clue search before any password testing.**

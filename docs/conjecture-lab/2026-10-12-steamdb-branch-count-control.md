# SteamDB branch-count control (12 October 2026)

The Steam beta interface is a real mechanism, but INSIDE's metadata does not by itself point to an additional ARG-related build.

- INSIDE (304430) currently displays public, local (2016), and `privatebranches=1`: https://steamdb.info/app/304430/depots/
- A cross-check game, walk (4563880), displays only public, but **also** `privatebranches=1`: https://steamdb.info/app/4563880/depots/
- ERROR143 (2066550) likewise displays only public and `privatebranches=1`: https://steamdb.info/app/2066550/depots/

Therefore the value 1 is **not** an independent positive signal of a CE-specific build. This does not imply that no undisclosed branch exists.

Valve documents that branch names themselves may remain unavailable until a correct password is supplied: https://partner.steamgames.com/doc/store/application/branches

**Disposition:** keep the Steam receiving-artifact hypothesis available for DISCOVER/DEVELOP experiments; do not use the metadata count to promote it to VALIDATE.

# Original INSIDE scene-image recovery: frozen 2016 witness URLs

**9 October 2026, acquisition experiment (no decoded CE foreground).**

This supplements [the source-graded ordinary-detail hunt](original-game-ordinary-detail-clue-hunt-2026-10-09.md), not the canonical sticker observation ledger. The exact 2016 references are frozen in [the retrieval manifest](../data/original-game-2016-witness-targets.json). The [offline-tested one-shot probe](../scripts/probe_inside_original_game_witnesses.py) makes at most **11 requests** to those URLs and preserves the result as a GitHub Actions **artifact**, not game files committed to the repository. It uses an HTTPS/hostname allowlist, per-file 6 MB cap, 12-second timeout and magic-byte classification to avoid treating 404/401 HTML as photos.

## Why do this?

Two high-priority external-reader candidates still lack source material:

- **OG-01 original status board:** The [July 10 2016 original Steam discussion](https://steamcommunity.com/app/304430/discussions/0/365172547948628597/) links three high-resolution original-scene screenshots uploaded by MASTAN. It reports nine entering yellow cables (one isolated), labels 2/4/11/12, lines 3-4/6-7/8-9 and four small squares. The reporter notes that the screenshot host already returned 401 by **July 11, 2016**, so a current image-link failure is expected and is not evidence of later removal of a secret.
- **OG-02 original SecretMap:** The July 2016 texture was identified as \`SecretMap_#916\` in a Steam user's extracted image gallery, and independently reposted in a low-resolution/watermarked 2018 [9game article](https://www.9game.cn/news/2199070.html). Even recovering that republished JPEG does **not** recover original DDS pixels, scene transforms or source dimensions. The [pre-existing native-orb registration audit](secretmap-original-asset-null-protocol-2026-10-08.md) remains blocked on genuine source bytes.
- **OG-03 buried elevator:** The [August 23, 2016 account](https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=11) reports \`_SignalConnectors\`, \`TriggerElevatorStart\`, a twelve-button console on \`Cargo_Elevator_Narrow\` and four small screens plus one large one. **These are one observer's account**; the exact screenshot URLs for *these* objects were not visible in the search index. Two July 25 VK photos are listed as separate **unidentified Atøm scene photos**, not fraudulently labelled "elevator" captures.
- **OG-04 Kaypro:** \`FX_ScreenKaypro_#742\` was reportedly in the July 2016 extraction gallery, but the original texture and location remain unavailable.

## What counts as recovered?

| Artifact type | Legitimate claim | Not permitted |
| --- | --- | --- |
| Image with matching JPEG/PNG/GIF/WebP magic and original fixed URL | Exact bytes at that URL on retrieval date; hash in JSON | That it is a native INSIDE asset, that it depicts any specific object without image inspection |
| Source-linked 2018 derivative SecretMap image | A timestamped witness to an alleged source texture, if visual identity checks out | Trustworthy native coordinate geometry or pixel-for-pixel original |
| Imgur/Postimg HTML page | HTML capture is available for later link extraction | Original photos have been recovered |
| 401/403/404, DNS, timeout, error page or redirect outside allowlist | URL unavailable to this bounded retrieval | The underlying asset never existed or cannot survive elsewhere |
| Native DDS acquired from a legitimate pinned game build | Potentially the required exact game source after verifying build, SHA and rendering use | An external CE linkage, without a separate sticker-facing rule |

The script refuses unrecognized response bodies and any redirect to a new hostname or insecure HTTP. An image served under the old path may still have been silently replaced; investigate visual provenance separately.

### Reproduce

\`\`\`sh
python scripts/probe_inside_original_game_witnesses.py --self-test
python scripts/probe_inside_original_game_witnesses.py \
  --manifest data/original-game-2016-witness-targets.json \
  --output original-2016-witnesses
\`\`\`

One pull-request CI execution is permitted. After its **Probe historical INSIDE scene witnesses** job completes, inspect the \`original-inside-2016-witnesses\` artifact and \`report.json\`, preserving URL, response code, MIME, detected file signature, file size, SHA-256, capture date and any redirect. Artifact retention is 30 days. The workflow can also be dispatched manually if original hosts revive; **do not run frequently**. Repeat only after a meaningful change in archived sources or host status.

If any image is recovered, inspect it **without stickers first**. For the board, count exactly which cables represent status versus scene wires and whether all marks track the existing 13+1 orb system. For SecretMap, do not run an arbitrary affine/projective fit against the sticker atlas; use the preexisting frozen \`scripts/audit_secretmap_registered_orbs.py\` once native coordinates are available. For the elevator, verify that the twelve buttons and four displays are connected in the retail object tree, not simply in proximity in a level editor.

### Source-frozen alternatives and independent control

Original source reports already contain decisive ordinary explanations:

- The board uses thirteen orb status lights; completing the final orb leaves **orb 2** lit to direct the original in-game bunker solution. See [Shacknews June 2016](https://www.shacknews.com/article/95640/inside-how-to-get-the-secret-ending).
- The **four squares** were already interpreted by contemporary 2016 solvers as the four lever/keyboard positions. A generic four-state stencil would be double-counted if reapplied to the stickers without a new clue.
- July 2016 players noticed that at least two game-world clocks reflect the computer's system time, independently corroborated in the July 10 [NeoGAF discussion](https://www.neogaf.com/threads/playdeads-inside-spoiler-thread.1240582/page-13); this weakens treating the reversible cover clock reading 12:12 as a self-evidently authored static cipher. The project had **already** documented this [on October 8](original-solvability-clock-asset-destination-audit-2026-10-08.md); it is not a new research discovery here.
- The previously cited SecretMap marker "extra beyond the thirteen" may refer simply to the final fourteenth orb; a July 2016 discussion already proposed that [pre-CE explanation](secretmap-original-asset-null-protocol-2026-10-08.md).

**Current result pending remote CI:** Known source bytes are still absent. This acquisition tool is a controlled attempt to obtain independent primary image witnesses. It does not add a sticker model, inferred code, completion or physical observation.

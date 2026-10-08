# Original INSIDE game asset: 2016 BoardText

**Provenance:** byte-exact copy of `gamesbyian/playdead-unofficial-exports` (master)
`assets/BoardText_13309-b0922098d7c08dbe.dds`.

- Upstream Git blob SHA: `d8e19793cb3b09764728fb2fc3cf4aaa4e1d32e8`
- Vendored Git blob SHA: `d8e19793cb3b09764728fb2fc3cf4aaa4e1d32e8`
- Size: 11,152 bytes
- Format: DDS / DXT5 (BC3), 256×32 primary image, complete stored mip chain
- Preserved to support source-level analysis of the historical secret-orb information board and original 2016 game texture.
- This is an extracted game artwork asset attributed to **Playdead**. Preserved solely for investigation/provenance; no assertion of an open-source license or permission to reuse in a game.

Reproduction:

```sh
python scripts/decode_inside_boardtext_dds.py \
  archive/external/inside-2016-game-assets/BoardText_13309-b0922098d7c08dbe.dds \
  /tmp/inside-boardtext-alpha.pgm
```

This directory contains **one** small binary ingested into Git without transcoding. The large full-resolution cover scans remain separately pinned by existing upstream Git object references under `archive/external/cover-source-audit/README.md`, not duplicated into this project.

**Negative result:** the DDS header, base layer and further BC3 mip footprints account for every source byte, leaving no unexplained trailing data under this layout. No alternative user input or sticker code has been observed from this texture.

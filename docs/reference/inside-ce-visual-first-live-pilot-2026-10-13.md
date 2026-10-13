# CE visual discovery: first live pilot, findings and remediation

**Observed:** 2026-10-13, GitHub Actions [run 38458997319](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38458997319), one-shot [PR #236](https://github.com/gamesbyian/GRA-EDISNI/pull/236). **Method:** public source-only DISCOVER. **Inference boundary:** no novel sticker owner or physical sticker confirmed.

## Observed, directly from the completed workflow job output

- **82 canonical original sticker photographs** were previously and successfully hash-verified/indexed under the merged [visual program PR #234](https://github.com/gamesbyian/GRA-EDISNI/pull/234); no changes to the sticker ledger or machine.
- All **6/6 exact sourced official/press image controls** downloaded and SHA-256 hashed with genuine image validation:
  - iam8bit INSIDE full CE `00001B`, 829,335 bytes, SHA-256 `1b313c374f88e76d0a9e8acf79a3b020eda08ef8f84c434016cfff0b2a1ee6bf`.
  - iam8bit CE `00018`, 2,896,284 bytes, SHA-256 `32ae4b4df95b6e20dcfe7391889539d40e3be8e30914f3b7f51ddb639a329222`.
  - iam8bit CE print and PS4 disc `00014`, 2,307,372 bytes, SHA-256 `13c1a34494af867b8351bfdfb8288e6e12ecfb1509e7423a78de4da8a50b6dcb`.
  - Polygon syndicated cards `00025`, 4,379,341 bytes, SHA-256 `9296becc5ad73aefa6a724ad67c3fa5597feb25f3def4cb3a9dabcd50f53d705`.
  - iam8bit standalone PS4 packshot, 36,904 bytes, SHA-256 `a281bd282d09238b57160518d2243df058e2328127c7ead81a90673c23b9800a`.
  - iam8bit standalone lifestyle `00013`, 2,767,990 bytes, SHA-256 `e8cb4b9e98bd569411f53dff0de866873de053d8d3e8e4b11d6484126dbd6c53`.
- **3/6 historical source pages** downloaded: the two official iam8bit products and Polygon's December 2019 contents article. **3/6 failed HTTP 403**: original Reddit owner-display `eers0x`, 2019 shipping thread `e9bteo`, and 2026 sticker PSA `1wruv2d`.
- `discover_html_images.py` reported **1,800 URL mentions**, NOT 1,800 distinct photographs. The Shopify/press page HTML contains `srcset` repetitions, banners, unrelated recommendations and multiple resolutions.
- Original downloader chose **16 public image URLs**. Eight were sizes 200–2200 of *the same* official INSIDE CE `00001B` marketing photograph; eight were variations of an unrelated `Billboardstickers.png` asset embedded in the standalone shop. These 16 are not new independent CE sightings.
- The fingerprint engine reported **8 real whole-image promotional matches** against reference `iam8bit-insidece-00001b` (dHash differences 0–2; aHash 0 across the resized versions). Zero new owner photographs and zero new sticker observations can be claimed. The eight generic shopping graphics lacked reference matches.

## Root causes and corrected plan

1. **Repeated resolution variants exhausted per-page allowance.** Fix in `fetch_html_images.py` by grouping discovered image URLs by host + path + version key and choosing a single high-resolution candidate before network download. That is a *budget-selection heuristic*, not evidence two independently sourced assets depict one physical CE.
2. **Keyword-based ranking surfaced generic shop promotions.** Exclude non-INSIDE filenames for explicitly official product controls while leaving genuine owner/post media with opaque filenames eligible.
3. **Polygon migrated its image CDN to `static0.polygonimages.com`.** Add that exact HTTPS host to permitted media targets. Frozen page evidence provides nine more unique source-identified `InsideCE_Lifestyle_*.jpg` image names; add as explicit **2019 press syndication/marketing controls**, never nine owners or stickers.
4. **Reddit 403 inhibits positive owner-photo controls.** First fallback is public archived post metadata from Arctic Shift's post-ID endpoint, then PullPush's submission-ID endpoint; preserve archive provider, response SHA-256, and original Reddit URL. Extract only public post media URLs and state archive incompleteness. Verify any recovered `i.redd.it`, `preview.redd.it` or `i.imgur.com` image in the ordinary bounded downloader. Never treat archival metadata as live-owner confirmation.
5. **Positive-control recall remains unknown.** Image matching is validated only for eight *marketing variants*. A true owner-post photo has not yet been fetched, so no sensitivity claims for genuine visual leads, arbitrary crops or post screenshots are justified.

## Follow-up campaign

Rerun with the corrections in [research/ce-visual-image-retrieval-quality-20261013](https://github.com/gamesbyian/GRA-EDISNI/tree/research/ce-visual-image-retrieval-quality-20261013) after CI. Preserve archive API failures as structured data. Include both source page and exact image URL, verify genuine photographic bytes, and cross-check any first-hand sticker claims against canonical known `U/L` cases and duplicate transfers.

**For raezores:** this is currently infrastructure calibration rather than a reportable new owner lead. Do not relay the 16 selected images or 1,800 URL mentions as 16 owners or 1,800 discoveries.

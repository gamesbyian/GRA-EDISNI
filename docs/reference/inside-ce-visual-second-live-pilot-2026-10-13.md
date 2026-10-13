# INSIDE CE visual discovery pilot v2: first recovered archived Reddit image

**Observed:** 2026-10-13. **Source:** successful [GitHub Actions run 38460570791](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38460570791) and its original 30-day GitHub Actions artifact `ce-visual-pilot-v2-38460570791` (artifact **11845551423**). **Scope:** public-source DISCOVER, photographic provenance and retrieval validation, no new physical sticker observations or owner outreach. **Source code:** merged [PR #237](https://github.com/gamesbyian/GRA-EDISNI/pull/237); direct-script CLI remediation [PR #239](https://github.com/gamesbyian/GRA-EDISNI/pull/239).

## Directly recorded results

| Quantity | Value | Interpretation |
|---|---:|---|
| Canonical source-backed original sticker references | 82 | Already SHA-256 verified by visual CI; not 82 newly found stickers. |
| First-party + syndicated 2019 press image controls | 15/15 downloaded | SHA-256 and image-format verified in this run; stored only in Actions artifact, not canonized as separate CE objects. |
| Historical public page fetches | 3/6 worked | iam8bit full CE, iam8bit standalone PS4 and Polygon article worked; three Reddit originals returned explicit HTTP 403. |
| Public Reddit post IDs successfully recovered in Arctic Shift | 3/3 | Public historical **post metadata** available; no claim of complete replies, archived photograph albums or additional ownership proof. |
| Image URLs recovered from those Reddit archival records | 2 | Both resolve to the **same original iam8bit promotional screenshot**, posted in the Dec 2019 CE shipping discussion. |
| Page HTML image-URL *mentions* | 1,800 | Duplicated `srcset`, scaled versions, page chrome and other unrelated assets; not unique photographs or discoveries. |
| Distinct image download URLs accepted | 25/25 | 25 retrieved media files, but multiple filenames can represent one source image. |
| Image comparisons against 82 physical photos + 15 controls | 17 matches | Ten byte-identical matches and seven near-duplicate whole-image matches to promotional or standalone references, **not physical CE owners**. |
| Remaining review-queue records without reference matches | 8 | Individually reviewed below; *zero* newly evidenced owner photos or sticker observations. |

### Recovered public Reddit screenshot (positive acquisition, negative sticker result)

The original 2019 [shipping thread](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/) was HTTP 403 from GitHub-hosted runners. The public Arctic Shift post-ID metadata endpoint returned archive SHA-256 `75993e40185a963b4e184d2b9adebce9282afa27cf988e1802619842b48df8cc` and two resolvable image URLs:

- [Original image](https://i.redd.it/4lrx6eh632441.jpg), **688,273 bytes**, SHA-256 **`cc90d751fb2e2d6efe0b59e66ef09d1fd914a81ae90cb6e3cedd88bc638471cf`**.
- [Reddit preview variant](https://preview.redd.it/4lrx6eh632441.jpg?auto=webp&s=8e1e04b4f86daa92dce18d05b290c8eb53e920eb), **97,888 bytes**, SHA-256 **`ec3a4011981a0dd13d7a5c01a34cb125489994b657cb8a7e0df68498b959d8e0`**.

Both original media files were retrieved, visually opened and compared from the Actions ZIP artifact. They are versions of one identical **screenshot of an iam8bit Instagram-style announcement**, showing a red-and-black INSIDE presentation box with **NOW SHIPPING** in white letters and iam8bit / Playdead / RealDoll branding. Below is publisher post text beginning *“Drum roll please...”* and describing the edition shipping, with social media interface elements. **No numbered sticker is shown, and the screenshot is a publicity repost, not an owner photograph.** In particular, it does not independently evidence any of the known 306/171/125 serial reports in the *comments* on that thread.

This is an important example of a *false positive from a textually relevant owner discussion*. The archive fallback did discover genuine lost-to-direct-scraping image bytes, but the photographed material had no physical sticker. The original URL, archive source and exact SHA are now registered as a **promotional screenshot negative control** in `data/reference/inside-ce-visual-sources.json`.

Other archive results:

- `eers0x`, 2019 owner-display thread: archival metadata SHA-256 `2d6f405ec8e4f36900ede573b4bff0485489c69fff7ec0ebe90970222817fd86`; **no image URL supplied by archived post metadata**. This is not proof that no photo exists in the original thread or its comments.
- `1wruv2d`, 2026 sticker PSA: archival metadata SHA-256 `03041f59b776cd210d88506de523fa3a8136ba4d2a40a69efb23bb06ca536a63`; **no image URL supplied by archived post metadata**. Do not infer photo absence from submission metadata alone.

### Manual visual adjudication of ALL eight unmatched items

All eight unmatched candidate images were recovered from the workflow artifact and visually inspected together as a contact sheet, with the Reddit original separately examined at its native 1024px width. Classification:

| Candidate | Original media source | Visual conclusion |
|---|---|---|
| `000005` | Polygon `ss_3fee4891...jpg` | In-game INSIDE screenshot: outdoor children in dark scene. **No CE or sticker**. |
| `000012` | Reddit `preview.redd.it/4lrx6eh632441.jpg` | iam8bit **NOW SHIPPING** social-media publicity screenshot. No sticker. |
| `000013` | Reddit `i.redd.it/4lrx6eh632441.jpg` | Original-size same publicity screenshot; not a second photo. No sticker. |
| `000016` | Official full CE `InsideCE_Lifestyle_00024.jpg` | First-party promotional spread of concept-art cards. No sticker. |
| `000018` | Standalone iam8bit `playdead_logo_480x480.png` | Playdead logo graphic. No CE or sticker. |
| `000020` | Standalone iam8bit `web_productimage_INSIDE_PS4_05.jpg` | Publisher graphic of PS4 case/disc and Limited Edition label, not full CE. No sticker. |
| `000021` | Standalone iam8bit `web_productimage_INSIDE_PS4_02.jpg` | Standalone PS4 game case, not full CE. No sticker. |
| `000024` | Standalone iam8bit `web_productimage_INSIDE_PS4_04.jpg` | Standalone PS4 game disc, not full CE. No sticker. |

The original social screenshot plus four additional full-CE/standalone publicity photographs have been explicitly added as *reference controls* (20 total controls after this report PR). The logo and in-game shot can remain negative controls by source-page context without needing expensive similarity training.

### What v2 established, and what it cannot establish

- **Real-world confirmed:** complete retrievability of 15 sourced reference photos, accurate marketing matches across re-encoded versions, working Reddit *post-ID archival metadata* lookup and subsequent full-byte media acquisition; asset-key deduplication advanced diversity from 16 repeated size URLs of only two resources to 25 URLs with diverse contents across media classes.
- **Not demonstrated:** any new CE-owning human, any newly printed sticker number, comprehensive Reddit comment/reply acquisition, discovery recall on genuine owner **photo** controls, robustness to arbitrary scene angle and in-frame sticker OCR. An archived subreddit post body is not a complete copy of original comments.
- **Newly established limitation:** screenshot of the iam8bit box in a social post was not recognized as marketing because the context frame surrounds the original media. Keeping the full screenshot as a control will prevent exact future reposts; a future geometric image-within-image detector should be evaluated on **known true positive owner photos** and diverse social screenshots, not inferred from the screenshot alone.
- **Media ownership inference:** reposted promotional screenshots and PS4 standalone product images remain negative even if the source page is within a discussion where actual CE recipients later report numbers. The same Reddit thread can have valuable textual evidence and an unhelpful image.

## Prospective next acquisition lane

Archive-based **comment/reply body and embedded-media URL** retrieval for positive-control threads (2019 shipping, known owner display, 2026 PSA) using explicit post IDs, pagination, original comment IDs/time and opt-in bounded host allowlists. Verify that user-supplied images in comments are not relinked promotional art, and keep posts/comments distinct. If the original comment image is truly lost, preserve failure rather than claiming exhaustive recovery. Beyond Reddit, prioritize old public marketplaces, unboxing images and third-party galleries found through existing multilingual index search. Keep the canonical observation ledger unchanged until original photo or independent owner claim is actually verified.

**Result to send to raezores:** none yet; infrastructure successfully recovers archives, but the newly recovered picture is an official promotional screenshot. Avoid handing it off as a new owner/sticker lead.

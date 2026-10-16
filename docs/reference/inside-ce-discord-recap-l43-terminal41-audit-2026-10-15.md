# Discord sticker-search recap: L43 dot candidates and Terminal41 archive leads

**Date:** 2026-10-15. **Mode:** VALIDATE for exact observation-compatible L43 candidate enumeration; DISCOVER for retrospective archive paths. **Source:** user-supplied 14–15 October 2026 `INSIDE Sticker Search Recap.md`, cross-checked against the current upstream [community sticker register](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md), [ARG chronology](https://github.com/twinysam/INSIDE-ARG), and local `data/observations.csv` at Git blob `2bf9f1352c1632986e5c672b4832848fde1e6d0c`.

**Outcome:** An exact, reproducible conditional candidate inventory and two source-status cautions. **No new number, decipherment, image classification, or previously unseen archive page is confirmed.** Existing physical corpus and model files are unchanged.

## 1. L43, the lost sticker with a dot, is NOT numbered sticker /043

Upstream L43 identifies the Discord user **Dirtwolf**, who provided a photo in which the dot is visible but fingers conceal the serial; the sticker was later lost. L43 is a lost-case *label*, and should not be confused with confirmed numbered sticker **/043**. The original L43 photo is linked from [the canonical register](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md#L43) via a Discord message, but its bytes were **not independently available** in this audit. Therefore its A–I background piece has **not** been classified.

### Exactly what the 261 count assumes

For a **hypothetical** print run of consecutive serials 001 through **597**, assume a single fixed symbol per residue of a 108-periodic foreground, and exclude the 84 already registered serial numbers in the local observation file as separately accounted for. A new unknown number is compatible with L43's dot if its residue currently has a recorded dot **or** has no symbol observation. Residues with a dash or slash observation are excluded. This does **not** impose U2, U5, POS3, one-hot, a learned completion, or a claimed physical production endpoint.

The exhaustive result is **261 remaining serials**. See [machine-readable exact candidates](../../data/reference/inside-ce-l43-dot-candidates-2026-10-15.tsv), sorted by serial. Column `residue_evidence` distinguishes already recorded dots from as-yet-unobserved residues. The artifact does not assert that each candidate is equally probable or that 597 was the actual final print-run serial.

| Background piece | Conditional candidates | Note |
|---|---:|---|
| A | 43 | No dot recorded for this piece in the current corpus |
| B | 15 | |
| C | 15 | No dot recorded |
| D | 35 | |
| E | 31 | |
| F | 22 | No dot recorded |
| G | 43 | |
| H | 30 | |
| I | 27 | |
| **Total** | **261** | |

Thus the recap's **15–43** piece-conditional range reproduces exactly. It mentioned C and F as classes without a known dot; the local corpus also has **no known A dot**. A recovered A/C/F piece would imply at least one dot in a currently unknown residue *under the 108-repeat hypothesis*, but without its serial it would be only an **existential** constraint, not identification of a specific residue. No extra sticker mark should be added to `data/observations.csv` from the class alone.

The **261** figure excludes already listed `427`, as a separately reported sticker, but **does not exclude** another owner's **reported •369**, which is not present in the local CSV. If independently treating •369 as a distinct occupied serial, there are **260**, not 261, candidate numbers; the artifact flags 369. Under a 600 endpoint, the equivalent count is **262** before excluding that separate report. The fact that known residue dots appear in other serial cycles does not make each possible serial an observed dot.

A uniform prior across those 261 *admissible serials*, solely as an illustration (not a production claim), would give 3.083 bits of expected class information and mean posterior candidate-set size 32.36. It is premature to attach probabilities to image classes or serials.

### Evidence-status problem: 427

The upstream community currently places **•427** with **•369** under **reported stickers awaiting images**. The local `data/observations.csv` includes `427,103,.,` among its 84 records while omitting •369. The user-provided owner communication previously corroborates the **dot statement**, but a **sticker photograph** has not been established in this audit. Thus present descriptions of all 84 as *photo-verified physical marks* conflate a reported owner statement with a photograph-based observation. Flag this provenance distinction and audit whichever experiments promote •427 as image-verified physical evidence; **do not unilaterally delete it**, since changing hypotheses/corpus baselines needs source reconciliation. The L43 candidate count itself remains numerically unchanged if 427 is treated as a separately occupied owner-reported serial and its residue is left open to dot.

### Next L43 experiment

Acquire the original L43 Discord image **with permission**, retain original pixels and source/capture metadata; perform rotation/crop/brightness-robust nine-way A–I template registration, with out-of-sample genuine sticker controls, human-blind ranking and confidence threshold; compare the class evidence to this table. If the printed serial is fully occluded there is no legitimate image enhancement that guarantees recovering it.

## 2. Terminal41 sibling directories: unverified archive lead

The Discord recap says a **2020-04** Wayback directory listing for `http://terminal41.link/sys/terminate_terminal/` displays folders `11/`, `23/`, `41/`, `42/`, `99/` with server-displayed **2019-12-16** modification timestamps, and says only `41/` received a captured page. The independently accessible [upstream community chronology](https://github.com/twinysam/INSIDE-ARG) confirms the known `41/terminate.html` and `41/y/` paths were discovered in April 2020, but does **not** independently confirm these four sibling entries or their content.

**Archive replay of the reported parent listing and sibling paths failed in the present browser environment.** Public text-index searches for exact sibling URLs did not produce recoverable archived HTML. This is a failed retrieval, **not** a verified absence or proof of emptiness. Keep the five-directory census as a *reported observation* until the original dated directory-listing HTML, Wayback capture metadata or independent archive witness can be pinned and hashed. Directory listing “Last modified” timestamps are not directory creation times.

Specific passive, bounded follow-ups:
1. Preserve exact Wayback **capture timestamp, original URL, status, MIME and digest** for the listing itself, and recover the HTML once before scaling.
2. Probe explicit literal variants `http://`, `https://`, `www.`, directories with/without trailing slash, and four sibling paths against Wayback CDX, Arquivo.pt and Common Crawl; distinguish provider failure from no capture.
3. Search archived `robots.txt`, `sitemap.xml`, historic site indexes and source-preserved internal links for these path segments, without brute-force crawling a dead site.
4. Compare any recovered sibling content to `41/terminate.html` and `sys/terminateall.html` using byte hashes and UI templates; look for real original content or redirects rather than inferring hidden numbered terminals from folder names.

This route is **independent of** the active [Terminal41 marked-data ECC research PR #208](https://github.com/gamesbyian/GRA-EDISNI/pull/208); avoid competing edits to that work. Original source-native operation, provenance and body availability must precede decoding claims.

## 3. Low-confidence possible contradiction: reported •150

The recap mentions a January 2020 secondhand YouTube comment claiming “other people got .150” but also observes the commenter misstated their own serial. The local source registers **/258** and **/366**, both residue `42` in the 108-repeat, so a physically verified **•150** would contradict a uniform period-108 symbol at that residue. No original direct owner photograph of 150 is supplied; its symbol is **not validated**. Preserve as a low-confidence contradicting claim for future original-source recovery. Do not change residue 42.

## 4. Archive/video/owner discoveries remain source-gated

The recap reports 148 lost/unknown public source links checked in Wayback (75 captures), roughly 2,700 archived tweets from 19 owners, ~2,400 multilingual YouTube candidates, and five small unboxing sticker appearances. These are **author-reported effort and yield**, not datasets examined by this project. The underlying searched URL list, image crop provenance, full video IDs, archive capture timestamps and negative-case denominators are not attached, so importing “all unboxings found” or “no sticker archived” as global facts would be invalid.

The recap identifies [Tom Caswell's Bluesky Huddle post](https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i) as a potential previously unlisted owner. **Ian has already sent this lead to Raezores**; no duplicate outreach from this project. Status remains possible ownership/physical sticker unknown until reconciled with their Discord/owner log. It must not be counted as a new observed sticker.

**Research boundary:** This audit prepares evidence handling and a practical photo experiment; it supplies **zero** new physically identified serials, **zero** independently verified new terminal pages, and no validated decoding model.

# Cover artwork source-audit preservation (2026-10-08)

This directory preserves the **inventory of all recovered/downloaded and derived cover-analysis files** in this conversation, rather than quietly treating transient local files as if they were safely checked into Git.

## Exact original-source references

The original reversible PS4 cover scans are preserved in the upstream GitHub archive (not reproduced in this research branch):

| Side | Archived path | Upstream Git blob SHA |
|---|---|---|
| A | [assets/INSIDE_A-5d197786f158c567.JPG](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/assets/INSIDE_A-5d197786f158c567.JPG) | `875403acac93d83a8acae97e14240c35b88d33ab` |
| B | [assets/INSIDE_B-80fbff1237c37913.JPG](https://github.com/gamesbyian/playdead-unofficial-exports/blob/master/assets/INSIDE_B-80fbff1237c37913.JPG) | `d533d4161f0572b65d134d54f4fa6477029f2d64` |

Metadata captured in earlier work says both source images are **6552 x 5040**. The original bytes are not present in the local ZIP audited here; GitHub's connected text-file reader returns zero data bytes for these particular large binary files, though it returns their SHA identities. Their source repository is the correct place to obtain exact full-resolution originals.

## Local derivative bundle audit

Local conversation workspace in the recovering session: `/mnt/data`.

- The 18,441,492-byte `inside-cover-source-audit.zip` has SHA-256 `ddaef4fe4e9402f9c291e022e315e01508c91a5df3b3f2973f14bbcb4985ee25`. Its 16 members are pixel transformations, downsized overviews, and notes, **not raw 6552x5040 originals**.
- The `cover_artifact/A-overview.jpg` and `B-overview.jpg` derivations are **2200 x 1692**.
- Sixteen ZIP member bytes were compared with same-named extracted files; **no mismatches**.
- Further generated files include a `cover-audit-rawmask.png`, `inside-cover-four-screens-control.png`, frozen `inside-cover-monitor-census.json` and helper/reproduction scripts.
- Two additional 320x246 JPG low-quality preview thumbnails were generated only to allow quick human inspection. They are *derived*, not independent source evidence.
- The 31-record exact size/SHA-256 audit (original 28 local files, plus those two previews and the machine-readable local manifest) is stored in [2026-10-08-local-sha256-manifest.psv](2026-10-08-local-sha256-manifest.psv). The 16 ZIP members also occur by their exact names and hashes in this inventory, under `cover_artifact/`.

**Preservation status: source URLs and cryptographic identities committed; raw 18 MB ZIP and individual binary visualizations remain locally attached artifacts, not GitHub blobs.** Avoid claiming they are Git-versioned. The source-reference strategy follows this repository's `archive/external/README.md` manifest-first policy for large/third-party binary material, and avoids increasing repository weight with duplicate photos. The 18 MB ZIP must be retained outside the repository if future exact reproduction of its transformed outputs is required.

The embedded source link [conversation download bundle](sandbox:/mnt/data/inside-cover-source-audit.zip) is specific to the conversation runtime and not a permanent GitHub source. Do not replace an actual archival URL with a sandbox filename.

## What was actually tested

- Source artwork A has four distinct orange monitor cores inside a manually delimited region; B does not in the same region, under eight tested threshold controls.
- Dataset: `data/original-cover-four-monitor-control-2026-10-08.json`.
- Portable checker: `scripts/audit_inside_cover_monitor_census.py`, accepting the local ZIP filename. This requires `numpy` and `opencv-python`.
- **This image test measures screen counts, not puzzle meaningfulness.** No original source-image registration to canonical acorn/planet assets, artwork transform, A-I index or CE-sticker decoding was achieved.

## Audit reproducibility

With this directory's hash inventory and the recovered local file directory, run:

```sh
python scripts/verify_cover_source_artifact_checksums.py \
    --root /path/to/recovered/mnt/data \
    --manifest archive/external/cover-source-audit/2026-10-08-local-sha256-manifest.psv
```

Missing files fail in full mode. To verify a partial recovered set and skip unavailable files, add `--allow-missing`. ZIP-member verification is built into the script.

## Unresolved binary gap

The user asked for downloaded data to be retained. This pass **does not accomplish byte-for-byte binary ingestion into the Git repository**, because the GitHub connector accepts text/base64 supplied as a tool argument but cannot load arbitrary local binary files directly, and the runtime has no direct GitHub network checkout. The accurate preservation claim is that **the full, exact integrity inventory, original GitHub blob references, and reproduction scripts are saved**. Full binary archival would require an authenticated environment that can transfer local files into Git or its appropriate artifact storage; it should not be declared complete until performed.

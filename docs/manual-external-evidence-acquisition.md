# Manual / Authenticated External Evidence Acquisition

Most public acquisition is handled by `scripts/external_evidence/` and GitHub Actions. The remaining work requires a logged-in human browser or a local machine that can access that browser session.

## Current division of labour

Use automated PR #57 acquisition now for YouTube and publicly extractable X/Instagram/VK sources. Use this manual guide only for sources that genuinely require a logged-in human browser or for refreshing the dedicated YouTube cookie jar. PR #56 owns archival promotion/vendor decisions and is currently active, so do not manually duplicate binary/archive acquisition already being handled there.


## Do not send authentication material to the repository

Do **not** commit, paste into issues, upload to Actions, or send in chat:

- passwords;
- cookie files;
- browser profiles;
- Facebook/Instagram/X session tokens;
- Playwright storage-state files.

Keep any authenticated acquisition local.

## Current human-only priorities

### 1. Facebook groups

Log into Facebook normally and search these groups:

- Limited Printed Games: `https://www.facebook.com/groups/1321230431268681`
- collector group: `https://www.facebook.com/groups/1527275480936152`

Run each of these searches inside each group:

- `INSIDE`
- `Playdead`
- `iam8bit`
- `RealDoll`
- `Huddle`
- `Collector's Edition`

For every potentially relevant result, preserve:

1. the exact post URL;
2. a full-page screenshot showing surrounding thread context;
3. original attached image/video at the highest available resolution;
4. author/display name and visible date;
5. relevant comments/replies;
6. a short note explaining why it may bear on sticker provenance.

Sticker #002 was recovered in the Limited Printed Games group, so prioritize owner photos and old unboxing/arrival posts even when the sticker is not mentioned in text.

Also inspect:

- `https://www.facebook.com/story.php?story_fbid=1422016306591561&id=100063496151489`
- `https://www.facebook.com/share/p/19GJT1NVQS/`

### 2. Instagram sources that reject public extraction

The canonical acquisition target list is `data/external-acquisition-targets.json`.

For any Instagram target that the public workflow classifies as login-required/extractor-broken:

- open it while logged in;
- save each original carousel image/video if the UI permits;
- capture caption and comment context;
- record the exact URL and date;
- do not merely screenshot an image if the original attached media can be saved.

### 3. X/Twitter targets that reject public extraction

For each failed target:

- open the exact status URL while logged in;
- save attached images/video at the highest available quality;
- capture the post plus relevant quoted/reply context;
- record the exact status URL and visible timestamp.

### 4. Oddheader comments

Authenticated automation now reaches the Oddheader metadata/caption/comment surface. Human review has established that the video itself contains no unknown sticker imagery, so do not spend time frame-mining it. Keep the comment stream as an owner-discovery source and capture reports that mention having a Collector's Edition, sticker, serial/number, photo, packaging, or willingness to inspect a copy.

Do not limit review to those keywords if a comment obviously contains new provenance.

## What to hand back to an agent

The easiest useful bundle is a directory or zip containing:

```
source-id/
  README.txt
  screenshot.png
  original-01.jpg
  original-02.jpg
  thread.txt
```

`README.txt` should contain the source URL, visible date/author if useful, and one sentence describing what you saw.

An agent can then hash, catalogue, deduplicate, add provenance metadata, and promote the useful items into the repo.

## Optional local command-line lane

If you already use `yt-dlp` or `gallery-dl` locally, authenticated sources can be attempted with those tools using browser-derived cookies **only on your own machine**. Keep their cookie/profile data outside the repository.

There is no requirement to do this. A normal logged-in browser plus saved originals/screenshots is sufficient for the human-only sources.


## Authenticated YouTube lane

GitHub-hosted runners originally hit YouTube's anti-bot gate for the critical unboxing videos. That path is now working with a dedicated research-only YouTube cookie jar plus yt-dlp's Node/EJS challenge solver. The Google password is not stored or used by the workflow.

### Recommended setup

1. On a computer you control, create or use a dedicated Chrome/Chromium profile.
2. Log into the dedicated research-only YouTube/Google account in that profile.
3. Install current `yt-dlp` locally.
4. From a terminal, run a harmless metadata-only command that both reads browser cookies and writes a standalone cookie jar:

   ```bash
   yt-dlp \
     --cookies-from-browser chrome \
     --cookies youtube-cookies.txt \
     --skip-download \
     "https://www.youtube.com/watch?v=zhCdGdqCIRU"
   ```

   If the dedicated account lives in a non-default Chrome profile, use yt-dlp's browser-profile syntax appropriate to that installation.

5. Confirm `youtube-cookies.txt` exists and is non-empty. Do **not** commit it.

### Local use

Run:

```bash
python scripts/external_evidence/harvest_public.py \
  --source-id youtube-iam8bit-ce-unboxing \
  --youtube-cookies /path/to/youtube-cookies.txt
```

Add `--include-media` when the metadata-only pass succeeds and the original video stream is desired.

The same cookie path may instead be supplied through:

```bash
export YTDLP_COOKIES_FILE=/path/to/youtube-cookies.txt
```

### GitHub Actions use

If authenticated harvesting from GitHub-hosted runners remains acceptable for the dedicated research account, store the cookie jar as a repository Actions secret, never as a tracked file.

On Linux/macOS:

```bash
base64 -w 0 youtube-cookies.txt
```

On systems whose `base64` lacks `-w`:

```bash
base64 < youtube-cookies.txt | tr -d '\n'
```

Create a repository Actions secret named:

`YOUTUBE_COOKIES_B64`

Paste only the resulting base64 text into that secret. The manual `External evidence public harvest` workflow will materialize it into `$RUNNER_TEMP`, chmod it to 0600, point `yt-dlp` at it, and never include that temporary cookie file in the uploaded evidence artifact.

Cookies can expire or be invalidated by Google. If an authenticated run returns `login-required-or-antibot`, refresh the local cookie jar and replace the secret. Current successful runs have reached metadata/comments/subtitles; HTTP 429 after that is a rate-limit issue, not an authentication failure.

### Security boundary

Do not put the account password in:

- GitHub secrets for this workflow;
- command-line arguments;
- workflow inputs;
- issues or PR comments;
- repository files.

Only the temporary cookie jar is needed for automated YouTube acquisition.

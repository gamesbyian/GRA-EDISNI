# Manual / Authenticated External Evidence Acquisition

Most public acquisition is handled by `scripts/external_evidence/` and GitHub Actions. The remaining work requires a logged-in human browser or a local machine that can access that browser session.

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

Public automation should attempt comments first. If YouTube withholds comments from the extractor, manually review the Oddheader September 2026 INSIDE mystery video and capture owner reports that mention having a Collector's Edition, sticker, serial/number, photo, packaging, or willingness to inspect their copy.

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

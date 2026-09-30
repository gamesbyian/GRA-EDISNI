# External asset fetch workflow

The canonical binary manifest at `data/canonical-binary-asset-manifest.json`
contains exact raw GitHub URLs, expected byte sizes, and Git blob SHA-1 values.

Run the **Fetch external ARG assets** workflow manually to download and verify:
- all canonical sticker images;
- Terminal 41 binary media such as the 19.36 MB transmission PNG.

The workflow stores downloads as a GitHub Actions artifact instead of committing
large binaries into repository history.

Examples of useful dispatch settings:

- `category=terminal41-media` to fetch only Terminal 41 media;
- `category=sticker-image` to fetch all sticker images;
- `max_bytes=1000000` for a lightweight pass over files <= 1 MB;
- `limit=10` for a smoke test.

Verification uses the actual Git blob hash formula:

`sha1(b"blob " + decimal_size + b"\\0" + file_bytes)`

so a successful fetch proves the downloaded bytes match the canonical source
blob recorded by GitHub.

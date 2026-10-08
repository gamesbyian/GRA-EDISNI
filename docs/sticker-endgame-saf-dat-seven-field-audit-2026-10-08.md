# The seven-field `saf_dat_col` ASCII island: primary-source correction and consumer audit

_Date: 2026-10-08. Destination-first supplement; observation not a sticker solution._

## Why the file matters

The original historical Terminal 41 mirror contains `terminal41.link/dat/saf_dat_col.html`, a shutdown safety-data collection page exceeding 1.9 MB in its GitHub blob. This is an actual surviving *downstream* ARG artifact, not a guess built by optimizing the stickers.

The previous audit of 72 small HTML files excluded this much larger source. The GitHub blob API can still return its Unicode-decoded textual representation, allowing exact inspection of preserved ASCII fields. Binary corruption/malformed UTF-8 is material: this pass **does not** establish that the original file can be losslessly recovered, nor that the reported 42x42 Sleep BMP has been reproduced.

Source: [twinysam/INSIDE-ARG historical saf_dat_col](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/dat/saf_dat_col.html), Git blob `349b818fce618ef55c404bedfb602b1d03f29a48`.

## Unique long ASCII island

A frozen scan of the decoded 1,265,970-character text for uninterrupted `[A-Za-z0-9+]{35,}` finds **one** match, at Unicode/JS string index 4736, 75 characters long:

```text
gvylmveqwr83409q3i3qpwslie+38546uy754j9j6tuk5fi34+2d34243544+56+567+6+41212
```

Splitting on the six literal `+` characters produces exactly seven fields:

| Field | Length | Preserved text |
| --- | ---: | --- |
| 0 | 26 | `gvylmveqwr83409q3i3qpwslie` |
| 1 | 22 | `38546uy754j9j6tuk5fi34` |
| 2 | 10 | `2d34243544` |
| 3 | 2 | `56` |
| 4 | 3 | `567` |
| 5 | 1 | `6` |
| 6 | 5 | `41212` |

The island is immediately surrounded by visibly corrupted/placeholder source content. It does not itself label which fields are payload, checksum, key or metadata.

The unusual long run and its delimiter grammar are direct facts. **It is not evidence that these seven values are a sticker lookup table without an external correspondence.**

### Specific correction to earlier independent research

The archived independent BigDusty dossier `archive/external/bigdusty/puzzles/viewgate-22char.md` describes the 22-character token as adjacent to a long string with **no visible separator**, and describes the 22-character token as *preceding* `gvylmveqwr...`.

Both details are wrong for the preserved primary source. The literal order is **26-character field, `+`, 22-character field, `+`, five more fields**.

The separately archived BigDusty extracted `block_116` in `archive/external/bigdusty/data/block_descriptions_full.json` also has **one transcription difference**:

```text
preserved: gvylmveqwr83409q3i3qpwslie
archive:   gvylmveqwr83409q3i3qpwsl1e
                                        ^
```

The substitution is source position 24 (zero-indexed), **lowercase i versus digit 1**. This is critical if a future author-provided key operation demands exact bytes or equality: even a single incorrect character can break a cryptographic comparison.

The independent source dossier already knew the larger composite string existed, so the discovery here is **primary-source verification and correction**, not a newly found secret known to no prior researchers.

## Candidate consumers, compatibility and discriminators

### A. Printed 22-position Viewgate field

The two archived `comms_main_viewgate` pages print `Input:[ ... ]` containing exactly **22 underscores** each. The second plus-delimited `saf_dat_col` field contains exactly 22 characters. This is a real cardinality match between independently preserved source surfaces, and a better candidate than fitting arbitrary three-state sticker symbols to a nonexistent HTML form.

But **neither page has a real HTML `<form>`, `<input>`, or `maxlength` attribute**. The original live server may have used an input mechanism lost in the static mirror. Without its request/response or source, the token remains an unvalidated candidate.

### B. Sticker foreground as 108-bit payload packed into 22 characters

Under the physically observed 81/27 binary sector alphabet, the sticker foreground has a **conditional maximum of 108 raw bits**. A standard five-bit-per-character base32 representation of 108 bits would require **22** characters, making the length match arithmetically feasible.

However the actual candidate token does **not** fit RFC 4648 standard Base32, extended-hex Base32 or Crockford Base32 alphabets: it contains numerals 8 and 9, lowercase i/u and y in incompatible combinations. It is compatible with ordinary case-insensitive base36, but that is common among arbitrary alphanumerics and requires a separately supplied conversion convention.

Thus 22 is **capacity compatibility, not evidence of intended sticker encoding**. The seven-field record predates physical sticker solving and the independent input confirmation is absent.

### C. The final field `41212` and the cover clock `12:12`

The physical reversible cover's clock reads `12:12`. The ASCII island ends with `41212`. A conceivable reading is **4 + 12:12**, or another encoding of the displayed time. There is no punctuation, pre-registered parse or operational reason to choose this split rather than thousands of equally possible integer partitions.

The four pre-existing Terminal41 status schemes make `4 + 12:12` rhetorically attractive, but this is **post-hoc** and must not be promoted. Specific next cue needed: original file metadata, message text or cover artifact that explicitly couples a field labeled four to clock time.

### D. Delimited record as independent text-based indexing surface

The seven-field grammar itself offers a more promising and falsifiable approach than brute-force cipher substitution: identify a **source-derived record schema**, then ask what each field addresses and whether the sticker code has a type-correct selector into it. Some fields are decimal, some mixed alphanumeric; the field lengths are highly heterogeneous. No known fixed 9/27/108 lookup keys are present.

The strongest direct negative is therefore that no validated layout or *consumer* presently makes the seven-field string semantically usable.

## Next evidence acquisition

1. Compare the same 75-character island across **independently dated Wayback captures**, if available, to distinguish original intentional data from later mirror assembly/transcoding. Record hash/size and ASCII exactly.
2. Locate source messages or contemporaneous descriptions that identify any of the seven fields or explain why plus signs separate them. Search for the complete **26-character** leading token, not just the previously discussed 22-character substring.
3. Recover an original live screenshot, request/response or archive of the Viewgate form. Printed underscores are not an accepted input control.
4. Reproduce the claimed 42x42 Sleep bitmap from the original source bytes/scripts **before** using its imagery as a sticker consumer. Do not apply arbitrary bit repairs to `534brn...`.
5. Test sticker-derived values only once a field naming/registration rule is independently supplied. Retain the primary-source `i` even if a derivative transcription uses `1`.

## Reproducibility

- Machine-readable fixture: `data/endgame-saf-dat-island-2026-10-08.json`.
- Deterministic standard-library verifier: `python scripts/audit_terminal41_saf_ascii_island.py`.
- Optional whole-source scan: `python scripts/audit_terminal41_saf_ascii_island.py --source /path/to/saf_dat_col.html`.
- The fixture preserves the exact original blob SHA. The verifier checks the source field grammar and archival one-character discrepancy; optional source scanning also tests uniqueness against the original decoded text.

No private data was accessed and no individual was contacted. This is a structural-source correction and additional testable target, **not** a solved code.

## Historical chronology countercheck: Viewgate predates the stickers

The [Game Detectives historical page](https://wiki.gamedetectives.net/w/Inside_ARG) preserves a chronology compiled from contemporaneous source and `Last-Modified` headers. It dates `/comms_main_viewgate.html` to **7 December 2017**, and `/comms_main_viewgate_002.html` to **25 June 2018**. The Collector's Edition sticker distribution began in December **2019**.

Those timestamps are secondary records of old HTTP metadata, not newly retrieved signed server logs, but their direction is decisive for proper framing. The **22-position Viewgate placeholder already existed before the Collector's Edition**. Therefore:

- 22→108-bit packaging does not establish that Viewgate was designed for the CE sticker solution;
- a CE connection would have to be deliberately **retroactive**, such as an earlier dormant interface meant to be unlocked by a later physical release, or reuse of an existing code vocabulary;
- without an independently supplied bridge, prioritizing the candidate as a CE final password just because the lengths fit is weak.

The original 2017–2018 stages did have dynamically accepted phrases on the **separate Playdead website printer endpoint**. No proof requires the static `terminal41.link` Viewgate text to be that interactive endpoint.

The data-island analysis was performed on the later preserved snapshot, so the **75-character string itself is not thereby dated to 2017**. The key chronological fact is the earlier existence of a 22-character *display field*; the island's own historical first appearance remains an acquisition target.

## Execution/verification note

In addition to the GitHub-connector source-wide scan, an **independent Python assertion check** reproduced the 75-character length, exact seven field sizes, unique i/1 discrepancy at character offset 24, and incompatibility of the 22-character token with the three common Base32 alphabets. These assertions passed on the source-island and archive-transcription strings.

The **committed standalone repository verifier** still needs a run from a checkout with the frozen `data/` and `archive/` files. The whole-source optional mode also requires locally acquired original `saf_dat_col.html`; the remote text inspection does not substitute for a binary-forensic reproduction.

## Additional exact capacity rejection: raw binary → ordinary Base36

A syntactic Base36 match is insufficient; the unsigned numeral must also fit the size of the presumed source bits.

The preserved 22-character token parsed as an ordinary positional Base36 integer is:

```text
1552529186059802721063562269367888
```

This requires **111 bits**. A full H108 foreground read as binary under the observed sector alphabets could hold **at most 108 bits**, whose maximum unsigned value is `324518553658426726783156020576255`.

So the **direct unsigned raw-foreground-to-Base36-token hypothesis is mathematically incompatible**, independently of all 42 missing marks. The companion verifier now asserts the 111-bit counterexample.

This test does not reject adding checksums, concatenating data from background/serial information, applying keyed hashes/encryption, or the possibility that the sector alphabets change for missing stickers; those are separate hypotheses with additional premises. Do not choose one to rescue the hypothesis without an external cue.

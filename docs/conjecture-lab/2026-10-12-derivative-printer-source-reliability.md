# Source-critical audit: apparent fourth INSIDE printer password and 22-character form

*12 October 2026. Source archaeology and negative source consistency checks. No decoded CE foreground, newly confirmed passcode or recovered live server is claimed.*

## Why this audit was necessary

A fresh search for original platform-specific printer code led to [BigDusty's INSIDE ARG Investigation Map](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map) and its [printer entry](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/puzzles/printer.md). It reports a **fourth "documented and reproducibly decoded" passcode**:

    HASTYANSWERSETRINGS

The same derivative project also [describes the Terminal41 Viewgate](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/puzzles/viewgate-22char.md) as containing a functional HTML text input with maxlength=22. If either claim were authentic, it could materially change the search for a sticker receiving artifact. This audit compares those assertions to the original archived source and other independently identifiable reports **before** elevating them to a candidate answer or receiver.

## The comparison

| Claim in the derivative map | Independent record | Disposition |
| --- | --- | --- |
| **HASTYANSWERSETRINGS** is a fourth original printer passcode, reproducibly decoded from retail game binaries | [Game Detectives' original ARG solution history](https://wiki.gamedetectives.net/w/Inside_ARG) and [twinysam](https://github.com/twinysam/INSIDE-ARG/blob/master/readme.md) document NEWPLANETDISCOVERED, MULTIPLEPROBESDISPATCHED, LIFEDETECTED as historically accepted Playdead website messages. The [April 2026 claimed code-level retail audit](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) does **not** identify HASTYANSWERSETRINGS. Targeted exact-string public web and GitHub code searches found the string only in files of that same BigDusty map (printer, viewgate and hash research), not in an independent dated acceptance witness, binary dump, output image or original developer testimony. | **Uncorroborated.** Do not add to the validated/accepted password set or use as a 2020 CE key. Search non-detection is not a proof the token never existed. |
| Terminal41 comms_main_viewgate.html contains an HTML input with **maxlength=22** | Direct read of the [archived original page](https://github.com/twinysam/INSIDE-ARG/blob/master/terminal41.link/comms_main_viewgate.html) returns **no HTML input element and no maxlength attribute**. It has ASCII terminal-screen text, including COMMS [req. req.] followed by underscores and an **Input:[ _ _ ... ]** depiction. Earlier [Exp. 476](../experiment-476-receiver-native-geometry-audit.md) likewise explicitly reports no actual input controls in the preserved Terminal41 HTML. | **Contradicted for the archived page.** A printed 22-position *graphic* is not a working input field. Different unpreserved historic page revisions could have existed, but no such revision is supplied by this derivative assertion. |
| The macOS Cutout overlay has **33** dots/letter pulses | [Exp. 476](../experiment-476-receiver-native-geometry-audit.md) counts **34** dot marks across the sixteen source-transcribed Mac strings and **34** letters in HIBERNATIONINPROGRESSREBOOTPENDING (spaces omitted). Original [twinysam's transcript](https://github.com/twinysam/INSIDE-ARG/blob/master/readme.md#macos-printer-codes) is available for an independent recount. | **Arithmetic inconsistent** with this independent recorded 16-strip corpus; don't promote the external 33-count as evidence. |
| "PC (Steam) Mach-O fork (x86-64)" supplies a platform-native decoder | The phrase conflates executable packaging. Mach-O is an Apple executable container, while Windows PC binaries use PE/COFF. The cited [2026 code-level account](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/) describes Mono Assembly-CSharp.dll for PC. No byte-level image/RVA hash is supplied by the map to resolve its claimed PC provenance. | **Source/provenance ambiguity.** A purported offset and port cannot authenticate a decoder without matching binary identity and architecture. |

A caution about the **April 2026 retail-code Reddit audit**: it contains detailed reported class names and platform offsets, including a Switch controller state-machine account and the claim that the Mac Cutout *game binary* lacks an embedded poem decoder. Those are **externally reported decompilation observations**. This project has not independently obtained matching retail binary bytes or replayed all assembly, so this report can motivate an acquisition/disassembly test but cannot prove that Playdead had no separate manually performed text overlay or external printer receiver.

Similarly, the original historical Mac community describes an overlay with the Cummings poem; an executable game engine need not perform an intentionally external paper-and-text operation. The [historical chronology](../inside-arg-historical-chronology.md) should continue to record the community *reported* solution while [Exp. 476](../experiment-476-receiver-native-geometry-audit.md) records the unresolved literal 34-letter reconstruction.

## Consequences for the sticker research program

1. **Do not manufacture a fourth confirmed printer-password receiver** from the BigDusty derivative page. The original Playdead form was a real receiver for three independently supported messages, but an additional fourth CE-era accepted token still requires an authentic response or source code.
2. **Do not treat 22 ASCII underscores as an original HTML maxlength contract.** The preserved Viewgate is a visual terminal simulation and no request body or success logic survives in that page. Searching for a 22-character CE string merely because of this alleged attribute would be circular.
3. **Keep independent original platform implementation leads open.** If the claimed retailer/decompilation material is recovered with hashes, verify native filenames/headers, code offsets, enum branches, call paths and observed paper outputs. Don't multiply conclusions from two derivative pages whose factual claims depend on a single unverified author.
4. **Retain the genuine cross-artifact design pattern.** The validated 2018 Playdead website intake, original printer outputs, 2021 acorn overlay, Xbox image/Braille and actual CE background route remain excellent positive controls even if a fan-written map contains errors.

## Reopening criteria

The fourth-passcode hypothesis can be reopened by **an independently dated accepted printer response**, a matching original binary/string/decoder with hashes, an original developer record or another source unrelated to the suspect derived map. The 22-character HTML-input hypothesis can be reopened by **actual captured HTML/JS** with an input or POST grammar, response witness and source date. An HTML mockup or a length match is not such a witness.

This is a **source reliability negative**, not proof that none of the imagined CE receiving-artifact formats exists. It narrows what we are justified in using as a parameter before decoding the remaining sticker foreground.
